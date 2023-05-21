import glob
import json
import time
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import List

import geopandas as gpd
import pandas as pd
import requests
import tqdm

from centraljersey import cache


@dataclass
class CensusCentroids:
    """
    A class for handling census tract shapefiles for New Jersey.
    """

    @cached_property
    def longlats(self) -> List[str]:
        """
        Returns a list of centroid coordinates (latitude, longitude) for census tracts in New Jersey.

        Returns:
            List[str]: A list of centroid coordinates in the format "latitude,longitude".
        """
        df = gpd.read_file("../data/tl_2018_34_tract/tl_2018_34_tract.shp")
        return [
            f"{y},{x}" for x, y in zip(df.geometry.centroid.x, df.geometry.centroid.y)
        ]


@dataclass
class FoursquareDownload(CensusCentroids):
    """
    A class for downloading Foursquare data based on census tract centroids.
    """

    secrets: dict
    company: str = "wawa"

    @property
    def company_id(self) -> dict:
        """
        Returns a dictionary mapping company names to their Foursquare IDs.

        Returns:
            dict: A dictionary mapping company names to their Foursquare IDs.
        """
        return {
            "wawa": "7dbc6a56-2391-4a50-b479-8b469beacebc",
            "dunkin": "2cb519f8-883c-4263-860a-cd83325fbb97",
        }

    @property
    def headers(self) -> dict:
        """
        Returns the headers for the Foursquare API request.

        Returns:
            dict: The headers for the Foursquare API request.
        """
        return {
            "Authorization": self.secrets["foursquare"]["api_key"],
            "accept": "application/json",
        }

    def querystring(self, longlat: str) -> dict:
        """
        Constructs the query string parameters for the Foursquare API request.

        Args:
            longlat (str): The centroid coordinates in the format "latitude,longitude".

        Returns:
            dict: The query string parameters for the Foursquare API request.
        """
        return {
            "chains": self.company_id[self.company],
            "ll": longlat,
            "radius": 100_000,
            "limit": 50,
            "sort": "DISTANCE",
        }

    def query(self, longlat: str) -> dict:
        """
        Sends a GET request to the Foursquare API and retrieves the response as JSON.

        Args:
            longlat (str): The centroid coordinates in the format "latitude,longitude".

        Returns:
            dict: The JSON response from the Foursquare API.
        """
        url = "https://api.foursquare.com/v3/places/search"
        response = requests.request(
            "GET", url, headers=self.headers, params=self.querystring(longlat)
        )
        return response.json()

    def fp_out(self, i: int) -> Path:
        """
        Returns the file path for saving the Foursquare data.

        Args:
            i (int): The index of the data.

        Returns:
            Path: The file path for saving the Foursquare data.
        """
        directory = Path(f"../data/{self.company}/")
        directory.mkdir(parents=True, exist_ok=True)
        return directory / f"{i}.json"

    def save(self):
        """
        Saves the Foursquare data for each centroid coordinate.
        This method queries the Foursquare API for each centroid coordinate and saves the response as JSON.
        The data is saved in separate files named "{i}.json" in the corresponding company directory.

        Returns:
            None
        """
        for i, x in tqdm.tqdm(enumerate(self.longlats)):
            result = self.query(longlat=x)
            if Path(self.fp_out(i)).exists():
                continue
            else:
                with open(self.fp_out(i), "w") as f:
                    json.dump(result, f)
                time.sleep(0.05)


class FoursquareGrouped:
    df_dunkins: pd.DataFrame
    df_wawas: pd.DataFrame

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


class FoursquareProcess(FoursquareGrouped):
    def get_df(self, company):
        files = glob.glob(f"../data/{company}/*.json")
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
                    res["chains"][0]["name"],
                )
                for f in df_files
                for res in f["results"]
            ],
            columns=[
                f"{company}_id",
                f"{company}_county",
                f"{company}_tract",
                "fsq_name",
            ],
        )
        return df.drop_duplicates(subset=f"{company}_id")

    @cached_property
    @cache.localcache(dtype={"dunkin_tract": str, "dunkin_county": str})
    def df_dunkins(self):
        return self.get_df(company="dunkin")

    @cached_property
    @cache.localcache(dtype={"wawa_tract": str, "wawa_county": str})
    def df_wawas(self):
        return self.get_df(company="wawa")
