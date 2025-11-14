#!/usr/bin/env python3
"""Debug specific verses to see detector predictions."""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / 'backend'))

from app.core.prosody.detector_v2 import BahrDetectorV2

def debug_verse(text, expected_meter, pattern):
    """Debug a single verse."""
    print(f"\nText: {text}")
    print(f"Expected: {expected_meter}")
    print(f"Pattern: {pattern}")

    detector = BahrDetectorV2()
    results = detector.detect(pattern)

    print(f"\nDetector results:")
    for i, result in enumerate(results[:5], 1):
        print(f"  {i}. {result.meter_name_ar} (confidence: {result.confidence:.2%})")

    if results and results[0].meter_name_ar == expected_meter:
        print(f"✅ CORRECT")
    else:
        print(f"❌ INCORRECT - detected as '{results[0].meter_name_ar if results else 'NO_DETECTION'}'")

# Test the two error verses
print("="*80)
print("DEBUGGING ERROR VERSES")
print("="*80)

debug_verse(
    "بَكَيْتُ عَلَى الشَّبَابِ بِدَمْعِ عَيْنِي",
    "السريع",
    "/o/o//o/o///o/o//o"
)

print("\n" + "="*80)

debug_verse(
    "لَا تَسْأَلِ الْمَرْءَ عَنْ خُلْقِهِ",
    "السريع (مفعولات)",
    "/o/o//o/o///o/o//"
)
