import os
import csv
import time
import joblib
import numpy as np
import pandas as pd

# Local imports
from integrated_regex_model import hybrid_predict

# ---- Config ----
MODEL_PATH = os.path.join("src", "models", "rf_model.pkl")
COLUMNS_PATH = os.path.join("data", "columns.txt")
X_TEST_PATH = os.path.join("data", "processed", "X_test.csv")
LOG_PATH = "results_log.csv"

def load_model_and_columns():
    print("🔹 Loading trained model + columns...")
    model = joblib.load(MODEL_PATH)
    with open(COLUMNS_PATH, "r") as f:
        feature_names = [line.strip() for line in f if line.strip()]
    print(f"✅ Loaded model and {len(feature_names)} feature names")
    return model, feature_names

def stream_preprocessed_rows(x_test_path, feature_names, limit=None):
    """
    Yield feature vectors from preprocessed X_test.csv in the same order
    as feature_names. Assumes X_test.csv columns align with training.
    """
    print(f"📥 Streaming rows from: {x_test_path}")
    with open(x_test_path, newline="") as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            feats = [float(row[col]) for col in feature_names]
            feats_df = pd.DataFrame([feats], columns=feature_names)
            yield feats_df
            count += 1
            if limit and count >= limit:
                break

def main():
    _, feature_names = load_model_and_columns()

    benign_packet_str = "src_ip=10.0.0.5 dst_ip=10.0.0.9 proto=tcp flags=S"
    suspicious_packet_str = "proto=tcp flags=SF ... attack_signature ..."

    # Open log file for writing
    with open(LOG_PATH, "w", newline="", encoding="utf-8") as logfile:
        writer = csv.writer(logfile)
        writer.writerow(["Index", "Prediction", "AlertType"])  # header

        i = 0
        for feats_df in stream_preprocessed_rows(X_TEST_PATH, feature_names, limit=10):
            pkt_str = suspicious_packet_str if (i % 3 == 0) else benign_packet_str

            result = hybrid_predict(feats_df, pkt_str)
            print(f"[{i:02d}] → {result}")

            alert_type = "DFA" if "DFA" in result else "ML"
            writer.writerow([i, result, alert_type])

            time.sleep(0.2)
            i += 1

if __name__ == "__main__":
    main()