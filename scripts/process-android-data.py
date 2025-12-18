import pandas as pd
import numpy as np

def process_sensor_data():
    print("🔄 Processing Sensor Logger exports...")

    #loading CSVs
    try:
        df_batt = pd.read_csv('data/raw_sources/android/Battery.csv')
        df_temp = pd.read_csv('data/raw_sources/android/BatteryTemp.csv')
        df_accel = pd.read_csv('data/raw_sources/android/TotalAcceleration.csv')
    except FileNotFoundError as e:
        print(f"❌ Error: Could not find file. {e}")
        return

    # 2. 'time' (nanoseconds) to Datetime objects
    # Sensor Logger uses Unix Ns. We convert to seconds for easier resampling.
    for df in [df_batt, df_temp, df_accel]:
        # specific to Sensor Logger format
        df['datetime'] = pd.to_datetime(df['time'], unit='ns') 
        df.set_index('datetime', inplace=True)

    # 3. Resample to 1-Second Intervals (Downsampling)
    # We take the mean (average) for each second.
    df_batt_1s = df_batt.resample('1s').mean(numeric_only=True)
    print(df_batt_1s.columns)
    df_temp_1s = df_temp.resample('1s').mean()
    df_accel_1s = df_accel.resample('1s').mean()

    # 4. Merge into one DataFrame
    merged = pd.DataFrame()
    
    # Use the length of the shortest recording to avoid NaNs
    min_len = min(len(df_batt_1s), len(df_temp_1s), len(df_accel_1s))
    
    merged['timestamp'] = df_accel_1s.index[:min_len]
    merged['device_type'] = 'Android'
    merged['battery'] = df_batt_1s['batteryLevel'].values[:min_len]
    merged['temp'] = df_temp_1s['temp'].values[:min_len]
    
    # 5. The "Hybrid" Logic: Create derived metrics
    # Map 'TotalAcceleration' to 'Vibration'
    # (TotalAcceleration usually has a 'z' or 'magnitude' column, usually named 'z' or 'seconds_elapsed' etc in some versions. 
    # Standard SensorLogger has 'x', 'y', 'z'. We calculate magnitude.)
    acc_x = df_accel_1s['x'].values[:min_len]
    acc_y = df_accel_1s['y'].values[:min_len]
    acc_z = df_accel_1s['z'].values[:min_len]
    merged['vibration'] = np.sqrt(acc_x**2 + acc_y**2 + acc_z**2)

    # 6. Simulate CPU/Memory based on Vibration (The "Trick")
    # Assumption: If device is moving (high vibration), it's being used -> higher CPU.
    # Base CPU is 10%, adds up to 50% based on vibration intensity.
    merged['cpu'] = 10 + (merged['vibration'] * 2) + np.random.normal(0, 2, min_len)
    merged['cpu'] = merged['cpu'].clip(5, 100) # Keep between 5% and 100%
    
    merged['memory'] = 40 + np.random.normal(0, 1, min_len) # Steady memory usage

    # 7. Clean and Save
    final_df = merged[['timestamp', 'device_type', 'cpu', 'memory', 'battery', 'temp', 'vibration']]
    final_df.to_csv('data/raw_sources/android_data.csv', index=False)
    print(f"✅ Success! processed {len(final_df)} seconds of Android data.")
    print("   Saved to: data/raw_sources/android_data.csv")

if __name__ == "__main__":
    process_sensor_data()