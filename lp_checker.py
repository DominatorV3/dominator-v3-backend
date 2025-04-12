import random

# 🔐 Analyse simplifiée du LP Lock (fake data pour l’instant)
# À terme on pourra utiliser Jupiter ou Solscan si on veut du real-time

def is_lp_locked(token):
    """
    Simule un contrôle de verrouillage de la LP.
    Retourne True si LP est probablement lockée, sinon False.
    """

    # 💡 Tu peux ici remplacer cette logique avec une vraie API plus tard
    # Pour l’instant, on simule 75% de LP lockées, 25% non
    fake_lock_status = random.choices([True, False], weights=[75, 25])[0]

    if fake_lock_status:
        print(f"🔐 LP pour {token} : LOCKÉE ✅")
    else:
        print(f"❌ LP pour {token} : NON LOCKÉE ❌")

    return fake_lock_status
