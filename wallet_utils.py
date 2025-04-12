import os
from solana.rpc.api import Client
from solana.keypair import Keypair
from solana.publickey import PublicKey
from solana.transaction import Transaction
from solana.system_program import TransferParams, transfer
from dotenv import load_dotenv
import base58

load_dotenv()

client = Client("https://api.mainnet-beta.solana.com")

def load_keypair_from_private_key():
    secret_base58 = os.getenv("PRIVATE_KEY")
    if not secret_base58:
        raise ValueError("❌ PRIVATE_KEY manquant dans le fichier .env")
    secret_bytes = base58.b58decode(secret_base58.strip())
    return Keypair.from_secret_key(secret_bytes)

def get_balance(wallet_address):
    response = client.get_balance(PublicKey(wallet_address))
    if hasattr(response, "value"):
        return response.value / 1e9
    else:
        raise ValueError("❌ Erreur récupération solde")

def send_sol(sender_keypair, recipient_pubkey_str, amount):
    recipient_pubkey = PublicKey(recipient_pubkey_str)
    lamports = int(amount * 1e9)
    txn = Transaction()
    txn.add(
        transfer(
            TransferParams(
                from_pubkey=sender_keypair.public_key,
                to_pubkey=recipient_pubkey,
                lamports=lamports,
            )
        )
    )
    response = client.send_transaction(txn, sender_keypair)

    # ✅ On récupère le résultat proprement
    try:
        tx_sig = response.value  # valeur propre du hash TX
        return str(tx_sig)
    except Exception as e:
        raise Exception(f"❌ Envoi échoué : {e}")
