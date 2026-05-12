"""
src/models/lstm_trainer.py
Day 13: LSTM model for sequence-based failure prediction
Focus: PyTorch LSTM on sensor time series, sliding window, failure horizon
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 15:39:09 — feat: log training curves to MLflow every epoch

# 15:39:09 — feat: add ONNX export for optimised serving
