Wi-Fi Intrusion Detection and Deauthentication Toolkit

A Flask-powered Wi-Fi IDS and ethical deauthentication attack simulation tool built for the Raspberry Pi 4 running Kali Linux. Designed for penetration testing, wireless network visibility, and hands-on learning in Wi-Fi security.

🔧 Project Overview

This project transforms a Raspberry Pi 4 into a portable Wi-Fi defense and penetration test suite. It uses:

Flask: For a live web-based dashboard

Scapy: For packet sniffing and deauthentication monitoring

airodump-ng & aireplay-ng: For access point and client discovery + deauth attack execution

Vendor lookup: For MAC address manufacturer recognition

Real-time IDS: Detects and logs deauth attempts

This system provides both offensive (simulated deauth attacks) and defensive (monitoring + auto-response) capabilities in a single, touchscreen-compatible interface.

🧵 Hardware & Environment

Raspberry Pi 4 (4GB+)

Kali Linux ARM Image (32 or 64-bit)

External Wi-Fi Adapter: Must support monitor mode and packet injection (e.g., Alfa AWUS036ACH)

Waveshare 3.5" GPIO Touchscreen (optional)

⚙️ Features

1. Access Point Scanning

Real-time scan using airodump-ng

Shows: BSSID, ESSID, Vendor, Signal, Channel, Band (2.4/5 GHz)

Automatically highlights the AP with the strongest signal

Refreshes AP list without restarting the scan logic

2. Client Monitoring

List all clients connected to a selected AP

Displays MAC address, signal strength, last seen, and vendor

Includes an option to rescan a specific AP

Optional AP-level deauth button

3. Deauth Attack Simulation

General broadcast deauth (via aireplay-ng)

Targeted device-level deauth

Targeted AP-level deauth

Real-time confirmation messages and status logging

4. IDS (Intrusion Detection System)

Passive detection of deauth packets via scapy

Logs activity with timestamp and source/destination MACs

Auto-refreshing alert log on dashboard

5. Live Defense Mode

Toggleable mode that automatically sends deauths back to suspected attackers in real-time

Uses custom defense_mode.py state controller

Integrated into ids_monitor.py via subprocess

6. Visualization & Analytics

Pie Chart: Breakdown of deauth vs other alerts

Bar Chart: Deauths over time (5-min buckets, toggle between 10/30/60 min view)

7. Utility Tools

Export IDS logs to CSV

Clear all logs with one click

Navigation buttons for returning to dashboard or previous scans

📂 File Structure

wifi_deauth_defense/
├── app.py                       # Flask app entry point
├── templates/                  # HTML templates (Jinja2)
│   ├── index.html              # Main dashboard
│   ├── scan.html               # AP scan results
│   ├── clients.html            # Clients under AP
├── scripts/
│   ├── scan_network.py         # AP scanning logic
│   ├── scan_clients.py         # Parses AP-specific clients
│   ├── deauth_general.py       # General deauth attack
│   ├── deauth_target.py        # Targeted device/AP deauth
│   ├── ids_monitor.py          # Real-time packet monitoring
│   ├── auto_switch_ap.py       # Connect to strongest AP
│   ├── mac_lookup.py           # MAC vendor lookup
│   ├── defense_mode.py         # Live defense toggle state
├── logs/
│   └── alerts.txt              # Logged deauth alerts
├── static/js/chart.min.js     # Chart.js library (local)
├── requirements.txt            # Python dependencies

🚀 Installation & Usage

1. Clone the Repo

git clone https://github.com/ChrisJones16/wifi-ids-project.git
cd wifi-ids-project

2. Install Dependencies

sudo apt update
pip3 install -r requirements.txt

3. Prepare Wireless Interface

sudo airmon-ng check kill
sudo airmon-ng start wlan1

4. Start the App

sudo -E python3 app.py

Then go to http://127.0.0.1:5000


🛡️ Ethical Usage Disclaimer

This project is for ethical research and educational purposes only.

Only test on networks you own or are authorized to assess

Deauthentication can disrupt Wi-Fi service; use responsibly

Any misuse of this tool is solely the responsibility of the user

📚 Resources

Kali Linux ARM for Pi

Waveshare LCD Drivers

Chart.js Docs

Aircrack-ng Suite

💻 Author

Christopher Jones M.S. Cybersecurity | Kali Linux | Wi-Fi Penetration Testing

💼 License

This project is licensed under the MIT License.
