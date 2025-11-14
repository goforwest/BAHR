#!/usr/bin/env python3
"""
BAHR ML Pipeline - Phase 5.3: Ensemble Model Training

Trains weighted voting ensemble combining:
1. RandomForest (optimized)
2. XGBoost (optimized)
3. LightGBM (optimized)

Implements 5-fold cross-validation and model serialization.

Usage:
    python ml_pipeline/ensemble_trainer.py --features data/ml/X_train.npy \
                                           --targets data/ml/y_train.npy \
                                           --params ml_pipeline/results/best_params.json \
                                           --output models/ensemble_v1
"""

import sys
import json
import argparse
import pickle
import numpy as np
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

sys.path.insert(0, 'backend')


class EnsembleTrainer:
    """
    Train and evaluate ensemble of optimized classifiers.
    
    Combines multiple models using weighted voting based on
    individual CV performance.
    """
    
    def __init__(self, random_state=42):
        self.random_state = random_state
        self.models = {}
        self.ensemble = None
        
    def load_data(self, X_path, y_path, feature_indices_path=None):
        """Load training data with optional feature selection."""
        print(f"Loading data from {X_path} and {y_path}")
        self.X = np.load(X_path)
        self.y = np.load(y_path)
        
        if feature_indices_path and Path(feature_indices_path).exists():
            print(f"Applying feature selection from {feature_indices_path}")
            feature_indices = np.load(feature_indices_path)
            self.X = self.X[:, feature_indices]
            print(f"✅ Reduced to {self.X.shape[1]} features")
        
        print(f"✅ Loaded: X shape={self.X.shape}, y shape={self.y.shape}")
        
    def load_hyperparameters(self, params_path):
        """Load optimized hyperparameters from JSON."""
        with open(params_path, 'r') as f:
            self.best_params = json.load(f)
        
        print(f"✅ Loaded hyperparameters from {params_path}")
        
    def train_random_forest(self):
        """Train RandomForest with optimized hyperparameters."""
        print("\n" + "="*80)
        print("Training RandomForest")
        print("="*80)
        
        params = self.best_params.get('random_forest', {}).get('best_params', {})
        print(f"Using parameters: {params}")
        
        rf = RandomForestClassifier(
            random_state=self.random_state,
            n_jobs=-1,
            **params
        )
        
        # Cross-validation
        cv_results = cross_validate(
            rf, self.X, self.y,
            cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=self.random_state),
            scoring=['accuracy', 'precision_macro', 'recall_macro', 'f1_macro'],
            return_train_score=True,
            n_jobs=-1,
            verbose=1
        )
        
        print(f"\nCross-Validation Results:")
        print(f"  Accuracy: {cv_results['test_accuracy'].mean():.4f} ± {cv_results['test_accuracy'].std():.4f}")
        print(f"  Precision: {cv_results['test_precision_macro'].mean():.4f} ± {cv_results['test_precision_macro'].std():.4f}")
        print(f"  Recall: {cv_results['test_recall_macro'].mean():.4f} ± {cv_results['test_recall_macro'].std():.4f}")
        print(f"  F1: {cv_results['test_f1_macro'].mean():.4f} ± {cv_results['test_f1_macro'].std():.4f}")
        
        # Train on full dataset
        print("\nTraining on full dataset...")
        rf.fit(self.X, self.y)
        
        self.models['random_forest'] = {
            'estimator': rf,
            'cv_accuracy': float(cv_results['test_accuracy'].mean()),
            'cv_std': float(cv_results['test_accuracy'].std())
        }
        
        print("✅ RandomForest training complete")
        
    def train_xgboost(self):
        """Train XGBoost with optimized hyperparameters."""
        print("\n" + "="*80)
        print("Training XGBoost")
        print("="*80)
        
        try:
            import xgboost as xgb
        except ImportError:
            print("⚠️  XGBoost not installed. Skipping.")
            return
        
        params = self.best_params.get('xgboost', {}).get('best_params', {})
        print(f"Using parameters: {params}")
        
        # Remap labels to 0-indexed
        y_remapped = self.y - 1
        
        xgb_clf = xgb.XGBClassifier(
            objective='multi:softmax',
            num_class=len(np.unique(y_remapped)),
            random_state=self.random_state,
            tree_method='hist',
            eval_metric='mlogloss',
            **params
        )
        
        # Cross-validation
        cv_results = cross_validate(
            xgb_clf, self.X, y_remapped,
            cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=self.random_state),
            scoring=['accuracy', 'precision_macro', 'recall_macro', 'f1_macro'],
            return_train_score=True,
            n_jobs=-1,
            verbose=1
        )
        
        print(f"\nCross-Validation Results:")
        print(f"  Accuracy: {cv_results['test_accuracy'].mean():.4f} ± {cv_results['test_accuracy'].std():.4f}")
        
        # Train on full dataset
        print("\nTraining on full dataset...")
        xgb_clf.fit(self.X, y_remapped)
        
        self.models['xgboost'] = {
            'estimator': xgb_clf,
            'cv_accuracy': float(cv_results['test_accuracy'].mean()),
            'cv_std': float(cv_results['test_accuracy'].std()),
            'label_offset': 1  # Remember to add 1 back to predictions
        }
        
        print("✅ XGBoost training complete")
        
    def train_lightgbm(self):
        """Train LightGBM with optimized hyperparameters."""
        print("\n" + "="*80)
        print("Training LightGBM")
        print("="*80)
        
        try:
            import lightgbm as lgb
        except ImportError:
            print("⚠️  LightGBM not installed. Skipping.")
            return
        
        params = self.best_params.get('lightgbm', {}).get('best_params', {})
        print(f"Using parameters: {params}")
        
        # Remap labels
        y_remapped = self.y - 1
        
        lgb_clf = lgb.LGBMClassifier(
            objective='multiclass',
            num_class=len(np.unique(y_remapped)),
            random_state=self.random_state,
            verbose=-1,
            **params
        )
        
        # Cross-validation
        cv_results = cross_validate(
            lgb_clf, self.X, y_remapped,
            cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=self.random_state),
            scoring=['accuracy', 'precision_macro', 'recall_macro', 'f1_macro'],
            return_train_score=True,
            n_jobs=-1,
            verbose=1
        )
        
        print(f"\nCross-Validation Results:")
        print(f"  Accuracy: {cv_results['test_accuracy'].mean():.4f} ± {cv_results['test_accuracy'].std():.4f}")
        
        # Train on full dataset
        print("\nTraining on full dataset...")
        lgb_clf.fit(self.X, y_remapped)
        
        self.models['lightgbm'] = {
            'estimator': lgb_clf,
            'cv_accuracy': float(cv_results['test_accuracy'].mean()),
            'cv_std': float(cv_results['test_accuracy'].std()),
            'label_offset': 1
        }
        
        print("✅ LightGBM training complete")
        
    def create_ensemble(self):
        """
        Create weighted voting ensemble.
        
        Weights are proportional to individual CV accuracy.
        """
        print("\n" + "="*80)
        print("Creating Weighted Voting Ensemble")
        print("="*80)
        
        if not self.models:
            print("❌ No models trained yet")
            return
        
        # Calculate weights from CV accuracy
        weights = []
        estimators = []
        
        for name, model_data in self.models.items():
            estimators.append((name, model_data['estimator']))
            weights.append(model_data['cv_accuracy'])
        
        # Normalize weights
        weights = np.array(weights)
        weights = weights / weights.sum()
        
        print(f"\nEnsemble composition:")
        for (name, _), weight in zip(estimators, weights):
            acc = self.models[name]['cv_accuracy']
            print(f"  {name}: weight={weight:.3f} (CV acc={acc:.4f})")
        
        # Note: sklearn VotingClassifier doesn't support different label spaces
        # We'll implement custom ensemble prediction
        self.ensemble_weights = dict(zip([name for name, _ in estimators], weights))
        
        print("\n✅ Ensemble created")
        
    def evaluate_ensemble(self):
        """
        Evaluate ensemble using cross-validation.
        
        Custom implementation to handle different label spaces.
        """
        print("\n" + "="*80)
        print("Evaluating Ensemble")
        print("="*80)
        
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=self.random_state)
        
        all_predictions = []
        all_true = []
        
        for fold, (train_idx, test_idx) in enumerate(cv.split(self.X, self.y), 1):
            X_train, X_test = self.X[train_idx], self.X[test_idx]
            y_train, y_test = self.y[train_idx], self.y[test_idx]
            
            # Train all models on fold
            fold_models = {}
            
            for name, model_data in self.models.items():
                estimator = model_data['estimator']
                label_offset = model_data.get('label_offset', 0)
                
                # Adjust labels if needed
                y_train_adj = y_train - label_offset if label_offset else y_train
                
                # Clone and train
                from sklearn.base import clone
                clf = clone(estimator)
                clf.fit(X_train, y_train_adj)
                
                fold_models[name] = (clf, label_offset)
            
            # Ensemble prediction (weighted voting)
            predictions = self._ensemble_predict(fold_models, X_test)
            
            all_predictions.extend(predictions)
            all_true.extend(y_test)
            
            acc = accuracy_score(y_test, predictions)
            print(f"  Fold {fold}: Accuracy = {acc:.4f}")
        
        # Overall metrics
        overall_acc = accuracy_score(all_true, all_predictions)
        
        print(f"\n{'='*80}")
        print(f"Ensemble Cross-Validation Accuracy: {overall_acc:.4f}")
        print(f"{'='*80}")
        
        self.ensemble_cv_accuracy = overall_acc
        
        return overall_acc
        
    def _ensemble_predict(self, models, X):
        """Custom ensemble prediction with weighted voting."""
        predictions_proba = []
        weights = []
        
        for name, (clf, label_offset) in models.items():
            # Get predictions
            pred = clf.predict(X)
            
            # Adjust labels back
            if label_offset:
                pred = pred + label_offset
            
            predictions_proba.append(pred)
            weights.append(self.ensemble_weights[name])
        
        # Weighted voting (simple majority)
        predictions_proba = np.array(predictions_proba)
        weights = np.array(weights)
        
        # For each sample, find most weighted prediction
        final_predictions = []
        for i in range(X.shape[0]):
            sample_preds = predictions_proba[:, i]
            # Count weighted votes for each class
            unique_preds = np.unique(sample_preds)
            weighted_votes = {}
            for pred in unique_preds:
                mask = sample_preds == pred
                weighted_votes[pred] = weights[mask].sum()
            
            # Select class with highest weighted vote
            final_pred = max(weighted_votes, key=weighted_votes.get)
            final_predictions.append(final_pred)
        
        return np.array(final_predictions)
        
    def save_models(self, output_dir):
        """Save all trained models and metadata."""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save individual models
        for name, model_data in self.models.items():
            model_path = output_dir / f'{name}_model.pkl'
            joblib.dump(model_data['estimator'], model_path)
            print(f"✅ Saved {name} to {model_path}")
        
        # Save ensemble metadata
        metadata = {
            'ensemble_weights': self.ensemble_weights,
            'model_cv_scores': {
                name: {
                    'accuracy': model_data['cv_accuracy'],
                    'std': model_data['cv_std']
                }
                for name, model_data in self.models.items()
            },
            'ensemble_cv_accuracy': getattr(self, 'ensemble_cv_accuracy', None),
            'n_features': int(self.X.shape[1]),
            'n_samples': int(self.X.shape[0]),
            'n_classes': int(len(np.unique(self.y)))
        }
        
        metadata_path = output_dir / 'ensemble_metadata.json'
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"✅ Saved ensemble metadata to {metadata_path}")


def main():
    parser = argparse.ArgumentParser(
        description='Train ensemble model for BAHR meter detection'
    )
    parser.add_argument('--features', default='data/ml/X_train.npy',
                       help='Path to feature matrix')
    parser.add_argument('--targets', default='data/ml/y_train.npy',
                       help='Path to target labels')
    parser.add_argument('--feature-indices',
                       default='ml_pipeline/results/optimized_feature_indices.npy',
                       help='Path to optimized feature indices')
    parser.add_argument('--params', default='ml_pipeline/results/best_params.json',
                       help='Path to best hyperparameters')
    parser.add_argument('--output', default='models/ensemble_v1',
                       help='Output directory for trained models')
    
    args = parser.parse_args()
    
    print("="*80)
    print("BAHR Ensemble Model Training Pipeline")
    print("="*80)
    
    trainer = EnsembleTrainer()
    
    # Load data and hyperparameters
    trainer.load_data(args.features, args.targets, args.feature_indices)
    trainer.load_hyperparameters(args.params)
    
    # Train individual models
    trainer.train_random_forest()
    trainer.train_xgboost()
    trainer.train_lightgbm()
    
    # Create and evaluate ensemble
    trainer.create_ensemble()
    trainer.evaluate_ensemble()
    
    # Save models
    trainer.save_models(args.output)
    
    print("\n" + "="*80)
    print("✅ Ensemble training complete!")
    print("="*80)
    print(f"\nModels saved to: {args.output}")
    print("\nNext steps:")
    print("  1. Review ensemble performance")
    print("  2. Implement sequence models (BiLSTM-CRF)")


if __name__ == '__main__':
    main()
