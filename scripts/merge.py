# %%
from IPython import get_ipython

if get_ipython() is not None:
    get_ipython().run_line_magic("load_ext", "autoreload")
    get_ipython().run_line_magic("autoreload", "2")

# %%
from unittest.mock import Mock

import geopandas as gpd

from centraljersey import config
from centraljersey.data import census, dialects, foursquare, njdotcom

NORTHJERSEY = [
    "Bergen",
    "Essex",
    "Hudson",
    "Morris",
    "Passaic",
    "Sussex",
    "Warren",
    # "Union",
]

SOUTHJERSEY = [
    "Atlantic",
    "Burlington",
    "Camden",
    "Cape May",
    "Cumberland",
    "Gloucester",
    "Salem",
]


self = Mock()
self.census = "some value"
self.census = census.Load().nj_data

self.fsq = foursquare.FoursquareProcess()

self.njdotcom = njdotcom.Njdotcom()

self.dialects = dialects.Load()

self.tracts = gpd.read_file("../data/tl_2018_34_tract/tl_2018_34_tract.shp")
self.counties = gpd.read_file(
    "../data/county_boundaries/County_Boundaries_of_NJ.shp"
).to_crs("EPSG:4269")

# %%
df = self.tracts.merge(
    self.census,
    how="left",
    left_on=["COUNTYFP", "TRACTCE"],
    right_on=["county", "tract"],
)
df = df.loc[df["total_pop"] > 0].reset_index(drop=True)

df["income_150k+"] = df[["income_150k_to_$200k", "income_200k_to_more"]].sum(axis=1)

df["pob_foreign_born"] = 100 * (df["pob_foreign_born"] / df["total_pop"])
df["income_150k+"] = 100 * (df["income_150k+"] / df["income_total"])
df["edu_college"] = 100 * (df["edu_college"] / df["edu_total"])

for col in df.columns:
    if col == "occu_Estimate!!Total:":
        continue
    if col[:5] == "occu_":
        df[col] = 100 * (df[col] / df["occu_Estimate!!Total:"])
    if col in ["white_pop", "black_pop", "native_pop", "asian_pop"]:
        df[col] = 100 * (df[col] / df["total_pop"])

df["county_name"] = (
    df["tract_name"].str.split(", ").str[1].str.split("County").str[0].str.strip()
)

df["label"] = None
df.loc[df["county_name"].isin(NORTHJERSEY), "label"] = "1"
df.loc[df["county_name"].isin(SOUTHJERSEY), "label"] = "0"
