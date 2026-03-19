from flask import Flask, request, jsonify
import os
import json
from datetime import datetime

app = Flask(__name__)

DATA_DIR = "devices"

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# ------------------ API ------------------
@app.route("/api/log", methods=["POST"])
def log_data():
    data = request.json
    print("🔥 RECEIVED:", data)

    device = data.get("device", "unknown")
    device_folder = os.path.join(DATA_DIR, device)

    if not os.path.exists(device_folder):
        os.makedirs(device_folder)

    filename = datetime.now().strftime("%Y-%m-%d") + ".json"
    filepath = os.path.join(device_folder, filename)

    # append data safely
    if os.path.exists(filepath):
        try:
            with open(filepath, "r") as f:
                logs = json.load(f)
        except:
            logs = []
    else:
        logs = []

    logs.append(data)

    with open(filepath, "w") as f:
        json.dump(logs, f, indent=4)

    return jsonify({"status": "success"})

# ------------------ DASHBOARD ------------------
@app.route("/")
def dashboard():
    devices_data = {}

    if not os.listdir(DATA_DIR):
        return "<h1>📊 Device Dashboard</h1><p>No data yet...</p>"

    for device in os.listdir(DATA_DIR):
        device_path = os.path.join(DATA_DIR, device)

        total_keys = 0
        total_clicks = 0

        for file in os.listdir(device_path):
            filepath = os.path.join(device_path, file)

            try:
                with open(filepath) as f:
                    logs = json.load(f)
            except:
                logs = []

            total_keys += sum(log.get("keys", 0) for log in logs)
            total_clicks += sum(log.get("clicks", 0) for log in logs)

        devices_data[device] = {
            "keys": total_keys,
            "clicks": total_clicks
        }

    return f"""
    <html>
    <head>
        <title>Device Dashboard</title>

        <!-- Auto Refresh -->
        <meta http-equiv="refresh" content="5">

        <!-- Chart.js -->
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

        <style>
            body {{
                font-family: Arial;
                background: #f4f4f4;
                padding: 20px;
                text-align: center;
            }}
            h1 {{
                margin-bottom: 30px;
            }}
            .card {{
                background: white;
                padding: 20px;
                margin: auto;
                border-radius: 10px;
                width: 70%;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
        </style>
    </head>

    <body>
        <h1>📊 Live Device Dashboard</h1>

        <div class="card">
            <canvas id="chart"></canvas>
        </div>

        <script>
            const data = {devices_data};

            const labels = Object.keys(data);
            const keyData = labels.map(d => data[d].keys);
            const clickData = labels.map(d => data[d].clicks);

            const ctx = document.getElementById('chart').getContext('2d');

            new Chart(ctx, {{
                type: 'bar',
                data: {{
                    labels: labels,
                    datasets: [
                        {{
                            label: '⌨️ Keys Pressed',
                            data: keyData
                        }},
                        {{
                            label: '🖱️ Mouse Clicks',
                            data: clickData
                        }}
                    ]
                }},
                options: {{
                    responsive: true,
                    scales: {{
                        y: {{
                            beginAtZero: true
                        }}
                    }}
                }}
            }});
        </script>

    </body>
    </html>
    """

# ------------------ RUN ------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)