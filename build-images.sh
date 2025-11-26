#!/bin/bash

set -e

echo "Building Docker image: iot-sim"
docker build -t iot-sim:latest ./iot-sim

echo "Building Docker image: analysis-engine"
docker build -t analysis-engine:latest ./analysis-engine

echo "Images built successfully"
