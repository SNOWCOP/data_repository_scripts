import pystac
import requests
import liboidcagent as agent
import os

class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r

#oidc-gen --pub terrascope --flow=device --client-id=public --iss=https://sso.terrascope.be/auth/realms/terrascope
os.environ["OIDC_SOCK"]="/tmp/oidc-agent-service-1000/oidc-agent.sock"
token, issuer, expires_at = agent.get_token_response("terrascope")

auth = BearerAuth(token)


collection = pystac.Collection.from_file("https://planetarycomputer.microsoft.com/api/stac/v1/collections/modis-10A1-061")

coll_dict = collection.to_dict()

default_auth = {
    "_auth": {
        "read": ["anonymous"],
        "write": ["stac-openeo-admin", "stac-openeo-editor"]
    }
}

coll_dict.update(default_auth)

response = requests.post("https://stac.openeo.vito.be/collections", auth=auth,json=coll_dict)