# ==============================================================================
# NeuralForge AI — Kubernetes Worker Stack Makefile
# ==============================================================================

SHELL := /bin/bash
NAMESPACE := wyolo-workers

.PHONY: all deploy status test-gpu logs-invoker logs-dozzle uninstall clean help

all: deploy

deploy:
	@chmod +x deploy.sh
	@./deploy.sh

status:
	@echo "=== [DAEMONSETS] ==="
	@kubectl get daemonsets -n $(NAMESPACE) -o wide
	@echo -e "\n=== [PODS] ==="
	@kubectl get pods -n $(NAMESPACE) -o wide
	@echo -e "\n=== [CONFIGMAPS & SECRETS] ==="
	@kubectl get configmaps,secrets -n $(NAMESPACE)

test-gpu:
	@echo "=== [RUNNING GPU SMOKE TEST POD] ==="
	@kubectl apply -f test_gpu_node.yaml
	@echo "Waiting for pod to complete..."
	@kubectl wait --namespace $(NAMESPACE) --for=condition=Ready pod/gpu-smoke-test --timeout=60s || true
	@kubectl logs -n $(NAMESPACE) pod/gpu-smoke-test
	@echo "Cleaning up smoke test pod..."
	@kubectl delete -f test_gpu_node.yaml

logs-invoker:
	@kubectl logs -n $(NAMESPACE) -l app=wyolo-invoker --tail=100 -f

logs-dozzle:
	@kubectl logs -n $(NAMESPACE) -l app=wyolo-dozzle --tail=100 -f

uninstall clean:
	@chmod +x uninstall.sh
	@./uninstall.sh

help:
	@echo "NeuralForge AI - Kubernetes Worker Management"
	@echo "  make deploy        - Deploy all manifests and start DaemonSets"
	@echo "  make status        - View status of worker pods and daemonsets"
	@echo "  make test-gpu      - Run a smoke test verifying NVIDIA GPU access"
	@echo "  make logs-invoker  - Stream real-time logs from the Invoker DaemonSet"
	@echo "  make logs-dozzle   - Stream logs from Dozzle log viewer"
	@echo "  make uninstall     - Remove all deployed resources"
