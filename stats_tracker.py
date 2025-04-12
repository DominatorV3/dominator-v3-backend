import json
import matplotlib.pyplot as plt
import os
from datetime import datetime

STATS_FILE = "trade_stats.json"

def update_dashboard_data(token, amount, tx_hash):
    data = load_stats()
    timestamp = datetime.utcnow().isoformat()

    entry = {
        "token": token,
        "amount": amount,
        "tx_hash": tx_hash,
        "timestamp": timestamp
    }

    data.append(entry)
    save_stats(data)
    print("✅ Dashboard mis à jour avec", token)

    generate_trade_graph()  # Génère un graphe à chaque update

def load_stats():
    if not os.path.exists(STATS_FILE):
        return []
    with open(STATS_FILE, "r") as f:
        return json.load(f)

def save_stats(data):
    with open(STATS_FILE, "w") as f:
        json.dump(data, f, indent=2)

def generate_trade_graph():
    data = load_stats()
    if len(data) < 2:
        print("⏳ Pas assez de données pour générer un graphique.")
        return

    tokens = [entry["token"] for entry in data]
    amounts = [entry["amount"] for entry in data]
    timestamps = [entry["timestamp"].split("T")[0] for entry in data]

    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, amounts, marker='o', linestyle='-')
    plt.xticks(rotation=45)
    plt.title("📈 Historique des trades")
    plt.xlabel("🕒 Date")
    plt.ylabel("💰 Montants SOL")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("graphique_trades.png")
    print("📊 Graphique généré : graphique_trades.png")
