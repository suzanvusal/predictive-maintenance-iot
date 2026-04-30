#!/usr/bin/env python3
"""Bootstrap predictive-maintenance-iot repo. Run once locally."""
import argparse
import subprocess
from pathlib import Path

DIRS = [
    "src/ingestion", "src/features", "src/models", "src/serving",
    "src/maintenance", "src/monitoring", "src/security", "src/retraining",
    "infra/docker", "infra/k8s", "infra/grafana/dashboards",
    "infra/grafana/provisioning", "infra/prometheus", "infra/airflow",
    "infra/mqtt",
    "tests/unit", "tests/integration", "tests/load",
    "notebooks", "docs/runbooks", "scripts", "configs",
    ".github/workflows", ".automation_state", "plan", "templates"
]

BASE_FILES = {
"README.md": """\
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
""",

"pyproject.toml": """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "predictive-maintenance-iot"
version = "0.1.0"
description = "IoT predictive maintenance MLOps system"
requires-python = ">=3.11"
dependencies = [
    "kafka-python>=2.0.2",
    "paho-mqtt>=1.6.1",
    "faust-streaming>=0.10.14",
    "redis>=5.0.1",
    "pydantic>=2.5.0",
    "fastapi>=0.104.1",
    "uvicorn[standard]>=0.24.0",
    "torch>=2.1.0",
    "pytorch-lightning>=2.1.2",
    "scikit-learn>=1.3.2",
    "mlflow>=2.9.2",
    "evidently>=0.4.11",
    "apache-airflow>=2.7.3",
    "prometheus-client>=0.19.0",
    "lifelines>=0.27.7",
    "scipy>=1.11.4",
    "numpy>=1.26.2",
    "pandas>=2.1.4",
    "asyncpg>=0.29.0",
    "pyyaml>=6.0.1",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.3",
    "pytest-asyncio>=0.21.1",
    "pytest-cov>=4.1.0",
    "hypothesis>=6.92.1",
    "black>=23.11.0",
    "ruff>=0.1.7",
    "mypy>=1.7.1",
    "locust>=2.19.1",
]

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
""",

"Makefile": """\
.PHONY: up down test lint serve simulate

up:
\tdocker compose up -d
\t@echo "✓ Stack started: MQTT, Kafka, Redis, MLflow, Prometheus, Grafana"

down:
\tdocker compose down -v

test:
\tpytest tests/ -v --cov=src --cov-report=term-missing

lint:
\truff check src/ tests/ --fix

serve:
\tuvicorn src.serving.api:app --reload --port 8000

simulate:
\tpython -m src.ingestion.simulator --machines 50 --rate 10.0

clean:
\tfind . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
""",

"configs/base_config.yaml": """\
mqtt:
  host: "localhost"
  port: 1883
  topics:
    sensors: "factory/sensors/#"
    alerts:  "factory/alerts"

kafka:
  bootstrap_servers: "localhost:9092"
  topics:
    sensor_raw:     "iot.sensors.raw"
    sensor_features:"iot.sensors.features"
    predictions:    "iot.predictions"
    work_orders:    "iot.work_orders"
  consumer_group: "maintenance-consumers"

redis:
  host: "localhost"
  port: 6379
  feature_ttl_seconds: 86400

mlflow:
  tracking_uri: "http://localhost:5000"
  experiment_name: "predictive-maintenance"
  model_name: "failure-predictor"

serving:
  host: "0.0.0.0"
  port: 8000
  prediction_cache_ttl_seconds: 30

features:
  fft_window_size: 1024
  rolling_windows: [60, 300, 3600]
  anomaly_threshold: 0.7

prediction:
  failure_horizon_hours: [24, 48, 72]
  critical_threshold: 0.80
  warning_threshold: 0.50
""",

".env.example": """\
MQTT_HOST=localhost
MQTT_PORT=1883
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
REDIS_HOST=localhost
MLFLOW_TRACKING_URI=http://localhost:5000
DATABASE_URL=postgresql://iot:iot@localhost/maintenance_db
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK
CMMS_API_URL=https://your-cmms-api.com
CMMS_API_KEY=your-cmms-key
""",

".gitignore": """\
__pycache__/
*.py[cod]
.venv/
venv/
.env
*.egg-info/
.pytest_cache/
.coverage
htmlcov/
mlruns/
.mypy_cache/
data/
*.pt
*.onnx
.DS_Store
""",

"src/__init__.py": '"""Predictive Maintenance IoT MLOps System."""\n__version__ = "0.1.0"\n',
"src/ingestion/__init__.py": '"""IoT data ingestion: MQTT, Kafka, sensor schemas, simulators."""\n',
"src/features/__init__.py": '"""Feature engineering: FFT, rolling stats, anomaly scoring."""\n',
"src/models/__init__.py": '"""ML models: Isolation Forest, LSTM, Survival Analysis, ensemble."""\n',
"src/serving/__init__.py": '"""FastAPI prediction API for asset health and failure probability."""\n',
"src/maintenance/__init__.py": '"""Maintenance automation: work orders, scheduling, alerts."""\n',
"src/monitoring/__init__.py": '"""Drift detection, Prometheus metrics, alerting."""\n',
"src/security/__init__.py": '"""Security: encryption, audit logging, OT/IT access control."""\n',
"src/retraining/__init__.py": '"""Automated retraining: Airflow DAGs, validation, canary."""\n',
"tests/__init__.py": "",
"tests/unit/__init__.py": "",
"tests/integration/__init__.py": "",
"tests/load/__init__.py": "",
"templates/__init__.py": "",
".automation_state/.gitkeep": "",

"infra/prometheus/prometheus.yml": """\
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: maintenance-api
    static_configs:
      - targets: ["host.docker.internal:8000"]
    metrics_path: /metrics

  - job_name: kafka-jmx
    static_configs:
      - targets: ["kafka:9101"]
""",

"infra/mqtt/mosquitto.conf": """\
listener 1883
allow_anonymous true
persistence true
persistence_location /mosquitto/data/
log_dest stdout
""",
}


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    args = parser.parse_args()

    print("\n🚀 Bootstrapping predictive-maintenance-iot repo...")
    print(f"   Remote: {args.repo}\n")

    print("📁 Creating directories...")
    for d in DIRS:
        Path(d).mkdir(parents=True, exist_ok=True)
    print(f"   ✓ {len(DIRS)} directories created")

    print("📝 Writing base files...")
    for filepath, content in BASE_FILES.items():
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    print(f"   ✓ {len(BASE_FILES)} files written")

    print("\n🔧 Initialising Git...")
    if not Path(".git").exists():
        run(["git", "init", "-b", "main"])
    run(["git", "config", "user.name", "MLOps Engineer"])
    run(["git", "config", "user.email", "86911143+suzanvusal@users.noreply.github.com"])
    run(["git", "remote", "remove", "origin"])
    run(["git", "remote", "add", "origin", args.repo])

    print("📦 Making initial commit...")
    run(["git", "add", "-A"])
    run(["git", "commit", "-m",
         "chore: bootstrap predictive-maintenance-iot project\n\n"
         "- IoT sensor ingestion via MQTT + Kafka\n"
         "- FFT signal processing + feature engineering\n"
         "- Isolation Forest + LSTM + Survival Analysis ensemble\n"
         "- Automated work order creation + Airflow retraining"])

    print("🚀 Pushing to GitHub...")
    result = run(["git", "push", "-u", "origin", "main"])
    if result.returncode == 0:
        print("   ✓ Pushed successfully!")
    else:
        print(f"   ⚠ Push failed: {result.stderr[:200]}")

    print("\n" + "="*55)
    print("  ✅ Bootstrap complete!")
    print("="*55)
    print("\nNext steps:")
    print("  1. Add AUTOMATION_PAT secret in GitHub repo Settings")
    print("  2. Actions → Run workflow → trigger Day 1")


if __name__ == "__main__":
    main()
