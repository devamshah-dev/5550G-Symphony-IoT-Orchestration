# 🛰️ Symphony IoT Monitoring & Predictive Analytics Pipeline

![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![License](https://img.shields.io/badge/License-MIT-blue)
![Platform](https://img.shields.io/badge/Platform-Eclipse%20Symphony-orange)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Minikube-blue)

---

## 🚀 Overview

This repository contains an **end-to-end IoT Monitoring and Prediction System** deployed using **Eclipse Symphony** on Kubernetes.

It integrates:

- **IoT Simulators** → generate environmental telemetry  
- **Prometheus (custom image)** → scrapes raw + predicted metrics  
- **Analysis Engine (Python)** → computes moving-average temperature predictions  
- **Grafana** → visualizes real-time data & predictions  
- **Eclipse Symphony** → orchestrates all components with desired-state management  

The system provides a complete pipeline from **telemetry → scraping → prediction → visualization**.

---

## 🧩 Architecture

```text
        ┌──────────────┐
        │   IoT-Sim     │  →  Fake sensors (temp, humidity, battery)
        └──────┬────────┘
               │  /metrics
               ▼
        ┌──────────────┐
        │  Prometheus   │  →  Scrapes IoT + Analysis Engine
        └──────┬────────┘
               │  /api/v1/query
               ▼
        ┌──────────────┐
        │ Analysis Eng. │  →  Predictive metrics (moving avg)
        └──────┬────────┘
               │
               ▼
        ┌──────────────┐
        │   Grafana     │  →  Dashboards
        └──────────────┘

        Orchestrated entirely by:
        ┌──────────────────────────┐
        │    Eclipse Symphony      │
        └──────────────────────────┘

| Component               | Purpose                                     | Port | Folder               |
| ----------------------- | ------------------------------------------- | ---- | -------------------- |
| **IoT-Sim**             | Generates random telemetry                  | 8085 | `iot-sim/`           |
| **Prometheus (custom)** | Scrapes raw + predicted metrics             | 9090 | `prometheus-deploy/` |
| **Analysis Engine**     | Computes predictions and re-exports metrics | 8086 | `analysis-engine/`   |
| **Grafana**             | Visualization dashboard                     | 3000 | `grafana/`           |
| **Symphony**            | Deployment + reconciliation                 | —    | All components       |


symphony-iot-monitoring/
├── analysis-engine/
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── solution.yaml
│   ├── solutioncontainer.yaml
│   ├── instance.yaml
│
├── iot-sim/
│   ├── iot_sim.py
│   ├── Dockerfile
│   ├── iot-sim-solution.yaml
│   ├── iot-sim-instance.yaml
│   ├── iot-sim-service.yaml
│
├── prometheus-deploy/
│   ├── target.yaml
│   ├── solution.yaml
│   ├── solutioncontainer.yaml
│   ├── instance.yaml
│   ├── prometheus-config.yaml
│   ├── prometheus-custom/
│       ├── Dockerfile
│       ├── prometheus.yml
│
├── grafana/
│   ├── solution.yaml
│   ├── instance.yaml
│
└── reset-scripts/
    ├── reset-prometheus.sh
    ├── reset-iot.sh
    ├── reset-analysis.sh
    ├── reset-grafana.sh
    ├── reset-all.sh


🔧 Deployment Instructions (Minikube + Symphony)

Start cluster:

minikube start

1️⃣ Deploy IoT-Sim
kubectl apply -f iot-sim/iot-sim-solution.yaml
kubectl apply -f iot-sim/iot-sim-instance.yaml

2️⃣ Deploy Prometheus (custom image)
kubectl apply -f prometheus-deploy/target.yaml
kubectl apply -f prometheus-deploy/solution.yaml
kubectl apply -f prometheus-deploy/solutioncontainer.yaml
kubectl apply -f prometheus-deploy/prometheus-config.yaml
kubectl apply -f prometheus-deploy/instance.yaml

3️⃣ Deploy Analysis Engine
kubectl apply -f analysis-engine/solution.yaml
kubectl apply -f analysis-engine/instance.yaml

4️⃣ Deploy Grafana
kubectl apply -f grafana/solution.yaml
kubectl apply -f grafana/instance.yaml

🌐 Accessing Services

| Service                     | Command                                                                    | URL                                                            |
| --------------------------- | -------------------------------------------------------------------------- | -------------------------------------------------------------- |
| **Prometheus**              | `kubectl port-forward svc/sample-prometheus 9090:9090 -n sample-k8s-scope` | [http://localhost:9090](http://localhost:9090)                 |
| **Grafana**                 | `kubectl port-forward svc/grafana 3000:3000 -n sample-k8s-scope`           | [http://localhost:3000](http://localhost:3000)                 |
| **Analysis Engine Metrics** | —                                                                          | [http://localhost:8086/metrics](http://localhost:8086/metrics) |



| Feature                        | Description                                           |
| ------------------------------ | ----------------------------------------------------- |
| **Live IoT Telemetry**         | Temperature, humidity, battery level scraped every 5s |
| **Predictive Analytics**       | Moving-average temperature forecasting                |
| **Unified Prometheus Dataset** | Raw + predicted metrics combined                      |
| **Grafana Dashboards**         | Real-time visualization                               |
| **Symphony Orchestration**     | Automated deployment, reconciliation, self-healing    |


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

MIT License © 2025
Nafis Bhamjee & Contributors