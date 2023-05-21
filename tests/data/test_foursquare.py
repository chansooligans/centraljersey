import json
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
import pytest

from centraljersey.data import foursquare


class TestFoursquareDownload:
    @pytest.fixture
    def foursquare(self):
        return foursquare.FoursquareDownload(secrets="")

    @pytest.mark.parametrize(
        "company, expected_chains",
        [
            ("wawa", "7dbc6a56-2391-4a50-b479-8b469beacebc"),
            ("dunkin", "2cb519f8-883c-4263-860a-cd83325fbb97"),
            # Add more test cases here if needed
        ],
    )
    def test_querystring(self, foursquare, company, expected_chains):
        longlat = "40.123,-74.456"

        foursquare.company = company
        query_string = foursquare.querystring(longlat)
        expected_query_string = {
            "chains": expected_chains,
            "ll": "40.123,-74.456",
            "radius": 100_000,
            "limit": 50,
            "sort": "DISTANCE",
        }
        assert query_string == expected_query_string


class TestFoursquareGrouped:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.df_dunkins = pd.DataFrame(
            {
                "dunkin_county": ["A", "A", "B", "B", "B"],
                "dunkin_tract": ["T1", "T2", "T3", "T4", "T4"],
                "dunkin_id": [1, 2, 3, 4, 5],
            }
        )

        self.df_wawas = pd.DataFrame(
            {
                "wawa_county": ["A", "B", "A", "B", "B"],
                "wawa_tract": ["T1", "T2", "T3", "T4", "T4"],
                "wawa_id": [1, 2, 3, 4, 5],
            }
        )

    def test_df_dunkins_tract(self):
        grouped = foursquare.FoursquareGrouped()
        grouped.df_dunkins = self.df_dunkins

        result = grouped.df_dunkins_tract

        assert len(result) == 4  # Number of rows
        assert "dunkin_county" in result.columns
        assert "dunkin_tract" in result.columns
        assert "dunkin_id" in result.columns
        # Add more specific assertions if needed

    def test_df_wawa_tract(self):
        grouped = foursquare.FoursquareGrouped()
        grouped.df_wawas = self.df_wawas

        result = grouped.df_wawa_tract

        assert len(result) == 4  # Number of rows
        assert "wawa_county" in result.columns
        assert "wawa_tract" in result.columns
        assert "wawa_id" in result.columns
        # Add more specific assertions if needed

    def test_df_dunkins_county(self):
        grouped = foursquare.FoursquareGrouped()
        grouped.df_dunkins = self.df_dunkins

        result = grouped.df_dunkins_county

        assert len(result) == 2  # Number of rows
        assert "dunkin_county" in result.columns
        assert "dunkin_id" in result.columns
        # Add more specific assertions if needed

    def test_df_wawa_county(self):
        grouped = foursquare.FoursquareGrouped()
        grouped.df_wawas = self.df_wawas

        result = grouped.df_wawa_county

        assert len(result) == 2  # Number of rows
        assert "wawa_county" in result.columns
        assert "wawa_id" in result.columns
        # Add more specific assertions if needed
