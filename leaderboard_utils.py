import json
import os

LEADERBOARD_FILE = "leaderboard.json"

def update_leaderboard(token, amount):
    leaderboard = {}
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "r") as f:
            leaderboard = json.load(f)

    if token in leaderboard:
        leaderboard[token] += amount
    else:
        leaderboard[token] = amount

    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(leaderboard, f, indent=2)

def generate_leaderboard_text(top_n=5):
    if not os.path.exists(LEADERBOARD_FILE):
        return "Aucun trade enregistré pour l'instant."

    with open(LEADERBOARD_FILE, "r") as f:
        data = json.load(f)

    if not data:
        return "Classement vide pour le moment."

    sorted_leaderboard = sorted(data.items(), key=lambda x: x[1], reverse=True)
    message = "🏆 *Leaderboard DOMINATOR* 🏆\n\n"
    for i, (token, amount) in enumerate(sorted_leaderboard[:top_n], 1):
        message += f"{i}. `{token}` → {amount:.4f} SOL\n"
    return message
