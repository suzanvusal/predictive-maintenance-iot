# Predictive Maintenance IoT System with MLOps

Production-grade predictive maintenance pipeline processing factory IoT sensor data
to predict machine failures before they happen — saving millions in unplanned downtime.

## Architecture

```
Factory IoT Sensors (vibration, temp, pressure, RPM)
        |
        v MQTT → Kafka Bridge
Signal Processing + FFT Feature Extraction
        |
        v Redis Feature Store
Isolation Forest + LSTM + Survival Analysis Ensemble
        |
        v Failure Prediction Engine
"Machine XYZ will fail in 48 hours"
        |
        v Automated Work Order (CMMS Integration)
Maintenance Scheduled → Production Loss Avoided
        |
        v Feedback Loop (actual failure outcomes)
Evidently Drift Detection → Airflow Retraining
```

## Tech Stack

| Layer | Technology |
|-------|------------|
| IoT Protocol | MQTT (Mosquitto) |
| Streaming | Apache Kafka, Faust |
| Signal Processing | FFT, NumPy, SciPy |
| ML Models | Isolation Forest, LSTM, Survival Analysis |
| Serving | FastAPI |
| Drift Detection | Evidently AI |
| Orchestration | Apache Airflow |
| Monitoring | Prometheus, Grafana |

## Quick Start

```bash
docker compose up -d
make simulate    # Start IoT sensor simulation
make serve       # Start prediction API
```

## License
MIT
