import json
import unittest
from unittest.mock import MagicMock, PropertyMock, patch

import pandas as pd

from centraljersey.data import census


class TestLoad(unittest.TestCase):
    def setUp(self):
        self.load = census.Load(
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

    def test_process(self):
        # Create a sample DataFrame
        df = pd.DataFrame(
            {
                "A": [1, -2, 3, -4],
                "B": [-5, 6, -7, 8],
                "state": ["apple", "banana", "cherry", "durian"],
                "tract": ["123", "456", "789", "012"],
            }
        )

        # Call the process method
        processed_df = self.load.process(df)

        # Assert the expected output
        expected_df = pd.DataFrame(
            {
                "A": [1, 0, 3, 0],
                "B": [0, 6, 0, 8],
                "state": ["apple", "banana", "cherry", "durian"],
                "tract": ["00123", "00456", "00789", "00012"],
            }
        )

        pd.testing.assert_frame_equal(processed_df, expected_df)
