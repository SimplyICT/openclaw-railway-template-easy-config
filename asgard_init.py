import os
import subprocess
import time

def start_services():
    print("🚀 Initializing Asgard Defensive Suite...")
    
    # Start the Report Watcher
    subprocess.Popen(["python3", "/data/workspace/watcher.py"])
    
    # Start the SOC Alert Monitor
    subprocess.Popen(["python3", "/data/workspace/soc_monitor.py"])
    
    print("✅ All services active. Monitoring Bifrost and Alerts.")

if __name__ == "__main__":
    start_services()
