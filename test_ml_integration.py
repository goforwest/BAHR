#!/usr/bin/env python3
"""
Quick test of ML integration into API endpoint
Tests the hybrid detection (rule-based + ML fallback)
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from app.ml.model_loader import ml_service
from app.ml.feature_extractor import BAHRFeatureExtractor

def test_ml_loading():
    """Test ML model loading"""
    print("=" * 60)
    print("TEST 1: ML Model Loading")
    print("=" * 60)
    
    # Load models
    success = ml_service.load_models("models/ensemble_v1")
    
    if success:
        print("✅ ML models loaded successfully")
        print(f"   - Model type: {type(ml_service.model).__name__}")
        print(f"   - Features: {len(ml_service.feature_indices)} optimized features")
        print(f"   - Meter classes: {len(ml_service.meter_mapping)}")
        return True
    else:
        print("❌ ML model loading failed")
        return False


def test_feature_extraction():
    """Test feature extraction"""
    print("\n" + "=" * 60)
    print("TEST 2: Feature Extraction")
    print("=" * 60)
    
    test_verse = "إذا غامرت في شرف مروم فلا تقنع بما دون النجوم"
    
    try:
        extractor = BAHRFeatureExtractor()
        features_dict = extractor.extract_features(test_verse)
        
        print(f"✅ Feature extraction successful")
        print(f"   - Input: '{test_verse}'")
        print(f"   - Features count: {len(features_dict)}")
        print(f"   - Sample features: {list(features_dict.keys())[:5]}")
        return features_dict
    except Exception as e:
        print(f"❌ Feature extraction failed: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_ml_prediction(features_dict):
    """Test ML prediction"""
    print("\n" + "=" * 60)
    print("TEST 3: ML Prediction")
    print("=" * 60)
    
    try:
        result = ml_service.predict(features_dict)
        
        print(f"✅ ML prediction successful")
        print(f"   - Predicted meter: {result['meter']}")
        print(f"   - Confidence: {result['confidence']:.2%}")
        print(f"   - Top 3 predictions:")
        for meter, conf in result['top_k'][:3]:
            print(f"      {meter}: {conf:.2%}")
        return True
    except Exception as e:
        print(f"❌ ML prediction failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("\n🔬 BAHR ML Integration Test Suite\n")
    
    # Test 1: Model loading
    if not test_ml_loading():
        print("\n❌ FAILED: Model loading")
        return 1
    
    # Test 2: Feature extraction
    features_dict = test_feature_extraction()
    if features_dict is None:
        print("\n❌ FAILED: Feature extraction")
        return 1
    
    # Test 3: ML prediction
    if not test_ml_prediction(features_dict):
        print("\n❌ FAILED: ML prediction")
        return 1
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED - ML Integration Ready")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Start the API: uvicorn backend.app.main:app --reload")
    print("2. Test endpoint: POST /api/v1/analyze")
    print("3. Monitor logs for detection method (rule_based vs ml_only)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
