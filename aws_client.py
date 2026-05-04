# aws_client.py
# Sends our traffic data to AWS IoT Core cloud

import paho.mqtt.client as mqtt
import json
import time
import ssl
from config import (AWS_ENDPOINT, AWS_PORT, AWS_TOPIC,
                    AWS_CERT_PATH, AWS_KEY_PATH, AWS_CA_PATH)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Connected to AWS IoT Core!")
    else:
        print(f"❌ AWS connection failed. Code: {rc}")

def on_publish(client, userdata, mid):
    print(f"☁️  Data sent to AWS successfully!")

def create_aws_client():
    """Creates a secure connection to AWS IoT Core"""
    client = mqtt.Client(client_id="smart-traffic-pi")

    # Attach callbacks
    client.on_connect = on_connect
    client.on_publish = on_publish

    # Set up SSL security certificates
    client.tls_set(
        ca_certs   = AWS_CA_PATH,
        certfile   = AWS_CERT_PATH,
        keyfile    = AWS_KEY_PATH,
        tls_version= ssl.PROTOCOL_TLSv1_2
    )

    # Connect to AWS
    print(f"🔌 Connecting to AWS IoT Core...")
    client.connect(AWS_ENDPOINT, AWS_PORT, keepalive=60)
    client.loop_start()
    time.sleep(2)

    return client

def send_to_aws(aws_client, distances, light_status):
    """Sends traffic data to the cloud"""
    data = {
        "timestamp"   : time.strftime("%Y-%m-%d %H:%M:%S"),
        "distances"   : distances,
        "light_status": light_status,
        "green_lane"  : light_status.index(True) if True in light_status else None,
        "location"    : "AL-ALAMEIN Intersection 1"
    }

    payload = json.dumps(data)
    aws_client.publish(AWS_TOPIC, payload, qos=1)
    print(f"☁️  Sent to AWS: {payload}")

# ─── Test connection ──────────────────────────────
if __name__ == "__main__":
    print("🧪 Testing AWS IoT connection...")
    aws_client = create_aws_client()

    # Send one test message
    test_data = json.dumps({
        "test"   : True,
        "message": "Hello from Smart Traffic System!",
        "time"   : time.strftime("%H:%M:%S")
    })

    aws_client.publish(AWS_TOPIC, test_data)
    print("📤 Test message sent!")
    time.sleep(3)

    aws_client.loop_stop()
    aws_client.disconnect()
    print("✅ AWS test complete!")