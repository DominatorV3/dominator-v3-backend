from token_security import get_token_score
from honeypot_detector import is_honeypot
from lp_checker import is_lp_locked
import random

# Config des pondérations
WEIGHTS = {
    "ia": 0.5,
    "lp": 0.2,
    "slippage": 0.15,
    "honeypot": 0.15
}

# Simulateur de slippage factice
def get_fake_slippage(token):
    return random.randint(2, 40)  # en %

def normalize_slippage(slip):
    if slip >= 30:
        return 0.0
    elif slip <= 5:
        return 1.0
    else:
        return max(0.0, 1 - (slip - 5) / 25)

def get_final_score(token):
    print(f"\n🎯 TOKEN {token} – Évaluation combinée")

    # 🤖 IA Score
    score_ia = get_token_score(token)
    print(f"🤖 Score IA = {score_ia:.2f}")

    # 🔐 LP Lock
    lp_ok = is_lp_locked(token)
    score_lp = 1.0 if lp_ok else 0.0
    print(f"🔐 LP Lock = {'OK' if lp_ok else 'Non lockée'}")

    # 🧪 Slippage
    slippage = get_fake_slippage(token)
    score_slip = normalize_slippage(slippage)
    print(f"🧪 Slippage = {slippage}% ({score_slip:.2f})")

    # 🧼 Honeypot Check (protégé)
    try:
        honeypot_ok = not is_honeypot(token)
    except Exception as e:
        print(f"❌ Erreur honeypot : {e}")
        honeypot_ok = False
    score_honeypot = 1.0 if honeypot_ok else 0.0
    print(f"🧼 Honeypot = {'Safe' if honeypot_ok else 'Bloqué'}")

    # 🧠 Score combiné final
    final = (
        score_ia * WEIGHTS["ia"] +
        score_lp * WEIGHTS["lp"] +
        score_slip * WEIGHTS["slippage"] +
        score_honeypot * WEIGHTS["honeypot"]
    )

    print(f"🧠 Score final = {final:.2f}")
    return final, {
        "ia": score_ia,
        "lp": lp_ok,
        "slippage": score_slip,
        "honeypot": honeypot_ok,
        "final": final
    }
