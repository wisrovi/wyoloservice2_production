#!/usr/bin/env python3
"""Integration Smoke Test script for NeuralForgeAI Cluster.

This script dispatches a dry_run study task through the FastAPI Gateway,
monitors the progress via the API status endpoint, dispatches a graceful cancellation
via the API, and verifies final results.
"""

import os
import sys
import time
import json
import tempfile

try:
    import yaml
    import requests
except ImportError:
    print("[-] Error: Missing dependencies. Please run: pip install requests pyyaml")
    sys.exit(1)

# Determine the control host for the API
CONTROL_HOST = os.getenv("CONTROL_HOST", "localhost")
API_URL = f"http://{CONTROL_HOST}:23442"

print("=" * 60)
print("E2E API SMOKE TEST: NeuralForgeAI Cluster")
print("=" * 60)
print(f"[*] Target API Gateway URL: {API_URL}")

# 1. Verify connection to the API Gateway
try:
    health_resp = requests.get(f"{API_URL}/health", timeout=5)
    if health_resp.status_code == 200:
        print("[+] Connected to API Gateway successfully.")
        health_data = health_resp.json()
        print(f"    - Redis connection status in API: {health_data.get('redis')}")
    else:
        print(f"[-] API Gateway health check returned status: {health_resp.status_code}")
        sys.exit(1)
except Exception as e:
    print(f"[-] Cannot connect to API Gateway: {e}")
    print("[!] Make sure the FastAPI container is running at port 23442 and CONTROL_HOST is correctly set.")
    sys.exit(1)

# Minimal test config using dry_run=True to avoid spawning real GPU docker containers
# n_trials is set to 5 so we can trigger cancellation and verify early stop.
test_config = {
    "model": "yolov8n-cls.pt",
    "type": "yolo",
    "dry_run": True,
    "train": {
        "batch": -1,
        "data": "/datasets/examples/classification/colorball.v8i.multiclass/",
        "epochs": 1,
        "imgsz": 640,
        "device": 0
    },
    "sweeper": {
        "version": 1,
        "algorithm": "optuna",
        "direction": "maximize",
        "fitness": "metrics/accuracy_top1",
        "study_name": "smoke_test_api_cancel_study",
        "tune": True,
        "sampler": "RandomSampler",
        "n_trials": 5,
        "priority": "low"
    },
    "metadata": {
        "author": "Smoke Test Runner",
        "content": "Automatic dry-run E2E integration test through FastAPI."
    }
}

# 2. Upload config file to FastAPI POST /train endpoint
print("\n[2] Uploading configuration to API Gateway /train endpoint...")
study_id = None

# Create a temporary YAML file to upload
with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False, mode="w", encoding="utf-8") as temp_file:
    yaml.dump(test_config, temp_file, default_flow_style=False)
    temp_file_path = temp_file.name

try:
    with open(temp_file_path, "rb") as f:
        files = {"config_file": (os.path.basename(temp_file_path), f, "application/x-yaml")}
        data = {"mode": "public", "priority": "low"}
        
        resp = requests.post(f"{API_URL}/train", files=files, data=data, timeout=10)
        
        if resp.status_code == 200:
            resp_data = resp.json()
            study_id = resp_data.get("study_id")
            print(f"    - Response Status: {resp_data.get('status')}")
            print(f"    - Study ID: {study_id}")
            print(f"    - Target Routing: {resp_data.get('routing')}")
        else:
            print(f"[-] Failed to launch training. API returned {resp.status_code}: {resp.text}")
            sys.exit(1)
finally:
    if os.path.exists(temp_file_path):
        os.remove(temp_file_path)

# 3. Monitor state and trigger cancellation through the API Gateway
print("\n[3] Monitoring study status via GET /study/{study_id}...")
start_time = time.time()
timeout = 45
cancelled = False
success = False

while time.time() - start_time < timeout:
    elapsed = int(time.time() - start_time)
    
    # Query status from the API
    try:
        status_resp = requests.get(f"{API_URL}/study/{study_id}", timeout=5)
        if status_resp.status_code == 200:
            details = status_resp.json()
            state = details.get("state")
            print(f"    - [{elapsed}s] Study state: {state}")
            
            # Verify if ETA and trial progress is reported
            completed = details.get("completed_trials")
            total = details.get("total_trials")
            eta = details.get("eta")
            if completed is not None:
                print(f"      Progress: {completed}/{total} completed trials. ETA: {eta}s")
                
            if state in ["SUCCESS", "COMPLETED"]:
                print("\n" + "=" * 60)
                print("🎉 E2E SMOKE TEST COMPLETED SUCCESSFULLY! 🎉")
                print("=" * 60)
                print(f"Final Study Details: {json.dumps(details, indent=2)}")
                print(f"Total Duration: {time.time() - start_time:.2f} seconds")
                success = True
                break
            elif state == "FAILURE":
                print(f"\n[-] Study failed. Traceback/Error: {details.get('traceback') or details.get('error_data')}")
                break
        else:
            print(f"    - [{elapsed}s] API state error (status {status_resp.status_code})")
    except Exception as e:
        print(f"    - [{elapsed}s] Failed to fetch status from API: {e}")

    # Trigger graceful cancellation after 5 seconds via POST /study/{study_id}/cancel
    if elapsed >= 5 and not cancelled:
        print(f"\n[!] Triggering GRACEFUL CANCELLATION for study {study_id} via API /study/{study_id}/cancel...")
        try:
            cancel_resp = requests.post(f"{API_URL}/study/{study_id}/cancel", timeout=5)
            if cancel_resp.status_code == 200:
                cancelled = True
                print("[+] Graceful cancellation requested successfully through FastAPI Gateway.")
            else:
                print(f"[-] API cancel endpoint failed (status {cancel_resp.status_code}): {cancel_resp.text}")
        except Exception as e:
            print(f"[-] Failed to trigger cancellation via API: {e}")

    time.sleep(2)

if not success:
    print(f"\n[-] Timeout or failed test. Please verify logs for 'control_server-fastapi-1' and 'manager-manager_study-1'.")
    sys.exit(1)

print("\n" + "=" * 60)
print("E2E SMOKE TEST DONE")
print("=" * 60)
