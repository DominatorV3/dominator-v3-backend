from telethon import TelegramClient, events
import re
import asyncio
import json
import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

API_ID = os.getenv("TG_API_ID")
API_HASH = os.getenv("TG_API_HASH")
SESSION_NAME = "dominator_session"
QUEUE_FILE = "sniped_tokens.json"
WHITELIST_FILE = "whitelist.json"
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# 🔍 Mots-clés à surveiller
KEYWORDS = ["ca:", "contract:", "launch", "solana", "stealth", "token live", "new gem"]

# ⚙️ Config auto-buy
AUTO_BUY_THRESHOLD = 3  # Nombre de détections
AUTO_BUY_WINDOW = 60    # Fenêtre de temps en secondes

# ⏱️ Mémoire des détections (in-memory)
token_activity = {}

def extract_token(message):
    matches = re.findall(r'\b[A-Za-z0-9]{32,44}\b', message)
    return matches[0] if matches else None

def message_contains_keyword(message):
    msg_lower = message.lower()
    return any(keyword in msg_lower for keyword in KEYWORDS)

def send_telegram_notification(token, auto=False):
    try:
        message = (
            f"🚨 *Token détecté via Telegram !*\n"
            f"`{token}`\n"
            + ("_Auto-buy déclenché après multiples détections._" if auto else "_Ajouté à la queue DOMINATOR._")
        )
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }
        requests.post(url, json=payload)
        print("📲 Notification Telegram envoyée.")
    except Exception as e:
        print(f"❌ Erreur envoi Telegram : {e}")

def add_token_to_queue(token):
    try:
        if not os.path.exists(QUEUE_FILE):
            with open(QUEUE_FILE, "w") as f:
                json.dump([], f)

        with open(QUEUE_FILE, "r") as f:
            queue = json.load(f)

        if token not in queue:
            queue.append(token)
            with open(QUEUE_FILE, "w") as f:
                json.dump(queue, f, indent=4)
            print(f"📥 Token {token} ajouté à la queue DOMINATOR.")
            send_telegram_notification(token)
        else:
            print(f"🔁 Token {token} déjà présent dans la queue.")
    except Exception as e:
        print(f"❌ Erreur ajout queue : {e}")

def add_token_to_whitelist(token):
    try:
        if not os.path.exists(WHITELIST_FILE):
            with open(WHITELIST_FILE, "w") as f:
                json.dump([], f)

        with open(WHITELIST_FILE, "r") as f:
            wl = json.load(f)
        if not isinstance(wl, list):
            wl = []

        if token not in wl:
            wl.append(token)
            with open(WHITELIST_FILE, "w") as f:
                json.dump(wl, f, indent=4)
            print(f"✅ Token {token} ajouté à la whitelist auto-buy.")
        else:
            print(f"🔁 Token {token} déjà dans la whitelist.")
    except Exception as e:
        print(f"❌ Erreur auto-whitelist : {e}")

def check_auto_buy(token):
    now = time.time()
    timestamps = token_activity.get(token, [])
    # Garder uniquement les détections récentes
    timestamps = [t for t in timestamps if now - t <= AUTO_BUY_WINDOW]
    timestamps.append(now)
    token_activity[token] = timestamps

    print(f"📊 {token} détecté {len(timestamps)}/{AUTO_BUY_THRESHOLD} fois (auto-buy check)")

    if len(timestamps) >= AUTO_BUY_THRESHOLD:
        add_token_to_whitelist(token)
        add_token_to_queue(token)
        send_telegram_notification(token, auto=True)
        token_activity[token] = []  # reset compteur

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

@client.on(events.NewMessage(chats=None))
async def handler(event):
    message = event.message.message
    if message:
        if not message_contains_keyword(message):
            print("⛔ Message ignoré (aucun mot-clé)")
            return

        token = extract_token(message)
        if token:
            print(f"🚨 TOKEN DÉTECTÉ : {token}")
            check_auto_buy(token)
        else:
            print("⚠️ Mot-clé détecté mais aucun token trouvé.")
    else:
        print("🔹 Message vide reçu.")

def run_sniper():
    print("🚀 TELEGRAM SNIPER AUTO-BUY ACTIVÉ")
    client.start()
    client.run_until_disconnected()

if __name__ == "__main__":
    run_sniper()
