#!/usr/bin/env python3
"""
BAHR ML Training - Week 3: Deep Hyperparameter Tuning

Strategy: GridSearchCV on RandomForest (best performer at 66.0%)
Target: 68-70% accuracy (match/exceed baseline)
Expected improvement: +2-4 pp

This will take 30-60 minutes depending on grid size.
"""

import sys
import numpy as np
import json
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.preprocessing import LabelEncoder
from datetime import datetime

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

    # Remap labels to 0-indexed
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    print(f"✅ Loaded {X.shape[0]} samples with {X.shape[1]} features")
    print(f"   Classes: {len(np.unique(y))} meters")

    return X, y_encoded, label_encoder

def run_grid_search(X, y, param_grid, cv_folds=5, n_jobs=-1):
    """Run GridSearchCV on RandomForest."""

    print("Parameter grid:")
    for param, values in param_grid.items():
        print(f"  {param}: {values}")

    # Calculate total combinations
    total_combinations = 1
    for values in param_grid.values():
        total_combinations *= len(values)

    total_fits = total_combinations * cv_folds
    print(f"\nTotal parameter combinations: {total_combinations}")
    print(f"Total model fits (with {cv_folds}-fold CV): {total_fits}")
    print(f"Estimated time: {total_fits * 2 / 60:.0f}-{total_fits * 4 / 60:.0f} minutes")
    print("\n🔄 Starting grid search... (this may take a while)\n")

    # Base model
    rf_base = RandomForestClassifier(random_state=42, n_jobs=1)  # n_jobs=1 for GridSearchCV

    # GridSearchCV
    grid_search = GridSearchCV(
        estimator=rf_base,
        param_grid=param_grid,
        cv=StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=42),
        scoring='accuracy',
        n_jobs=n_jobs,  # Parallelize across grid
        verbose=2,      # Show progress
        return_train_score=True
    )

    # Fit
    start_time = datetime.now()
    grid_search.fit(X, y)
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    print(f"\n✅ Grid search complete! ({duration:.0f} seconds)")

    return grid_search

def analyze_results(grid_search, baseline=0.682, target=0.70):
    """Analyze and display grid search results."""

    print_header("GRID SEARCH RESULTS")

    # Best parameters
    print("🏆 Best Parameters Found:")
    for param, value in grid_search.best_params_.items():
        print(f"   {param}: {value}")

    # Best score
    best_score = grid_search.best_score_
    best_std = grid_search.cv_results_['std_test_score'][grid_search.best_index_]

    print(f"\n📊 Best Cross-Validation Score:")
    print(f"   Accuracy: {best_score:.1%} ± {best_std:.1%}")

    # Comparison
    print(f"\n📈 Performance Comparison:")
    print(f"   Previous best (RF optimized):  66.0%")
    print(f"   Tuned model (GridSearch):      {best_score:.1%}")
    improvement = (best_score - 0.660) * 100
    print(f"   Improvement:                   +{improvement:.1f} pp")

    print(f"\n🎯 Target Comparison:")
    print(f"   Baseline (hybrid detector):    68.2%")
    print(f"   Week 2 Target (minimum):       70.0%")
    print(f"   Week 2 Goal:                   75.0%")

    gap_to_baseline = (baseline - best_score) * 100
    gap_to_target = (target - best_score) * 100

    if best_score >= target:
        print(f"\n✅ SUCCESS: Exceeded 70% target by {(best_score - target)*100:.1f} pp!")
        status = "TARGET_REACHED"
    elif best_score >= baseline:
        print(f"\n✅ EXCELLENT: Exceeded baseline by {(best_score - baseline)*100:.1f} pp!")
        print(f"   Gap to 70% target: {gap_to_target:.1f} pp")
        status = "ABOVE_BASELINE"
    elif best_score >= 0.67:
        print(f"\n⚡ VERY CLOSE: Only {gap_to_baseline:.1f} pp below baseline")
        print(f"   Gap to 70% target: {gap_to_target:.1f} pp")
        status = "CLOSE_TO_BASELINE"
    else:
        print(f"\n⚠️  GAP REMAINS:")
        print(f"   Gap to baseline: {gap_to_baseline:.1f} pp")
        print(f"   Gap to 70% target: {gap_to_target:.1f} pp")
        status = "BELOW_BASELINE"

    # Top 5 parameter combinations
    print("\n📋 Top 5 Parameter Combinations:")
    print("-" * 80)
    results = grid_search.cv_results_
    indices = np.argsort(results['mean_test_score'])[::-1][:5]

    for i, idx in enumerate(indices, 1):
        score = results['mean_test_score'][idx]
        std = results['std_test_score'][idx]
        params = results['params'][idx]

        print(f"\n{i}. Accuracy: {score:.1%} ± {std:.1%}")
        print(f"   Parameters: {params}")

    return best_score, status

def save_results(grid_search, best_score, status):
    """Save best model and results."""

    print_header("SAVING RESULTS")

    # Save best model
    best_model = grid_search.best_estimator_

    import pickle
    model_path = 'data/ml/best_rf_model.pkl'
    with open(model_path, 'wb') as f:
        pickle.dump(best_model, f)
    print(f"✅ Saved best model to: {model_path}")

    # Save hyperparameters
    params_path = 'data/ml/best_hyperparameters.json'
    with open(params_path, 'w') as f:
        json.dump({
            'best_params': grid_search.best_params_,
            'best_score': float(best_score),
            'status': status,
            'timestamp': datetime.now().isoformat()
        }, f, indent=2)
    print(f"✅ Saved hyperparameters to: {params_path}")

    # Save full results
    results_path = 'data/ml/grid_search_results.json'
    results = {
        'mean_test_score': grid_search.cv_results_['mean_test_score'].tolist(),
        'std_test_score': grid_search.cv_results_['std_test_score'].tolist(),
        'params': [str(p) for p in grid_search.cv_results_['params']],
        'rank_test_score': grid_search.cv_results_['rank_test_score'].tolist(),
    }
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"✅ Saved full grid search results to: {results_path}")

def main():
    print_header("BAHR ML - WEEK 3: HYPERPARAMETER TUNING")
    print("Model: RandomForest (best performer at 66.0%)")
    print("Method: GridSearchCV with 5-fold cross-validation")
    print("Target: 68-70% accuracy")

    # Load data
    X, y, label_encoder = load_training_data()

    print_header("PARAMETER GRID")

    # Strategy: Focused grid around optimal ranges
    # Based on RandomForest theory and initial results (66% with n_estimators=200, max_depth=15)

    param_grid = {
        # Number of trees: More trees = better, but diminishing returns after 300
        'n_estimators': [200, 300, 400],

        # Tree depth: 15 worked well, try nearby values
        'max_depth': [12, 15, 18, 20],

        # Min samples to split: Higher = more conservative, prevents overfitting
        'min_samples_split': [2, 5, 8],

        # Min samples per leaf: Higher = smoother decision boundaries
        'min_samples_leaf': [1, 2, 4],

        # Max features: 'sqrt' is standard, try variations
        'max_features': ['sqrt', 'log2', 0.3, 0.5],

        # Bootstrap: Should be True for Random Forest, but test
        'bootstrap': [True],

        # Class weight: Handle imbalanced classes
        'class_weight': [None, 'balanced', 'balanced_subsample']
    }

    # Run grid search
    grid_search = run_grid_search(X, y, param_grid, cv_folds=5, n_jobs=-1)

    # Analyze results
    best_score, status = analyze_results(grid_search)

    # Save results
    save_results(grid_search, best_score, status)

    print_header("NEXT STEPS")

    if status == "TARGET_REACHED":
        print("✅ 70% target reached! Next steps:")
        print("  1. Test on held-out validation set")
        print("  2. Analyze per-class performance")
        print("  3. If ≥75%: Proceed to Week 4 (production integration)")
        print("  4. If <75%: Consider data augmentation for final boost")
    elif status == "ABOVE_BASELINE":
        print("✅ Exceeded baseline! Next steps:")
        print("  1. Consider data augmentation to reach 70-75%")
        print("  2. Or proceed with current model (above baseline is success)")
    elif status == "CLOSE_TO_BASELINE":
        print("⚡ Very close! Next steps:")
        print("  1. Try one more round of fine-tuning around best params")
        print("  2. OR implement data augmentation (likely +3-5 pp)")
    else:
        print("⚠️  Gap remains. Next steps:")
        print("  1. Review feature engineering (may need more discriminative features)")
        print("  2. Implement data augmentation (critical)")
        print("  3. Consider collecting more training data")

    print_header("✅ HYPERPARAMETER TUNING COMPLETE")

    return status in ["TARGET_REACHED", "ABOVE_BASELINE"]

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
