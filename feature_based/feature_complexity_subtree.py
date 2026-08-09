import numpy as np

# Zero-indexed full tree indices for grandparent kintypes
GP_INDEX = [8, 9, 10, 11, 64, 65, 66, 67]

# The lists for each feature are zero-indexed full tree indices
LATERAL_MOM = [0, 1, 2, 3, 8, 9, 12, 13, 14, 15, 16, 46, 47, 52,53,54,55,56, 57, 58, 59, 64, 65, 68, 69, 70, 71, 72, 102,103,108,109,110,111]
LATERAL_DAD = [4, 5, 6, 7, 10, 11, 17, 18, 19, 20, 21,46, 47, 52,53,54,55, 60, 61, 62, 63, 66, 67, 73, 74, 75, 76, 77,102,103,108,109,110,111]
def get_laterality(index):
    """Determine laterality of a kintype"""
    if index in LATERAL_MOM:
        return 0
    elif index in LATERAL_DAD:
        return 1
    else:
        return None
    
def get_generation(index):
    """Determine generation of a kintype"""
    if index in list(range(8, 12)) + list(range(64, 68)):
        return 2  # Grandparents
    elif index in list(range(12, 22)) + list(range(68, 78)):
        return 1  # Parents and aunts/uncles
    elif index in list(range(30, 34)) + list(range(86, 90)):
        return 0   # Siblings
    elif index in list(range(42, 52)) + list(range(98, 108)):
        return -1  # Children and nieces/nephews
    elif index in list(range(52, 56)) + list(range(108, 112)):
        return -2  # Grandchildren
    else:
        return None

FEMALE = [8, 10, 12, 13, 14, 17, 18, 30, 31, 42, 44, 46, 48, 50, 52, 54, 64, 66, 68, 69, 70, 73, 74, 86, 87, 98, 100, 102, 104, 106, 108, 110]
MALE = [9, 11, 15, 16, 19, 20, 21, 32, 33, 43, 45, 47, 49, 51, 53, 55, 65, 67, 71, 72, 75, 76, 77, 88, 89, 99, 101, 103, 105, 107, 109, 111]
def get_sex(index):
    """Determine sex of a kintype"""
    if index in FEMALE:
        return 0
    elif index in MALE:
        return 1
    else:
        return None
    
ELDER = [13, 16, 18, 21, 31, 33, 69, 72, 74, 77, 87, 89]
YOUNGER = [12, 15, 17, 20, 30, 32, 68, 71, 73, 76, 86, 88]
def get_relative_age(index):
    """Determine relative age of a kintype within a subtree"""
    if index in ELDER:
        return 1
    elif index in YOUNGER:
        return 0
    else:
        return None

def get_speaker_sex(index):
    """Determine sex of speaker"""
    if index in list(range(0, 56)):
        return 0 # Female speaker
    elif index in list(range(56, 112)):
        return 1 # Male speaker
    else:
        return None

def make_feature_arr(index):
    """Create feature array for a given kintype index"""
    features = []
    features.append(get_generation(index))
    features.append(get_sex(index))
    features.append(get_laterality(index))
    features.append(get_relative_age(index))
    features.append(get_speaker_sex(index))
    return features

def make_feature_matrix():
    """Create feature matrix for all grandparent kintypes"""
    feature_matrix = []
    for index in GP_INDEX:
        feature_matrix.append(make_feature_arr(index))
    return feature_matrix

def calculate_feature_complexity(partition, subtree):
    """Calculate feature complexity as the number of unique feature combinations"""
    feature_matrix = make_feature_matrix()
    split_index = len(feature_matrix) // 2
    alice_matrix = feature_matrix[:split_index]
    bob_matrix = feature_matrix[split_index:]
    alice_partition = partition[:split_index]
    bob_partition = partition[split_index:]

    total_complexity = 0

    # First reduce feature matrix for Alice
    eliminated_indices = [-1] * len(partition)
    for label in np.unique(alice_partition):
        label_kintypes = np.where(partition == label)[0]
        matching_matrix = [alice_matrix[k] for k in label_kintypes]
        more_than_max = arrays_have_differences(matching_matrix, max_differences=1)
        for k in label_kintypes:
            eliminated_indices[k] = more_than_max[1]
    
    # Then reduce feature matrix for Bob
    for label in np.unique(bob_partition):
        label_kintypes = np.where(partition == label)[0]
        matching_matrix = [bob_matrix[k] for k in label_kintypes]
        more_than_max = arrays_have_differences(matching_matrix, max_differences=1)
        for k in label_kintypes:
            eliminated_indices[k + len(alice_partition)] = more_than_max[1]
    
    # Calculate total complexity
    for label in np.unique(partition):
        label_kintypes = np.where(partition == label)[0]
        matching_matrix = [feature_matrix[k] for k in label_kintypes]
        more_than_max = arrays_have_differences(matching_matrix, max_differences=2)
        if more_than_max[0]:
            total_complexity += 2
        else:
            if eliminated_indices[label_kintypes[0]] != -1:
                total_complexity += 1

def arrays_have_differences(arrays, max_differences):
    """Check if there are more than max_differences different values at any index across arrays"""
    if not arrays:
        return False
    
    length = len(arrays[0])
    differences = 0
    index_of_difference = -1
    
    for i in range(length):
        first_value = arrays[0][i]
        for j in range(1, len(arrays)):
            if arrays[j][i] != first_value:
                differences += 1
                index_of_difference = i
                break
        if differences > max_differences:
            return (True, -1)
    
    return (False, index_of_difference)