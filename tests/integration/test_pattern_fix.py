#!/usr/bin/env python3
"""
Test script to verify that المتدارك patterns now include classical notation.
"""

import sys
sys.path.insert(0, '/home/user/BAHR/backend')

from app.core.prosody.detector_v2 import BahrDetectorV2

def test_mutadarik_patterns():
    """Check if المتدارك patterns include classical notation."""

    print("=" * 80)
    print("Testing المتدارك Pattern Generation Fix")
    print("=" * 80)

    detector = BahrDetectorV2()

    # Get المتدارك meter ID (16)
    mutadarik_id = 16

    # Get all patterns for المتدارك
    if mutadarik_id in detector.pattern_cache:
        patterns = detector.pattern_cache[mutadarik_id]
        print(f"\n✅ المتدارك patterns found: {len(patterns)} patterns")

        # Check for classical notation patterns
        classical_patterns = [
            "///o///o///o///o",  # All positions with khabn (letter-based)
            "///o///o///o///",   # With final حذف
            "/o//o///o///o///o", # Mixed notation
        ]

        print("\n🔍 Checking for classical notation patterns:")
        print("-" * 80)

        for pattern in classical_patterns:
            if pattern in patterns:
                print(f"✅ FOUND: {pattern}")
            else:
                print(f"❌ MISSING: {pattern}")

        # Show first 10 patterns for inspection
        print("\n📋 First 10 المتدارك patterns:")
        print("-" * 80)
        for i, pattern in enumerate(sorted(patterns)[:10], 1):
            print(f"{i:2d}. {pattern}")

        # Count patterns with /// sequence (letter-based notation)
        letter_based = [p for p in patterns if "///" in p]
        print(f"\n📊 Patterns with letter-based notation (///): {len(letter_based)}/{len(patterns)}")

        if letter_based:
            print("\n✨ Sample letter-based patterns:")
            for pattern in sorted(letter_based)[:5]:
                print(f"   {pattern}")

        return len(patterns), len(letter_based)
    else:
        print(f"\n❌ ERROR: المتدارك (ID {mutadarik_id}) not found in pattern cache")
        return 0, 0

if __name__ == "__main__":
    total, letter_based = test_mutadarik_patterns()

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total المتدارك patterns: {total}")
    print(f"Letter-based patterns: {letter_based}")

    if letter_based > 0:
        print("\n✅ SUCCESS: Classical notation support added!")
    else:
        print("\n⚠️  WARNING: No letter-based patterns found. May need to regenerate pattern cache.")
