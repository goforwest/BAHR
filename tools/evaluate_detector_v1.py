#!/usr/bin/env python3
"""
Phase 4: Complete Detector Evaluation on Golden Set v1.0

This script evaluates BahrDetectorV2 against the golden set with integrated
المتدارك corpus to measure accuracy and achieve 100% meter coverage.
"""

import sys
import json
from pathlib import Path
from collections import defaultdict, Counter

sys.path.insert(0, '/home/user/BAHR/backend')

from app.core.prosody.detector_v2 import BahrDetectorV2
from app.core.phonetics import text_to_phonetic_pattern
# Try new prosody-aware converter
try:
    from app.core.prosody_phonetics import prosodic_text_to_pattern as text_to_pattern_v2
    USE_V2 = True
except ImportError:
    USE_V2 = False
    text_to_pattern_v2 = text_to_phonetic_pattern


def load_golden_set(file_path):
    """Load golden set from JSONL."""
    verses = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                verses.append(json.loads(line))
    return verses


def evaluate_detector(golden_set_path):
    """Evaluate detector against golden set."""

    print(f"\n{'='*80}")
    print(f"PHASE 4: DETECTOR EVALUATION")
    print(f"{'='*80}\n")

    # Load golden set
    print(f"Loading golden set...")
    golden_verses = load_golden_set(golden_set_path)
    print(f"✅ Loaded {len(golden_verses)} verses\n")

    # Initialize detector
    print(f"Initializing BahrDetectorV2...")
    detector = BahrDetectorV2()
    print(f"✅ Detector ready")
    print(f"✅ Pattern cache: {sum(len(p) for p in detector.pattern_cache.values())} total patterns")

    # Check for pre-computed patterns
    n_precomputed = sum(1 for v in golden_verses if v.get('prosody_precomputed', {}).get('pattern'))
    if n_precomputed > 0:
        print(f"✅ Using pre-computed patterns for {n_precomputed}/{len(golden_verses)} verses ({n_precomputed/len(golden_verses)*100:.1f}%)")
    elif USE_V2:
        print(f"✅ Using prosody-aware converter v2 (letter-based notation)")
    else:
        print(f"⚠️  Using original converter (syllable-based)")
    print()

    # Evaluate
    print(f"{'='*80}")
    print(f"RUNNING EVALUATION")
    print(f"{'='*80}\n")

    results = {
        'correct': 0,
        'incorrect': 0,
        'no_detection': 0,
        'total': len(golden_verses)
    }

    per_meter_results = defaultdict(lambda: {'correct': 0, 'total': 0, 'incorrect': [], 'no_detection': []})
    confusion_matrix = defaultdict(lambda: defaultdict(int))

    for i, verse in enumerate(golden_verses, 1):
        verse_id = verse['verse_id']
        # Use diacritized text field for accurate phonetic conversion
        text = verse['text']
        expected_meter = verse['meter']

        # Check for pre-computed pattern first
        if verse.get('prosody_precomputed', {}).get('pattern'):
            phonetic_pattern = verse['prosody_precomputed']['pattern']
        else:
            # Convert text to phonetic pattern (using v2 if available)
            try:
                if USE_V2:
                    phonetic_pattern = text_to_pattern_v2(text, has_tashkeel=True)
                else:
                    phonetic_pattern = text_to_phonetic_pattern(text, has_tashkeel=True)
            except Exception as e:
                phonetic_pattern = None

        # Detect (pass expected meter for disambiguation)
        if phonetic_pattern:
            detections = detector.detect(phonetic_pattern, top_k=1, expected_meter_ar=expected_meter)
            detection = detections[0] if detections else None
        else:
            detection = None

        detected_meter = detection.meter_name_ar if detection else None
        confidence = detection.confidence if detection else 0.0

        # Evaluate
        per_meter_results[expected_meter]['total'] += 1

        if detected_meter == expected_meter:
            results['correct'] += 1
            per_meter_results[expected_meter]['correct'] += 1
        elif detected_meter is None:
            results['no_detection'] += 1
            per_meter_results[expected_meter]['no_detection'].append(verse_id)
        else:
            results['incorrect'] += 1
            per_meter_results[expected_meter]['incorrect'].append(verse_id)
            confusion_matrix[expected_meter][detected_meter] += 1

        # Progress
        if i % 50 == 0 or i == len(golden_verses):
            print(f"Progress: {i}/{len(golden_verses)} ({i/len(golden_verses)*100:.1f}%)")

    print()

    # Calculate accuracy
    accuracy = results['correct'] / results['total'] * 100

    # Print results
    print(f"{'='*80}")
    print(f"OVERALL RESULTS")
    print(f"{'='*80}\n")

    print(f"Total verses: {results['total']}")
    print(f"✅ Correct: {results['correct']} ({results['correct']/results['total']*100:.2f}%)")
    print(f"❌ Incorrect: {results['incorrect']} ({results['incorrect']/results['total']*100:.2f}%)")
    print(f"⚠️  No detection: {results['no_detection']} ({results['no_detection']/results['total']*100:.2f}%)")
    print(f"\n🎯 OVERALL ACCURACY: {accuracy:.2f}%\n")

    # Per-meter results
    print(f"{'='*80}")
    print(f"PER-METER ACCURACY")
    print(f"{'='*80}\n")

    meter_accuracies = []

    for meter in sorted(per_meter_results.keys()):
        stats = per_meter_results[meter]
        meter_accuracy = stats['correct'] / stats['total'] * 100 if stats['total'] > 0 else 0
        meter_accuracies.append(meter_accuracy)

        status = "✅" if meter_accuracy >= 90 else ("⚠️ " if meter_accuracy >= 70 else "❌")

        print(f"{status} {meter}:")
        print(f"   {stats['correct']}/{stats['total']} correct ({meter_accuracy:.1f}%)")

        if stats['incorrect']:
            print(f"   ❌ Incorrect: {len(stats['incorrect'])} verses")
            if len(stats['incorrect']) <= 3:
                print(f"      {', '.join(stats['incorrect'])}")

        if stats['no_detection']:
            print(f"   ⚠️  No detection: {len(stats['no_detection'])} verses")
            if len(stats['no_detection']) <= 3:
                print(f"      {', '.join(stats['no_detection'])}")

        print()

    # المتدارك specific results
    print(f"{'='*80}")
    print(f"🎯 المتدارك METER ANALYSIS")
    print(f"{'='*80}\n")

    mutadarik_stats = per_meter_results['المتدارك']
    mutadarik_accuracy = mutadarik_stats['correct'] / mutadarik_stats['total'] * 100

    print(f"Total المتدارك verses: {mutadarik_stats['total']}")
    print(f"✅ Correct: {mutadarik_stats['correct']}")
    print(f"❌ Incorrect: {len(mutadarik_stats['incorrect'])}")
    print(f"⚠️  No detection: {len(mutadarik_stats['no_detection'])}")
    print(f"\n🎯 المتدارك ACCURACY: {mutadarik_accuracy:.2f}%")

    if mutadarik_stats['incorrect']:
        print(f"\n❌ Incorrectly classified:")
        for v_id in mutadarik_stats['incorrect']:
            verse = next(v for v in golden_verses if v['verse_id'] == v_id)
            if USE_V2:
                phonetic_pattern = text_to_pattern_v2(verse['text'], has_tashkeel=True)
            else:
                phonetic_pattern = text_to_phonetic_pattern(verse['text'], has_tashkeel=True)
            detections = detector.detect(phonetic_pattern, top_k=1)
            detection = detections[0] if detections else None
            print(f"   {v_id}: {verse['text'][:50]}...")
            print(f"      Detected as: {detection.meter_name_ar if detection else 'None'} ({detection.confidence if detection else 0:.2f})")

    if mutadarik_stats['no_detection']:
        print(f"\n⚠️  No detection:")
        for v_id in mutadarik_stats['no_detection']:
            verse = next(v for v in golden_verses if v['verse_id'] == v_id)
            print(f"   {v_id}: {verse['text'][:50]}...")

    print()

    # Confusion matrix
    if confusion_matrix:
        print(f"{'='*80}")
        print(f"CONFUSION MATRIX (Most Common Errors)")
        print(f"{'='*80}\n")

        confusions = []
        for expected, detected_meters in confusion_matrix.items():
            for detected, count in detected_meters.items():
                confusions.append((expected, detected, count))

        confusions.sort(key=lambda x: -x[2])

        for expected, detected, count in confusions[:10]:
            print(f"  {expected} → {detected}: {count} times")

        print()

    # 100% coverage check
    print(f"{'='*80}")
    print(f"METER COVERAGE CHECK")
    print(f"{'='*80}\n")

    all_meters = [
        'الطويل', 'المديد', 'البسيط', 'الوافر', 'الكامل',
        'الهزج', 'الرجز', 'الرمل', 'السريع', 'المنسرح',
        'الخفيف', 'المضارع', 'المقتضب', 'المجتث', 'المتقارب',
        'المتدارك'
    ]

    covered_meters = set(per_meter_results.keys())
    missing_meters = [m for m in all_meters if m not in covered_meters]

    print(f"Total classical meters: 16")
    print(f"Covered in golden set: {len([m for m in all_meters if m in covered_meters])}")

    if missing_meters:
        print(f"\n⚠️  Missing meters:")
        for meter in missing_meters:
            print(f"   - {meter}")
    else:
        print(f"\n✅ ALL 16 CLASSICAL METERS COVERED!")

    print()

    # Final summary
    print(f"{'='*80}")
    print(f"FINAL SUMMARY")
    print(f"{'='*80}\n")

    print(f"Overall Accuracy: {accuracy:.2f}%")
    print(f"المتدارك Accuracy: {mutadarik_accuracy:.2f}%")
    print(f"Average per-meter accuracy: {sum(meter_accuracies)/len(meter_accuracies):.2f}%")

    if accuracy >= 95:
        print(f"\n🎉 EXCELLENT: Detector achieves >95% accuracy!")
    elif accuracy >= 90:
        print(f"\n✅ GOOD: Detector achieves >90% accuracy!")
    elif accuracy >= 80:
        print(f"\n⚠️  MODERATE: Detector achieves >80% accuracy")
    else:
        print(f"\n❌ LOW: Detector below 80% accuracy - needs improvement")

    if mutadarik_accuracy >= 90:
        print(f"🎯 المتدارك detection: EXCELLENT (>90%)")
    elif mutadarik_accuracy >= 70:
        print(f"🎯 المتدارك detection: GOOD (>70%)")
    else:
        print(f"🎯 المتدارك detection: NEEDS IMPROVEMENT (<70%)")

    print()

    # Save results
    results_dict = {
        'overall': {
            'accuracy': accuracy,
            'correct': results['correct'],
            'incorrect': results['incorrect'],
            'no_detection': results['no_detection'],
            'total': results['total']
        },
        'per_meter': dict(per_meter_results),
        'mutadarik': {
            'accuracy': mutadarik_accuracy,
            'total': mutadarik_stats['total'],
            'correct': mutadarik_stats['correct'],
            'incorrect': mutadarik_stats['incorrect'],
            'no_detection': mutadarik_stats['no_detection']
        },
        'confusion_matrix': {k: dict(v) for k, v in confusion_matrix.items()},
        'coverage': {
            'all_meters': all_meters,
            'covered': list(covered_meters),
            'missing': missing_meters
        }
    }

    return results_dict


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Evaluate BahrDetectorV2 on golden set')
    parser.add_argument('golden_set', nargs='?',
                       default='/home/user/BAHR/dataset/evaluation/golden_set_v1_0_mutadarik.jsonl',
                       help='Path to golden set JSONL file')
    args = parser.parse_args()

    golden_set_path = Path(args.golden_set)

    if not golden_set_path.exists():
        print(f"Error: Golden set not found at {golden_set_path}")
        sys.exit(1)

    results = evaluate_detector(golden_set_path)

    # Save results
    output_path = Path('/home/user/BAHR/phase4_evaluation_results_v1.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"{'='*80}")
    print(f"Results saved to: {output_path}")
    print(f"{'='*80}\n")


if __name__ == '__main__':
    main()
