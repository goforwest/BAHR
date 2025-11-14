#!/usr/bin/env python3
"""
BAHR ML Training - Week 2.5: Ensemble Models

Quick win strategy:
1. Ensemble voting classifier (RandomForest + XGBoost)
2. Quick hyperparameter tuning
3. Target: 68-71% accuracy

Expected improvement: +2-5 pp over best single model (64.4%)
"""

import sys
import numpy as np
import xgboost as xgb
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.pipeline import Pipeline

# Add backend to path
sys.path.insert(0, 'backend')

def print_header(text):
    """Print formatted section header."""
    print("\n" + "=" * 80)
    print(text)
    print("=" * 80 + "\n")

def load_training_data():
    """Load pre-extracted features."""
    print("Loading training data...")
    X = np.load('data/ml/X_train.npy')
    y = np.load('data/ml/y_train.npy')

    # Remap labels to 0-indexed for XGBoost compatibility
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    print(f"✅ Loaded {X.shape[0]} samples with {X.shape[1]} features")
    print(f"   Classes: {len(np.unique(y))} meters (IDs: {np.unique(y)})")

    return X, y_encoded, label_encoder

def evaluate_model(model, X, y, model_name, cv_folds=5):
    """Evaluate model with cross-validation."""
    print(f"\n{'='*60}")
    print(f"Evaluating: {model_name}")
    print(f"{'='*60}")

    # Stratified K-Fold for balanced evaluation
    cv = StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=42)

    # Cross-validation
    scores = cross_val_score(model, X, y, cv=cv, scoring='accuracy', n_jobs=-1)

    mean_acc = scores.mean()
    std_acc = scores.std()

    print(f"✅ {model_name}:")
    print(f"   Accuracy: {mean_acc:.1%} ± {std_acc:.1%}")
    print(f"   Fold scores: {[f'{s:.1%}' for s in scores]}")

    return mean_acc, std_acc

def main():
    print_header("BAHR ML - WEEK 2.5: ENSEMBLE MODELS")
    print("Strategy: Quick ensemble + tuning")
    print("Target: 68-71% accuracy (match/exceed 68.2% baseline)")

    # Load data
    X, y, label_encoder = load_training_data()

    print_header("STEP 1: Individual Models (Optimized)")

    # Optimized RandomForest (increased from default)
    print("\n1️⃣  RandomForest (optimized)")
    rf_model = RandomForestClassifier(
        n_estimators=200,      # Increased from 100
        max_depth=15,          # Limited to prevent overfitting
        min_samples_split=5,   # Require more samples to split
        min_samples_leaf=2,    # Require more samples per leaf
        max_features='sqrt',   # Standard for classification
        random_state=42,
        n_jobs=-1
    )
    rf_acc, rf_std = evaluate_model(rf_model, X, y, "RandomForest (optimized)")

    # Optimized XGBoost
    print("\n2️⃣  XGBoost (optimized)")
    xgb_model = xgb.XGBClassifier(
        n_estimators=200,      # Increased from 100
        max_depth=8,           # Deeper trees
        learning_rate=0.05,    # Lower learning rate for better generalization
        subsample=0.8,
        colsample_bytree=0.8,
        min_child_weight=3,    # Prevent overfitting
        gamma=0.1,             # Minimum loss reduction
        random_state=42,
        n_jobs=-1,
        eval_metric='mlogloss'
    )
    xgb_acc, xgb_std = evaluate_model(xgb_model, X, y, "XGBoost (optimized)")

    # Logistic Regression with scaling (for diversity)
    print("\n3️⃣  LogisticRegression (with scaling)")
    lr_pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('classifier', LogisticRegression(
            max_iter=2000,
            solver='lbfgs',
            C=0.5,  # Regularization
            random_state=42
        ))
    ])
    lr_acc, lr_std = evaluate_model(lr_pipeline, X, y, "LogisticRegression (scaled)")

    print_header("STEP 2: Ensemble Voting Classifier")

    # Strategy 1: RF + XGBoost (both strong performers)
    print("\n🔹 Ensemble 1: RandomForest + XGBoost")
    ensemble_rf_xgb = VotingClassifier(
        estimators=[
            ('rf', rf_model),
            ('xgb', xgb_model)
        ],
        voting='soft',  # Probability-based voting
        weights=[1.2, 1.0]  # RF slightly weighted (it performed better)
    )
    ens1_acc, ens1_std = evaluate_model(ensemble_rf_xgb, X, y, "Ensemble (RF + XGB)")

    # Strategy 2: All three models (diverse ensemble)
    print("\n🔹 Ensemble 2: RandomForest + XGBoost + LogisticRegression")
    ensemble_all = VotingClassifier(
        estimators=[
            ('rf', rf_model),
            ('xgb', xgb_model),
            ('lr', lr_pipeline)
        ],
        voting='soft',
        weights=[1.5, 1.0, 0.5]  # RF highest, LR lowest
    )
    ens2_acc, ens2_std = evaluate_model(ensemble_all, X, y, "Ensemble (All 3)")

    print_header("STEP 3: Results Summary")

    # Compare all models
    results = [
        ("RandomForest (optimized)", rf_acc, rf_std),
        ("XGBoost (optimized)", xgb_acc, xgb_std),
        ("LogisticRegression (scaled)", lr_acc, lr_std),
        ("Ensemble (RF + XGB)", ens1_acc, ens1_std),
        ("Ensemble (All 3)", ens2_acc, ens2_std),
    ]

    # Sort by accuracy
    results.sort(key=lambda x: x[1], reverse=True)

    print("Model Performance Comparison:")
    print("-" * 80)
    print(f"{'Model':<35} {'Accuracy':<20} {'Status':<20}")
    print("-" * 80)

    baseline = 0.682
    target_min = 0.70
    target_goal = 0.75

    for model_name, acc, std in results:
        status = ""
        if acc >= target_goal:
            status = "🎯 TARGET REACHED"
        elif acc >= baseline:
            status = "✅ Above Baseline"
        elif acc >= target_min - 0.02:
            status = "⚡ Close to Target"
        else:
            status = "⚠️  Below Target"

        acc_str = f"{acc:.1%} ± {std:.1%}"
        print(f"{model_name:<35} {acc_str:<20} {status}")

    print("-" * 80)
    print(f"Baseline (hybrid detector):       68.2%")
    print(f"Week 2 Target:                    70-75%")
    print(f"Week 2 Stretch Goal:              75-80%")
    print("-" * 80)

    # Best model
    best_model_name, best_acc, best_std = results[0]
    improvement = (best_acc - 0.644) * 100  # vs previous best (64.4%)

    print(f"\n🏆 Best Model: {best_model_name}")
    print(f"   Accuracy: {best_acc:.1%} ± {best_std:.1%}")
    print(f"   Improvement: +{improvement:.1f} pp over single RF")

    gap_to_baseline = (baseline - best_acc) * 100
    gap_to_target = (target_goal - best_acc) * 100

    if best_acc >= target_goal:
        print(f"\n✅ SUCCESS: Reached 75% target!")
        print("Next steps:")
        print("  1. Train final model on full dataset")
        print("  2. Save model for production")
        print("  3. Proceed to Week 3 (integration)")
    elif best_acc >= baseline:
        print(f"\n✅ GOOD PROGRESS: Exceeded baseline by {(best_acc - baseline)*100:.1f} pp")
        print(f"   Gap to 75% target: {gap_to_target:.1f} pp")
        print("\nNext steps:")
        print("  1. Deep hyperparameter tuning (GridSearchCV)")
        print("  2. Expected gain: +2-4 pp → 70-73%")
        print("  3. If needed: Data augmentation for final push to 75%")
    else:
        print(f"\n⚡ PROGRESS: Close to baseline")
        print(f"   Gap to baseline: {gap_to_baseline:.1f} pp")
        print(f"   Gap to 75% target: {gap_to_target:.1f} pp")
        print("\nNext steps:")
        print("  1. Deep hyperparameter tuning (critical)")
        print("  2. Feature engineering review")
        print("  3. Data augmentation")

    print_header("✅ ENSEMBLE EVALUATION COMPLETE")

    return best_acc >= baseline

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
