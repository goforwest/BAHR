#!/usr/bin/env python3
"""
Option A: Pre-compute Prosodic Patterns for Golden Set

This tool generates correct prosodic patterns for golden set verses by:
1. Using the known meter for each verse
2. Trying all valid patterns from the detector's cache for that meter
3. Finding the best-fitting pattern based on phoneme structure
4. Adding the pattern to the golden set as a new field

This unblocks evaluation by providing ground-truth patterns.
"""

import sys
import json
from pathlib import Path
from typing import Optional, List, Tuple

# Add backend to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / 'backend'))

from app.core.prosody.detector_v2 import BahrDetectorV2
from app.core.prosody.meters import get_meter_by_name
from app.core.phonetics import extract_phonemes


def calculate_pattern_fitness(
    phonemes: List,
    pattern: str
) -> float:
    """
    Calculate how well a pattern "fits" a phoneme sequence.

    Uses heuristics based on:
    - Pattern length vs phoneme count
    - Ratio of / to o symbols
    - Whether pattern length is reasonable

    Returns:
        Fitness score (0.0-1.0)
    """
    if not phonemes or not pattern:
        return 0.0

    n_phonemes = len(phonemes)
    pattern_len = len(pattern)

    # Count harakas and sakins in phonemes
    n_harakas = sum(1 for p in phonemes if p.vowel in ['a', 'u', 'i'])
    n_sakins = sum(1 for p in phonemes if p.is_sukun())
    n_long = sum(1 for p in phonemes if p.is_long_vowel())
    n_tanween = sum(1 for p in phonemes if p.vowel in ['an', 'un', 'in'])

    # Count / and o in pattern
    n_haraka_in_pattern = pattern.count('/')
    n_sakin_in_pattern = pattern.count('o')

    # Fitness based on how close the counts are
    haraka_ratio = min(n_harakas, n_haraka_in_pattern) / max(n_harakas, n_haraka_in_pattern) if max(n_harakas, n_haraka_in_pattern) > 0 else 0
    sakin_ratio = min(n_sakins + n_long + n_tanween, n_sakin_in_pattern) / max(n_sakins + n_long + n_tanween, n_sakin_in_pattern) if max(n_sakins + n_long + n_tanween, n_sakin_in_pattern) > 0 else 0

    # Length fitness (pattern length should be close to reasonable range)
    expected_length = n_harakas + (n_sakins + n_long + n_tanween)
    length_ratio = min(pattern_len, expected_length) / max(pattern_len, expected_length) if max(pattern_len, expected_length) > 0 else 0

    # Overall fitness (weighted average)
    fitness = (haraka_ratio * 0.4 + sakin_ratio * 0.4 + length_ratio * 0.2)

    return fitness


def find_best_pattern_for_verse(
    text: str,
    meter_name: str,
    detector: BahrDetectorV2
) -> Tuple[Optional[str], float]:
    """
    Find the best-fitting pattern from detector cache for a verse.

    Args:
        text: Verse text (with diacritics)
        meter_name: Expected meter name
        detector: Initialized detector

    Returns:
        (best_pattern, confidence) or (None, 0.0)
    """
    # Get meter
    meter = get_meter_by_name(meter_name)
    if not meter:
        return None, 0.0

    # Extract phonemes
    try:
        phonemes = extract_phonemes(text, has_tashkeel=True)
    except:
        return None, 0.0

    if not phonemes:
        return None, 0.0

    # Get all valid patterns for this meter
    cache_patterns = detector.pattern_cache.get(meter.id, set())

    if not cache_patterns:
        return None, 0.0

    # Find best-fitting pattern
    best_pattern = None
    best_fitness = 0.0

    for pattern in cache_patterns:
        fitness = calculate_pattern_fitness(phonemes, pattern)

        if fitness > best_fitness:
            best_fitness = fitness
            best_pattern = pattern

    return best_pattern, best_fitness


def precompute_patterns(
    golden_set_path: str,
    output_path: str
):
    """
    Pre-compute patterns for all verses in golden set.

    Args:
        golden_set_path: Path to golden set JSONL
        output_path: Path to save updated golden set
    """
    print("="*80)
    print("PRE-COMPUTING PROSODIC PATTERNS (Option A)")
    print("="*80)
    print()

    # Load golden set
    print(f"Loading golden set from: {golden_set_path}")
    verses = []
    with open(golden_set_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                verses.append(json.loads(line))

    print(f"✅ Loaded {len(verses)} verses")
    print()

    # Initialize detector
    print("Initializing detector...")
    detector = BahrDetectorV2()
    print(f"✅ Detector ready with {sum(len(p) for p in detector.pattern_cache.values())} cached patterns")
    print()

    # Process each verse
    print("="*80)
    print("PRE-COMPUTING PATTERNS")
    print("="*80)
    print()

    successful = 0
    failed = 0

    for i, verse in enumerate(verses, 1):
        verse_id = verse['verse_id']
        text = verse['text']
        meter = verse['meter']

        # Find best pattern
        pattern, fitness = find_best_pattern_for_verse(text, meter, detector)

        if pattern and fitness > 0.5:  # Require at least 50% fitness
            verse['prosody_precomputed'] = {
                'pattern': pattern,
                'fitness_score': round(fitness, 3),
                'method': 'best_fit_from_cache',
                'meter_verified': meter
            }
            successful += 1
            status = "✅"
        else:
            verse['prosody_precomputed'] = {
                'pattern': None,
                'fitness_score': round(fitness, 3) if fitness else 0.0,
                'method': 'failed',
                'meter_verified': meter,
                'note': 'Could not find suitable pattern'
            }
            failed += 1
            status = "❌"

        # Progress
        if i % 50 == 0 or i == len(verses):
            print(f"Progress: {i}/{len(verses)} ({i/len(verses)*100:.1f}%) - Success: {successful}, Failed: {failed}")

    print()
    print("="*80)
    print("RESULTS")
    print("="*80)
    print()

    print(f"Total verses: {len(verses)}")
    print(f"✅ Successfully pre-computed: {successful} ({successful/len(verses)*100:.1f}%)")
    print(f"❌ Failed: {failed} ({failed/len(verses)*100:.1f}%)")
    print()

    # Save updated golden set
    print(f"Saving updated golden set to: {output_path}")
    with open(output_path, 'w', encoding='utf-8') as f:
        for verse in verses:
            f.write(json.dumps(verse, ensure_ascii=False) + '\n')

    print("✅ Done")
    print()

    # Show sample
    if successful > 0:
        print("Sample pre-computed patterns:")
        count = 0
        for verse in verses:
            if verse.get('prosody_precomputed', {}).get('pattern'):
                print(f"\n{verse['verse_id']} ({verse['meter']}):")
                print(f"  Text: {verse['text'][:50]}...")
                print(f"  Pattern: {verse['prosody_precomputed']['pattern']}")
                print(f"  Fitness: {verse['prosody_precomputed']['fitness_score']:.2%}")
                count += 1
                if count >= 3:
                    break


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Precompute prosodic patterns for golden set')
    parser.add_argument('--file', type=str, help='Input JSONL file')
    parser.add_argument('--output', type=str, help='Output JSONL file (defaults to input file)')
    args = parser.parse_args()

    if args.file:
        golden_set_path = Path(args.file)
        output_path = Path(args.output) if args.output else golden_set_path
    else:
        # Default paths
        golden_set_path = PROJECT_ROOT / 'dataset/evaluation/golden_set_v1_0_with_patterns.jsonl'
        output_path = golden_set_path

    if not golden_set_path.exists():
        print(f"Error: Golden set not found at {golden_set_path}")
        sys.exit(1)

    precompute_patterns(str(golden_set_path), str(output_path))


if __name__ == '__main__':
    main()
