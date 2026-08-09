import csv
import pandas as pd
from feature_based_cost_subtree import load_rw_partitions

SUBSYSTEM_FEATURES_MAP = {
    14: ["nib_sex", "nib_ra", "nib_scr", "nib_lin"],
    15: ["gp_sex", "gp_scr"],
    16: ["gc_sex", "gc_scr"],
    17: ["aunt_scr", "aunt_ra", "aunt_lin"],
    18: ["sib_sex", "sib_ra"],
    19: ["unc_scr", "unc_ra", "unc_lin"],
}

FEATURE_COUNT_MAP = {
    "nib_sex": [2, 5, 6, 7, 13, 14, 15, 16, 19, 20, 23],
    "nib_ra": [10, 17, 18], # NOTE: relative age between ego's siblings, not niblings themselves
    "nib_scr": [1, 2, 3, 7, 8, 9, 10, 11, 12, 14, 18, 21],

    # NOTE: difference between niece/nephew vs children
    "nib_lin": [3, 4, 5, 7, 8, 9, 10, 11, 12, 14, 16, 17, 18, 19, 20, 21, 22, 23],
    "gp_sex": [1, 3, 4, 6, 7, 10, 13, 14, 18, 19],
    "gp_scr": [3, 5, 8, 12, 18, 19],
    "gc_sex": [2, 4, 12, 15, 16, 18],
    "gc_scr": [3, 4, 6, 8, 9, 11, 12, 14, 20],
    "aunt_scr": [1, 2, 5, 7, 8, 9, 12],
    "aunt_ra": [6, 7, 10, 11], #NOTE: should i include the ones that have ra on one side?
    "aunt_lin": [1, 3, 5, 6, 7, 8, 10, 11, 12],
    "sib_sex": [1, 2, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 18, 19, 20, 22, 23, 24, 25, 26, 27, 28, 29, 36, 37, 38, 39, 40, 41],
    "sib_ra": [1, 3, 4, 13, 15, 19, 21, 22, 24, 30, 32, 33, 34],
    "unc_scr": [1, 2, 3, 6, 8, 9, 12, 13],
    "unc_ra": [6, 7, 10, 13], #NOTE: Same as aunts
    "unc_lin": [2, 3, 4, 6, 7, 9, 10, 11, 12],
}


def get_subsystem_feature_count(filepath, feature):
    count = 0
    df = pd.read_csv(filepath, header=None)
    for row in FEATURE_COUNT_MAP[feature]:
        count += int(df.iloc[row - 1, 0])
    return count


def get_feature_weights():
    feature_weights_df = pd.DataFrame(columns=["kin", "gen", "sex", "scr", "ra", "lin", "ss"])
    for i in range(14, 20):
        freqs, partitions_df = load_rw_partitions(i)
        filepath = f"feature_based/output/partitions/rw_partitions_{i}.csv"
        for feature in SUBSYSTEM_FEATURES_MAP[i]:
            feature_count = get_subsystem_feature_count(filepath, feature)
            feature_prob = feature_count / sum(freqs)
            raw_feature = feature.split("_")[1]
            feature_weights_df.loc[i - 14, raw_feature] = feature_prob

        if i != 14:
            speaker_sex_prob = get_speaker_sex_weight(partitions_df, freqs)
            feature_weights_df.loc[i - 14, "ss"] = speaker_sex_prob
    
    # normalize the weights so that they sum to 1
    norm_df = feature_weights_df.div(feature_weights_df.sum(axis=1), axis=0)
    return norm_df

def get_speaker_sex_weight(partitions_df, freqs):
    total_different = 0
    total_partitions = len(partitions_df)
    for i, partition in enumerate(partitions_df.values):
        split_index = len(partition) // 2
        alice_partition = partition[:split_index]
        bob_partition = partition[split_index:]
        num_different = 0

        for j in range(len(alice_partition)):
            if alice_partition[j] != bob_partition[j]:
                num_different += 1
        total_different += num_different / len(alice_partition) * freqs[i]
    return total_different / sum(freqs)

if __name__ == "__main__":
    norm_df = get_feature_weights()
    norm_df.to_csv("feature_based/feature_weights.csv", index=False)

