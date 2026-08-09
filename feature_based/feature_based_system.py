from consts import SUBTREE_INDICES, IS_FEATURE_COMPLEXITY, IS_FEATURE_COST, OUTPUT_COMPLEXITY_SUBFOLDER, OUTPUT_COST_SUBFOLDER, OUTPUT_SYSTEM_SUBFOLDER, IS_UNI_FEAT_WEIGHTS
from feature_complexity_opt import calculate_complexity, KintypeFeatures
from feature_based_cost_subtree import calculate_cost, get_need_probabilities, calculate_feature_cost
import pandas as pd
from pathlib import Path
import json

NIB_FEATURES = [
        KintypeFeatures(0, 0, 1, 0, 0, 1), # 0: Bob's YoSisDa
        KintypeFeatures(0, 1, 1, 0, 0, 1), # 1: Bob's YoSisSo
        KintypeFeatures(0, 0, 1, 0, 1, 1), # 2: Bob's ElSisDa
        KintypeFeatures(0, 1, 1, 0, 1, 1), # 3: Bob's ElSisSo
        KintypeFeatures(0, 0, 0, None, None, 1), # 4: Bob's Da
        KintypeFeatures(0, 1, 0, None, None, 1), # 5: Bob's So
        KintypeFeatures(0, 0, 1, 1, 0, 1), # 6: Bob's YoBrDa
        KintypeFeatures(0, 1, 1, 1, 0, 1), # 7: Bob's YoBrSo
        KintypeFeatures(0, 0, 1, 1, 1, 1), # 8: Bob's ElBrDa
        KintypeFeatures(0, 1, 1, 1, 1, 1), # 9: Bob's ElBrSo
]

NIB_LABELS = [
    'A-YoSisDa', 'A-YoSisSo', 'A-ElSisDa', 'A-ElSisSo',
    'B-YoSisDa', 'B-YoSisSo', 'B-ElSisDa', 'B-ElSisSo'
]  

GP_FEATURES = [
        KintypeFeatures(2, 0, 0, 0, None, 0),  # 0: Alice's MoMo
        KintypeFeatures(2, 1, 0, 0, None, 0),  # 1: Alice's MoFa
        KintypeFeatures(2, 0, 0, 1, None, 0),  # 2: Alice's FaMo
        KintypeFeatures(2, 1, 0, 1, None, 0),  # 3: Alice's FaFa
        KintypeFeatures(2, 0, 0, 0, None, 1),  # 4: Bob's MoMo
        KintypeFeatures(2, 1, 0, 0, None, 1),  # 5: Bob's MoFa
        KintypeFeatures(2, 0, 0, 1, None, 1),  # 6: Bob's FaMo
        KintypeFeatures(2, 1, 0, 1, None, 1),  # 7: Bob's FaFa
    ]
    
GP_LABELS = ['A-MoMo', 'A-MoFa', 'A-FaMo', 'A-FaFa', 
              'B-MoMo', 'B-MoFa', 'B-FaMo', 'B-FaFa']

GC_FEATURES = [
    KintypeFeatures(-2, 0, 0, 0, None, 0),  # 0: Alice's DaDa
    KintypeFeatures(-2, 1, 0, 0, None, 0),  # 1: Alice's DaSo
    KintypeFeatures(-2, 0, 0, 1, None, 0),  # 2: Alice's SoDa
    KintypeFeatures(-2, 1, 0, 1, None, 0),  # 3: Alice's SoSo
    KintypeFeatures(-2, 0, 0, 0, None, 1),  # 4: Bob's DaDa
    KintypeFeatures(-2, 1, 0, 0, None, 1),  # 5: Bob's DaSo
    KintypeFeatures(-2, 0, 0, 1, None, 1),  # 6: Bob's SoDa
    KintypeFeatures(-2, 1, 0, 1, None, 1),  # 7: Bob's SoSo
]

GC_LABELS = ['A-DaDa', 'A-DaSo', 'A-SoDa', 'A-SoSo', 
              'B-DaDa', 'B-DaSo', 'B-SoDa', 'B-SoSo']

AUNT_FEATURES = [
    KintypeFeatures(1, 0, 1, 0, 0, 0), # 0: Alice's MoYoSis
    KintypeFeatures(1, 0, 1, 0, 1, 0), # 1: Alice's MoElSis
    KintypeFeatures(1, 0, 0, None, None, 0), # 2: Alice's Mo
    KintypeFeatures(1, 0, 1, 1, 0, 0), # 3: Alice's FaYoSis
    KintypeFeatures(1, 0, 1, 1, 1, 0), # 4: Alice's FaElSis
    KintypeFeatures(1, 0, 1, 0, 0, 1), # 5: Bob's MoYoSis
    KintypeFeatures(1, 0, 1, 0, 1, 1), # 6: Bob's MoElSis
    KintypeFeatures(1, 0, 0, None, None, 1), # 7: Bob's Mo
    KintypeFeatures(1, 0, 1, 1, 0, 1), # 8: Bob's FaYoSis
    KintypeFeatures(1, 0, 1, 1, 1, 1), # 9: Bob's FaElSis
]   

AUNT_LABELS = [
    'A-MoYoSis', 'A-MoElSis', 'A-Mo', 
    'A-FaYoSis', 'A-FaElSis', 'B-MoYoSis', 'B-MoElSis', 'B-Mo', 
    'B-FaYoSis', 'B-FaElSis'
]

SIBLING_FEATURES = [
    KintypeFeatures(0, 0, 1, None, 0, 0), # 0: Alice's YoSis
    KintypeFeatures(0, 0, 1, None, 1, 0), # 1: Alice's ElSis
    KintypeFeatures(0, 1, 1, None, 0, 0), # 2: Alice's YoBr
    KintypeFeatures(0, 1, 1, None, 1, 0), # 3: Alice's ElBr
    KintypeFeatures(0, 0, 1, None, 0, 1), # 4: Bob's YoSis
    KintypeFeatures(0, 0, 1, None, 1, 1), # 5: Bob's ElSis
    KintypeFeatures(0, 1, 1, None, 0, 1), # 6: Bob's YoBr
    KintypeFeatures(0, 1, 1, None, 1, 1), # 7: Bob's ElBr
]

SIBLING_LABELS = [
    'A-YoSis', 'A-ElSis', 'A-YoBr', 'A-ElBr', 
    'B-YoSis', 'B-ElSis', 'B-YoBr', 'B-ElBr'
]

UNCLE_FEATURES = [
    KintypeFeatures(1, 1, 1, 0, 0, 0), # 0: Alice's MoYoBr
    KintypeFeatures(1, 1, 1, 0, 1, 0), # 1: Alice's MoElBr
    KintypeFeatures(1, 1, 0, None, None, 0), # 2: Alice's Fa
    KintypeFeatures(1, 1, 1, 1, 0, 0), # 3: Alice's FaYoBr
    KintypeFeatures(1, 1, 1, 1, 1, 0), # 4: Alice's FaElBr
    KintypeFeatures(1, 1, 1, 0, 0, 1), # 5: Bob's MoYoBr
    KintypeFeatures(1, 1, 1, 0, 1, 1), # 6: Bob's MoElBr
    KintypeFeatures(1, 1, 0, None, None, 1), # 7: Bob's Fa
    KintypeFeatures(1, 1, 1, 1, 0, 1), # 8: Bob's FaYoBr
    KintypeFeatures(1, 1, 1, 1, 1, 1), # 9: Bob's FaElBr
]   

UNCLE_LABELS = [
    'A-MoYoBr', 'A-MoElBr', 'A-Fa', 
    'A-FaYoBr', 'A-FaElBr', 'B-MoYoBr', 'B-MoElBr', 'B-Fa', 
    'B-FaYoBr', 'B-FaElBr'
]

KINTYPE_FEATURES_MAP = {
    14: NIB_FEATURES,
    15: GP_FEATURES,
    16: GC_FEATURES,
    17: AUNT_FEATURES,
    18: SIBLING_FEATURES,
    19: UNCLE_FEATURES,
}

KINTYPE_LABELS_MAP = {
    14: NIB_LABELS,
    15: GP_LABELS,
    16: GC_LABELS,
    17: AUNT_LABELS,
    18: SIBLING_LABELS,
    19: UNCLE_LABELS,
}

def load_rw_partitions(tree_index):
    """Load RW partitions for a given tree index"""
    file_path = Path("feature_based") / "output" / "partitions" / f"rw_partitions_{tree_index}.csv"
    df = pd.read_csv(file_path, header=None)
    freqs = df.iloc[:, 0]
    partitions = df.iloc[:, 1:]
    return freqs, partitions

def load_rw_scores(tree_index):
    """Load real-world scores"""

    rw_complexity_file = Path("input") / f"complex_{tree_index}_1_1_1_2_rpt1_rand0"
    rw_cost_file = Path("input") / f"cost_{tree_index}_1_1_1_2_6_rpt1_rand0"

    rw_complexity = (
        pd.read_csv(rw_complexity_file, sep=" ", names=["complexity", "count"])
    )

    rw_complexity["complexity"] = rw_complexity["complexity"] / 3

    rw_cost = pd.read_csv(rw_cost_file, names=["cost"])

    # Create scores tibble
    scores = pd.DataFrame({
        "complexity": rw_complexity["complexity"],
        "cost": rw_cost["cost"],
    })
    return scores

def load_hypothetical_partitions(tree_index):
    """Load hypothetical partitions for a given tree index"""
    file_path = Path("feature_based") / "output" / "partitions" / f"hyp_partitions_{tree_index}.csv"
    df = pd.read_csv(file_path, header=None)
    return df

def load_hypothetical_scores(tree_index):
    hyp_complexity_file = Path("input") / f"complex_{tree_index}_1_1_1_4_rpt1_rand0"
    hyp_cost_file = Path("input") / f"cost_{tree_index}_1_1_1_4_6_rpt1_rand0"

    hyp_complexity = (
        pd.read_csv(hyp_complexity_file, sep=" ", names=["complexity", "count"])
    )

    hyp_complexity["complexity"] = hyp_complexity["complexity"] / 3

    hyp_cost = pd.read_csv(hyp_cost_file, names=["cost"])

    # Create scores tibble
    scores = pd.DataFrame({
        "complexity": hyp_complexity["complexity"],
        "cost": hyp_cost["cost"],
    })
    return scores

if __name__ == "__main__":
    
    need_probs = get_need_probabilities()

    for tree_index in SUBTREE_INDICES:
        FEATURES = KINTYPE_FEATURES_MAP[tree_index]
        LABELS = KINTYPE_LABELS_MAP[tree_index]
        freqs, rw_partitions_df = load_rw_partitions(tree_index)
        rw_scores_df = load_rw_scores(tree_index)
        rw_feature_complexities = []
        rw_feature_costs = []
        rw_feature_representations = {}
        for partition in rw_partitions_df.values:
            if IS_FEATURE_COMPLEXITY:
                min_expr, complexity = calculate_complexity(partition.tolist(), FEATURES)
                min_expr['complexity'] = complexity
                rw_feature_complexities.append(complexity)
                rw_feature_representations[str(partition)] = min_expr

            if IS_FEATURE_COST:
                feature_based_cost = calculate_cost(tree_index, partition, need_probs)
                rw_feature_costs.append(feature_based_cost)
        
        rw_scores_df['freqs'] = freqs
        if IS_FEATURE_COMPLEXITY:
            rw_scores_df['feature_complexity'] = rw_feature_complexities
        if IS_FEATURE_COST:
            rw_scores_df['feature_cost'] = rw_feature_costs

        rw_output_file = None

        if IS_FEATURE_COMPLEXITY and IS_FEATURE_COST:
            if IS_UNI_FEAT_WEIGHTS:
                rw_output_file = OUTPUT_SYSTEM_SUBFOLDER / f"rw_combined_uni_weights_{tree_index}.csv"
            else:
                rw_output_file = OUTPUT_SYSTEM_SUBFOLDER / f"rw_combined_feat_weights_{tree_index}.csv"
            with open(Path("feature_based") / "output" / "feature_representations" / f"rw_feature_reprs_{tree_index}.json", 'w') as json_file:
                json.dump(rw_feature_representations, json_file, indent=4)        
        elif IS_FEATURE_COMPLEXITY:
            rw_output_file = OUTPUT_COMPLEXITY_SUBFOLDER / f"rw_complex_{tree_index}.csv"
            with open(Path("feature_based") / "output" / "feature_representations" / f"rw_feature_reprs_{tree_index}.json", 'w') as json_file:
                json.dump(rw_feature_representations, json_file, indent=4)
        elif IS_FEATURE_COST:
            if IS_UNI_FEAT_WEIGHTS:
                rw_output_file = OUTPUT_COST_SUBFOLDER / f"rw_cost_uni_weights_{tree_index}.csv"
            else:
                rw_output_file = OUTPUT_COST_SUBFOLDER / f"rw_cost_feat_weights_{tree_index}.csv"


        rw_scores_df.to_csv(rw_output_file, index=False)
        print(f"Processed real-world tree index {tree_index}")

        hyp_partitions_df = load_hypothetical_partitions(tree_index)
        hyp_scores_df = load_hypothetical_scores(tree_index)
        hyp_feature_complexities = []
        hyp_feature_costs = []
        for partition in hyp_partitions_df.values:
            if IS_FEATURE_COMPLEXITY:
                _, complexity = calculate_complexity(partition, FEATURES)
                hyp_feature_complexities.append(complexity)

            if IS_FEATURE_COST:
                feature_based_cost = calculate_cost(tree_index, partition, need_probs)
                hyp_feature_costs.append(feature_based_cost)

        hyp_scores_df['freqs'] = freqs
        if IS_FEATURE_COMPLEXITY:
            hyp_scores_df['feature_complexity'] = hyp_feature_complexities
        if IS_FEATURE_COST:
            hyp_scores_df['feature_cost'] = hyp_feature_costs


        hyp_output_file = None
        if IS_FEATURE_COMPLEXITY and IS_FEATURE_COST:
            if IS_UNI_FEAT_WEIGHTS:
                hyp_output_file = OUTPUT_SYSTEM_SUBFOLDER / f"hyp_combined_uni_weights_{tree_index}.csv"
            else:
                hyp_output_file = OUTPUT_SYSTEM_SUBFOLDER / f"hyp_combined_feat_weights_{tree_index}.csv"
        elif IS_FEATURE_COMPLEXITY:
            hyp_output_file = OUTPUT_COMPLEXITY_SUBFOLDER / f"hyp_complex_{tree_index}.csv"
        elif IS_FEATURE_COST:
            if IS_UNI_FEAT_WEIGHTS:
                hyp_output_file = OUTPUT_COST_SUBFOLDER / f"hyp_cost_uni_weights_{tree_index}.csv"
            else:
                hyp_output_file = OUTPUT_COST_SUBFOLDER / f"hyp_cost_feat_weights_{tree_index}.csv"

        hyp_scores_df.to_csv(hyp_output_file, index=False)        
        print(f"Processed hypothetical tree index {tree_index}")