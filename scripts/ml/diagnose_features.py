#!/usr/bin/env python3
"""
Diagnose why ML models are performing poorly.
Check feature distributions and correlations.
"""

import sys
import numpy as np
import pandas as pd

sys.path.insert(0, 'backend')

# Load the saved features
X = np.load('data/ml/X_train.npy')
y = np.load('data/ml/y_train.npy')

with open('data/ml/feature_names.json', 'r') as f:
    import json
    feature_names = json.load(f)

print("=" * 80)
print("FEATURE DISTRIBUTION DIAGNOSIS")
print("=" * 80)
print()

# Create DataFrame
df = pd.DataFrame(X, columns=feature_names)
df['meter_id'] = y

print(f"Dataset shape: {X.shape}")
print(f"Meters: {np.unique(y)}")
print()

# Check similarity features
similarity_features = [f for f in feature_names if f.startswith('similarity_to_meter_')]

print("Similarity Features Statistics:")
print("-" * 80)
for feat in similarity_features[:5]:  # Show first 5
    values = df[feat]
    print(f"{feat}:")
    print(f"  Mean: {values.mean():.3f}, Std: {values.std():.3f}")
    print(f"  Min: {values.min():.3f}, Max: {values.max():.3f}")
    print(f"  Unique values: {len(values.unique())}")
    print()

# Check pattern features
print("Pattern Features Statistics:")
print("-" * 80)
pattern_features = ['pattern_length', 'sakin_count', 'mutaharrik_count', 'sakin_ratio']
for feat in pattern_features:
    values = df[feat]
    print(f"{feat}:")
    print(f"  Mean: {values.mean():.3f}, Std: {values.std():.3f}")
    print(f"  Min: {values.min():.3f}, Max: {values.max():.3f}")
    print()

# Check if similarity features are all ~1.0 (problem!)
print("Checking for feature quality issues:")
print("-" * 80)

# Average similarity across all meters for each verse
avg_similarities = df[similarity_features].mean(axis=1)
print(f"Average similarity across all meters:")
print(f"  Mean: {avg_similarities.mean():.3f}")
print(f"  Std: {avg_similarities.std():.3f}")
print()

if avg_similarities.mean() > 0.9:
    print("❌ PROBLEM DETECTED: All similarity features are too high!")
    print("   This means features aren't discriminative.")
    print("   The model can't tell meters apart.")
    print()

# Check for a sample verse
sample_idx = 0
print(f"Sample verse (meter_id = {y[sample_idx]}):")
print("-" * 80)
sample_sims = {feat: df.loc[sample_idx, feat] for feat in similarity_features}
sorted_sims = sorted(sample_sims.items(), key=lambda x: x[1], reverse=True)
print("Top 5 similarities:")
for feat, val in sorted_sims[:5]:
    meter_id = feat.split('_')[-1]
    correct = "✓ CORRECT" if int(meter_id) == y[sample_idx] else ""
    print(f"  Meter {meter_id}: {val:.3f} {correct}")
print()

# Check spread (difference between top and second)
top_sim = sorted_sims[0][1]
second_sim = sorted_sims[1][1]
spread = top_sim - second_sim
print(f"Spread (top - second): {spread:.3f}")
if spread < 0.1:
    print("❌ PROBLEM: Very small spread between top matches!")
    print("   Features aren't discriminative enough.")
print()
