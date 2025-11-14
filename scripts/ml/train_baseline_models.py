#!/usr/bin/env python3
"""
BAHR ML Training - Week 2: Baseline Models

Train and evaluate baseline ML models for Arabic meter detection:
1. Extract features from full golden dataset (471 verses)
2. Train 3 baseline models (LogisticRegression, RandomForest, XGBoost)
3. 5-fold cross-validation evaluation
4. Feature importance analysis

Target: 75-80% accuracy (beat current 68.2% hybrid detector)
"""

import sys
import json
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.model_selection import cross_val_score, cross_validate, train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.pipeline import Pipeline
import xgboost as xgb
from collections import Counter

sys.path.insert(0, 'backend')

from app.ml.feature_extractor import BAHRFeatureExtractor


# Meter name to ID mapping
METER_NAME_TO_ID = {
    'الطويل': 1,
    'الكامل': 2,
    'الوافر': 3,
    'الرمل': 4,
    'البسيط': 5,
    'المتقارب': 6,
    'الرجز': 7,
    'السريع': 8,
    'المديد': 9,
    'المنسرح': 10,
    'الهزج': 11,
    'الخفيف': 12,
    'المجتث': 13,
    'المقتضب': 14,
    'المضارع': 15,
    'المتدارك': 16,
}

METER_ID_TO_NAME = {v: k for k, v in METER_NAME_TO_ID.items()}


def load_golden_dataset(filepath: str):
    """Load golden dataset verses."""
    verses_with_meters = []

    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                verse_data = json.loads(line)
                text = verse_data.get('text', '')
                meter_name = verse_data.get('meter', '')
                meter_id = METER_NAME_TO_ID.get(meter_name)

                if text and meter_id:
                    verses_with_meters.append((text, meter_id))

    return verses_with_meters


def extract_full_dataset_features():
    """Extract features from full golden dataset."""
    print("=" * 80)
    print("STEP 1: Extracting Features from Golden Dataset")
    print("=" * 80)
    print()

    # Load golden dataset
    dataset_path = 'dataset/evaluation/golden_set_v1_3_with_sari.jsonl'
    print(f"Loading dataset: {dataset_path}")

    verses = load_golden_dataset(dataset_path)
    print(f"✅ Loaded {len(verses)} verses with meter labels")
    print()

    # Show meter distribution
    meter_counts = Counter(meter_id for _, meter_id in verses)
    print("Meter distribution:")
    for meter_id in sorted(meter_counts.keys()):
        meter_name = METER_ID_TO_NAME.get(meter_id, f'Unknown_{meter_id}')
        count = meter_counts[meter_id]
        print(f"  {meter_name} (ID {meter_id}): {count} verses")
    print()

    # Extract features
    print("Extracting features using BAHRFeatureExtractor...")
    extractor = BAHRFeatureExtractor()

    X, y = extractor.extract_batch(verses)

    print(f"✅ Feature extraction complete!")
    print(f"   Feature matrix shape: {X.shape}")
    print(f"   Target array shape: {y.shape}")
    print()

    # Show feature statistics
    print("Feature matrix statistics:")
    print(f"  Mean: {X.mean():.3f}")
    print(f"  Std: {X.std():.3f}")
    print(f"  Min: {X.min():.3f}")
    print(f"  Max: {X.max():.3f}")
    print()

    # Save to disk
    data_dir = Path('data/ml')
    data_dir.mkdir(parents=True, exist_ok=True)

    np.save(data_dir / 'X_train.npy', X)
    np.save(data_dir / 'y_train.npy', y)

    # Save feature names
    feature_names = extractor.get_feature_names()
    with open(data_dir / 'feature_names.json', 'w') as f:
        json.dump(feature_names, f, indent=2)

    print(f"✅ Saved training data to {data_dir}/")
    print(f"   - X_train.npy: {X.shape}")
    print(f"   - y_train.npy: {y.shape}")
    print(f"   - feature_names.json: {len(feature_names)} features")
    print()

    return X, y, feature_names


def train_baseline_models(X, y, feature_names):
    """Train and evaluate 3 baseline models."""
    print("=" * 80)
    print("STEP 2: Training Baseline Models")
    print("=" * 80)
    print()

    # Remap labels to 0-indexed for compatibility
    print("Remapping labels to 0-indexed...")
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    print(f"Original labels: {np.unique(y)}")
    print(f"Encoded labels: {np.unique(y_encoded)}")
    print()

    results = {}

    # 1. Logistic Regression (Simple Baseline) - WITH SCALING
    print("1️⃣  Logistic Regression (Simple Baseline)")
    print("-" * 80)

    lr_pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('classifier', LogisticRegression(
            max_iter=2000,
            solver='lbfgs',
            random_state=42
        ))
    ])

    print("Training with 5-fold cross-validation (with feature scaling)...")
    lr_cv_results = cross_validate(
        lr_pipeline, X, y_encoded,
        cv=5,
        scoring=['accuracy', 'f1_macro'],
        return_train_score=True,
        n_jobs=-1
    )

    lr_acc_mean = lr_cv_results['test_accuracy'].mean()
    lr_acc_std = lr_cv_results['test_accuracy'].std()
    lr_f1_mean = lr_cv_results['test_f1_macro'].mean()

    print(f"✅ Results:")
    print(f"   Accuracy: {lr_acc_mean:.1%} ± {lr_acc_std:.1%}")
    print(f"   F1-Score (macro): {lr_f1_mean:.1%}")
    print()

    results['LogisticRegression'] = {
        'accuracy_mean': lr_acc_mean,
        'accuracy_std': lr_acc_std,
        'f1_macro': lr_f1_mean,
        'cv_results': lr_cv_results
    }

    # 2. Random Forest (Ensemble Baseline)
    print("2️⃣  Random Forest (Ensemble Baseline)")
    print("-" * 80)

    rf = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )

    print("Training with 5-fold cross-validation...")
    rf_cv_results = cross_validate(
        rf, X, y_encoded,
        cv=5,
        scoring=['accuracy', 'f1_macro'],
        return_train_score=True,
        n_jobs=-1
    )

    rf_acc_mean = rf_cv_results['test_accuracy'].mean()
    rf_acc_std = rf_cv_results['test_accuracy'].std()
    rf_f1_mean = rf_cv_results['test_f1_macro'].mean()

    print(f"✅ Results:")
    print(f"   Accuracy: {rf_acc_mean:.1%} ± {rf_acc_std:.1%}")
    print(f"   F1-Score (macro): {rf_f1_mean:.1%}")
    print()

    results['RandomForest'] = {
        'accuracy_mean': rf_acc_mean,
        'accuracy_std': rf_acc_std,
        'f1_macro': rf_f1_mean,
        'cv_results': rf_cv_results
    }

    # 3. XGBoost (Gradient Boosting - Best Expected)
    print("3️⃣  XGBoost (Gradient Boosting)")
    print("-" * 80)

    xgb_model = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=6,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        n_jobs=-1,
        eval_metric='mlogloss'
    )

    print("Training with 5-fold cross-validation...")
    xgb_cv_results = cross_validate(
        xgb_model, X, y_encoded,
        cv=5,
        scoring=['accuracy', 'f1_macro'],
        return_train_score=True,
        n_jobs=-1
    )

    xgb_acc_mean = xgb_cv_results['test_accuracy'].mean()
    xgb_acc_std = xgb_cv_results['test_accuracy'].std()
    xgb_f1_mean = xgb_cv_results['test_f1_macro'].mean()

    print(f"✅ Results:")
    print(f"   Accuracy: {xgb_acc_mean:.1%} ± {xgb_acc_std:.1%}")
    print(f"   F1-Score (macro): {xgb_f1_mean:.1%}")
    print()

    results['XGBoost'] = {
        'accuracy_mean': xgb_acc_mean,
        'accuracy_std': xgb_acc_std,
        'f1_macro': xgb_f1_mean,
        'cv_results': xgb_cv_results
    }

    return results


def analyze_feature_importance(X, y, feature_names):
    """Analyze feature importance using XGBoost."""
    print("=" * 80)
    print("STEP 3: Feature Importance Analysis")
    print("=" * 80)
    print()

    # Encode labels for XGBoost
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    xgb_model = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=6,
        learning_rate=0.1,
        random_state=42
    )

    print("Training XGBoost on full dataset...")
    xgb_model.fit(X, y_encoded)
    print("✅ Training complete!")
    print()

    # Get feature importance
    importance = xgb_model.feature_importances_

    # Create dataframe
    importance_df = pd.DataFrame({
        'feature': feature_names,
        'importance': importance
    }).sort_values('importance', ascending=False)

    # Show top 15 features
    print("Top 15 Most Important Features:")
    print("-" * 80)
    for i, row in importance_df.head(15).iterrows():
        print(f"{row['feature']:40s} {row['importance']:.4f}")
    print()

    # Save to CSV
    data_dir = Path('data/ml')
    importance_df.to_csv(data_dir / 'feature_importance.csv', index=False)
    print(f"✅ Saved feature importance to {data_dir}/feature_importance.csv")
    print()

    return importance_df


def compare_results(results):
    """Compare all model results."""
    print("=" * 80)
    print("STEP 4: Model Comparison")
    print("=" * 80)
    print()

    print("Model Performance Summary:")
    print("-" * 80)
    print(f"{'Model':<20} {'Accuracy':<15} {'F1-Score':<15} {'Status':<15}")
    print("-" * 80)

    baseline_accuracy = 0.682  # Current hybrid detector: 68.2%

    for model_name, result in results.items():
        acc_mean = result['accuracy_mean']
        acc_std = result['accuracy_std']
        f1_mean = result['f1_macro']

        # Determine status
        if acc_mean > 0.80:
            status = "🎯 Excellent"
        elif acc_mean > baseline_accuracy:
            status = "✅ Beat Baseline"
        else:
            status = "⚠️  Below Baseline"

        print(f"{model_name:<20} {acc_mean:.1%} ± {acc_std:.1%}   {f1_mean:.1%}           {status}")

    print("-" * 80)
    print(f"Baseline (hybrid):   {baseline_accuracy:.1%}            (current)")
    print()

    # Find best model
    best_model = max(results.items(), key=lambda x: x[1]['accuracy_mean'])
    best_name = best_model[0]
    best_acc = best_model[1]['accuracy_mean']

    print(f"🏆 Best Model: {best_name} ({best_acc:.1%})")
    print(f"   Improvement over baseline: {(best_acc - baseline_accuracy)*100:+.1f} pp")
    print()

    # Week 2 success criteria
    print("Week 2 Success Criteria:")
    if best_acc >= 0.80:
        print("   ✅ EXCELLENT: ≥80% accuracy achieved!")
        print("   → Ready for Week 3 (hyperparameter tuning)")
    elif best_acc >= 0.75:
        print("   ✅ TARGET MET: 75-80% accuracy achieved!")
        print("   → On track for 80-85% final target")
    elif best_acc >= 0.70:
        print("   ⚠️  ACCEPTABLE: 70-75% accuracy")
        print("   → Consider data augmentation before Week 3")
    else:
        print("   ❌ BELOW TARGET: <70% accuracy")
        print("   → Need feature engineering or data augmentation")
    print()


def main():
    """Run full Week 2 training pipeline."""
    print("=" * 80)
    print("BAHR ML TRAINING - WEEK 2: BASELINE MODELS")
    print("=" * 80)
    print()
    print("Target: 75-80% accuracy (beat current 68.2% hybrid detector)")
    print()

    try:
        # Step 1: Extract features
        X, y, feature_names = extract_full_dataset_features()

        # Step 2: Train models
        results = train_baseline_models(X, y, feature_names)

        # Step 3: Feature importance
        importance_df = analyze_feature_importance(X, y, feature_names)

        # Step 4: Compare results
        compare_results(results)

        print("=" * 80)
        print("✅ WEEK 2 TRAINING COMPLETE!")
        print("=" * 80)
        print()
        print("Next steps:")
        print("1. Review results above")
        print("2. If ≥75% accuracy: Proceed to Week 3 (hyperparameter tuning)")
        print("3. If 70-75%: Consider data augmentation")
        print("4. Check feature_importance.csv for insights")
        print()

        return 0

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
