import pandas as pd

# Load the dataset
df = pd.read_csv("your_file.csv")
label_col = df.columns[-1]

# Force 'login_failed' = 'total_connexion' if label == 1
df.loc[df[label_col] == 1, "login_failed"] = df.loc[df[label_col] == 1, "total_connexion"]

# Save the result
df.to_csv("modified_file.csv", index=False)
