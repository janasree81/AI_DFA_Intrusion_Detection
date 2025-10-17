import pandas as pd
from dfa import decision_feedback_analysis
import numpy as np
import joblib
import os
import pickle

def load_processed_data():
    X_test = pd.read_csv("data/processed/X_test.csv")
    y_test = pd.read_csv("data/processed/y_test.csv").squeeze()
    return X_test, y_test

def main():
    print("🧠 Loading processed data...")
    X_test, y_test = load_processed_data()

    print("🔄 Loading trained Random Forest model and label encoder...")
    model_path = os.path.join("src", "models", "rf_model.pkl")
    encoder_path = os.path.join("src", "models", "label_encoder.pkl")
    rf = joblib.load(model_path)
    with open(encoder_path, "rb") as f:
        le = pickle.load(f)

    print("🔁 Encoding labels...")
    y_test_enc = le.transform(y_test)

    print("🔮 Predicting...")
    predicted_classes = rf.predict(X_test)

    print("📊 Running DFA (Decision Feedback Analysis)...")
    feedback = decision_feedback_analysis(predicted_classes, y_test_enc)
    for i in range(5):
        pred_label = le.inverse_transform([predicted_classes[i]])[0]
        actual_label = le.inverse_transform([y_test_enc[i]])[0]
        print(f"Sample {i+1}: Prediction={pred_label}, Actual={actual_label}, Feedback={feedback[i]}")

    accuracy = np.mean(predicted_classes == y_test_enc)
    print(f"✅ Test Accuracy: {accuracy:.4f}")

if __name__ == "__main__":
    main()