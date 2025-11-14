#!/usr/bin/env python3
"""
BAHR ML Pipeline - Phase 5.2: Hyperparameter Optimization

Implements grid search with cross-validation for:
1. RandomForest
2. XGBoost
3. LightGBM

Saves best hyperparameters for ensemble training.

Usage:
    python ml_pipeline/hyperparameter_search.py --features data/ml/X_train.npy \
                                                 --targets data/ml/y_train.npy \
                                                 --output ml_pipeline/results/best_params.json
"""

import sys
import json
import argparse
import numpy as np
import time
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.metrics import accuracy_score, make_scorer
import xgboost as xgb
import lightgbm as lgb


class HyperparameterOptimizer:
    """
    Optimize hyperparameters for multiple classifiers.
    
    Uses GridSearchCV with 5-fold stratified cross-validation.
    """
    
    def __init__(self, random_state=42, cv=5, n_jobs=-1):
        self.random_state = random_state
        self.cv = StratifiedKFold(n_splits=cv, shuffle=True, random_state=random_state)
        self.n_jobs = n_jobs
        self.results = {}
        
    def load_data(self, X_path, y_path, feature_indices_path=None):
        """
        Load training data and optionally apply feature selection.
        
        Args:
            X_path: Path to feature matrix
            y_path: Path to target labels
            feature_indices_path: Optional path to selected feature indices
        """
        print(f"Loading data from {X_path} and {y_path}")
        self.X = np.load(X_path)
        self.y = np.load(y_path)
        
        # Apply feature selection if provided
        if feature_indices_path and Path(feature_indices_path).exists():
            print(f"Applying feature selection from {feature_indices_path}")
            feature_indices = np.load(feature_indices_path)
            self.X = self.X[:, feature_indices]
            print(f"✅ Reduced features: {self.X.shape[1]} features selected")
        
        print(f"✅ Loaded: X shape={self.X.shape}, y shape={self.y.shape}")
        print(f"   Classes: {np.unique(self.y)}")
        print(f"   Class distribution: {np.bincount(self.y.astype(int))}")
        
    def optimize_random_forest(self):
        """
        Grid search for RandomForest hyperparameters.
        
        Parameter grid:
        - n_estimators: Number of trees
        - max_depth: Maximum tree depth
        - min_samples_split: Minimum samples to split node
        - min_samples_leaf: Minimum samples in leaf
        - max_features: Features to consider for split
        """
        print("\n" + "="*80)
        print("Optimizing RandomForest Hyperparameters")
        print("="*80)
        
        param_grid = {
            'n_estimators': [100, 200, 300, 500],
            'max_depth': [10, 20, 30, None],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4],
            'max_features': ['sqrt', 'log2', None],
            'class_weight': ['balanced', None]
        }
        
        print(f"\nParameter grid:")
        for param, values in param_grid.items():
            print(f"  {param}: {values}")
        
        total_combinations = np.prod([len(v) for v in param_grid.values()])
        print(f"\nTotal combinations: {total_combinations}")
        print(f"Total CV fits: {total_combinations * self.cv.n_splits}")
        
        rf = RandomForestClassifier(random_state=self.random_state, n_jobs=1)
        
        grid_search = GridSearchCV(
            estimator=rf,
            param_grid=param_grid,
            cv=self.cv,
            scoring='accuracy',
            n_jobs=self.n_jobs,
            verbose=2,
            return_train_score=True
        )
        
        start_time = time.time()
        print("\nStarting grid search...")
        grid_search.fit(self.X, self.y)
        elapsed = time.time() - start_time
        
        print(f"\n✅ Grid search complete in {elapsed:.1f}s")
        print(f"\nBest parameters:")
        for param, value in grid_search.best_params_.items():
            print(f"  {param}: {value}")
        print(f"\nBest CV accuracy: {grid_search.best_score_:.4f}")
        
        # Get top 5 configurations
        results_df = pd.DataFrame(grid_search.cv_results_)
        results_df = results_df.sort_values('rank_test_score')
        
        print("\nTop 5 configurations:")
        for i, row in results_df.head(5).iterrows():
            print(f"  {int(row['rank_test_score'])}. Accuracy: {row['mean_test_score']:.4f} ± {row['std_test_score']:.4f}")
            print(f"     Params: {row['params']}")
        
        self.results['random_forest'] = {
            'best_params': grid_search.best_params_,
            'best_score': float(grid_search.best_score_),
            'best_score_std': float(results_df.iloc[0]['std_test_score']),
            'search_time_seconds': float(elapsed),
            'total_fits': int(total_combinations * self.cv.n_splits)
        }
        
        self.rf_best_estimator = grid_search.best_estimator_
        
    def optimize_xgboost(self):
        """
        Grid search for XGBoost hyperparameters.
        
        Parameter grid:
        - n_estimators: Number of boosting rounds
        - max_depth: Maximum tree depth
        - learning_rate: Step size shrinkage
        - subsample: Subsample ratio
        - colsample_bytree: Feature sampling ratio
        """
        print("\n" + "="*80)
        print("Optimizing XGBoost Hyperparameters")
        print("="*80)
        
        param_grid = {
            'n_estimators': [100, 200, 300],
            'max_depth': [3, 5, 7, 10],
            'learning_rate': [0.01, 0.05, 0.1, 0.2],
            'subsample': [0.7, 0.8, 0.9, 1.0],
            'colsample_bytree': [0.7, 0.8, 0.9, 1.0],
            'min_child_weight': [1, 3, 5],
            'gamma': [0, 0.1, 0.2]
        }
        
        print(f"\nParameter grid:")
        for param, values in param_grid.items():
            print(f"  {param}: {values}")
        
        total_combinations = np.prod([len(v) for v in param_grid.values()])
        print(f"\nTotal combinations: {total_combinations}")
        print(f"⚠️  This will take significant time. Consider reducing grid size.")
        
        # Remap labels to 0-indexed for XGBoost
        y_remapped = self.y - 1  # Assuming labels are 1-16
        
        xgb_clf = xgb.XGBClassifier(
            objective='multi:softmax',
            num_class=len(np.unique(y_remapped)),
            random_state=self.random_state,
            tree_method='hist',
            eval_metric='mlogloss'
        )
        
        grid_search = GridSearchCV(
            estimator=xgb_clf,
            param_grid=param_grid,
            cv=self.cv,
            scoring='accuracy',
            n_jobs=self.n_jobs,
            verbose=2,
            return_train_score=True
        )
        
        start_time = time.time()
        print("\nStarting grid search...")
        grid_search.fit(self.X, y_remapped)
        elapsed = time.time() - start_time
        
        print(f"\n✅ Grid search complete in {elapsed:.1f}s")
        print(f"\nBest parameters:")
        for param, value in grid_search.best_params_.items():
            print(f"  {param}: {value}")
        print(f"\nBest CV accuracy: {grid_search.best_score_:.4f}")
        
        self.results['xgboost'] = {
            'best_params': grid_search.best_params_,
            'best_score': float(grid_search.best_score_),
            'search_time_seconds': float(elapsed)
        }
        
        self.xgb_best_estimator = grid_search.best_estimator_
        
    def optimize_lightgbm(self):
        """
        Grid search for LightGBM hyperparameters.
        
        Parameter grid:
        - n_estimators: Number of boosting rounds
        - max_depth: Maximum tree depth
        - learning_rate: Learning rate
        - num_leaves: Maximum leaves per tree
        - subsample: Data sampling ratio
        """
        print("\n" + "="*80)
        print("Optimizing LightGBM Hyperparameters")
        print("="*80)
        
        param_grid = {
            'n_estimators': [100, 200, 300],
            'max_depth': [5, 10, 15, -1],
            'learning_rate': [0.01, 0.05, 0.1],
            'num_leaves': [31, 50, 70, 100],
            'subsample': [0.7, 0.8, 0.9],
            'colsample_bytree': [0.7, 0.8, 0.9],
            'min_child_samples': [10, 20, 30]
        }
        
        print(f"\nParameter grid:")
        for param, values in param_grid.items():
            print(f"  {param}: {values}")
        
        total_combinations = np.prod([len(v) for v in param_grid.values()])
        print(f"\nTotal combinations: {total_combinations}")
        
        # Remap labels
        y_remapped = self.y - 1
        
        lgb_clf = lgb.LGBMClassifier(
            objective='multiclass',
            num_class=len(np.unique(y_remapped)),
            random_state=self.random_state,
            verbose=-1
        )
        
        grid_search = GridSearchCV(
            estimator=lgb_clf,
            param_grid=param_grid,
            cv=self.cv,
            scoring='accuracy',
            n_jobs=self.n_jobs,
            verbose=2,
            return_train_score=True
        )
        
        start_time = time.time()
        print("\nStarting grid search...")
        grid_search.fit(self.X, y_remapped)
        elapsed = time.time() - start_time
        
        print(f"\n✅ Grid search complete in {elapsed:.1f}s")
        print(f"\nBest parameters:")
        for param, value in grid_search.best_params_.items():
            print(f"  {param}: {value}")
        print(f"\nBest CV accuracy: {grid_search.best_score_:.4f}")
        
        self.results['lightgbm'] = {
            'best_params': grid_search.best_params_,
            'best_score': float(grid_search.best_score_),
            'search_time_seconds': float(elapsed)
        }
        
        self.lgb_best_estimator = grid_search.best_estimator_
        
    def save_results(self, output_path):
        """Save optimized hyperparameters to JSON."""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n✅ Saved hyperparameter results to {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description='Hyperparameter optimization for BAHR classifiers'
    )
    parser.add_argument('--features', default='data/ml/X_train.npy',
                       help='Path to feature matrix')
    parser.add_argument('--targets', default='data/ml/y_train.npy',
                       help='Path to target labels')
    parser.add_argument('--feature-indices', 
                       default='ml_pipeline/results/optimized_feature_indices.npy',
                       help='Path to optimized feature indices (optional)')
    parser.add_argument('--output', default='ml_pipeline/results/best_params.json',
                       help='Output path for best parameters')
    parser.add_argument('--models', nargs='+', 
                       choices=['rf', 'xgb', 'lgb', 'all'],
                       default=['all'],
                       help='Models to optimize (default: all)')
    
    args = parser.parse_args()
    
    print("="*80)
    print("BAHR Hyperparameter Optimization Pipeline")
    print("="*80)
    
    optimizer = HyperparameterOptimizer()
    
    # Load data
    optimizer.load_data(args.features, args.targets, args.feature_indices)
    
    # Run optimization for selected models
    models_to_run = args.models
    if 'all' in models_to_run:
        models_to_run = ['rf', 'xgb', 'lgb']
    
    if 'rf' in models_to_run:
        optimizer.optimize_random_forest()
    
    if 'xgb' in models_to_run:
        optimizer.optimize_xgboost()
    
    if 'lgb' in models_to_run:
        optimizer.optimize_lightgbm()
    
    # Save results
    optimizer.save_results(args.output)
    
    print("\n" + "="*80)
    print("✅ Hyperparameter optimization complete!")
    print("="*80)
    print(f"\nBest parameters saved to: {args.output}")
    print("\nNext steps:")
    print("  1. Review best hyperparameters")
    print("  2. Train ensemble model with optimized parameters")


if __name__ == '__main__':
    # Import pandas here to avoid loading it if not needed
    import pandas as pd
    main()
