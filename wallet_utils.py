from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.signature import Signature
from solana.rpc.api import Client
from solana.transaction import Transaction
from solana.system_program import TransferParams, transfer


def get_balance(client: Client, address: str) -> float:
    """Retourne le solde SOL d'une adresse Solana."""
    try:
        pubkey = Pubkey.from_string(address)
        response = client.get_balance(pubkey)
        lamports = response.value
        return lamports / 1_000_000_000  # Convertit en SOL
    except Exception as e:
        print(f"[❌] Erreur get_balance: {e}")
        return 0.0


def send_sol(client: Client, sender: Keypair, recipient: str, amount_sol: float) -> str:
    """Envoie du SOL à une adresse spécifiée."""
    try:
        recipient_pubkey = Pubkey.from_string(recipient)
        lamports = int(amount_sol * 1_000_000_000)  # Convertit SOL → lamports
        txn = Transaction().add(
            transfer(
                TransferParams(
                    from_pubkey=sender.pubkey(),
                    to_pubkey=recipient_pubkey,
                    lamports=lamports
                )
            )
        )
        result = client.send_transaction(txn, sender)
        return str(result.value)
    except Exception as e:
        return f"Erreur lors de l'envoi de SOL : {e}"


def load_keypair_from_private_key(private_key: str) -> Keypair:
    """Charge un Keypair depuis une clé privée en base58 (format Solana CLI)."""
    try:
        secret = list(map(int, private_key.strip("[]").split(",")))
        return Keypair.from_bytes(bytes(secret))
    except Exception as e:
        print(f"[❌] Erreur load_keypair_from_private_key: {e}")
        raise
