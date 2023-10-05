import requests
import time
import subprocess
import abc
import requests_gssapi
import bs4 
import urllib 
import uuid
import os
import json
import logging
from getpass import getpass
from authlib.oauth2.rfc7636 import create_s256_code_challenge
from authlib.common.security import generate_token
from authlib.jose import JsonWebKey, jwt
from authlib.oidc.core import ImplicitIDToken, IDToken


"""
This package allows us to retrieve OIDC tokens from the CERN SSO 

It consists of a base class which defines the interface, specifically for the user there are two methods

  token(): returns the access token acquiring it first if necessary
  headers(): returns the necessary headers to make a request to an api which accepts said token

There is also a helper function parse_token which will parse a token into an authlib.oidc.core.IDToken, 
its claims are accessed by ["key"] and can printed directly

It has the ability to store a token for later use in a file, this is most useful for the device auth flow

There are various ways of authenticating which is handled by the specific derived class. There are two main types
application auth: where we log in as an application registered with the CERN SSO
user auth: where we log in as a user (or service account, basically soemthing with cern account)

The authentication methods are as follows:
ClientAuth: application auth, this authenticates using a client id and secret
KerbAuth: user auth, this authenticates using kerberos
AuthGetSSOTokenAuth: user auth, this authenticates using auth-get-sso-token
DeviceAuth: user auth, this authenticates using the device authorization flow

author: Sam Harper (RAL) 2022

"""
def parse_token(token,jwks_url="https://auth.cern.ch/auth/realms/cern/protocol/openid-connect/certs",
                issuer="https://auth.cern.ch/auth/realms/cern",
                client_id=None,validate=True):
    """
    parses a token (optionally validated) into an authlib.oidc.core.IDToken, its claims are accessed by key() and can printed directly

    :param token: the token to parse
    :jwks_url: the url from which to obtain the the json web key sets to verify and decode the token
    :issuer: the issuer of token for validation purposes
    :client_id: the client id this token is for (aud) for validation purposes
    :returns: the parsed token as an authlib.oidc.core.IDToken  
    :rtype: authlib.oidc.core.IDToken  

    """
    def load_key(header, payload):
        jwk_set = requests.get(jwks_url).json()
        return JsonWebKey.import_key(jwk_set["keys"][0], header)

    claims_cls = IDToken
    claims_options = {}
    if issuer:
        claims_options["iss"] = {"values": [issuer]}
    if client_id:
        claims_options["aud"] = {"values": [client_id]}        
    
    claims = jwt.decode(
        token,
        key=load_key,
        claims_cls=claims_cls,
        claims_options=claims_options,
    )   
    if validate:
        claims.validate(leeway=120)     
    return claims




class AuthError(Exception):
    pass 


class AuthBase(abc.ABC): 
    """
    base class for authenticating with the CERN SSO using the oidc standard
    the resulting token is accessable via token() and a helper function headers() supplies the necessary headers
    to pass this to an api request

    child classes are intended to define the _set_token_impl method to actually retrieve the token via a concrete authentication method

    if authentication fails, an AuthError is thrown 

    """
    def __init__(self,client_id,target_client_id=None,hostname="auth.cern.ch",realm="cern",use_token_file=False):        
        """
        does basic setup
        :param hostname: the hostname of the authentication service (default: auth.cern.ch)
        :param realm: the realm of the authentication service (default: cern)
        :param use_token_file: if true, the token is stored in a file and reused if possible        
        """
        
        self.token_response = None
        self.token_iat = None
        self.token_exp = None        
        self.client_id = client_id
        self.target_client_id = target_client_id
        self.hostname = hostname
        self.realm = realm
        self.use_token_file = use_token_file
        self.token_url = f"https://{hostname}/auth/realms/{realm}/protocol/openid-connect/token"
        self.api_access_token_url = f"https://{hostname}/auth/realms/{realm}/api-access/token"
        self.device_auth_url = f"https://{hostname}/auth/realms/{realm}/protocol/openid-connect/auth/device"
        self.auth_url = f"https://{hostname}/auth/realms/{realm}/protocol/openid-connect/auth"
        self.jwks_url = f"https://{hostname}/auth/realms/{realm}/protocol/openid-connect/certs"

    def _refresh_token(self):
        """
        determines if the token needs to be refreshed and if so, refreshes it
        :returns: True if the token is valid or was refreshed, False if the token was not refreshed or is invalid
        """
        current_time = time.time()
        required_remaining_time = 20 #seconds
        token_remaining_time = self.token_exp - current_time if self.token_exp!=None else None
        logging.getLogger("TSGAuth").debug(f"remaining token time {token_remaining_time}")
        if self.token_response:
            if token_remaining_time > required_remaining_time: 
                logging.getLogger("TSGAuth").debug("token still valid")
                return True
            elif self.token_response.get("refresh_token",None)!=None:
                logging.getLogger("TSGAuth").debug("refreshing token")   
                
                r_refresh = requests.post(self.token_url, data={
                    "client_id": self.client_id,
                    "grant_type": "refresh_token",                    
                    "refresh_token": self.token_response["refresh_token"],
                })                
                if "access_token" in r_refresh.json():
                    logging.getLogger("TSGAuth").debug("refreshing token refreshed")   
                    self.token_response = r_refresh.json()                   
                    self._post_update_token()
                    return True
                        
        self.token_response = None
        return False

    def set_token(self):
        """
        if no token or token is expired, it obtains and sets the access token 
        """
        if self.token_response == None and self.use_token_file:
            self.token_response = self.read_token_from_file()
            self._post_update_token(validate=False,write_to_file=False)
            
        if not self._refresh_token():
            self._set_token_impl()
            self._post_update_token()

    def get_token_filename(self):
        token_dir = os.path.expanduser(os.environ.get('CERNSSO_TOKEN_DIR','~/.sso_token'))
        if not os.path.exists(token_dir):
            os.mkdir(token_dir,mode=0o700)
        elif not os.path.isdir(token_dir):
            logging.getLogger("TSGAuth").warning(f"specified directory for token {token_dir} exists and is not a directory")
            return None
        
        token_filename_tag = ""
        if self.target_client_id:
            token_filename_tag = f"_{self.target_client_id}"
        elif self.client_id:
            token_filename_tag = f"_{self.client_id}"

        token_filename = os.path.join(token_dir,f"access_token{token_filename_tag}.json")
        return token_filename
    
    def read_token_from_file(self):
        filename = self.get_token_filename()
        if os.path.exists(filename):
            with open(filename,'r') as f:
                return json.load(f)
        else:
            return None

    def write_token_to_file(self):
        filename = self.get_token_filename()
        if filename!=None and (not os.path.exists(filename) or os.path.isfile(filename)):
            with open(filename,'w') as f:
                json.dump(self.token_response,f)
        else:
            logging.getLogger("TSGAuth").warning(f"error writing token to file {filename}")

    def _post_update_token(self,validate=True,write_to_file=True):
        if self.token_response == None:
            self.token_exp = None
            self.token_iat = None
        else:
            claims = parse_token(self.token_response["access_token"],validate=validate)
            self.token_iat = claims["iat"]
            self.token_exp = claims["exp"]
            if self.use_token_file and write_to_file:
                self.write_token_to_file()


    @abc.abstractmethod
    def _set_token_impl(self):
        """
        derived classes should define this method to set the token_ member to the requested token
        it is assumed the _refresh_token check is already done
        """
        pass

    def headers(self,extra_headers=None):
        """
        returns the necessary headers to pass the token to the api call, throws an AuthError if unable to do so
        :param extra_headers: any extra headers to add to the request, this is a dictionary which is then updated with the Authorization key
        """        
        if extra_headers == None:
            return {'Authorization':'Bearer ' + self.token()}
        else:
            new_headers = dict(extra_headers)
            new_headers.update({'Authorization':'Bearer ' + self.token()})
            return new_headers

    def token(self):
        """
        returns the access token, throws an AuthError if unable to do so
        """
        self.set_token()
        return self.token_response["access_token"]


class ClientAuth(AuthBase): 
    """
    oidc token retriver which takes a client_id, secret and requests a token for a given application (audience)

    """

    def __init__(self,client_id,client_secret,target_client_id=None,audience=None,
                hostname="auth.cern.ch", realm="cern",cert_verify=True):
        """
        :param client_id: id of the client to authenticate as
        :param client_secret: secret of the client to authenticate as
        :param audience: audience of the token, ie the client id of the target api, currently being phased out in favor of target_client_id for homogenity
        :param target_client_id: audience of the token, ie the client id of the target api, replacement for audience, is an error specify both
        :param hostname: the hostname of the authentication service (default: auth.cern.ch)
        :param realm: the realm of the authentication service (default: cern)
        :param cert_verify: verify the certificate of the api_access_token_url
        """
        if audience and target_client_id:
            raise ValueError("cannot specify both audience and target_client_id for ClientAuth, please use just target_client_id")
        if audience:
            print("audience is deprecated, please use target_client_id instead")
            target_client_id = audience

        super().__init__(client_id=client_id,target_client_id=target_client_id,hostname=hostname,realm=realm)        
        self.client_secret = client_secret        
        self.cert_verify = cert_verify
        
    def _set_token_impl(self):
        """
        requests and saves a token from the issuer (eg the CERN SSO service)
        throws an exception AuthError if it was not successful

        :raises AuthError: incase of unsuccessful authentication
        """

        token_req_data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'audience': self.target_client_id
        }
        rep = requests.post(self.api_access_token_url, data=token_req_data, verify=self.cert_verify)
        if rep.status_code!=200 or not "access_token" in rep.json():
            raise AuthError(rep.content.decode())

        self.token_response = rep.json()

class AuthGetSSOTokenAuth(AuthBase):
    """
    oidc token retriver which logs in via kerberos
    using auth-get-sso-token 
    mostly for folks who want to be "official"(ish)
    its a mildy annoying as we dont get full token auth info, just the access token so we refresh it more often than we need
    we guess at the token expiry time of 5mins, may adjust this to zero in the future to avoid issues

    """
    def __init__(self,client_id,redirect_url="http://localhost:8080/",target_client_id=None,hostname="auth.cern.ch",realm="cern",cert_verify=True):
        """
        :param client_id: id of an implicit flow client to authenticate as
        :param redirect_url: a valid redirect_url of the above client
        :param target_client_id: the client_id of the application you wish to exchange your token for (None means no token exchange is required)
        :param token_exchange_url: the url where to exchange tokens at, only required if target_client_id is not None        
        :param cert_verify: verify the certificate of the token exchange url
        """
        super().__init__(client_id=client_id,target_client_id=target_client_id,hostname=hostname,realm=realm)        
        self.redirect_url = redirect_url        
        self.cert_verify = cert_verify
        
    def _set_token_impl(self):
        """
        requests and saves a token from the issuer (eg the CERN SSO service)
        throws an exception AuthError if it was not successful
        """
                
        proc = subprocess.Popen(["auth-get-sso-token", "-u", self.redirect_url, "-c", self.client_id],
                                universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        token, err = proc.communicate()

        if (proc.returncode != 0) or (err != ""):
            raise AuthError(f"""The following error occured while getting SSO token:
                            
                            {err}
                            
                            Common errors are lack of kerberos ticket or perhaps the 
                            program "auth-get-sso-token"  is not installed on your
                            submission machine.""")

        if token.endswith("\n"):
            token = token[:-1]
        
        #see if we need to token swap, if not, we are done
        if not self.target_client_id:
            self.token_response = {"access_token" : token}
            return 
                    
        #now we token swap        
        r = requests.post(
                self.token_url,           
                data={    
                    "client_id" : self.client_id,
                    "grant_type": "urn:ietf:params:oauth:grant-type:token-exchange",                
                    "audience" : self.target_client_id,
                    "subject_token" : token
                },
            )
        if "access_token" in r.json():
            self.token_response = r.json()
            
        else:
            raise AuthError(f"""The following error occured when exchanging the token                            
                            {r.text}                                                        
                            """)

class KerbAuth(AuthBase):
    """
    oidc token retriver which logs in via kerberos

    """
    def __init__(self,client_id,redirect_url="http://localhost:8080/",target_client_id=None,hostname="auth.cern.ch",realm="cern",cert_verify=True):
        """
        :param client_id: id of an implicit flow client to authenticate as
        :param redirect_url: a valid redirect_url of the above client
        :param target_client_id: the client_id of the application you wish to exchange your token for (None means no token exchange is required)
        :param hostname: the hostname of the authentication service (default: auth.cern.ch)
        :param realm: the realm of the authentication service (default: cern)
        :param cert_verify: verify the certificate of the token exchange url
        """
        super().__init__(client_id=client_id,target_client_id=target_client_id,hostname=hostname,realm=realm)        
        self.redirect_url = redirect_url        
        self.cert_verify = cert_verify
    
    @staticmethod   
    def _parse_login_err_msg(text):
        """
        parses the error message from the CERN login page
        code is heavily borrowed from https://gitlab.cern.ch/authzsvc/tools/auth-get-sso-cookie/

        :param text: html text with err msg to parse
        """
        err_page = bs4.BeautifulSoup(text, features="html.parser")
        err_msg= err_page.find(id="kc-error-message")
        if not err_msg:
            return "no error message found, this has sometimes meant you are 2FA user and cant use KerbAuth, try DeviceAuth"            
        else:
            return err_msg.find("p").text


    def _set_token_impl(self):
        """
        requests and saves a token from the issuer (eg the CERN SSO service)
        throws an exception AuthError if it was not successful

        code is heavily borrowed from https://gitlab.cern.ch/authzsvc/tools/auth-get-sso-cookie/
        """
        session = requests.Session()
        random_state = str(uuid.uuid4()).split("-")[0]
        auth_url = f"{self.auth_url}?client_id={self.client_id}&response_type=code&state={random_state}&redirect_uri={self.redirect_url}"        
        #this will return us the log in page which gives us the uris needed to log in , specifically it gives us the session_code for the auth session we have initiated 
        #unfortunately its a webpage so we need to parse the url (really its the session_code in the url we need, everything else is known)
        #I feel there must be an API to do this but so far havent found it
        r_login = session.get(auth_url)
        soup = bs4.BeautifulSoup(r_login.text, features="html.parser")
        kerb_button = soup.find(id="social-kerberos")
        if not kerb_button:
            raise AuthError(f"Issue with the log on page, no kerb option\nstatus code: {r_login.status_code}\nerror msg:{KerbAuth._parse_login_err_msg(r_login.text)}")
        kerb_url = f"https://{self.hostname}{kerb_button.get('href')}"        
        r_kerb = session.get(kerb_url)
        r_auth = session.get(
            r_kerb.url,
            auth=requests_gssapi.HTTPSPNEGOAuth(mutual_authentication=requests_gssapi.OPTIONAL),
            allow_redirects=False,
        )
        
        while r_auth.status_code == 302 and "auth.cern.ch" in r_auth.headers["Location"]:    
            r_auth = session.get(
            r_auth.headers["Location"], allow_redirects=False
            )

        if r_auth.status_code != 302:
            raise AuthError(f"Login failed, error msg {KerbAuth._parse_login_err_msg(r_auth.text)}" )
        auth_params = urllib.parse.parse_qs(r_auth.headers["location"].split("?")[1])
        r_token = requests.post(
            self.token_url,                    
            data={
            "client_id": self.client_id,
            "grant_type": "authorization_code",
            "code": auth_params["code"][0],
            "redirect_uri": self.redirect_url,
            },
        )
        if "access_token" in r_token.json():
            token = r_token.json()
        else:
            raise AuthError(f"""The following error occured when getting the token                            
                            {r_token.text}
                            """)
        
        #see if we need to token swap, if not, we are done
        if not self.target_client_id:
            self.token_response = token
            return 
                    
        #now we token swap        
        r = requests.post(
                self.token_url,           
                data={    
                    "client_id" : self.client_id,
                    "grant_type": "urn:ietf:params:oauth:grant-type:token-exchange",                
                    "audience" : self.target_client_id,
                    "subject_token" : token["access_token"]
                },
            )
        try:        
            self.token_response = r.json()
            
        except KeyError:
            raise AuthError(f"""The following error occured when exchanging the token                            
                            {r.text}                                                        
                            """)


class DeviceAuth(AuthBase):
    """
    gets a token via device authorization flow

    """        
    def __init__(self,client_id,target_client_id=None,use_token_file=True,hostname="auth.cern.ch",realm="cern",cert_verify=True):
        """
        :param client_id: id of an implicit flow client to authenticate as
        :param redirect_url: a valid redirect_url of the above client
        :param target_client_id: the client_id of the application you wish to exchange your token for (None means no token exchange is required)
        :param hostname: the hostname of the authentication service (default: auth.cern.ch)
        :param realm: the realm of the authentication service (default: cern)
        :param cert_verify: verify the certificate of the token exchange url
        """
        super().__init__(client_id=client_id,target_client_id=target_client_id,hostname=hostname,realm=realm,use_token_file=use_token_file)        
        self.cert_verify = cert_verify
    

    def _set_token_impl(self):
        """
        sets the token via the device authorization flow    
        """
        random_state = str(uuid.uuid4()).split("-")[0]
        code_verifier = generate_token(48)
        code_challenge = create_s256_code_challenge(code_verifier)

        r_token_request = requests.post(self.device_auth_url, data={
            "client_id": self.client_id,
            "state" : random_state,
            "code_challenge": code_challenge,
            "code_challenge_method": "S256"
        }, verify=self.cert_verify)

        if r_token_request.status_code != 200:
            raise AuthError(f"Login failed, error msg {r_token_request.text}" )
        
        print("Please visit the following url to authenticate:")
        print(r_token_request.json()["verification_uri_complete"])

        got_token = False
        start_time = time.time()
        while not got_token and time.time() - start_time < 300:
            time.sleep(5)
            r_token = requests.post(self.token_url, data={
                "client_id": self.client_id,
                "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                "device_code": r_token_request.json()["device_code"],
                "code_verifier": code_verifier
            }, verify=self.cert_verify)
            if r_token.status_code == 200:
                got_token = True
        if not got_token:
            raise AuthError(f"Login failed timed out after 5mins, last message:\n{r_token.text}" )
        if "access_token" in r_token.json():
            self.token_response = r_token.json()
        else:
            raise AuthError(f"Login failed, error msg {r_token.text}" )
        
        