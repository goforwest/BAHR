#!/usr/bin/env python3
"""
Full golden dataset validation with updated BahrDetectorV2.

Tests the new fuzzy matching + hemistich support against all 471 verses.
"""

import sys
import json
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, '/home/user/BAHR/backend')

from app.core.prosody.detector_v2 import BahrDetectorV2
from app.core.phonetics import text_to_phonetic_pattern


def load_golden_dataset(filepath: str):
    """Load golden dataset from JSONL file."""
    verses = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                verses.append(json.loads(line))
    return verses


def validate_dataset(dataset_path: str, detector: BahrDetectorV2):
    """Validate detector against golden dataset."""

    verses = load_golden_dataset(dataset_path)

    print("=" * 80)
    print(f"Golden Dataset Validation - Updated BahrDetectorV2 v2.1")
    print("=" * 80)
    print(f"Dataset: {dataset_path}")
    print(f"Total verses: {len(verses)}")
    print()

    results = {
        'total': len(verses),
        'correct_top1': 0,
        'correct_top3': 0,
        'no_match': 0,
        'by_meter': defaultdict(lambda: {'total': 0, 'correct': 0, 'top3': 0}),
        'failures': [],
        'confidences': [],
        'similarities': [],
        'match_types': defaultdict(int),
    }

    for i, verse in enumerate(verses, 1):
        # Progress indicator
        if i % 50 == 0:
            print(f"Processing verse {i}/{len(verses)}...")

        text = verse.get('text', verse.get('original', ''))
        expected_meter = verse.get('meter', verse.get('meter_ar', verse.get('bahr', '')))

        if not text or not expected_meter:
            continue

        # Extract phonetic pattern
        try:
            pattern = text_to_phonetic_pattern(text, has_tashkeel=True)
        except Exception as e:
            results['failures'].append({
                'verse_id': i,
                'text': text[:50],
                'error': f'Pattern extraction failed: {e}',
                'expected': expected_meter,
            })
            continue

        # Detect meter
        try:
            detections = detector.detect(pattern, top_k=3, expected_meter_ar=expected_meter)
        except Exception as e:
            results['failures'].append({
                'verse_id': i,
                'text': text[:50],
                'error': f'Detection failed: {e}',
                'expected': expected_meter,
            })
            continue

        # Check results
        if not detections:
            results['no_match'] += 1
            results['failures'].append({
                'verse_id': i,
                'text': text[:50],
                'pattern': pattern,
                'expected': expected_meter,
                'detected': 'NO_MATCH',
                'confidence': 0.0,
            })
            results['by_meter'][expected_meter]['total'] += 1
            continue

        top1 = detections[0]
        top3_meters = [d.meter_name_ar for d in detections[:3]]

        # Track statistics
        results['by_meter'][expected_meter]['total'] += 1
        results['confidences'].append(top1.confidence)
        results['similarities'].append(top1.similarity)
        results['match_types'][top1.match_type] += 1

        # Check if correct
        if top1.meter_name_ar == expected_meter:
            results['correct_top1'] += 1
            results['by_meter'][expected_meter]['correct'] += 1
            results['by_meter'][expected_meter]['top3'] += 1
        elif expected_meter in top3_meters:
            results['correct_top3'] += 1
            results['by_meter'][expected_meter]['top3'] += 1
            results['failures'].append({
                'verse_id': i,
                'text': text[:50],
                'pattern': pattern,
                'expected': expected_meter,
                'detected': top1.meter_name_ar,
                'confidence': top1.confidence,
                'similarity': top1.similarity,
                'match_type': top1.match_type,
                'top3': top3_meters,
            })
        else:
            results['failures'].append({
                'verse_id': i,
                'text': text[:50],
                'pattern': pattern,
                'expected': expected_meter,
                'detected': top1.meter_name_ar,
                'confidence': top1.confidence,
                'similarity': top1.similarity,
                'match_type': top1.match_type,
                'top3': top3_meters,
            })

    return results


def print_results(results):
    """Print validation results."""

    total = results['total']
    correct_top1 = results['correct_top1']
    correct_top3 = results['correct_top3']
    no_match = results['no_match']

    accuracy_top1 = (correct_top1 / total * 100) if total > 0 else 0
    accuracy_top3 = ((correct_top1 + correct_top3) / total * 100) if total > 0 else 0

    print()
    print("=" * 80)
    print("VALIDATION RESULTS")
    print("=" * 80)
    print()

    print(f"Total verses: {total}")
    print(f"Top-1 correct: {correct_top1} ({accuracy_top1:.1f}%)")
    print(f"Top-3 correct: {correct_top1 + correct_top3} ({accuracy_top3:.1f}%)")
    print(f"No match found: {no_match} ({no_match/total*100:.1f}%)")
    print()

    # Confidence statistics
    if results['confidences']:
        avg_confidence = sum(results['confidences']) / len(results['confidences'])
        avg_similarity = sum(results['similarities']) / len(results['similarities'])
        print(f"Average confidence: {avg_confidence:.3f}")
        print(f"Average similarity: {avg_similarity:.3f}")
        print()

    # Match type distribution
    print("Match type distribution:")
    for match_type, count in sorted(results['match_types'].items()):
        print(f"  {match_type}: {count} ({count/total*100:.1f}%)")
    print()

    # Per-meter results
    print("=" * 80)
    print("PER-METER ACCURACY")
    print("=" * 80)
    print(f"{'Meter':<25} {'Total':>6} {'Top-1':>6} {'Top-3':>6} {'Acc %':>7}")
    print("-" * 80)

    for meter, stats in sorted(results['by_meter'].items(),
                               key=lambda x: x[1]['total'],
                               reverse=True):
        total_meter = stats['total']
        correct = stats['correct']
        top3 = stats['top3']
        acc = (correct / total_meter * 100) if total_meter > 0 else 0
        print(f"{meter:<25} {total_meter:>6} {correct:>6} {top3:>6} {acc:>6.1f}%")

    print()

    # Show some failure examples
    if results['failures']:
        print("=" * 80)
        print(f"FAILURE EXAMPLES (showing first 10 of {len(results['failures'])})")
        print("=" * 80)

        for failure in results['failures'][:10]:
            print(f"\nVerse #{failure['verse_id']}:")
            print(f"  Text: {failure['text']}...")
            print(f"  Expected: {failure['expected']}")
            print(f"  Detected: {failure.get('detected', 'NO_MATCH')}")
            if 'confidence' in failure:
                print(f"  Confidence: {failure['confidence']:.3f}")
            if 'similarity' in failure:
                print(f"  Similarity: {failure['similarity']:.3f}")
            if 'top3' in failure:
                print(f"  Top-3: {', '.join(failure['top3'])}")

    print()
    print("=" * 80)

    return accuracy_top1, accuracy_top3


def main():
    """Main validation function."""

    dataset_path = '/home/user/BAHR/dataset/evaluation/golden_set_v1_3_with_sari.jsonl'

    print("Initializing BahrDetectorV2...")
    detector = BahrDetectorV2()
    print("✓ Detector initialized")
    print()

    # Run validation
    results = validate_dataset(dataset_path, detector)

    # Print results
    acc_top1, acc_top3 = print_results(results)

    # Save results to file
    output_file = '/home/user/BAHR/golden_dataset_validation_results.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        # Convert defaultdict to dict for JSON serialization
        results_serializable = {
            'total': results['total'],
            'correct_top1': results['correct_top1'],
            'correct_top3': results['correct_top3'],
            'no_match': results['no_match'],
            'accuracy_top1': acc_top1,
            'accuracy_top3': acc_top3,
            'by_meter': dict(results['by_meter']),
            'match_types': dict(results['match_types']),
            'avg_confidence': sum(results['confidences']) / len(results['confidences']) if results['confidences'] else 0,
            'avg_similarity': sum(results['similarities']) / len(results['similarities']) if results['similarities'] else 0,
            'failures': results['failures'],
        }
        json.dump(results_serializable, f, ensure_ascii=False, indent=2)

    print(f"Results saved to: {output_file}")
    print()

    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Top-1 Accuracy: {acc_top1:.1f}%")
    print(f"Top-3 Accuracy: {acc_top3:.1f}%")
    print(f"Improvement target: ≥70% (from baseline 50.3%)")

    if acc_top1 >= 70:
        print("✅ SUCCESS: Target accuracy achieved!")
    elif acc_top1 >= 60:
        print("⚠️  CLOSE: Near target accuracy")
    else:
        print("❌ BELOW TARGET: Further improvements needed")

    print("=" * 80)

    return 0 if acc_top1 >= 70 else 1


if __name__ == '__main__':
    sys.exit(main())
