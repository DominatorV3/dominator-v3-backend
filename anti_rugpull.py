import json
import base58
import os
from solders.pubkey import Pubkey

def is_valid_public_key(token_address):
    try:
        decoded = base58.b58decode(token_address)
        return len(decoded) == 32
    except Exception:
        return False

def is_token_whitelisted(token_address):
    try:
        with open("whitelist.json", "r") as file:
            data = json.load(file)
        return token_address in data.get("trusted_tokens", [])
    except Exception:
        return False

def is_token_safe(token_address):
    if is_token_whitelisted(token_address):
        print(f"✅ Token {token_address} est dans la whitelist, autorisé.")
        return True

    if not is_valid_public_key(token_address):
        print(f"❌ Erreur analyse rugpull : {token_address} n'est pas une clé publique valide.")
        return False

    try:
        # Simulation de logique avancée ici (peut être branchée sur API ou smart-contract checker)
        print(f"🔎 Analyse contractuelle : {token_address}")
        score = 0  # Score fictif pour test
        rug_pull_detected = False  # À remplacer par vraie logique

        if rug_pull_detected or score < 1:
            print(f"❌ Token {token_address} suspecté de rug pull ❌")
            return False
        return True
    except Exception as e:
        print(f"❌ Erreur analyse rugpull : {e}")
        return False
