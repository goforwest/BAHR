#!/usr/bin/env python3
"""
Quick test to verify enhanced feature extractor has 71 features.
"""

import sys
sys.path.insert(0, 'backend')

from app.ml.feature_extractor import BAHRFeatureExtractor

# Create extractor
extractor = BAHRFeatureExtractor()

# Test verse
verse = "قِفَا نَبْكِ مِنْ ذِكْرَى حَبِيبٍ وَمَنْزِلِ"

# Extract features
features = extractor.extract_features(verse)

print(f"Total features extracted: {len(features)}")
print(f"Expected: 71 features")
print()

# Get feature names
feature_names = extractor.get_feature_names()
print(f"Feature names count: {len(feature_names)}")
print()

# Check for discriminative features
discriminative_features = [f for f in features.keys() if 'spread' in f or 'ratio' in f or 'relative' in f]
print(f"Discriminative features found: {len(discriminative_features)}")
for feat in discriminative_features[:10]:
    print(f"  {feat}: {features[feat]:.3f}")

print()
if len(features) == 71:
    print("✅ Feature extractor correctly returning 71 features!")
else:
    print(f"❌ ERROR: Expected 71 features, got {len(features)}")
