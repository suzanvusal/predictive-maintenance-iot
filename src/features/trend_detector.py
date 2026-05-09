"""
src/features/trend_detector.py
Day 7: Rolling statistics & time-series features
Focus: Rolling mean/std/trend, exponential smoothing, change point detection
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 14:16:32 — docs: fix typo in trend_detector
