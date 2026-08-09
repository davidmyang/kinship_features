"""
Plots subtree scatterplots of cost vs complexity and feature-based cost vs complexity.
Saves plots to feature_based/figs directory.
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from consts import IS_REDUCTION, IS_UNI_FEAT_WEIGHTS, IS_FEATURE_COMPLEXITY, IS_FEATURE_COST, OUTPUT_SYSTEM_SUBFOLDER, OUTPUT_COMPLEXITY_SUBFOLDER, OUTPUT_COST_SUBFOLDER, FIGS_COMPLEXITY_SUBFOLDER, FIGS_COST_SUBFOLDER, FIGS_SYSTEM_SUBFOLDER

outdir = "feature_based/figs"

subtrees = [14]#[12, 14, 15, 16, 17, 18, 19]
subtree_names = {
    12: "Full Tree",
    14: "Niblings",
    15: "Grandparents",
    16: "Grandchildren",
    17: "Aunts",
    18: "Siblings",
    19: "Uncles"
}

def get_filepath(index, is_rw=True):
    if is_rw:
        if IS_FEATURE_COST and IS_FEATURE_COMPLEXITY:
            if IS_UNI_FEAT_WEIGHTS:
                return OUTPUT_SYSTEM_SUBFOLDER / f"rw_combined_uni_weights_{index}.csv"
            else:
                return OUTPUT_SYSTEM_SUBFOLDER / f"rw_combined_feat_weights_{index}.csv"
        elif IS_FEATURE_COMPLEXITY:
            return OUTPUT_COMPLEXITY_SUBFOLDER / f"rw_complex_{index}.csv"
        elif IS_FEATURE_COST:
            if IS_UNI_FEAT_WEIGHTS:
                return OUTPUT_COST_SUBFOLDER / f"rw_cost_uni_weights_{index}.csv"
            else:
                return OUTPUT_COST_SUBFOLDER / f"rw_cost_feat_weights_{index}.csv"
    else:
        if IS_FEATURE_COST and IS_FEATURE_COMPLEXITY:
            if IS_UNI_FEAT_WEIGHTS:
                return OUTPUT_SYSTEM_SUBFOLDER / f"hyp_combined_uni_weights_{index}.csv"
            else:
                return OUTPUT_SYSTEM_SUBFOLDER / f"hyp_combined_feat_weights_{index}.csv"
        elif IS_FEATURE_COMPLEXITY:
            return OUTPUT_COMPLEXITY_SUBFOLDER / f"hyp_complex_{index}.csv"
        elif IS_FEATURE_COST:
            if IS_UNI_FEAT_WEIGHTS:
                return OUTPUT_COST_SUBFOLDER / f"hyp_cost_uni_weights_{index}.csv"
            else:
                return OUTPUT_COST_SUBFOLDER / f"hyp_cost_feat_weights_{index}.csv"
        
for subtree in subtrees:

    #rw_df = pd.read_csv(rw_pattern.format(features, subtree))
    rw_df = pd.read_csv(get_filepath(subtree, is_rw=True))
    #hyp_df = pd.read_csv(hyp_pattern.format(features, subtree))
    hyp_df = pd.read_csv(get_filepath(subtree, is_rw=False))

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

    outfile = None
    if IS_FEATURE_COMPLEXITY and IS_FEATURE_COST:
        if IS_UNI_FEAT_WEIGHTS:
            outfile = FIGS_SYSTEM_SUBFOLDER / f"subtree_combined_uni_weight_{subtree}.png"
        else:
            outfile = FIGS_SYSTEM_SUBFOLDER / f"subtree_combined_feat_weight_{subtree}.png"
    elif IS_FEATURE_COMPLEXITY:
        outfile = FIGS_COMPLEXITY_SUBFOLDER / f"subtree_complex_{subtree}.png"
    elif IS_FEATURE_COST:
        if IS_UNI_FEAT_WEIGHTS:
            outfile = FIGS_COST_SUBFOLDER / f"subtree_cost_uni_weight_{subtree}.png"
        else:
            outfile = FIGS_COST_SUBFOLDER / f"subtree_cost_feat_weight_{subtree}.png"

    plt.tight_layout()
    #plt.show()
    plt.savefig(outfile, dpi=300)
    plt.close(fig)

    print(f"Saved {outfile}")
