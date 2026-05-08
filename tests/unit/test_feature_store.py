"""
tests/unit/test_feature_store.py
Day 9: Feature store & Redis caching
Focus: Redis-backed feature store, feature versioning, cache invalidation
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 14:50:43 — feat: add stale feature detection and alerting
