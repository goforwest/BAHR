#!/usr/bin/env python3
"""
Analyze the exact mismatch between text_to_phonetic_pattern and detector cache.
"""

import sys
sys.path.insert(0, '/home/user/BAHR/backend')

from app.core.phonetics import text_to_phonetic_pattern, extract_phonemes
from app.core.prosody.detector_v2 import BahrDetectorV2
from app.core.prosody.meters import get_meter_by_name, METERS_REGISTRY


def analyze_mismatch():
    """Analyze pattern generation differences."""

    print("="*80)
    print("PATTERN MISMATCH ANALYSIS")
    print("="*80)
    print()

    # Example verse - الطويل
    text = "قِفا نَبْكِ مِن ذِكرى حَبيبٍ ومَنْزِلِ"
    expected_meter = "الطويل"

    print(f"Text: {text}")
    print(f"Expected: {expected_meter}")
    print()

    # Extract phonemes
    phonemes = extract_phonemes(text, has_tashkeel=True)
    print(f"Phonemes ({len(phonemes)}):")
    for i, p in enumerate(phonemes):
        print(f"  {i+1}. {p.consonant} + '{p.vowel}' {'(shadda)' if p.has_shadda else ''}")
    print()

    # Convert to pattern
    pattern = text_to_phonetic_pattern(text, has_tashkeel=True)
    print(f"Generated pattern: {pattern}")
    print(f"Pattern length: {len(pattern)}")
    print()

    # Get detector cache patterns
    detector = BahrDetectorV2()
    meter_obj = get_meter_by_name(expected_meter)

    if meter_obj:
        print(f"Meter: {meter_obj.name_ar} (ID {meter_obj.id})")
        print(f"Base tafail: {[t.name for t in meter_obj.base_tafail]}")
        print(f"Base pattern: {meter_obj.base_pattern}")
        print()

        # Show tafail breakdown
        print("Tafail phonetic breakdown:")
        for i, tafila in enumerate(meter_obj.base_tafail, 1):
            print(f"  {i}. {tafila.name} = '{tafila.phonetic}'")
        print()

        # Sample cache patterns
        cache_patterns = list(detector.pattern_cache[meter_obj.id])
        print(f"Cache patterns for {expected_meter}: {len(cache_patterns)} total")
        print("Sample patterns (first 5):")
        for p in cache_patterns[:5]:
            print(f"  '{p}' (len={len(p)})")
        print()

        # Check if generated pattern is in cache
        if pattern in cache_patterns:
            print(f"✅ Generated pattern FOUND in cache!")
        else:
            print(f"❌ Generated pattern NOT in cache")
            print()

            # Find closest matches
            print("Finding closest cache patterns...")
            from difflib import SequenceMatcher

            similarities = []
            for cache_pattern in cache_patterns:
                sim = SequenceMatcher(None, pattern, cache_pattern).ratio()
                similarities.append((cache_pattern, sim))

            similarities.sort(key=lambda x: -x[1])

            print("Top 5 closest matches:")
            for i, (cache_pattern, sim) in enumerate(similarities[:5], 1):
                print(f"  {i}. '{cache_pattern}' (similarity: {sim:.2%})")

            print()
            print("Character-by-character comparison with closest match:")
            closest = similarities[0][0]
            print(f"Generated: {pattern}")
            print(f"Closest:   {closest}")
            print(f"Match:     {''.join('✓' if i < len(closest) and pattern[i] == closest[i] else '✗' for i in range(len(pattern)))}")


if __name__ == '__main__':
    analyze_mismatch()
