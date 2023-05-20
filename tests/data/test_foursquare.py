import json
from dataclasses import dataclass
from pathlib import Path

import pytest

from centraljersey.data import foursquare


class TestFoursquareDownload:
    @pytest.fixture
    def foursquare(self):
        return foursquare.FoursquareDownload()

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
