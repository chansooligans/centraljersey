# %%
import geopandas as gpd
import requests
import yaml
import time
import tqdm
import json
import pandas as pd

def query(auth, longlat):
    url = "https://api.foursquare.com/v3/places/search"

    querystring = {
        "chains":"2cb519f8-883c-4263-860a-cd83325fbb97",
        "ll":longlat,
        'radius':100_000,
        "limit":50,
        "sort":"DISTANCE"
    }

    headers = {
        'Authorization': authorization,
        'accept': "application/json"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    return response.json()

# Load the census tract data for New Jersey
tracts = gpd.read_file("../../data/tl_2018_34_tract/tl_2018_34_tract.shp")

# Calculate the centroid of each tract and store in a new column
tracts["centroid"] = tracts.geometry.centroid
centroids = tracts[["centroid"]]
tracts["longlat"] = [
    f"{y},{x}"
    for x,y in 
    zip(tracts.geometry.centroid.x,tracts.geometry.centroid.y)
]
# Access the centroid coordinates for each tract

# %%
with open("../api.yaml", "r") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

authorization = config["authorization"]

# %%
dflist = []
for i,x in tqdm.tqdm(enumerate(tracts["longlat"].values)):
    if i < 122:
        continue
    result = query(
        auth=authorization,
        longlat=x
    )
    with open(f"../../data/dunkin/{i}.json", "w") as f:
        json.dump(result, f)
    # dflist.append(pd.DataFrame(result["results"]))
    # df = pd.concat(dflist).drop_duplicates(subset="fsq_id")
    # df.to_csv(f"../../data/dunkin.csv", index=False)
    time.sleep(0.25)

# %%
