#!/usr/bin/env python3
"""
Diagnose why specific meters have low detection accuracy.

This tool analyzes:
1. المتدارك (15.8%) - المتقارب confusion
2. المقتضب (0%) - no detection
3. الخفيف (38.5%) - الرجز/الرمل confusion
4. الكامل (3 تفاعيل) (20%) - الرجز confusion
5. المجتث (66.7%) - no detection cases
"""

import sys
import json
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, '/home/user/BAHR/backend')

from app.core.prosody.detector_v2 import BahrDetectorV2
from app.core.prosody.meters import get_meter_by_name
from app.core.phonetics import extract_phonemes


def load_golden_set(file_path):
    """Load golden set from JSONL."""
    verses = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                verses.append(json.loads(line))
    return verses


def analyze_meter_issues(meter_name, golden_set_path):
    """Analyze detection issues for a specific meter."""
    print(f"\n{'='*80}")
    print(f"DIAGNOSING: {meter_name}")
    print(f"{'='*80}\n")

    # Load golden set
    golden_verses = load_golden_set(golden_set_path)

    # Filter for this meter
    meter_verses = [v for v in golden_verses if v['meter'] == meter_name]

    print(f"Total {meter_name} verses: {len(meter_verses)}")
    print()

    # Initialize detector
    detector = BahrDetectorV2()
    meter_obj = get_meter_by_name(meter_name)

    # Analyze each verse
    results = {
        'correct': [],
        'confused': defaultdict(list),
        'no_detection': []
    }

    for verse in meter_verses:
        verse_id = verse['verse_id']
        text = verse['text']

        # Check for pre-computed pattern
        if verse.get('prosody_precomputed', {}).get('pattern'):
            pattern = verse['prosody_precomputed']['pattern']
            source = 'precomputed'
        else:
            # No pattern available
            print(f"⚠️  {verse_id}: No pre-computed pattern")
            continue

        # Detect
        detections = detector.detect(pattern, top_k=5)

        if not detections:
            results['no_detection'].append({
                'verse_id': verse_id,
                'text': text[:60],
                'pattern': pattern,
                'phonemes': extract_phonemes(text, has_tashkeel=True)
            })
        elif detections[0].meter_name_ar == meter_name:
            results['correct'].append({
                'verse_id': verse_id,
                'confidence': detections[0].confidence
            })
        else:
            # Confused
            detected_meter = detections[0].meter_name_ar
            results['confused'][detected_meter].append({
                'verse_id': verse_id,
                'text': text[:60],
                'detected_meter': detected_meter,
                'confidence': detections[0].confidence,
                'pattern': pattern,
                'top_5': [(d.meter_name_ar, d.confidence) for d in detections[:5]]
            })

    # Report
    print(f"✅ Correct: {len(results['correct'])}/{len(meter_verses)}")
    print(f"❌ Confused: {sum(len(v) for v in results['confused'].values())}/{len(meter_verses)}")
    print(f"⚠️  No detection: {len(results['no_detection'])}/{len(meter_verses)}")
    print()

    # Confusion details
    if results['confused']:
        print("CONFUSION BREAKDOWN:")
        for confused_meter, verses in sorted(results['confused'].items(), key=lambda x: -len(x[1])):
            print(f"\n  {meter_name} → {confused_meter}: {len(verses)} times")
            for v in verses[:3]:  # Show first 3
                print(f"    {v['verse_id']}: {v['text']}...")
                print(f"      Pattern: {v['pattern']}")
                print(f"      Confidence: {v['confidence']:.3f}")
                print(f"      Top 5: {v['top_5']}")

    # No detection details
    if results['no_detection']:
        print("\nNO DETECTION CASES:")
        for v in results['no_detection']:
            print(f"\n  {v['verse_id']}: {v['text']}...")
            print(f"    Pattern: {v['pattern']}")
            print(f"    Pattern length: {len(v['pattern'])}")
            print(f"    Phoneme count: {len(v['phonemes'])}")

            # Check if pattern exists in cache
            cache_patterns = detector.pattern_cache.get(meter_obj.id, set())
            pattern_in_cache = v['pattern'] in cache_patterns
            print(f"    Pattern in cache: {pattern_in_cache}")

            if not pattern_in_cache:
                # Find closest patterns in cache
                pattern_len = len(v['pattern'])
                similar_patterns = [p for p in cache_patterns if abs(len(p) - pattern_len) <= 2]
                print(f"    Similar length patterns in cache: {len(similar_patterns)}/{len(cache_patterns)}")
                if similar_patterns:
                    print(f"    Example: {list(similar_patterns)[:3]}")

    print()
    return results


def analyze_pattern_overlap(meter1_name, meter2_name, detector):
    """Analyze pattern overlap between two meters."""
    print(f"\n{'='*80}")
    print(f"PATTERN OVERLAP ANALYSIS: {meter1_name} vs {meter2_name}")
    print(f"{'='*80}\n")

    meter1 = get_meter_by_name(meter1_name)
    meter2 = get_meter_by_name(meter2_name)

    patterns1 = detector.pattern_cache.get(meter1.id, set())
    patterns2 = detector.pattern_cache.get(meter2.id, set())

    overlap = patterns1 & patterns2

    print(f"{meter1_name} patterns: {len(patterns1)}")
    print(f"{meter2_name} patterns: {len(patterns2)}")
    print(f"Overlap: {len(overlap)} patterns ({len(overlap)/min(len(patterns1), len(patterns2))*100:.1f}%)")

    if overlap:
        print(f"\nShared patterns (first 10):")
        for pattern in list(overlap)[:10]:
            print(f"  {pattern}")

    print()
    return overlap


def main():
    golden_set_path = Path('/home/user/BAHR/dataset/evaluation/golden_set_v1_0_with_patterns.jsonl')

    print("\n" + "="*80)
    print("PROBLEMATIC METERS DIAGNOSTIC TOOL")
    print("="*80)

    # Initialize detector
    detector = BahrDetectorV2()

    # Analyze each problematic meter
    problematic_meters = [
        'المتدارك',
        'المقتضب',
        'الخفيف',
        'الكامل (3 تفاعيل)',
        'المجتث'
    ]

    results = {}
    for meter in problematic_meters:
        results[meter] = analyze_meter_issues(meter, golden_set_path)

    # Analyze pattern overlaps for confused pairs
    print("\n" + "="*80)
    print("PATTERN OVERLAP ANALYSIS")
    print("="*80)

    # المتدارك vs المتقارب
    analyze_pattern_overlap('المتدارك', 'المتقارب', detector)

    # الخفيف vs الرجز
    analyze_pattern_overlap('الخفيف', 'الرجز', detector)

    # الخفيف vs الرمل
    analyze_pattern_overlap('الخفيف', 'الرمل', detector)

    # الكامل (3 تفاعيل) vs الرجز
    analyze_pattern_overlap('الكامل (3 تفاعيل)', 'الرجز', detector)

    # Save results
    output_path = Path('/home/user/BAHR/problematic_meters_diagnosis.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False, default=str)

    print(f"\n{'='*80}")
    print(f"Diagnosis saved to: {output_path}")
    print(f"{'='*80}\n")


if __name__ == '__main__':
    main()
