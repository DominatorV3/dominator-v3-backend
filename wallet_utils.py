from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solana.rpc.api import Client
import base64
import os

def get_balance(wallet_address):
    client = Client("https://api.mainnet-beta.solana.com")
    response = client.get_balance(Pubkey.from_string(wallet_address))
    if response.get("result") and "value" in response["result"]:
        lamports = response["result"]["value"]
        return lamports / 1e9  # Convert lamports to SOL
    return 0

def load_keypair_from_private_key(private_key_str):
    decoded = base64.b64decode(private_key_str)
    return Keypair.from_bytes(decoded[:64])
