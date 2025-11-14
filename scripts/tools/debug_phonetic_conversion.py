#!/usr/bin/env python3
"""
Debug script to understand why phonetic conversion is failing.
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, '/home/user/BAHR/backend')

from app.core.phonetics import text_to_phonetic_pattern
from app.core.prosody.detector_v2 import BahrDetectorV2
from app.core.prosody.meters import get_meter_by_name


def test_phonetic_conversion():
    """Test phonetic conversion on sample verses."""

    # Load a few verses from golden set
    golden_set_path = Path('/home/user/BAHR/dataset/evaluation/golden_set_v1_0_mutadarik.jsonl')

    verses = []
    with open(golden_set_path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i < 10:  # First 10 verses
                verses.append(json.loads(line.strip()))
            else:
                break

    print(f"{'='*80}")
    print(f"PHONETIC CONVERSION DEBUG")
    print(f"{'='*80}\n")

    # Initialize detector
    detector = BahrDetectorV2()

    for verse in verses:
        verse_id = verse['verse_id']
        # Use diacritized text
        text = verse['text']
        expected_meter = verse['meter']

        print(f"Verse: {verse_id}")
        print(f"Text: {text[:60]}...")
        print(f"Expected meter: {expected_meter}")

        # Try conversion
        try:
            phonetic_pattern = text_to_phonetic_pattern(text, has_tashkeel=True)
            print(f"✅ Phonetic pattern: {phonetic_pattern}")

            # Try detection
            detections = detector.detect(phonetic_pattern, top_k=3)

            if detections:
                print(f"✅ Detections found: {len(detections)}")
                for i, det in enumerate(detections[:3], 1):
                    print(f"   {i}. {det.meter_name_ar} ({det.confidence:.2f})")
            else:
                print(f"❌ No detections")

                # Check if pattern exists in cache
                print(f"   Checking cache for pattern...")
                found_in_cache = False
                for meter_id, patterns in detector.pattern_cache.items():
                    if phonetic_pattern in patterns:
                        meter_obj = detector.meters.get(meter_id)
                        meter_name = meter_obj.name_ar if meter_obj else f"ID {meter_id}"
                        print(f"   ✅ Pattern EXISTS in cache for: {meter_name}")
                        found_in_cache = True
                        break

                if not found_in_cache:
                    print(f"   ❌ Pattern NOT in cache")

                    # Get expected meter ID
                    expected_meter_obj = get_meter_by_name(expected_meter)
                    if expected_meter_obj:
                        print(f"   Sample cache patterns for {expected_meter} (ID {expected_meter_obj.id}):")
                        sample_patterns = list(detector.pattern_cache[expected_meter_obj.id])[:3]
                        for p in sample_patterns:
                            print(f"      {p}")
                    else:
                        print(f"   ⚠️ Meter {expected_meter} not found in registry")

        except Exception as e:
            print(f"❌ Conversion failed: {e}")

        print()


if __name__ == '__main__':
    test_phonetic_conversion()
