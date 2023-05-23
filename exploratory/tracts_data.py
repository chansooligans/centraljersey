# %%
from IPython import get_ipython

if get_ipython() is not None:
    get_ipython().run_line_magic("load_ext", "autoreload")
    get_ipython().run_line_magic("autoreload", "2")
import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from centraljersey.models import PredictionModels

model = PredictionModels()
df = model.df_tracts
df["label"] = df["label"].str.replace("1", "north").str.replace("0", "south")


# %%
def plot_density_by_label_grid(data, variables):
    # Calculate the number of rows and columns in the grid based on the number of variables
    num_variables = len(variables)
    num_cols = min(3, num_variables)
    num_rows = math.ceil(num_variables / num_cols)

    # Set the style of the plots
    sns.set(style="whitegrid")

    # Create the grid of subplots
    fig, axes = plt.subplots(nrows=num_rows, ncols=num_cols, figsize=(12, num_rows * 3))
    axes = axes.flatten()  # Flatten the 2D axes array into a 1D array

    # Iterate over the variables and plot the density plots on each subplot
    for i, variable in enumerate(variables):
        ax = axes[i]
        sns.kdeplot(data=data, x=variable, hue="label", fill=True, ax=ax)
        # ax.set_title("Density")
        ax.set_xlabel(variable)
        ax.set_ylabel("Density")

        # Remove legend except for the last plot
        if i != 0:
            ax.get_legend().remove()

    # Remove any unused subplots
    if len(variables) < len(axes):
        for j in range(len(variables), len(axes)):
            fig.delaxes(axes[j])

    # Adjust the layout and spacing of the subplots
    fig.tight_layout()

    # Display the plot
    plt.show()


# %% [markdown]
"""
# Culture: Dunkin / Wawa / NFL / Dialects
"""

# %%
culture_variables = [
    "dunkin_id",
    "wawa_id",
    "giants_or_jets",
    "pork_roll",
    "calm-no-l",
    "almond-no-l",
    "forward-no-r",
    "drawer",
    "gone-don",
]
plot_density_by_label_grid(data=df, variables=culture_variables)

# %% [markdown]
"""
# Census Variables: Demographics, Occupation, Income, Education
"""

# %%
census_variables = [
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

plot_density_by_label_grid(data=df, variables=census_variables)

# %%
