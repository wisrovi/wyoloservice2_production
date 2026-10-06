#!/usr/bin/env bash
# ==============================================================================
# NeuralForge AI — Kubernetes Worker Stack Teardown / Uninstall Script
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MANIFESTS_DIR="${SCRIPT_DIR}/manifests"

echo "=================================================================="
echo "  NeuralForge AI — Tearing down Kubernetes Worker Stack"
echo "=================================================================="

if ! command -v kubectl &> /dev/null; then
    echo "[ERROR] kubectl command not found."
    exit 1
fi

echo "[1/4] Deleting DaemonSets (Invoker & Dozzle)..."
kubectl delete daemonset wyolo-invoker wyolo-dozzle -n wyolo-workers --ignore-not-found=true

echo "[2/4] Deleting ConfigMaps and Secrets..."
kubectl delete configmap train-service-global-config -n wyolo-workers --ignore-not-found=true
kubectl delete secret train-service-secrets -n wyolo-workers --ignore-not-found=true

echo "[3/4] Deleting RBAC (Roles, Bindings, ServiceAccounts)..."
kubectl delete -f "${MANIFESTS_DIR}/01-rbac.yaml" --ignore-not-found=true

echo "[4/4] Deleting Namespace (wyolo-workers)..."
kubectl delete -f "${MANIFESTS_DIR}/00-namespace.yaml" --ignore-not-found=true

echo ""
echo "=================================================================="
echo "  [SUCCESS] All worker resources cleaned up successfully."
echo "=================================================================="
