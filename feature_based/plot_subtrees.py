import pandas as pd
import matplotlib.pyplot as plt

outdir = "feature_based/figs"

subtrees = [14, 15, 16, 17, 18, 19]
subtree_names = {
    14: "Niblings",
    15: "Grandparents",
    16: "Grandchildren",
    17: "Aunts",
    18: "Siblings",
    19: "Uncles"
}

# Determines which output score file is plotted (e.g. laterality_generation_)
features = "laterality_" 

rw_pattern = "feature_based/output/rw_all_scores_{}{}.csv"
hyp_pattern = "feature_based/output/hyp_all_scores_{}{}.csv"

for subtree in subtrees:

    rw_df = pd.read_csv(rw_pattern.format(features, subtree))
    hyp_df = pd.read_csv(hyp_pattern.format(features, subtree))

    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))
    ax_left, ax_right = axes

    y_values = pd.concat([
        rw_df["cost"],
        hyp_df["cost"],
        rw_df["feature_based_cost"],
        hyp_df["feature_based_cost"],
    ])

    y_min = y_values.min() - .1
    y_max = y_values.max() + .1

    # left plot
    ax_left.scatter(rw_df["complexity"], rw_df["cost"],
                    color="blue", alpha=0.8, zorder=10, label="Real-world")

    ax_left.scatter(hyp_df["complexity"], hyp_df["cost"],
                    color="gray", alpha=0.8, label="Hypothetical")

    ax_left.set_title(f"{subtree_names[subtree]}: Cost vs Complexity")
    ax_left.set_xlabel("Complexity")
    ax_left.set_ylabel("Cost")
    #ax_left.set_ylim(y_min, y_max)
    ax_left.legend()

    # right plot
    ax_right.scatter(rw_df["complexity"], rw_df["feature_based_cost"],
                     color="blue", alpha=1, zorder=10, label="Real-world")

    ax_right.scatter(hyp_df["complexity"], hyp_df["feature_based_cost"],
                     color="gray", alpha=0.8, label="Hypothetical")

    ax_right.set_title(f"{subtree_names[subtree]}: Feature-based Cost vs Complexity")
    ax_right.set_xlabel("Complexity")
    ax_right.set_ylabel("Feature-based Cost")
    #ax_right.set_ylim(y_min, y_max)
    ax_right.legend()

    outfile = f"{outdir}/subtree_{features}{subtree}.png"
    plt.tight_layout()
    plt.savefig(outfile, dpi=150)
    plt.close(fig)

    print(f"Saved {outfile}")
