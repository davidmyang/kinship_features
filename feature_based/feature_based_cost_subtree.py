from pathlib import Path
import pandas as pd
import numpy as np

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
LATERAL_MOM = [0, 1, 2, 3, 8, 9, 12, 13, 14, 15, 16, 46, 47, 52,53,54,55,56, 57, 58, 59, 64, 65, 68, 69, 70, 71, 72, 102,103,108,109,110,111]
LATERAL_DAD = [4, 5, 6, 7, 10, 11, 17, 18, 19, 20, 21,46, 47, 52,53,54,55, 60, 61, 62, 63, 66, 67, 73, 74, 75, 76, 77,102,103,108,109,110,111]
def get_laterality(index):
    """Determine laterality of a kintype"""
    if index in LATERAL_MOM:
        return 'M'
    elif index in LATERAL_DAD:
        return 'F'
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

# Maps feature to its function
FEATURE_FUNCS = {"kintype": get_kintype, "laterality": get_laterality, "generation": get_generation, "sex": get_sex}

# Probabilities for each feature
FEATURE_PROBS = {"kintype": 0, "laterality": 0, "generation": 1, "sex": 0}

# Make file subname
nonzero_keys = [key for key, value in FEATURE_PROBS.items() if value != 0 and key != 'kintype']
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
    file_path = Path("feature_based") / "output" / f"hyp_partitions_{tree_index}.csv"
    df = pd.read_csv(file_path, header=None)
    return df

def load_rw_partitions(tree_index):
    """Load RW partitions for a given tree index"""
    file_path = Path("feature_based") / "output" / f"rw_partitions_{tree_index}.csv"
    df = pd.read_csv(file_path, header=None)
    return df

def calculate_cost(tree_index, partition, need_probs):
    split_index = len(partition) // 2
    # for niblings, the partition is only for bob
    if tree_index == 14:
        split_index = 0
    alice_partition = partition[:split_index]
    bob_partition = partition[split_index:]
    alice_cost = calculate_feature_cost(tree_index, alice_partition, need_probs)
    bob_cost = calculate_feature_cost(tree_index, bob_partition, need_probs)
    return (alice_cost + bob_cost)

def calculate_feature_cost(tree_index, partition, need_probs):
    """Calculate communicative cost based on kintype feature uncertainty"""
    total_cost = 0.0
    if sum(FEATURE_PROBS.values()) != 1.0:
        raise ValueError("Feature probabilities must sum to 1.")
    
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

        # Apply feature functions
        for func_name, func in FEATURE_FUNCS.items():
            # maps the index in subtree partition to zero-indexed mastertree index
            true_index = full_tree_mapping[i] - 1
            true_feat = func(true_index)
            if true_feat is None:
                continue
            matching_kintypes = [k for k in full_tree_label_kintypes if func(k) == true_feat]
            Z_feat = np.sum(need_probs[matching_kintypes])
            if Z == 0:
                continue
            # probability of choosing object from subtree
            p_o = need_probs[true_index] / np.sum(need_probs[full_tree_mapping - 1])
            p_f_given_o = FEATURE_PROBS[func_name]
            p_value_given_label_feat = Z_feat / Z
            surprisal_feat = -np.log2(p_value_given_label_feat)
            total_cost += p_o * p_f_given_o * surprisal_feat
    
    return total_cost

def load_rw_scores(tree_index):
    """Load real-world scores"""

    rw_complexity_file = Path("output") / f"complex_{tree_index}_1_1_1_2_rpt1_rand0"
    rw_cost_file = Path("output") / f"cost_{tree_index}_1_1_1_2_6_rpt1_rand0"

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
    hyp_complexity_file = Path("output") / f"complex_{tree_index}_1_1_1_4_rpt1_rand0"
    hyp_cost_file = Path("output") / f"cost_{tree_index}_1_1_1_4_6_rpt1_rand0"

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
    for tree_index in range(14, 20):
        print(f"Processing tree index: {tree_index}")

        # Load hypothetical and RW partitions
        hyp_partitions_df = load_hypothetical_partitions(tree_index)
        rw_partitions_df = load_rw_partitions(tree_index)

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
        hyp_scores_df['feature_based_cost'] = hyp_feature_based_costs

        # Load real-world scores and add feature-based costs
        rw_scores_df = load_rw_scores(tree_index)
        rw_scores_df['feature_based_cost'] = rw_feature_based_costs
        
        # Save all scores
        rw_output_file = Path("feature_based") / "output" / f"rw_all_scores_{features}_{tree_index}.csv"
        rw_scores_df.to_csv(rw_output_file, index=False)
        hyp_output_file = Path("feature_based") / "output" / f"hyp_all_scores_{features}_{tree_index}.csv"
        hyp_scores_df.to_csv(hyp_output_file, index=False)
        
if __name__ == "__main__":
    main()
