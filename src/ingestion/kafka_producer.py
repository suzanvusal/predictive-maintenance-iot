"""
src/ingestion/kafka_producer.py
Day 2: IoT sensor schemas & MQTT/Kafka producers
Focus: Pydantic schemas for sensor readings, MQTT subscriber, Kafka producer bridge
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 15:09:53 — feat: implement realistic IoT sensor data simulator
