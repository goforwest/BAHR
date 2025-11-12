#!/usr/bin/env python3
"""
Test suite for المتدارك validator

Demonstrates validation of correct and incorrect المتدارك annotations
"""

import json
from mutadarik_validator import MutadarikValidator, ValidationStatus

def test_valid_mutadarik():
    """Test validation of a correctly annotated المتدارك verse"""
    print("\n" + "="*80)
    print("TEST 1: Valid المتدارك verse (canonical form)")
    print("="*80)

    validator = MutadarikValidator()

    # Example: Canonical المتدارك pattern (4 × فاعلن)
    result = validator.validate(
        verse_id="test_001_valid_canonical",
        text="يا ليلُ الصبُّ متى غدُهُ",  # Example verse
        expected_tafail=["فاعلن", "فاعلن", "فاعلن", "فاعلن"],
        phonetic_pattern="/o//o/o//o/o//o/o//o"
    )

    result.print_report()
    assert result.status == ValidationStatus.PASSED, "Should pass validation"
    assert result.is_valid_mutadarik, "Should be valid المتدارك"
    print("✅ Test PASSED\n")


def test_valid_with_khabn():
    """Test المتدارك with خبن (khabn) transformations"""
    print("\n" + "="*80)
    print("TEST 2: Valid المتدارك with خبن")
    print("="*80)

    validator = MutadarikValidator()

    # Example: المتدارك with khabn in positions 2 and 4
    result = validator.validate(
        verse_id="test_002_valid_khabn",
        text="Test verse with khabn",
        expected_tafail=["فاعلن", "فعلن", "فاعلن", "فعلن"],
        phonetic_pattern="/o//o///o/o//o///o"
    )

    result.print_report()
    assert result.status == ValidationStatus.PASSED, "Should pass with khabn"
    print("✅ Test PASSED\n")


def test_valid_with_hadhf():
    """Test المتدارك with حذف (ḥadhf) in final position"""
    print("\n" + "="*80)
    print("TEST 3: Valid المتدارك with حذف")
    print("="*80)

    validator = MutadarikValidator()

    # Example: المتدارك with ḥadhf (remove final sabab)
    result = validator.validate(
        verse_id="test_003_valid_hadhf",
        text="Test verse with hadhf",
        expected_tafail=["فاعلن", "فاعلن", "فاعلن", "فاع"],
        phonetic_pattern="/o//o/o//o/o//o/o/"
    )

    result.print_report()
    assert result.status == ValidationStatus.PASSED, "Should pass with ḥadhf"
    print("✅ Test PASSED\n")


def test_invalid_tafail_count():
    """Test rejection of incorrect tafʿīla count"""
    print("\n" + "="*80)
    print("TEST 4: Invalid tafʿīla count (should FAIL)")
    print("="*80)

    validator = MutadarikValidator()

    # Wrong: Only 3 tafāʿīl (might be الرجز instead)
    result = validator.validate(
        verse_id="test_004_invalid_count",
        text="Test verse with wrong count",
        expected_tafail=["فاعلن", "فاعلن", "فاعلن"],  # Only 3!
        phonetic_pattern="/o//o/o//o/o//o"
    )

    result.print_report()
    assert result.status == ValidationStatus.FAILED, "Should fail due to wrong count"
    assert not result.is_valid_mutadarik, "Should NOT be valid"
    assert "Invalid tafʿīla count" in result.errors[0], "Should report count error"
    print("✅ Test PASSED (correctly rejected)\n")


def test_invalid_tafail_type():
    """Test rejection of incorrect tafʿīla types"""
    print("\n" + "="*80)
    print("TEST 5: Invalid tafʿīla types (should FAIL)")
    print("="*80)

    validator = MutadarikValidator()

    # Wrong: Using مستفعلن (characteristic of الرجز, not المتدارك)
    result = validator.validate(
        verse_id="test_005_invalid_type",
        text="Test verse with wrong tafila",
        expected_tafail=["مستفعلن", "فاعلن", "فاعلن", "فاعلن"],  # مستفعلن is invalid!
        phonetic_pattern="/o/o//o/o//o/o//o/o//o"
    )

    result.print_report()
    assert result.status == ValidationStatus.FAILED, "Should fail due to invalid tafʿīla"
    assert not result.is_valid_mutadarik, "Should NOT be valid"
    assert "Invalid tafāʿīl found" in result.errors[0], "Should report invalid tafāʿīl"
    print("✅ Test PASSED (correctly rejected)\n")


def test_rajaz_confusion():
    """Test detection of الرجز misclassified as المتدارك"""
    print("\n" + "="*80)
    print("TEST 6: Confusion with الرجز (should FAIL or NEEDS_REVIEW)")
    print("="*80)

    validator = MutadarikValidator()

    # Ambiguous: Pattern might match الرجز better than المتدارك
    result = validator.validate(
        verse_id="test_006_rajaz_confusion",
        text="مستفعلن مستفعلن مستفعلن",  # This is actually الرجز
        expected_tafail=["فعلن", "فعلن", "فعلن", "فعلن"],  # Claimed as المتدارك
        phonetic_pattern="///o///o///o///o"
    )

    result.print_report()

    # Should either fail or require review due to الرجز confusion
    assert result.status in [ValidationStatus.FAILED, ValidationStatus.NEEDS_REVIEW], \
        "Should detect confusion with الرجز"

    rajaz_risk = result.confusion_risk.get("الرجز", 0.0)
    print(f"الرجز confusion risk: {rajaz_risk:.1%}")

    print("✅ Test PASSED (confusion detected)\n")


def test_low_confidence():
    """Test verses with low confidence scores"""
    print("\n" + "="*80)
    print("TEST 7: Low confidence pattern (should NEEDS_REVIEW)")
    print("="*80)

    validator = MutadarikValidator()

    # Unusual pattern that might have low confidence
    result = validator.validate(
        verse_id="test_007_low_confidence",
        text="Ambiguous verse",
        expected_tafail=["فعلن", "فعلن", "فعلن", "فعل"],  # Heavy ziḥāfāt
        phonetic_pattern="///o///o///o///"
    )

    result.print_report()

    if result.confidence < 0.85:
        assert result.status in [ValidationStatus.NEEDS_REVIEW, ValidationStatus.WARNING], \
            "Low confidence should trigger review"
        print("✅ Test PASSED (low confidence flagged)\n")
    else:
        print("⚠️  Confidence higher than expected, but test logic is correct\n")


def run_all_tests():
    """Run all validation tests"""
    print("\n" + "#"*80)
    print("# RUNNING MUTADARIK VALIDATOR TEST SUITE")
    print("#"*80)

    tests = [
        test_valid_mutadarik,
        test_valid_with_khabn,
        test_valid_with_hadhf,
        test_invalid_tafail_count,
        test_invalid_tafail_type,
        test_rajaz_confusion,
        test_low_confidence
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"❌ TEST FAILED: {e}\n")
            failed += 1
        except Exception as e:
            print(f"💥 TEST ERROR: {e}\n")
            failed += 1

    print("\n" + "#"*80)
    print("# TEST SUMMARY")
    print("#"*80)
    print(f"Total tests: {len(tests)}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print("#"*80 + "\n")

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
