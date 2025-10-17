from flask import Flask, render_template_string, request
import pandas as pd
from src.integrated_regex_model import hybrid_predict
import os
import datetime

# Load feature names
COLUMNS_PATH = os.path.join("data", "columns.txt")
with open(COLUMNS_PATH, "r") as f:
    feature_names = [line.strip() for line in f if line.strip()]

app = Flask(__name__)

HTML_FORM = """
<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title> Intrusion Detection System</title>
<style>
  /* ==== RESET & BASE ==== */
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', sans-serif; }
  body {
    background: radial-gradient(circle at top, #0a0a0f 0%, #010101 100%);
    color: #eee;
    overflow-x: hidden;
    min-height: 100vh;
    perspective: 1000px;
  }

  /* ==== BACKGROUND ANIMATION ==== */
  .matrix-bg {
    position: fixed;
    top: 0; left: 0; width: 100%; height: 100%;
    z-index: -2;
    background: repeating-linear-gradient(
      0deg, rgba(0,255,128,0.05) 0px, rgba(0,255,128,0.1) 2px, transparent 3px, transparent 6px
    );
    animation: matrixMove 12s linear infinite;
  }
  @keyframes matrixMove {
    from { background-position-y: 0; }
    to { background-position-y: 100%; }
  }

  /* ==== 3D CARD CONTAINER ==== */
  .container {
    max-width: 720px;
    margin: 70px auto;
    padding: 40px;
    background: rgba(0,0,0,0.75);
    border: 1px solid rgba(0,255,128,0.3);
    border-radius: 20px;
    box-shadow: 0 0 25px rgba(0,255,128,0.3), inset 0 0 40px rgba(0,255,128,0.1);
    transform: rotateY(0deg);
    transition: transform 0.8s;
    animation: fadeIn 1.5s ease;
  }
  .container:hover {
    transform: rotateY(2deg);
  }
  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
  }

  h2 {
    text-align: center;
    color: #00ff99;
    font-size: 2.2em;
    letter-spacing: 2px;
    margin-bottom: 25px;
    text-shadow: 0 0 15px #00ff99, 0 0 40px #00cc88;
  }

  /* ==== FORM DESIGN ==== */
  form {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 15px;
  }
  label {
    display: block;
    font-weight: 600;
    font-size: 0.95em;
    color: #aef;
    text-shadow: 0 0 5px rgba(0,255,255,0.3);
  }
  input[type="text"], input[type="number"] {
    width: 100%;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(0,255,128,0.4);
    color: #fff;
    border-radius: 6px;
    padding: 10px;
    font-size: 0.95em;
    transition: all 0.3s;
    box-shadow: inset 0 0 8px rgba(0,255,128,0.2);
  }
  input[type="text"]:focus, input[type="number"]:focus {
    outline: none;
    border-color: #00ff99;
    box-shadow: 0 0 15px #00ff99;
    transform: scale(1.03);
  }

  /* ==== SUBMIT BUTTON ==== */
  input[type="submit"] {
    grid-column: 1 / -1;
    margin-top: 25px;
    background: linear-gradient(90deg, #00ff99 0%, #00ccff 100%);
    color: #000;
    border: none;
    border-radius: 10px;
    padding: 15px;
    font-size: 1.2em;
    font-weight: bold;
    cursor: pointer;
    box-shadow: 0 0 15px #00ff99, 0 0 40px #00ccff;
    transition: all 0.3s;
  }
  input[type="submit"]:hover {
    background: linear-gradient(90deg, #00ccff 0%, #00ff99 100%);
    transform: translateY(-3px);
    box-shadow: 0 0 30px #00ccff, 0 0 60px #00ff99;
  }

  /* ==== RESULT BOX ==== */
  .result-card {
    margin-top: 35px;
    text-align: center;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.2);
    background: rgba(0,255,128,0.1);
    box-shadow: 0 0 25px rgba(0,255,128,0.2);
    animation: fadeIn 1.5s ease;
  }
  .attack {
    border-color: #ff4444;
    background: rgba(255,0,0,0.1);
    box-shadow: 0 0 20px rgba(255,0,0,0.3);
    color: #ff6666;
  }
  .normal {
    border-color: #00ff99;
    background: rgba(0,255,128,0.1);
    box-shadow: 0 0 20px rgba(0,255,128,0.3);
    color: #00ff99;
  }

  /* ==== FOOTER ==== */
  footer {
    margin-top: 30px;
    text-align: center;
    font-size: 0.85em;
    color: #888;
    letter-spacing: 1px;
  }
</style>
</head>
<body>
<div class="matrix-bg"></div>
<div class="container">
  <h2>INTRUSION DETECTION SYSTEM </h2>
  <form method="post">
    {% for name in feature_names %}
      <label>{{ name }}:
        <input name="{{name}}" value="0" type="number" step="any">
      </label>
    {% endfor %}
    <label>Packet String:
      <input name="packet_str" value="proto=tcp flags=S" type="text">
    </label>
    <input type="submit" value="🚀 Predict">
  </form>

  {% if result %}
    <div class="result-card {{color_class}}">
      <h3>{{result}}</h3>
    </div>
  {% endif %}
</div>

<footer>© 2025 Defense Lab | Powered by DFA + ML Hybrid Model</footer>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    color_class = ""
    if request.method == "POST":
        feats = [float(request.form.get(name, 0)) for name in feature_names]
        feats_df = pd.DataFrame([feats], columns=feature_names)
        pkt_str = request.form.get("packet_str", "")
        result = hybrid_predict(feats_df, pkt_str)

        # ✅ Color logic: red for attack, green for normal
        if "normal" in str(result).lower():
            color_class = "normal"
        else:
            color_class = "attack"

        # --- Logging ---
        log_line = f"{datetime.datetime.now().isoformat()} | Result: {result} | Packet String: {pkt_str}\n"
        with open("web_ui_predictions.log", "a", encoding="utf-8") as logf:
            logf.write(log_line)
        # ---------------

    return render_template_string(HTML_FORM, feature_names=feature_names, result=result, color_class=color_class)

if __name__ == "__main__":
    app.run(debug=True)
