from solana.keypair import Keypair
from solana.rpc.api import Client
from solana.publickey import PublicKey
from solders.keypair import Keypair as SoldersKeypair
import base58

def get_balance(wallet_address):
    client = Client("https://api.mainnet-beta.solana.com")
    response = client.get_balance(PublicKey(wallet_address))
    if response["result"]:
        return response["result"]["value"] / 10**9
    return 0

def get_keypair_from_private_key(private_key: str):
    decoded = base58.b58decode(private_key)
    return SoldersKeypair.from_bytes(decoded)
