import tsgauth
import requests

if __name__ == "__main__":
    #auth = tsgauth.oidcauth.KerbAuth("cms-tsg-frontend-client")
    #r = requests.get("https://hltsupervisor.app.cern.ch/api/v0/thresholds",headers=auth.headers())
    #print(r.text)

    authsession = tsgauth.oidcauth.KerbAuthSession()