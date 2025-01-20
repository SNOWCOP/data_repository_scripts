import nest_asyncio
from pystac_client import Client
import pystac
import planetary_computer
import stac_asset

collection_url = "https://planetarycomputer.microsoft.com/api/stac/v1/collections/modis-10A1-061"

import json
from shapely.geometry import shape
with open("senales.geojson") as f:
    data = json.load(f)


#%%
aoi = shape(data["features"][0]["geometry"])

client = Client.open("https://planetarycomputer.microsoft.com/api/stac/v1",modifier=planetary_computer.sign_inplace)
item_search = client.search(
   collections=["modis-10A1-061"],
   max_items=4,
    datetime="2017/2018",
      intersects=aoi
)
item_collection = item_search.item_collection()


stac_asset.blocking.download_item_collection(item_collection,directory="/data/open/",path_template="${collection}/${year}/${month}/${id}/",config=stac_asset.Config(exclude=["hdf","tilejson","rendered_preview","granule_pnt","orbit_pnt"]))