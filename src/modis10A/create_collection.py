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

collection.description = collection.description + """

This collection is a limited mirror of the original. It is offered 'as-is', with no guarantees on long term availability.
"""

del collection.assets["geoparquet-items"]
item_assets = collection.extra_fields["item_assets"]

del item_assets["hdf"]
del item_assets["orbit_pnt"]
del item_assets["granule_pnt"]

del collection.extra_fields["msft:group_id"]
del collection.extra_fields["msft:container"]
del collection.extra_fields["msft:storage_account"]
del collection.extra_fields["msft:short_description"]
del collection.extra_fields["msft:region"]

collection.providers.append(pystac.Provider(name="VITO",roles=[pystac.ProviderRole.HOST]))
collection.providers[1].roles = [pystac.ProviderRole.PROCESSOR]


coll_dict = collection.to_dict()

default_auth = {
    "_auth": {
        "read": ["anonymous"],
        "write": ["stac-openeo-admin", "stac-openeo-editor"]
    }
}

coll_dict.update(default_auth)

#requests.delete("https://stac.openeo.vito.be/collections/modis-10A1-061", auth=auth)
#response = requests.post("https://stac.openeo.vito.be/collections", auth=auth,json=coll_dict)
response = requests.put("https://stac.openeo.vito.be/collections/modis-10A1-061", auth=auth,json=coll_dict)
print(response)