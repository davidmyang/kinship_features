from pathlib import Path
import csv

full = list(range(9, 23)) + list(range(31, 35)) + list(range(47, 49)) + list(range(53, 57)) + list(range(65, 79)) + list(range(87, 91)) + list(range(99, 113))
niblings = [99,100,101,102,103,104,105,106,107,108]
grandparents = [9,10,11,12, 65,66,67,68]
grandchildren = [53,54,55,56, 109,110,111,112]
aunts = [13,14,15,18,19, 69,70,71,74,75]
siblings = [31,32,33,34, 87,88,89,90]
uncles = [16,17,20,21,22, 72,73,76,77,78]

FULL_TREE_INDEX = 12

tree_index_map = {
    FULL_TREE_INDEX: full,
    14: niblings,
    15: grandparents,
    16: grandchildren,
    17: aunts,
    18: siblings,
    19: uncles,
}

base_dir = Path(".")
input_dir = Path("input")
output_dir = Path("feature_based/output")

def make_full_tree_partitions():
    dlinkout_path = input_dir / f'dlinkout_{FULL_TREE_INDEX}_1_1_9_3_rpt1.txt'
    dlinkout = []
    try:
        with open(dlinkout_path, "r") as file:
            lines = file.readlines()
            for line in lines:
                # skip last line in dlinkout files
                if line == lines[-1]:
                    continue
                dlinkout.append([int(s) for s in line.split()])
    except FileNotFoundError:
        print(f'File {dlinkout_path} not found')
    except Exception as e:
        print(f"An error occurred: {e}")
    dlinkin_path = input_dir / f'dlinkin_{FULL_TREE_INDEX}_1_1_9_4.txt'
    dlinkin = []
    try:
        with open(dlinkin_path, "r") as file:
            lines = file.readlines()
            for line in lines:
                dlinkin.append([int(s, 36) for s in line.split()])
    except FileNotFoundError:
        print(f'File {dlinkout_path} not found')
    except Exception as e:
        print(f"An error occurred: {e}")
   
    final_partitions = []

    try:
        partition_len = len(tree_index_map[FULL_TREE_INDEX])
        for i, system in enumerate(dlinkout):
            final_partition = [-1] * partition_len
            label = 1
            for category in system:
                if category > len(dlinkin):
                    continue
                indices = dlinkin[category] 
                for index in indices:
                    final_partition[index - 1] = label
                label += 1
            final_partitions += [final_partition]
            #print(final_partition)
    except Exception as e:
        print(f'error: {e} \n index: {i} \n dlinkout: {dlinkout_path} \n dlinkin length: {len(dlinkin)} \n subtree: {FULL_TREE_INDEX} \n system: {system} \n category: {category}')
   
    output_path = output_dir / f'hyp_partitions_{FULL_TREE_INDEX}.csv'
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(final_partitions)

def main():
    make_full_tree_partitions()

if __name__ == "__main__":
    main()