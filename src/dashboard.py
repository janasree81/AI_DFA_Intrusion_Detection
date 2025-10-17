import streamlit as st
import pandas as pd

st.set_page_config(page_title="Intrusion Detection Dashboard", layout="wide")

st.title("Intrusion Detection Dashboard")

# Load log file (adjust path if needed)
log_file = "web_ui_predictions.log"

# Parse the log file into a DataFrame
def parse_log(log_file):
    rows = []
    with open(log_file, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split(" | ")
            if len(parts) == 3:
                timestamp = parts[0]
                result = parts[1].replace("Result: ", "")
                pkt_str = parts[2].replace("Packet String: ", "")
                rows.append({"timestamp": timestamp, "result": result, "packet_str": pkt_str})
    return pd.DataFrame(rows)

df = parse_log(log_file)

st.dataframe(df)

# Show alert counts
st.subheader("Alert Statistics")
st.write(df["result"].value_counts())

# Filter by alert type
alert_type = st.selectbox("Filter by Result", ["All"] + df["result"].unique().tolist())
if alert_type != "All":
    st.dataframe(df[df["result"] == alert_type])