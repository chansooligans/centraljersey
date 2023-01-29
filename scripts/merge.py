# %%
import pandas as pd
import glob
import json
import geopandas as gpd

# %%
census = pd.read_csv(f"../../data/censustracts.csv", dtype={"tract_name":str})
census = census.drop_duplicates(subset="tract_name")
nfl = (
    pd.read_csv(f"../../data/nfl.csv")
    .rename({
        "County":"COUNTY",
        "Giants":"nfl_giants",
        "Jets":"nfl_jets",
        "Eagles":"nfl_eagles",
        "Other":"nfl_other"
    }, axis=1)
)
nfl["COUNTY"] = nfl["COUNTY"].str.upper()
pork = (
    pd.read_csv(f"../../data/pork_ham.csv")
    .rename({
        "County":"COUNTY",
        "Pork Roll":"pork_pork_roll",
        "Taylor Ham":"pork_taylor_ham",
    }, axis=1)
)
pork["COUNTY"] = pork["COUNTY"].str.upper()

# %%
tracts = gpd.read_file("../../data/tl_2018_34_tract/tl_2018_34_tract.shp")
counties = gpd.read_file("../../data/county_boundaries/County_Boundaries_of_NJ.shp")
counties = counties.to_crs("EPSG:4269")

# Perform the spatial merge
merged = gpd.sjoin(tracts, counties, how="inner", op="intersects")
df = merged.drop_duplicates(subset="TRACTCE")

# %%
census
df = df.merge(nfl).merge(pork)
df = df.merge(census, how='left', left_on = "TRACTCE", right_on="tract_name")

# %%
df

# %% [markdown]
"""
Dunkin / Wawa
"""

# %%
files = glob.glob("../../data/dunkin/*")

dunkinfiles = []
for file in files:
    with open(file, "r") as f:
        dunkinfiles.append(json.load(f))

df_dunkins = pd.DataFrame([
    (res["fsq_id"],res["location"]["census_block"][:-4])
    for dunkinfile in dunkinfiles
    for res in dunkinfile["results"]
], columns=["dunkin_id","dunkin_censusblock"])
df_dunkins = df_dunkins.drop_duplicates(subset="dunkin_id")

df_dunkins = (
    df_dunkins
    .groupby("dunkin_censusblock")
    .agg({
        "dunkin_id":"count"
    })
    .reset_index()
)

df = df.merge(
    df_dunkins, 
    how="left", 
    left_on="GEOID",
    right_on="dunkin_censusblock"
)


# %%
files = glob.glob("../../data/wawa/*")

wawafiles = []
for file in files:
    with open(file, "r") as f:
        wawafiles.append(json.load(f))

df_wawas = pd.DataFrame([
    (res["fsq_id"],res["location"]["census_block"][:-4])
    for wawafile in wawafiles
    for res in wawafile["results"]
], columns=["wawa_id","wawa_censusblock"])
df_wawas = df_wawas.drop_duplicates(subset="wawa_id")

df_wawas = (
    df_wawas
    .groupby("wawa_censusblock")
    .agg({
        "wawa_id":"count"
    })
    .reset_index()
)

df = df.merge(
    df_wawas, 
    how="left", 
    left_on="GEOID",
    right_on="wawa_censusblock"
)

# %% [markdown]
"""
Export
"""
# %%
df = df.fillna(0)

# %%
df.to_csv("../../data/merged.csv", index=False)
# %%
