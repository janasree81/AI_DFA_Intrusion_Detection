from scapy.all import sniff, IP, TCP, UDP, Raw
import pandas as pd
from integrated_regex_model import hybrid_predict
import os
# Load feature names
COLUMNS_PATH = os.path.join("data", "columns.txt")
with open(COLUMNS_PATH, "r") as f:
    feature_names = [line.strip() for line in f if line.strip()]

def extract_features(packet):
    # Initialize all features to 0
    feats = [0] * len(feature_names)
    feature_map = dict(zip(feature_names, feats))

    # --- Basic feature extraction from packet ---
    if IP in packet:
        feature_map['duration'] = 0  # Not available from a single packet
        feature_map['protocol_type'] = {6: 1, 17: 2}.get(packet[IP].proto, 0)  # 1: TCP, 2: UDP, 0: other
        feature_map['src_bytes'] = len(packet[IP].payload)
        feature_map['dst_bytes'] = len(packet[IP])
        feature_map['land'] = 1 if packet[IP].src == packet[IP].dst else 0

    if TCP in packet:
        # Example: SYN flag
        feature_map['flag'] = 1 if packet[TCP].flags == "S" else 0
        # You can map ports to services if you want, here just an example
        feature_map['service'] = 1
    elif UDP in packet:
        feature_map['service'] = 2
        feature_map['flag'] = 0
    else:
        feature_map['service'] = 0
        feature_map['flag'] = 0

    # --- The rest are set to 0 or default ---
    # These require session/flow tracking or are not available from a single packet:
    # wrong_fragment, urgent, hot, num_failed_logins, logged_in, num_compromised, root_shell,
    # su_attempted, num_root, num_file_creations, num_shells, num_access_files, num_outbound_cmds,
    # is_host_login, is_guest_login, count, srv_count, serror_rate, srv_serror_rate, rerror_rate,
    # srv_rerror_rate, same_srv_rate, diff_srv_rate, srv_diff_host_rate, dst_host_count,
    # dst_host_srv_count, dst_host_same_srv_rate, dst_host_diff_srv_rate, dst_host_same_src_port_rate,
    # dst_host_srv_diff_host_rate, dst_host_serror_rate, dst_host_srv_serror_rate,
    # dst_host_rerror_rate, dst_host_srv_rerror_rate

    # If you want to try to extract more, you can add logic here.

    # Return as DataFrame
    feats = [feature_map[name] for name in feature_names]
    return pd.DataFrame([feats], columns=feature_names)

def process_packet(packet):
    feats_df = extract_features(packet)
    # Include raw payload in pkt_str for DFA matching
    raw_payload = bytes(packet[Raw]).decode(errors="ignore") if Raw in packet else ""
    pkt_str = str(packet.summary()) + " " + raw_payload
    result = hybrid_predict(feats_df, pkt_str)
    print(f"Packet: {pkt_str}\nResult: {result}\n")

if __name__ == "__main__":
    print("Starting real-time intrusion detection agent...")
    sniff(prn=process_packet, store=0)