#!/bin/bash
# Launcher script for Worker Invoker using Docker Compose
# Author: William Rodriguez - wisrovi

# --- 1. CONFIGURATION ---
# Variables inherited from Systemd (EnvironmentFile=/etc/default/worker_invoker)
DEFAULT_IP=$(hostname -I | awk '{print $1}')
export WORKER_NAME=${WORKER_NAME:-$DEFAULT_IP}

# Process parameters (optional for manual overrides)
while [[ $# -gt 0 ]]; do
  case $1 in
    -n|--private_name)
      export WORKER_NAME="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# Generate random CPU affinity if it doesn't exist
if [ -z "$CORE_ASSIGNED" ]; then
    export CORE_ASSIGNED=$((RANDOM % $(nproc)))
fi

echo "Starting Worker Invoker Stack for: $WORKER_NAME"
echo "Assigned core: $CORE_ASSIGNED"

# --- 2. EXECUTION ---
# Enter the directory where docker-compose.yaml is located
cd /home/wisrovi/scripts/ || exit

# Use the worker name as project name to avoid collisions
PROJECT_NAME="invoker_${WORKER_NAME//./_}"

cleanup() {
    echo "Signal received. Stopping and removing containers gracefully..."
    docker-compose -p "$PROJECT_NAME" down
    exit 0
}

# Catch termination signals from systemd
trap cleanup SIGTERM SIGINT

# Re-create network if it doesn't exist (silent)
docker network create train_service 2>/dev/null || true

echo "Starting Watchdog loop... (Monitoring containers every 30 seconds)"
# --- 3. WATCHDOG LOOP ---
while true; do
    # Run in detached mode. If a container was deleted or stopped, this brings it back up.
    # It runs silently to avoid spamming the systemd journal.
    docker-compose -p "$PROJECT_NAME" up -d --remove-orphans > /dev/null 2>&1
    
    # Sleep in background and wait allows the trap to interrupt the sleep instantly
    sleep 30 &
    wait $!
done
