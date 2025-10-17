import os
import re
import joblib
import pandas as pd
import pickle

# Paths
MODEL_PATH = os.path.join("src", "models", "rf_model.pkl")
COLUMNS_PATH = os.path.join("data", "columns.txt")
ENCODER_PATH = os.path.join("src", "models", "label_encoder.pkl")

# Precompile DFA regex signatures
patterns = [
    re.compile(r"\battack_signature\b", re.IGNORECASE),
    re.compile(r"\bworm\b", re.IGNORECASE),
    re.compile(r"\bmalicious_pattern\b", re.IGNORECASE),
    re.compile(r"\bback\b", re.IGNORECASE),
    re.compile(r"\bbuffer_overflow\b", re.IGNORECASE),
    re.compile(r"\bftp_write\b", re.IGNORECASE),
    re.compile(r"\bguess_passwd\b", re.IGNORECASE),
    re.compile(r"\bimap\b", re.IGNORECASE),
    re.compile(r"\bipsweep\b", re.IGNORECASE),
    re.compile(r"\bland\b", re.IGNORECASE),
    re.compile(r"\bloadmodule\b", re.IGNORECASE),
    re.compile(r"\bmultihop\b", re.IGNORECASE),
    re.compile(r"\bneptune\b", re.IGNORECASE),
    re.compile(r"\bnmap\b", re.IGNORECASE),
    re.compile(r"\bperl\b", re.IGNORECASE),
    re.compile(r"\bphf\b", re.IGNORECASE),
    re.compile(r"\bpod\b", re.IGNORECASE),
    re.compile(r"\bportsweep\b", re.IGNORECASE),
    re.compile(r"\brootkit\b", re.IGNORECASE),
    re.compile(r"\bsatan\b", re.IGNORECASE),
    re.compile(r"\bsmurf\b", re.IGNORECASE),
    re.compile(r"\bspy\b", re.IGNORECASE),
    re.compile(r"\bteardrop\b", re.IGNORECASE),
    re.compile(r"\bwarezclient\b", re.IGNORECASE),
    re.compile(r"\bwarezmaster\b", re.IGNORECASE),
    re.compile(r"\bnormal\b", re.IGNORECASE),
]

_model = None
_feature_names = None
_label_encoder = None

def load_model_and_columns():
    global _model, _feature_names, _label_encoder
    if _model is None:
        print(f"🔹 Loading model from {MODEL_PATH}")
        _model = joblib.load(MODEL_PATH)
        with open(COLUMNS_PATH, "r") as f:
            _feature_names = [line.strip() for line in f if line.strip()]
        with open(ENCODER_PATH, "rb") as f:
            _label_encoder = pickle.load(f)
    return _model, _feature_names, _label_encoder


def hybrid_predict(features: pd.DataFrame, packet_str: str) -> str:
    """Combine DFA + ML for final decision"""

    # --- Step 1: DFA check ---
    dfa_result = None
    for pat in patterns:
        if pat.search(packet_str):
            dfa_result = pat.pattern.strip("\\b").replace("\\", "")
            break

    # --- Step 2: ML prediction ---
    model, _, label_encoder = load_model_and_columns()
    pred = model.predict(features)[0]
    ml_result = label_encoder.inverse_transform([pred])[0]

    # --- Step 3: Combine Results ---
    if dfa_result:
        if dfa_result.lower() == ml_result.lower():
            return f"✅ Match Detected | DFA & ML both predict: {ml_result}"
        else:
            return f"⚠️ Mismatch | DFA: {dfa_result} | ML: {ml_result}"
    else:
        return f"ML Prediction: {ml_result} (no DFA match)"
