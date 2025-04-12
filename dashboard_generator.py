import json
from datetime import datetime

HTML_FILE = "dashboard.html"
DATA_FILE = "dashboard_data.json"

def generate_dashboard():
    if not os.path.exists(DATA_FILE):
        return

    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    html = """
    <html>
    <head>
        <title>DASHBOARD DOMINATOR V3</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #111; color: #eee; padding: 20px; }
            h1 { color: #00FF88; }
            table { width: 100%; border-collapse: collapse; }
            th, td { border: 1px solid #444; padding: 8px; text-align: center; }
            th { background-color: #222; }
            tr:nth-child(even) { background-color: #1a1a1a; }
        </style>
    </head>
    <body>
        <h1>🔥 DASHBOARD DOMINATOR V3</h1>
        <table>
            <tr>
                <th>Token</th>
                <th>Status</th>
                <th>TX Hash</th>
                <th>Montant (SOL)</th>
                <th>Heure</th>
            </tr>
    """

    for tx in reversed(data[-50:]):  # Derniers 50
        html += f"""
        <tr>
            <td>{tx['token']}</td>
            <td>{tx['status']}</td>
            <td>{tx['tx_hash']}</td>
            <td>{tx['amount']}</td>
            <td>{tx['time']}</td>
        </tr>
        """

    html += "</table></body></html>"

    with open(HTML_FILE, "w") as f:
        f.write(html)
