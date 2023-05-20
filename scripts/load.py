# %%
from IPython import get_ipython

if get_ipython() is not None:
    get_ipython().run_line_magic("load_ext", "autoreload")
    get_ipython().run_line_magic("autoreload", "2")

from centraljersey.data import census as censusload
from centraljersey.data import dialects as diaload

# %%
census = censusload.Load(
    endpoint="https://api.census.gov/data/2020/acs/acs5",
    state_code="34",  # New Jersey's FIPS code
    tract_code="*",  # All census tracts
)
census.nj_data

# %%
dialects = diaload.Load()
dialects.calm
dialects.forward
dialects.draw
dialects.gone


# %%
