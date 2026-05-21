"""
tests/integration/test_full_pipeline.py
Day 22: Integration tests — full pipeline
Focus: End-to-end tests: sensor data to work order creation
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 16:15:26 — fix: integration test not cleaning up Redis feature store
