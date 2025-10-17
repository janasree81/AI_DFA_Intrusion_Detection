# main.py
"""
🧠 Hybrid Intrusion Detection System (DFA + ML)
------------------------------------------------
Entry point for launching the Flask-based Web UI
for the hybrid intrusion detection system.

Author: [Your Name]
Year: 2025
"""

from src.web_ui import app

if __name__ == "__main__":
    print("🚀 Starting Hybrid Intrusion Detection System Web Interface...")
    print("🌐 Access it at: http://127.0.0.1:5000/")
    app.run(host="127.0.0.1", port=5000, debug=True)
