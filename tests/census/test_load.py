import json
import unittest
from unittest.mock import MagicMock, PropertyMock, patch

from centraljersey.census import load


class TestLoad(unittest.TestCase):
    def setUp(self):
        self.load = load.Load(
            secrets={"census": {"api_key": "abcde"}},
            variables={
                "B02001_001E": "total_pop",
                "B02001_002E": "white_pop",
                "B02001_003E": "black_pop",
            },
        )
        self.load.get_response = MagicMock(
            return_value=json.dumps(
                [
                    ["header1", "header2"],
                    ["value1", "value2"],
                ]
            )
        )

    def test_var_string(self):
        expected_var_string = "B02001_001E,B02001_002E,B02001_003E"
        self.assertEqual(self.load.var_string, expected_var_string)

    def test_api_url(self):
        expected_url = "https://api.census.gov/data/2020/acs/acs5?get=B02001_001E,B02001_002E,B02001_003E&for=tract:*&in=state:34&key=abcde"
        self.assertEqual(self.load.api_url, expected_url)

    def test_get_df(self):
        df = self.load.get_df()
        self.assertEqual(df.columns.tolist(), ["header1", "header2"])
        self.assertEqual(df.iloc[0]["header1"], "value1")
        self.assertEqual(df.iloc[0]["header2"], "value2")
