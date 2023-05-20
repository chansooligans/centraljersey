from dataclasses import dataclass
from functools import cached_property

import pandas as pd


class Njdotcom:
    @cached_property
    def nfl(self):
        df = pd.read_csv("../data/manually_extracted/nfl.csv").rename(
            {
                "County": "COUNTY",
                "Giants": "nfl_giants",
                "Jets": "nfl_jets",
                "Eagles": "nfl_eagles",
                "Other": "nfl_other",
            },
            axis=1,
        )
        df["COUNTY"] = df["COUNTY"].str.upper()
        return df

    @cached_property
    def pork(self):
        df = pd.read_csv("../data/manually_extracted/pork_ham.csv").rename(
            {
                "County": "COUNTY",
                "Pork Roll": "pork_pork_roll",
                "Taylor Ham": "pork_taylor_ham",
            },
            axis=1,
        )
        df["COUNTY"] = df["COUNTY"].str.upper()
        return df
