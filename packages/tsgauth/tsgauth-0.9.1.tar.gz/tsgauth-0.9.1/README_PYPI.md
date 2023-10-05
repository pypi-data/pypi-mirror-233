# tsgauth

A collection of CERN SSO based authentication and authorisation tools used by the CMS TSG Group

## modules

### flaskoidc

This adds OpenIDC Connect based authorisation for flask servers. It currently has the single function "accept_token"
which decorates any routes you wish to require authorisation for

The function expects the following variables to be added to the flask application

  * OIDC_ISSUER : the issuer of the claims, for cern this is [https://auth.cern.ch/auth/realms/cern](https://auth.docs.cern.ch/user-documentation/oidc/config/)
  * OIDC_JWKS_URI : the uri to obtain the JSON web key set used to obtain the public keys to verify the signature of the received token, for cern this is [https://auth.cern.ch/auth/realms/cern/protocol/openid-connect/certs](https://auth.docs.cern.ch/user-documentation/oidc/config/)
  * OIDC_CLIENT_ID : the client id of the application. This will be used to check that the aud claim contains this client id. 

It will add the decoded claims of the token to flask.g.oidc_token_info if the token can be validiated. If require_token is true, it will only allow access to the endpoint if there is a validiated token, otherwise it will return a 401 and a little britain reference. 

### oidcauth

These are a collection of clients which request and manage a sso token for a given application. Each client is for a different authentication mechansism. We currrently have the following ways of authenticating

ClientAuth : pass in a client id and secret and request a token for a given audience. This is used by applications to access other applications. Basically any script where you dont easily have a user to login with.\

KerbAuth: uses kerberos to login in as user (or service account) and request a token for a given audience

AuthGetSSOTokenAuth: uses the auth-get-sso-token command line tool to request a token for a given audience. Basically wraps the cern authz cli tool in a libary. Note you must install this tool yourself, see [cern authsvc tools](https://gitlab.cern.ch/authzsvc/tools/auth-get-sso-cookie/-/tree/master/) for mode details. 

DeviceAuth: used to log in as a user who uses 2FA or can not get a kerberos ticket for some reason. Will print a url that needs to be copied into the users browser who will then authenticate the request. By default it caches the token in a file in the users home directory (~/.sso_token) which is used for subsequent requests for the next 10 hrs.

The interface of the classes is:

 * token() : returns the access token for a given application, requesting/renewing it first if necessary
 * headers() : returns the headers necessar to pass the token to target api.  eg  requests.get(url,headers=auth.headers())
