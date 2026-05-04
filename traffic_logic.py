# traffic_logic.py — Updated with MQTT
import time
from config import NUMBER_OF_LANES, GREEN_LIGHT_TIME, MIN_DISTANCE_CM
from simulator import read_all_lanes
from mqtt_client import create_client, publish_sensor_data

# Track light status: True=Green, False=Red
light_status = [False, False, False, False]

def find_busiest_lane(distances):
    """Finds lane with closest car. Returns lane number or None."""
    busiest_lane = None
    min_distance = MIN_DISTANCE_CM

    for lane_number, distance in enumerate(distances):
        if distance < min_distance:
            busiest_lane = lane_number
            min_distance = distance

    return busiest_lane

def set_lights(green_lane):
    """Sets one lane green, all others red."""
    global light_status

    for lane in range(NUMBER_OF_LANES):
        light_status[lane] = (lane == green_lane)

    print("\n  🚦 Light Status:")
    for lane in range(NUMBER_OF_LANES):
        status = "🟢 GREEN" if light_status[lane] else "🔴 RED"
        print(f"     Lane {lane}: {status}")

def run_traffic_cycle(mqtt_client):
    """One full traffic cycle with MQTT publishing."""
    print("\n" + "="*40)
    print("📡 Reading all lane sensors...")
    print("="*40)

    # Step 1: Read sensors
    distances = read_all_lanes()

    # Step 2: Find busiest lane
    green_lane = find_busiest_lane(distances)

    # Step 3: Set lights
    if green_lane is not None:
        print(f"\n  ✅ Lane {green_lane} gets GREEN light")
        set_lights(green_lane)
    else:
        print("\n  ℹ️  No cars → all RED")
        set_lights(None)

    # Step 4: Send data via MQTT
    publish_sensor_data(mqtt_client, distances, light_status)

    # Step 5: Wait
    wait_time = GREEN_LIGHT_TIME if green_lane is not None else 2
    time.sleep(wait_time)

# ─── MAIN ────────────────────────────────────────
if __name__ == "__main__":
    print("🚦 Smart Traffic System Starting...")

    # Connect to MQTT
    mqtt_client = create_client()

    try:
        while True:
            run_traffic_cycle(mqtt_client)

    except KeyboardInterrupt:
        print("\n🛑 System stopped.")
        set_lights(None)
        mqtt_client.loop_stop()
        mqtt_client.disconnect()