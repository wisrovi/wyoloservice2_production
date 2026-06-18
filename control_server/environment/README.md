# 🏗️ Control Server: Environment <br> <span style="font-size:0.6em; font-weight:normal;">The Data Foundation Layer</span>

![Layer](https://img.shields.io/badge/layer-Infrastructure-emerald.svg)

The `environment` subsystem is the absolute bedrock of the NeuralForgeAI cluster. It must be deployed **first**, as all other services (API, Manager, and remote Workers) depend on the databases and message brokers running here.

---

## 📦 Deployed Services (`docker-compose.env.yml`)

This stack provisions the following mission-critical infrastructure:

*   **Redis (`:23437`)**: The high-speed message broker used by Celery to queue training tasks, and the in-memory database used by the React UI to store the roaming profiles (Users, Projects, Links).
*   **PostgreSQL (`:23436`)**: The relational database acting as the persistent backend for Optuna. It stores all historical trials, parameter sweeps, and fitness scores.
*   **MinIO (`:23438`, Console: `:23439`)**: An S3-compatible high-performance object storage server. Used by the GPU workers to upload the resulting YOLO weights (`best.pt`) and validation artifacts.
*   **MLflow Tracking Server (`:23435`)**: The central hub for logging metrics (loss, mAP), hyperparameters, and artifacts in real-time during training.
*   **Filebrowser (`:23443`)**: A web-based file manager providing visual access to the underlying storage volumes (useful for quick dataset inspections).

---

## 🌐 Network Architecture
This docker-compose file initiates the creation of the external `control_network`. All subsequent stacks (`api` and `manager`) must attach to this network to communicate with the databases without exposing unnecessary ports to the public internet.

---

## 🗺️ Environment Topology

```mermaid
graph LR
    subgraph Host OS (Master Node)
        subgraph control_network (Docker Bridge)
            R[(Redis :23437)]
            P[(PostgreSQL :23436)]
            M[(MinIO :23438)]
            ML[MLflow :23435]
            F[Filebrowser :23443]
        end
        
        Vol1[(Volumes: PG Data)] -.-> P
        Vol2[(Volumes: MinIO Data)] -.-> M
        Vol3[(Volumes: MLflow artifacts)] -.-> ML
    end

    ML -->|Logs run metadata| P
    ML -->|Saves artifacts| M
```

---

## 🚀 Usage

**Start the infrastructure:**
```bash
docker-compose -f docker-compose.env.yml --env-file control_host.env up -d
```

**Stop the infrastructure:**
```bash
docker-compose -f docker-compose.env.yml --env-file control_host.env down
```

*Note: Persistent data is stored in Docker volumes. Tearing down the containers with `down` will NOT delete your MLflow runs, Redis queues, or MinIO buckets.*