import logging
from datetime import datetime, timedelta

from django.contrib.auth import (
    authenticate,
    get_user_model,
    password_validation,
)
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.core.validators import validate_email
from django.template import loader
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters

import jwt

from pfx.pfxcore.apidoc import ModelSchema, Schema, Tag
from pfx.pfxcore.decorator import rest_api, rest_doc, rest_view
from pfx.pfxcore.exceptions import AuthenticationError
from pfx.pfxcore.http import JsonResponse
from pfx.pfxcore.models import CacheableMixin
from pfx.pfxcore.settings import PFXSettings
from pfx.pfxcore.shortcuts import delete_token_cookie

from .rest_views import (
    BaseRestView,
    BodyMixin,
    CreateRestViewMixin,
    ModelMixin,
)

settings = PFXSettings()
logger = logging.getLogger(__name__)
UserModel = get_user_model()
AUTHENTICATION_TAG = Tag("Authentication")


@rest_view("/auth")
class AuthenticationView(ModelMixin, BodyMixin, BaseRestView):
    model = UserModel
    tags = [AUTHENTICATION_TAG]
    token_generator = default_token_generator

    def login_error_response(self):
        raise AuthenticationError()

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    @rest_api(
        "/login", public=True, method="post", priority_doc=0,
        response_schema='login_schema')
    def login(self, *args, **kwargs):
        """Login.
        ---
        post:
            summary: Login
            requestBody:
                content:
                    application/json:
                        schema:
                            properties:
                                username:
                                    type: string
                                password:
                                    type: string
                                    format: password
            parameters:
              - in: query
                name: mode
                schema:
                    type: string
                    enum: ['jwt', 'cookie']
                    default: 'jwt'
        """
        data = self.deserialize_body()
        user = authenticate(self.request, username=data.get('username'),
                            password=data.get('password'))
        if isinstance(user, CacheableMixin):
            user.cache_delete()
        if user is not None:
            mode = self.request.GET.get('mode', 'jwt')
            remember_me = data.get('remember_me', False)
            return self._login_success(user, mode, remember_me)
        return self.login_error_response()

    def _login_success(self, user, mode, remember_me=False):
        token = self._prepare_token(user, remember_me)
        if mode == 'cookie':
            if remember_me:
                expires = datetime.utcnow() + timedelta(
                    **settings.PFX_TOKEN_LONG_VALIDITY)
            else:
                expires = None  # create a session cookie

            res = JsonResponse({
                'user': self.get_user_information(user)
            })
            res.set_cookie(
                'token', token, secure=settings.PFX_COOKIE_SECURE,
                expires=expires, domain=settings.PFX_COOKIE_DOMAIN,
                httponly=True, samesite=settings.PFX_COOKIE_SAMESITE)
            return res
        else:
            return JsonResponse({
                'token': token,
                'user': self.get_user_information(user)
            })

    @method_decorator(never_cache)
    @rest_api(
        "/logout", public=True, method="get", priority_doc=1,
        response_schema='message_schema')
    def logout(self, *args, **kwargs):
        """Logout.
        ---
        get:
            summary: Logout
            description: Delete cookie (for `mode` `'cookie'`).
        """
        return delete_token_cookie(JsonResponse(dict(message="Goodbye")))

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    @rest_api(
        "/change-password", method="post", priority_doc=2,
        response_schema='message_schema')
    def change_password(self, *args, **kwargs):
        """Change password.
        ---
        post:
            summary: Change password
            requestBody:
                content:
                    application/json:
                        schema:
                            properties:
                                old_password:
                                    type: string
                                    format: password
                                new_password:
                                    type: string
                                    format: password
        """
        data = self.deserialize_body()
        user = authenticate(self.request,
                            username=self.request.user.get_username(),
                            password=data.get('old_password'))
        errors = dict()
        try:
            if user is not None and data.get('new_password'):
                password_validation.validate_password(data['new_password'],
                                                      user)
                user.set_password(data.get('new_password'))
                user.save()
                return JsonResponse({
                    'message': _('password updated successfully')
                })
        except ValidationError as e:
            errors['new_password'] = e.error_list
        if not user:
            errors['old_password'] = [_("Incorrect password")]
        if not data.get('new_password'):
            errors.setdefault('new_password', []).append(
                _("Empty password is not allowed"))
        return JsonResponse(
            ValidationError(errors), status=422)

    def _prepare_token(self, user, remember_me):
        if remember_me:
            exp = datetime.utcnow() + timedelta(
                **settings.PFX_TOKEN_LONG_VALIDITY)
        else:
            exp = datetime.utcnow() + timedelta(
                **settings.PFX_TOKEN_SHORT_VALIDITY)
        payload = dict(
            pfx_user_pk=user.pk,
            exp=exp)
        payload.update(self.get_extra_payload(user))
        return jwt.encode(
            payload, settings.PFX_SECRET_KEY, algorithm="HS256")

    def get_extra_payload(self, user):
        return {}

    def get_user_information(self, user):
        return {
            'username': user.get_username(),
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email}

    @classmethod
    def get_user_information_schema(cls):
        return ModelSchema(UserModel, cls._process_fields([
            'username', 'first_name', 'last_name', 'email']))

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    @rest_api(
        "/validate-user-token", public=True, method="post", priority_doc=4,
        response_schema='message_schema')
    def validate_user_token(self, *args, **kwargs):
        """Validate user token.
        ---
        post:
            summary: Validate user token
            requestBody:
                content:
                    application/json:
                        schema:
                            properties:
                                token:
                                    type: string
        """
        data = self.deserialize_body()
        assert 'uidb64' in data and 'token' in data

        user = self.get_user(data['uidb64'])

        if (user is not None and
                self.token_generator.check_token(user, data['token'])):
            return JsonResponse(
                ValidationError(_('User and token are valid')), status=200)
        return JsonResponse(
            ValidationError(_('User or token is invalid')), status=422)

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    @rest_api(
        "/set-password", public=True, method="post", priority_doc=3,
        response_schema='login_or_message_schema')
    def set_password(self, *args, **kwargs):
        """Set password.
        ---
        post:
            summary: Set password
            requestBody:
                content:
                    application/json:
                        schema:
                            properties:
                                token:
                                    type: string
                                password:
                                    type: string
                                    format: password
                                autologin:
                                    type: boolean
        """
        data = self.deserialize_body()
        assert 'uidb64' in data and 'token' in data

        user = self.get_user(data['uidb64'])

        try:
            if (user is not None and data.get('password') and
                    self.token_generator.check_token(user, data['token'])):
                password_validation.validate_password(data['password'], user)
                user.set_password(data['password'])
                user.is_active = True
                user.save()
                if 'autologin' in data and data['autologin'] in (
                        'jwt', 'cookie'):
                    return self._login_success(user, data['autologin'])
                return JsonResponse({
                    'message': _('password updated successfully')
                })
        except ValidationError as e:
            return JsonResponse(
                ValidationError(dict(password=e.error_list)), status=422)

        if not data.get('password'):
            return JsonResponse(
                ValidationError(dict(
                    password=_("Empty password is not allowed"))), status=422)
        raise AuthenticationError()

    def get_user(self, uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist,
                ValidationError):
            user = None
        return user

    @classmethod
    def generate_schemas(cls):
        super().generate_schemas()
        cls.login_schema = Schema("login", "Login", properties=dict(
            token=dict(
                type='string',
                description="Returned only if `mode` is `'jwt'`"),
            user=cls.get_user_information_schema().to_schema()))
        cls.login_or_message_schema = Schema(
            "login_or_message",
            "Login or message (depending autologin parameter)",
            oneOf=[cls.message_schema.id(), cls.login_schema.id()])

    @classmethod
    def get_apidoc_schemas(cls):
        return super().get_apidoc_schemas() + [
            cls.login_schema, cls.login_or_message_schema]


class SendMessageTokenMixin:
    email_template_name = None
    subject_template_name = None
    token_generator = default_token_generator
    extra_email_context = None
    from_email = None
    html_email_template_name = None
    email_field = 'email'
    language_field = 'language'

    def send_token_message(self, user):
        from django.utils import translation
        lang = str(getattr(user, self.language_field, settings.LANGUAGE_CODE))

        token = self.token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        data = {
            'target_user': user,
            'token': token,
            'uid': uid,
            'reset_url': self.reset_url(token, uid),
            'site_name': settings.PFX_SITE_NAME,
            'user': user,
            **(self.extra_email_context or {})
        }
        with translation.override(lang):
            subject = loader.render_to_string(self.subject_template_name, data)
            # Email subject *must not* contain newlines
            subject = ''.join(subject.splitlines())
            body = loader.render_to_string(self.email_template_name, data)
            email_message = EmailMultiAlternatives(
                subject, body, self.from_email,
                [getattr(user, self.email_field)])
            if self.html_email_template_name is not None:
                html_email = loader.render_to_string(
                    self.html_email_template_name, data)
                email_message.attach_alternative(html_email, 'text/html')
            email_message.send()

    def reset_url(self, token, uid):
        return settings.PFX_RESET_PASSWORD_URL.format(
            token=token,
            uid=uid,
        )


@rest_doc("", "post", summary="Signup")
@rest_doc("/meta", "get", summary="Get signup metadata")
@rest_view("/auth/signup")
class SignupView(SendMessageTokenMixin, CreateRestViewMixin, BaseRestView):
    email_template_name = 'registration/welcome_email.txt'
    subject_template_name = 'registration/welcome_subject.txt'
    token_generator = default_token_generator
    extra_email_context = None
    from_email = None
    html_email_template_name = None
    default_public = True
    model = UserModel
    fields = ['first_name', 'last_name', 'username', 'email']
    tags = [AUTHENTICATION_TAG]

    def validate(self, obj, **kwargs):
        obj.set_unusable_password()
        super().validate(obj, **kwargs)

    def is_valid(self, obj, created=True, **kwargs):
        r = super().is_valid(obj, created, **kwargs)
        self.send_token_message(obj)
        return r


@rest_view("/auth")
class ForgottenPasswordView(SendMessageTokenMixin, BodyMixin, BaseRestView):
    email_template_name = 'registration/password_reset_email.txt'
    subject_template_name = 'registration/password_reset_subject.txt'
    token_generator = default_token_generator
    extra_email_context = None
    from_email = None
    html_email_template_name = None
    tags = [AUTHENTICATION_TAG]

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    @rest_api(
        "/forgotten-password", public=True, method="post",
        response_schema='message_schema')
    def forgotten_password(self, *args, **kwargs):
        """Request a link to reset the password.
           Send an e-mail to the provided email address in the post body
           if it exits with a link to change the user password.
        ---
        post:
            summary: Forgotten password
            description: Send an e-mail with a link
                to change the user password.
            requestBody:
                content:
                    application/json:
                        schema:
                            properties:
                                email:
                                    type: string
        """
        data = self.deserialize_body()
        email = data.get('email')
        try:
            validate_email(email)
        except ValidationError as e:
            return JsonResponse(
                ValidationError(dict(email=e.error_list)), status=422)
        if email:
            try:
                user = UserModel._default_manager.get(email=email)
            except UserModel.DoesNotExist:
                user = None
            if user is not None:
                self.send_token_message(user)
        return JsonResponse({
            'message': _('If the email address you entered is correct, '
                         'you will receive an email from us with '
                         'instructions to reset your password.')
        })
