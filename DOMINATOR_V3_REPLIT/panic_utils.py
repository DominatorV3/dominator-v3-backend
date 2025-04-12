import json
import os

PANIC_FILE = "panic_mode.json"

def is_panic_mode():
    if not os.path.exists(PANIC_FILE):
        return False
    try:
        with open(PANIC_FILE, "r") as f:
            data = json.load(f)
            return data.get("panic", False)
    except:
        return False

def set_panic_mode(state: bool):
    with open(PANIC_FILE, "w") as f:
        json.dump({"panic": state}, f)
