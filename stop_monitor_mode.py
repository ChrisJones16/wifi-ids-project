import subprocess

def stop_monitor_mode(interface="wlan1"):
    try:
        print(f"[SHUTDOWN] Stopping monitor mode on {interface}...")
        subprocess.run(["sudo", "airmon-ng", "stop", interface], check=True)
        subprocess.run(["sudo", "systemctl", "restart", "NetworkManager"], check=True)
        print("[SHUTDOWN] Wi-Fi services restored.")
    except subprocess.CalledProcessError:
        print("[ERROR] Failed to stop monitor mode properly.")

if __name__ == "__main__":
    stop_monitor_mode()
