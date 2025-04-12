# rugpull_checker.py

import requests
from solana.publickey import PublicKey
from solders.rpc.requests import GetTokenLargestAccounts, GetAccountInfo
from solana.rpc.api import Client

client = Client("https://api.mainnet-beta.solana.com")


def is_token_suspect(token_address: str) -> bool:
    try:
        pubkey = PublicKey(token_address)

        # 1. Vérifie les plus grosses balances (trop concentrées = danger)
        largest_accounts_resp = client._provider.make_request(
            GetTokenLargestAccounts(pubkey))
        accounts = largest_accounts_resp.get("result", {}).get("value", [])
        if not accounts:
            return True

        # 2. Total supply
        total_balance = sum([float(a.get("amount", 0)) for a in accounts])
        if total_balance == 0:
            return True

        # 3. Si un seul wallet détient >50%, c’est un gros red flag
        top_holder = float(accounts[0].get("amount", 0)) / total_balance
        if top_holder > 0.5:
            return True

        return False

    except Exception as e:
        print(f"❌ Erreur analyse rugpull : {e}")
        return True
