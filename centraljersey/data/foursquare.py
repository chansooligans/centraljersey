import glob
import json
import time
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path

import geopandas as gpd
import pandas as pd
import requests
import tqdm

from centraljersey import cache


@dataclass
class CensusCentroids:
    # Load the census tract data for New Jersey
    @cached_property
    def longlats(self):
        df = gpd.read_file("../data/tl_2018_34_tract/tl_2018_34_tract.shp")
        return [
            f"{y},{x}" for x, y in zip(df.geometry.centroid.x, df.geometry.centroid.y)
        ]


@dataclass
class FoursquareDownload(CensusCentroids):
    secrets: dict
    company: str = "wawa"

    @property
    def company_id(self):
        return {
            "wawa": "7dbc6a56-2391-4a50-b479-8b469beacebc",
            "dunkin": "2cb519f8-883c-4263-860a-cd83325fbb97",
        }

    @property
    def headers(self):
        return {
            "Authorization": self.secrets["foursquare"]["api_key"],
            "accept": "application/json",
        }

    def querystring(self, longlat):
        return {
            "chains": self.company_id[self.company],
            "ll": longlat,
            "radius": 100_000,
            "limit": 50,
            "sort": "DISTANCE",
        }

    def query(self, longlat):
        url = "https://api.foursquare.com/v3/places/search"
        response = requests.request(
            "GET", url, headers=self.headers, params=self.querystring(longlat)
        )
        return response.json()

    def fp_out(self, i):
        directory = Path(f"../data/{self.company}/")
        directory.mkdir(parents=True, exist_ok=True)
        return directory / f"{i}.json"

    def save(self):
        for i, x in tqdm.tqdm(enumerate(self.longlats[:2])):
            result = self.query(longlat=x)
            if Path(self.fp_out(i)).exists():
                continue
            else:
                with open(self.fp_out(i), "w") as f:
                    json.dump(result, f)
                time.sleep(0.05)


@dataclass
class FoursquareProcess:
    company: str = "wawa"

    def get_df(self):
        files = glob.glob(f"../data/{self.company}/*.json")
        df_files = []
        for file in files:
            with open(file, "r") as f:
                df_files.append(json.load(f))

        df = pd.DataFrame(
            [
                (
                    res["fsq_id"],
                    res["location"]["census_block"][2:5],
                    res["location"]["census_block"][5:11],
                )
                for f in df_files
                for res in f["results"]
            ],
            columns=[
                f"{self.company}_id",
                f"{self.company}_county",
                f"{self.company}_tract",
            ],
        )
        return df.drop_duplicates(subset=f"{self.company}_id")

    @cached_property
    @cache.localcache(dtype={"dunkin_tract": str, "dunkin_county": str})
    def df_dunkins(self):
        return self.get_df()

    @cached_property
    @cache.localcache(dtype={"wawa_tract": str, "wawa_county": str})
    def df_wawas(self):
        return self.get_df()

    @cached_property
    def df_dunkins_tract(self):
        return (
            self.df_dunkins.groupby(["dunkin_county", "dunkin_tract"])
            .agg({"dunkin_id": "count"})
            .reset_index()
        )

    @cached_property
    def df_wawa_tract(self):
        return (
            self.df_wawas.groupby(["wawa_county", "wawa_tract"])
            .agg({"wawa_id": "count"})
            .reset_index()
        )

    @cached_property
    def df_dunkins_county(self):
        return (
            self.df_dunkins.groupby("dunkin_county")
            .agg({"dunkin_id": "count"})
            .reset_index()
        )

    @cached_property
    def df_wawa_county(self):
        return (
            self.df_wawas.groupby("wawa_county").agg({"wawa_id": "count"}).reset_index()
        )
