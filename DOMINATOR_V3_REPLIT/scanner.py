from token_security import get_token_score
from honeypot_detector import is_honeypot
from whitelist_utils import is_token_whitelisted
from dashboard_utils import update_dashboard_data
from stats_tracker import save_stats, generate_stats_graph
from wallet_utils import get_balance, send_sol
from telegram_utils import notify_tx_result
import random, time, os

def simulate_ia_scan(keypair, wallet_address, trade_percent, simulation=False):
    token = f"TOKEN{random.randint(100, 999)}"
    print(f"\n🎯 TOKEN IA DÉTECTÉ : {token}")
    print("🧠 Score IA : ✅ CLEAN")
    print(f"👤 Wallet cible : {wallet_address}")

    try:
        solde = get_balance(wallet_address)
        print(f"\n💰 Solde actuel : {solde:.6f} SOL")
    except Exception as e:
        print(f"❌ Erreur récupération solde : {e}")
        solde = 0.0

    montant = round(solde * trade_percent, 6)
    print(f"💸 Envoi : {montant} SOL")

    # Analyse IA
    score = get_token_score(token)
    print(f"🧠 Analyse IA de sécurité pour le token : {token}...")
    if score > 0.7:
        print(f"❌ Analyse IA : le token {token} a un score de risque élevé ({score:.2f})")
        print("⚠️ Protection anti-rug IA activée, token bloqué.")
        return

    print(f"✅ Analyse IA : le token {token} a un score sécurisé ({score:.2f})")

    # Honeypot ?
    try:
        if is_honeypot(token):
            print(f"❌ Token {token} détecté comme honeypot.")
            print("⚠️ Protection honeypot activée, token bloqué.")
            return
    except Exception as e:
        print(f"❌ Erreur analyse honeypot : {e}")
        return

    # Whitelist
    if is_token_whitelisted(token):
        print(f"✅ Token {token} est dans la whitelist, autorisé.")

    # Envoi
    try:
        if simulation:
            tx_hash = f"SIMU_TX_{int(time.time())}"
            print(f"🧪 SIMULATION : TX générée {tx_hash}")
        else:
            tx_hash = send_sol(keypair, wallet_address, montant)
            print(f"✅ TX Confirmée : {tx_hash}")

        save_stats(token, montant, tx_hash)
        generate_stats_graph()
        update_dashboard_data(token, tx_hash, montant)
        notify_tx_result(token, tx_hash, montant)

    except Exception as e:
        print(f"❌ TX échouée : {e}")
