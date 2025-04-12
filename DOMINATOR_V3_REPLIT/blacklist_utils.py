import json
import os

BLACKLIST_FILE = "blacklist.json"

def load_blacklist():
    if not os.path.exists(BLACKLIST_FILE):
        with open(BLACKLIST_FILE, "w") as f:
            json.dump([], f)
    with open(BLACKLIST_FILE, "r") as f:
        return json.load(f)

def save_blacklist(blacklist):
    with open(BLACKLIST_FILE, "w") as f:
        json.dump(blacklist, f, indent=4)

def is_token_blacklisted(token):
    bl = load_blacklist()
    return token in bl

def add_to_blacklist(token):
    bl = load_blacklist()
    if token not in bl:
        bl.append(token)
        save_blacklist(bl)
        print(f"⛔ Token {token} ajouté à la blacklist automatique.")
    else:
        print(f"⚠️ Token {token} déjà blacklisté.")
