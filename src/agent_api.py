from flask import Flask, request, jsonify
import pandas as pd
import joblib
import pickle
import os
from integrated_regex_model import hybrid_predict

app = Flask(__name__)

# Load feature names for input validation
COLUMNS_PATH = os.path.join("data", "columns.txt")
with open(COLUMNS_PATH, "r") as f:
    feature_names = [line.strip() for line in f if line.strip()]

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    # Expecting: {"features": {...}, "packet_str": "..."}
    features = data.get("features")
    packet_str = data.get("packet_str", "")

    # Convert features dict to DataFrame
    feats_df = pd.DataFrame([features], columns=feature_names)
    result = hybrid_predict(feats_df, packet_str)
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)