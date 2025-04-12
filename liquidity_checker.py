from solana.rpc.api import Client
from solana.publickey import PublicKey

client = Client("https://api.mainnet-beta.solana.com")

def get_token_liquidity(token_address: str) -> float:
    """
    Vérifie la liquidité disponible pour un token donné sur les DEX de Solana.
    Retourne la valeur de la liquidité en SOL.
    """
    try:
        # Implémentez ici la logique pour interroger les DEX comme Raydium ou Orca
        # pour obtenir les informations de liquidité du token.
        # Cela peut nécessiter l'utilisation de leurs SDK ou API respectives.
        # Exemple fictif :
        liquidity = 1000.0  # Remplacez par la valeur réelle obtenue
        return liquidity
    except Exception as e:
        print(f"❌ Erreur lors de la vérification de la liquidité : {e}")
        return 0.0
