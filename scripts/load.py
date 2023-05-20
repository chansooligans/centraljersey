# %%
from IPython import get_ipython
if get_ipython() is not None:
    get_ipython().run_line_magic("load_ext", "autoreload")
    get_ipython().run_line_magic("autoreload", "2")
from centraljersey.census import load as censusload
from pathlib import Path

# %%
fp_out = Path.cwd().parent

# %%
census = censusload.Load(
    fp_out = fp_out / 'data',
    endpoint = "https://api.census.gov/data/2020/acs/acs5",
    state_code = "34",  # New Jersey's FIPS code
    tract_code = "*",  # All census tracts
)
census.save()

# %%
