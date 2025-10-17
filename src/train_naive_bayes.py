# train_naive_bayes.py

import os
import pickle
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # project root
DATA_PATH = os.path.join(BASE_DIR,  "data", "processed", "train_test_data.pkl")
MODEL_PATH = os.path.join(BASE_DIR, "models", "naive_bayes_model.pkl")

print("🔹 Loading preprocessed data...")
with open(DATA_PATH, "rb") as f:
    X_train, X_test, y_train, y_test = pickle.load(f)

print("🔹 Training Naive Bayes model...")
nb = GaussianNB()
nb.fit(X_train, y_train)

print("🔹 Evaluating model...")
y_pred = nb.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Save trained model
os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
with open(MODEL_PATH, "wb") as f:
    pickle.dump(nb, f)

print(f"✅ Naive Bayes model saved to {MODEL_PATH}")
