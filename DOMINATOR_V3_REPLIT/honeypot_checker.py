import requests

def is_honeypot(token_address: str) -> bool:
    """
    Vérifie si le token est un honeypot en utilisant une API tierce.
    Retourne True si c'est un honeypot, sinon False.
    """
    try:
        # Remplacez l'URL par celle de l'API de détection de honeypot appropriée
        api_url = f"https://api.honeypotdetector.com/solana/{token_address}"
        response = requests.get(api_url)
        response.raise_for_status()
        result = response.json()
        return result.get("is_honeypot", False)
    except Exception as e:
        print(f"❌ Erreur lors de la vérification du honeypot : {e}")
        return False
