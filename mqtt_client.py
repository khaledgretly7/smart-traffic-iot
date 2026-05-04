# mqtt_client.py
# This file handles ALL communication via MQTT
# It sends sensor data and receives control commands

import paho.mqtt.client as mqtt
import json
import time
from config import MQTT_BROKER, MQTT_PORT, MQTT_TOPIC_SENSOR, MQTT_TOPIC_CONTROL

# ─── Callback Functions ──────────────────────────
# These functions run AUTOMATICALLY when something happens

def on_connect(client, userdata, flags, rc):
    """Runs when we successfully connect to the broker"""
    if rc == 0:
        print("✅ Connected to MQTT Broker!")
        # Subscribe to control topic so we receive commands
        client.subscribe(MQTT_TOPIC_CONTROL)
        print(f"📥 Subscribed to: {MQTT_TOPIC_CONTROL}")
    else:
        print(f"❌ Connection failed with code {rc}")

def on_message(client, userdata, msg):
    """Runs automatically when a message arrives"""
    topic   = msg.topic
    payload = msg.payload.decode()  # Convert bytes to text
    print(f"\n📨 Message received!")
    print(f"   Topic  : {topic}")
    print(f"   Content: {payload}")

def on_disconnect(client, userdata, rc):
    """Runs when disconnected from broker"""
    print("⚠️  Disconnected from MQTT Broker")

# ─── Main MQTT Client ────────────────────────────

def create_client():
    """Creates and returns a connected MQTT client"""
    client = mqtt.Client()

    # Attach our callback functions
    client.on_connect    = on_connect
    client.on_message    = on_message
    client.on_disconnect = on_disconnect

    # Connect to broker
    print(f"🔌 Connecting to broker at {MQTT_BROKER}:{MQTT_PORT}...")
    client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)

    # Start background thread to handle messages
    client.loop_start()
    time.sleep(1)  # Wait for connection to establish

    return client

def publish_sensor_data(client, distances, light_status):
    """
    Sends sensor data to the broker.
    Packages everything as JSON (like a neat box of data).
    """
    # Build the data package
    data = {
        "timestamp"   : time.strftime("%Y-%m-%d %H:%M:%S"),
        "distances"   : distances,      # e.g. [23, 150, 12, 98]
        "light_status": light_status,   # e.g. [False, False, True, False]
        "green_lane"  : light_status.index(True) if True in light_status else None
    }

    # Convert to JSON string and send
    payload = json.dumps(data)
    client.publish(MQTT_TOPIC_SENSOR, payload)
    print(f"\n📤 Published to '{MQTT_TOPIC_SENSOR}':")
    print(f"   {payload}")

# ─── Test if run directly ─────────────────────────
if __name__ == "__main__":
    print("🧪 Testing MQTT connection...")
    client = create_client()

    # Send 3 test messages
    for i in range(3):
        test_data = {
            "test"   : True,
            "message": f"Test message {i+1}",
            "time"   : time.strftime("%H:%M:%S")
        }
        payload = json.dumps(test_data)
        client.publish(MQTT_TOPIC_SENSOR, payload)
        print(f"📤 Sent test message {i+1}")
        time.sleep(2)

    client.loop_stop()
    client.disconnect()
    print("\n✅ MQTT test complete!")