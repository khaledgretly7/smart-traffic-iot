# 🚦 Smart Traffic Control System
### AL-ALAMEIN Smart City — CSE 464: IoT Final Project

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![MQTT](https://img.shields.io/badge/MQTT-Mosquitto-orange?logo=eclipse-mosquitto)
![AWS](https://img.shields.io/badge/Cloud-AWS%20IoT%20Core-yellow?logo=amazon-aws)
![Flask](https://img.shields.io/badge/Dashboard-Flask-green?logo=flask)
![Pi](https://img.shields.io/badge/Gateway-Raspberry%20Pi%204-red?logo=raspberry-pi)

---

## 📋 Project Overview

A fully functional IoT-based Smart Traffic Control System designed for the 
AL-ALAMEIN Smart City, Egypt. The system dynamically manages traffic lights 
at a 4-lane intersection using real-time sensor data, eliminating the 
inefficiency of fixed-cycle traffic signals.

---

## 🎯 Problem Statement

Traditional traffic lights operate on fixed timers regardless of actual 
traffic conditions, causing:
- Unnecessary waiting at empty intersections
- Increased fuel consumption and CO2 emissions
- No data collection for urban planning

---

## ✅ Proposed Solution

An IoT system that:
- **Detects** vehicles using HC-SR04 ultrasonic sensors
- **Decides** which lane is busiest using real-time data
- **Controls** traffic lights dynamically via Raspberry Pi GPIO
- **Sends** all data to AWS IoT Core for cloud storage
- **Displays** live status on a web dashboard

---

## 🏗️ System Architecture
[HC-SR04 Sensors x4] ──GPIO──► [Raspberry Pi 4]
[Red/Green LEDs  x8] ◄─GPIO──      │
│ MQTT (Local)
[Mosquitto Broker]
│
│ MQTT over TLS
[AWS IoT Core ☁️]
│
[Web Dashboard 🌐]

<img width="1152" height="928" alt="system smart architicture" src="https://github.com/user-attachments/assets/e6a84356-1073-4d57-9f0d-410d5d58488d" />


### 3-Layer IoT Architecture

| Layer | Components |
|---|---|
| **Device Layer** | 4x HC-SR04 sensors, 4x Red LEDs, 4x Green LEDs, 8x 220Ω resistors |
| **Gateway Layer** | Raspberry Pi 4, Mosquitto MQTT Broker, Python traffic logic |
| **Cloud Layer** | AWS IoT Core, Flask Web Dashboard |

---

## 🛒 Hardware Components

| Component | Quantity | Purpose |
|---|---|---|
| Raspberry Pi 4 Model B | 1 | Gateway + Controller |
| HC-SR04 Ultrasonic Sensor | 4 | Vehicle detection |
| Red LED (5mm) | 4 | Red traffic light |
| Green LED (5mm) | 4 | Green traffic light |
| 220Ω Resistor | 8 | LED current limiting |
| Breadboard | 1 | Component wiring |
| Jumper Wires (M-F) | 20+ | GPIO connections |
| MicroSD Card (16GB+) | 1 | Raspberry Pi OS |

---

## 🔌 GPIO Pin Assignment

| Lane | TRIG | ECHO | Red LED | Green LED |
|---|---|---|---|---|
| Lane 0 | GPIO 23 | GPIO 24 | GPIO 17 | GPIO 27 |
| Lane 1 | GPIO 5  | GPIO 6  | GPIO 22 | GPIO 10 |
| Lane 2 | GPIO 19 | GPIO 26 | GPIO 9  | GPIO 11 |
| Lane 3 | GPIO 13 | GPIO 21 | GPIO 0  | GPIO 7  |

---

## 📁 Project Structure
smart-traffic-iot/
│
├── config.py              # All settings and pin assignments
├── simulator.py           # Sensor simulator (no hardware needed)
├── traffic_logic.py       # Core traffic management algorithm
├── mqtt_client.py         # Local MQTT communication
├── aws_client.py          # AWS IoT Core cloud connection
├── gpio_controller.py     # Real hardware GPIO control (Pi only)
│
└── dashboard/
├── app.py             # Flask web server
├── templates/
│   └── index.html     # Real-time web dashboard
└── static/

---

## ⚙️ How It Works

1. HC-SR04 sensors measure distance to nearest vehicle in each lane
2. If distance < 50cm → car detected in that lane
3. Algorithm finds the lane with the closest car (highest priority)
4. That lane gets the green light for 10 seconds
5. All data published via MQTT to local broker and AWS cloud
6. Web dashboard updates every 2 seconds with live status

---

## 🚀 Getting Started

### Prerequisites

```bash
pip install paho-mqtt flask fake-rpigpio
```

Also install **Mosquitto MQTT Broker**:
👉 mosquitto.org/download

### Run on Windows (Simulation Mode)

```bash
# Terminal 1 — Start the traffic system
python traffic_logic.py

# Terminal 2 — Listen to MQTT messages
mosquitto_sub -h localhost -t "traffic/sensors"

# Terminal 3 — Start the web dashboard
cd dashboard
python app.py
```

Then open your browser at: **http://localhost:5000**

### Run on Raspberry Pi (Real Hardware)

```bash
# Copy project to Pi
scp -r smart-traffic-iot/ pi@<PI_IP>:/home/pi/

# SSH into Pi
ssh pi@<PI_IP>

# Install dependencies
pip3 install paho-mqtt flask RPi.GPIO --break-system-packages

# Run the system
python3 traffic_logic.py
```

---

## ☁️ AWS IoT Core Setup

1. Create an AWS account at aws.amazon.com
2. Go to IoT Core → Create a Thing named `smart-traffic-pi`
3. Auto-generate certificates and download all 3 files
4. Create and attach a policy allowing Connect, Publish, Subscribe, Receive
5. Copy your endpoint to `config.py`
6. Place certificate files in the project root

---

## 🌐 Web Dashboard Features

- ✅ Real-time traffic light visualization (4 lanes)
- ✅ Live distance readings per lane
- ✅ Car detection status badges
- ✅ Active green lane indicator
- ✅ Manual override buttons (Force Green / Force Red)
- ✅ Auto-updates every 2 seconds

---

## 🧪 Test Strategy

| Test | Description | Result |
|---|---|---|
| TC-01 | Single sensor detection | ✅ Pass |
| TC-02 | Empty lane detection | ✅ Pass |
| TC-03 | Green light priority algorithm | ✅ Pass |
| TC-04 | LED output verification | ✅ Pass |
| TC-05 | MQTT local publishing | ✅ Pass |
| TC-06 | AWS cloud connectivity | ✅ Pass |
| TC-07 | Dashboard live update | ✅ Pass |
| TC-08 | Manual override | ✅ Pass |
| TC-09 | Green light timer accuracy | ✅ Pass |
| TC-10 | System restart recovery | ✅ Pass |
| TC-11 | Tie-breaking (equal distances) | ✅ Pass |
| TC-12 | Network disconnection handling | ✅ Pass |

---

## 👨‍💻 Technologies Used

- **Python 3.x** — Core logic and backend
- **Raspberry Pi 4** — Gateway and GPIO controller
- **HC-SR04** — Ultrasonic distance sensing
- **Mosquitto** — Local MQTT broker
- **paho-mqtt** — Python MQTT client library
- **AWS IoT Core** — Cloud messaging and storage
- **Flask** — Web server for dashboard
- **HTML / CSS / JavaScript** — Frontend dashboard

---

## 📄 License

This project was developed as a Final Project for CSE 464: Internet of Things  
at AL-ALAMEIN International University, Egypt.

Submitted to: **Dr. Ahmed Shalaby**  
Academic Year: 2025 – 2026
