# test_import.py
import solana
print("Solana module path:", solana.__file__)

from solana.transaction import Transaction
print("Import Transaction: OK")
