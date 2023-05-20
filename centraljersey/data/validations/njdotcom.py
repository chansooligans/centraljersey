import pandera as pa

schema_nfl = pa.DataFrameSchema(
    {
        "COUNTY": pa.Column(pa.String),
        "nfl_giants": pa.Column(pa.Float, checks=[pa.Check.in_range(0, 100)]),
        "nfl_jets": pa.Column(pa.Float, checks=[pa.Check.in_range(0, 100)]),
        "nfl_eagles": pa.Column(pa.Float, checks=[pa.Check.in_range(0, 100)]),
        "nfl_other": pa.Column(pa.Float, checks=[pa.Check.in_range(0, 100)]),
    }
)

schema_pork = pa.DataFrameSchema(
    {
        "COUNTY": pa.Column(pa.String),
        "pork_pork_roll": pa.Column(pa.Float, checks=[pa.Check.in_range(0, 100)]),
        "pork_taylor_ham": pa.Column(pa.Float, checks=[pa.Check.in_range(0, 100)]),
    }
)
