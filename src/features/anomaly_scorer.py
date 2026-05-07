"""
src/features/anomaly_scorer.py
Day 8: Anomaly scoring & sensor fusion
Focus: Multi-sensor anomaly score, Mahalanobis distance, sensor fusion
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 15:27:44 — fix: sensor fusion weights not summing to 1.0
