#!/usr/bin/env python
"""
Manual test script for BahrDetectorV2.
"""

import sys
sys.path.insert(0, '/home/user/BAHR/backend')

from app.core.prosody.detector_v2 import BahrDetectorV2, MatchQuality
from app.core.prosody.meters import METERS_REGISTRY

def test_all_base_patterns():
    """Test detection of all 16 meter base patterns."""
    print("=" * 80)
    print("Testing All 16 Meter Base Patterns")
    print("=" * 80)
    print()

    detector = BahrDetectorV2()
    passed = 0
    failed = 0

    for meter_id, meter in sorted(METERS_REGISTRY.items()):
        base_pattern = meter.base_pattern
        result = detector.detect_best(base_pattern)

        if result and result.meter_id == meter_id and result.confidence >= 0.98:
            print(f"✓ {meter_id:2d}. {meter.name_ar:12s} | {result.confidence:.1%} | {result.match_quality.value}")
            passed += 1
        else:
            print(f"✗ {meter_id:2d}. {meter.name_ar:12s} | FAILED")
            if result:
                print(f"   Got: {result.meter_name_ar} (confidence: {result.confidence:.1%})")
            else:
                print(f"   Got: None")
            failed += 1

    print()
    print(f"Results: {passed} passed, {failed} failed out of 16 meters")
    print()
    return failed == 0


def test_zihafat_detection():
    """Test detection of patterns with zihafat."""
    print("=" * 80)
    print("Testing Zihafat Detection")
    print("=" * 80)
    print()

    detector = BahrDetectorV2()

    test_cases = [
        {
            "name": "الطويل with قبض",
            "pattern": "/o////o/o/o/o//o//o/o/o",
            "expected_meter": 1,
            "min_confidence": 0.85,
        },
        {
            "name": "الكامل with إضمار",
            "pattern": "//oo//o//oo//o//oo//o",
            "expected_meter": 2,
            "min_confidence": 0.85,
        },
    ]

    passed = 0
    failed = 0

    for test in test_cases:
        result = detector.detect_best(test["pattern"])

        if (result and
            result.meter_id == test["expected_meter"] and
            result.confidence >= test["min_confidence"]):
            print(f"✓ {test['name']}")
            print(f"  Confidence: {result.confidence:.1%}")
            print(f"  Quality: {result.match_quality.value}")
            print(f"  Explanation: {result.explanation}")
            print()
            passed += 1
        else:
            print(f"✗ {test['name']} | FAILED")
            if result:
                print(f"  Got meter: {result.meter_name_ar} (expected: {test['expected_meter']})")
                print(f"  Confidence: {result.confidence:.1%} (min: {test['min_confidence']:.1%})")
            else:
                print(f"  Got: None")
            print()
            failed += 1

    print(f"Results: {passed} passed, {failed} failed")
    print()
    return failed == 0


def test_top_k_detection():
    """Test top-K detection."""
    print("=" * 80)
    print("Testing Top-K Detection")
    print("=" * 80)
    print()

    detector = BahrDetectorV2()
    pattern = "/o//o//o/o/o/o//o//o/o/o"  # الطويل

    results = detector.detect(pattern, top_k=3)

    print(f"Pattern: {pattern}")
    print(f"Top {len(results)} matches:")
    for i, result in enumerate(results, 1):
        print(f"  {i}. {result.meter_name_ar:12s} | {result.confidence:.1%} | {result.match_quality.value}")

    print()

    # Verify:
    # 1. Got results
    # 2. Top result is correct
    # 3. Sorted by confidence
    success = (
        len(results) > 0 and
        results[0].meter_id == 1 and
        results[0].confidence >= 0.98 and
        all(results[i].confidence >= results[i+1].confidence
            for i in range(len(results)-1))
    )

    if success:
        print("✓ Top-K detection working correctly")
    else:
        print("✗ Top-K detection failed")

    print()
    return success


def test_validation():
    """Test pattern validation."""
    print("=" * 80)
    print("Testing Pattern Validation")
    print("=" * 80)
    print()

    detector = BahrDetectorV2()

    tests = [
        ("Valid الطويل pattern", "/o//o//o/o/o/o//o//o/o/o", 1, True),
        ("Invalid pattern", "xyz123", 1, False),
        ("الطويل pattern for wrong meter", "/o//o//o/o/o/o//o//o/o/o", 2, False),
    ]

    passed = 0
    failed = 0

    for name, pattern, meter_id, expected in tests:
        result = detector.validate_pattern(pattern, meter_id)

        if result == expected:
            print(f"✓ {name}")
            passed += 1
        else:
            print(f"✗ {name} | Expected: {expected}, Got: {result}")
            failed += 1

    print()
    print(f"Results: {passed} passed, {failed} failed")
    print()
    return failed == 0


def test_statistics():
    """Test statistics."""
    print("=" * 80)
    print("Testing Statistics")
    print("=" * 80)
    print()

    detector = BahrDetectorV2()
    stats = detector.get_statistics()

    print(f"Total meters: {stats['total_meters']}")
    print(f"Total patterns: {stats['total_patterns']}")
    print(f"Patterns by tier:")
    for tier, count in stats['patterns_by_tier'].items():
        print(f"  Tier {tier}: {count} patterns")
    print(f"Meters by tier:")
    for tier, count in stats['meters_by_tier'].items():
        print(f"  Tier {tier}: {count} meters")

    print()

    success = (
        stats['total_meters'] == 16 and
        stats['total_patterns'] == 365 and
        stats['patterns_by_tier'][1] > 0
    )

    if success:
        print("✓ Statistics working correctly")
    else:
        print("✗ Statistics failed")

    print()
    return success


def main():
    """Run all tests."""
    print()
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "BahrDetectorV2 Manual Test Suite" + " " * 26 + "║")
    print("╚" + "═" * 78 + "╝")
    print()

    results = []

    results.append(("Base Patterns", test_all_base_patterns()))
    results.append(("Zihafat Detection", test_zihafat_detection()))
    results.append(("Top-K Detection", test_top_k_detection()))
    results.append(("Validation", test_validation()))
    results.append(("Statistics", test_statistics()))

    print("=" * 80)
    print("FINAL RESULTS")
    print("=" * 80)
    print()

    for name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{status:10s} | {name}")

    print()

    total_passed = sum(1 for _, p in results if p)
    total = len(results)

    print(f"Overall: {total_passed}/{total} test suites passed")
    print()

    if total_passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("❌ Some tests failed")
        return 1


if __name__ == "__main__":
    exit(main())
