# token_scanner.py

import asyncio
from token_security import is_token_clean
from anti_rugpull import is_token_safe
from telegram_utils import notify_tx_result

async def process_new_token(token_address):
    print(f"🔍 Analyse du nouveau token {token_address}...")

    try:
        ia_score = is_token_clean(token_address)
        rug_check = is_token_safe(token_address)

        if not rug_check:
            print(f"❌ {token_address} bloqué : risque de rugpull.")
            return

        if ia_score > 0.85:
            print(f"❌ {token_address} bloqué : IA détecte un risque élevé ({ia_score})")
            return

        print(f"✅ Nouveau token CLEAN détecté : {token_address} (score IA: {ia_score})")
        notify_tx_result(token_address, f"🆕 Nouveau token CLEAN détecté (score: {ia_score})")

    except Exception as e:
        print(f"❌ Erreur traitement token {token_address} : {e}")
