import pandas as pd

def merge_and_shuffle_csv(file1, file2, output_file):
    # Read both CSV files
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    # Merge the two DataFrames
    merged_df = pd.concat([df1, df2], ignore_index=True)

    # Shuffle the rows randomly
    shuffled_df = merged_df.sample(frac=1, random_state=42).reset_index(drop=True)

    # Write the shuffled DataFrame to a new CSV file
    shuffled_df.to_csv(output_file, index=False)
    print(f"Files have been merged and shuffled into {output_file}")

# Example usage
file1_path = 'cowrie_sessions_20k.csv'
file2_path = 'ssh_legitimate_20k.csv'
output_file_path = 'cowrie_dataset_40k.csv'
merge_and_shuffle_csv(file1_path, file2_path, output_file_path)
