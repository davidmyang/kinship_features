import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

ALICE_TREE_MAPPING = np.array(list(range(9, 23)) + list(range(31, 35)) + list(range(47, 49)) 
                             + list(range(53, 57)))
BOB_TREE_MAPPING = np.array(list(range(65, 79)) + list(range(87, 91)) 
                             + list(range(99, 113)))

def get_kintype(index):
    """Determine kintype of a kintype"""
    return index

# The lists for each feature are zero-indexed full tree indices
LATERAL_MOM = [0, 1, 2, 3, 8, 9, 12, 13, 14, 15, 16, 46, 47, 52,53,56, 57, 58, 59, 64, 65, 68, 69, 70, 71, 72, 102,103,108,109,110,111]
LATERAL_DAD = [4, 5, 6, 7, 10, 11, 17, 18, 19, 20, 21,46, 47, 54,55, 60, 61, 62, 63, 66, 67, 73, 74, 75, 76, 77,102,103,108,109,110,111]
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
    

# Maps feature to its function
FEATURE_FUNCS = {"kin": get_kintype, "lat": get_laterality, "gen": get_generation, "sex": get_sex, "relative_age": get_relative_age}

# Probabilities for each feature
FEATURE_WEIGHTS = {
    "kin": 100/100, 
    "lat": 0/100, 
    "gen": 0/100, 
    "sex": 0/100, 
    "relative_age": 0/100, 
    "speaker_sex": 0/100
}

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
    file_path = Path("feature_based") / "output" / f"hyp_partitions_{tree_index}.csv"
    df = pd.read_csv(file_path, header=None)
    return df

def load_rw_partitions(tree_index):
    """Load RW partitions for a given tree index"""
    file_path = Path("feature_based") / "output" / f"rw_partitions_{tree_index}.csv"
    df = pd.read_csv(file_path, header=None)
    freqs = df.iloc[:, 0]
    partitions = df.iloc[:, 1:]
    return freqs, partitions

def calculate_cost(partition, need_probs):
    split_index = 24
    alice_partition = partition[:split_index]
    bob_partition = partition[split_index:]
    alice_cost = calculate_feature_cost(alice_partition, need_probs, ALICE_TREE_MAPPING)
    bob_cost = calculate_feature_cost(bob_partition, need_probs, BOB_TREE_MAPPING)
    #speaker_sex_cost = calculate_speaker_sex_cost(tree_index, partition, need_probs)
    return (alice_cost + bob_cost) #+ speaker_sex_cost

def calculate_feature_cost(partition, need_probs, tree_mapping):
    """Calculate communicative cost based on kintype feature uncertainty"""
    total_cost = 0.0
    if sum(FEATURE_WEIGHTS.values()) != 1.0:
        raise ValueError("Feature probabilities must sum to 1.")
    
    for i, label in enumerate(partition):
        if label == -1:
            continue
        label_kintypes = np.where(partition == label)[0]
        full_tree_label_kintypes = tree_mapping[label_kintypes]
        print(partition)
        print(full_tree_label_kintypes)
        # subtract one from all elements here to match zero-indexing of need_probs array
        full_tree_label_kintypes = full_tree_label_kintypes - 1 

        Z = np.sum(need_probs[full_tree_label_kintypes])
        if Z == 0:
            continue

        # Apply feature functions
        for func_name, func in FEATURE_FUNCS.items():
            true_index = tree_mapping[i] - 1

            true_feat = func(true_index)
            if true_feat is None:
                continue
            matching_kintypes = [k for k in full_tree_label_kintypes if func(k) == true_feat]
            Z_feat = np.sum(need_probs[matching_kintypes])

            p_o = need_probs[true_index]
            if p_o == 0:
                continue
            p_f_given_o = FEATURE_WEIGHTS[func_name]
            p_value_given_label_feat = Z_feat / Z
            surprisal_feat = -np.log2(p_value_given_label_feat)
            total_cost += p_o * p_f_given_o * surprisal_feat
    
    return total_cost

# def calculate_speaker_sex_cost(tree_index, partition, need_probs):
#     """Calculate cost of determining speaker's sex"""
#     if tree_index == 14:
#         return 0.0  # niblings subtree does not have partition for female speaker
#     full_tree_mapping = subtree_index_map[tree_index]
#     partition_len = len(partition)
#     total_cost = 0.0
#     for i in range(partition_len // 2):
#         true_index = full_tree_mapping[i] - 1
#         p_o = need_probs[true_index] / np.sum(need_probs[full_tree_mapping - 1])
#         if partition[i] == -1:
#             continue
#         alice_label = partition[i]
#         bob_label = partition[(partition_len // 2) + i]
#         p_f_given_o = FEATURE_WEIGHTS['speaker_sex']
#         p_value_given_label_feat = 1.0 if alice_label != bob_label else 0.5
#         surprisal_feat = -np.log2(p_value_given_label_feat)
#         total_cost += p_o * p_f_given_o * surprisal_feat
#     return total_cost

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
    hyp_complexity_file = Path("input") / f"complex_{tree_index}_1_1_9_3_rpt1_rand0"
    hyp_cost_file = Path("input") / f"cost_{tree_index}_1_1_9_3_6_rpt1_rand0"

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
    tree_index = 12
    print(f"Processing tree index: {tree_index}")

    # Load hypothetical and RW partitions
    hyp_partitions_df = load_hypothetical_partitions(tree_index)
    freqs, rw_partitions_df = load_rw_partitions(tree_index)

    # Calculate feature-based costs for hypothetical partitions
    hyp_feature_based_costs = []
    for partition in hyp_partitions_df.values:
        feature_based_cost = calculate_cost(partition, need_probs)
        hyp_feature_based_costs.append(feature_based_cost)

    # Calculate feature-based costs for RW partitions
    rw_feature_based_costs = []
    for partition in rw_partitions_df.values:
        feature_based_cost = calculate_cost(partition, need_probs)
        rw_feature_based_costs.append(feature_based_cost)



    # Load hypothetical scores and add feature-based costs
    hyp_scores_df = load_hypothetical_scores(tree_index)
    hyp_scores_df['feature_based_cost'] = hyp_feature_based_costs

    # Load real-world scores and add feature-based costs
    rw_scores_df = load_rw_scores(tree_index)
    rw_scores_df['feature_based_cost'] = rw_feature_based_costs
    rw_scores_df['freqs'] = freqs
    
    # Save all scores
    rw_output_file = Path("feature_based") / "output" / f"rw_all_scores_{features}_{tree_index}.csv"
    rw_scores_df.to_csv(rw_output_file, index=False)
    hyp_output_file = Path("feature_based") / "output" / f"hyp_all_scores_{features}_{tree_index}.csv"
    hyp_scores_df.to_csv(hyp_output_file, index=False)
        
if __name__ == "__main__":
    main()