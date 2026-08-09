import pandas as pd
from consts import OUTPUT_SYSTEM_SUBFOLDER, OUTPUT_COMPLEXITY_SUBFOLDER, OUTPUT_COST_SUBFOLDER, SUBTREE_INDICES, IS_UNI_FEAT_WEIGHTS

def combine_scores(feature_cost_path, feature_complexity_path, tree_index, is_rw):
    feature_cost_df = pd.read_csv(feature_cost_path)
    feature_complexity_df = pd.read_csv(feature_complexity_path)

    combined_df = pd.merge(feature_cost_df, feature_complexity_df, on=["tree_index", "label"], suffixes=("_cost", "_complexity"))

    if is_rw:
        output_path = f"{OUTPUT_SYSTEM_SUBFOLDER} / rw_combined_uni_weights_{tree_index}" if IS_UNI_FEAT_WEIGHTS else f"{OUTPUT_SYSTEM_SUBFOLDER} / rw_combined_feat_weights_{tree_index}"
        combined_df.to_csv(output_path, index=False)
    else:
        output_path = f"{OUTPUT_SYSTEM_SUBFOLDER} / hyp_combined_uni_weights_{tree_index}" if IS_UNI_FEAT_WEIGHTS else f"{OUTPUT_SYSTEM_SUBFOLDER} / hyp_combined_feat_weights_{tree_index}"
        combined_df.to_csv(output_path, index=False)


if __name__ == "main":
    for i in SUBTREE_INDICES:
        rw_feat_cost_path = f"{OUTPUT_COST_SUBFOLDER} / rw_cost_uni_weights_{i}" if IS_UNI_FEAT_WEIGHTS else f"{OUTPUT_COST_SUBFOLDER} / rw_cost_feat_weights_{i}"
        hyp_feat_cost_path = f"{OUTPUT_COST_SUBFOLDER} / hyp_cost_uni_weights_{i}" if IS_UNI_FEAT_WEIGHTS else f"{OUTPUT_COST_SUBFOLDER} / hyp_cost_feat_weights_{i}"

        combine_scores(rw_feat_cost_path, f"{OUTPUT_COMPLEXITY_SUBFOLDER} / rw_complex_{i}", i, is_rw=True)
        combine_scores(rw_feat_cost_path, f"{OUTPUT_COMPLEXITY_SUBFOLDER} / hyp_complex_{i}", i, is_rw=False)
