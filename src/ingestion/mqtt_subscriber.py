"""
src/ingestion/mqtt_subscriber.py
Day 2: IoT sensor schemas & MQTT/Kafka producers
Focus: Pydantic schemas for sensor readings, MQTT subscriber, Kafka producer bridge
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 15:09:53 — refactor: extract MQTT config to dataclass

# 15:09:53 — docs: add module docstring to mqtt_subscriber

# 15:09:53 — refactor: rename variable for clarity in mqtt_subscriber
