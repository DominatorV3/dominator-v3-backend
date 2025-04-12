import json
import os
import time

SCAN_LOG_FILE = "scan_history.json"

def load_log():
    if not os.path.exists(SCAN_LOG_FILE):
        with open(SCAN_LOG_FILE, "w") as f:
            json.dump([], f)
    with open(SCAN_LOG_FILE, "r") as f:
        return json.load(f)

def save_log(log):
    with open(SCAN_LOG_FILE, "w") as f:
        json.dump(log, f, indent=4)

def log_scan(token, result_dict):
    log = load_log()

    entry = {
        "token": token,
        "score_ia": round(result_dict.get("ia", 0.0), 2),
        "lp": bool(result_dict.get("lp", False)),
        "honeypot": not bool(result_dict.get("honeypot", True)),  # on inverse ici car "safe" = True
        "slippage": int(result_dict.get("slippage", 0) * 100),    # slippage = 0.85 → 85%
        "score_final": round(result_dict.get("final", 0.0), 2),
        "status": result_dict.get("status", "unknown"),  # "accepted" / "blocked"
        "timestamp": int(time.time())
    }

    log.append(entry)
    save_log(log)
    print(f"📁 Log ajouté : {entry}")
