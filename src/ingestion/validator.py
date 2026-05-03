"""
src/ingestion/validator.py
Day 5: Kafka consumer & data validation
Focus: Sensor data consumer, validation pipeline, DLQ, offset management
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 14:10:39 — fix: remove unused import in validator
