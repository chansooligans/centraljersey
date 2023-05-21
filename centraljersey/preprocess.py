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
        return df.merge(
            wawa,
            how="left",
            left_on="COUNTYFP",
            right_on="wawa_county",
        )

    def income_cols(self, df):
        df["income_150k+"] = df[["income_150k_to_$200k", "income_200k_to_more"]].sum(
            axis=1
        )
        return df

    def fsq_cols(self, df):
        for col in ["wawa_id", "dunkin_id"]:
            df[col] = (df[col] / df["total_pop"]) * 100_000
        return df

    def nfl_cols(self, df):
        df["giants_or_jets"] = df[["nfl_giants", "nfl_jets"]].sum(axis=1) / df[
            ["nfl_giants", "nfl_jets", "nfl_eagles"]
        ].sum(axis=1)
        return df

    def pork_cols(self, df):
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
