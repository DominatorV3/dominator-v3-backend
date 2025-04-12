import json
import os

WHITELIST_FILE = "whitelist.json"
BLACKLIST_FILE = "blacklist.json"

def load_list(path):
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump([], f)
    with open(path, "r") as f:
        return json.load(f)

def save_list(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def add_to_whitelist(token):
    whitelist = load_list(WHITELIST_FILE)
    if token not in whitelist:
        whitelist.append(token)
        save_list(WHITELIST_FILE, whitelist)
        return True
    return False

def remove_from_whitelist(token):
    whitelist = load_list(WHITELIST_FILE)
    if token in whitelist:
        whitelist.remove(token)
        save_list(WHITELIST_FILE, whitelist)
        return True
    return False

def add_to_blacklist(token):
    blacklist = load_list(BLACKLIST_FILE)
    if token not in blacklist:
        blacklist.append(token)
        save_list(BLACKLIST_FILE, blacklist)
        return True
    return False

def remove_from_blacklist(token):
    blacklist = load_list(BLACKLIST_FILE)
    if token in blacklist:
        blacklist.remove(token)
        save_list(BLACKLIST_FILE, blacklist)
        return True
    return False
