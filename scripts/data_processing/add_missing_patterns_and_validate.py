#!/usr/bin/env python3
"""
Add missing empirical patterns to detector and validate accuracy.

Expected result: 41.2% → 50%+ accuracy
"""

import sys
import json
from pathlib import Path

# Import the missing patterns
from missing_meters_patterns import MISSING_METERS_PATTERNS

sys.path.insert(0, 'backend')

# Import detector
from app.core.prosody.detector_v2_hybrid import BahrDetectorV2Hybrid, EMPIRICAL_PATTERNS

def main():
    print("=" * 80)
    print("Adding Missing Empirical Patterns & Validating")
    print("=" * 80)
    print()

    # Show before state
    print(f"BEFORE: EMPIRICAL_PATTERNS has {len(EMPIRICAL_PATTERNS)} meters")
    print()

    # Add missing patterns
    print("Adding 7 missing meters...")
    EMPIRICAL_PATTERNS.update(MISSING_METERS_PATTERNS)
    print(f"AFTER: EMPIRICAL_PATTERNS has {len(EMPIRICAL_PATTERNS)} meters")
    print()

    # Show what was added
    print("Added meters:")
    for meter_id in sorted(MISSING_METERS_PATTERNS.keys()):
        data = MISSING_METERS_PATTERNS[meter_id]
        print(f"  {meter_id:2}: {data['name_ar']:20} ({len(data['patterns'])} patterns)")
    print()

    # Now run validation
    print("=" * 80)
    print("Running Golden Dataset Validation")
    print("=" * 80)
    print()

    # Load golden dataset
    golden_path = 'dataset/evaluation/golden_set_v1_3_with_sari.jsonl'
    if not Path(golden_path).exists():
        print(f"❌ ERROR: Golden dataset not found at {golden_path}")
        sys.exit(1)

    verses = []
    with open(golden_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                verses.append(json.loads(line))

    print(f"✅ Loaded {len(verses)} verses from golden dataset")
    print()

    # Create detector
    detector = BahrDetectorV2Hybrid()

    # Validate
    correct = 0
    total = len(verses)

    for i, verse in enumerate(verses, 1):
        text = verse.get('text', '')
        expected_meter = verse.get('meter', '')

        if not text or not expected_meter:
            continue

        try:
            result = detector.detect(text)
            detected = result.get('meter', '')

            if detected == expected_meter:
                correct += 1

            if i % 50 == 0:
                print(f"  Progress: {i}/{total} verses ({correct}/{i} correct = {100*correct/i:.1f}%)")

        except Exception as e:
            print(f"  ⚠️  Error on verse {i}: {e}")

    accuracy = 100 * correct / total
    print()
    print("=" * 80)
    print("VALIDATION RESULTS")
    print("=" * 80)
    print(f"Total verses: {total}")
    print(f"Correct: {correct}")
    print(f"Accuracy: {accuracy:.1f}%")
    print()
    print(f"Baseline (Phase 2): 50.3%")
    print(f"Before fix: 41.2%")
    print(f"After fix: {accuracy:.1f}%")
    print()

    if accuracy >= 50.0:
        print("✅ SUCCESS: Accuracy restored to ≥50% baseline!")
    elif accuracy >= 45.0:
        print("⚠️  PARTIAL: Significant improvement but below 50% target")
    else:
        print("❌ ISSUE: Accuracy still below 45%")

    print()

if __name__ == '__main__':
    main()
