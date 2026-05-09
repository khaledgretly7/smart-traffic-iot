# run.py
# Runs everything together — traffic logic + dashboard
import threading
import os
import sys

def run_traffic():
    os.system("python3 /home/pi/smart-traffic/traffic_logic.py")

def run_dashboard():
    os.system("python3 /home/pi/smart-traffic/dashboard/app.py")

if __name__ == "__main__":
    print("🚦 Starting Smart Traffic System...")
    print("🌐 Starting Dashboard...")
    
    # Run both at same time
    t1 = threading.Thread(target=run_traffic)
    t2 = threading.Thread(target=run_dashboard)
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()