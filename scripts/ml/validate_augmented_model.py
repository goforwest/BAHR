#!/usr/bin/env python3
"""
Comprehensive validation of augmented model.

Validates:
1. Per-meter accuracy breakdown
2. Confusion matrix analysis
3. Comparison to baseline methods
4. Error analysis
"""

import sys
import json
from pathlib import Path
import numpy as np
import pandas as pd
import joblib
from collections import Counter, defaultdict
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

sys.path.insert(0, 'backend')

from app.ml.feature_extractor import BAHRFeatureExtractor
from app.core.prosody.detector_v2_hybrid import BahrDetectorV2Hybrid


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
    texts = []

    for verse in dataset:
        text = verse.get('text', '')
        meter = verse.get('meter', '')

        if not text or not meter:
            continue

        try:
            features = extractor.extract_features(text)
            X.append(features)
            y.append(meter)
            texts.append(text)
        except Exception:
            continue

    df = pd.DataFrame(X)
    return df, np.array(y), texts


def main():
    print("=" * 80)
    print("Comprehensive Validation of Augmented Model")
    print("=" * 80)
    print()

    # Load model
    model_path = 'models/rf_augmented_v1.joblib'
    if not Path(model_path).exists():
        print(f"❌ ERROR: Model not found at {model_path}")
        sys.exit(1)

    print(f"Loading model from: {model_path}")
    rf = joblib.load(model_path)
    print("✅ Model loaded")
    print()

    # Load original dataset
    original_path = 'dataset/evaluation/golden_set_v1_3_with_sari.jsonl'
    if not Path(original_path).exists():
        print(f"❌ ERROR: Original dataset not found at {original_path}")
        sys.exit(1)

    print(f"Loading original dataset from: {original_path}")
    original_verses = load_dataset(original_path)
    print(f"✅ Loaded {len(original_verses)} verses")
    print()

    # Extract features
    print("Extracting features...")
    extractor = BAHRFeatureExtractor()
    X, y_true, texts = extract_features_from_dataset(original_verses, extractor)
    print(f"✅ Extracted features from {len(X)} verses")
    print()

    # Predict
    print("Making predictions...")
    y_pred = rf.predict(X)
    y_pred_proba = rf.predict_proba(X)
    print("✅ Predictions complete")
    print()

    # Overall accuracy
    accuracy = accuracy_score(y_true, y_pred)
    print("=" * 80)
    print(f"Overall Accuracy: {accuracy:.1%}")
    print("=" * 80)
    print()

    # Per-meter accuracy
    print("=" * 80)
    print("Per-Meter Accuracy Breakdown")
    print("=" * 80)
    print()

    meter_results = defaultdict(lambda: {'correct': 0, 'total': 0})

    for true, pred in zip(y_true, y_pred):
        meter_results[true]['total'] += 1
        if true == pred:
            meter_results[true]['correct'] += 1

    # Sort by frequency
    sorted_meters = sorted(meter_results.items(), key=lambda x: -x[1]['total'])

    print(f"{'Rank':<6} {'Meter':<30} {'Correct':<10} {'Total':<10} {'Accuracy':<10}")
    print("-" * 80)

    for rank, (meter, stats) in enumerate(sorted_meters, 1):
        correct = stats['correct']
        total = stats['total']
        acc = 100 * correct / total if total > 0 else 0

        print(f"{rank:<6} {meter:<30} {correct:<10} {total:<10} {acc:>6.1f}%")

    print("-" * 80)
    print()

    # Identify problematic meters
    problematic_meters = [(m, s) for m, s in sorted_meters if (s['correct'] / s['total']) < 0.80]

    if problematic_meters:
        print("Meters with <80% accuracy:")
        for meter, stats in problematic_meters:
            acc = 100 * stats['correct'] / stats['total']
            print(f"  - {meter}: {acc:.1f}% ({stats['correct']}/{stats['total']})")
        print()
    else:
        print("✅ All meters have ≥80% accuracy!")
        print()

    # Compare to baseline detector
    print("=" * 80)
    print("Comparison to Baseline Hybrid Detector")
    print("=" * 80)
    print()

    detector = BahrDetectorV2Hybrid()

    baseline_correct = 0
    for verse, true_meter in zip(original_verses, y_true):
        text = verse.get('text', '')
        try:
            result = detector.detect(text)
            detected = result.get('meter', '')
            if detected == true_meter:
                baseline_correct += 1
        except Exception:
            pass

    baseline_accuracy = baseline_correct / len(y_true)

    print(f"Hybrid Detector Baseline: {baseline_accuracy:.1%}")
    print(f"RandomForest (Augmented): {accuracy:.1%}")
    print(f"Improvement: {accuracy - baseline_accuracy:+.1%}")
    print()

    # Error analysis
    print("=" * 80)
    print("Error Analysis - Top 10 Misclassifications")
    print("=" * 80)
    print()

    errors = []
    for i, (true, pred, text) in enumerate(zip(y_true, y_pred, texts)):
        if true != pred:
            # Get confidence
            true_idx = list(rf.classes_).index(true) if true in rf.classes_ else -1
            pred_idx = list(rf.classes_).index(pred)

            true_conf = y_pred_proba[i][true_idx] if true_idx >= 0 else 0.0
            pred_conf = y_pred_proba[i][pred_idx]

            errors.append({
                'text': text,
                'true_meter': true,
                'pred_meter': pred,
                'true_conf': true_conf,
                'pred_conf': pred_conf,
                'conf_diff': pred_conf - true_conf
            })

    # Sort by confidence difference (most confident errors first)
    errors.sort(key=lambda x: -x['conf_diff'])

    print(f"Total errors: {len(errors)}/{len(y_true)} ({100*len(errors)/len(y_true):.1f}%)")
    print()

    if errors:
        print("Top 10 most confident misclassifications:")
        print()

        for i, error in enumerate(errors[:10], 1):
            print(f"{i}. Text: {error['text'][:60]}...")
            print(f"   True meter: {error['true_meter']} (conf: {error['true_conf']:.2%})")
            print(f"   Predicted: {error['pred_meter']} (conf: {error['pred_conf']:.2%})")
            print(f"   Confidence diff: {error['conf_diff']:+.2%}")
            print()

    # Confusion matrix for top 5 meters
    print("=" * 80)
    print("Confusion Matrix (Top 5 Most Frequent Meters)")
    print("=" * 80)
    print()

    top_5_meters = [m for m, _ in sorted_meters[:5]]

    # Filter to only top 5 meters
    y_true_top5 = []
    y_pred_top5 = []
    for true, pred in zip(y_true, y_pred):
        if true in top_5_meters:
            y_true_top5.append(true)
            y_pred_top5.append(pred)

    cm = confusion_matrix(y_true_top5, y_pred_top5, labels=top_5_meters)

    # Print confusion matrix
    print(f"{'':20}", end='')
    for meter in top_5_meters:
        print(f"{meter[:15]:>15}", end='')
    print()
    print("-" * (20 + 15 * len(top_5_meters)))

    for i, true_meter in enumerate(top_5_meters):
        print(f"{true_meter[:20]:20}", end='')
        for j, pred_meter in enumerate(top_5_meters):
            count = cm[i][j]
            print(f"{count:>15}", end='')
        print()

    print()

    # Overall statistics
    print("=" * 80)
    print("Overall Statistics")
    print("=" * 80)
    print()

    print(f"Total verses: {len(y_true)}")
    print(f"Unique meters: {len(set(y_true))}")
    print(f"Correct predictions: {sum(y_true == y_pred)}")
    print(f"Incorrect predictions: {sum(y_true != y_pred)}")
    print(f"Overall accuracy: {accuracy:.1%}")
    print()

    # Confidence statistics
    max_confidences = np.max(y_pred_proba, axis=1)
    print(f"Average prediction confidence: {np.mean(max_confidences):.1%}")
    print(f"Median prediction confidence: {np.median(max_confidences):.1%}")
    print(f"Min prediction confidence: {np.min(max_confidences):.1%}")
    print(f"Max prediction confidence: {np.max(max_confidences):.1%}")
    print()

    # High confidence predictions
    high_conf_count = sum(max_confidences >= 0.9)
    print(f"High confidence predictions (≥90%): {high_conf_count}/{len(y_true)} ({100*high_conf_count/len(y_true):.1f}%)")

    # Accuracy on high confidence predictions
    high_conf_correct = sum((y_true == y_pred) & (max_confidences >= 0.9))
    high_conf_accuracy = high_conf_correct / high_conf_count if high_conf_count > 0 else 0
    print(f"Accuracy on high confidence: {high_conf_accuracy:.1%}")
    print()

    # Save detailed results
    results = {
        'overall_accuracy': float(accuracy),
        'baseline_accuracy': float(baseline_accuracy),
        'improvement': float(accuracy - baseline_accuracy),
        'total_verses': len(y_true),
        'unique_meters': len(set(y_true)),
        'errors': len(errors),
        'error_rate': float(len(errors) / len(y_true)),
        'avg_confidence': float(np.mean(max_confidences)),
        'high_confidence_count': int(high_conf_count),
        'high_confidence_accuracy': float(high_conf_accuracy),
        'per_meter_accuracy': {
            meter: {
                'correct': int(stats['correct']),
                'total': int(stats['total']),
                'accuracy': float(stats['correct'] / stats['total'])
            }
            for meter, stats in meter_results.items()
        }
    }

    results_path = 'validation_results.json'
    with open(results_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"✅ Detailed results saved to {results_path}")
    print()

    # Final summary
    print("=" * 80)
    print("VALIDATION SUMMARY")
    print("=" * 80)
    print(f"✅ Overall Accuracy: {accuracy:.1%}")
    print(f"✅ Baseline: {baseline_accuracy:.1%}")
    print(f"✅ Improvement: {accuracy - baseline_accuracy:+.1%}")
    print(f"✅ High Confidence Accuracy: {high_conf_accuracy:.1%}")
    print()

    if accuracy >= 0.90:
        print("🎉 EXCELLENT: Model achieves 90%+ accuracy!")
    elif accuracy >= 0.85:
        print("✅ VERY GOOD: Model achieves 85%+ accuracy!")
    elif accuracy >= 0.75:
        print("✅ GOOD: Model achieves 75%+ accuracy!")
    else:
        print("⚠️  Model accuracy below 75% target")

    print()


if __name__ == '__main__':
    main()
