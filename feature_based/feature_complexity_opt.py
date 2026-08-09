from itertools import combinations
from typing import List, Tuple, Dict, Set, Optional

class KintypeFeatures:
    """Represents the features of a kintype."""
    def __init__(self, generation: int, sex: int, lineality: int, 
                 scr: Optional[int],relative_age: Optional[int], speaker_sex: int):
        self.generation = generation
        self.sex = sex
        self.lineality = lineality
        self.scr = scr
        self.relative_age = relative_age
        self.speaker_sex = speaker_sex
    
    def __getitem__(self, idx: int):
        """Allow indexing into features."""
        features = [self.generation, self.sex, self.lineality, 
                   self.scr, self.relative_age, self.speaker_sex]
        return features[idx]
    
    def __repr__(self):
        return f"KintypeFeatures(gen={self.generation}, sex={self.sex}, " \
               f"lin={self.lineality}, scr={self.scr}, ra={self.relative_age}, " \
               f"ss={self.speaker_sex})"


FEATURE_NAMES = ['gen', 'sex', 'lin', 'scr', 'ra', 'ss']
def feature_name_to_index(feature_name: str) -> int:
    """Convert feature name to index."""
    return FEATURE_NAMES.index(feature_name)


def satisfies_positive_constraints(kintype: KintypeFeatures, 
                                   constraints: Dict[str, Set]) -> bool:
    """Check if a kintype satisfies positive constraints."""
    for feature, valid_values in constraints.items():
        feat_idx = feature_name_to_index(feature)
        if kintype[feat_idx] not in valid_values:
            return False
    return True


def satisfies_relational_constraint(kintype: KintypeFeatures,
                                    rel_constraint: Tuple[str, str, str]) -> bool:
    """
    Check if a kintype satisfies a relational constraint.
    
    rel_constraint is (feature1, operator, feature2) where operator is '=' or '!='
    """
    feat1, operator, feat2 = rel_constraint
    feat1_idx = feature_name_to_index(feat1)
    feat2_idx = feature_name_to_index(feat2)
    
    val1 = kintype[feat1_idx]
    val2 = kintype[feat2_idx]
    
    if operator == '=':
        return val1 == val2
    elif operator == '!=':
        return val1 != val2
    else:
        raise ValueError(f"Unknown operator: {operator}")


def satisfies_negative_constraint(kintype: KintypeFeatures, 
                                  constraints: Dict[str, Set]) -> bool:
    """Check if a kintype satisfies (matches) a negative constraint."""
    for feature, valid_values in constraints.items():
        feat_idx = feature_name_to_index(feature)
        if kintype[feat_idx] in valid_values:
            return False
    return True


def find_negative_constraints(term_features: List[KintypeFeatures],
                              matching_others: List[KintypeFeatures],
                              all_feature_names: List[str]) -> Dict[str, Set]:
    """
    Find minimal set of negative constraints to exclude matching_others
    while keeping all term_features.
    
    Returns: List of feature combinations to negate, or None if impossible
    e.g., [[('sex', 1), ('laterality', 1)]] means NOT(sex=1 AND lat=1)
    """
        
    # Try different sizes of negative constraints
    for neg_size in range(1, len(all_feature_names) + 1):
        for neg_features in combinations(all_feature_names, neg_size):
            # Build constraint: these features have these specific values in other_kf
            neg_constraints = {}
            for feat in neg_features:
                feat_idx = feature_name_to_index(feat)
                values = set([other_kf[feat_idx] for other_kf in matching_others])
                neg_constraints[feat] = values
            
            matching_terms = [
                term_kf for term_kf in term_features
                if satisfies_positive_constraints(term_kf, neg_constraints)
            ]
            
            if len(matching_terms) == 0:
                return neg_constraints

def find_minimal_representation(term_features: List[KintypeFeatures],
                                other_features: List[KintypeFeatures]) -> Dict:
    """
    Find minimal representation using positive, negative, and relational constraints.
    
    Returns: {
        'positive': dict of {feature: set of values},
        'negative': list of lists of (feature, value) tuples,
        'relational': list of (feature1, operator, feature2) tuples
    }
    """    
    best_rep = None
    best_cost = float('inf')
    
    # relational constraints for sex of target and sex of speaker
    relational_constraints = [('sex', '=', 'ss'),
                              ('sex', '!=', 'ss'),
                              ('sex', '=', 'scr'),
                              ('sex', '!=', 'scr'),
                              ('ss', '=', 'scr'),
                              ('ss', '!=', 'scr')] 
    
    # Filter to only those satisfied by all term features
    valid_relational = []
    for rel_constraint in relational_constraints:
        if all(satisfies_relational_constraint(kf, rel_constraint) for kf in term_features):
            valid_relational.append(rel_constraint)
    
    # Try positive features only (no relational, no negative)
    for num_pos in range(1, len(FEATURE_NAMES) + 1):
        if num_pos == 0:
            pos_combos = [()]
        else:
            pos_combos = combinations(FEATURE_NAMES, num_pos)
        
        for pos_features in pos_combos:
            # Build positive constraints
            pos_constraints = {}
            for feat in pos_features:
                feat_idx = feature_name_to_index(feat)
                values = set([kf[feat_idx] for kf in term_features])
                pos_constraints[feat] = values
            
            # Check if this alone works
            matching_others = [
                other_kf for other_kf in other_features
                if satisfies_positive_constraints(other_kf, pos_constraints)
            ]
            
            if len(matching_others) == 0:
                cost = num_pos
                if cost < best_cost:
                    best_cost = cost
                    best_rep = {
                        'positive': pos_constraints,
                        'negative': {},
                        'relational': []
                    }

     # Try positive + negative (no relational)
    for num_pos in range(1, len(FEATURE_NAMES) + 1):
        if num_pos == 0:
            pos_combos = [()]
        else:
            pos_combos = combinations(FEATURE_NAMES, num_pos)
        
        for pos_features in pos_combos:
            # Build positive constraints
            pos_constraints = {}
            for feat in pos_features:
                feat_idx = feature_name_to_index(feat)
                values = set([kf[feat_idx] for kf in term_features])
                pos_constraints[feat] = values
            
            # TODO: Make sure positive matches term_features?
            
            # Find matching others
            matching_others = [
                other_kf for other_kf in other_features
                if satisfies_positive_constraints(other_kf, pos_constraints)
            ]
            
            if len(matching_others) == 0:
                continue  # Already handled in Phase 1
            
            # Try negative constraints
            neg_constraints = find_negative_constraints(term_features,
                                                       matching_others,
                                                       FEATURE_NAMES)
            
            if neg_constraints is not None:
                neg_cost = sum(len(neg) for neg in neg_constraints)
                total_cost = num_pos + neg_cost
                
                if total_cost < best_cost:
                    best_cost = total_cost
                    best_rep = {
                        'positive': pos_constraints,
                        'negative': neg_constraints,
                        'relational': []
                    }

    # Try positive + relational (no negative)
    for num_pos in range(len(FEATURE_NAMES) + 1):
        if num_pos == 0:
            pos_combos = [()]
        else:
            pos_combos = combinations(FEATURE_NAMES, num_pos)
        
        for pos_features in pos_combos:
            # Build positive constraints
            pos_constraints = {}
            for feat in pos_features:
                feat_idx = feature_name_to_index(feat)
                values = set([kf[feat_idx] for kf in term_features])
                pos_constraints[feat] = values
            
            # Try each valid relational constraint
            for rel_constraint in valid_relational:
                current_cost = num_pos + 1
                
                if current_cost >= best_cost:
                    continue
                
                # Find matching others
                matching_others = []
                for other_kf in other_features:
                    if satisfies_positive_constraints(other_kf, pos_constraints):
                        if satisfies_relational_constraint(other_kf, rel_constraint):
                            matching_others.append(other_kf)
                
                if len(matching_others) == 0:
                    if current_cost < best_cost:
                        best_cost = current_cost
                        best_rep = {
                            'positive': pos_constraints,
                            'negative': {},
                            'relational': [rel_constraint]
                        }
    
    # Fallback
    if best_rep is None:
        all_positive = {}
        for feat in FEATURE_NAMES:
            feat_idx = feature_name_to_index(feat)
            values = set([kf[feat_idx] for kf in term_features])
            all_positive[feat] = values
        
        best_rep = {
            'positive': all_positive,
            'negative': {},
            'relational': []
        }
    
    return best_rep

def count_features(representation) -> int:
    """Count total features in a representation."""
    # Full representation with positive, negative, and relational
    positive_count = len(representation.get('positive', {}))
    negative_count = len(representation.get('negative', {}))
    both_count = len(representation.get('both', {}))
    relational_count = len(representation.get('relational', []))
    return positive_count + negative_count + both_count + relational_count

def find_common_features(term_representations: Dict[int, Dict]) -> Dict:
    """
    Find features that can be factored out across all terms.
    Returns dict with 'positive', 'negative', 'both', and 'relational' keys.
    """
    if len(term_representations) == 0 or len(term_representations) == 1:
        return {'positive': {}, 'negative': {}, 'both': {}, 'relational': []}
    
    # Find common positive features
    all_positive_features = [frozenset(rep['positive'].keys()) for rep in term_representations.values()]
    all_negative_features = [frozenset(rep['negative'].keys()) for rep in term_representations.values()]
    common_positive_candidates = frozenset.intersection(*all_positive_features) if all_positive_features else frozenset()
    common_negative_candidates = frozenset.intersection(*all_negative_features) if all_negative_features else frozenset()
    matching_frozensets = set(all_positive_features) & set(all_negative_features)
    common_both_candidates = frozenset.union(*matching_frozensets) if matching_frozensets else frozenset()

    common_positive = {}
    common_negative = {}
    common_both = {}

    for feature in common_positive_candidates:
        # Check if all terms have the SAME constraint for this feature
        pos_feature_constraints = []
        neg_feature_constraints = []
        for _, rep in term_representations.items():
            constraint_pos_values = rep['positive'][feature]
            pos_feature_constraints.append(frozenset(constraint_pos_values))
        
        # If all terms have the same constraint, it's truly common
        if len(set(pos_feature_constraints)) == 1:
            common_positive[feature] = pos_feature_constraints.pop()
        
    for feature in common_negative_candidates:
        # Check if all terms have the SAME constraint for this feature
        neg_feature_constraints = []
        for _, rep in term_representations.items():
            constraint_neg_values = rep['negative'].get(feature, set())
            neg_feature_constraints.append(frozenset(constraint_neg_values))
        
        # If all terms have the same constraint, it's truly common
        if len(set(neg_feature_constraints)) == 1:
            common_negative[feature] = neg_feature_constraints.pop()

    for feature in common_both_candidates:
        # Check if all terms have the SAME constraint for this feature
        both_feature_constraints = set()
        for _, rep in term_representations.items():
            constraint_neg_value = rep['negative'].get(feature, set()).copy()
            if constraint_neg_value:
                both_feature_constraints.add(constraint_neg_value.pop())
            
            constraint_pos_value = rep['positive'].get(feature, set()).copy()
            if constraint_pos_value:
                both_feature_constraints.add(constraint_pos_value.pop())
        # If all terms have the same constraint, it's truly common
        if len(both_feature_constraints) == 1:
            common_both[feature] = both_feature_constraints
    # Find common relational constraints
    all_relational = [set(rep.get('relational', [])) for rep in term_representations.values()]
    common_relational = list(set.intersection(*all_relational)) if all_relational else []
    
    return {
        'positive': common_positive,
        'negative': common_negative,
        'both': common_both,
        'relational': common_relational
    }

def remove_common_features(representation: Dict, common_features: Dict) -> Dict:
    """Remove common features from a representation."""
    try:
        new_positive = {feat: values for feat, values in representation['positive'].items()
                    if feat not in common_features['positive']}
        new_positive = {feat: values for feat, values in representation['positive'].items()
                    if feat not in common_features['both']}
        new_negative = {feat: values for feat, values in representation['negative'].items()
                    if feat not in common_features['negative']}
        new_negative = {feat: values for feat, values in representation['negative'].items()
                    if feat not in common_features['both']}
        new_relational = [rel for rel in representation.get('relational', [])
                        if rel not in common_features['relational']]
        return {
            'positive': new_positive,
            'negative': new_negative,
            'relational': new_relational
        }
    except TypeError as e:
        print(f"Type of representation: {type(representation)}, type of common_features: {type(common_features)}")


def calculate_complexity_no_reduction(partition: List[int],
                        all_kintype_features: List[KintypeFeatures]) -> int:
    """
    Calculate the total complexity of the shortest representation language
    for a given partition.
    
    Args:
        partition: Array mapping kintype indices to term identifiers
        all_kintype_features: List of KintypeFeatures for each kintype in the full tree
        
    Returns:
        Total complexity (number of features needed)
    """
    # Verify partition and feature array lengths
    if len(partition) != len(all_kintype_features):
        raise Exception(f'Partition length ({len(partition)}) and kintype feature length ({len(all_kintype_features)}) not equal')
    # Group kintypes by term
    term_groups = {}
    for i, term in enumerate(partition):
        if term not in term_groups:
            term_groups[term] = []
        term_groups[term].append(i)

    # Find minimal representation for each term 
    term_representations = {} 
    for term, kintype_indices in term_groups.items(): 
        term_features = [all_kintype_features[i] for i in kintype_indices] 
        other_indices = [i for i in range(len(all_kintype_features)) if i not in kintype_indices]
        other_features = [all_kintype_features[i] for i in other_indices] 
        min_rep = find_minimal_representation(term_features, other_features) 
        term_representations[term] = min_rep
    
    # Find common features across all terms
    common_features = find_common_features(term_representations)
    
    if common_features['positive'] or common_features['negative'] or common_features['relational']:
        term_representations['common'] = str(common_features)

    # Calculate total complexity
    complexity = count_features(common_features)
    for term, rep in term_representations.items():
        # Skip the 'common' term since this was already calculated above
        if term == 'common':
            continue
        remaining_rep = remove_common_features(rep, common_features)
        complexity += count_features(remaining_rep)

        rep['positive'] = str(rep['positive']) # convert set to str for json
        rep['negative'] = str(rep['negative']) # convert set to str for json
        if rep['positive'] == '{}':
            del rep['positive']
        if rep['negative'] == '{}':
            del rep['negative']
        if len(rep['relational']) == 0:
            del rep['relational']
    
    # convert set value to list for json
    return term_representations, complexity

def calculate_complexity(partition: List[int], all_kintype_features: List[KintypeFeatures]):
    return calculate_complexity_no_reduction(partition, all_kintype_features)
