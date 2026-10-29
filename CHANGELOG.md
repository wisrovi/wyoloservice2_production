# Changelog - WDarwin Ops Production

## [2.2.9] - 2026-10-29
### Added
- **Host Physical RAM and SWAP Total Export in Invoker DaemonSet:**
  - Updated `03 workers k8s/manifests/04-invoker-daemonset.yaml` hardware detector initContainer to calculate and export `WORKER_PHYSICAL_RAM_TOTAL` and `WORKER_SWAP_TOTAL` directly into the worker environment file.
  - Allows invokers and the cluster control interface to distinguish between true hardware capacities and default conservative safe allocations (60% RAM baseline).

## [2.2.8] - 2026-10-28
### Fixed
- **Worker Node Resource Guard & Freeze Prevention in DaemonSet:**
  - Updated `03 workers k8s/manifests/04-invoker-daemonset.yaml` hardware detector initContainer:
    * Removed unnecessary `resources.limits.nvidia.com/gpu: 1` from `hardware-detector` initContainer so it does not block scheduling or lock GPU devices.
    * Changed `WORKER_RAM_MEMORY` auto-configuration from 80% to max 60% of total host RAM, reserving at least 40% (minimum 4-6GB) strictly for the developer desktop and operating system to prevent swap thrashing.
    * Changed `WORKER_CPU_CORES_AVAILABLE` to reserve 2 to 4 cores strictly for developer desktop and interactive applications.

## [2.2.7] - 2026-10-28
### Changed
- Updated API service image tag to `wisrovi/train_service:api_server_v1.2.1` in `01 control_server/api/docker-compose.yaml` (supports private mode queue override and scheduled training via `start_at`).
- Updated Manager service image tag to `wisrovi/train_service:manager_orchestrator_v1.2.1` in `01 control_server/manager/docker-compose.manager.yml` (supports multi-source target queue resolution: `sweeper.debug`, root `debug`, `target_worker_queue`).

## [2.2.6] - 2026-10-26
### Added
- Documented `sweeper.debug` configuration parameter for direct worker IP node targeting (`debug: "<WORKER_IP>"`) and shared debug queue routing (`debug: true`) in `README.md`.
- Clarified that `debug` must be nested under the `sweeper:` dictionary, not at the root YAML level.
- Updated `test/config_train.yaml` template with correct `sweeper.debug` placement.

## [2.2.5] - 2026-10-06
### Added
- Production Kubernetes GPU Worker daemonset deployment guides and timeout cascades.

## [2.2.4] - 2026-08-06
### Changed
- Remapped the `gradio_invoker` service host port from `7860` to `23430` (`23430:7860`) to avoid conflicts with other host-bound Gradio instances.

### Added
- Added `deploy.resources.limits` (`cpus: '1.0'`, `memory: 100M`) to the `gradio_invoker` service to cap resource consumption on worker nodes.

## [2.2.3] - 2026-08-04
### Added
- New `gradio_invoker` service running `wisrovi/train_service:worker_invoker_gradio_v1.0.0` on port 7860, mounting `/home/wyolo/train_service_results` for results download.

### Removed
- Removed the local `build:` context from the `worker` service (now pulled from the Docker Hub image).
- Deleted the obsolete `docker-compose.extras.yaml`.

## [2.2.2] - 2026-08-04
### Refactored
- Added dynamic detection for Docker Compose: uses `docker compose` (V2) or fallback to `docker-compose` (V1) dynamically on the host to avoid script execution failures depending on installed version.

## [2.2.1] - 2026-08-03
### Added
- Integrated auto-update synchronization logic in the worker node watchdog loop (`launcher_invoker.sh`) to automatically pull the latest `docker-compose.yaml` and `launcher_worker.sh` from the GitHub production repository main branch every 10 minutes.

## [2.2.0] - 2026-07-03
### Added
- Strategic **Partnership & Community Outreach Roadmap** in the production hub, planning the pitch of NeuralForge AI to the Ultralytics/YOLO ecosystem.
- Integrated the new **Phase 4: Outreach** into the project evolution GANTT timeline.
- Updated the main portfolio Web RPG (`wisrovi.github.io`) quest guidelines and the suite main index (`wisrovi` README) to align with v2.0.0 components.

## [2.1.0] - 2026-05-27
### Added
- Unified marketing landing page for the entire ecosystem.
- Gemini API key propagation across all environment files.

### Changed
- Refactored `docker-compose.frontend.yaml` for dynamic URL handling.
