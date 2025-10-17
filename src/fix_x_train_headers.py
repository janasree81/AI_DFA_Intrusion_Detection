import pandas as pd

columns_path = "data/columns.txt"
x_train_path = "data/processed/X_train.csv"

with open(columns_path) as f:
    columns = [line.strip() for line in f if line.strip()]

df = pd.read_csv(x_train_path, header=0)  # or header=None if no header
df.columns = columns
df.to_csv(x_train_path, index=False)
print("✅ X_train.csv columns updated to match columns.txt")