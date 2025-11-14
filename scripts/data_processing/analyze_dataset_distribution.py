#!/usr/bin/env python3
"""
Analyze golden dataset distribution to identify augmentation priorities.
"""

import sys
import json
from collections import Counter
from pathlib import Path

sys.path.insert(0, 'backend')

def load_golden_dataset(filepath):
    """Load golden dataset."""
    verses = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                verses.append(json.loads(line))
    return verses

def analyze_distribution(verses):
    """Analyze meter distribution."""
    # Count meters
    meter_counts = Counter(v.get('meter', '') for v in verses)

    # Sort by frequency
    sorted_meters = sorted(meter_counts.items(), key=lambda x: x[1], reverse=True)

    print("=" * 80)
    print("Golden Dataset Distribution Analysis")
    print("=" * 80)
    print()

    total = len(verses)
    print(f"Total verses: {total}")
    print(f"Unique meters: {len(meter_counts)}")
    print()

    print("Meter Distribution:")
    print("-" * 80)
    print(f"{'Rank':<6} {'Meter':<25} {'Count':<8} {'%':<8} {'Priority':<10}")
    print("-" * 80)

    priorities = []
    for rank, (meter, count) in enumerate(sorted_meters, 1):
        percentage = 100 * count / total

        # Determine augmentation priority
        if count < 20:
            priority = "CRITICAL"
            aug_factor = 3.0  # Triple the data
        elif count < 25:
            priority = "HIGH"
            aug_factor = 2.5
        elif count < 30:
            priority = "MEDIUM"
            aug_factor = 2.0
        else:
            priority = "LOW"
            aug_factor = 1.5

        priorities.append({
            'meter': meter,
            'count': count,
            'priority': priority,
            'aug_factor': aug_factor,
            'target_count': int(count * aug_factor)
        })

        print(f"{rank:<6} {meter:<25} {count:<8} {percentage:>6.1f}%  {priority:<10}")

    print("-" * 80)
    print()

    # Summary
    critical = [p for p in priorities if p['priority'] == 'CRITICAL']
    high = [p for p in priorities if p['priority'] == 'HIGH']
    medium = [p for p in priorities if p['priority'] == 'MEDIUM']
    low = [p for p in priorities if p['priority'] == 'LOW']

    print("Augmentation Strategy:")
    print("-" * 80)
    print(f"CRITICAL (< 20 verses): {len(critical)} meters → 3x augmentation")
    for p in critical:
        print(f"  - {p['meter']}: {p['count']} → {p['target_count']} verses")
    print()

    print(f"HIGH (20-24 verses): {len(high)} meters → 2.5x augmentation")
    for p in high:
        print(f"  - {p['meter']}: {p['count']} → {p['target_count']} verses")
    print()

    print(f"MEDIUM (25-29 verses): {len(medium)} meters → 2x augmentation")
    for p in medium:
        print(f"  - {p['meter']}: {p['count']} → {p['target_count']} verses")
    print()

    print(f"LOW (≥30 verses): {len(low)} meters → 1.5x augmentation")
    for p in low:
        print(f"  - {p['meter']}: {p['count']} → {p['target_count']} verses")
    print()

    # Total projection
    original_total = sum(p['count'] for p in priorities)
    augmented_total = sum(p['target_count'] for p in priorities)

    print("=" * 80)
    print(f"Original dataset size: {original_total} verses")
    print(f"Augmented dataset size: {augmented_total} verses")
    print(f"Augmentation factor: {augmented_total / original_total:.1f}x")
    print(f"Expected accuracy gain: +5-8 pp (68% → 73-76%)")
    print("=" * 80)
    print()

    # Save priorities for augmentation script
    with open('augmentation_priorities.json', 'w', encoding='utf-8') as f:
        json.dump(priorities, f, ensure_ascii=False, indent=2)

    print("✅ Saved augmentation priorities to augmentation_priorities.json")

def main():
    golden_path = 'dataset/evaluation/golden_set_v1_3_with_sari.jsonl'

    if not Path(golden_path).exists():
        print(f"❌ ERROR: Golden dataset not found at {golden_path}")
        return

    verses = load_golden_dataset(golden_path)
    analyze_distribution(verses)

if __name__ == '__main__':
    main()
