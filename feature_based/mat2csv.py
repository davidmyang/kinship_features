import pandas as pd
from scipy.io import loadmat

def mat2csv(mat_path, csv_path):
    """Convert a .mat file containing 'compactp' matrix to a .csv file."""
    mat_data = loadmat(mat_path)

    data_matrix = mat_data['compactp']

    df = pd.DataFrame(data_matrix)
    df.to_csv(csv_path, index=False, header=False)

def main():
    for i in range(14, 20):
        mat_path = f'output/partitions_tree{i}_1_1_1_2_rpt1.mat'
        csv_path = f'feature_based/output/rw_partitions_{i}.csv'
        mat2csv(mat_path, csv_path)
    
    for i in range(14, 20):
        mat_path = f'output/partitions_tree{i}_1_1_1_4_rpt1.mat'
        csv_path = f'feature_based/output/hyp_partitions_{i}.csv'
        mat2csv(mat_path, csv_path)

if __name__ == "__main__":
    main()

