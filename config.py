# config.py
# This file contains ALL settings for the project
# If you want to change anything, change it here only

# ─── MQTT Settings ───────────────────────────────
MQTT_BROKER = "localhost"   # Where MQTT runs (our laptop for now)
MQTT_PORT   = 1883          # Standard MQTT port number
MQTT_TOPIC_SENSOR  = "traffic/sensors"   # Topic for sensor data
MQTT_TOPIC_CONTROL = "traffic/control"   # Topic for light control

# ─── Traffic Settings ────────────────────────────
NUMBER_OF_LANES     = 4     # We have 4 lanes
GREEN_LIGHT_TIME    = 5    # Seconds a lane stays green
MIN_DISTANCE_CM     = 25    # If car is closer than this → car detected

# ─── GPIO Pin Numbers (used when Pi arrives) ─────
LANES = [
    {"trig": 23, "echo": 24, "red": 17, "green": 27},  # Lane 0
    {"trig": 5,  "echo": 6,  "red": 22, "green": 10},  # Lane 1
    {"trig": 19, "echo": 26, "red": 9,  "green": 11},  # Lane 2
    {"trig": 13, "echo": 21, "red": 0,  "green": 7},   # Lane 3
]

# ─── AWS IoT Settings ────────────────────────────
AWS_ENDPOINT    = "a28q9p2shy7ivw-ats.iot.eu-north-1.amazonaws.com"   # paste your endpoint
AWS_PORT        = 8883                   # AWS MQTT uses this port
AWS_TOPIC       = "traffic/sensors"      # same topic name
AWS_CA_PATH = r"C:\Users\khaled elgreitly\smart-traffic\AmazonRootCA1.pem"
AWS_CERT_PATH = r"C:\Users\khaled elgreitly\smart-traffic\certificate.pem.crt.crt"
AWS_KEY_PATH = r"C:\Users\khaled elgreitly\smart-traffic\private.pem.key"