#!/usr/bin/env python3
"""
BAHR ML Pipeline - Comprehensive Evaluation Suite

Implements advanced evaluation metrics:
1. Top-1, Top-3, Top-5 accuracy
2. Mean Reciprocal Rank (MRR)
3. Expected Calibration Error (ECE)
4. Per-meter F1, Precision, Recall
5. Confidence-Accuracy correlation
6. Error taxonomy and confusion matrices

Usage:
    python ml_pipeline/evaluation_suite.py --model models/ensemble_v1 \
                                            --test-data dataset/evaluation/golden_set_v1_3_with_sari.jsonl \
                                            --output ml_pipeline/results/evaluation_report.json
"""

import sys
import json
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Tuple
from collections import defaultdict
from sklearn.metrics import (
    accuracy_score, precision_recall_fscore_support,
    confusion_matrix, classification_report
)
from sklearn.calibration import calibration_curve
import joblib

sys.path.insert(0, 'backend')
from app.ml.feature_extractor import BAHRFeatureExtractor


# Meter name to ID mapping
METER_NAME_TO_ID = {
    'الطويل': 1, 'الكامل': 2, 'الوافر': 3, 'الرمل': 4,
    'البسيط': 5, 'المتقارب': 6, 'الرجز': 7, 'السريع': 8,
    'المديد': 9, 'المنسرح': 10, 'الهزج': 11, 'الخفيف': 12,
    'المجتث': 13, 'المقتضب': 14, 'المضارع': 15, 'المتدارك': 16,
}

METER_ID_TO_NAME = {v: k for k, v in METER_NAME_TO_ID.items()}


@dataclass
class ErrorCase:
    """Represents a single misclassification."""
    verse_id: str
    verse_text: str
    true_meter: str
    predicted_meter: str
    confidence: float
    error_type: str
    true_meter_rank: int
    top_3_predictions: List[Tuple[str, float]]


class ComprehensiveEvaluator:
    """
    Comprehensive evaluation suite for BAHR meter detection.
    
    Provides multiple evaluation metrics and error analysis.
    """
    
    def __init__(self, model_dir: str):
        """
        Initialize evaluator with trained model.
        
        Args:
            model_dir: Directory containing trained ensemble models
        """
        self.model_dir = Path(model_dir)
        self.feature_extractor = BAHRFeatureExtractor()
        self.load_models()
        
    def load_models(self):
        """Load trained ensemble models and metadata."""
        print(f"Loading models from {self.model_dir}")
        
        # Load metadata
        metadata_path = self.model_dir / 'ensemble_metadata.json'
        with open(metadata_path, 'r') as f:
            self.metadata = json.load(f)
        
        # Check if feature selection was used
        self.feature_indices = None
        feature_indices_path = Path('ml_pipeline/results/optimized_feature_indices.npy')
        if feature_indices_path.exists() and self.metadata.get('n_features', 71) < 71:
            self.feature_indices = np.load(feature_indices_path)
            print(f"✅ Loaded feature selection: {len(self.feature_indices)} features")
        
        # Load individual models
        self.models = {}
        for name in self.metadata['ensemble_weights'].keys():
            model_path = self.model_dir / f'{name}_model.pkl'
            if model_path.exists():
                self.models[name] = joblib.load(model_path)
                print(f"✅ Loaded {name}")
        
        self.ensemble_weights = self.metadata['ensemble_weights']
        
    def load_test_data(self, test_path: str):
        """Load and prepare test dataset."""
        print(f"\nLoading test data from {test_path}")
        
        verses = []
        with open(test_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    data = json.loads(line)
                    verses.append(data)
        
        print(f"✅ Loaded {len(verses)} test verses")
        
        # Extract features
        print("Extracting features...")
        self.test_verses = verses
        self.test_features = []
        self.test_labels = []
        
        for verse in verses:
            features = self.feature_extractor.extract_features(
                verse['text'],
                include_target=False
            )
            
            # Convert to array (ensure same order as training)
            feature_array = np.array([
                features[fname] 
                for fname in self.feature_extractor.get_feature_names()
            ])
            
            self.test_features.append(feature_array)
            
            meter_name = verse.get('meter', '')
            meter_id = METER_NAME_TO_ID.get(meter_name, 0)
            self.test_labels.append(meter_id)
        
        self.X_test = np.array(self.test_features)
        self.y_test = np.array(self.test_labels)
        
        # Apply feature selection if available
        if self.feature_indices is not None:
            self.X_test = self.X_test[:, self.feature_indices]
            print(f"✅ Applied feature selection: {self.X_test.shape[1]} features")
        
        print(f"✅ Feature extraction complete: {self.X_test.shape}")
        
    def predict_with_probabilities(self):
        """
        Generate predictions with probability scores.
        
        Returns predicted classes and probability distributions.
        """
        print("\nGenerating predictions...")
        
        # Determine number of classes from metadata or data
        n_classes = self.metadata.get('n_classes', 16)
        
        # Get predictions from each model
        all_predictions = []
        all_probas = []
        
        for name, model in self.models.items():
            weight = self.ensemble_weights[name]
            
            # Predict
            if hasattr(model, 'predict_proba'):
                proba = model.predict_proba(self.X_test)
                pred = model.predict(self.X_test)
            else:
                pred = model.predict(self.X_test)
                # Create pseudo-probabilities (one-hot)
                proba = np.zeros((len(pred), n_classes))
                for i, p in enumerate(pred):
                    proba[i, int(p)] = 1.0
            
            # Ensure probability array has correct shape (n_samples, n_classes+1) for 1-indexed labels
            # XGBoost/LightGBM return 0-indexed classes, RandomForest returns 1-indexed
            if proba.shape[1] == n_classes:
                # 0-indexed (XGBoost, LightGBM) - add column at start for label 0
                proba_aligned = np.zeros((proba.shape[0], n_classes + 1))
                proba_aligned[:, 1:] = proba
                pred = pred + 1  # Convert to 1-indexed
            else:
                # Already correct shape
                proba_aligned = proba
            
            all_predictions.append(pred)
            all_probas.append(proba_aligned * weight)
        
        # Weighted ensemble voting
        ensemble_proba = np.sum(all_probas, axis=0)
        
        # Normalize probabilities
        ensemble_proba = ensemble_proba / ensemble_proba.sum(axis=1, keepdims=True)
        
        # Get final predictions (probabilities are 0-indexed with extra column for label 0)
        # argmax gives 0-16, where 0 is unused, so we keep as-is (1-16 are valid meters)
        self.predictions = np.argmax(ensemble_proba, axis=1)
        
        # If all predictions are 0, something went wrong - use max probability column > 0
        if np.all(self.predictions == 0):
            self.predictions = np.argmax(ensemble_proba[:, 1:], axis=1) + 1
        
        self.prediction_probas = ensemble_proba
        
        print(f"✅ Predictions generated for {len(self.predictions)} samples")
        print(f"   Prediction range: {self.predictions.min()}-{self.predictions.max()}")
        
    def compute_top_k_accuracy(self, k_values=[1, 3, 5]):
        """
        Compute Top-K accuracy.
        
        Args:
            k_values: List of K values to compute
            
        Returns:
            Dictionary with Top-K accuracies
        """
        print(f"\nComputing Top-K accuracy for K={k_values}")
        
        top_k_results = {}
        
        for k in k_values:
            # Get top-k predictions for each sample
            top_k_preds = np.argsort(self.prediction_probas, axis=1)[:, -k:] + 1
            
            # Check if true label is in top-k
            correct = 0
            for i, true_label in enumerate(self.y_test):
                if true_label in top_k_preds[i]:
                    correct += 1
            
            accuracy = correct / len(self.y_test)
            top_k_results[f'top_{k}_accuracy'] = accuracy
            
            print(f"  Top-{k} Accuracy: {accuracy:.4f} ({correct}/{len(self.y_test)})")
        
        return top_k_results
        
    def compute_mrr(self):
        """
        Compute Mean Reciprocal Rank.
        
        MRR measures where the correct answer appears in the ranked list.
        """
        print("\nComputing Mean Reciprocal Rank (MRR)")
        
        reciprocal_ranks = []
        
        for i, true_label in enumerate(self.y_test):
            # Get ranking of predictions
            ranked_preds = np.argsort(self.prediction_probas[i])[::-1] + 1
            
            # Find rank of true label
            rank = np.where(ranked_preds == true_label)[0][0] + 1
            reciprocal_ranks.append(1.0 / rank)
        
        mrr = np.mean(reciprocal_ranks)
        
        print(f"  MRR: {mrr:.4f}")
        
        return mrr
        
    def compute_ece(self, n_bins=10):
        """
        Compute Expected Calibration Error.
        
        ECE measures the difference between predicted confidence
        and actual accuracy.
        
        Args:
            n_bins: Number of bins for calibration curve
        """
        print(f"\nComputing Expected Calibration Error (ECE) with {n_bins} bins")
        
        # Get confidence scores (max probability)
        confidences = np.max(self.prediction_probas, axis=1)
        
        # Binary correctness
        correct = (self.predictions == self.y_test).astype(int)
        
        # Compute calibration curve
        prob_true, prob_pred = calibration_curve(
            correct, confidences, n_bins=n_bins, strategy='uniform'
        )
        
        # Compute ECE
        ece = np.mean(np.abs(prob_true - prob_pred))
        
        print(f"  ECE: {ece:.4f}")
        
        # Plot calibration curve
        plt.figure(figsize=(8, 6))
        plt.plot([0, 1], [0, 1], 'k--', label='Perfect calibration')
        plt.plot(prob_pred, prob_true, 's-', label=f'Model (ECE={ece:.3f})')
        plt.xlabel('Predicted Confidence')
        plt.ylabel('Actual Accuracy')
        plt.title('Calibration Curve')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        output_dir = Path('ml_pipeline/results/figures')
        output_dir.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_dir / 'calibration_curve.png', dpi=150)
        print(f"  Saved calibration curve to {output_dir / 'calibration_curve.png'}")
        plt.close()
        
        return ece
        
    def compute_per_meter_metrics(self):
        """
        Compute precision, recall, F1 for each meter.
        """
        print("\nComputing per-meter metrics")
        
        # Get unique meters in test set
        unique_meters = np.unique(self.y_test)
        
        # Compute metrics
        precision, recall, f1, support = precision_recall_fscore_support(
            self.y_test, self.predictions, labels=unique_meters, zero_division=0
        )
        
        per_meter_results = {}
        
        print(f"\n{'Meter':<20} {'Precision':<10} {'Recall':<10} {'F1':<10} {'Support':<10}")
        print("="*70)
        
        for i, meter_id in enumerate(unique_meters):
            meter_name = METER_ID_TO_NAME.get(meter_id, f'Unknown_{meter_id}')
            
            per_meter_results[meter_name] = {
                'precision': float(precision[i]),
                'recall': float(recall[i]),
                'f1': float(f1[i]),
                'support': int(support[i])
            }
            
            print(f"{meter_name:<20} {precision[i]:<10.4f} {recall[i]:<10.4f} "
                  f"{f1[i]:<10.4f} {support[i]:<10}")
        
        # Compute macro averages
        macro_precision = np.mean(precision)
        macro_recall = np.mean(recall)
        macro_f1 = np.mean(f1)
        
        print("="*70)
        print(f"{'Macro Average':<20} {macro_precision:<10.4f} {macro_recall:<10.4f} "
              f"{macro_f1:<10.4f}")
        
        return per_meter_results
        
    def analyze_confidence_accuracy_gap(self):
        """
        Analyze correlation between confidence and correctness.
        """
        print("\nAnalyzing confidence-accuracy correlation")
        
        confidences = np.max(self.prediction_probas, axis=1)
        correct = (self.predictions == self.y_test).astype(int)
        
        # Compute correlation
        correlation = np.corrcoef(confidences, correct)[0, 1]
        
        print(f"  Confidence-Accuracy Correlation: {correlation:.4f}")
        
        # Plot confidence distribution by correctness
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Histogram
        axes[0].hist(confidences[correct == 1], bins=20, alpha=0.7, 
                     label='Correct', color='green')
        axes[0].hist(confidences[correct == 0], bins=20, alpha=0.7,
                     label='Incorrect', color='red')
        axes[0].set_xlabel('Confidence')
        axes[0].set_ylabel('Count')
        axes[0].set_title('Confidence Distribution')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # Accuracy by confidence bin
        confidence_bins = np.linspace(0, 1, 11)
        bin_centers = (confidence_bins[:-1] + confidence_bins[1:]) / 2
        bin_accuracies = []
        
        for i in range(len(confidence_bins) - 1):
            mask = (confidences >= confidence_bins[i]) & (confidences < confidence_bins[i+1])
            if mask.sum() > 0:
                bin_acc = correct[mask].mean()
            else:
                bin_acc = 0
            bin_accuracies.append(bin_acc)
        
        axes[1].plot(bin_centers, bin_accuracies, 'o-', label='Accuracy')
        axes[1].plot([0, 1], [0, 1], 'k--', label='Perfect calibration')
        axes[1].set_xlabel('Confidence Bin')
        axes[1].set_ylabel('Accuracy')
        axes[1].set_title('Accuracy vs. Confidence')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        output_dir = Path('ml_pipeline/results/figures')
        plt.savefig(output_dir / 'confidence_analysis.png', dpi=150)
        print(f"  Saved confidence analysis to {output_dir / 'confidence_analysis.png'}")
        plt.close()
        
        return correlation
        
    def generate_confusion_matrix(self):
        """Generate and visualize confusion matrix."""
        print("\nGenerating confusion matrix")
        
        cm = confusion_matrix(self.y_test, self.predictions)
        
        # Normalize by true labels
        cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        
        # Plot
        fig, axes = plt.subplots(1, 2, figsize=(20, 8))
        
        # Raw counts
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[0],
                    xticklabels=[METER_ID_TO_NAME.get(i, f'{i}') for i in range(1, 17)],
                    yticklabels=[METER_ID_TO_NAME.get(i, f'{i}') for i in range(1, 17)])
        axes[0].set_title('Confusion Matrix (Counts)')
        axes[0].set_xlabel('Predicted')
        axes[0].set_ylabel('True')
        
        # Normalized
        sns.heatmap(cm_normalized, annot=True, fmt='.2f', cmap='Blues', ax=axes[1],
                    xticklabels=[METER_ID_TO_NAME.get(i, f'{i}') for i in range(1, 17)],
                    yticklabels=[METER_ID_TO_NAME.get(i, f'{i}') for i in range(1, 17)])
        axes[1].set_title('Confusion Matrix (Normalized)')
        axes[1].set_xlabel('Predicted')
        axes[1].set_ylabel('True')
        
        plt.tight_layout()
        
        output_dir = Path('ml_pipeline/results/figures')
        plt.savefig(output_dir / 'confusion_matrix.png', dpi=150)
        print(f"  Saved confusion matrix to {output_dir / 'confusion_matrix.png'}")
        plt.close()
        
    def categorize_errors(self):
        """
        Categorize errors into types:
        1. Ambiguous patterns (multiple meters share pattern)
        2. Rare transformations (unusual ziḥāfāt)
        3. Low confidence (model uncertain)
        4. Systematic confusions (specific meter pairs)
        """
        print("\nCategorizing errors")
        
        errors = []
        error_taxonomy = defaultdict(list)
        
        for i, (true, pred) in enumerate(zip(self.y_test, self.predictions)):
            if true != pred:
                verse = self.test_verses[i]
                confidence = float(np.max(self.prediction_probas[i]))
                
                # Get top-3 predictions
                top_3_indices = np.argsort(self.prediction_probas[i])[-3:][::-1] + 1
                top_3_probs = sorted(self.prediction_probas[i], reverse=True)[:3]
                top_3 = [(METER_ID_TO_NAME.get(idx, f'{idx}'), float(prob))
                         for idx, prob in zip(top_3_indices, top_3_probs)]
                
                # Find rank of true meter
                ranked_preds = np.argsort(self.prediction_probas[i])[::-1] + 1
                true_rank = int(np.where(ranked_preds == true)[0][0] + 1)
                
                # Categorize error
                if confidence < 0.5:
                    error_type = 'low_confidence'
                elif true_rank <= 3:
                    error_type = 'ambiguous_pattern'
                else:
                    error_type = 'systematic_confusion'
                
                error_case = ErrorCase(
                    verse_id=verse.get('verse_id', f'verse_{i}'),
                    verse_text=verse['text'],
                    true_meter=METER_ID_TO_NAME.get(true, f'{true}'),
                    predicted_meter=METER_ID_TO_NAME.get(pred, f'{pred}'),
                    confidence=confidence,
                    error_type=error_type,
                    true_meter_rank=true_rank,
                    top_3_predictions=top_3
                )
                
                errors.append(error_case)
                error_taxonomy[error_type].append(error_case)
        
        # Print summary
        print(f"\nTotal errors: {len(errors)}")
        for error_type, cases in error_taxonomy.items():
            print(f"  {error_type}: {len(cases)} ({len(cases)/len(errors)*100:.1f}%)")
        
        # Save detailed error log
        errors_data = [asdict(err) for err in errors]
        
        return errors_data, error_taxonomy
        
    def generate_report(self, output_path: str):
        """Generate comprehensive evaluation report."""
        print("\n" + "="*80)
        print("Generating Comprehensive Evaluation Report")
        print("="*80)
        
        report = {
            'dataset': {
                'n_samples': int(len(self.y_test)),
                'n_classes': int(len(np.unique(self.y_test))),
                'class_distribution': {
                    METER_ID_TO_NAME.get(meter_id, f'{meter_id}'): int(count)
                    for meter_id, count in zip(*np.unique(self.y_test, return_counts=True))
                }
            },
            'top_k_accuracy': self.compute_top_k_accuracy(),
            'mrr': self.compute_mrr(),
            'ece': self.compute_ece(),
            'per_meter_metrics': self.compute_per_meter_metrics(),
            'confidence_accuracy_correlation': self.analyze_confidence_accuracy_gap(),
            'overall_accuracy': float(accuracy_score(self.y_test, self.predictions))
        }
        
        # Generate confusion matrix
        self.generate_confusion_matrix()
        
        # Error analysis
        errors, error_taxonomy = self.categorize_errors()
        report['errors'] = errors
        report['error_summary'] = {
            error_type: len(cases)
            for error_type, cases in error_taxonomy.items()
        }
        
        # Save report
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Evaluation report saved to {output_path}")
        
        # Print summary
        print("\n" + "="*80)
        print("EVALUATION SUMMARY")
        print("="*80)
        print(f"Overall Accuracy: {report['overall_accuracy']:.4f}")
        print(f"Top-3 Accuracy: {report['top_k_accuracy']['top_3_accuracy']:.4f}")
        print(f"MRR: {report['mrr']:.4f}")
        print(f"ECE: {report['ece']:.4f}")
        print(f"Confidence-Accuracy Correlation: {report['confidence_accuracy_correlation']:.4f}")
        print("="*80)


def main():
    parser = argparse.ArgumentParser(
        description='Comprehensive evaluation for BAHR meter detection'
    )
    parser.add_argument('--model', default='models/ensemble_v1',
                       help='Directory containing trained ensemble')
    parser.add_argument('--test-data',
                       default='dataset/evaluation/golden_set_v1_3_with_sari.jsonl',
                       help='Test dataset (JSONL format)')
    parser.add_argument('--output',
                       default='ml_pipeline/results/evaluation_report.json',
                       help='Output path for evaluation report')
    
    args = parser.parse_args()
    
    print("="*80)
    print("BAHR Comprehensive Evaluation Suite")
    print("="*80)
    
    evaluator = ComprehensiveEvaluator(args.model)
    evaluator.load_test_data(args.test_data)
    evaluator.predict_with_probabilities()
    evaluator.generate_report(args.output)
    
    print("\n✅ Evaluation complete!")


if __name__ == '__main__':
    main()
