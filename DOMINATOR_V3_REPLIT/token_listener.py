# token_listener.py

import asyncio
import websockets
import json
from token_scanner import process_new_token

async def listen_to_token_creations():
    uri = "wss://api.mainnet-beta.solana.com"

    async with websockets.connect(uri) as websocket:
        print("🌐 Connexion au WebSocket SOLANA...")

        subscribe_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "programSubscribe",
            "params": [
                "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA",  # SPL Token program ID
                {"encoding": "jsonParsed"}
            ]
        }

        await websocket.send(json.dumps(subscribe_request))
        print("🛰️  Abonnement aux nouveaux tokens SOLANA actif.")

        while True:
            try:
                response = await websocket.recv()
                data = json.loads(response)

                if "params" in data and "result" in data["params"]:
                    account_info = data["params"]["result"]["value"]
                    token_address = account_info.get("pubkey", "unknown")

                    print(f"🚨 Nouveau token détecté : {token_address}")
                    await process_new_token(token_address)
            except Exception as e:
                print(f"❌ Erreur dans le listener WebSocket : {e}")
                await asyncio.sleep(3)
