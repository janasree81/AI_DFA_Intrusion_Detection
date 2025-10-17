# fix_x_test_headers.py
import pandas as pd

# Path to your columns.txt and X_test.csv
columns_path = "data/columns.txt"
x_test_path = "data/processed/X_test.csv"

# Read the correct column names
with open(columns_path) as f:
    columns = [line.strip() for line in f if line.strip()]
    

# Load X_test.csv (header=0 if it has a header row, header=None if not)
df = pd.read_csv(x_test_path, header=0)  # Use header=None if your CSV has no header row

# Assign the correct column names
df.columns = columns

# Save back to the same file (overwrite)
df.to_csv(x_test_path, index=False)
print(f"✅ X_test.csv columns updated to match columns.txt")