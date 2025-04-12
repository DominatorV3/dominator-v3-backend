import json
import os

WHITELIST_FILE = "whitelist.json"

def load_whitelist():
    if not os.path.exists(WHITELIST_FILE):
        return []
    with open(WHITELIST_FILE, "r") as f:
        return json.load(f)

def save_whitelist(tokens):
    with open(WHITELIST_FILE, "w") as f:
        json.dump(tokens, f, indent=4)

def is_token_whitelisted(token):
    return token in load_whitelist()

def add_to_whitelist(token):
    tokens = load_whitelist()
    if token not in tokens:
        tokens.append(token)
        save_whitelist(tokens)
        return True
    return False
