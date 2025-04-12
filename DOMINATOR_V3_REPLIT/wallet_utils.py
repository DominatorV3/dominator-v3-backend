from solana.rpc.api import Client
from solana.keypair import Keypair
from solana.publickey import PublicKey
from solders.transaction import VersionedTransaction as Transaction
from solana.system_program import TransferParams, transfer
from solders.keypair import Keypair as SoldersKeypair
from solders.pubkey import Pubkey
from base64 import b64decode

# Connexion au cluster Solana
solana_client = Client("https://api.mainnet-beta.solana.com")


def get_balance(public_key: str) -> float:
    """Retourne le solde d’un wallet SOL en SOL."""
    pubkey = PublicKey(public_key)
    balance_response = solana_client.get_balance(pubkey)
    lamports = balance_response['result']['value']
    return lamports / 1_000_000_000


def create_wallet() -> dict:
    """Crée un nouveau wallet et retourne la clé publique et privée."""
    keypair = Keypair()
    return {
        "public_key": str(keypair.public_key),
        "private_key": list(keypair.secret_key)
    }


def transfer_sol(from_private_key: list, to_public_key: str, amount: float) -> str:
    """Transfert du SOL depuis une clé privée vers une clé publique."""
    from_keypair = Keypair.from_secret_key(bytes(from_private_key))
    to_pubkey = PublicKey(to_public_key)

    txn = Transaction()
    txn.add(
        transfer(
            TransferParams(
                from_pubkey=from_keypair.public_key,
                to_pubkey=to_pubkey,
                lamports=int(amount * 1_000_000_000)
            )
        )
    )

    response = solana_client.send_transaction(txn, from_keypair)
    return response['result']


def transfer_sol(from_private_key: list, to_public_key: str, amount: float) -> str:
    """Transfert du SOL depuis une clé privée vers une clé publique."""
    from_keypair = Keypair.from_secret_key(bytes(from_private_key))
    to_pubkey = PublicKey(to_public_key)

    txn = Transaction()
    txn.add(
        transfer(
            TransferParams(
                from_pubkey=from_keypair.public_key,
                to_pubkey=to_pubkey,
                lamports=int(amount * 1_000_000_000)
            )
        )
    )

    response = solana_client.send_transaction(txn, from_keypair)
    return response['result']


