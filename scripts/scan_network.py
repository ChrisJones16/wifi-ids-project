from scripts.mac_lookup import lookup_vendor
import subprocess
import time
import csv
import os

CHANNELS_24GHZ = list(range(1, 14))  # Channels 1 through 13
CHANNELS_5GHZ = [36, 40, 44, 48, 149, 153, 157, 161]
ALL_CHANNELS = CHANNELS_24GHZ + CHANNELS_5GHZ

OUTPUT_DIR = "/tmp"
BASE_OUTPUT = os.path.join(OUTPUT_DIR, "scan_smart")

def run_scan_on_channel(interface, channel, duration=2):
    file_prefix = f"{BASE_OUTPUT}_ch{channel}"
    args = [
        "airodump-ng", "--output-format", "csv",
        "-w", file_prefix,
        "--channel", str(channel),
        interface
    ]

    proc = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(duration)
    proc.terminate()
    time.sleep(1)
    return f"{file_prefix}-01.csv"

def parse_csv(csv_file):
    aps = []
    if not os.path.exists(csv_file):
        return aps

    with open(csv_file, "r", encoding="utf-8", errors="ignore") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or row[0].startswith("BSSID") or row[0].strip() == "Station MAC":
                continue
            if len(row) > 13:
                bssid = row[0].strip()
                channel = row[3].strip()
                power = row[8].strip()
                essid = row[13].strip()
                freq_band = "5 GHz" if channel and int(channel) >= 36 else "2.4 GHz"
                aps.append({
                    "bssid": bssid,
                    "channel": channel,
                    "power": power,
                    "essid": essid or "(hidden)",
                    "band": freq_band,
                    "vendor": lookup_vendor(bssid)
                })
    return aps

def scan_all_channels(interface="wlan1"):
    print(f"[INFO] Starting smart scan on interface: {interface}")
    
    # Clear previous files
    for file in os.listdir(OUTPUT_DIR):
        if file.startswith("scan_smart"):
            os.remove(os.path.join(OUTPUT_DIR, file))

    all_aps = []
    seen_bssids = set()

    for ch in ALL_CHANNELS:
        print(f"[SCAN] Channel {ch}...")
        csv_file = run_scan_on_channel(interface, ch)
        aps = parse_csv(csv_file)

        for ap in aps:
            if ap["bssid"] not in seen_bssids:
                seen_bssids.add(ap["bssid"])
                all_aps.append(ap)

    print(f"[DONE] Found {len(all_aps)} unique APs.")
    return all_aps

if __name__ == "__main__":
    results = scan_all_channels()
    for ap in results:
        print(ap)
