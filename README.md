📡 Symphony IoT Monitoring & Prediction System

Complete End-to-End Monitoring + Prediction Pipeline using Eclipse Symphony, Prometheus, Grafana, IoT Simulators, and a Python Analysis Engine.

🚀 Overview

This repository implements a cloud-native IoT monitoring and prediction system deployed using Eclipse Symphony on Kubernetes.
The system provides:
	•	Real-time IoT telemetry from simulated devices
	•	Centralized metric scraping via a custom Prometheus deployment
	•	Predictive analytics (moving-average temperature prediction) via a Python microservice
	•	Live dashboards using Grafana
	•	Automated orchestration & reconciliation managed entirely by Eclipse Symphony
	•	Reset scripts for reproducible deployments

The design demonstrates how Symphony can orchestrate a multi-service, container-based monitoring stack end-to-end.

## 🧩 Architecture

            ┌───────────────────┐
            │   IoT Simulators  │
            │  /metrics @ 8085  │
            └─────────┬─────────┘
                      │
                      ▼
            ┌───────────────────┐
            │   Prometheus      │
            │  (Custom Image)   │
            │ Scrapes: IoT, AE  │
            │        9090       │
            └─────────┬─────────┘
                      │
                      ▼
            ┌───────────────────┐
            │  Analysis Engine  │
            │ Queries PromQL    │
            │ Exposes /metrics  │
            │     @ 8086        │
            └─────────┬─────────┘
                      │
                      ▼
            ┌───────────────────┐
            │      Grafana      │
            │ Dashboards from   │
            │   Prometheus      │
            │     @ 3000        │
            └───────────────────┘

        Orchestration Layer → Eclipse Symphony
Components
Component	Purpose	Port	Folder
Prometheus	Scrapes metrics from IoT-Sim and Analysis Engine	9090	prometheus-deploy/
IoT-Sim	Generates random IoT data (temp, humidity, battery)	8085	iot-sim/
Analysis Engine	Processes data from Prometheus and emits predictions	8086	analysis-engine/

🧱 Folder Structure
symphony-iot-monitoring/
│
├── iot-sim/
│   ├── Dockerfile
│   ├── app.py
│   ├── solution.yaml
│   ├── solutioncontainer.yaml
│   ├── instance.yaml
│
├── analysis-engine/
│   ├── Dockerfile
│   ├── app.py
│   ├── requirements.txt
│   ├── solution.yaml
│   ├── solutioncontainer.yaml
│   ├── instance.yaml
│
├── prometheus-deploy/
│   ├── prometheus-config.yaml        # ConfigMap
│   ├── prometheus-custom/
│   │    ├── Dockerfile               # Custom Prometheus image
│   │    └── prometheus.yml
│   ├── solution.yaml
│   ├── solutioncontainer.yaml
│   ├── instance.yaml
│
├── grafana/
│   ├── solution.yaml
│   ├── solutioncontainer.yaml
│   ├── instance.yaml
│   ├── dashboard.json
│
├── reset-all.sh
├── reset-prometheus.sh
├── reset-iot.sh
├── reset-analysis.sh
├── reset-grafana.sh
│
└── README.md (you are here)

🛠️ Deployment Instructions

1️⃣ Start Minikube
minikube start

2️⃣ Deploy IoT Simulators
kubectl apply -f iot-sim/solution.yaml
kubectl apply -f iot-sim/instance.yaml

3️⃣ Deploy Custom Prometheus
kubectl apply -f prometheus-deploy/prometheus-config.yaml
kubectl apply -f prometheus-deploy/solution.yaml
kubectl apply -f prometheus-deploy/instance.yaml

4️⃣ Deploy Analysis Engine
kubectl apply -f analysis-engine/solution.yaml
kubectl apply -f analysis-engine/instance.yaml

5️⃣ Deploy Grafana
kubectl apply -f grafana/solution.yaml
kubectl apply -f grafana/instance.yaml

🌐 Port Forwarding

Prometheus
kubectl -n sample-k8s-scope port-forward svc/sample-prometheus-instance 9090:9090

Grafana
kubectl -n sample-k8s-scope port-forward svc/grafana-instance 3000:3000

Analysis Engine Metrics
kubectl -n sample-k8s-scope port-forward deployment/analysis-engine-instance 8086:8086

Access Prometheus → http://localhost:9090

Access Analysis Engine metrics → http://localhost:8086/metrics

## 🔄 Reset Scripts

To simplify development and ensure reproducible states, the project includes automated reset scripts for each component as well as a global reset.

### **Available Reset Scripts**

| Script Name                | Purpose |
|---------------------------|---------|
| `reset-iot.sh`            | Removes IoT-Sim solution, solutioncontainer, instance, and redeploys them cleanly. |
| `reset-prometheus.sh`     | Resets the custom Prometheus deployment (solution, instance, config). |
| `reset-analysis.sh`       | Resets the Analysis Engine Python microservice. |
| `reset-grafana.sh`        | Resets Grafana solution, container, and instance. |
| `reset-all.sh`            | Runs all individual reset scripts in sequence for a complete system refresh. |

### **Usage**

Run individual scripts:

```bash
./reset-iot.sh
./reset-prometheus.sh
./reset-analysis.sh
./reset-grafana.sh

📊 Monitoring & Prediction Features

## 📊 Monitoring & Prediction Features

| Capability                    | Description |
|------------------------------|-------------|
| **IoT Telemetry Generation** | IoT simulators emit temperature, humidity, and battery metrics. |
| **Centralized Scraping**     | Prometheus pulls metrics from all simulator pods and analysis engine. |
| **Prediction Engine**        | Python-based service computes moving-average forecasts. |
| **Metric Reinjection**       | Predicted values re-exposed on `/metrics` for Prometheus. |
| **Full Visualization**       | Grafana dashboards show real-time and predicted values. |
| **Automated Orchestration**  | Symphony deploys containers, self-heals failures, and manages replicas. |


## 👥 Contributors

We gratefully acknowledge the efforts of the team members who developed this IoT Monitoring & Prediction System:

| Name                         | Role / Contribution |
|------------------------------|----------------------|
| **Nafis Bhamjee**            | Lead Developer, Architecture Design, Prometheus/Grafana Integration |
| **Canchi Sathya**            | IoT Simulator Development, Testing |
| **Ankita Jayraj Patel**      | Documentation, Research, Config Management |
| **Oluwadamifola Ademoye**    | Pipeline Debugging, System Analysis |
| **Devam Dharmendrabhai Shah**| Service Deployment, Testing & Validation |

**Guided by:**  
**Professor Mohamed El-Darieby**

📝 License

MIT License © 2025 Nafis Bhamjee and Contributors