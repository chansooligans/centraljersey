# %%
from IPython import get_ipython

if get_ipython() is not None:
    get_ipython().run_line_magic("load_ext", "autoreload")
    get_ipython().run_line_magic("autoreload", "2")

# %%
from centraljersey.merge import Merge

merged = Merge()

# %%
merged.df_tracts

# %%
merged.df_counties
# %%
