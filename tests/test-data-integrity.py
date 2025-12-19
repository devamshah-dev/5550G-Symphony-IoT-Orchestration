import pytest
import pandas as pd
import os

# Define expected columns
EXPECTED_COLUMNS = ['timestamp', 'device_type', 'cpu', 'memory', 'battery', 'temp', 'vibration']

def test_raw_sources_exist():
    """Ensure all required simulation files are generated."""
    required_files = ['ios_data.csv', 'win11_data.csv', 'rpi_data.csv']
    for f in required_files:
        path = os.path.join('data/raw_sources', f)
        assert os.path.exists(path), f"Missing simulation file: {f}. Run generate_fake_data.py first."

def test_android_processed_data():
    path = 'data/raw_sources/android_data.csv'
    if os.path.exists(path):
        df = pd.read_csv(path)
        # Check for the calculated/hybrid columns
        assert 'vibration' in df.columns, "Android data missing 'vibration' column"
        assert 'cpu' in df.columns, "Android data missing 'cpu' column"
        # Check values are within physical bounds
        assert df['cpu'].max() <= 100, "Android CPU > 100%"
        assert df['battery'].max() <= 100, "Android Battery > 100%"

def test_telemetry_stream_schema():
    path = 'data/telemetry.csv'
    if os.path.exists(path):
        df = pd.read_csv(path)
        # if current columns match expected columns
        assert set(EXPECTED_COLUMNS).issubset(df.columns) or set(df.columns).issubset(EXPECTED_COLUMNS), \
            f"Schema mismatch. Got: {df.columns}"