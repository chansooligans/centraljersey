import pandera as pa

schema_nfl = pa.DataFrameSchema(
    {
        "COUNTY": pa.Column(pa.String),
        "giants_or_jets": pa.Column(pa.Float64, checks=[pa.Check.in_range(0, 100)]),
    }
)

schema_pork = pa.DataFrameSchema(
    {
        "COUNTY": pa.Column(pa.String),
        "pork_roll": pa.Column(pa.Float64, checks=[pa.Check.in_range(0, 100)]),
    }
)
