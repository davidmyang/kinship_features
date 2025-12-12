import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

def get_kintype(index):
    """Determine kintype of a kintype"""
    return index

LATERAL_MOM = [0, 1, 2, 3, 8, 9, 12, 13, 14, 15, 16, 56, 57, 58, 59, 64, 65, 68, 69, 70, 71, 72]
LATERAL_DAD = [4, 5, 6, 7, 10, 11, 17, 18, 19, 20, 21, 60, 61, 62, 63, 66, 67, 73, 74, 75, 76, 77]
LATERAL_DAU = [42, 44, 46, 48, 50, 98, 100, 102, 104, 106]
LATERAL_SON = [43, 45, 47, 49, 51, 99, 101, 103, 105, 107]
def get_laterality(index):
    """Determine laterality of a kintype"""
    if index in LATERAL_MOM:
        return 'M'
    elif index in LATERAL_DAD:
        return 'F'
    elif index in LATERAL_DAU:
        return 'D'
    elif index in LATERAL_SON:
        return 'S'
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
FEATURE_PROBS = {"kintype": 1/4, "laterality": 1/4, "generation": 1/4, "sex": 1/4}

def load_partitions(filepath):
    """Load partition data from rwpartitions.txt"""
    partitions = np.loadtxt(filepath)
    frequencies = partitions[:, 0]
    systems = partitions[:, 1:]
    return frequencies, systems

def load_system_mapping(filepath):
    """
    Load mapping between society indices and kinship system numbers.
    Returns a dictionary where key is the society index and value is the kinship system number.
    """
    mapping = {}
    with open(filepath, 'r') as f:
        for i, line in enumerate(f, 1):
            system_num = int(line.strip().split()[1])
            mapping[i] = system_num
    return mapping

def load_language_info(filepath):
    """Load language information from kinterm_orig.txt, skipping header text"""
    languages = []
    index = 1
    with open(filepath, 'r', encoding='utf-8') as f:
        # Skip header until we find the first data line
        for line in f:
            # Look for lines that start with numbers (province numbers)
            if line.strip() and line.strip()[0].isdigit():
                parts = line.strip().split()
                if len(parts) >= 3:  # Valid data line
                    # Name might contain spaces, so join remaining parts
                    name_end = 2
                    while name_end < len(parts) and not parts[name_end].isdigit():
                        name_end += 1
                    name = ''.join(parts[2:name_end])
                    languages.append((index, name))
                    index += 1
    return languages

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

def calculate_cost(partition, need_probs):
    alice_partition = partition[:56]
    bob_partition = partition[56:]
    alice_cost = calculate_feature_cost(alice_partition, need_probs)
    bob_cost = calculate_feature_cost(bob_partition, need_probs)
    return (alice_cost + bob_cost)

def calculate_feature_cost(partition, need_probs):
    """Calculate communicative cost based on kintype feature uncertainty"""
    total_cost = 0.0
    if sum(FEATURE_PROBS.values()) != 1.0:
        raise ValueError("Feature probabilities must sum to 1.")
    
    # p_f_given_o = 1/len(FEATURE_FUNCS)
    for i, label in enumerate(partition):
        if label == -1:
            continue
        label_kintypes = np.where(partition == label)[0]
        Z = np.sum(need_probs[label_kintypes])
        # if Z == 0:
        #     continue
        # p_o = need_probs[i]
        # if p_o == 0:
        #     continue
        # p_value_given_label = p_o / Z
        # surprisal = -np.log2(p_value_given_label)
        # total_cost += p_o * 1 * surprisal

        # Apply feature functions
        for func_name, func in FEATURE_FUNCS.items():

            true_feat = func(i)
            if true_feat is None:
                continue
            matching_kintypes = [k for k in label_kintypes if func(k) == true_feat]
            Z_feat = np.sum(need_probs[matching_kintypes])

            if Z == 0:
                continue
            p_o = need_probs[i]
            if p_o == 0:
                continue
            p_f_given_o = FEATURE_PROBS[func_name]
            p_value_given_label_feat = Z_feat / Z
            surprisal_feat = -np.log2(p_value_given_label_feat)
            total_cost += p_o * p_f_given_o * surprisal_feat
    
    return total_cost

def load_original_scores(base_dir, tree_index=12):
    """Load original cost and complexity calculations"""
    complexity_file = base_dir / "output" / f"complex_{tree_index}_1_1_1_2_rpt1_rand0"
    cost_file = base_dir / "output" / f"cost_{tree_index}_1_1_1_2_6_rpt1_rand0"
    
    # Load complexity scores
    complexities = {}
    with open(complexity_file, 'r') as f:
        for i, line in enumerate(f, 1):
            complexity = float(line.strip().split()[0])
            complexities[i] = complexity / 3 
    
    # Load cost scores
    costs = {}
    with open(cost_file, 'r') as f:
        for i, line in enumerate(f, 1):
            cost = float(line.strip())
            costs[i] = cost
            
    return complexities, costs

def load_artificial_systems(path):
    artificial = pd.read_csv(path, names=['complexity', 'cost', 'index'], header=None)
    return artificial

def create_scatterplots(results, artificial):
    """Create two scatterplots comparing costs vs complexity"""
    valid_data = [r for r in results if r['complexity'] and r['original_cost'] and r['feature_cost']]
    valid_artificial = [r for r in artificial if r['complexity'] and r['cost']]

    y1 = [r['original_cost'] for r in valid_data]
    y2 = [r['feature_cost'] for r in valid_data]
    all_y = y1 + y2
    y_min = -0.05
    y_max = max(valid_artificial['cost'])

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # plot original cost
    x1 = [r['complexity'] for r in valid_data]
    ax1.scatter(x1, y1, alpha=0.8)
    ax1.scatter(valid_artificial['complexity'], valid_artificial['cost'], alpha=0.5)
    ax1.set_xlabel('Complexity')
    ax1.set_ylabel('Communicative Cost')
    ax1.set_title('Original Cost vs Complexity')
    ax1.set_ylim(y_min, y_max)
    
    # plot feature-based cost
    x2 = [r['complexity'] for r in valid_data]
    ax2.scatter(x2, y2, alpha=0.8)
    ax2.scatter(valid_artificial['complexity'], valid_artificial['cost'], alpha=0.5)
    ax2.set_xlabel('Complexity')
    ax2.set_ylabel('Communicative Cost')
    ax2.set_title('Feature Cost vs Complexity')
    ax2.set_ylim(y_min, y_max)
    
    plt.tight_layout()
    plt.show()
    plt.savefig('feature_based/figs/feature_cost_all_comparison.png')
    plt.close()

def main():
    base_dir = Path(".")
    data_dir = Path("murdockdata")
    
    # Load data
    frequencies, systems = load_partitions(data_dir / "rwpartitions.txt")
    system_mapping = load_system_mapping(data_dir / "system_mapping.txt")
    languages = load_language_info(data_dir / "kinterm_orig.txt")
    artificial = load_artificial_systems("./output/combinedscores_12_10_10_10_10_6_rpt1_rand0")
    #print(languages)
    # Load original scores
    complexities, costs = load_original_scores(base_dir)
    need_probs = get_need_probabilities()
    #print(need_probs)
    d_map_file = base_dir / "2025_plots" / f"rwmapindex12.csv"

    d_map = pd.read_csv(d_map_file, names=["analysis_index", "score_index"])
    #print(d_map)
    #print(len(systems[0]))
    # Calculate and compare costs
    results = []
    #print(system_mapping)
    for i, system in enumerate(systems):
        feature_cost = calculate_cost(system, need_probs)

        d_mapped_system = d_map[d_map['analysis_index'] == (i + 1)]
        if (d_mapped_system.empty): # no mapping found between analysis_index and score_index
            continue

        orig_cost = costs.get(d_mapped_system['score_index'].values[0])
        complexity = complexities.get(d_mapped_system['score_index'].values[0])

        #print(f"System {i+1}: Feature Cost = {feature_cost:.4f}, Original Cost = {orig_cost_str}, Complexity = {complexity_str}")
        system_languages = [lang for lang in languages if system_mapping.get(lang[0], -1) == i + 1]
        for lang in system_languages:
            results.append({
                'system_id': i+1,
                'name': lang[1],
                'frequency': frequencies[i],
                'feature_cost': feature_cost,
                'original_cost': orig_cost,
                'complexity': complexity
            })
    #print(results)
    # Sort by feature cost
    #results.sort(key=lambda x: x['feature_cost'])
    # Output results
    # print("\nComparison of costs:")
    # print("System\tLanguage\t\tFeature Cost\tOriginal Cost\tComplexity\tFrequency")
    # print("-" * 100)
    # for r in results:
    #     orig_cost_str = f"{r['original_cost']:.4f}" if r['original_cost'] else "N/A"
    #     complexity_str = f"{r['complexity']:.4f}" if r['complexity'] else "N/A"

    #     # Then use them in the print statement
    #     print(f"{r['system_id']}\t{r['name']:<20}\t{r['feature_cost']:.4f}\t"
    #         f"{orig_cost_str}\t{complexity_str}\t{r['frequency']:.1f}")
    # # Create scatterplots
    create_scatterplots(results, artificial)
if __name__ == "__main__":
    main()