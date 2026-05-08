"""
src/features/feature_schema.py
Day 9: Feature store & Redis caching
Focus: Redis-backed feature store, feature versioning, cache invalidation
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 14:50:43 — feat: implement feature freshness checker

# 14:50:43 — refactor: abstract feature store behind interface
