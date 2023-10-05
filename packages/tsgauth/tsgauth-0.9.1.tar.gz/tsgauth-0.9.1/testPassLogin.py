import requests
import bs4
import getpass
import os
import urllib.parse
import sys
if __name__ == "__main__":
    
    session = requests.Session()
    session.headers.update({"User-Agent":"Chrome/103.0.0.0"})
    url = "https://twiki.cern.ch/twiki/bin/viewauth/CMS/HLTOnCallGuide"
    url = "https://gitlab.cern.ch/"
    r = session.get(url)
    soup = bs4.BeautifulSoup(r.text,"html.parser")
    login_form = soup.find(id="kc-form-login")
    if login_form is None:
        print("CERN SSO page not recognized (either its changed or we are not accessing a CERN SSO projected page), exiting")
        sys.exit(0)

    

    request_login_url = login_form["action"]
    parsed_login_url = urllib.parse.urlparse(request_login_url)
    login_params = urllib.parse.parse_qs(parsed_login_url.query)

    button_2fa = soup.find(id="social-mfa")
    url_2fa = button_2fa["href"]

    r_2fa = session.get(f"https://auth.cern.ch/auth/realms/cern/broker/mfa/login",params=login_params)
    soup_2fa = bs4.BeautifulSoup(r_2fa.text,"html.parser")
    login_form = soup_2fa.find(id="kc-form-login")
    request_login_url = login_form["action"]
    parsed_login_url = urllib.parse.urlparse(request_login_url)
    login_params = urllib.parse.parse_qs(parsed_login_url.query)
    


    login_url = "https://auth.cern.ch/auth/realms/mfa/login-actions/authenticate"
    parsed_login_url_woparams = f"{parsed_login_url.scheme}://{parsed_login_url.netloc}{parsed_login_url.path}"
    if parsed_login_url_woparams != login_url:
        print(f"login url {parsed_login_url_woparams} is not the expected cern SSO login url {login_url}, either this page is not protected by the SSO or it is possible somebody is doing something very nasty and trying to steal your password.\nExiting")
        sys.exit(0)

    #password = os.environ["CMSTSG_PASS"]
    password = getpass.getpass()    
    r_login = session.post(login_url,params=login_params,data={"username":"sharper","password":password})
    print(r_login.text)
    soup_login = bs4.BeautifulSoup(r_login.text,"html.parser")
    twofa_form = soup_login.find(id="kc-otp-login-form")
    twofa_params = urllib.parse.parse_qs(urllib.parse.urlparse(twofa_form["action"]).query)
    twofa_url = "https://auth.cern.ch/auth/realms/cern/login-actions/post-broker-login"
    
    print("Please enter your 2fa code")
    twofa_code = input()
    r = session.post(twofa_url,params=twofa_params,data={"otp":twofa_code})
    print(r.text)