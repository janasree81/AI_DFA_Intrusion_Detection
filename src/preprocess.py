import os
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

def preprocess():
    # Paths
    data_path = os.path.join("data", "raw", "kdd_test.csv")
    output_dir = os.path.join("data", "processed")
    output_file = os.path.join(output_dir, "train_test_data.pkl")
    columns_file = os.path.join("data", "columns.txt")

    print("🔹 Loading dataset...")
    df = pd.read_csv(data_path, header=None, dtype=str)

    # ✅ KDD Cup 1999 dataset has 41 features + 1 label
    col_names = [
        "duration","protocol_type","service","flag","src_bytes","dst_bytes","land",
        "wrong_fragment","urgent","hot","num_failed_logins","logged_in","num_compromised",
        "root_shell","su_attempted","num_root","num_file_creations","num_shells",
        "num_access_files","num_outbound_cmds","is_host_login","is_guest_login",
        "count","srv_count","serror_rate","srv_serror_rate","rerror_rate","srv_rerror_rate",
        "same_srv_rate","diff_srv_rate","srv_diff_host_rate","dst_host_count",
        "dst_host_srv_count","dst_host_same_srv_rate","dst_host_diff_srv_rate",
        "dst_host_same_src_port_rate","dst_host_srv_diff_host_rate","dst_host_serror_rate",
        "dst_host_srv_serror_rate","dst_host_rerror_rate","dst_host_srv_rerror_rate","labels"
    ]
    df.columns = col_names
    print(f"Dataset shape: {df.shape}")

    # ✅ Encode categorical columns
    categorical_cols = ["protocol_type", "service", "flag"]
    le_dict = {}

    for col in categorical_cols:
        if col in df.columns:
            print(f"Encoding column: {col}")
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
            le_dict[col] = le

    # Convert all remaining non-label cols to numeric
    for col in df.columns:
        if col != "labels":
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # Split features and labels
    X = df.drop("labels", axis=1)
    y = df["labels"]

    # Scale features
    print("Scaling features...")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Drop rare labels (<2 samples), otherwise stratify fails
    value_counts = y.value_counts()
    rare_classes = value_counts[value_counts < 2].index
    if len(rare_classes) > 0:
        print(f"⚠️ Dropping {len(rare_classes)} rare classes: {list(rare_classes)}")
        mask = ~y.isin(rare_classes)
        X_scaled = X_scaled[mask]
        y = y[mask]

    # Train-test split with stratify
    print("Splitting train/test data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42, stratify=y
    )

    print("Train shape:", X_train.shape, y_train.shape)
    print("Test shape:", X_test.shape, y_test.shape)

    # Ensure processed dir exists
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.dirname(columns_file), exist_ok=True)

    # Save preprocessed data
    with open(output_file, "wb") as f:
        pickle.dump((X_train, X_test, y_train, y_test), f)
    print(f"✅ Preprocessed data saved to {output_file}")

    # Save feature columns
    with open(columns_file, "w") as f:
        for col in X.columns:
            f.write(col + "\n")
    print(f"✅ Feature column names saved to {columns_file}")


if __name__ == "__main__":
    preprocess()
