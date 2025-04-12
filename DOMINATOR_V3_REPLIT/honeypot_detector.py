import random

def is_honeypot(token_address: str) -> bool:
    """
    Simule une détection de honeypot.
    Ici on pourrait intégrer une vraie API de détection si disponible.
    Pour l’instant, c’est un random simulé + format de clé vérifié.
    """
    if not isinstance(token_address, str) or len(token_address) < 32:
        raise ValueError(f"{token_address} n'est pas une clé publique valide.")

    # Simulation : 10% de chance que ce soit un honeypot
    return random.random() < 0.1
