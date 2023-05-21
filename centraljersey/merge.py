import glob
import json
from functools import cached_property

import geopandas as gpd
import pandas as pd

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


class Merge:
    def __init__(self):
        self.census = census.Census().nj_data.drop_duplicates(subset="tract_name")

        self.dunkin = foursquare.Foursquare(company="dunkin")
        self.wawa = foursquare.Foursquare(company="wawa")

        self.njdotcom = njdotcom.Njdotcom()

        self.dialects = dialects.Dialects()

        self.tracts = gpd.read_file("../data/tl_2018_34_tract/tl_2018_34_tract.shp")
        self.counties = gpd.read_file(
            "../data/county_boundaries/County_Boundaries_of_NJ.shp"
        ).to_crs("EPSG:4269")

    @cached_property
    def df_tracts(self):
        # Perform the spatial merge

        df = self.tracts.merge(
            self.census,
            how="left",
            left_on=["COUNTYFP", "TRACTCE"],
            right_on=["county", "tract"],
        )
        df = df.loc[df["total_pop"] > 0].reset_index(drop=True)

        df["income_150k+"] = df[["income_150k_to_$200k", "income_200k_to_more"]].sum(
            axis=1
        )

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
            df["tract_name"]
            .str.split(", ")
            .str[1]
            .str.split("County")
            .str[0]
            .str.strip()
        )

        df["label"] = None
        df.loc[df["county_name"].isin(NORTHJERSEY), "label"] = "1"
        df.loc[df["county_name"].isin(SOUTHJERSEY), "label"] = "0"

        return df

    @cached_property
    def df_counties(self):

        df = gpd.sjoin(self.counties, self.tracts, how="inner", op="intersects")
        df["FIPSCO"] = df["FIPSCO"].astype(str).str.zfill(3)
        df = df.loc[
            df["FIPSCO"] == df["COUNTYFP"], ["COUNTY", "COUNTYFP", "geometry"]
        ].drop_duplicates()
        df = (
            df.merge(self.njdotcom.nfl, how="left")
            .merge(self.njdotcom.pork)
            .merge(self.dialects.calm)
            .merge(self.dialects.forward)
            .merge(self.dialects.draw)
            .merge(self.dialects.gone)
        )

        for col in self.census.columns:
            if col not in ["tract_name", "tract", "county"]:
                self.census[col] = self.census[col].astype(float)
        census_county = (
            self.census.groupby("county")
            .agg(
                {
                    x: sum
                    for x in self.census.columns
                    if x not in ["tract_name", "tract", "county"]
                }
            )
            .reset_index()
        )
        df = df.merge(census_county, how="left", left_on="COUNTYFP", right_on="county")

        df = df.merge(
            self.dunkin.df_dunkins_county,
            how="left",
            left_on="COUNTYFP",
            right_on="dunkin_county",
        )

        df = df.merge(
            self.wawa.df_wawa_county,
            how="left",
            left_on="COUNTYFP",
            right_on="wawa_county",
        )

        df["income_150k+"] = df[["income_150k_to_$200k", "income_200k_to_more"]].sum(
            axis=1
        )
        for col in ["wawa_id", "dunkin_id"]:
            df[col] = (df[col] / df["total_pop"]) * 100_000

        df["giants_or_jets"] = df[["nfl_giants", "nfl_jets"]].sum(axis=1) / df[
            ["nfl_giants", "nfl_jets", "nfl_eagles"]
        ].sum(axis=1)
        df["pork_roll"] = df["pork_pork_roll"] / df[
            ["pork_pork_roll", "pork_taylor_ham"]
        ].sum(axis=1)

        return df
