import json
from dataclasses import dataclass, field
from functools import cached_property
from typing import Dict

import pandas as pd
import pandera as pa
import requests
from pandera import check_output

from centraljersey import cache
from centraljersey.config import setup
from centraljersey.data.validations.census import schema

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
    "B06009_001E": "edu_total",
    "B06009_002E": "edu_less_than_hs",
    "B06009_003E": "edu_hs_degree",
    "B06009_004E": "edu_some_college",
    "B06009_005E": "edu_college",
    "B06009_006E": "edu_grad_degree",
    "C16001_002E": "lang_only_english",
    "B19001_001E": "income_total",
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
    "C24050_001E": "occu_Estimate!!Total:",
    "C24050_002E": "occu_Agricul/fish/mining/forest",
    "C24050_003E": "occu_Construction",
    "C24050_004E": "occu_Manufacturing",
    "C24050_005E": "occu_Wholesale trade",
    "C24050_006E": "occu_Retail trade",
    "C24050_007E": "occu_transport/warehouse/utils",
    "C24050_008E": "occu_Information",
    "C24050_009E": "occu_finance/insurance/realestate",
    "C24050_010E": "occu_administrative",
    "C24050_011E": "occu_educational/healthcare/social",
    "C24050_012E": "occu_arts/entertainment/foodservices",
    "C24050_014E": "occu_public administration",
    "C24050_015E": "occu_management, business",
    "C24050_029E": "occu_Service occupations:",
    "C24050_043E": "occu_Sales and office occupations:",
    "C24050_057E": "occu_Natural resources, construction",
    "C24050_071E": "occu_production/transport/materials",
}


class Process:
    def process_incomes(self, df):
        df["income_150k+"] = df[["income_150k_to_$200k", "income_200k_to_more"]].sum(
            axis=1
        )
        df["pob_foreign_born"] = 100 * (df["pob_foreign_born"] / df["total_pop"])
        df["income_150k+"] = 100 * (df["income_150k+"] / df["income_total"])
        return df

    def process_education(self, df):
        df["edu_college"] = 100 * (df["edu_college"] / df["edu_total"])
        return df

    def process_occupations(self, df):
        for col in df.columns:
            if col == "occu_Estimate!!Total:":
                continue
            if col[:5] == "occu_":
                df[col] = 100 * (df[col] / df["occu_Estimate!!Total:"])
        return df

    def process_populations(self, df):
        for col in df.columns:
            if col in ["white_pop", "black_pop", "native_pop", "asian_pop"]:
                df[col] = 100 * (df[col] / df["total_pop"])
        return df

    def process_numeric(self, df):
        numeric_columns = [
            x for x in df.columns if x not in ["state", "county", "tract"]
        ]
        df[numeric_columns] = df[numeric_columns].astype(int)
        df[numeric_columns] = df[numeric_columns].mask(df[numeric_columns] < 0, 0)
        df["tract"] = df["tract"].str.zfill(5)
        return df

    def process(self, df):
        df = self.process_numeric(df)
        df = self.process_incomes(df)
        df = self.process_education(df)
        df = self.process_occupations(df)
        df = self.process_populations(df)
        return df


@dataclass
class Load(Process):
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

    @property
    @cache.localcache(dtype={"tract": str, "county": str, "state": str})
    def censusdata(self) -> pd.DataFrame:
        """
        Cached property to retrieve New Jersey data as a DataFrame.

        Returns:
            pd.DataFrame: The New Jersey data as a DataFrame.
        """
        return self.get_df()

    @cached_property
    def nj_data(self):
        """
        Cached property to retrieve validated dataFrame from cache.

        Returns:
            pd.DataFrame: The New Jersey data as a DataFrame.
        """
        return self.process(schema.validate(self.censusdata))
