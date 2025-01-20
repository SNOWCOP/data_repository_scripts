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
#os.environ["OIDC_SOCK"]="/tmp/oidc-agent-service-1000/oidc-agent.sock"
token, issuer, expires_at = agent.get_token_response("terrascope")

auth = BearerAuth(token)

items = pystac.ItemCollection.from_file("/data/open/modis-10A1-061/item-collection.json")

item_map = { i["id"]:i for i in items.to_dict()["features"]}

response = requests.post("https://stac.openeo.vito.be/collections/modis-10A1-061/bulk_items", auth=auth,json={"items":item_map})
print(response)
print(response.json())
