import pandera as pa

CENSUS_COLUMNS = [
    "total_pop",
    "white_pop",
    "black_pop",
    "native_pop",
    "asian_pop",
    "pob_total",
    "pob_native_jeresy",
    "pob_native",
    "pob_foreign_born",
    "edu_total",
    "edu_less_than_hs",
    "edu_hs_degree",
    "edu_some_college",
    "edu_college",
    "edu_grad_degree",
    "lang_only_english",
    "income_total",
    "income_less_10k",
    "income_10k_to_$15k",
    "income_15k_to_$25k",
    "income_25k_to_$35k",
    "income_35k_to_$50k",
    "income_50k_to_$75k",
    "income_75k_to_$100k",
    "income_100k_to_$150k",
    "income_150k_to_$200k",
    "income_200k_to_more",
    "occu_Estimate!!Total:",
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
]

schema = pa.DataFrameSchema(
    {
        **{
            x: pa.Column(pa.Int, checks=[pa.Check.greater_than_or_equal_to(0)])
            for x in CENSUS_COLUMNS
        },
        **{
            "state": pa.Column(
                pa.String, checks=[pa.Check.isin(["34"])]  # Valid state code
            ),
            "county": pa.Column(
                pa.String,
                checks=[pa.Check.str_length(3)],
            ),
            "tract": pa.Column(
                pa.String,
                checks=[pa.Check.str_length(5)],
            ),
        },
    }
)
