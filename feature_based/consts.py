from pathlib import Path

SUBTREE_INDICES = [14, 15, 16, 17, 18, 19]

# Whether to use uniform feature weights or feature-specific weights
IS_UNI_FEAT_WEIGHTS = False

# Whether to use feature cost or original cost
IS_FEATURE_COST = True

# Whether to use feature complexity or original complexity
IS_FEATURE_COMPLEXITY = True
IS_REDUCTION = False # only used in feature_complexity_opt.py for now

# Folder paths
BASE_FOLDER = Path("feature_based")
OUTPUT_FOLDER = BASE_FOLDER / "output"
FIGS_FOLDER = BASE_FOLDER / "figs"
OUTPUT_COST_SUBFOLDER = OUTPUT_FOLDER / "feature_cost_only"
OUTPUT_COMPLEXITY_SUBFOLDER = OUTPUT_FOLDER / "feature_complexity"
OUTPUT_SYSTEM_SUBFOLDER = OUTPUT_FOLDER / "feature_system"
FIGS_COST_SUBFOLDER = FIGS_FOLDER / "feature_cost_only"
FIGS_COMPLEXITY_SUBFOLDER = FIGS_FOLDER / "feature_complexity"
FIGS_SYSTEM_SUBFOLDER = FIGS_FOLDER / "feature_system"