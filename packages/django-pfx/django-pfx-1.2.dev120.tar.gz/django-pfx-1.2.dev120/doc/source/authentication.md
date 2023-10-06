# Authentication

## Modes

There are 2 authentication modes: cookie and bearer token.
You can activate either or both by adding middleware:

* `'pfx.pfxcore.middleware.AuthenticationMiddleware'` (bearer token)
* `'pfx.pfxcore.middleware.CookieAuthenticationMiddleware'` (cookie)

To use the `CookieAuthenticationMiddleware`, you have to configure following settings:

* `PFX_COOKIE_DOMAIN`: the cookie domain
* `PFX_COOKIE_SECURE`: `Secure` attribute of the cookie (`True`/`False`)
* `PFX_COOKIE_SAMESITE`: `SameSite` attribute of the cookie (`'Strict'`/`'Lax'`/`'None'`)
* `PFX_TOKEN_SHORT_VALIDITY`: validity for short validity token (optional, default `{'hours': 12}`)
* `PFX_TOKEN_LONG_VALIDITY`: validity for long validity token (optional, default `{'days': 30}`)

`/auth/login?mode=jwt` will return a token for bearer token authentication.
`/auth/login?mode=cookie` will set and return the authentication cookie.

## Authentication views

The following views provide standard services:

* `AuthenticationView`
  * `/auth/login`
  * `/auth/logout`
  * `/auth/set-password`
  * `/auth/change-password`
  * `/auth/validate-user-token`
* `ForgottenPasswordView`
  * `/auth/forgotten-password`

See the API doc for details.
