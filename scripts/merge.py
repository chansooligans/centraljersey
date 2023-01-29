# %%
import pandas as pd
import glob
import json
import geopandas as gpd

# %%
census = pd.read_csv(f"../../data/censustracts.csv", dtype={"tract":str,"county":str})
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
df = df.merge(nfl).merge(pork)
df = df.merge(census, how='left', left_on = "TRACTCE", right_on="tract")

# %%
df.fillna(0).to_file("../../data/merged_tracts.geojson", driver='GeoJSON')

# %% [markdown]
"""
County level
"""

# %%
# Perform the spatial merge
merged = gpd.sjoin(counties, tracts, how="inner", op="intersects")
df_county = merged.drop_duplicates(subset="TRACTCE")
df_county = df_county[["COUNTY","COUNTYFP","geometry"]].drop_duplicates()
df_county = df_county.merge(nfl).merge(pork)
for col in census.columns:
    if col not in ["tract_name","tract","county"]:
        census[col] = census[col].astype(float)
census_county = census.groupby("county").agg({x:sum for x in census.columns if x not in ["tract_name","tract","county"]}).reset_index()
df_county = df_county.merge(census_county, how='left', left_on = "COUNTYFP", right_on="county")

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
    (res["fsq_id"],res["location"]["census_block"][2:5])
    for dunkinfile in dunkinfiles
    for res in dunkinfile["results"]
], columns=["dunkin_id","dunkin_county"])
df_dunkins = df_dunkins.drop_duplicates(subset="dunkin_id")

df_dunkins = (
    df_dunkins
    .groupby("dunkin_county")
    .agg({
        "dunkin_id":"count"
    })
    .reset_index()
)

df_county = df_county.merge(
    df_dunkins, 
    how="left", 
    left_on="COUNTYFP",
    right_on="dunkin_county"
)


# %%
files = glob.glob("../../data/wawa/*")

wawafiles = []
for file in files:
    with open(file, "r") as f:
        wawafiles.append(json.load(f))

df_wawas = pd.DataFrame([
    (res["fsq_id"],res["location"]["census_block"][2:5])
    for wawafile in wawafiles
    for res in wawafile["results"]
], columns=["wawa_id","wawa_county"])
df_wawas = df_wawas.drop_duplicates(subset="wawa_id")

df_wawas = (
    df_wawas
    .groupby("wawa_county")
    .agg({
        "wawa_id":"count"
    })
    .reset_index()
)

df_county = df_county.merge(
    df_wawas, 
    how="left", 
    left_on="COUNTYFP",
    right_on="wawa_county"
)

# %% [markdown]
"""
Export
"""
# %%
df_county.fillna(0).to_file("../../data/merged_counties.geojson", driver='GeoJSON')

# %%
