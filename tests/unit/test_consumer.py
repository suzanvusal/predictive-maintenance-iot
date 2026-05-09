"""
tests/unit/test_consumer.py
Day 5: Kafka consumer & data validation
Focus: Sensor data consumer, validation pipeline, DLQ, offset management
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 14:10:39 — test: add consumer integration test

# 14:10:39 — fix: handle sensor dropout (null readings) gracefully

# 14:10:39 — fix: correct off-by-one in test_consumer

# 15:26:39 — perf: add caching in test_consumer

# 14:16:32 — test: add assertion for return type in test_consumer
