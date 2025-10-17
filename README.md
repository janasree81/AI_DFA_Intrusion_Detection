Hybrid Intrusion Detection System (DFA + ML)

Overview
This project implements a Hybrid Intrusion Detection System (IDS) that combines Deterministic Finite Automata (DFA) based pattern recognition with a Machine Learning model (Random Forest) to detect and classify network attacks such as Neptune, Smurf, Portsweep, and others from the KDD Cup 99 dataset.
The system is powered by Flask for an interactive web-based interface, allowing users to manually input network features and observe both DFA rule-based and ML-based predictions in real-time.

Features

Hybrid Detection: Combines DFA regex matching and ML classification

Real-time Prediction: Web interface for manual packet input and instant results

Logging System: Every prediction is stored in web_ui_predictions.log

ML Model: Trained on preprocessed KDD data using Random Forest

Flask Web UI: Modern cyber-themed interface with colored result output

Extensible Design: Modular structure for easy integration and retraining

Project Structure
data/
┣ raw/
┃ ┣ kddtrain.csv
┃ ┗ kddtest.csv
┣ processed/
┃ ┣ X_train.csv
┃ ┣ y_train.csv
┃ ┣ X_test.csv
┃ ┗ y_test.csv
┗ columns.txt

notebooks/
┗ train_and_evaluate.ipynb

src/
┣ models/
┃ ┣ rf_model.pkl
┃ ┗ label_encoder.pkl
┣ PYRASCHE/
┃ ┣ integrated_regex_model.cpython-.pyc
┃ ┣ dfa.cpython-.pyc
┃ ┗ preprocess.cpython-.pyc
┣ integrated_regex_model.py
┣ web_ui.py
┣ model.py
┣ preprocess.py
┣ aiengine.py
┣ dashboard.py
┣ simulate_attack.py
┗ utils.py

main.py
requirements.txt
README.md
results_log.csv
web_ui_predictions.log

How to Run

Step 1 – Create Virtual Environment
python -m venv venv
Activate it:
Windows: venv\Scripts\activate
macOS/Linux: source venv/bin/activate

Step 2 – Install Dependencies
pip install -r requirements.txt

Step 3 – Launch the Web UI
python main.py

Then open your browser and visit:
http://127.0.0.1:5000/

Step 4 – Enter Feature Values
Fill in the numerical feature fields.
Enter the packet string (example: proto=tcp flags=S).
Click Predict to view the result.

You will see:
🟢 ML Prediction: normal → Safe traffic
🔴 ⚠️ ALERT: DFA detected malicious traffic → Attack detected

Model Information
Algorithm: RandomForestClassifier
Dataset: KDD Cup 99
Training Data: Processed using feature engineering and encoding
Hybrid Rule Engine: Regex DFA to identify known attack signatures before ML model prediction

Logs
All predictions are recorded in web_ui_predictions.log
Each entry contains:
Timestamp | Result | Packet String

Requirements
flask
pandas
scikit-learn
joblib
numpy
pickle5
gunicorn

Testing
A simple test file exists under tests/test_prediction.py
Run the test: python tests/test_prediction.py
Expected Output: ✅ Tests passed successfully!

Author
Developed by [JANASREE , HARINA MAVEERKUMAR , DHARSHINI]
For academic and research purposes.
Hybrid DFA + ML Intrusion Detection | 2025

Disclaimer
This project is for educational and research purposes only.
Do not deploy in production environments without proper testing and validation.