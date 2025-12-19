#!/bin/bash

echo "---------------------------------------------------"
echo "🛑 Symphony Edge: Initiating Cluster Reset..."
echo "---------------------------------------------------"

#kill the background processes
echo " [Process] Stopping Control Plane (Dashboard)..."
pkill -f "streamlit run dashboard.py" || echo "   - Dashboard was not running."

echo " [Process] Stopping Edge Agent (IoT Sim)..."
pkill -f "components/iot-sim/iot_sim.py" || echo "   - IoT Agent was not running."

echo " [Process] Stopping Analysis Engine..."
pkill -f "components/analysis-engine/app.py" || echo "   - Analysis Engine was not running."

#clean data streams
echo " [Storage] Cleaning Telemetry Volumes..."
if [ -f "data/telemetry.csv" ]; then
    rm data/telemetry.csv
    echo "   - Removed active telemetry stream."
else
    echo "   - No active stream found."
fi

echo "---------------------------------------------------"
echo "✅ Cluster Reset Complete. Ready for 'make run-edge'"
echo "---------------------------------------------------"