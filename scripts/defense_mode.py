import json
import os

STATE_FILE = "defense_mode.json"

def is_enabled():
    if not os.path.exists(STATE_FILE):
        return False
    try:
        with open(STATE_FILE, "r") as f:
            state = json.load(f)
            return state.get("enabled", False)
    except:
        return False

def set_enabled(value):
    with open(STATE_FILE, "w") as f:
        json.dump({"enabled": value}, f)
