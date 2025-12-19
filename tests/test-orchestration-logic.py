import pytest

def check_thermal_threshold(temp, limit=80):
    """Utility function used in Analysis Engine."""
    return temp > limit

def test_predictive_maintenance_alert():
    """Test if the logic correctly flags overheating."""
    # Normal case
    assert check_thermal_threshold(45) == False
    # Critical case
    assert check_thermal_threshold(85) == True
    # Boundary case
    assert check_thermal_threshold(80) == False

def test_device_personality_ranges():
    """Verify that simulated RPi runs hotter than iOS (Logic validation)."""
    import pandas as pd
    import os
    
    # Load data if available
    try:
        rpi = pd.read_csv('data/raw_sources/rpi_data.csv')
        ios = pd.read_csv('data/raw_sources/ios_data.csv')
        
        avg_rpi_temp = rpi['temp'].mean()
        avg_ios_temp = ios['temp'].mean()
        
        # RaspberryPi (Passive cooling) should theoretically be hotter than iOS (Active/Efficient)
        assert avg_rpi_temp > avg_ios_temp, "Simulation Logic Fail: RPi should be hotter than iOS"
    except FileNotFoundError:
        pytest.skip("Simulation data not found. Skipping logic test.")