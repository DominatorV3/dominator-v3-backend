import os
import requests
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(message):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ TOKEN ou CHAT_ID manquant")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }

    try:
        response = requests.post(url, data=data)
        if response.status_code != 200:
            print(f"❌ Erreur Telegram : {response.text}")
    except Exception as e:
        print(f"❌ Erreur envoi Telegram : {e}")

def notify_token_detected(token, wallet_cible, amount):
    message = f"""<b>🎯 TOKEN DÉTECTÉ :</b> <code>{token}</code>
🧠 <b>Score :</b> ✅ CLEAN
👤 <b>Wallet :</b> <code>{wallet_cible}</code>
💸 <b>Envoi :</b> {amount:.6f} SOL
"""
    send_telegram_message(message)

def notify_tx_result(token, status):
    message = f"📦 <b>Transaction envoyée :</b> {status} pour <code>{token}</code>"
    send_telegram_message(message)

def notify_auto_sell(token, amount, status):
    message = f"💸 <b>AUTO-SELL :</b> {token} — {amount} SOL — {status}"
    send_telegram_message(message)

def notify_tx_error(token, error_msg):
    message = f"❌ <b>Erreur TX :</b> {token}\n<code>{error_msg}</code>"
    send_telegram_message(message)
