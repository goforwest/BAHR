#!/usr/bin/env python3
"""
Train RandomForest on augmented dataset and validate.

Expected result: 73-76% accuracy (up from 66%)
"""

import sys
import json
from pathlib import Path
import numpy as np
import pandas as pd
from collections import Counter
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import accuracy_score, classification_report

sys.path.insert(0, 'backend')

from app.ml.feature_extractor import BAHRFeatureExtractor


def load_dataset(filepath):
    """Load dataset from JSONL."""
    verses = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                verses.append(json.loads(line))
    return verses


def extract_features_from_dataset(dataset, extractor):
    """Extract features from all verses."""
    X = []
    y = []

    print(f"Extracting features from {len(dataset)} verses...")

    for i, verse in enumerate(dataset, 1):
        text = verse.get('text', '')
        meter = verse.get('meter', '')

        if not text or not meter:
            continue

        try:
            features = extractor.extract_features(text)
            X.append(features)
            y.append(meter)

            if i % 100 == 0:
                print(f"  Processed {i}/{len(dataset)} verses...")

        except Exception as e:
            print(f"  ⚠️  Error extracting features from verse {i}: {e}")
            continue

    print(f"✅ Extracted features from {len(X)} verses")

    # Convert to DataFrame
    df = pd.DataFrame(X)

    return df, np.array(y)


def main():
    print("=" * 80)
    print("Training on Augmented Dataset")
    print("=" * 80)
    print()

    # Load augmented dataset
    augmented_path = 'dataset/augmented_golden_set.jsonl'
    if not Path(augmented_path).exists():
        print(f"❌ ERROR: Augmented dataset not found at {augmented_path}")
        print("   Run run_full_augmentation.py first!")
        sys.exit(1)

    print(f"Loading augmented dataset from: {augmented_path}")
    augmented_verses = load_dataset(augmented_path)
    print(f"✅ Loaded {len(augmented_verses)} verses")
    print()

    # Extract features
    print("=" * 80)
    print("Feature Extraction")
    print("=" * 80)
    print()

    extractor = BAHRFeatureExtractor()
    X, y = extract_features_from_dataset(augmented_verses, extractor)

    print()
    print(f"Feature matrix shape: {X.shape}")
    print(f"Target vector shape: {y.shape}")
    print()

    # Show class distribution
    print("Class distribution:")
    meter_counts = Counter(y)
    for meter, count in sorted(meter_counts.items(), key=lambda x: -x[1])[:10]:
        print(f"  {meter}: {count}")
    print(f"  ... ({len(meter_counts)} meters total)")
    print()

    # Split into train/test (80/20) - stratified by meter
    print("=" * 80)
    print("Train/Test Split")
    print("=" * 80)
    print()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print(f"Training set: {len(X_train)} verses")
    print(f"Test set: {len(X_test)} verses")
    print()

    # Train optimized RandomForest
    # (Use best hyperparameters from GridSearchCV if available)
    print("=" * 80)
    print("Training RandomForest")
    print("=" * 80)
    print()

    # Check if GridSearchCV results exist
    gridsearch_results_path = 'gridsearch_results.json'
    if Path(gridsearch_results_path).exists():
        print("✅ Found GridSearchCV results, loading best parameters...")
        with open(gridsearch_results_path, 'r') as f:
            gridsearch_results = json.load(f)
        best_params = gridsearch_results.get('best_params', {})
        print(f"Best parameters: {best_params}")
        print()

        rf = RandomForestClassifier(**best_params, random_state=42, n_jobs=-1)
    else:
        print("⚠️  No GridSearchCV results found, using optimized defaults...")
        rf = RandomForestClassifier(
            n_estimators=200,
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            max_features='sqrt',
            class_weight='balanced',
            random_state=42,
            n_jobs=-1
        )

    print("Training model...")
    rf.fit(X_train, y_train)
    print("✅ Training complete!")
    print()

    # Evaluate on test set
    print("=" * 80)
    print("Test Set Evaluation")
    print("=" * 80)
    print()

    y_pred = rf.predict(X_test)
    test_accuracy = accuracy_score(y_test, y_pred)

    print(f"Test Accuracy: {test_accuracy:.1%}")
    print()

    # Cross-validation on full augmented dataset
    print("=" * 80)
    print("5-Fold Cross-Validation on Augmented Dataset")
    print("=" * 80)
    print()

    cv_scores = cross_val_score(rf, X, y, cv=5, scoring='accuracy', n_jobs=-1)

    print("Cross-validation scores:")
    for i, score in enumerate(cv_scores, 1):
        print(f"  Fold {i}: {score:.1%}")

    print()
    print(f"Mean CV Accuracy: {cv_scores.mean():.1%} ± {cv_scores.std():.1%}")
    print()

    # Validate on ORIGINAL (non-augmented) dataset
    print("=" * 80)
    print("Validation on Original Dataset")
    print("=" * 80)
    print()

    original_path = 'dataset/evaluation/golden_set_v1_3_with_sari.jsonl'
    if Path(original_path).exists():
        print(f"Loading original dataset from: {original_path}")
        original_verses = load_dataset(original_path)
        print(f"✅ Loaded {len(original_verses)} original verses")
        print()

        # Extract features from original dataset
        X_orig, y_orig = extract_features_from_dataset(original_verses, extractor)

        # Predict on original dataset
        y_orig_pred = rf.predict(X_orig)
        original_accuracy = accuracy_score(y_orig, y_orig_pred)

        print(f"Original Dataset Accuracy: {original_accuracy:.1%}")
        print()

        # Compare to baseline
        print("Comparison to Baseline:")
        print("-" * 80)
        print(f"Hybrid Detector Baseline: 68.2%")
        print(f"RandomForest (non-augmented): 66.0%")
        print(f"RandomForest (augmented): {original_accuracy:.1%}")
        print()

        improvement = original_accuracy - 0.660
        print(f"Improvement from augmentation: {improvement:+.1%}")
        print()

        if original_accuracy >= 0.73:
            print("✅ SUCCESS: Reached 73%+ target!")
        elif original_accuracy >= 0.70:
            print("⚠️  GOOD: Significant improvement, close to target")
        else:
            print("⚠️  MODERATE: Some improvement, but below 70% target")

    else:
        print(f"⚠️  Original dataset not found at {original_path}")
        print("   Skipping original dataset validation")

    print()

    # Feature importance analysis
    print("=" * 80)
    print("Top 20 Most Important Features")
    print("=" * 80)
    print()

    feature_importances = pd.DataFrame({
        'feature': X.columns,
        'importance': rf.feature_importances_
    }).sort_values('importance', ascending=False)

    print(feature_importances.head(20).to_string(index=False))
    print()

    # Save model
    print("=" * 80)
    print("Saving Model")
    print("=" * 80)
    print()

    import joblib
    model_path = 'models/rf_augmented_v1.joblib'
    Path('models').mkdir(exist_ok=True)
    joblib.dump(rf, model_path)
    print(f"✅ Model saved to {model_path}")
    print()

    # Save results summary
    results = {
        'augmented_dataset_size': len(augmented_verses),
        'original_dataset_size': len(original_verses) if Path(original_path).exists() else None,
        'test_accuracy': float(test_accuracy),
        'cv_mean': float(cv_scores.mean()),
        'cv_std': float(cv_scores.std()),
        'original_accuracy': float(original_accuracy) if Path(original_path).exists() else None,
        'baseline_hybrid': 0.682,
        'baseline_rf': 0.660,
        'improvement': float(improvement) if Path(original_path).exists() else None,
        'feature_count': X.shape[1],
        'model_path': model_path
    }

    results_path = 'augmented_training_results.json'
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"✅ Results saved to {results_path}")
    print()

    # Final summary
    print("=" * 80)
    print("TRAINING SUMMARY")
    print("=" * 80)
    print(f"✅ Dataset: {len(original_verses)} → {len(augmented_verses)} verses (1.85x)")
    print(f"✅ Features: {X.shape[1]} features per verse")
    print(f"✅ Test Accuracy: {test_accuracy:.1%}")
    print(f"✅ CV Accuracy: {cv_scores.mean():.1%} ± {cv_scores.std():.1%}")
    if Path(original_path).exists():
        print(f"✅ Original Dataset Accuracy: {original_accuracy:.1%}")
        print(f"✅ Improvement: {improvement:+.1%} from non-augmented baseline")
    print()

    if Path(original_path).exists() and original_accuracy >= 0.73:
        print("🎉 TARGET ACHIEVED: 73%+ accuracy on original dataset!")
    elif Path(original_path).exists() and original_accuracy >= 0.70:
        print("🎯 CLOSE TO TARGET: 70%+ accuracy achieved!")
    else:
        print("📊 Results available - see analysis above for next steps")

    print()


if __name__ == '__main__':
    main()
