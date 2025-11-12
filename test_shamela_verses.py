#!/usr/bin/env python3
"""
Test Shamela verses against updated المتدارك patterns.
"""

import sys
import json
sys.path.insert(0, '/home/user/BAHR/backend')

from app.core.prosody.detector_v2 import BahrDetectorV2

def test_shamela_verses():
    """Test all 6 Shamela verses with updated patterns."""

    print("=" * 80)
    print("Testing Shamela المتدارك Verses with Updated Patterns")
    print("=" * 80)

    detector = BahrDetectorV2()

    # Load verses from JSONL
    verses = []
    with open('/home/user/BAHR/dataset/mutadarik_shamela_candidates.jsonl', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                verses.append(json.loads(line))

    passed = 0
    failed = 0

    for verse in verses:
        verse_id = verse['verse_id']
        text = verse['normalized_text']
        expected_pattern = verse.get('phonetic_pattern', 'N/A')
        verse_num = verse_id.split('_')[-1]

        print(f"\n{'=' * 80}")
        print(f"Verse {verse_num}: {verse_id}")
        print(f"{'=' * 80}")
        print(f"Text: {text}")
        print(f"Expected pattern: {expected_pattern}")
        print(f"Source: {verse.get('source', 'N/A')}")

        # Check if pattern exists in المتدارك patterns
        mutadarik_patterns = detector.pattern_cache.get(16, set())

        if expected_pattern in mutadarik_patterns:
            print(f"\n✅ PASS: Pattern found in المتدارك patterns")
            passed += 1

            # Try detection
            result = detector.detect(text)
            if result and result.meter_name == "المتدارك":
                print(f"✅ Detection confirmed: {result.meter_name} (confidence: {result.confidence:.2f})")
            else:
                detected = result.meter_name if result else "NONE"
                conf = result.confidence if result else 0.0
                print(f"⚠️  Detection mismatch: {detected} (confidence: {conf:.2f})")
        else:
            print(f"\n❌ FAIL: Pattern NOT found in المتدارك patterns")
            failed += 1

            # Try detection anyway
            result = detector.detect(text)
            if result:
                print(f"🔍 Detected as: {result.meter_name} (confidence: {result.confidence:.2f})")
                print(f"   Pattern: {result.matched_pattern}")
            else:
                print(f"🔍 No meter detected")

        # Show notes
        notes = verse.get('notes', '')
        if notes:
            print(f"\n📝 Notes: {notes}")

    print(f"\n{'=' * 80}")
    print(f"RESULTS SUMMARY")
    print(f"{'=' * 80}")
    print(f"✅ PASSED: {passed}/6 verses ({passed/6*100:.1f}%)")
    print(f"❌ FAILED: {failed}/6 verses ({failed/6*100:.1f}%)")

    if passed >= 4:
        print(f"\n🎉 SUCCESS: {passed} verses now validate correctly!")
    elif passed > 0:
        print(f"\n⚡ PROGRESS: {passed} verses now pass (was 0/6 before fix)")
    else:
        print(f"\n⚠️  WARNING: No verses passed. Further investigation needed.")

    return passed, failed

if __name__ == "__main__":
    test_shamela_verses()
