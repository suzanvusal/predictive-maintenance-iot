.PHONY: up down test lint serve simulate

up:
	docker compose up -d
	@echo "✓ Stack started: MQTT, Kafka, Redis, MLflow, Prometheus, Grafana"

down:
	docker compose down -v

test:
	pytest tests/ -v --cov=src --cov-report=term-missing

lint:
	ruff check src/ tests/ --fix

serve:
	uvicorn src.serving.api:app --reload --port 8000

simulate:
	python -m src.ingestion.simulator --machines 50 --rate 10.0

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
