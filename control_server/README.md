# 🧠 Control Server (Master Node) <br> <span style="font-size:0.6em; font-weight:normal;">NeuralForgeAI Core Deployment</span>

![Role](https://img.shields.io/badge/role-Master%20Node-0ea5e9.svg)
![Orchestration](https://img.shields.io/badge/orchestration-Docker%20Compose-2496ED.svg)

This directory contains the necessary orchestration files to deploy the **Control Plane** (Master Node) of the NeuralForgeAI cluster. The Control Server acts as the centralized brain of the platform, managing state, data, API gateways, user interfaces, and the core hyperparameter optimization loop.

---

## 🏗️ Directory Structure & Separation of Concerns

To guarantee stability, modularity, and isolated updates, the deployment of the Master Node is split into three distinct subsystems, each housed in its own subdirectory:

1.  **`/environment`**: The **Data Foundation**. Deploys persistent and foundational services like Redis (Message Broker), PostgreSQL (Relational DB for Optuna), MLflow (Experiment Tracking), MinIO (Object Storage), and Filebrowser.
2.  **`/api`**: The **Gateway & UI**. Deploys the FastAPI server (handling telemetry, YAML parsing, and Redis synchronization) and the WDarwin Ops React Frontend.
3.  **`/manager`**: The **Orchestrator**. Deploys the Celery worker dedicated exclusively to consuming the `managers` queue, executing Optuna genetic algorithms, and routing sub-tasks to the GPU nodes.

Each folder contains its own `docker-compose.yml` and `.env` template, allowing independent restarts and scaling.

---

## 🚀 Quick Start (Makefile)

A `Makefile` is provided in this root directory to simplify the sequential deployment of the entire stack.

**To deploy everything sequentially:**
```bash
make start_all
```
*This command creates the shared Docker network (`control_network`), and systematically spins up the `environment`, followed by the `api`, and finally the `manager`.*

**To stop the entire stack:**
```bash
make stop_all
```

### Individual Service Management
You can also manage the subsystems individually:
*   `make start_env` / `make stop_env`
*   `make start_api` / `make stop_api`
*   `make start_manager` / `make stop_manager`

---

## 🔧 Environment Configuration (`control_host.env`)
While each subfolder contains its own `.env` file, ensure that the IP addresses and credentials match your network setup. Specifically, the `CONTROL_HOST` variable must point to the IP address of this machine, as both the internal services and the remote GPU workers will use it to communicate.