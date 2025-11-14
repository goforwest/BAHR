"""ML Model Loader for Production API

Loads the trained RandomForest ensemble on startup and provides
prediction interface for the analyze endpoint.
"""

import joblib
import numpy as np
from pathlib import Path
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class MLModelService:
    """Singleton service for ML model inference"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        self.model = None
        self.feature_indices = None
        self.metadata = None
        self.meter_mapping = None
        self._initialized = True
        
    def load_models(self, models_dir: str = "models/ensemble_v1"):
        """Load the production RandomForest model and metadata"""
        try:
            models_path = Path(models_dir)
            
            # Load RandomForest (best performer: 60.1% test accuracy)
            model_path = models_path / "random_forest_model.pkl"
            self.model = joblib.load(model_path)
            logger.info(f"✅ Loaded RandomForest model from {model_path}")
            
            # Load optimized feature indices (45 features)
            feature_path = models_path / "optimized_feature_indices.npy"
            self.feature_indices = np.load(feature_path)
            logger.info(f"✅ Loaded {len(self.feature_indices)} optimized features")
            
            # Load metadata
            import json
            metadata_path = models_path / "ensemble_metadata.json"
            with open(metadata_path) as f:
                self.metadata = json.load(f)
            logger.info(f"✅ Loaded ensemble metadata (CV: {self.metadata.get('cv_scores', {}).get('random_forest', 'N/A')}%)")
            
            # Meter mapping (same order as training)
            self.meter_mapping = [
                'طويل', 'مديد', 'بسيط', 'وافر', 'كامل', 'هزج', 'رجز', 'رمل',
                'سريع', 'منسرح', 'خفيف', 'مضارع', 'مقتضب', 'مجتث', 'متقارب', 'متدارك'
            ]
            
            logger.info("🚀 ML Model Service initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to load ML models: {e}")
            return False
    
    def predict(self, features_dict: Dict[str, float]) -> Dict[str, any]:
        """
        Predict meter using the RandomForest model
        
        Args:
            features_dict: Dictionary of features from BAHRFeatureExtractor
            
        Returns:
            dict with keys: meter, confidence, probabilities, top_k
        """
        if self.model is None:
            raise RuntimeError("Model not loaded. Call load_models() first.")
        
        try:
            # Convert dict to array using feature names
            from app.ml.feature_extractor import BAHRFeatureExtractor
            extractor = BAHRFeatureExtractor()
            feature_names = extractor.get_feature_names()
            
            # Build feature array in correct order
            features = np.array([features_dict[fname] for fname in feature_names])
            
            # Select optimized features (71 → 45)
            if self.feature_indices is not None:
                features_optimized = features[self.feature_indices]
            else:
                features_optimized = features
            
            # Reshape for sklearn (expects 2D)
            features_2d = features_optimized.reshape(1, -1)
            
            # Get prediction and probabilities
            prediction = self.model.predict(features_2d)[0]
            probabilities = self.model.predict_proba(features_2d)[0]
            
            # Map to meter name
            meter = self.meter_mapping[prediction]
            confidence = float(probabilities[prediction])
            
            # Get top 3 predictions
            top_k_indices = np.argsort(probabilities)[-3:][::-1]
            top_k_meters = [(self.meter_mapping[i], float(probabilities[i])) for i in top_k_indices]
            
            return {
                "meter": meter,
                "confidence": confidence,
                "top_k": top_k_meters,
                "probabilities": {self.meter_mapping[i]: float(p) for i, p in enumerate(probabilities)}
            }
            
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            raise
    
    def is_loaded(self) -> bool:
        """Check if model is loaded and ready"""
        return self.model is not None


# Global singleton instance
ml_service = MLModelService()
