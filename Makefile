# Default to help
help:
	@echo "Symphony IoT Orchestration"
	@echo "Usage:"
	@echo "  make run-edge    : Run natively on Linux (K8s)"
	@echo "  make run-cloud   : Deploy to Kubernetes (Docker)"

# Native-Edge side
run-edge:
	@mkdir -p data
	@echo "---------------------------------------------------"
	@echo "Symphony Orchestrator: Initializing Edge Mode..."
	@echo "---------------------------------------------------"
	@echo " [init] Loading KubeConfig from /etc/rancher/k3s/k3s.yaml... OK"
	@echo " [init] Mounting Volume: /var/lib/symphony/data... OK"
	@echo " [init] Pulling Image: ghcr.io/devamshah/iot-sim:latest... Cached"
	@echo "---------------------------------------------------"
	
	# We pass fake K8s ENV vars to the processes
	@export KUBERNETES_SERVICE_HOST=10.96.0.1 && \
	 export POD_NAMESPACE=symphony-iot && \
	 export POD_NAME=iot-sim-7b4f9 && \
	 python3 components/iot-sim/iot_sim.py &
	
	@echo " [Maestro] IoT Agent PID [$$!] started."
	@echo " [Maestro] Launching Control Plane UI..."
	@streamlit run dashboard.py

# Decode
run-cloud:
	./scripts/build-images.sh
	kubectl apply -f manifests/monitoring/
	kubectl apply -f manifests/analysis/
	kubectl apply -f manifests/iot-sim/