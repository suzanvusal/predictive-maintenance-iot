"""
tests/conftest.py
Day 22: Integration tests — full pipeline
Focus: End-to-end tests: sensor data to work order creation
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 16:15:26 — test: verify DLQ routing on out-of-range readings
