from scapy.all import send, IP, TCP, Raw

# Send a TCP packet with a payload that matches your DFA signature
packet = IP(dst="127.0.0.1")/TCP(dport=12345, flags="SF")/Raw(load="attack_signature")
send(packet)
print("Attack packet sent!")