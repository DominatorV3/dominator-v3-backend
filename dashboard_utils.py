import json
from datetime import datetime
from stats_tracker import save_stats, generate_stats_graph

DASHBOARD_FILE = "dashboard.html"

def update_dashboard_data(token, status, tx_hash, amount):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        with open(DASHBOARD_FILE, "r") as f:
            html = f.read()
    except FileNotFoundError:
        html = """
        <html><head><title>DASHBOARD DOMINATOR V3</title></head><body>
        <h1>🔥 Transactions DOMINATOR</h1>
        <table border="1" cellpadding="8" cellspacing="0">
        <tr><th>Token</th><th>Status</th><th>TX</th><th>Amount</th><th>Time</th></tr>
        </table></body></html>
        """

    new_row = f"<tr><td>{token}</td><td>{status}</td><td>{tx_hash}</td><td>{round(amount, 6)}</td><td>{now}</td></tr>"

    html = html.replace("</table>", new_row + "</table>")

    with open(DASHBOARD_FILE, "w") as f:
        f.write(html)

    # Sauvegarde stats + graphique
    save_stats(token, amount)
    generate_stats_graph()

    print(f"✅ Dashboard mis à jour avec {token}")
