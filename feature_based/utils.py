
from consts import IS_FEATURE_COMPLEXITY, IS_FEATURE_COST, IS_UNI_FEAT_WEIGHTS, IS_FEATURE_COST, OUTPUT_SYSTEM_SUBFOLDER, OUTPUT_COMPLEXITY_SUBFOLDER, OUTPUT_COST_SUBFOLDER, FIGS_SYSTEM_SUBFOLDER, FIGS_COMPLEXITY_SUBFOLDER, FIGS_COST_SUBFOLDER

def get_filepath(prefix, index, extension):
    output_folder = None
    if extension == "csv":
        if IS_FEATURE_COST and IS_FEATURE_COMPLEXITY:
            output_folder = OUTPUT_SYSTEM_SUBFOLDER
        elif IS_FEATURE_COMPLEXITY:
            output_folder = OUTPUT_COMPLEXITY_SUBFOLDER
        elif IS_FEATURE_COST:
            output_folder = OUTPUT_COST_SUBFOLDER
    else:
        if IS_FEATURE_COST and IS_FEATURE_COMPLEXITY:
            output_folder = FIGS_SYSTEM_SUBFOLDER
        elif IS_FEATURE_COMPLEXITY:
            output_folder = FIGS_COMPLEXITY_SUBFOLDER
        elif IS_FEATURE_COST:
            output_folder = FIGS_COST_SUBFOLDER

    return _get_filepath(output_folder, prefix, index, extension)

def _get_filepath(output_folder, prefix, index, extension):
        if IS_FEATURE_COST and IS_FEATURE_COMPLEXITY:
            if IS_UNI_FEAT_WEIGHTS:
                return output_folder / f"{prefix}_combined_uni_weights_{index}.{extension}"
            else:
                return output_folder / f"{prefix}_combined_feat_weights_{index}.{extension}"
        elif IS_FEATURE_COMPLEXITY:
            return output_folder / f"{prefix}_complex_{index}.{extension}"
        elif IS_FEATURE_COST:
            if IS_UNI_FEAT_WEIGHTS:
                return output_folder / f"{prefix}_cost_uni_weights_{index}.{extension}"
            else:
                return output_folder / f"{prefix}_cost_feat_weights_{index}.{extension}"
