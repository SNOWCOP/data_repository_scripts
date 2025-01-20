from pathlib import Path

import openeo

c = openeo.connect("https://openeo.vito.be").authenticate_oidc()


import json
from shapely.geometry import shape

with open(Path(__file__).parent.parent.parent / "resources" / "senales.geojson") as f:
    data = json.load(f)



aoi = shape(data["features"][0]["geometry"])

cube = c.load_stac("https://stac.openeo.vito.be/collections/modis-10A1-061").filter_spatial(aoi)

result  =cube.validate()
print(result)
cube.execute_batch("modis10.nc")
