from dataclasses import dataclass
from functools import cached_property

import pandas as pd
from pandera import check_output

from centraljersey.data.validations.njdotcom import schema_nfl, schema_pork


class Njdotcom:
    @cached_property
    @check_output(schema_nfl)
    def nfl(self):
        df = pd.read_csv(
            "/home/chansoo/projects/centraljersey/data/manually_extracted/nfl.csv"
        ).rename(
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
        df["giants_or_jets"] = df[["nfl_giants", "nfl_jets"]].sum(axis=1) / df[
            ["nfl_giants", "nfl_jets", "nfl_eagles"]
        ].sum(axis=1)
        return df

    @cached_property
    @check_output(schema_pork)
    def pork(self):
        df = pd.read_csv(
            "/home/chansoo/projects/centraljersey/data/manually_extracted/pork_ham.csv"
        ).rename(
            {
                "County": "COUNTY",
                "Pork Roll": "pork_pork_roll",
                "Taylor Ham": "pork_taylor_ham",
            },
            axis=1,
        )
        df["COUNTY"] = df["COUNTY"].str.upper()
        df["pork_roll"] = df["pork_pork_roll"] / df[
            ["pork_pork_roll", "pork_taylor_ham"]
        ].sum(axis=1)
        return df
