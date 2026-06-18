# 🌐 Control Server: API & UI <br> <span style="font-size:0.6em; font-weight:normal;">Gateway and User Interface Layer</span>

![Layer](https://img.shields.io/badge/layer-Application-blue.svg)

The `api` subsystem acts as the front-facing entry point for researchers, developers, and administrators. It connects the user to the underlying infrastructure defined in the `/environment` folder.

---

## 📦 Deployed Services (`docker-compose.yaml`)

This stack provisions the core application servers:

*   **WDarwin Ops Frontend (`api-ui-1` on `:23432`)**: The React Single Page Application (SPA). It provides the interactive dashboard, configuration panels, API reference, and the training launcher interface.
*   **FastAPI Gateway (`control_server-fastapi-1` on `:23442`)**: The central REST API. It handles:
    *   YAML parsing and validation.
    *   Task enqueueing into Redis (`/train`).
    *   Real-time system telemetry via `psutil` (`/health`, `/workers`, `/tasks`).
    *   Roaming Profile persistence (Users, Projects, Settings) directly into Redis.

---

## ⚙️ Configuration Notes

*   **CORS:** The FastAPI server is configured to accept Cross-Origin Resource Sharing (CORS) from any origin (`*`), allowing the React UI to connect regardless of the domain name used to access it.
*   **Dynamic UI Targeting:** The React UI dynamically resolves the API address using the browser's URL (`window.location.hostname`), avoiding hardcoded `localhost` issues when accessed remotely.

---

## 🚀 Usage

*Ensure the `/environment` stack is running before starting the API, as FastAPI immediately attempts to ping Redis upon startup.*

**Start the API & UI:**
```bash
docker-compose up -d
```

**Stop the services:**
```bash
docker-compose down
```