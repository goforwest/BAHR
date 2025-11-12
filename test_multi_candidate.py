#!/usr/bin/env python3
"""
Quick test script for multi-candidate meter detection.
Tests the Mu'allaqah verse to verify alternative meters are shown.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.schemas.analyze import AnalyzeRequest
from app.core.normalization import normalize_arabic_text, has_diacritics
from app.core.prosody.detector_v2 import BahrDetectorV2
from app.core.prosody.phoneme_based_detector import detect_with_phoneme_fitness
from app.core.prosody.meters import METERS_REGISTRY

def test_multi_candidate():
    """Test multi-candidate detection with Mu'allaqah verse."""

    # Test verse: Imru' al-Qais Mu'allaqah (famous, should show الطويل vs الرجز)
    test_verse = "قفا نبك من ذكرى حبيب ومنزل"

    print("=" * 70)
    print("MULTI-CANDIDATE METER DETECTION TEST")
    print("=" * 70)
    print(f"\nTest Verse: {test_verse}")
    print(f"Expected: Should show الرجز and الطويل as close alternatives")
    print()

    # Normalize
    normalized = normalize_arabic_text(
        test_verse,
        remove_tashkeel=False,
        normalize_hamzas=True,
        normalize_alefs=True
    )

    has_tashkeel = has_diacritics(normalized)
    print(f"Has diacritics: {has_tashkeel}")
    print()

    # Initialize detector
    detector = BahrDetectorV2()

    # Get top 3 candidates
    print("Getting top 3 candidates using hybrid detection...")
    all_candidates = detect_with_phoneme_fitness(
        normalized,
        has_tashkeel,
        detector,
        top_k=3,
        use_hybrid_scoring=True
    )

    print(f"\nFound {len(all_candidates)} candidates:")
    print("-" * 70)

    for i, (meter_id, name_ar, score, pattern) in enumerate(all_candidates, 1):
        meter = METERS_REGISTRY.get(meter_id)
        name_en = meter.name_en if meter else "Unknown"
        freq_rank = meter.frequency_rank if meter else "?"

        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉"
        print(f"{medal} #{i}: {name_ar} ({name_en})")
        print(f"   Confidence: {score:.2%}")
        print(f"   Frequency Rank: {freq_rank}")
        print(f"   Pattern: {pattern[:40]}...")
        print()

    # Check uncertainty conditions
    print("=" * 70)
    print("UNCERTAINTY ANALYSIS")
    print("=" * 70)

    if len(all_candidates) >= 1:
        top_confidence = all_candidates[0][2]
        print(f"\nTop confidence: {top_confidence:.2%}")

        is_uncertain = False
        reason = None

        if top_confidence < 0.90:
            is_uncertain = True
            reason = "low_confidence"
            print(f"✓ UNCERTAIN: Low confidence ({top_confidence:.2%} < 90%)")
        else:
            print(f"✗ Not low confidence ({top_confidence:.2%} >= 90%)")

        if len(all_candidates) >= 2:
            top_diff = all_candidates[0][2] - all_candidates[1][2]
            print(f"\nTop 2 difference: {top_diff:.2%}")

            # Updated logic: very close race OR moderately close + not high confidence
            if top_diff < 0.02 or (top_diff < 0.05 and top_confidence < 0.97):
                is_uncertain = True
                reason = "close_candidates"
                if top_diff < 0.02:
                    print(f"✓ UNCERTAIN: Very close race (diff={top_diff:.2%} < 2%)")
                else:
                    print(f"✓ UNCERTAIN: Close candidates (diff={top_diff:.2%} < 5% and confidence < 97%)")
            else:
                print(f"✗ Not close candidates (diff={top_diff:.2%} >= 2% and (diff >= 5% or confidence >= 97%))")

        print()
        if is_uncertain:
            print(f"🎯 RESULT: Detection is UNCERTAIN (reason: {reason})")
            print(f"   → Should show {len(all_candidates) - 1} alternative meter(s) to user")
            print(f"   → Alternatives: {', '.join(c[1] for c in all_candidates[1:])}")
        else:
            print(f"🎯 RESULT: Detection is CERTAIN")
            print(f"   → Should show only top candidate: {all_candidates[0][1]}")

    print("\n" + "=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    test_multi_candidate()
