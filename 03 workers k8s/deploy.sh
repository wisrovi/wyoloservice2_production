#!/usr/bin/env bash
# ==============================================================================
# NeuralForge AI — Kubernetes Worker Cluster Deployment Script
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MANIFESTS_DIR="${SCRIPT_DIR}/manifests"
ENV_FILE="${SCRIPT_DIR}/control_host.env"

echo "=================================================================="
echo "  NeuralForge AI — Deploying Kubernetes Worker Stack"
echo "=================================================================="

# 1. Verify kubectl connectivity
if ! command -v kubectl &> /dev/null; then
    echo "[ERROR] kubectl command not found. Please install kubectl and configure cluster access."
    exit 1
fi

if ! kubectl cluster-info &> /dev/null; then
    echo "[ERROR] Cannot communicate with Kubernetes API. Check your kubeconfig."
    exit 1
fi

# 2. Load Environment Variables
if [[ -f "${ENV_FILE}" ]]; then
    echo "[INFO] Loading configuration from ${ENV_FILE}..."
    # shellcheck disable=SC1090
    set -a
    source "${ENV_FILE}"
    set +a
else
    echo "[WARNING] ${ENV_FILE} not found! Using default configuration values."
    CONTROL_HOST="192.168.10.252"
    REDIS_PORT="23437"
    MINIO_PORT="9000"
    MLFLOW_PORT="5000"
    DOZZLE_HOST_PORT="8888"
    CIFS_SHARE_NAME="wyolo"
    CIFS_USER="wyolo"
    CIFS_PASS="wyolo"
    MINIO_ROOT_USER="wyolo"
    MINIO_ROOT_PASSWORD="wyolopassword"
fi

# 3. Apply Namespace
echo "[1/6] Applying namespace (train-service)..."
kubectl apply -f "${MANIFESTS_DIR}/00-namespace.yaml"

# 4. Apply RBAC (ServiceAccounts, Roles, RoleBindings)
echo "[2/6] Applying RBAC permissions..."
kubectl apply -f "${MANIFESTS_DIR}/01-rbac.yaml"

# 5. Create or Update Global ConfigMap dynamically from ENV
echo "[3/6] Applying global ConfigMap (train-service-global-config)..."
kubectl create configmap train-service-global-config \
    --namespace train-service \
    --from-literal=CONTROL_HOST="${CONTROL_HOST}" \
    --from-literal=REDIS_HOST="${CONTROL_HOST}" \
    --from-literal=REDIS_PORT="${REDIS_PORT:-23437}" \
    --from-literal=REDIS_DB="${REDIS_DB:-0}" \
    --from-literal=REDIS_URL="redis://${CONTROL_HOST}:${REDIS_PORT:-23437}/${REDIS_DB:-0}" \
    --from-literal=MINIO_HOST="${CONTROL_HOST}" \
    --from-literal=MINIO_PORT="${MINIO_PORT:-9000}" \
    --from-literal=MINIO_SECURE="false" \
    --from-literal=MINIO_BUCKET_NAME="train-service" \
    --from-literal=MLFLOW_PORT="${MLFLOW_PORT:-5000}" \
    --from-literal=MLFLOW_TRACKING_URI="http://${CONTROL_HOST}:${MLFLOW_PORT:-5000}" \
    --from-literal=CIFS_SERVER="${CONTROL_HOST}" \
    --from-literal=CIFS_SHARE_NAME="${CIFS_SHARE_NAME:-wyolo}" \
    --from-literal=CIFS_SHARE_PATH="//${CONTROL_HOST}/${CIFS_SHARE_NAME:-wyolo}" \
    --from-literal=NUM_CURRENT_TRAIN="${NUM_CURRENT_TRAIN:-1}" \
    --from-literal=MAX_GPU="${MAX_GPU:-30}" \
    --from-literal=WORKER_NAME="${WORKER_NAME:-worker_wisrovi}" \
    --from-literal=EXECUTOR_TIMEOUT_SECONDS="56160" \
    --from-literal=EXECUTOR_IMAGE="${EXECUTOR_IMAGE:-wisrovi/train_service:worker_executor_v1.0.0}" \
    --from-literal=DEFAULT_RESULTS_DIR="/wyolo/worker/train_service_results" \
    --dry-run=client -o yaml | kubectl apply -f -

# 6. Create or Update Secrets dynamically from ENV
echo "[4/6] Applying Secrets (train-service-secrets)..."
kubectl create secret generic train-service-secrets \
    --namespace train-service \
    --from-literal=CIFS_USER="${CIFS_USER:-wyolo}" \
    --from-literal=CIFS_PASS="${CIFS_PASS:-wyolo}" \
    --from-literal=MINIO_ROOT_USER="${MINIO_ROOT_USER:-wyolo}" \
    --from-literal=MINIO_ROOT_PASSWORD="${MINIO_ROOT_PASSWORD:-wyolopassword}" \
    --from-literal=AWS_ACCESS_KEY_ID="${MINIO_ROOT_USER:-wyolo}" \
    --from-literal=AWS_SECRET_ACCESS_KEY="${MINIO_ROOT_PASSWORD:-wyolopassword}" \
    --dry-run=client -o yaml | kubectl apply -f -

# 7. Apply Invoker DaemonSet
echo "[5/6] Applying Invoker DaemonSet..."
kubectl apply -f "${MANIFESTS_DIR}/04-invoker-daemonset.yaml"

# 8. Apply Dozzle DaemonSet
echo "[6/6] Applying Dozzle Log Viewer DaemonSet..."
kubectl apply -f "${MANIFESTS_DIR}/05-dozzle-daemonset.yaml"

echo ""
echo "=================================================================="
echo "  [SUCCESS] Deployment complete!"
echo "=================================================================="
echo "Status of DaemonSets in 'train-service':"
kubectl get daemonsets -n train-service -o wide
echo ""
echo "Accessing Real-Time Logs via Dozzle:"
echo "  👉 Open your browser on any worker node: http://localhost:${DOZZLE_HOST_PORT:-8888}"
echo "  👉 Or remotely: http://<WORKER_IP>:${DOZZLE_HOST_PORT:-8888}"
echo "=================================================================="
