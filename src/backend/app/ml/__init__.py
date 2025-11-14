"""
Machine Learning module for BAHR Arabic prosody detection.

This module provides:
- Feature extraction for ML models
- Model training and evaluation utilities
- Hybrid ML+rule-based detection
- Production model loading and inference
"""

from .feature_extractor import BAHRFeatureExtractor
from .model_loader import ml_service

__all__ = ['BAHRFeatureExtractor', 'ml_service']
