"""
src/models/isolation_forest.py
Day 12: Isolation Forest for anomaly detection
Focus: Isolation Forest on sensor features, contamination tuning, scoring
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 15:54:40 — feat: add anomaly threshold optimisation for precision-recal
