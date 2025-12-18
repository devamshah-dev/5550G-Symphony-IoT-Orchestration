# 📡 Symphony IoT Orchestration Platform

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Platform](https://img.shields.io/badge/platform-linux%20%7C%20k8s-blue)
![Orchestration](https://img.shields.io/badge/orchestrator-Eclipse%20Symphony-purple)

## 📖 Executive Summary
The **Symphony IoT Orchestration Platform** is a cloud-native telemetry and control plane designed to manage heterogeneous edge devices (Linux Gateways, Android Edge Nodes, RTOS sensors) at scale.

Leveraging **Eclipse Symphony** for solution lifecycle management, this project implements a "Hybrid Edge" architecture. It allows critical telemetry aggregation and predictive analysis to run natively on resource-constrained edge gateways, while maintaining full Kubernetes API compatibility for cloud-tier management.

## 🏗 Architecture
The solution follows the **Symphony Solution Model**, separating infrastructure from application logic.

*   **Control Plane:** Eclipse Symphony (Manages targets, instances, and solution binaries).
*   **Edge Tier:** Python-based telemetry agents using direct kernel hooks (`psutil`) for zero-latency monitoring.
*   **Data Pipeline:** Aggregates streams from 5 distinct OS architectures (Linux, Windows, Android, iOS, RPi) into a unified time-series stream.
*   **Visualization:** Real-time Dashboard with 30Hz polling for millisecond-level link latency tracking.

## 🚀 Deployment Modes

This repository supports two deployment targets depending on infrastructure constraints.

### 1. Cloud Native Mode (Kubernetes)
Intended for scalable cloud clusters. Deploys the full microservices stack using Helm charts and Docker containers.
```bash
# Deploys Solution Manifests to the Cluster
make run-cloud
### 2. Edge Native Mode (Bare Metal)
Intended for Edge Gateways (e.g., Raspberry Pi, Single Board Computers). Runs the orchestration agents as native system processes to minimize overhead (No Docker daemon required).
# Initializes the Agent and Control Plane locally
make run-edge

📂 Repository Structure
manifests/: Kubernetes & Symphony Solution definitions (YAML).
components/: Source code for the Analysis Engine and IoT Simulators.
data/: Persistent volume mount points for telemetry streams.
tests/: PyTest suite for validating data integrity and alerting logic.


⚡ Key Features
Multi-Tenancy: Simultaneous monitoring of Android, iOS, and Linux kernel metrics.
Self-Healing: Automatic data rotation and stream recovery logic.
Predictive Maintenance: Real-time thermal threshold analysis.
GitOps Compliance: Infrastructure defined as Code (IaC) via Symphony Manifests.

🧩 Components

| Component             | Purpose                                | Port | Directory          |
| ----------------------| -------------------------------------- | ---- | ------------------ |
| **Prometheus**        | Scrapes IoT + Analysis Engine metrics  | 9090 | `prometheus/`      |
| **Real IoT Devices**  | Generates IoT telemetry                | 8085 | `iot-sim/`         |
| **Analysis Engine**   | Computes moving-average predictions    | 8086 | `analysis-engine/` |
| **Grafana**           | Real-time monitoring dashboards        | 3000 | `grafana/`         |
| **Symphony**          | Orchestration and lifecycle management | N/A  | All solution dirs  |


---

⚙️ Deployment Instructions

1️⃣ Start Minikube  
minikube start  

2️⃣ Deploy Prometheus  
kubectl apply -f prometheus/solution.yaml  
kubectl apply -f prometheus/instance.yaml  

3️⃣ Deploy IoT-Sim  
kubectl apply -f iot-sim/solution.yaml  
kubectl apply -f iot-sim/instance.yaml  

4️⃣ Deploy Analysis Engine  
kubectl apply -f analysis-engine/solution.yaml  
kubectl apply -f analysis-engine/instance.yaml  

5️⃣ Deploy Grafana  
kubectl apply -f grafana/solution.yaml  
kubectl apply -f grafana/instance.yaml  

🔍 Accessing the System  

Prometheus  
kubectl port-forward svc/sample-prometheus 9090:9090 -n sample-k8s-scope  
→ http://localhost:9090  

Grafana  
kubectl port-forward svc/grafana 3000:3000 -n sample-k8s-scope  
→ http://localhost:3000  

IoT-Sim Metrics → http://localhost:8085/metrics  

Analysis Engine Predictions → http://localhost:8086/metrics  



📊 Features

| Feature                     | Description                                        |
| --------------------------- | -------------------------------------------------- |
| **Live IoT Telemetry**      | Sensor data scraped every 5 seconds                |
| **Predictive Analytics**    | Moving-average temperature forecasting             |
| **Unified Prometheus TSDB** | Raw + predicted metrics in one dataset             |
| **Grafana Dashboards**      | Real-time, low-latency visualization               |
| **Symphony Orchestration**  | Automated deployment, reconciliation, self-healing |

👥 Contributors

| Name                          | Contribution                                           |
| ----------------------------- | -------------------------------------------------------|
| **Devam Dharmendrabhai Shah** | Lead Development, Extension Development, Research, CI/CD                              |                                                        |
| **Nafis Bhamjee**             | Architecture, Prometheus/Grafana Integration   		 |
| **Canchi Sathya**             | Validation, Documentation                              |
| **Ankita Jayraj Patel**       | Documentation, Research, Configuration                 |
| **Oluwadamifola Ademoye**     | Documentation                                   		 |


Guided by:
Professor Mohamed El-Darieby

📜 License

© 2025 Symphony IoT Project. Powered by Eclipse Symphony.
