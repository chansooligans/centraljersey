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
    "edu_less_than_hs",
    "edu_hs_degree",
    "edu_some_college",
    "edu_college",
    "edu_grad_degree",
    "lang_only_english",
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
    "occu_Construction",
    "occu_Manufacturing",
    "occu_Wholesale trade",
    "occu_Retail trade",
    "occu_Transportation and warehousing, and utilities",
    "occu_Agriculture, forestry, fishing and hunting",
    "occu_Mining, quarrying, and oil and gas extraction",
    "occu_Professional, scientific, and technical services",
    "occu_Management of companies and enterprises",
    "occu_Administrative and support and waste management services",
    "occu_Transportation and warehousing",
    "occu_Utilities",
    "occu_Information",
    "occu_Finance and insurance",
    "occu_Real estate and rental and leasing",
    "occu_Professional, scientific, and management, and administrative, and waste management services",
    "occu_health care and social assistance",
    "occu_Educational services",
    "occu_Health care and social assistance",
    "occu_Arts, entertainment, and recreation",
    "occu_Accommodation and food services",
    "occu_Other services, except public administration",
    "occu_public_administration",
]

schema = pa.DataFrameSchema(
    {
        **{
            x: pa.Column(pa.Int, checks=[pa.Check.greater_than_or_equal_to(0)])
            for x in []
        },
    },
    **{
        "state": pa.Column(
            pa.String, checks=[pa.Check.isin(["34"])]  # Valid state code
        ),
        "county": pa.Column(
            pa.String, checks=[pa.Check.isin(["13"])]  # Valid county code
        ),
        "tract": pa.Column(
            pa.String,
            checks=[
                pa.Check.regex(
                    r"^\d{5}$"
                )  # Pattern for valid tract codes (four digits)
            ],
        ),
    }
)
