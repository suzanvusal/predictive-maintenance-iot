"""
tests/integration/sensor_simulator.py
Day 22: Integration tests — full pipeline
Focus: End-to-end tests: sensor data to work order creation
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 16:15:26 — feat: add sensor fault injection for testing

# 16:15:26 — refactor: extract fixtures to conftest.py
