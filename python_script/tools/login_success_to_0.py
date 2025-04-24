import pandas as pd

# Load the file
df = pd.read_csv("your_file.csv")

# Identify the name of the last column (label)
label_col = df.columns[-1]

# Set the 'login_success' column to 0 when the label is 1
df.loc[df[label_col] == 1, "login_success"] = 0

# (Optional) Save the modified file
df.to_csv("your_modified_file.csv", index=False)
