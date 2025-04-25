import subprocess

def stop_monitor_mode_kali(interface="wlan1"):
    try:
        print(f"[SHUTDOWN] Stopping monitor mode on {interface}...")
        subprocess.run(["sudo", "airmon-ng", "stop", interface], check=True)
        subprocess.run(["sudo", "systemctl", "restart", "NetworkManager"], check=True)
        print("[SHUTDOWN] Wi-Fi services restored.")
    except subprocess.CalledProcessError:
        print("[ERROR] Failed to stop monitor mode properly.")


def stop_monitor_mode_raspberry(interface="wlan1"):
    try:
        print(f"[SHUTDOWN] Stopping monitor mode on {interface}...")
        subprocess.run(["sudo", "airmon-ng", "stop", interface], check=True)
        subprocess.run(["sudo", "ip", "link", "set", interface, "up"], check=True)

        print("[SHUTDOWN] Restarting Wi-Fi services...")
        subprocess.run(["sudo", "systemctl", "restart", "dhcpcd"], check=True)
        subprocess.run(["sudo", "systemctl", "restart", "wpa_supplicant"], check=True)
        subprocess.run(["sudo", "systemctl", "restart", "NetworkManager"], check=True)

        print("[✅] Wi-Fi services should now be restored.")
    except subprocess.CalledProcessError:
        print("[ERROR] Failed to stop monitor mode or restore services.")

if __name__ == "__main__":
    stop_monitor_mode_raspberry()
