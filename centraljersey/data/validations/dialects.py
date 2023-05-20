import pandera as pa

schema_gone = pa.DataFrameSchema(
    {
        "COUNTY": pa.Column(pa.String),
        "gone-don": pa.Column(pa.Float, checks=[pa.Check.in_range(0, 100)]),
    }
)

schema_calm = pa.DataFrameSchema(
    {
        "COUNTY": pa.Column(pa.String),
        "calm-don": pa.Column(pa.Float, checks=[pa.Check.in_range(0, 100)]),
    }
)

schema_draw = pa.DataFrameSchema(
    {
        "COUNTY": pa.Column(pa.String),
        "draw-don": pa.Column(pa.Float, checks=[pa.Check.in_range(0, 100)]),
    }
)

schema_forward = pa.DataFrameSchema(
    {
        "COUNTY": pa.Column(pa.String),
        "forward-don": pa.Column(pa.Float, checks=[pa.Check.in_range(0, 100)]),
    }
)
