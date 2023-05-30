import glob
import json
from functools import cached_property

import geopandas as gpd
import pandas as pd

from centraljersey import preprocess
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
        self.preprocess_tract = preprocess.TractLevelProcessor()
        self.preprocess_cnty = preprocess.CountyLevelProcessor()
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

        df = self.preprocess_tract.append_county(df, self.df_counties)

        df = df.loc[
            df["occu_administrative"].notnull(),
            preprocess.MODEL_COLS + ["label", "geometry"],
        ].reset_index()

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

        df = self.preprocess_cnty.process(
            df=df,
            census=self.census,
            dunkin=self.fsq.df_dunkins_county,
            wawa=self.fsq.df_wawa_county,
        )

        return df
