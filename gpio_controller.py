# gpio_controller.py
# Controls REAL sensors and REAL LEDs via GPIO pins on Raspberry Pi

import RPi.GPIO as GPIO
import time
from config import LANES, MIN_DISTANCE_CM

# Set GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def setup_pins():
    """Sets up all GPIO pins for input/output"""
    for lane in LANES:
        GPIO.setup(lane["trig"],  GPIO.OUT)
        GPIO.setup(lane["echo"],  GPIO.IN)
        GPIO.setup(lane["red"],   GPIO.OUT)
        GPIO.setup(lane["green"], GPIO.OUT)
        # Start with all lights RED
        GPIO.output(lane["red"],   GPIO.HIGH)
        GPIO.output(lane["green"], GPIO.LOW)
    print("✅ All GPIO pins configured!")

def get_distance(lane_number):
    """Reads REAL distance from HC-SR04 sensor in centimeters."""
    lane = LANES[lane_number]
    trig = lane["trig"]
    echo = lane["echo"]

    # Send trigger pulse
    GPIO.output(trig, GPIO.LOW)
    time.sleep(0.000002)
    GPIO.output(trig, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(trig, GPIO.LOW)

    # Wait for echo to start
    pulse_start = time.time()
    timeout = pulse_start + 0.04
    while GPIO.input(echo) == 0:
        pulse_start = time.time()
        if pulse_start > timeout:
            return 999  # No echo received

    # Wait for echo to end
    pulse_end = time.time()
    timeout = pulse_end + 0.04
    while GPIO.input(echo) == 1:
        pulse_end = time.time()
        if pulse_end > timeout:
            return 999  # Echo too long

    # Calculate distance
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)

    print(f"  Lane {lane_number}: {distance}cm")
    return distance

def set_led(lane_number, is_green):
    """
    Controls LED for a lane.
    is_green=True  → Green ON, Red OFF
    is_green=False → Red ON, Green OFF
    """
    lane = LANES[lane_number]
    if is_green:
        GPIO.output(lane["green"], GPIO.HIGH)
        GPIO.output(lane["red"],   GPIO.LOW)
    else:
        GPIO.output(lane["green"], GPIO.LOW)
        GPIO.output(lane["red"],   GPIO.HIGH)

def read_all_lanes():
    """Reads all 4 real sensors and returns distances list."""
    distances = []
    for lane in range(len(LANES)):
        dist = get_distance(lane)
        distances.append(dist)
        time.sleep(0.1)
    return distances

def cleanup():
    """Resets all GPIO pins safely when system stops."""
    GPIO.cleanup()
    print("🔌 GPIO cleaned up safely")