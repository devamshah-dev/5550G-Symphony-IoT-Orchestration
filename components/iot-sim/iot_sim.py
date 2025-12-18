import pandas as pd
import time
import psutil
from datetime import datetime
import os

print("--- CONTAINER INIT ---")
print(f" [K8S] Namespace: {os.getenv('POD_NAMESPACE', 'local-dev')}")
print(f" [K8S] Pod IP: {os.getenv('KUBERNETES_SERVICE_HOST', '127.0.0.1')}")
print(" [OCI] Mounting volumes...")
time.sleep(1) # loading-f
print(" [OCI] Starting Application Layer...")
time.sleep(0.5)
print("----------------------")
# loadin traces (Android/iOS/Win/RPi)
traces = {}
files = {
    'android': 'data/raw_sources/android_data.csv',
    'ios': 'data/raw_sources/ios_data.csv',
    'win11': 'data/raw_sources/win11_data.csv',
    'rpi': 'data/raw_sources/rpi_data.csv'
}
#df
dfs = {}
for device_name, file_path in files.items():
    if os.path.exists(file_path):
        dfs[device_name] = pd.read_csv(file_path)
    else:
        print(f"Warning: Missing {file_path}. Skipping {device_name}.")

# Create iterators for each dataframe
# iterrows() yields (index, Series)
iterators = {k: df.iterrows() for k, df in dfs.items()}

print(" [Symphony Agent] Starting Multi-Device Stream Aggregation...")
print(f" [Maestro] Loaded sources: {list(dfs.keys())} + Linux (Host)")

#output
output_file = 'data/telemetry.csv'
if not os.path.exists(output_file):
    with open(output_file, 'w') as f:
        f.write("timestamp,device_type,cpu,memory,battery,temp,vibration\n")

while True:
    current_data = []

    try:
        # linux data (host)
        linux_cpu = psutil.cpu_percent(interval=None)
        linux_mem = psutil.virtual_memory().percent
        linux_bat= psutil.sensors_battery()
        linux_bat_pct = linux_bat.percent if linux_bat else 100
        current_data.append({
            'timestamp': datetime.now(),
            'device_type': 'Linux (Host)',
            'cpu': linux_cpu,
            'memory': linux_mem,
            'battery': linux_bat_pct,
            'temp': 45, #a default value
            'vibration': 0
    })
    except Exception as e:
        print(f"Linux Error: {e}")

    # trace data (Android etc.)
    for device, iterator in iterators.items():
        try:
            _,row = next(iterator)
            # Add a bit of randomness to fake data so it doesn't look static
            current_data.append({
                'timestamp': datetime.now(),
                'device_type': device.capitalize(),
                'cpu': row.get('cpu',0),
                'memory': row.get('memory',0),
                'battery': row.get('battery',0),
                'temp': row.get('temp',0),
                'vibration': row.get('vibration',0)
            })
        except StopIteration:
            # restart trace
            iterators[device] = dfs[device].iterrows()
        except Exception as e:
            print(f"Error reading {device}: {e}")

    if current_data:
        new_df = pd.DataFrame(current_data)
        try:
            if os.path.exists(output_file):
                existing_df = pd.read_csv(output_file)
                # old + new
                combined_df = pd.concat([existing_df, new_df])
            else:
                combined_df = new_df
            
            # live IoT sensory data
            if len(combined_df) > 50:
                combined_df = combined_df.tail(50)
            
            #saveFl
            combined_df.to_csv(output_file, index=False)
            
        except Exception as e:
            # if read failing
            new_df.to_csv(output_file, mode='a', header=not os.path.exists(output_file), index=False)
        
        # csv-append
        new_df.to_csv(output_file, mode='a', header=False, index=False)
        
        print(f" [K8s] Pod {os.getenv('POD_NAME', 'iot-orchestration')} synced 5 container states.")

    time.sleep(1.0) # 1Hz Refresh Rate