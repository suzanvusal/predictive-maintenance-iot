"""
src/models/data_pipeline.py
Day 11: MLflow experiment tracking & training data pipeline
Focus: MLflow setup, labelled failure dataset, train/val/test split
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 14:19:31 — test: add data pipeline tests for temporal split correctness

# 14:19:31 — refactor: separate label generation from feature extraction
