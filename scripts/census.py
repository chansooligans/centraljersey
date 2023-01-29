# %%
import censusdata

# Define the variables to retrieve
variables = { 
    'B02001_001E':'total_pop', 
    'B02001_002E':'white_pop', 
    'B02001_003E':'black_pop', 
    'B02001_004E':'native_pop',
    'B02001_005E':'asian_pop',
    'B05002_001E':'pob_total',
    'B05002_003E':'pob_native_jeresy',
    'B05002_002E':'pob_native',
    'B05002_013E':'pob_foreign_born',
    'B06009_002E':'edu_less_than_hs',
    'B06009_003E':'edu_hs_degree',
    'B06009_004E':'edu_some_college',
    'B06009_005E':'edu_college',
    'B06009_006E':'edu_grad_degree',
    'C16001_002E':'lang_only_english',
    'B19001_002E':'income_less_10k',
    'B19001_003E':'income_10k_to_$15k',
    'B19001_004E':'income_15k_to_$25k',
    'B19001_005E':'income_25k_to_$35k',
    'B19001_006E':'income_35k_to_$50k',
    'B19001_007E':'income_50k_to_$75k',
    'B19001_008E':'income_75k_to_$100k',
    'B19001_009E':'income_100k_to_$150k',
    'B19001_010E':'income_150k_to_$200k',
    'B19001_011E':'income_200k_to_more',
    'B24041_005E':'occu_Construction',
    'B24041_006E':'occu_Manufacturing',
    'B24041_007E':'occu_Wholesale trade',
    'B24041_008E':'occu_Retail trade',
    'B24041_009E':'occu_Transportation and warehousing, and utilities',
    'B24041_003E':'occu_Agriculture, forestry, fishing and hunting',
    'B24041_004E':'occu_Mining, quarrying, and oil and gas extraction',
    'B24041_017E':'occu_Professional, scientific, and technical services',
    'B24041_018E':'occu_Management of companies and enterprises',
    'B24041_019E':'occu_Administrative and support and waste management services',
    'B24041_010E':'occu_Transportation and warehousing',
    'B24041_011E':'occu_Utilities',
    'B24041_012E':'occu_Information',
    'B24041_014E':'occu_Finance and insurance',
    'B24041_015E':'occu_Real estate and rental and leasing',
    'B24041_016E':'occu_Professional, scientific, and management, and administrative, and waste management services',
    'B24041_020E':'occu_health care and social assistance',
    'B24041_021E':'occu_Educational services',
    'B24041_022E':'occu_Health care and social assistance',
    'B24041_024E':'occu_Arts, entertainment, and recreation',
    'B24041_025E':'occu_Accommodation and food services',
    'B24041_026E':'occu_Other services, except public administration',
    'B24041_027E':'occu_public_administration',
}

# Retrieve the data for census tracts in New Jersey
nj_data = censusdata.download(
    'acs5', 2019, 
    censusdata.censusgeo([('state', '34'), ('county', '*'), ('tract', '*')]), 
    list(variables.keys())
).rename(variables, axis=1)

nj_data = nj_data.clip(lower=0).reset_index().rename({"index":"tract_name"}, axis=1)

# %%
nj_data["tract_name"] = [x.params()[2][1] for x in nj_data["tract_name"].values]

# %%
nj_data.to_csv(f"../../data/censustracts.csv", index=False)

# %%
