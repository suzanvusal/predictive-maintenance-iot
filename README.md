# Predictive Maintenance IoT System with MLOps

[![CI](https://github.com/suzanvusal/predictive-maintenance-iot/actions/workflows/ci.yml/badge.svg)](https://github.com/suzanvusal/predictive-maintenance-iot/actions)
[![30-Day Build](https://github.com/suzanvusal/predictive-maintenance-iot/actions/workflows/daily_commit_automation.yml/badge.svg)](https://github.com/suzanvusal/predictive-maintenance-iot/actions)

Production-grade predictive maintenance system that processes factory IoT sensor data
in real-time to predict machine failures before they happen — saving millions in unplanned downtime.

## Architecture

```
Factory IoT Sensors (vibration, temperature, pressure, RPM)
        |
        v MQTT (Mosquitto) → Kafka Bridge
FFT Signal Processing + Rolling Statistics
        |
        v Redis Feature Store (47 engineered features)
Isolation Forest + LSTM + Weibull Survival Analysis
        |
        v Ensemble Failure Predictor
"Machine MACH-0042 will fail in 36 hours (87% probability)"
        |
        v Automated Work Order → CMMS Integration
Maintenance Scheduled → $2.3M downtime avoided
        |
        v Feedback Loop (actual failure outcomes)
Evidently Drift Detection + Grafana Dashboards
        |
        v Airflow DAG (drift triggered)
Auto Retrain → Validate → Canary Deploy
```

## Key Features

- 🔧 **Multi-sensor fusion** — vibration, temperature, pressure, RPM
- 📊 **FFT signal processing** — bearing fault frequency detection
- 🤖 **Three-model ensemble** — Isolation Forest + LSTM + Survival Analysis
- ⚡ **Sub-200ms predictions** for 1000+ asset fleet
- 📋 **Automated work orders** — integrates with any CMMS via webhook
- 🔄 **Self-healing ML** — drift detection triggers automatic retraining

## Tech Stack

| Layer | Technology |
|-------|------------|
| IoT Protocol | MQTT (Mosquitto) |
| Streaming | Apache Kafka |
| Signal Processing | FFT, NumPy, SciPy |
| Anomaly Detection | Isolation Forest |
| Sequence Model | PyTorch LSTM |
| Survival Analysis | Lifelines (Weibull AFT) |
| Serving | FastAPI |
| Experiment Tracking | MLflow |
| Drift Detection | Evidently AI |
| Orchestration | Apache Airflow |
| Monitoring | Prometheus, Grafana |
| Infrastructure | Docker Compose, Kubernetes |

## Quick Start

```bash
docker compose up -d
make simulate    # Start IoT sensor data stream (50 machines)
make serve       # Start prediction API on :8000

# Get asset health score
curl http://localhost:8000/assets/MACH-0001/health

# Get failure prediction
curl -X POST http://localhost:8000/assets/predict \
  -d '{"machine_id": "MACH-0001", "features": {"rms": 3.2, "kurtosis": 4.1}}'
```

## License
MIT

# 15:22:33 — security: add SECURITY.md with vulnerability reporting
