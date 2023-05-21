import glob
import json
from functools import cached_property

import geopandas as gpd
import pandas as pd

from centraljersey.data import census, dialects, foursquare, njdotcom

NORTHJERSEY = [
    "003",  # "Bergen",
    "013",  # "Essex",
    "017",  # "Hudson",
    "027",  # "Morris",
    "031",  # "Passaic",
    "037",  # "Sussex",
    "041",  # "Warren",
    # include? "Union",
]

SOUTHJERSEY = [
    "001",  # "Atlantic",
    "005",  # "Burlington",
    "007",  # "Camden",
    "009",  # "Cape May",
    "011",  # "Cumberland",
    "015",  # "Gloucester",
    "033",  # "Salem",
]


class Merge:
    def __init__(self):
        self.census = census.Load().nj_data

        self.fsq = foursquare.FoursquareProcess()

        self.njdotcom = njdotcom.Njdotcom()

        self.dialects = dialects.Load()

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

        df["label"] = None
        df.loc[df["COUNTYFP"].isin(NORTHJERSEY), "label"] = "1"
        df.loc[df["COUNTYFP"].isin(SOUTHJERSEY), "label"] = "0"

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
