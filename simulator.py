# simulator.py
# This file PRETENDS to be the HC-SR04 sensors
# Since we don't have the Pi yet, we simulate random car arrivals

import random   # Used to generate random numbers
import time     # Used to add delays

def get_distance(lane_number):
    """
    Pretends to measure distance with HC-SR04 sensor.
    Returns a random distance in centimeters.
    When Pi arrives, this function will read the REAL sensor.
    """
    # 60% chance a car is detected (distance < 50cm)
    # 40% chance lane is empty (distance > 50cm)
    if random.random() < 0.6:
        distance = random.randint(5, 45)   # Car is close!
        print(f"  Lane {lane_number}: Car detected at {distance}cm")
    else:
        distance = random.randint(60, 200) # Lane is empty
        print(f"  Lane {lane_number}: Empty ({distance}cm)")
    
    return distance

def read_all_lanes():
    """
    Reads all 4 lanes and returns their distances.
    Returns a list like: [30, 150, 20, 80]
    """
    distances = []
    for lane in range(4):
        dist = get_distance(lane)
        distances.append(dist)
        time.sleep(0.1)  # Small delay between readings
    return distances