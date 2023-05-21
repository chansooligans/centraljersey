import pandera as pa

schema_dunkins_county = pa.DataFrameSchema(
    {
        "dunkin_county": pa.Column(pa.String),
        "dunkin_id": pa.Column(pa.Int64, checks=[pa.Check.greater_than_or_equal_to(0)]),
    }
)

schema_dunkins_tract = pa.DataFrameSchema(
    {
        "dunkin_county": pa.Column(pa.String),
        "dunkin_tract": pa.Column(pa.String),
        "dunkin_id": pa.Column(pa.Int64, checks=[pa.Check.greater_than_or_equal_to(0)]),
    }
)

schema_wawas_county = pa.DataFrameSchema(
    {
        "wawa_county": pa.Column(pa.String),
        "wawa_id": pa.Column(pa.Int64, checks=[pa.Check.greater_than_or_equal_to(0)]),
    }
)

schema_wawas_tract = pa.DataFrameSchema(
    {
        "wawa_county": pa.Column(pa.String),
        "wawa_tract": pa.Column(pa.String),
        "wawa_id": pa.Column(pa.Int64, checks=[pa.Check.greater_than_or_equal_to(0)]),
    }
)
