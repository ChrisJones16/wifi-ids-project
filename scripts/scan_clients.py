from scripts.mac_lookup import lookup_vendor
import subprocess
import time
import csv
import os

#Used for finding susupicious clients (too intensive for my project)
"""recent_mac_activity = {}  # MAC -> [(timestamp, BSSID)]

def record_mac_activity(mac, bssid):
    now = time.time()
    if mac not in recent_mac_activity:
        recent_mac_activity[mac] = []
    recent_mac_activity[mac].append((now, bssid))

    # Keep only last 10 minutes of activity
    recent_mac_activity[mac] = [
        (ts, b) for ts, b in recent_mac_activity[mac] if now - ts < 600
    ]

def is_mac_suspicious(mac):
    # If connected to 2+ unique BSSIDs in last 10 minutes
    bssids = {bssid for _, bssid in recent_mac_activity.get(mac, [])}
    return len(bssids) >= 2
"""

def scan_clients(bssid, channel, interface="wlan1", duration=10):
    output_prefix = "/tmp/client_scan"
    csv_file = f"{output_prefix}-01.csv"

    # Clean up old scan files
    for f in os.listdir("/tmp"):
        if f.startswith("client_scan"):
            os.remove(os.path.join("/tmp", f))

    # Run airodump-ng focused on this AP
    print(f"[INFO] Scanning clients for BSSID {bssid} on channel {channel}...")
    proc = subprocess.Popen([
        "airodump-ng",
        "--bssid", bssid,
        "--channel", str(channel),
        "--output-format", "csv",
        "-w", output_prefix,
        interface
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    time.sleep(duration)
    proc.terminate()
    time.sleep(2)

    clients = []
    found_station_mac = False

    with open(csv_file, "r", encoding="utf-8", errors="ignore") as f:
        reader = csv.reader(f)
        for row in reader:
            # Station/client section starts after this marker
            if row and row[0].strip() == "Station MAC":
                found_station_mac = True
                continue

            if not found_station_mac or not row or len(row) < 6:
                continue

            mac = row[0].strip()
            last_seen = row[1].strip()
            power = row[3].strip()
            ap_mac = row[5].strip()

            if ap_mac == bssid:
                vendor = lookup_vendor(mac)
                #record_mac_activity(mac, ap_bssid)
                #suspicious = is_mac_suspicious(mac)
                clients.append({
                    "mac": mac,
                    "last_seen": last_seen,
                    "power": power,
                    "vendor": vendor,
                    #"suspicious": suspicious
                })

    return clients
