#!/usr/bin/env python3
"""
Run full dataset augmentation using prosodic augmentation engine.

Expected result: 471 verses → ~1,012 verses (2.1x augmentation)
"""

import sys
import json
from pathlib import Path
from collections import Counter

sys.path.insert(0, 'backend')

from app.ml.prosodic_augmenter import ProsodicAugmenter


def load_golden_dataset(filepath):
    """Load golden dataset JSONL."""
    verses = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                verses.append(json.loads(line))
    return verses


def save_augmented_dataset(dataset, filepath):
    """Save augmented dataset to JSONL."""
    with open(filepath, 'w', encoding='utf-8') as f:
        for item in dataset:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')


def main():
    print("=" * 80)
    print("Full Dataset Augmentation")
    print("=" * 80)
    print()

    # Load golden dataset
    golden_path = 'dataset/evaluation/golden_set_v1_3_with_sari.jsonl'
    if not Path(golden_path).exists():
        print(f"❌ ERROR: Golden dataset not found at {golden_path}")
        sys.exit(1)

    print(f"Loading golden dataset from: {golden_path}")
    verses = load_golden_dataset(golden_path)
    print(f"✅ Loaded {len(verses)} verses")
    print()

    # Load augmentation priorities
    priorities_path = 'augmentation_priorities.json'
    if not Path(priorities_path).exists():
        print(f"❌ ERROR: Augmentation priorities not found at {priorities_path}")
        print("   Run analyze_dataset_distribution.py first!")
        sys.exit(1)

    with open(priorities_path, 'r', encoding='utf-8') as f:
        priorities_list = json.load(f)

    # Convert to dict keyed by meter name
    priorities = {}
    for item in priorities_list:
        priorities[item['meter']] = item

    print(f"✅ Loaded augmentation priorities for {len(priorities)} meters")
    print()

    # Prepare dataset for augmentation
    dataset = []
    for verse in verses:
        text = verse.get('text', '')
        meter = verse.get('meter', '')
        if text and meter:
            dataset.append((text, meter))

    print(f"Prepared {len(dataset)} verses for augmentation")
    print()

    # Run augmentation
    print("=" * 80)
    print("Running Prosodic Augmentation")
    print("=" * 80)
    print()

    augmenter = ProsodicAugmenter()
    augmented_dataset = augmenter.augment_dataset(dataset, priorities)

    print()
    print("=" * 80)
    print("Augmentation Complete!")
    print("=" * 80)
    print()

    # Statistics
    original_count = len(dataset)
    augmented_count = len(augmented_dataset)
    new_verses = augmented_count - original_count

    print(f"Original dataset: {original_count} verses")
    print(f"Augmented dataset: {augmented_count} verses")
    print(f"New verses generated: {new_verses}")
    print(f"Augmentation factor: {augmented_count / original_count:.2f}x")
    print()

    # Per-meter breakdown
    original_meters = Counter(meter for text, meter in dataset)
    augmented_meters = Counter(meter for text, meter in augmented_dataset)

    print("Per-Meter Augmentation:")
    print("-" * 80)
    print(f"{'Meter':<25} {'Original':<10} {'Augmented':<10} {'New':<10} {'Factor':<10}")
    print("-" * 80)

    for meter in sorted(original_meters.keys()):
        orig = original_meters[meter]
        aug = augmented_meters[meter]
        new = aug - orig
        factor = aug / orig if orig > 0 else 0

        print(f"{meter:<25} {orig:<10} {aug:<10} {new:<10} {factor:<10.2f}x")

    print("-" * 80)
    print()

    # Save augmented dataset
    print("Saving augmented dataset...")

    # Convert back to JSONL format with all original fields
    augmented_verses = []
    verse_lookup = {(v.get('text', ''), v.get('meter', '')): v for v in verses}

    for text, meter in augmented_dataset:
        # Check if this is an original verse
        if (text, meter) in verse_lookup:
            # Keep original verse with all fields
            augmented_verses.append(verse_lookup[(text, meter)])
        else:
            # New augmented verse - create minimal entry
            augmented_verses.append({
                'text': text,
                'meter': meter,
                'source': 'augmented',
                'original': False
            })

    output_path = 'dataset/augmented_golden_set.jsonl'
    save_augmented_dataset(augmented_verses, output_path)

    print(f"✅ Saved {len(augmented_verses)} verses to {output_path}")
    print()

    # Summary
    print("=" * 80)
    print("AUGMENTATION SUMMARY")
    print("=" * 80)
    print(f"✅ Dataset expanded: {original_count} → {augmented_count} verses")
    print(f"✅ New verses: {new_verses} ({100*new_verses/augmented_count:.1f}% of total)")
    print(f"✅ Augmentation factor: {augmented_count/original_count:.2f}x")
    print()
    print(f"Next steps:")
    print(f"1. Extract features from augmented dataset")
    print(f"2. Retrain RandomForest with best hyperparameters")
    print(f"3. Validate on original test set (target: 73-76% accuracy)")
    print()


if __name__ == '__main__':
    main()
