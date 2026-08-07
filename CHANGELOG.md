# Changelog - WDarwin Ops Production

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
