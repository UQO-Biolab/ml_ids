import pandas as pd

# Load the dataset
df = pd.read_csv("modified_file2.csv")
label_col = df.columns[-1]

# Mask for rows where label == 1 and total_connexion > 2
mask = (df[label_col] == 1) & (df["total_connexion"] > 2)

# Calculate and assign with rounding to 2 decimal places
df.loc[mask, "avg_time_between_failed"] = (df.loc[mask, "duration"] / df.loc[mask, "total_connexion"]).round(2)

# Save the result
df.to_csv("modified_file3.csv", index=False)
