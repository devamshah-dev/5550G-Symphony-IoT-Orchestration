import psutil
import time
import csv
from datetime import datetime

# real-time stream of linux health
def log_linux_data():
    with open('data/raw_sources/linux_data.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'device_id', 'cpu_usage', 'memory_usage', 'battery_percent'])
        
        while True:
            cpu = psutil.cpu_percent(interval=1)
            mem = psutil.virtual_memory().percent
            # Battery data only on Laptops only.
            bat = psutil.sensors_battery()
            bat_pct = bat.percent if bat else 100
            
            writer.writerow([datetime.now(), 'linux-host-xubuntu', cpu, mem, bat_pct])
            f.flush()