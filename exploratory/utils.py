import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


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
