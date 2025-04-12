# DOMINATOR_V3_REPLIT/generate_graph_test.py

import matplotlib.pyplot as plt
import datetime
import random
import os

# Génère des données fictives de trades
def simulate_graph():
    tokens = ["TOKEN777", "TOKEN333", "TOKEN666"]
    times = [datetime.datetime.now() - datetime.timedelta(minutes=i*5) for i in range(len(tokens))]
    scores = [round(random.uniform(0.2, 0.8), 2) for _ in tokens]
    amounts = [round(random.uniform(0.01, 0.2), 4) for _ in tokens]

    plt.figure(figsize=(8, 5))
    for i in range(len(tokens)):
        plt.scatter(times[i], scores[i], s=amounts[i] * 1000, alpha=0.8, label=f"{tokens[i]}")

    plt.xlabel("Heure du Trade")
    plt.ylabel("Score IA")
    plt.title("Simu DOMINATOR - graphique_trades")
    plt.ylim(0, 1)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    path = "DOMINATOR_V3_REPLIT/graphique_trades.png"
    plt.savefig(path)
    plt.close()
    print(f"✅ Graphique généré ici : {path}")

simulate_graph()
