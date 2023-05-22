from functools import cached_property

from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import (GridSearchCV, cross_val_predict,
                                     cross_val_score)
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

from centraljersey import merge


class PredictionModels:
    def __init__(self):
        self.merger = merge.Merge()
        self.df_county = self.merger.df_counties
        self.df_tracts = self.merger.df_tracts
        self.sc = StandardScaler()
        self.models = {
            "Logistic Regression": LogisticRegression(random_state=0),
            "SVM": SVC(probability=True),
            "KNN": KNeighborsClassifier(3),
            "Random Forest": RandomForestClassifier(),
            "AdaBoost": AdaBoostClassifier(),
        }

    @cached_property
    def X(self):
        return self.df_tracts.loc[self.df_tracts["label"].notnull()].fillna(0)

    @cached_property
    def features(self):
        return self.X.columns

    @cached_property
    def y(self):
        return self.df_tracts.loc[self.df_tracts["label"].notnull(), "label"]

    @cached_property
    def X_test(self):
        return self.df_tracts.fillna(0)

    def preprocess_data(self):
        self.X = self.sc.fit_transform(self.X)
        self.X_test = self.sc.transform(self.X_test)

    def logistic_regression(self):
        clf = self.models["Logistic Regression"].fit(self.X, self.y)
        y_test = clf.predict_proba(self.X_test)
        self.df_tracts["_loc"] = y_test[:, 1]

    def svm(self):
        param_grid = {
            "C": [0.1, 1, 10, 100],
            "gamma": [1, 0.1, 0.01, 0.001],
            "kernel": ["rbf", "poly", "sigmoid"],
        }
        grid = GridSearchCV(self.models["SVM"], param_grid, refit=True, verbose=2)
        clf = grid.fit(self.X, self.y)
        y_test = clf.predict_proba(self.X_test)
        self.df_tracts["svc_loc"] = y_test[:, 1]

    def knn(self):
        clf = self.models["KNN"].fit(self.X, self.y)
        y_test = clf.predict_proba(self.X_test)
        self.df_tracts["knn_loc"] = y_test[:, 1]

    def random_forest(self):
        param_grid = {
            "n_estimators": [25, 50, 100, 150],
            "max_features": ["sqrt", "log2", None],
            "max_depth": [3, 6, 9],
            "max_leaf_nodes": [3, 6, 9],
        }
        grid_search = GridSearchCV(
            self.models["Random Forest"], param_grid=param_grid, verbose=2
        )
        clf = grid_search.fit(self.X, self.y)
        y_test = clf.predict_proba(self.X_test)
        self.df_tracts["rf_loc"] = y_test[:, 1]

    def adaboost(self):
        clf = self.models["AdaBoost"].fit(self.X, self.y)
        y_test = clf.predict_proba(self.X_test)
        self.df_tracts["ada_loc"] = y_test[:, 1]

    def run_predictions(self):
        self.preprocess_data()
        self.logistic_regression()
        self.svm()
        self.knn()
        self.random_forest()
        self.adaboost()
