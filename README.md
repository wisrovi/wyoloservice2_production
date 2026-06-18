# 🧠 NeuralForgeAI & WDarwin Ops <br> <span style="font-size:0.6em; font-weight:normal;">Production Environment & Ecosystem Hub</span>

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Status](https://img.shields.io/badge/status-production-success.svg)
![Docker](https://img.shields.io/badge/docker-ready-2496ED.svg?logo=docker)

**NeuralForgeAI** (y su panel de control **WDarwin Ops**) es una plataforma de grado empresarial diseñada para la **orquestación distribuida, el entrenamiento escalable y la optimización evolutiva de hiperparámetros (Genetic Algorithms)** para arquitecturas avanzadas de visión artificial, específicamente **YOLOv8** y **YOLOv11**.

El objetivo central de este sistema es desacoplar la capa de interfaz de usuario de la capa de cómputo intensivo, permitiendo a investigadores y desarrolladores enviar configuraciones YAML simples hacia un clúster centralizado. El clúster se encarga de balancear la carga, asignar prioridades, evolucionar modelos y registrar todas las métricas sin intervención manual.

---

## 🛠️ Stack Tecnológico

El proyecto está construido sobre un stack moderno y de alto rendimiento:

### Frontend (UI)
*   **Core:** React 19, TypeScript
*   **Build System:** Vite, Node.js (18-alpine)
*   **Styling:** Tailwind CSS (v3.4, PostCSS nativo)
*   **Icons:** Lucide React

### Backend (API & Orchestration)
*   **API Gateway:** FastAPI, Python 3.10, Uvicorn (Endpoints RESTful)
*   **Task Queue:** Celery
*   **Hyperparameter Optimization:** Optuna (TPESampler, Genetic Algorithms)
*   **System Telemetry:** `psutil`

### Infraestructura y Datos
*   **Message Broker / State:** Redis
*   **Relational Database:** PostgreSQL (para estudios de Optuna)
*   **Artifacts Storage:** MinIO (compatible con S3)
*   **Experiment Tracking:** MLflow
*   **Deployment:** Docker Compose, Systemd (Watchdogs de resiliencia), Watchtower

---

## 🧩 Ecosistema de Microservicios

El sistema se compone de múltiples piezas especializadas que interactúan de forma asíncrona:

| Microservicio | Origen (Repo) | Descripción y Propósito |
| :--- | :--- | :--- |
| **Control Host (Infra)** | `wyoloservice2_control_server` | Levanta los cimientos de datos: Redis (colas), PostgreSQL (DB), MLflow (métricas) y MinIO (pesos). |
| **API Server** | `NeuralForgeAI/api` | Servidor FastAPI (`:23442`). Recibe los YAMLs, provee telemetría real del cluster y gestiona la persistencia de usuarios/proyectos en Redis. |
| **WDarwin Ops (UI)** | `NeuralForgeAI/UI` | Single Page Application en React (`:23432`). Panel de control global, dashboard de observabilidad, y gestión de identidad (Roaming Profile). |
| **Study Manager** | `wyoloservice2_manager` | Consumidor de Celery. Escucha la cola `managers`, recibe los estudios de Optuna, crea trials (mutaciones) y los envía a la cola de GPUs. |
| **Worker Invoker** | `wyoloservice2_invoker` | Nodo GPU de ejecución pesada. Toma tareas de las colas de prioridad (`gpus_high`, etc.), entrena YOLO y envía resultados a MLflow y MinIO. |
| **Gradio / Simple UI** | `wyoloservice2_manager/UI` | Interfaz alternativa (Fallback) levantada con Gradio para operaciones rápidas sin React. |

---

## 🗺️ Diagramas de Arquitectura

### 1. Relación de Repositorios (Codebase)

```mermaid
graph TD
    subgraph "Monorepo Lógico (Train Service 2)"
        P[wyoloservice2_production] -->|Define despliegue para| C[wyoloservice2_control_server]
        P -->|Construye imágenes desde| N[NeuralForgeAI]
        P -->|Instala nodos desde| I[wyoloservice2_invoker]
        P -->|Orquesta manager de| M[wyoloservice2_manager]
        
        N -->|Contiene| N_API(API FastAPI)
        N -->|Contiene| N_UI(React UI)
    end
    classDef main fill:#0d1117,stroke:#0ea5e9,stroke-width:2px,color:#fff;
    class P main;
```

### 2. Arquitectura del Sistema (Hub and Spoke)

```mermaid
graph TD
    Client((Investigador / Browser)) -->|HTTP/REST| UI[WDarwin Ops React UI]
    Client -->|HTTP/REST| API[FastAPI Gateway]
    UI -->|Sincronización Dinámica| API
    
    subgraph "Control Plane (Master Node)"
        API -->|Cola YAML| Redis[(Redis Broker)]
        API -->|Read Telemetry| Redis
        Redis <--> Manager[Optuna Manager]
        Manager <--> PostgreSQL[(PostgreSQL)]
        MLflow[MLflow Server] <--> PostgreSQL
        MinIO[(MinIO S3)]
    end

    subgraph "Compute Fleet (GPU Nodes)"
        Worker1[Invoker GPU 01]
        Worker2[Invoker GPU 02]
        WorkerN[Invoker GPU N]
    end

    Manager -->|Despacha Trials| Redis
    Redis -->|Consume Cola| Worker1
    Redis -->|Consume Cola| Worker2
    Redis -->|Consume Cola| WorkerN
    
    Worker1 -->|Registra Métricas| MLflow
    Worker1 -->|Sube best.pt| MinIO
```

### 3. Flujo de Datos (Lanzamiento de Entrenamiento)

```mermaid
sequenceDiagram
    participant User as Usuario (React UI)
    participant API as FastAPI
    participant Redis as Redis (Queue)
    participant Manager as Optuna Manager
    participant Worker as GPU Invoker
    participant Tracking as MLflow / MinIO

    User->>API: POST /train (config.yaml)
    API->>Redis: Encola tarea en "managers"
    API-->>User: Retorna Study ID (200 OK)
    
    Redis->>Manager: Recibe YAML
    Manager->>Manager: Inicia Optuna Study
    Manager->>Redis: Encola Trial en "gpus_high"
    
    Redis->>Worker: Asigna tarea al nodo libre
    Worker->>Worker: Descarga Dataset & Inicia YOLO
    
    loop Durante el Entrenamiento
        Worker->>Tracking: Loggea Epochs, Loss, mAP
    end
    
    Worker->>Tracking: Sube artefactos (best.pt, confusion_matrix.png)
    Worker->>Manager: Retorna 'Accuracy' (Fitness)
    Manager->>Manager: Genera nueva mutación (Siguiente Trial)
```

---

## 🚀 Despliegue en Producción

### Nodo de Control (Master)
Levanta la infraestructura base, la base de datos, la API y la interfaz React.

```bash
# 1. Levantar variables de entorno
cd wyoloservice2_production/control_server
make start_env

# 2. Levantar API y UI (Construidas nativamente)
make start_api

# 3. Levantar Optuna Manager
make start_manager
```

### Nodos GPU (Workers)
Cada máquina que tenga tarjetas gráficas debe registrarse en el clúster ejecutando el script de instalación automática (Watchdog).

```bash
cd wyoloservice2_production/workers
sudo chmod +x install.sh
sudo ./install.sh
```
*El script crea un demonio de `systemd` que garantiza que el worker se reinicie automáticamente ante fallos (indestructible) y configura `Watchtower` para descargar actualizaciones desde Docker Hub cada 10 minutos.*

---

## 👨‍💻 Autor

**William Steve Rodriguez Villamizar (wisrovi)**  
*AI Leader & Solutions Architect*  
[LinkedIn Profile](https://www.linkedin.com/in/wisrovi-rodriguez/)

> *"Bridging the gap between complex AI research and scalable industrial applications."*