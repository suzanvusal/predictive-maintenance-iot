"""
src/models/anomaly_model.py
Day 12: Isolation Forest for anomaly detection
Focus: Isolation Forest on sensor features, contamination tuning, scoring
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 15:54:40 — feat: implement per-asset anomaly baseline

# 15:54:40 — fix: contamination too high causing false positive flood
