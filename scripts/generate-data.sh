import pandas as pd
import numpy as np

def generate_device_data(device_type, rows=500):
    # Base configuration for "Personalities"
    if device_type == 'ios':
        # Efficient, handheld, battery drains
        cpu_base, cpu_noise = 15, 10
        mem_base, mem_noise = 40, 5
        temp_base, temp_noise = 30, 2
        vib_base, vib_noise = 0.5, 1.5 # Hand movement
        batt_start, batt_drain = 90, 0.05
        
    elif device_type == 'win11':
        # Heavy, hot, plugged in (desktop)
        cpu_base, cpu_noise = 45, 25
        mem_base, mem_noise = 60, 15
        temp_base, temp_noise = 55, 10
        vib_base, vib_noise = 0.1, 0.1 # Desktop fan vibration only
        batt_start, batt_drain = 100, 0 # Plugged in
        
    elif device_type == 'rpi':
        # Passive cooling (hot), steady load, static mount
        cpu_base, cpu_noise = 25, 5
        mem_base, mem_noise = 30, 2
        temp_base, temp_noise = 65, 5 # Runs hot!
        vib_base, vib_noise = 0, 0 # Mounted on wall
        batt_start, batt_drain = 100, 0

    # Generate Data
    rng = np.random.default_rng(42) # Fixed seed for consistency
    data = {
        'timestamp': pd.date_range(start='now', periods=rows, freq='1s'),
        'device_type': [device_type.capitalize()] * rows,
        'cpu': np.clip(rng.normal(cpu_base, cpu_noise, rows), 0, 100),
        'memory': np.clip(rng.normal(mem_base, mem_noise, rows), 0, 100),
        'battery': np.clip(np.linspace(batt_start, batt_start - (batt_drain * rows), rows), 0, 100),
        'temp': np.clip(rng.normal(temp_base, temp_noise, rows), 0, 100),
        'vibration': np.clip(rng.normal(vib_base, vib_noise, rows), 0, 10)
    }
    
    df = pd.DataFrame(data)
    # Save
    df.to_csv(f"data/raw_sources/{device_type}_data.csv", index=False)
    print(f"✅ Generated {rows} rows for {device_type}")

if __name__ == "__main__":
    generate_device_data('ios')
    generate_device_data('win11')
    generate_device_data('rpi') 