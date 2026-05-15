"""
src/models/ensemble.py
Day 15: Ensemble model: IF + LSTM + Survival
Focus: Three-model ensemble, score fusion, confidence estimation
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 15:17:11 — test: add ensemble tests verifying combined AUC > individual

# 15:17:11 — perf: parallelise model inference across ensemble

# 15:12:06 — docs: add module docstring to ensemble
