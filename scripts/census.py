# %%
from IPython import get_ipython
if get_ipython() is not None:
    get_ipython().run_line_magic("load_ext", "autoreload")
    get_ipython().run_line_magic("autoreload", "2")
from centraljersey.census import load
census = load.Load()

# %%
df = census.get_df()


# %%
# Retrieve the data for census tracts in New Jersey
nj_data = censusdata.download(
    'acs5', 2019, 
    censusdata.censusgeo([('state', '34'), ('county', '*'), ('tract', '*')]), 
    list(variables.keys())
).rename(variables, axis=1)

# %%
nj_data.to_csv(f"../../data/censustracts.csv", index=False)

# %%
