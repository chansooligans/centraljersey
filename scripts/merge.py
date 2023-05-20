# %%
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
from src import merge
from src.load import census, dialects, foursquare

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
# Predictions
"""

# %%
df_tracts = df_tracts.merge(
    df_county[
        [
            "COUNTYFP",
            "dunkin_id",
            "wawa_id",
            "pork_roll",
            "giants_or_jets",
            "calm-no-l",
            "almond-no-l",
            "forward-no-r",
            "drawer",
            "gone-don",
        ]
    ],
    how="left",
)

INCLUDE = [
    "dunkin_id",
    "wawa_id",
    "giants_or_jets",
    "pork_roll",
    "calm-no-l",
    "almond-no-l",
    "forward-no-r",
    "drawer",
    "gone-don",
    "white_pop",
    "black_pop",
    "asian_pop",
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
    "income_150k+",
    "pob_foreign_born",
    "edu_college",
]

X = df_tracts.loc[df_tracts["label"].notnull(), INCLUDE].fillna(0)
features = X.columns
y = df_tracts.loc[df_tracts["label"].notnull(), "label"]
X_test = df_tracts[INCLUDE].fillna(0)

# %% [markdown]
"""
# Prep
"""

# %%
sc = StandardScaler()
X = sc.fit_transform(X)
X_test = sc.transform(X_test)

# %% [markdown]
"""
# Logistic Regression
"""
# %%
m = LogisticRegression(random_state=0)
clf = m.fit(X, y)

# Use cross_val_predict to perform cross-validation
y_pred = cross_val_predict(clf, X, y, cv=5)

# Use cross_val_score to calculate cross-validated performance scores
scores = cross_val_score(clf, X, y, cv=5)
print("Cross-validated scores:", scores)

df_features = pd.DataFrame({"feature": features, "blue=north": m.coef_[0]})

y_test = clf.predict_proba(X_test)

df_features.sort_values("blue=north").to_csv(
    "../apps/static/csv/summary.csv", index=False
)
df_tracts["_loc"] = y_test[:, 1]

# %% [markdown]
"""
# SVM
"""
# %%
m = SVC(probability=True)
# clf = m.fit(X, y)
from sklearn.model_selection import GridSearchCV

param_grid = {
    "C": [0.1, 1, 10, 100],
    "gamma": [1, 0.1, 0.01, 0.001],
    "kernel": ["rbf", "poly", "sigmoid"],
}
grid = GridSearchCV(m, param_grid, refit=True, verbose=2)
clf = grid.fit(X, y)

y_test = clf.predict_proba(X_test)
print(clf.best_estimator_)

df_tracts["svc_loc"] = y_test[:, 1]

# %% [markdown]
"""
# KNN
"""
# %%
m = KNeighborsClassifier(3)
clf = m.fit(X, y)

# Use cross_val_predict to perform cross-validation
y_pred = cross_val_predict(clf, X, y, cv=5)

# Use cross_val_score to calculate cross-validated performance scores
scores = cross_val_score(clf, X, y, cv=5)
print("Cross-validated scores:", scores)

y_test = clf.predict_proba(X_test)

df_tracts["knn_loc"] = y_test[:, 1]

# %% [markdown]
"""
# Random Forest
"""
# %%
m = RandomForestClassifier()
param_grid = {
    "n_estimators": [25, 50, 100, 150],
    "max_features": ["sqrt", "log2", None],
    "max_depth": [3, 6, 9],
    "max_leaf_nodes": [3, 6, 9],
}
grid_search = GridSearchCV(m, param_grid=param_grid, verbose=2)
clf = grid_search.fit(X, y)
y_test = clf.predict_proba(X_test)

df_tracts["rf_loc"] = y_test[:, 1]

# %% [markdown]
"""
# AdaBoost
"""
# %%
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier

m = AdaBoostClassifier()
clf = m.fit(X, y)

# Use cross_val_predict to perform cross-validation
y_pred = cross_val_predict(clf, X, y, cv=5)

# Use cross_val_score to calculate cross-validated performance scores
scores = cross_val_score(clf, X, y, cv=5)
print("Cross-validated scores:", scores)

y_test = clf.predict_proba(X_test)

df_tracts["ada_loc"] = y_test[:, 1]

# %% [markdown]
"""
# Export
"""
# %%
df_tracts[
    ["geometry", "_loc", "svc_loc", "knn_loc", "rf_loc", "ada_loc"] + INCLUDE
].fillna(0).to_file("../apps/static/geojson/merged_tracts.geojson", driver="GeoJSON")
