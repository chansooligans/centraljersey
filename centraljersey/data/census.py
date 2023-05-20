import json
from dataclasses import dataclass, field
from functools import cached_property
from typing import Dict

import pandas as pd
import requests

from centraljersey import cache
from centraljersey.config import setup

VARIABLES = {
    "B02001_001E": "total_pop",
    "B02001_002E": "white_pop",
    "B02001_003E": "black_pop",
    "B02001_004E": "native_pop",
    "B02001_005E": "asian_pop",
    "B05002_001E": "pob_total",
    "B05002_003E": "pob_native_jeresy",
    "B05002_002E": "pob_native",
    "B05002_013E": "pob_foreign_born",
    "B06009_002E": "edu_less_than_hs",
    "B06009_003E": "edu_hs_degree",
    "B06009_004E": "edu_some_college",
    "B06009_005E": "edu_college",
    "B06009_006E": "edu_grad_degree",
    "C16001_002E": "lang_only_english",
    "B19001_002E": "income_less_10k",
    "B19001_003E": "income_10k_to_$15k",
    "B19001_004E": "income_15k_to_$25k",
    "B19001_005E": "income_25k_to_$35k",
    "B19001_006E": "income_35k_to_$50k",
    "B19001_007E": "income_50k_to_$75k",
    "B19001_008E": "income_75k_to_$100k",
    "B19001_009E": "income_100k_to_$150k",
    "B19001_010E": "income_150k_to_$200k",
    "B19001_011E": "income_200k_to_more",
    "B24041_005E": "occu_Construction",
    "B24041_006E": "occu_Manufacturing",
    "B24041_007E": "occu_Wholesale trade",
    "B24041_008E": "occu_Retail trade",
    "B24041_009E": "occu_Transportation and warehousing, and utilities",
    "B24041_003E": "occu_Agriculture, forestry, fishing and hunting",
    "B24041_004E": "occu_Mining, quarrying, and oil and gas extraction",
    "B24041_017E": "occu_Professional, scientific, and technical services",
    "B24041_018E": "occu_Management of companies and enterprises",
    "B24041_019E": "occu_Administrative and support and waste management services",
    "B24041_010E": "occu_Transportation and warehousing",
    "B24041_011E": "occu_Utilities",
    "B24041_012E": "occu_Information",
    "B24041_014E": "occu_Finance and insurance",
    "B24041_015E": "occu_Real estate and rental and leasing",
    "B24041_016E": "occu_Professional, scientific, and management, and administrative, and waste management services",
    "B24041_020E": "occu_health care and social assistance",
    "B24041_021E": "occu_Educational services",
    "B24041_022E": "occu_Health care and social assistance",
    "B24041_024E": "occu_Arts, entertainment, and recreation",
    "B24041_025E": "occu_Accommodation and food services",
    "B24041_026E": "occu_Other services, except public administration",
    "B24041_027E": "occu_public_administration",
}


@dataclass
class Load:
    """
    Represents a data loader for census data.

    Attributes:
        secrets (Dict[str, str]): A dictionary containing secrets for accessing the census API.
        variables (Dict[str, str]): A dictionary mapping variable codes to their corresponding names.
        endpoint (str): The API endpoint for the census data.
        state_code (str): The FIPS code for the state.
        tract_code (str): The census tract code.

    Properties:
        var_string (str): Comma-separated string of variable codes.
        api_url (str): The URL for the API request.

    Methods:
        get_response(): Sends an API request and returns the response.
        get_df(): Fetches data from the API and returns it as a DataFrame.
    """

    secrets: Dict[str, str] = field(default_factory=setup)
    variables: Dict[str, str] = field(default_factory=lambda: VARIABLES)
    endpoint: str = "https://api.census.gov/data/2020/acs/acs5"
    state_code: str = "34"  # New Jersey's FIPS code
    tract_code: str = "*"  # All census tracts

    @property
    def var_string(self) -> str:
        """
        Comma-separated string of variable codes.

        Returns:
            str: Comma-separated string of variable codes.
        """
        return ",".join(self.variables.keys())

    @property
    def api_url(self) -> str:
        """
        The URL for the API request.

        Returns:
            str: The URL for the API request.
        """
        return f"{self.endpoint}?get={self.var_string}&for=tract:{self.tract_code}&in=state:{self.state_code}&key={self.secrets['census']['api_key']}"

    def get_response(self) -> requests.Response:
        """
        Sends an API request and returns the response.

        Returns:
            requests.Response: The response from the API request.
        """
        response = requests.get(self.api_url)
        response.raise_for_status()
        return response.content

    def get_df(self) -> pd.DataFrame:
        """
        Fetches data from Census API and returns it as a DataFrame.

        Returns:
            pd.DataFrame: The fetched data as a DataFrame.
        """
        data = json.loads(self.get_response())
        headers = data.pop(0)
        df = pd.DataFrame(data, columns=headers)
        df.rename(columns=self.variables, inplace=True)
        return df

    def process(self, df):
        numeric_columns = df.select_dtypes(include=["int", "float"]).columns
        df[numeric_columns] = df[numeric_columns].mask(df[numeric_columns] < 0, 0)
        df["tract"] = df["tract"].str.zfill(5)
        return df

    @cached_property
    @cache.localcache(dtype={"tract": str, "county": str})
    def nj_data(self) -> pd.DataFrame:
        """
        Cached property to retrieve New Jersey data as a DataFrame.

        Returns:
            pd.DataFrame: The New Jersey data as a DataFrame.
        """
        df = self.get_df()
        return self.process(df)
