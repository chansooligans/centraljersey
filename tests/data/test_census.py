import json
import unittest
from unittest.mock import MagicMock, PropertyMock, patch

import pandas as pd
import pytest

from centraljersey.data import census


class TestLoad:
    @pytest.fixture
    def load(self):
        load = census.Load(
            secrets={"census": {"api_key": "abcde"}},
            variables={
                "B02001_001E": "total_pop",
                "B02001_002E": "white_pop",
                "B02001_003E": "black_pop",
            },
        )
        load.get_response = MagicMock(
            return_value=json.dumps(
                [
                    ["header1", "header2"],
                    ["value1", "value2"],
                ]
            )
        )
        return load

    def test_var_string(self, load):
        expected_var_string = "B02001_001E,B02001_002E,B02001_003E"
        assert load.var_string == expected_var_string

    def test_api_url(self, load):
        expected_url = "https://api.census.gov/data/2020/acs/acs5?get=B02001_001E,B02001_002E,B02001_003E&for=tract:*&in=state:34&key=abcde"
        assert load.api_url == expected_url

    def test_get_df(self, load):
        df = load.get_df()
        expected_df = pd.DataFrame(
            {
                "header1": ["value1"],
                "header2": ["value2"],
            }
        )
        pd.testing.assert_frame_equal(df, expected_df)


class TestProcess:
    @pytest.fixture
    def process(self):
        return census.Process()

    def test_process_numeric(self, process):
        # Create a sample DataFrame
        df = pd.DataFrame(
            {
                "A": ["1", "-2", "3", "-4"],
                "B": [-5, 6, -7, 8],
                "state": ["apple", "banana", "cherry", "durian"],
                "tract": ["123", "456", "789", "012"],
            }
        )

        # Call the process method
        processed_df = process.process_numeric(df)

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

    def test_process_incomes(self, process):
        df = pd.DataFrame(
            {
                "income_150k_to_$200k": [10, 20, 30],
                "income_200k_to_more": [5, 10, 15],
                "pob_foreign_born": [1000, 2000, 3000],
                "total_pop": [10000, 15000, 20000],
                "income_total": [100000, 150000, 200000],
            }
        )

        expected_df = pd.DataFrame(
            {
                "income_150k_to_$200k": [10, 20, 30],
                "income_200k_to_more": [5, 10, 15],
                "pob_foreign_born": [10.0, 13.333333, 15.0],
                "total_pop": [10000, 15000, 20000],
                "income_total": [100000, 150000, 200000],
                "income_150k+": [0.015, 0.02, 0.0225],
            }
        )

        processed_df = process.process_incomes(df)
        pd.testing.assert_frame_equal(processed_df, expected_df)

    def test_process_education(self, process):
        df = pd.DataFrame(
            {
                "edu_college": [2000, 4000, 6000],
                "edu_total": [10000, 15000, 20000],
            }
        )

        expected_df = pd.DataFrame(
            {
                "edu_college": [20.0, 26.666667, 30.0],
                "edu_total": [10000, 15000, 20000],
            }
        )

        processed_df = process.process_education(df)
        pd.testing.assert_frame_equal(processed_df, expected_df)

    def test_process_occupations(self, process):
        df = pd.DataFrame(
            {
                "occu_Estimate!!Total:": [100, 200, 300],
                "occu_Architecture and Engineering Occupations:": [10, 20, 30],
                "occu_Computer and Mathematical Occupations:": [5, 10, 15],
            }
        )

        expected_df = pd.DataFrame(
            {
                "occu_Estimate!!Total:": [100, 200, 300],
                "occu_Architecture and Engineering Occupations:": [10.0, 10.0, 10.0],
                "occu_Computer and Mathematical Occupations:": [5.0, 5.0, 5.0],
            }
        )

        processed_df = process.process_occupations(df)
        pd.testing.assert_frame_equal(processed_df, expected_df)

    def test_process_populations(self, process):
        df = pd.DataFrame(
            {
                "white_pop": [50, 100, 150],
                "black_pop": [20, 40, 60],
                "native_pop": [5, 10, 15],
                "asian_pop": [15, 30, 45],
                "total_pop": [1000, 2000, 3000],
            }
        )

        expected_df = pd.DataFrame(
            {
                "white_pop": [5.0, 5.0, 5.0],
                "black_pop": [2.0, 2.0, 2.0],
                "native_pop": [0.5, 0.5, 0.5],
                "asian_pop": [1.5, 1.5, 1.5],
                "total_pop": [1000, 2000, 3000],
            }
        )

        processed_df = process.process_populations(df)
        pd.testing.assert_frame_equal(processed_df, expected_df)
