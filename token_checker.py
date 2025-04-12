from solana.rpc.api import Client
from solana.publickey import PublicKey

client = Client("https://api.mainnet-beta.solana.com")

def check_token_metadata(token_address: str):
    try:
        pubkey = PublicKey(token_address)
        resp = client.get_token_supply(pubkey)
        if resp["result"]:
            supply = int(resp["result"]["value"]["amount"])
            decimals = int(resp["result"]["value"]["decimals"])
            print(f"🧬 Token trouvé sur Solana - Decimals: {decimals}, Supply: {supply}")
            return True, decimals, supply
        else:
            print("❌ Token non trouvé ou invalide.")
            return False, None, None
    except Exception as e:
        print(f"❌ Erreur check_token_metadata : {e}")
        return False, None, None
