import os
import random
import time
from dotenv import load_dotenv

from telegram.ext import Updater
from telegram_utils import (
    register_commands,
    notify_startup,
    notify_tx_result
)

from wallet_utils import (
    load_keypair_from_private_key,
    get_balance,
    send_sol
)

from token_security import get_token_score
from honeypot_detector import is_honeypot
from anti_rugpull import is_token_safe
from whitelist_utils import is_token_whitelisted
from stats_tracker import update_dashboard_data
from leaderboard_utils import update_leaderboard
from panic_utils import is_panic_mode

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")
TRADE_PERCENT = float(os.getenv("TRADE_PERCENT", 0.05))
SIMULATION_MODE = os.getenv("SIMULATION_MODE", "True") == "True"

keypair = load_keypair_from_private_key()

def simulate_ia_scan():
    fake_tokens = ["TOKEN333", "TOKEN666", "TOKEN777"]
    token = random.choice(fake_tokens)

    print(f"\n🎯 TOKEN À ANALYSER : {token}")
    print(f"👤 Wallet cible : {WALLET_ADDRESS}")

    if is_panic_mode():
        print("🛑 PANIC MODE ACTIVÉ : Aucune transaction autorisée.")
        return

    balance = get_balance(WALLET_ADDRESS)
    if balance is None or balance <= 0:
        print("❌ Solde insuffisant ou erreur récupération.")
        return

    print(f"💰 Solde actuel : {balance:.6f} SOL")
    montant = round(balance * TRADE_PERCENT, 6)
    print(f"💸 Envoi : {montant} SOL")

    score = get_token_score(token)
    if score >= 0.7:
        print(f"❌ Analyse IA : le token {token} a un score de risque élevé ({score})")
        return
    else:
        print(f"✅ Analyse IA : le token {token} a un score sécurisé ({score})")

    if not is_token_safe(token):
        print(f"❌ Erreur analyse rugpull : token {token} bloqué")
        return

    if not is_token_whitelisted(token):
        print(f"❌ Token {token} non whitelisté.")
        return
    else:
        print(f"✅ Token {token} est dans la whitelist.")

    if SIMULATION_MODE:
        tx_hash = f"SIMU-{int(time.time())}"
        print(f"✅ TX (Simulation) : {tx_hash}")
    else:
        tx_hash = send_sol(keypair, WALLET_ADDRESS, montant)
        if tx_hash:
            print(f"✅ TX Confirmée : {tx_hash}")
        else:
            print("❌ TX échouée")
            return

    update_dashboard_data(token, montant, tx_hash)
    update_leaderboard(token, montant)
    notify_tx_result(token, tx_hash, montant)

# 🟢 Démarrage
print("🔥 DOMINATOR Vx EN LIGNE 🔥")
print(f"🔎 TELEGRAM_TOKEN = {TELEGRAM_TOKEN}")
print(f"🔎 TELEGRAM_CHAT_ID = {TELEGRAM_CHAT_ID}")
print(f"🔎 PRIVATE_KEY = {PRIVATE_KEY[:10]}...{PRIVATE_KEY[-10:]}")
print(f"🔎 WALLET_ADDRESS = {WALLET_ADDRESS}")
print(f"🔎 TRADE_PERCENT = {TRADE_PERCENT}")
print(f"🔎 MODE SIMULATION = {SIMULATION_MODE}")

updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
register_commands(updater.dispatcher)
updater.start_polling()
notify_startup()
print("📡 Commandes Telegram actives.\n")

while True:
    simulate_ia_scan()
    time.sleep(15)
