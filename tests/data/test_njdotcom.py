import unittest
from functools import cached_property
from pathlib import Path
from unittest.mock import patch

import pandas as pd

from centraljersey.data import njdotcom

nfl = pd.DataFrame(
    {
        "COUNTY": ["atlantic", "bergen", "burlington"],
        "nfl_giants": [14.5, 43.4, 17.4],
        "nfl_jets": [1.7, 35.3, 2.4],
        "nfl_eagles": [79.5, 14.8, 78.8],
        "nfl_other": [4.3, 6.5, 1.5],
    }
)

pork = pd.DataFrame(
    {
        "COUNTY": ["atlantic", "bergen", "burlington"],
        "pork_pork_roll": [23, 0, 40],
        "pork_taylor_ham": [0, 70, 0],
    }
)


class TestNjdotcom(unittest.TestCase):
    def setUp(self):
        self.njdotcom = njdotcom.Njdotcom()

    @patch("pandas.read_csv", return_value=nfl)
    def test_nfl(self, mock_read_csv):

        # Test if the 'nfl' property returns a DataFrame
        self.assertIsInstance(self.njdotcom.nfl, pd.DataFrame)

        # Test if the DataFrame has the expected columns
        expected_columns = [
            "COUNTY",
            "nfl_giants",
            "nfl_jets",
            "nfl_eagles",
            "nfl_other",
        ]
        self.assertListEqual(list(self.njdotcom.nfl.columns), expected_columns)

        # Test if the 'COUNTY' column values are uppercase
        self.assertTrue(all(self.njdotcom.nfl["COUNTY"].str.isupper()))

    @patch("pandas.read_csv", return_value=pork)
    def test_pork(self, mock_read_csv):
        # Test if the 'pork' property returns a DataFrame
        self.assertIsInstance(self.njdotcom.pork, pd.DataFrame)

        # Test if the DataFrame has the expected columns
        expected_columns = [
            "COUNTY",
            "pork_pork_roll",
            "pork_taylor_ham",
        ]
        self.assertListEqual(list(self.njdotcom.pork.columns), expected_columns)

        # Test if the 'COUNTY' column values are uppercase
        self.assertTrue(all(self.njdotcom.pork["COUNTY"].str.isupper()))
