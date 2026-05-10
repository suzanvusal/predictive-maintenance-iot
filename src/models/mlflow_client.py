"""
src/models/mlflow_client.py
Day 11: MLflow experiment tracking & training data pipeline
Focus: MLflow setup, labelled failure dataset, train/val/test split
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 14:19:31 — feat: add dataset statistics logging to MLflow

# 14:19:31 — fix: SMOTE failing with very few positive failure samples
