import os

VENDOR_DB = "mac-vendors.txt"  # or wherever you saved it
CACHE = {}

def load_vendors():
    if not os.path.exists(VENDOR_DB):
        return {}

    vendors = {}
    with open(VENDOR_DB, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if "(hex)" in line:
                parts = line.split("(hex)")
                if len(parts) == 2:
                    mac_prefix = parts[0].strip().replace("-", ":").upper()
                    vendor = parts[1].strip()
                    vendors[mac_prefix] = vendor
    return vendors

VENDORS = load_vendors()

def lookup_vendor(mac):
    if not mac:
        return "Unknown"
    prefix = mac.upper()[0:8]
    if prefix in CACHE:
        return CACHE[prefix]
    vendor = VENDORS.get(prefix, "Unknown")
    CACHE[prefix] = vendor
    return vendor
