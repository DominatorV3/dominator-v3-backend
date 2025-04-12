from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.transaction import VersionedTransaction
from solders.message import MessageV0, LoadedAddresses
from solana.rpc.api import Client
from solana.rpc.types import TxOpts
from base64 import b64decode
from solana.rpc.commitment import Confirmed
import json
import os

# 🔐 Init Solana client
RPC_URL = "https://api.mainnet-beta.solana.com"
client = Client(RPC_URL)

def get_balance(wallet_address):
    try:
        balance = client.get_balance(wallet_address)["result"]["value"] / 1e9
        return round(balance, 6)
    except Exception as e:
        print(f"[Erreur Solana Balance] : {e}")
        return None

def send_sol(private_key_str, recipient_address, amount_sol):
    try:
        # Génération de la clé depuis la string privée (64 bytes JSON base58)
        private_key_list = json.loads(private_key_str)
        sender = Keypair.from_bytes(bytes(private_key_list))

        recipient = Pubkey.from_string(recipient_address)
        lamports = int(amount_sol * 1e9)

        latest_blockhash = client.get_latest_blockhash()["result"]["value"]["blockhash"]
        message = MessageV0.try_compile(
            payer=sender.pubkey(),
            instructions=[
                {
                    "program_id": Pubkey.from_string("11111111111111111111111111111111"),  # System program
                    "accounts": [
                        {"pubkey": sender.pubkey(), "is_signer": True, "is_writable": True},
                        {"pubkey": recipient, "is_signer": False, "is_writable": True}
                    ],
                    "data": b'\x02' + lamports.to_bytes(8, 'little')
                }
            ],
            recent_blockhash=latest_blockhash,
            address_lookup_table_accounts=[]
        )

        tx = VersionedTransaction(message, [sender])
        result = client.send_transaction(tx, opts=TxOpts(skip_confirmation=False, preflight_commitment=Confirmed))
        print(f"✅ Transaction envoyée ! Signature : {result['result']}")
        return result['result']
    except Exception as e:
        print(f"[Erreur envoi SOL] : {e}")
        return None
