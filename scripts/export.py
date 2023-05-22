# %%
from IPython import get_ipython

if get_ipython() is not None:
    get_ipython().run_line_magic("load_ext", "autoreload")
    get_ipython().run_line_magic("autoreload", "2")
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_predict, cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

from centraljersey import merge, preprocess
from centraljersey.data import census, dialects, foursquare

# %%
merger = merge.Merge()
df_county = merger.df_counties
df_tracts = merger.df_tracts

# %% [markdown]
"""
# Export Geojson
"""

# %%
county_cols = [
    "COUNTY",
    "COUNTYFP",
    "geometry",
    "wawa_id",
    "dunkin_id",
    "giants_or_jets",
    "pork_roll",
    "calm-no-l",
    "almond-no-l",
    "forward-no-r",
    "drawer",
    "gone-don",
]
df_county[county_cols].fillna(0).to_file(
    "../apps/static/geojson/merged_counties.geojson", driver="GeoJSON"
)

# %% [markdown]
"""
# Export
"""
# %%
df_tracts[
    ["geometry", "_loc", "svc_loc", "knn_loc", "rf_loc", "ada_loc"]
    + preprocess.TRACTS_INCLUDE
].fillna(0).to_file("../apps/static/geojson/merged_tracts.geojson", driver="GeoJSON")
