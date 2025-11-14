#!/usr/bin/env python3
"""
BAHR ML Pipeline - Phase 7: AraBERT Transfer Learning

Fine-tunes aubmindlab/bert-base-arabertv2 for 16-way meter classification.

Features:
- Frozen early layers (preserve Arabic language knowledge)
- Fine-tuning of final layers
- Early stopping and checkpointing
- Learning rate warmup and decay
- Class-weighted loss for imbalanced data

Usage:
    python ml_pipeline/arabert_finetuner.py \
        --data dataset/evaluation/golden_set_v1_3_with_sari.jsonl \
        --output models/arabert_v1 \
        --epochs 10 \
        --batch-size 16
"""

import sys
import json
import argparse
import numpy as np
import pandas as pd
from pathlib import Path
from typing import List, Dict, Tuple
from dataclasses import dataclass
from collections import Counter

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader, random_split
from transformers import (
    AutoTokenizer, 
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
    EarlyStoppingCallback
)
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, classification_report
from sklearn.model_selection import train_test_split

# Meter mapping
METER_NAME_TO_ID = {
    'الطويل': 0, 'الكامل': 1, 'الوافر': 2, 'الرمل': 3,
    'البسيط': 4, 'المتقارب': 5, 'الرجز': 6, 'السريع': 7,
    'المديد': 8, 'المنسرح': 9, 'الهزج': 10, 'الخفيف': 11,
    'المجتث': 12, 'المقتضب': 13, 'المضارع': 14, 'المتدارك': 15,
}

METER_ID_TO_NAME = {v: k for k, v in METER_NAME_TO_ID.items()}


class VerseDataset(Dataset):
    """Dataset for verse meter classification."""
    
    def __init__(self, texts: List[str], labels: List[int], tokenizer, max_length=128):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length
        
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self, idx):
        text = self.texts[idx]
        label = self.labels[idx]
        
        # Tokenize
        encoding = self.tokenizer(
            text,
            add_special_tokens=True,
            max_length=self.max_length,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(label, dtype=torch.long)
        }


class AraBERTFineTuner:
    """
    Fine-tune AraBERT for meter classification.
    
    Implements transfer learning with frozen early layers,
    learning rate scheduling, and early stopping.
    """
    
    def __init__(
        self,
        model_name: str = 'aubmindlab/bert-base-arabertv2',
        num_labels: int = 16,
        freeze_layers: int = 8,
        max_length: int = 128,
        device: str = None
    ):
        """
        Initialize AraBERT fine-tuner.
        
        Args:
            model_name: Hugging Face model identifier
            num_labels: Number of meter classes
            freeze_layers: Number of BERT layers to freeze (0-12)
            max_length: Maximum sequence length
            device: Device to use ('cuda', 'mps', 'cpu')
        """
        self.model_name = model_name
        self.num_labels = num_labels
        self.freeze_layers = freeze_layers
        self.max_length = max_length
        
        # Determine device
        if device is None:
            if torch.cuda.is_available():
                self.device = 'cuda'
            else:
                # Use CPU for stability with transformers (MPS support is experimental)
                self.device = 'cpu'
        else:
            self.device = device
            
        print(f"Using device: {self.device}")
        
        # Load tokenizer and model
        print(f"Loading {model_name}...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_name,
            num_labels=num_labels,
            ignore_mismatched_sizes=True
        )
        
        # Freeze early layers
        if freeze_layers > 0:
            print(f"Freezing first {freeze_layers} layers...")
            for i, layer in enumerate(self.model.bert.encoder.layer):
                if i < freeze_layers:
                    for param in layer.parameters():
                        param.requires_grad = False
        
        # Count trainable parameters
        trainable_params = sum(p.numel() for p in self.model.parameters() if p.requires_grad)
        total_params = sum(p.numel() for p in self.model.parameters())
        print(f"Trainable parameters: {trainable_params:,} / {total_params:,} ({100*trainable_params/total_params:.1f}%)")
        
    def load_data(self, data_path: str, val_split: float = 0.2, test_split: float = 0.1):
        """
        Load and split dataset.
        
        Args:
            data_path: Path to JSONL dataset
            val_split: Fraction for validation
            test_split: Fraction for testing
        """
        print(f"\nLoading data from {data_path}")
        
        # Load verses
        verses = []
        with open(data_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    data = json.loads(line)
                    meter_name = data.get('meter', '')
                    if meter_name in METER_NAME_TO_ID:
                        verses.append({
                            'text': data['text'],
                            'meter_id': METER_NAME_TO_ID[meter_name],
                            'meter_name': meter_name
                        })
        
        print(f"✅ Loaded {len(verses)} verses")
        
        # Class distribution
        meter_counts = Counter([v['meter_id'] for v in verses])
        print("\nClass distribution:")
        for meter_id in sorted(meter_counts.keys()):
            meter_name = METER_ID_TO_NAME[meter_id]
            count = meter_counts[meter_id]
            print(f"  {meter_name}: {count} verses")
        
        # Split data
        texts = [v['text'] for v in verses]
        labels = [v['meter_id'] for v in verses]
        
        # Train/temp split
        train_texts, temp_texts, train_labels, temp_labels = train_test_split(
            texts, labels, 
            test_size=(val_split + test_split),
            random_state=42,
            stratify=labels
        )
        
        # Val/test split
        val_size = val_split / (val_split + test_split)
        val_texts, test_texts, val_labels, test_labels = train_test_split(
            temp_texts, temp_labels,
            test_size=(1 - val_size),
            random_state=42,
            stratify=temp_labels
        )
        
        print(f"\nDataset splits:")
        print(f"  Train: {len(train_texts)} verses")
        print(f"  Val:   {len(val_texts)} verses")
        print(f"  Test:  {len(test_texts)} verses")
        
        # Create datasets
        self.train_dataset = VerseDataset(train_texts, train_labels, self.tokenizer, self.max_length)
        self.val_dataset = VerseDataset(val_texts, val_labels, self.tokenizer, self.max_length)
        self.test_dataset = VerseDataset(test_texts, test_labels, self.tokenizer, self.max_length)
        
        # Calculate class weights for imbalanced data
        label_counts = np.bincount(train_labels, minlength=self.num_labels)
        # Avoid division by zero
        label_counts = np.where(label_counts == 0, 1, label_counts)
        self.class_weights = torch.FloatTensor(len(train_labels) / (self.num_labels * label_counts))
        
        print(f"\nClass weights (for imbalanced classes): min={self.class_weights.min():.2f}, max={self.class_weights.max():.2f}")
        
    def compute_metrics(self, eval_pred):
        """Compute metrics for evaluation."""
        predictions, labels = eval_pred
        predictions = np.argmax(predictions, axis=1)
        
        # Accuracy
        accuracy = accuracy_score(labels, predictions)
        
        # Precision, Recall, F1 (weighted average)
        precision, recall, f1, _ = precision_recall_fscore_support(
            labels, predictions, average='weighted', zero_division=0
        )
        
        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1': f1
        }
    
    def train(
        self,
        output_dir: str,
        epochs: int = 10,
        batch_size: int = 16,
        learning_rate: float = 2e-5,
        warmup_ratio: float = 0.1,
        weight_decay: float = 0.01,
        early_stopping_patience: int = 3,
        save_total_limit: int = 2
    ):
        """
        Train the model.
        
        Args:
            output_dir: Directory to save checkpoints
            epochs: Number of training epochs
            batch_size: Training batch size
            learning_rate: Peak learning rate
            warmup_ratio: Warmup ratio for learning rate scheduler
            weight_decay: L2 regularization
            early_stopping_patience: Patience for early stopping
            save_total_limit: Maximum number of checkpoints to keep
        """
        print("\n" + "="*80)
        print("Training AraBERT for Meter Classification")
        print("="*80)
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Training arguments
        training_args = TrainingArguments(
            output_dir=str(output_path),
            eval_strategy='epoch',
            save_strategy='epoch',
            learning_rate=learning_rate,
            per_device_train_batch_size=batch_size,
            per_device_eval_batch_size=batch_size,
            num_train_epochs=epochs,
            weight_decay=weight_decay,
            warmup_ratio=warmup_ratio,
            logging_dir=str(output_path / 'logs'),
            logging_steps=10,
            load_best_model_at_end=True,
            metric_for_best_model='accuracy',
            save_total_limit=save_total_limit,
            fp16=False,  # Disable for MPS
            use_cpu=(self.device == 'cpu'),  # Force CPU if not using GPU
            dataloader_num_workers=0,  # For MPS compatibility
            report_to='none',  # Disable wandb/tensorboard
            remove_unused_columns=False,
        )
        
        # Custom trainer with class weights
        class WeightedTrainer(Trainer):
            def compute_loss(self, model, inputs, return_outputs=False, **kwargs):
                labels = inputs.pop("labels")
                outputs = model(**inputs)
                logits = outputs.logits
                
                # Apply class weights
                loss_fct = nn.CrossEntropyLoss(weight=self.class_weights.to(logits.device))
                loss = loss_fct(logits, labels)
                
                return (loss, outputs) if return_outputs else loss
        
        # Initialize trainer
        trainer = WeightedTrainer(
            model=self.model,
            args=training_args,
            train_dataset=self.train_dataset,
            eval_dataset=self.val_dataset,
            compute_metrics=self.compute_metrics,
            callbacks=[EarlyStoppingCallback(early_stopping_patience=early_stopping_patience)]
        )
        
        # Add class weights to trainer
        trainer.class_weights = self.class_weights
        
        # Train
        print("\nStarting training...")
        train_result = trainer.train()
        
        # Save final model
        trainer.save_model(str(output_path / 'final_model'))
        self.tokenizer.save_pretrained(str(output_path / 'final_model'))
        
        # Training summary
        print("\n" + "="*80)
        print("Training Complete")
        print("="*80)
        print(f"Total steps: {train_result.global_step}")
        print(f"Training loss: {train_result.training_loss:.4f}")
        
        # Save training metadata
        metadata = {
            'model_name': self.model_name,
            'num_labels': self.num_labels,
            'freeze_layers': self.freeze_layers,
            'max_length': self.max_length,
            'train_samples': len(self.train_dataset),
            'val_samples': len(self.val_dataset),
            'test_samples': len(self.test_dataset),
            'training_args': {
                'epochs': epochs,
                'batch_size': batch_size,
                'learning_rate': learning_rate,
                'warmup_ratio': warmup_ratio,
                'weight_decay': weight_decay
            },
            'training_result': {
                'global_step': train_result.global_step,
                'training_loss': float(train_result.training_loss)
            }
        }
        
        with open(output_path / 'training_metadata.json', 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Model saved to {output_path / 'final_model'}")
        
        return trainer
    
    def evaluate(self, trainer, output_dir: str):
        """
        Evaluate on test set.
        
        Args:
            trainer: Trained Trainer object
            output_dir: Directory to save evaluation results
        """
        print("\n" + "="*80)
        print("Evaluating on Test Set")
        print("="*80)
        
        # Evaluate
        test_results = trainer.evaluate(self.test_dataset)
        
        print(f"\nTest Results:")
        print(f"  Accuracy:  {test_results['eval_accuracy']:.4f}")
        print(f"  Precision: {test_results['eval_precision']:.4f}")
        print(f"  Recall:    {test_results['eval_recall']:.4f}")
        print(f"  F1 Score:  {test_results['eval_f1']:.4f}")
        
        # Get predictions for detailed analysis
        predictions = trainer.predict(self.test_dataset)
        pred_labels = np.argmax(predictions.predictions, axis=1)
        true_labels = predictions.label_ids
        
        # Per-meter performance
        print("\nPer-Meter Performance:")
        report = classification_report(
            true_labels,
            pred_labels,
            target_names=[METER_ID_TO_NAME[i] for i in range(self.num_labels)],
            zero_division=0
        )
        print(report)
        
        # Save evaluation results
        output_path = Path(output_dir)
        eval_results = {
            'test_metrics': {
                'accuracy': float(test_results['eval_accuracy']),
                'precision': float(test_results['eval_precision']),
                'recall': float(test_results['eval_recall']),
                'f1': float(test_results['eval_f1'])
            },
            'classification_report': report
        }
        
        with open(output_path / 'test_results.json', 'w', encoding='utf-8') as f:
            json.dump(eval_results, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Evaluation results saved to {output_path / 'test_results.json'}")
        
        return test_results


def main():
    parser = argparse.ArgumentParser(
        description='Fine-tune AraBERT for Arabic meter classification'
    )
    parser.add_argument('--data', 
                       default='dataset/evaluation/golden_set_v1_3_with_sari.jsonl',
                       help='Path to dataset (JSONL format)')
    parser.add_argument('--output', 
                       default='models/arabert_v1',
                       help='Output directory for model')
    parser.add_argument('--model-name',
                       default='aubmindlab/bert-base-arabertv2',
                       help='Hugging Face model name')
    parser.add_argument('--freeze-layers',
                       type=int,
                       default=8,
                       help='Number of BERT layers to freeze (0-12)')
    parser.add_argument('--epochs',
                       type=int,
                       default=10,
                       help='Number of training epochs')
    parser.add_argument('--batch-size',
                       type=int,
                       default=16,
                       help='Training batch size')
    parser.add_argument('--learning-rate',
                       type=float,
                       default=2e-5,
                       help='Learning rate')
    parser.add_argument('--max-length',
                       type=int,
                       default=128,
                       help='Maximum sequence length')
    parser.add_argument('--val-split',
                       type=float,
                       default=0.2,
                       help='Validation split ratio')
    parser.add_argument('--test-split',
                       type=float,
                       default=0.1,
                       help='Test split ratio')
    
    args = parser.parse_args()
    
    # Initialize fine-tuner
    finetuner = AraBERTFineTuner(
        model_name=args.model_name,
        num_labels=16,
        freeze_layers=args.freeze_layers,
        max_length=args.max_length
    )
    
    # Load data
    finetuner.load_data(
        args.data,
        val_split=args.val_split,
        test_split=args.test_split
    )
    
    # Train
    trainer = finetuner.train(
        output_dir=args.output,
        epochs=args.epochs,
        batch_size=args.batch_size,
        learning_rate=args.learning_rate
    )
    
    # Evaluate
    finetuner.evaluate(trainer, args.output)
    
    print("\n" + "="*80)
    print("✅ AraBERT Fine-Tuning Complete!")
    print("="*80)


if __name__ == '__main__':
    main()
