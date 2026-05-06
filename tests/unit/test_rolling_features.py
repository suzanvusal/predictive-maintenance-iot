"""
tests/unit/test_rolling_features.py
Day 7: Rolling statistics & time-series features
Focus: Rolling mean/std/trend, exponential smoothing, change point detection
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 15:26:39 — feat: add Hampel outlier detector for sensor spike removal

# 15:26:39 — fix: CUSUM threshold too sensitive for normal machine variat
