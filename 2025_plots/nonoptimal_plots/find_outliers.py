
import pandas as pd
from pathlib import Path

base_dir = Path(".")
DIR_PATH = base_dir / "2025_plots" / "nonoptimal_plots" / "output"

output_csv = DIR_PATH / "deviation_regression_data.csv"
d_murdock_file = base_dir / "murdockdata" / "murdock_orig_codes.csv"

d_murdock = pd.read_csv(d_murdock_file)
df_all = pd.read_csv(output_csv)


subset = ['dev_14', 'dev_15', 'dev_16', 'dev_17', 'dev_18', 'dev_19']

outliers_filtered = df_all[
    (df_all[subset] == 0).all(axis=1) &  # all those columns are 0
    (df_all['dev_full'] != 0)            # dev_full is non-zero
]

print(outliers_filtered)

merged_df = (
    outliers_filtered
    .merge(d_murdock, on="name", how="left")
    .drop(
        ['dev_14', 'dev_15', 'dev_16', 'dev_17', 'dev_18', 'dev_19',
         'orig_index', 'analysis_index', 'province', 'society', 'crosscousin_major', 'crosscousin_variant',
         'siblinginlaw_major', 'siblinginlaw_variant'],
        axis=1
    )
)

# other thing to check is languages that are still optimal with full system but have some nonoptimal subsystems

print(merged_df)
