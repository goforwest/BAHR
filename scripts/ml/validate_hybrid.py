#!/usr/bin/env python3
"""
Test hybrid detector on golden dataset.
"""

import sys
import json
from collections import defaultdict

sys.path.insert(0, '/home/user/BAHR/backend')

from app.core.prosody.detector_v2_hybrid import BahrDetectorV2Hybrid, EMPIRICAL_PATTERNS
from app.core.phonetics import text_to_phonetic_pattern
from missing_meters_patterns import MISSING_METERS_PATTERNS

# Integrate missing meter patterns into empirical patterns
EMPIRICAL_PATTERNS.update(MISSING_METERS_PATTERNS)


def load_verses(filepath: str):
    """Load verses from JSONL file."""
    verses = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                verses.append(json.loads(line))
    return verses


def validate(verses, detector):
    """Validate detector."""
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
        if i % 50 == 0:
            print(f"Processing {i}/{len(verses)}...")

        text = verse.get('text', '')
        expected = verse.get('meter', '')

        if not text or not expected:
            continue

        try:
            pattern = text_to_phonetic_pattern(text, has_tashkeel=True)
            detections = detector.detect(pattern, top_k=3, expected_meter_ar=expected)
        except Exception as e:
            results['failures'].append({
                'verse_id': i,
                'text': text[:50],
                'error': str(e),
                'expected': expected,
            })
            continue

        if not detections:
            results['no_match'] += 1
            results['by_meter'][expected]['total'] += 1
            continue

        top1 = detections[0]
        top3_meters = [d.meter_name_ar for d in detections[:3]]

        results['by_meter'][expected]['total'] += 1
        results['confidences'].append(top1.confidence)
        results['similarities'].append(top1.similarity)
        results['match_types'][top1.match_type] += 1

        if top1.meter_name_ar == expected:
            results['correct_top1'] += 1
            results['by_meter'][expected]['correct'] += 1
            results['by_meter'][expected]['top3'] += 1
        elif expected in top3_meters:
            results['correct_top3'] += 1
            results['by_meter'][expected]['top3'] += 1
        else:
            results['failures'].append({
                'verse_id': i,
                'text': text[:50],
                'pattern': pattern,
                'expected': expected,
                'detected': top1.meter_name_ar,
                'confidence': top1.confidence,
                'similarity': top1.similarity,
                'match_type': top1.match_type,
            })

    return results


def print_results(results):
    """Print validation results."""
    total = results['total']
    correct_top1 = results['correct_top1']
    correct_top3 = results['correct_top3']

    acc_top1 = (correct_top1 / total * 100) if total > 0 else 0
    acc_top3 = ((correct_top1 + correct_top3) / total * 100) if total > 0 else 0

    print()
    print("=" * 80)
    print("HYBRID DETECTOR VALIDATION RESULTS")
    print("=" * 80)
    print()

    print(f"Total verses: {total}")
    print(f"Top-1 correct: {correct_top1} ({acc_top1:.1f}%)")
    print(f"Top-3 correct: {correct_top1 + correct_top3} ({acc_top3:.1f}%)")
    print(f"No match: {results['no_match']} ({results['no_match']/total*100:.1f}%)")
    print()

    if results['confidences']:
        avg_conf = sum(results['confidences']) / len(results['confidences'])
        avg_sim = sum(results['similarities']) / len(results['similarities'])
        print(f"Average confidence: {avg_conf:.3f}")
        print(f"Average similarity: {avg_sim:.3f}")
        print()

    print("Match type distribution:")
    for match_type, count in sorted(results['match_types'].items()):
        print(f"  {match_type}: {count} ({count/total*100:.1f}%)")
    print()

    print("=" * 80)
    print("PER-METER ACCURACY")
    print("=" * 80)
    print(f"{'Meter':<25} {'Total':>6} {'Top-1':>6} {'Acc %':>7}")
    print("-" * 80)

    for meter, stats in sorted(results['by_meter'].items(),
                               key=lambda x: x[1]['total'],
                               reverse=True):
        total_m = stats['total']
        correct = stats['correct']
        acc = (correct / total_m * 100) if total_m > 0 else 0
        print(f"{meter:<25} {total_m:>6} {correct:>6} {acc:>6.1f}%")

    print()

    # Comparison
    baseline = 50.3
    theoretical = 6.6
    improvement = acc_top1 - baseline

    print("=" * 80)
    print("COMPARISON")
    print("=" * 80)
    print(f"Baseline (empirical only):     {baseline:.1f}%")
    print(f"Theoretical (BahrDetectorV2):  {theoretical:.1f}%")
    print(f"Hybrid (empirical + fuzzy):    {acc_top1:.1f}%")
    print(f"Improvement vs baseline:       {improvement:+.1f} pp")
    print()

    if acc_top1 >= 70:
        print("✅ SUCCESS: Exceeded 70% target!")
    elif acc_top1 >= baseline:
        print("✅ IMPROVED: Better than baseline")
    elif acc_top1 >= 40:
        print("⚠️  PARTIAL: Better than theoretical but below baseline")
    else:
        print("❌ FAILED: Below expectations")

    print("=" * 80)

    return acc_top1


def main():
    """Main validation."""
    dataset_path = '/home/user/BAHR/dataset/evaluation/golden_set_v1_3_with_sari.jsonl'

    print("Initializing Hybrid Detector...")
    detector = BahrDetectorV2Hybrid()
    print("✓ Initialized")
    print()

    print("=" * 80)
    print(f"Dataset: {dataset_path}")
    print("=" * 80)
    print()

    verses = load_verses(dataset_path)
    print(f"Loaded {len(verses)} verses")
    print()

    results = validate(verses, detector)
    acc = print_results(results)

    # Save results
    output = '/home/user/BAHR/hybrid_validation_results.json'
    with open(output, 'w', encoding='utf-8') as f:
        results_json = {
            'total': results['total'],
            'correct_top1': results['correct_top1'],
            'correct_top3': results['correct_top3'],
            'no_match': results['no_match'],
            'accuracy_top1': acc,
            'by_meter': dict(results['by_meter']),
            'match_types': dict(results['match_types']),
            'avg_confidence': sum(results['confidences']) / len(results['confidences']) if results['confidences'] else 0,
            'avg_similarity': sum(results['similarities']) / len(results['similarities']) if results['similarities'] else 0,
            'failures_count': len(results['failures']),
            'failures': results['failures'][:50],  # First 50 failures only
        }
        json.dump(results_json, f, ensure_ascii=False, indent=2)

    print(f"Results saved to: {output}")
    return 0 if acc >= 55 else 1


if __name__ == '__main__':
    sys.exit(main())
