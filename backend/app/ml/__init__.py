"""
Machine Learning module for BAHR Arabic prosody detection.

This module provides:
- Feature extraction for ML models
- Model training and evaluation utilities
- Hybrid ML+rule-based detection
"""

from .feature_extractor import BAHRFeatureExtractor

__all__ = ['BAHRFeatureExtractor']
