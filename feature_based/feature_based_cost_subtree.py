"""
Calculates feature-based cost for real-world and hypothetical partitions of kinship subtrees.
Saves the scores with feature-based costs to CSV files.

To change feature weights, modify the FEATURE_WEIGHTS dictionary below.
"""
from pathlib import Path
import pandas as pd
import numpy as np
from consts import IS_UNI_FEAT_WEIGHTS

# Index of kintypes in the full kinship tree
niblings = np.array([99,100,101,102,103,104,105,106,107,108])
grandparents = np.array([9,10,11,12, 65,66,67,68])
grandchildren = np.array([53,54,55,56, 109,110,111,112])
aunts = np.array([13,14,15,18,19, 69,70,71,74,75])
siblings = np.array([31,32,33,34, 87,88,89,90])
uncles = np.array([16,17,20,21,22, 72,73,76,77,78])

subtree_index_map = {
    14: niblings,
    15: grandparents,
    16: grandchildren,
    17: aunts,
    18: siblings,
    19: uncles,
}

def get_kintype(index):
    """Determine kintype of a kintype"""
    return index

# The lists for each feature are zero-indexed full tree indices
SCR_F = [0, 1, 2, 3, 8, 9, 12, 13, 15, 16, 52,53,56, 57, 58, 59, 64, 65, 68, 69, 70, 71, 72, 108,109]
SCR_M = [4, 5, 6, 7, 10, 11, 17, 18, 20, 21, 54,55, 60, 61, 62, 63, 66, 67, 73, 74, 75, 76, 77,110,111]
def get_sex_connecting_relative(index):
    """Determine sex of connecting relative of a kintype"""
    if index in SCR_F:
        return 'F'
    elif index in SCR_M:
        return 'M'
    else:
        return None

LINEAL = [8, 9, 10, 11, 14, 19, 46, 47, 52, 53, 54, 55, 64, 65, 66, 67, 70, 75, 102, 103, 108, 109, 110, 111]
COLLATERAL = [12, 13, 15, 16, 17, 18, 20, 21, 30, 31, 32, 33, 68, 69, 71, 72, 73, 74, 76, 77, 86, 87, 88, 89, 98, 99, 100, 101, 104, 105, 106, 107]
def get_lineality(index):
    """Determine lineality of a kintype""" 
    if index in LINEAL:
        return 'Lineal'
    elif index in COLLATERAL:
        return 'Collateral'
    else:
        return None   

def get_generation(index):
    """Determine generation of a kintype"""
    if index in list(range(8, 12)) + list(range(64, 68)):
        return 'G+2'  # Grandparents
    elif index in list(range(12, 22)) + list(range(68, 78)):
        return 'G+1'  # Parents and aunts/uncles
    elif index in list(range(30, 34)) + list(range(86, 90)):
        return 'G0'   # Siblings
    elif index in list(range(42, 52)) + list(range(98, 108)):
        return 'G-1'  # Children and nieces/nephews
    elif index in list(range(52, 56)) + list(range(108, 112)):
        return 'G-2'  # Grandchildren
    else:
        return None

FEMALE = [8, 10, 12, 13, 14, 17, 18, 30, 31, 42, 44, 46, 48, 50, 52, 54, 64, 66, 68, 69, 70, 73, 74, 86, 87, 98, 100, 102, 104, 106, 108, 110]
MALE = [9, 11, 15, 16, 19, 20, 21, 32, 33, 43, 45, 47, 49, 51, 53, 55, 65, 67, 71, 72, 75, 76, 77, 88, 89, 99, 101, 103, 105, 107, 109, 111]
def get_sex(index):
    """Determine sex of a kintype"""
    if index in FEMALE:
        return 'F'
    elif index in MALE:
        return 'M'
    else:
        return None
    
ELDER = [13, 16, 18, 21, 31, 33, 69, 72, 74, 77, 87, 89]
YOUNGER = [12, 15, 17, 20, 30, 32, 68, 71, 73, 76, 86, 88]
def get_relative_age(index):
    """Determine relative age of a kintype within a subtree"""
    if index in ELDER:
        return 'Elder'
    elif index in YOUNGER:
        return 'Younger'
    else:
        return None
    
ALICE = list(range(0, 56))
BOB = list(range(56, 112))
def get_speaker_sex(index):
    """Determine speaker sex of kintype within a subtree"""
    if index in ALICE:
        return 'A'
    elif index in BOB:
        return 'B'
    else:
        return None

# Maps feature to its function
FEATURE_FUNCS = {"kin": get_kintype, "lin": get_lineality, "scr": get_sex_connecting_relative, "gen": get_generation, "sex": get_sex, "ra": get_relative_age, "ss": get_speaker_sex}

# Probabilities for each feature
FEATURE_WEIGHTS = {
    "kin": 0/100, 
    "lin": 100/5/100, 
    "scr": 100/5/100,
    "gen": 100/5/100, 
    "sex": 100/5/100, 
    "ra": 100/5/100, 
    "ss": 0,
}

feat_weights_df = pd.read_csv("feature_based/feature_weights.csv").fillna(0)

# Make file subname
nonzero_keys = [key for key, value in FEATURE_WEIGHTS.items() if value != 0]
features = '_'.join(nonzero_keys)

def get_need_probabilities():
    """Get need probabilities for each position in the kinship tree"""
    probs = np.zeros(114)
    
    freqs = {
        'gma': 21.4, 'gpa': 16.3, 'ant': 4.7, 'unc': 7.1,
        'dad': 438.1, 'mom': 432.1, 'sis': 39.1, 'bro': 50.5,
        'son': 145.7, 'dau': 130.9, 'gda': 2.1, 'gso': 3.3, 'cou': 0.93, 'nie': 1.0, 'nep': 1.2
    }
    
    # Map to tree positions
    gp_pos = list(range(8,12)) + list(range(64,68))
    probs[gp_pos] = [freqs['gma'], freqs['gpa'], freqs['gma'], freqs['gpa']] * 2
    
    parent_pos = [14,19,70,75]
    probs[parent_pos] = [freqs['mom'], freqs['dad']] * 2
    
    sib_pos = list(range(30,34)) + list(range(86,90))
    probs[sib_pos] = [freqs['sis'], freqs['sis'], freqs['bro'], freqs['bro']] * 2
    
    gc_pos = (list(range(52,56)) + list(range(108,112)))
    probs[gc_pos] = [freqs['gda'], freqs['gso'], freqs['gda'], freqs['gso']] * 2
    
    child_pos = [46,47,102,103]
    probs[child_pos] = [freqs['dau'], freqs['son']] * 2

    unc_pos = [15,16,20,21,71,72,76,77]
    probs[unc_pos] = [freqs['unc']] * 8

    ant_pos = [12,13,17,18,68,69,73,74]
    probs[ant_pos] = [freqs['ant']] * 8

    nie_pos = [42,44,48,50,98,100,104,106]
    probs[nie_pos] = [freqs['nie']] * 8

    nep_pos = [43,45,49,51,99,101,105,107]
    probs[nep_pos] = [freqs['nep']] * 8
    #cou_pos=list(range(22,30)) + list(range(34, 42)) + list(range(78,86)) + list(range(90,98))
    #probs[cou_pos] = [freqs['cou']] * len(cou_pos)
    return probs / np.sum(probs)

def load_hypothetical_partitions(tree_index):
    """Load hypothetical partitions for a given tree index"""
    file_path = Path("feature_based") / "output" / "partitions" / f"hyp_partitions_{tree_index}.csv"
    df = pd.read_csv(file_path, header=None)
    return df

def load_rw_partitions(tree_index):
    """Load RW partitions for a given tree index"""
    file_path = Path("feature_based") / "output" / "partitions" / f"rw_partitions_{tree_index}.csv"
    df = pd.read_csv(file_path, header=None)
    freqs = df.iloc[:, 0]
    partitions = df.iloc[:, 1:]
    return freqs, partitions

def calculate_cost(tree_index, partition, need_probs):
    split_index = len(partition) // 2

    # for niblings, the partition is only for bob
    if tree_index == 14:
        split_index = 0

    alice_partition = partition[:split_index]
    bob_partition = partition[split_index:]
    alice_cost = calculate_feature_cost(tree_index, alice_partition, need_probs)
    bob_cost = calculate_feature_cost(tree_index, bob_partition, need_probs)
    speaker_sex_cost = calculate_speaker_sex_cost(tree_index, partition, alice_partition, need_probs)

    return alice_cost + bob_cost + speaker_sex_cost

def calculate_feature_cost(tree_index, partition, need_probs, used_features={'lin', 'scr', 'gen', 'sex', 'ra'}):
    """Calculate communicative cost based on kintype feature uncertainty"""
    total_cost = 0.0
    if round(sum(FEATURE_WEIGHTS.values()), 2) != 1.0:
        raise ValueError(f"Feature weights must sum to 1, currently {sum(FEATURE_WEIGHTS.values())}.")

    full_tree_mapping = subtree_index_map[tree_index]
    # p_f_given_o = 1/len(FEATURE_FUNCS)
    for i, label in enumerate(partition):
        if label == -1:
            continue
        subtree_label_kintypes = np.where(partition == label)[0]
        full_tree_label_kintypes = full_tree_mapping[subtree_label_kintypes]

        # subtract one from all elements here to match zero-indexing of need_probs array
        full_tree_label_kintypes = full_tree_label_kintypes - 1 

        Z = np.sum(need_probs[full_tree_label_kintypes])
        if Z == 0:
            continue

        p_f_given_o = 1 / len(used_features)

        # Apply feature functions
        for func_name in used_features:
            func = FEATURE_FUNCS[func_name]
            # niblings subtree does not have partition for female speaker
            if tree_index == 14 and func_name == 'ss':
                continue
            if func_name == 'ss' and i >= len(partition) // 2:
                continue

            # Maps the index in subtree partition to zero-indexed mastertree index
            true_index = full_tree_mapping[i] - 1
            true_feat = func(true_index)
            if true_feat is None:
                continue
            matching_kintypes = [k for k in full_tree_label_kintypes if func(k) == true_feat]
            Z_feat = np.sum(need_probs[matching_kintypes])

            # probability of choosing object from subtree
            p_o = need_probs[true_index] / np.sum(need_probs[full_tree_mapping - 1])

            if not IS_UNI_FEAT_WEIGHTS:
                p_f_given_o = feat_weights_df[func_name][tree_index - 14]

            p_value_given_label_feat = Z_feat / Z
            surprisal_feat = -np.log2(p_value_given_label_feat)

            total_cost += p_o * p_f_given_o * surprisal_feat
    return total_cost

def calculate_speaker_sex_cost(tree_index, partition, alice_partition, need_probs):
    """Calculate cost of determining speaker's sex"""
    if tree_index == 14:
        return 0.0  # niblings subtree does not have partition for female speaker
    full_tree_mapping = subtree_index_map[tree_index]
    partition_len = len(partition)
    total_cost = 0.0
    for i in range(partition_len // 2):
        true_index = full_tree_mapping[i] - 1
        p_o = need_probs[true_index] / np.sum(need_probs[full_tree_mapping - 1])
        #print(p_o)
        if partition[i] == -1:
            continue
        alice_label = partition[i]
        subtree_label_kintypes = np.where(partition == alice_label)[0]
        full_tree_label_kintypes = full_tree_mapping[subtree_label_kintypes]

        # subtract one from all elements here to match zero-indexing of need_probs array
        full_tree_label_kintypes = full_tree_label_kintypes - 1 
        Z = np.sum(need_probs[full_tree_label_kintypes])
        matching_alice_kintypes = np.where(alice_partition == alice_label)[0]
        full_tree_label_kintypes = full_tree_mapping[matching_alice_kintypes]

        # subtract one from all elements here to match zero-indexing of need_probs array
        full_tree_label_kintypes = full_tree_label_kintypes - 1 
        Z_feat = np.sum(need_probs[full_tree_label_kintypes])
        if Z_feat == 0 or Z == 0:
            continue
        p_f_given_o = feat_weights_df['ss'][tree_index - 14] if not IS_UNI_FEAT_WEIGHTS else 1 / len(FEATURE_FUNCS)
        p_value_given_label_feat = Z_feat / Z
        surprisal_feat = -np.log2(p_value_given_label_feat)
        total_cost += p_o * p_f_given_o * surprisal_feat
    return total_cost

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

def main():
    need_probs = get_need_probabilities()
    
    for tree_index in range(15,20):#range(14, 20):
        print(f"Processing tree index: {tree_index}")

        # Load hypothetical and RW partitions
        hyp_partitions_df = load_hypothetical_partitions(tree_index)
        freqs, rw_partitions_df = load_rw_partitions(tree_index)

        # Calculate feature-based costs for hypothetical partitions
        hyp_feature_based_costs = []
        for partition in hyp_partitions_df.values:
            feature_based_cost = calculate_cost(tree_index, partition, need_probs)
            hyp_feature_based_costs.append(feature_based_cost)
        
        # Calculate feature-based costs for RW partitions
        rw_feature_based_costs = []
        for partition in rw_partitions_df.values:
            feature_based_cost = calculate_cost(tree_index, partition, need_probs)
            rw_feature_based_costs.append(feature_based_cost)
        

        # Load hypothetical scores and add feature-based costs
        hyp_scores_df = load_hypothetical_scores(tree_index)
        hyp_scores_df['feature_cost'] = hyp_feature_based_costs

        # Load real-world scores and add feature-based costs
        rw_scores_df = load_rw_scores(tree_index)
        rw_scores_df['feature_cost'] = rw_feature_based_costs
        rw_scores_df['freqs'] = freqs
        
        # Save all scores
        base_file = Path("feature_based") / "output" / "feature_cost_only"

        if IS_UNI_FEAT_WEIGHTS:
            rw_output_file = base_file / f"rw_all_scores_{tree_index}.csv"
            hyp_output_file = base_file / f"hyp_all_scores_{tree_index}.csv"
        else:
            rw_output_file = base_file / f"rw_all_scores_feat_weights_{tree_index}.csv"
            hyp_output_file = base_file / f"hyp_all_scores_feat_weights_{tree_index}.csv"

        rw_scores_df.to_csv(rw_output_file, index=False)    
        hyp_scores_df.to_csv(hyp_output_file, index=False)
        
if __name__ == "__main__":
    main()
