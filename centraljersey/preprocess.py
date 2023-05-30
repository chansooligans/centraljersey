MODEL_COLS = [
    "dunkin_id",
    "wawa_id",
    "giants_or_jets",
    "pork_roll",
    "calm-no-l",
    "almond-no-l",
    "forward-no-r",
    "drawer",
    "gone-don",
    "white_pop",
    "black_pop",
    "asian_pop",
    "occu_Agricul/fish/mining/forest",
    "occu_Construction",
    "occu_Manufacturing",
    "occu_Wholesale trade",
    "occu_Retail trade",
    "occu_transport/warehouse/utils",
    "occu_Information",
    "occu_finance/insurance/realestate",
    "occu_administrative",
    "occu_educational/healthcare/social",
    "occu_arts/entertainment/foodservices",
    "occu_public administration",
    "occu_management, business",
    "occu_Service occupations:",
    "occu_Sales and office occupations:",
    "occu_Natural resources, construction",
    "occu_production/transport/materials",
    "income_150k+",
    "pob_foreign_born",
    "edu_college",
]

TOTAL_COLS = ["occu_Estimate!!Total:", "income_total", "total_pop", "pob_total"]


class TractLevelProcessor:
    def append_county(self, df, county):
        return df.merge(
            county[
                [
                    "COUNTYFP",
                    "dunkin_id",
                    "wawa_id",
                    "pork_roll",
                    "giants_or_jets",
                    "calm-no-l",
                    "almond-no-l",
                    "forward-no-r",
                    "drawer",
                    "gone-don",
                ]
            ],
            how="left",
        )


class CountyLevelProcessor:
    def get_census_county(self, census):
        return (
            census.groupby(["state", "county"])
            .agg(
                {
                    "total_pop": "sum",
                    "income_150k_to_$200k": "sum",
                    "income_200k_to_more": "sum",
                }
            )
            .reset_index()
        )

    def merge_county(self, df, census):
        return df.merge(
            self.get_census_county(census),
            how="left",
            left_on="COUNTYFP",
            right_on="county",
        )

    def merge_dunkin(self, df, dunkin):
        return df.merge(
            dunkin,
            how="left",
            left_on="COUNTYFP",
            right_on="dunkin_county",
        )

    def merge_wawa(self, df, wawa):
        df = df.merge(
            wawa,
            how="left",
            left_on="COUNTYFP",
            right_on="wawa_county",
        )
        df["wawa_id"] = df["wawa_id"].fillna(0)
        return df

    def income_cols(self, df):
        df["income_150k+"] = df[["income_150k_to_$200k", "income_200k_to_more"]].sum(
            axis=1
        )
        return df

    def fsq_cols(self, df):
        """
        convert to wawas / dunkins per 100k people
        """
        for col in ["wawa_id", "dunkin_id"]:
            df[col] = (df[col] / df["total_pop"]) * 100_000
        return df

    def nfl_cols(self, df):
        """
        percent Giants / Jets fans
        """
        df["giants_or_jets"] = df[["nfl_giants", "nfl_jets"]].sum(axis=1) / df[
            ["nfl_giants", "nfl_jets", "nfl_eagles"]
        ].sum(axis=1)
        return df

    def pork_cols(self, df):
        """
        percent pork roll compared to taylor ham
        """
        df["pork_roll"] = df["pork_pork_roll"] / df[
            ["pork_pork_roll", "pork_taylor_ham"]
        ].sum(axis=1)
        return df

    def process(self, df, census, dunkin, wawa):
        df = self.merge_county(df, census)
        df = self.merge_dunkin(df, dunkin)
        df = self.merge_wawa(df, wawa)
        df = self.income_cols(df)
        df = self.fsq_cols(df)
        df = self.nfl_cols(df)
        df = self.pork_cols(df)
        return df
