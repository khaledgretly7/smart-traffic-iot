# dashboard/app.py
# This is the web server that serves our dashboard website
# It uses Flask — a simple Python web framework

from flask import Flask, render_template, jsonify, request
import paho.mqtt.client as mqtt
import json
import threading
import time
import sys
import os

# Add parent folder to path so we can import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import MQTT_BROKER, MQTT_PORT, MQTT_TOPIC_SENSOR, MQTT_TOPIC_CONTROL

app = Flask(__name__)

# ─── Global State ────────────────────────────────
# This stores the LATEST data received from MQTT
latest_data = {
    "timestamp"   : "Waiting for data...",
    "distances"   : [0, 0, 0, 0],
    "light_status": [False, False, False, False],
    "green_lane"  : None
}

# ─── MQTT Setup ──────────────────────────────────
def on_connect(client, userdata, flags, rc, properties=None):
    print(f"✅ Dashboard connected to MQTT broker!")
    client.subscribe(MQTT_TOPIC_SENSOR)

def on_message(client, userdata, msg):
    global latest_data
    try:
        data = json.loads(msg.payload.decode())
        latest_data = data
        print(f"📨 Dashboard received: {data}")
    except Exception as e:
        print(f"❌ Error parsing message: {e}")

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
mqtt_client.loop_start()

# ─── Web Routes ──────────────────────────────────

@app.route("/")
def index():
    """Serves the main dashboard page"""
    return render_template("index.html")

@app.route("/api/status")
def get_status():
    """Returns latest traffic data as JSON — called by the website every 2 seconds"""
    return jsonify(latest_data)

@app.route("/api/override", methods=["POST"])
def override_light():
    """Lets user manually control a traffic light"""
    data      = request.json
    lane      = data.get("lane")
    action    = data.get("action")  # "green" or "red"

    command = {"override": True, "lane": lane, "action": action}
    mqtt_client.publish(MQTT_TOPIC_CONTROL, json.dumps(command))
    print(f"🎛️  Manual override: Lane {lane} → {action}")

    return jsonify({"success": True, "message": f"Lane {lane} set to {action}"})

# ─── Start Server ─────────────────────────────────
if __name__ == "__main__":
    print("🌐 Starting Smart Traffic Dashboard...")
    print("   Open your browser and go to: http://localhost:5000")
    app.run(host="0.0.0.0", debug=True, port=5000)