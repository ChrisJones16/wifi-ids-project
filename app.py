from flask import Flask, render_template,redirect, url_for, abort, request, flash, jsonify, send_file
from datetime import timedelta
from scripts import scan_network
from scripts import scan_clients
from scripts import deauth_attack
from collections import defaultdict
from datetime import datetime
from scripts import defense_mode
import os
import threading
import subprocess
import psutil

def setup_monitor_mode(interface="wlan1"):
    try:
        print("[BOOT] Killing conflicting network services...")
        subprocess.run(["sudo", "airmon-ng", "check", "kill"], check=True)

        print(f"[BOOT] Enabling monitor mode on {interface}...")
        subprocess.run(["sudo", "airmon-ng", "start", interface], check=True)

        print("[BOOT] Monitor mode is active.")
    except subprocess.CalledProcessError:
        print("[ERROR] Failed to start monitor mode.")

def is_monitor_running():
    print("[INFO] Checking for existing IDS monitor...")
    for proc in psutil.process_iter(['cmdline']):
        if proc.info['cmdline'] and "ids_monitor.py" in " ".join(proc.info['cmdline']):
            return True
    return False

def start_ids_monitor():
    if is_monitor_running():
        print("[INFO] IDS monitor already running. Skipping launch.")
        return

    def run_monitor():
        print("[INFO] Starting IDS monitor...")
        subprocess.Popen(["sudo", "python3", "scripts/ids_monitor.py"])
    threading.Thread(target=run_monitor, daemon=True).start()


app = Flask(__name__)
LOG_PATH = os.path.join(os.path.dirname(__file__), "logs/alerts.txt")

@app.route("/")
def home():
    alerts = []
    deauth_count = 0
    other_count = 0
    deauth_over_time = defaultdict(int)

    # 1. Chart range from dropdown
    time_range = int(request.args.get("range", 30))  # default to 30 minutes
    chart_cutoff = datetime.now() - timedelta(minutes=time_range)

    # 2. Log retention window
    log_cutoff = datetime.now() - timedelta(days=30)

    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r") as f:
            for line in f:
                if "[ALERT]" not in line:
                    continue
                try:
                    timestamp_str, message = line.strip().split(" [ALERT] ", 1)
                    ts = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    continue

                if ts < log_cutoff:
                    continue  # too old — skip this log line

                alerts.append({"timestamp": timestamp_str, "message": message})

                if "Deauth" in message:
                    deauth_count += 1

                    if ts >= chart_cutoff:
                        # Group deauths by 5-minute bucket
                        rounded_minute = ts.minute - (ts.minute % 5)
                        bucket = ts.replace(minute=rounded_minute, second=0).strftime("%H:%M")
                        deauth_over_time[bucket] += 1
                else:
                    other_count += 1

    # Convert to sorted lists for chart
    sorted_time = sorted(deauth_over_time.items())
    time_labels = [x[0] for x in sorted_time]
    time_counts = [x[1] for x in sorted_time]

    return render_template("index.html",
                           alerts=alerts,
                           deauth_count=deauth_count,
                           other_count=other_count,
                           time_labels=time_labels,
                           time_counts=time_counts,
                           time_range=time_range,
                           defense_mode=defense_mode.is_enabled()
                        )



scan_results = []
@app.route("/start-scan")
def start_scan():
    def run_scan():
        global scan_results
        scan_results = scan_network.scan_all_channels(interface="wlan1")

    # Launch background scan thread
    thread = threading.Thread(target=run_scan)
    thread.start()
    return render_template("scan_status.html")  # Loading screen

@app.route("/scan-status")
def scan_status():
    global scan_results
    return jsonify({"done": bool(scan_results)})

@app.route("/scan")
def scan():
    global scan_results
    if not scan_results:
        return redirect(url_for("start_scan"))
    aps = scan_results
    scan_results = []
    return render_template("scan.html", aps=aps)

"""@app.route("/clients/<bssid>/<channel>")
def view_clients(bssid, channel):
    clients = scan_clients.scan_clients(bssid, channel, interface="wlan1")
    return render_template("clients.html", bssid=bssid, channel=channel, clients=clients)
"""
@app.route("/clients/<bssid>/<channel>", methods=["GET", "POST"])
def view_clients(bssid, channel):
    if request.method == "POST":
        action = request.form.get("action")
        
        if action == "deauth_ap":
            print(f"[DEAUTH] Sending broadcast deauth to AP {bssid}...")
            # Call the existing aireplay logic
            deauth_attack.send_deauth("FF:FF:FF:FF:FF:FF", bssid, channel)
            return redirect(url_for("view_clients", bssid=bssid, channel=channel))

        elif action == "rescan":
            print(f"[RESCAN] Refreshing client list for AP {bssid}...")
            # Just fall through and re-scan

    clients = scan_clients.scan_clients(bssid, channel, interface="wlan1")
    return render_template("clients.html", bssid=bssid, channel=channel, clients=clients)


@app.route("/deauth", methods=["POST"])
def deauth():
    target_mac = request.form.get("target_mac")
    ap_bssid = request.form.get("ap_bssid")
    channel = request.form.get("channel")

    print(f"[DEAUTH] Targeting {target_mac} on AP {ap_bssid} CH {channel}")

    success = deauth_attack.send_deauth(target_mac, ap_bssid, channel)

    return render_template("deauth_result.html", success=success, target_mac=target_mac, ap_bssid=ap_bssid, channel=channel)

@app.route("/toggle-defense", methods=["POST"])
def toggle_defense():
    current = defense_mode.is_enabled()
    defense_mode.set_enabled(not current)
    return redirect(url_for("home"))

@app.route("/download-logs")
def download_logs():
    log_path = os.path.join(os.path.dirname(__file__), "logs/alerts.txt")
    return send_file(log_path, as_attachment=True, attachment_filename="alerts.csv")


@app.route("/clear-logs", methods=["POST"])
def clear_logs():
    log_path = os.path.join(os.path.dirname(__file__), "logs/alerts.txt")
    with open(log_path, "w") as f:
        f.write("")  # Clear the file
    return redirect(url_for("home"))


if __name__ == "__main__":
    print("[BOOT] Launching Wi-Fi IDS Flask Dashboard")
    setup_monitor_mode()
    start_ids_monitor()  # <-- auto-start background monitoring
    app.run(host="0.0.0.0", port=5000)
