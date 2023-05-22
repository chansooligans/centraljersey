# %%
from IPython import get_ipython

if get_ipython() is not None:
    get_ipython().run_line_magic("load_ext", "autoreload")
    get_ipython().run_line_magic("autoreload", "2")
from functools import cached_property

import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import (GridSearchCV, cross_val_predict,
                                     cross_val_score)
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

from centraljersey import merge, preprocess
from centraljersey.data import census, dialects, foursquare
from centraljersey.models import PredictionModels

# %% [markdown]
"""
# Prep
"""
# %%
# Example usage:
predictions = PredictionModels()
predictions.run_predictions()

# %%
predictions.df_tracts["_loc"]
# %%
