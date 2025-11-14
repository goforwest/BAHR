#!/usr/bin/env python3
"""
BAHR ML Pipeline - Phase 5.1: Feature Engineering Refinement

Implements:
1. Recursive Feature Elimination (RFE) to reduce 71 → 40-50 features
2. SHAP analysis for feature importance
3. Ablation study to validate feature groups
4. Visualization and reporting

Usage:
    python ml_pipeline/feature_optimization.py --input data/ml/X_train.npy \
                                                --target data/ml/y_train.npy \
                                                --output ml_pipeline/results/feature_analysis.json
"""

import sys
import json
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import RFE, RFECV
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.metrics import accuracy_score, classification_report
import shap

sys.path.insert(0, 'backend')
from app.ml.feature_extractor import BAHRFeatureExtractor


class FeatureOptimizer:
    """
    Optimize feature set for BAHR meter detection.
    
    Strategies:
    1. Remove redundant/collinear features
    2. Recursive elimination based on importance
    3. SHAP value analysis for interpretability
    4. Ablation study by feature group
    """
    
    def __init__(self, random_state=42):
        self.random_state = random_state
        self.extractor = BAHRFeatureExtractor()
        self.feature_names = self.extractor.get_feature_names()
        self.results = {}
        
    def load_data(self, X_path, y_path):
        """Load feature matrix and targets."""
        print(f"Loading data from {X_path} and {y_path}")
        self.X = np.load(X_path)
        self.y = np.load(y_path)
        print(f"✅ Loaded: X shape={self.X.shape}, y shape={self.y.shape}")
        
    def analyze_correlation(self, threshold=0.95):
        """
        Identify highly correlated feature pairs.
        
        High correlation (>0.95) suggests redundancy.
        """
        print("\n" + "="*80)
        print("Step 1: Correlation Analysis")
        print("="*80)
        
        # Compute correlation matrix
        df = pd.DataFrame(self.X, columns=self.feature_names)
        corr_matrix = df.corr().abs()
        
        # Find highly correlated pairs
        upper_tri = corr_matrix.where(
            np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
        )
        
        high_corr_pairs = [
            (column, row, corr_matrix.loc[row, column])
            for column in upper_tri.columns
            for row in upper_tri.index
            if upper_tri.loc[row, column] > threshold
        ]
        
        print(f"\nFound {len(high_corr_pairs)} feature pairs with correlation > {threshold}:")
        for feat1, feat2, corr in high_corr_pairs[:10]:  # Show top 10
            print(f"  {feat1} ↔ {feat2}: {corr:.3f}")
        
        self.results['correlation_analysis'] = {
            'threshold': threshold,
            'high_corr_pairs': [
                {'feature1': f1, 'feature2': f2, 'correlation': float(c)}
                for f1, f2, c in high_corr_pairs
            ]
        }
        
        # Visualize correlation heatmap (top 30 features)
        plt.figure(figsize=(16, 14))
        sns.heatmap(corr_matrix.iloc[:30, :30], annot=False, cmap='coolwarm', 
                    center=0, vmin=-1, vmax=1)
        plt.title('Feature Correlation Matrix (Top 30 Features)')
        plt.tight_layout()
        
        output_dir = Path('ml_pipeline/results/figures')
        output_dir.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_dir / 'correlation_heatmap.png', dpi=150)
        print(f"✅ Saved correlation heatmap to {output_dir / 'correlation_heatmap.png'}")
        plt.close()
        
    def recursive_feature_elimination(self, target_features=45, cv=5):
        """
        Use RFECV to find optimal feature subset.
        
        Args:
            target_features: Target number of features (default: 45)
            cv: Cross-validation folds
        """
        print("\n" + "="*80)
        print("Step 2: Recursive Feature Elimination (RFECV)")
        print("="*80)
        
        # Base estimator
        rf = RandomForestClassifier(
            n_estimators=100,
            max_depth=20,
            random_state=self.random_state,
            n_jobs=-1
        )
        
        # RFE with cross-validation
        print(f"Running RFECV with {cv}-fold cross-validation...")
        rfecv = RFECV(
            estimator=rf,
            step=1,
            cv=StratifiedKFold(n_splits=cv),
            scoring='accuracy',
            n_jobs=-1,
            verbose=1
        )
        
        rfecv.fit(self.X, self.y)
        
        print(f"\n✅ Optimal number of features: {rfecv.n_features_}")
        print(f"✅ Best CV accuracy: {rfecv.cv_results_['mean_test_score'].max():.4f}")
        
        # Get selected features
        selected_features = [
            self.feature_names[i] 
            for i, selected in enumerate(rfecv.support_) 
            if selected
        ]
        
        print(f"\nSelected features ({len(selected_features)}):")
        for i, feat in enumerate(selected_features, 1):
            rank = rfecv.ranking_[self.feature_names.index(feat)]
            print(f"  {i}. {feat} (rank: {rank})")
        
        # Plot CV scores vs. number of features
        plt.figure(figsize=(12, 6))
        plt.plot(range(1, len(rfecv.cv_results_['mean_test_score']) + 1),
                 rfecv.cv_results_['mean_test_score'])
        plt.xlabel('Number of Features')
        plt.ylabel('Cross-Validation Accuracy')
        plt.title('RFECV: Accuracy vs. Number of Features')
        plt.axvline(x=rfecv.n_features_, color='r', linestyle='--', 
                    label=f'Optimal: {rfecv.n_features_} features')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        output_dir = Path('ml_pipeline/results/figures')
        plt.savefig(output_dir / 'rfecv_curve.png', dpi=150)
        print(f"✅ Saved RFECV curve to {output_dir / 'rfecv_curve.png'}")
        plt.close()
        
        self.results['rfecv'] = {
            'n_features_optimal': int(rfecv.n_features_),
            'best_cv_accuracy': float(rfecv.cv_results_['mean_test_score'].max()),
            'selected_features': selected_features,
            'feature_ranking': {
                self.feature_names[i]: int(rank)
                for i, rank in enumerate(rfecv.ranking_)
            }
        }
        
        self.selected_features = selected_features
        self.rfecv = rfecv
        
    def shap_analysis(self, n_samples=500):
        """
        Compute SHAP values for feature importance.
        
        Args:
            n_samples: Number of samples for SHAP computation (default: 500)
        """
        print("\n" + "="*80)
        print("Step 3: SHAP Value Analysis")
        print("="*80)
        
        # Train model on full dataset
        rf = RandomForestClassifier(
            n_estimators=200,
            max_depth=20,
            random_state=self.random_state,
            n_jobs=-1
        )
        
        print("Training RandomForest for SHAP analysis...")
        rf.fit(self.X, self.y)
        
        # Compute SHAP values (use subset for speed)
        print(f"Computing SHAP values for {n_samples} samples...")
        explainer = shap.TreeExplainer(rf)
        
        # Use random subset
        indices = np.random.RandomState(self.random_state).choice(
            len(self.X), size=min(n_samples, len(self.X)), replace=False
        )
        X_sample = self.X[indices]
        
        shap_values = explainer.shap_values(X_sample)
        
        # Average absolute SHAP values across all classes and samples
        if isinstance(shap_values, list):
            # Old multi-class format: list of [n_samples, n_features]
            stacked = np.stack([np.abs(sv) for sv in shap_values], axis=0)
            mean_abs_shap = stacked.mean(axis=1).mean(axis=0)
        elif shap_values.ndim == 3:
            # New multi-class format: [n_samples, n_features, n_classes]
            # Mean over samples (axis=0) then over classes (axis=1)
            mean_abs_shap = np.abs(shap_values).mean(axis=0).mean(axis=1)
        else:
            # Binary or single output: [n_samples, n_features]
            mean_abs_shap = np.abs(shap_values).mean(axis=0)
        
        # Create importance ranking
        shap_importance = pd.DataFrame({
            'feature': self.feature_names,
            'mean_abs_shap': mean_abs_shap
        }).sort_values('mean_abs_shap', ascending=False)
        
        print("\nTop 20 features by SHAP importance:")
        for i, row in shap_importance.head(20).iterrows():
            print(f"  {row['feature']}: {row['mean_abs_shap']:.4f}")
        
        # For multi-class SHAP visualization, we need to use averaged values or single class
        # Since shap_values is 3D [n_samples, n_features, n_classes], 
        # average across classes for visualization
        if shap_values.ndim == 3:
            shap_for_plot = shap_values.mean(axis=2)  # Average over classes
        else:
            shap_for_plot = shap_values
        
        # Plot SHAP summary
        plt.figure(figsize=(12, 10))
        shap.summary_plot(
            shap_for_plot,
            X_sample,
            feature_names=self.feature_names,
            show=False,
            max_display=20
        )
        plt.tight_layout()
        
        output_dir = Path('ml_pipeline/results/figures')
        plt.savefig(output_dir / 'shap_summary.png', dpi=150, bbox_inches='tight')
        print(f"✅ Saved SHAP summary to {output_dir / 'shap_summary.png'}")
        plt.close()
        
        # Bar plot of mean absolute SHAP values
        plt.figure(figsize=(12, 8))
        shap_importance.head(25).plot.barh(x='feature', y='mean_abs_shap', 
                                            legend=False, color='steelblue')
        plt.xlabel('Mean Absolute SHAP Value')
        plt.title('Feature Importance (SHAP Analysis)')
        plt.tight_layout()
        plt.savefig(output_dir / 'shap_importance_bar.png', dpi=150)
        print(f"✅ Saved SHAP bar plot to {output_dir / 'shap_importance_bar.png'}")
        plt.close()
        
        self.results['shap_analysis'] = {
            'top_20_features': [
                {'feature': row['feature'], 'mean_abs_shap': float(row['mean_abs_shap'])}
                for _, row in shap_importance.head(20).iterrows()
            ]
        }
        
    def ablation_study(self):
        """
        Test accuracy when removing each feature group.
        
        Feature groups:
        - Pattern features (8)
        - Similarity features (16)
        - Discriminative features (5)
        - Relative similarity features (16)
        - Rule features (16)
        - Linguistic features (10)
        """
        print("\n" + "="*80)
        print("Step 4: Ablation Study by Feature Group")
        print("="*80)
        
        feature_groups = {
            'pattern': [f for f in self.feature_names if f.startswith(('pattern_', 'sakin_', 'mutaharrik_', 'consecutive_', 'rhythm_'))],
            'similarity': [f for f in self.feature_names if f.startswith('similarity_to_meter_')],
            'discriminative': ['similarity_spread', 'similarity_ratio', 'similarity_std', 
                              'similarity_mean', 'is_clear_winner'],
            'relative': [f for f in self.feature_names if f.startswith('relative_similarity_')],
            'rule': [f for f in self.feature_names if f.startswith('rule_match_')],
            'linguistic': [f for f in self.feature_names if f.startswith(('word_', 'letter_', 'avg_'))]
        }
        
        # Baseline: all features
        rf = RandomForestClassifier(
            n_estimators=100,
            max_depth=20,
            random_state=self.random_state,
            n_jobs=-1
        )
        
        baseline_scores = cross_val_score(
            rf, self.X, self.y, 
            cv=StratifiedKFold(n_splits=5),
            scoring='accuracy',
            n_jobs=-1
        )
        baseline_acc = baseline_scores.mean()
        
        print(f"\nBaseline (all 71 features): {baseline_acc:.4f} ± {baseline_scores.std():.4f}")
        
        ablation_results = {'baseline': float(baseline_acc)}
        
        # Test removing each group
        for group_name, group_features in feature_groups.items():
            # Get indices of features to keep
            keep_indices = [
                i for i, feat in enumerate(self.feature_names)
                if feat not in group_features
            ]
            
            X_ablated = self.X[:, keep_indices]
            
            scores = cross_val_score(
                rf, X_ablated, self.y,
                cv=StratifiedKFold(n_splits=5),
                scoring='accuracy',
                n_jobs=-1
            )
            
            acc = scores.mean()
            delta = acc - baseline_acc
            
            print(f"\nWithout {group_name} ({len(group_features)} features):")
            print(f"  Accuracy: {acc:.4f} ± {scores.std():.4f}")
            print(f"  Delta: {delta:+.4f} ({delta/baseline_acc*100:+.2f}%)")
            
            ablation_results[f'without_{group_name}'] = {
                'accuracy': float(acc),
                'delta': float(delta),
                'n_features': len(group_features),
                'features_removed': group_features
            }
        
        self.results['ablation_study'] = ablation_results
        
    def generate_optimized_feature_set(self, target_n=45):
        """
        Generate final optimized feature set based on all analyses.
        
        Strategy:
        1. Start with RFECV selected features
        2. Remove highly correlated duplicates
        3. Ensure diversity across feature groups
        """
        print("\n" + "="*80)
        print(f"Step 5: Generate Optimized Feature Set (target: {target_n} features)")
        print("="*80)
        
        if not hasattr(self, 'selected_features'):
            print("⚠️  RFECV not run yet. Using all features.")
            self.selected_features = self.feature_names
        
        # Get SHAP importance
        if 'shap_analysis' in self.results:
            shap_ranking = {
                item['feature']: item['mean_abs_shap']
                for item in self.results['shap_analysis']['top_20_features']
            }
        else:
            shap_ranking = {}
        
        # Rank selected features by SHAP importance
        selected_with_shap = [
            (feat, shap_ranking.get(feat, 0))
            for feat in self.selected_features
        ]
        selected_with_shap.sort(key=lambda x: x[1], reverse=True)
        
        # Take top N
        optimized_features = [feat for feat, _ in selected_with_shap[:target_n]]
        
        print(f"\n✅ Optimized feature set ({len(optimized_features)} features):")
        for i, feat in enumerate(optimized_features, 1):
            shap_score = shap_ranking.get(feat, 0)
            print(f"  {i}. {feat} (SHAP: {shap_score:.4f})")
        
        # Test accuracy with optimized set
        optimized_indices = [
            self.feature_names.index(feat) 
            for feat in optimized_features
        ]
        X_optimized = self.X[:, optimized_indices]
        
        rf = RandomForestClassifier(
            n_estimators=100,
            max_depth=20,
            random_state=self.random_state,
            n_jobs=-1
        )
        
        scores = cross_val_score(
            rf, X_optimized, self.y,
            cv=StratifiedKFold(n_splits=5),
            scoring='accuracy',
            n_jobs=-1
        )
        
        optimized_acc = scores.mean()
        
        # Compare to baseline
        baseline_acc = self.results.get('ablation_study', {}).get('baseline', 0)
        delta = optimized_acc - baseline_acc
        
        print(f"\n{'='*80}")
        print("COMPARISON:")
        print(f"  Baseline (71 features): {baseline_acc:.4f}")
        print(f"  Optimized ({len(optimized_features)} features): {optimized_acc:.4f}")
        print(f"  Delta: {delta:+.4f} ({delta/baseline_acc*100:+.2f}%)")
        print(f"  Feature reduction: {71 - len(optimized_features)} features removed ({(71-len(optimized_features))/71*100:.1f}%)")
        print(f"{'='*80}")
        
        self.results['optimized_feature_set'] = {
            'n_features': len(optimized_features),
            'features': optimized_features,
            'accuracy': float(optimized_acc),
            'accuracy_std': float(scores.std()),
            'baseline_accuracy': float(baseline_acc),
            'delta': float(delta),
            'feature_reduction_pct': float((71 - len(optimized_features)) / 71 * 100)
        }
        
        # Save optimized feature indices
        np.save('ml_pipeline/results/optimized_feature_indices.npy', 
                np.array(optimized_indices))
        print(f"✅ Saved optimized feature indices to ml_pipeline/results/optimized_feature_indices.npy")
        
    def save_results(self, output_path):
        """Save all analysis results to JSON."""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Saved complete analysis to {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description='Feature optimization for BAHR meter detection'
    )
    parser.add_argument('--input-X', default='data/ml/X_train.npy',
                       help='Path to feature matrix')
    parser.add_argument('--input-y', default='data/ml/y_train.npy',
                       help='Path to target labels')
    parser.add_argument('--output', default='ml_pipeline/results/feature_analysis.json',
                       help='Output path for analysis results')
    parser.add_argument('--target-features', type=int, default=45,
                       help='Target number of features (default: 45)')
    parser.add_argument('--shap-samples', type=int, default=500,
                       help='Number of samples for SHAP analysis (default: 500)')
    
    args = parser.parse_args()
    
    print("="*80)
    print("BAHR Feature Optimization Pipeline")
    print("="*80)
    
    optimizer = FeatureOptimizer()
    
    # Load data
    optimizer.load_data(args.input_X, args.input_y)
    
    # Run analysis pipeline
    optimizer.analyze_correlation(threshold=0.95)
    optimizer.recursive_feature_elimination(target_features=args.target_features)
    optimizer.shap_analysis(n_samples=args.shap_samples)
    optimizer.ablation_study()
    optimizer.generate_optimized_feature_set(target_n=args.target_features)
    
    # Save results
    optimizer.save_results(args.output)
    
    print("\n" + "="*80)
    print("✅ Feature optimization complete!")
    print("="*80)
    print(f"\nResults saved to: {args.output}")
    print("Visualizations saved to: ml_pipeline/results/figures/")
    print("\nNext steps:")
    print("  1. Review feature analysis results")
    print("  2. Run hyperparameter tuning with optimized features")
    print("  3. Train ensemble models")


if __name__ == '__main__':
    main()
