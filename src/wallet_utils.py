from solders.transaction import VersionedTransaction
from solana.rpc.api import Client
from solana.publickey import PublicKey

def get_balance(wallet_address: str) -> float:
    client = Client("https://api.mainnet-beta.solana.com")
    balance_lamports = client.get_balance(PublicKey(wallet_address))["result"]["value"]
    return balance_lamports / 1_000_000_000  # Convert lamports to SOL
