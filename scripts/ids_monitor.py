from scapy.all import sniff, Dot11Deauth
from datetime import datetime
import defense_mode
import os
import subprocess

LOG_FILE = os.path.join(os.path.dirname(__file__), "../logs/alerts.txt")

def log_alert(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp} [ALERT] {message}\n")
    print(f"[LOGGED] {message}")

def detect_deauth(pkt):
    if pkt.haslayer(Dot11Deauth):
        src = pkt.addr2
        dst = pkt.addr1
        log_alert(f"Deauth packet detected: from {src} to {dst}")

        if defense_mode.is_enabled():
            print(f"[DEFENSE MODE] Auto-deauthing {mac}")
            subprocess.call(["python3", "scripts/deauth_target.py", mac, ap_bssid, channel])


def start_monitoring(interface="wlan1"):
    print(f"[INFO] Starting deauth detection on {interface}")
    sniff(iface=interface, prn=detect_deauth)

if __name__ == "__main__":
    start_monitoring()
