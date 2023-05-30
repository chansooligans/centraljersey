import statsmodels.api as sm


def split_data(df, vars):
    X_train = df.loc[df["label"].notnull(), vars]
    X_train = sm.add_constant(X_train)
    y_train = df.loc[df["label"].notnull(), ["label"]].astype(int)

    X_test = df.loc[df["label"].isnull(), vars]

    return {"X_train": X_train, "y_train": y_train, "X_test": X_test}
