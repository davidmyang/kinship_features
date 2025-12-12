import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import json

ALL_INDEX = 12
TREE_INDEX = 18  # 12:full tree, 14:niblings, 15:grandparents, 16:grandchildren, 
                 # 17:aunts, 18:siblings, 19: uncles

SUBSYSTEMS = [] # used to define highlighted category when full tree (12) is plotted

filename_prefixes = ["merging", "separate_term", "speaker_difference"]
other_category_name = "Other natural systems"

# File paths
base_dir = Path(".") 
DIR_PATH = base_dir / "2025_plots" / "nonoptimal_plots" / "plots"

d_murdock_file = base_dir / "murdockdata" / "murdock_orig_codes.csv"
d_map_file = base_dir / "2025_plots" / f"rwmapindex{TREE_INDEX}.csv"
selected_languages = {}
for filename_prefix in filename_prefixes:
    json_filename = f"{filename_prefix}_languages.json"
    with open(f"2025_plots/nonoptimal_plots/{json_filename}", "r", encoding="utf-8") as f:
        data = json.load(f)
        for category, languages in data.items():
            if category not in selected_languages:
                selected_languages[category] = dict()
            if filename_prefix not in selected_languages[category]:
                selected_languages[category][filename_prefix] = set()
            selected_languages[category][filename_prefix].update(languages)


rw_complexity_file = base_dir / "output" / f"complex_{TREE_INDEX}_1_1_1_2_rpt1_rand0"
rw_cost_file = base_dir / "output" / f"cost_{TREE_INDEX}_1_1_1_2_6_rpt1_rand0"

d_murdock = pd.read_csv(d_murdock_file)
d_map = pd.read_csv(d_map_file, names=["analysis_index", "score_index"])

d = d_murdock.merge(d_map, on="analysis_index", how="left")[["name", "score_index"]]

rw_complexity = pd.read_csv(rw_complexity_file, sep=" ", names=["complexity", "count"])
rw_complexity["complexity"] = rw_complexity["complexity"] / 3  # normalize
rw_cost = pd.read_csv(rw_cost_file, names=["cost"])

# Combine scores
scores = pd.DataFrame({
    "complexity": rw_complexity["complexity"],
    "cost": rw_cost["cost"],
    "score_index": range(1, len(rw_complexity) + 1)
})

# Merge with Murdock data
d_scores = d.merge(scores, on="score_index", how="left")
d_scores = d_scores.dropna()

# Determine which categories to highlight based on tree_index
TREE_TO_CATEGORY = {
    ALL_INDEX: [],  # all
    14: ["niblings"],
    15: ["grandparents"],
    16: ["grandchildren"],
    17: ["aunts"],
    18: ["siblings"],
    19: ["uncles"],
}
categories_to_show = TREE_TO_CATEGORY.get(TREE_INDEX)

if (TREE_INDEX == ALL_INDEX):
    for system in SUBSYSTEMS:
        categories_to_show += (TREE_TO_CATEGORY.get(system, []))

# Assign default color and category column
d_scores["category"] = other_category_name
highlight_langs = set()

# Languages that will be highlighted
if categories_to_show:
    # Start with the first category’s languages
    highlight_langs = set(selected_languages.get(categories_to_show[0], []))

    # Intersect with the rest
    for category in categories_to_show[1:]:
        highlight_langs &= set(selected_languages.get(category, []))
else: # plot all subsystems against all
    for category in selected_languages:
        highlight_langs |= set(selected_languages[category])

if TREE_INDEX == ALL_INDEX:
    category_name = ' & '.join(categories_to_show)
    for category in selected_languages:
        d_scores.loc[d_scores["name"].isin(selected_languages[category]), "category"] = category
else:
    for system_type in selected_languages[categories_to_show[0]]:
        d_scores.loc[d_scores["name"].isin(selected_languages[categories_to_show[0]][system_type]), "category"] = system_type.replace('_', ' ').title()

# --- Plot ---
plt.figure(figsize=(8, 6))

if TREE_INDEX == ALL_INDEX and len(SUBSYSTEMS) == 0:
    sns.scatterplot(
        data=d_scores,
        x="complexity", y="cost", hue="category",
        palette=sns.color_palette(), s=60, alpha=0.7, zorder=10
    )
else:
    sns.scatterplot(
        data=d_scores[d_scores["category"] != other_category_name],
        x="complexity", y="cost", hue="category",
        s=60, alpha=1, zorder=1,
        palette=sns.color_palette()
    )
    sns.scatterplot(
        data=d_scores[d_scores["category"] == other_category_name],
        x="complexity", y="cost",
        s=60, alpha=0.7, zorder=1,
        edgecolor="gray", facecolor="none", linewidth=1,
        label=other_category_name
    )
    plt.legend(title="Category")

save_path = ""
if (TREE_INDEX == ALL_INDEX):
    save_path = DIR_PATH / f"{filename_prefix}" / f"comp_cost_{'_'.join(filename_prefixes)}_{TREE_INDEX}_{'_'.join(str(s) for s in SUBSYSTEMS)}.png"
else:
    save_path = DIR_PATH / f"{filename_prefix}" / f"comp_cost_{filename_prefix}_{TREE_INDEX}.png"

plt.xlabel("Complexity")
plt.ylabel("Communicative Cost")
plt.title(f"{', '.join(categories_to_show).title()}")
plt.tight_layout()
plt.savefig(save_path, dpi=1000, bbox_inches="tight")
plt.show()