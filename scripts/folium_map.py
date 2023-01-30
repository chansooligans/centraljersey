# %%
import folium
import pandas as pd
import geopandas as gpd

filename = "../../data/merged_counties.geojson"
with open(filename) as file:
    df = gpd.read_file(file, driver='GeoJSON')    

# %%
for col in df.columns:
    if col not in ["COUNTY","COUNTYFP","total_pop","pob_total","geometry","dunkin_county", "wawa_county"]:
        df[col] = df[col] / df["total_pop"]
    
df["wawa"] = df["wawa_id"] * 100_000
df["dunkin"] = df["dunkin_id"] * 100_000

df["nfl_giants_jets"] = df["nfl_giants"] + df["nfl_jets"]

for col in ["nfl_giants_jets","nfl_eagles"]:
    df[col] = df[col] / df[["nfl_giants_jets","nfl_eagles"]].sum(axis=1)

for col in ["pork_pork_roll","pork_taylor_ham"]:
    df[col] = df[col] / df[["pork_pork_roll","pork_taylor_ham"]].sum(axis=1)

# %%
cols = [
    "wawa",
    "dunkin",
    "nfl_giants_jets",
    "nfl_eagles",
    "pork_pork_roll",
    "pork_taylor_ham",
    "pob_native_jeresy",
    "pob_foreign_born",
    "edu_college"
]

for col in cols:
    figure = folium.Figure()
    m = folium.Map(
        location=[40.133851, -74.871826],
        zoom_start=8,
        tiles='cartodbpositron'
    )
    m.add_to(figure)

    m.choropleth(
    geo_data=df,
    name='Choropleth',
    data=df,
    columns=['COUNTY',col],
    key_on="feature.properties.COUNTY",
    fill_color='YlGnBu',
    fill_opacity=1,
    line_opacity=0.2,
    legend_name=col,
    smooth_factor=0
    )

    m.save(f"../jerseyproj/templates/maps/{col}.html")

# %%
df
# %%
# cp * ../../central_jersey/jerseyproj/templates/maps