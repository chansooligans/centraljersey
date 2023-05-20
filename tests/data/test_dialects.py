import unittest
from dataclasses import dataclass

import pandas as pd

from centraljersey.data import dialects

COUNTIES = ["Atlantic", "Burlington", "Camden"]  # Example list of counties for testing


class TestDialects(unittest.TestCase):
    def test_process(self):
        # Create a sample DataFrame for testing
        data = {
            "COUNTY": ["Alantic", "New York"],
            "Column1": [1, 2],
            "Column2": [5, 6],
        }
        df = pd.DataFrame(data)

        # Apply the process function on the DataFrame
        processed_df = dialects.Load.process(df)

        # Define the expected DataFrame after processing
        expected_data = {
            "COUNTY": ["ATLANTIC"],
            "Column1": [1],
            "Column2": [5],
        }
        expected_df = pd.DataFrame(expected_data)

        # Assert that the processed DataFrame matches the expected DataFrame
        pd.testing.assert_frame_equal(processed_df, expected_df)
