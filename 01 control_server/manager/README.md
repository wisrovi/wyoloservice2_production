# 🧬 Control Server: Manager <br> <span style="font-size:0.6em; font-weight:normal;">Optuna Orchestration & Trial Dispatcher</span>

![Layer](https://img.shields.io/badge/layer-Orchestration-purple.svg)

The `manager` subsystem contains the core intelligence of the hyperparameter evolution system. While the `/environment` stores the data and the `/api` receives the commands, the Manager is the entity that actually translates high-level YAML studies into actionable training tasks for the GPUs.

---

## 📦 Deployed Services

### Core Orchestrator (`docker-compose.manager.yml`)
*   **Study Manager (`manager_...`)**: A highly specialized Celery worker. It *only* listens to the `managers` queue in Redis. Its job is to:
    1.  Pick up new YAML training requests.
    2.  Connect to PostgreSQL to create or resume an Optuna Study.
    3.  Generate specific hyperparameters for the next Trial (Mutation).
    4.  Dispatch the actual training task into the `gpus_high`, `gpus_medium`, or `gpus_low` queues to be processed by the remote Worker Invokers.

### Extras (`docker-compose.manager.extras.yml`)
*   **Gradio Launcher (`:8083`)**: A fallback user interface for launching training tasks, useful for quick debugging or if the main React UI is unavailable.
*   **Optuna Dashboard (`:8082`)**: A web interface directly connected to PostgreSQL to visually inspect the progress of the Genetic Algorithms, parameter importances, and Pareto fronts.

---

## 🗺️ Manager Logic Loop

```mermaid
sequenceDiagram
    participant Queue as Redis ('managers' queue)
    participant Celery as Study Manager Worker
    participant Optuna as Optuna (PostgreSQL)
    participant GPU as Redis ('gpus_*' queues)
    
    Queue->>Celery: Pop Task (YAML Config)
    Celery->>Optuna: Load/Create Study (study_name)
    loop N Trials (Genetic Algorithm)
        Optuna-->>Celery: Suggest Hyperparameters
        Celery->>GPU: Push Train Task (Mutated YAML)
        GPU-->>Celery: Wait for result
        GPU->>Celery: Return Fitness Score (e.g. mAP 0.85)
        Celery->>Optuna: Report Trial Value
        Optuna->>Optuna: Evolve Population (TPE)
    end
    Celery->>Optuna: Finish Study
```

---

## 🚀 Usage

*Ensure the `/environment` stack is running, specifically Redis and PostgreSQL, before launching the Manager.*

**Start the Manager:**
```bash
docker-compose -f docker-compose.manager.yml --env-file control_host.env up -d
```

**Start the Extras (Gradio / Optuna Dash):**
```bash
docker-compose -f docker-compose.manager.extras.yml --env-file control_host.env up -d
```