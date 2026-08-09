import pandas as pd
from scipy.io import loadmat

def mat2csv(mat_path, csv_path, is_rw):
    """Convert a .mat file with partitions to a .csv file."""
    mat_data = loadmat(mat_path)

    data_matrix = mat_data['compactp']

    df = pd.DataFrame(data_matrix)
    if is_rw:
        freqs = mat_data['rwfreqs'].flatten()
        df.insert(0, 'Frequency', freqs)
    df.to_csv(csv_path, index=False, header=False)

def main():
    for i in range(14, 20):
        mat_path = f'input/partitions_tree{i}_1_1_1_2_rpt1.mat'
        csv_path = f'feature_based/output/rw_partitions_{i}.csv'
        mat2csv(mat_path, csv_path, is_rw=True)
    
    for i in range(14, 20):
        mat_path = f'input/partitions_tree{i}_1_1_1_4_rpt1.mat'
        csv_path = f'feature_based/output/hyp_partitions_{i}.csv'
        mat2csv(mat_path, csv_path, is_rw=False)

    # Convert full tree partitions
    mat_path = 'input/partitions_tree12_1_1_1_2_rpt1.mat'
    csv_path = 'feature_based/output/rw_partitions_12.csv'
    mat2csv(mat_path, csv_path, is_rw=True)

if __name__ == "__main__":
    main()

