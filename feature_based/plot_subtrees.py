"""
Plots subtree scatterplots of cost vs complexity and feature-based cost vs complexity.
Saves plots to feature_based/figs directory.
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from consts import SUBTREE_INDICES, IS_UNI_FEAT_WEIGHTS, IS_FEATURE_COMPLEXITY, IS_FEATURE_COST, OUTPUT_SYSTEM_SUBFOLDER, OUTPUT_COMPLEXITY_SUBFOLDER, OUTPUT_COST_SUBFOLDER, FIGS_COMPLEXITY_SUBFOLDER, FIGS_COST_SUBFOLDER, FIGS_SYSTEM_SUBFOLDER
from utils import get_filepath

outdir = "feature_based/figs"

subtree_names = {
    12: "Full Tree",
    14: "Niblings",
    15: "Grandparents",
    16: "Grandchildren",
    17: "Aunts",
    18: "Siblings",
    19: "Uncles"
}
        
for subtree in SUBTREE_INDICES:
    #rw_df = pd.read_csv(rw_pattern.format(features, subtree))
    rw_df = pd.read_csv(get_filepath("rw", subtree, "csv"))
    #hyp_df = pd.read_csv(hyp_pattern.format(features, subtree))
    hyp_df = pd.read_csv(get_filepath("hyp", subtree, "csv"))

    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))
    ax_left, ax_right = axes

    y_values = pd.concat([
        rw_df["cost"],
        #hyp_df["cost"],
        #rw_df["feature_based_cost"],
        #hyp_df["feature_based_cost"],
    ])

    y_min = y_values.min() - .1
    y_max = y_values.max() + .1

    rw_freqs = rw_df['freqs']

    # left plot (original 2012 cost vs complexity)
    ax_left.scatter(rw_df["complexity"], rw_df["cost"], s=rw_freqs * 5,
                    color="red", alpha=0.8, zorder=10, label="Real-world")

    ax_left.scatter(hyp_df["complexity"], hyp_df["cost"],
                    color="gray", alpha=0.8, label="Hypothetical")

    ax_left.set_title(f"{subtree_names[subtree]}: Cost vs Complexity")
    ax_left.set_xlabel("Complexity")
    ax_left.set_ylabel("Cost")

    custom_handles = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor='red', 
            markersize=8, alpha=0.7, linestyle=''),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='grey', 
            markersize=8, alpha=0.8, linestyle='')
    ]

    ax_left.legend(handles=custom_handles, labels=["Real-world", "Hypothetical"])

    # right plot
    complexity_col = "feature_complexity" if IS_FEATURE_COMPLEXITY else "complexity"
    cost_col = "feature_cost" if IS_FEATURE_COST else "cost"

    ax_right.scatter(rw_df[complexity_col], rw_df[cost_col], s=rw_freqs * 5,
                     color="red", alpha=0.7, zorder=10, label="Real-world")

    ax_right.scatter(hyp_df[complexity_col], hyp_df[cost_col],
                     color="gray", alpha=0.8, label="Hypothetical")

    ax_right.set_title(f"{subtree_names[subtree]}: Feature-based Cost vs Complexity")

    xlabel = "Feature Complexity" if IS_FEATURE_COMPLEXITY else "Complexity"
    ylabel = "Feature Cost" if IS_FEATURE_COST else "Cost"
    ax_right.set_xlabel(xlabel)
    ax_right.set_ylabel(ylabel)

    custom_handles = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor='red', 
            markersize=8, alpha=0.8, linestyle=''),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='grey', 
            markersize=8, alpha=0.8, linestyle='')
    ]

    ax_right.legend(handles=custom_handles, labels=["Real-world", "Hypothetical"])

    outfile = get_filepath("subtree", subtree, "png")

    plt.tight_layout()
    #plt.show()
    plt.savefig(outfile, dpi=300)
    plt.close(fig)

    print(f"Saved {outfile}")
