import os
import joblib
import pickle
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder

def build_model():
    """Returns a configured RandomForestClassifier instance."""
    return RandomForestClassifier(n_estimators=200, max_depth=20, random_state=42)

def train_and_evaluate():
    # Load data
    processed_path = os.path.join("data", "processed")
    X_train = pd.read_csv(os.path.join(processed_path, "X_train.csv"))
    X_test = pd.read_csv(os.path.join(processed_path, "X_test.csv"))
    y_train = pd.read_csv(os.path.join(processed_path, "y_train.csv")).squeeze()
    y_test = pd.read_csv(os.path.join(processed_path, "y_test.csv")).squeeze()

    # Encode labels
    le = LabelEncoder()
    y_train_enc = le.fit_transform(y_train)
    y_test_enc = le.transform(y_test)

    print(f"Train: {X_train.shape}, Test: {X_test.shape}")

    # Train Random Forest
    print("🚀 Training Random Forest...")
    rf = build_model()
    rf.fit(X_train, y_train_enc)

    # Evaluate
    y_pred = rf.predict(X_test)
    acc = accuracy_score(y_test_enc, y_pred)
    print(f"✅ Accuracy: {acc:.4f}")
    print("\n📊 Report:\n", classification_report(y_test_enc, y_pred))

    # Save model and encoder
    model_dir = os.path.join("src", "models")
    os.makedirs(model_dir, exist_ok=True)
    joblib.dump(rf, os.path.join(model_dir, "rf_model.pkl"))
    with open(os.path.join(model_dir, "label_encoder.pkl"), "wb") as f:
        pickle.dump(le, f)
    print(f"💾 Model and label encoder saved to: {model_dir}")

if __name__ == "__main__":
    train_and_evaluate()