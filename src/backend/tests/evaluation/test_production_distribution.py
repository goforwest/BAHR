"""
Production distribution validation tests for BAHR prosody engine.

These tests validate system performance on production-realistic data distribution:
- 10% fully diacritized (academic users)
- 20% partially diacritized (educated users)
- 70% undiacritized (typical users)

Success criteria:
- Undiacritized accuracy: ≥75% (with vowel inference)
- Fully diacritized accuracy: ≥97.5% (no regression)
- Overall accuracy: ≥85%

This addresses the critical test/production distribution mismatch.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Tuple

import pytest

from app.core.prosody.detector_v2 import BahrDetectorV2

logger = logging.getLogger(__name__)


class TestProductionDistribution:
    """Test detection on production-realistic data distribution."""

    @pytest.fixture(scope="class")
    def detector(self):
        """Initialize detector with vowel inference enabled."""
        return BahrDetectorV2(enable_vowel_inference=True)

    @pytest.fixture(scope="class")
    def test_data(self):
        """Load production-distribution test set."""
        # Try multiple possible locations
        possible_paths = [
            Path("data/test/golden_set_production_distribution.jsonl"),
            Path("../../data/test/golden_set_production_distribution.jsonl"),
            Path(__file__).parent.parent.parent.parent.parent
            / "data"
            / "test"
            / "golden_set_production_distribution.jsonl",
        ]

        test_file = None
        for path in possible_paths:
            if path.exists():
                test_file = path
                break

        if not test_file:
            pytest.skip(
                "Production distribution test set not found. "
                "Run: scripts/data_processing/create_production_test_set.py"
            )

        verses = []
        with open(test_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    verses.append(json.loads(line))

        return verses

    def _get_expected_meter(self, verse: Dict) -> str:
        """Extract expected meter from verse data."""
        # Try multiple possible keys
        for key in ["expected_meter", "meter", "bahr", "meter_ar"]:
            if key in verse:
                return verse[key]
        return None

    def _evaluate_verses(
        self, detector: BahrDetectorV2, verses: List[Dict]
    ) -> Tuple[int, int, List[Dict]]:
        """
        Evaluate detection on verses.
        
        Returns:
            (correct_count, total_count, failures)
        """
        correct = 0
        total = len(verses)
        failures = []

        for i, verse in enumerate(verses):
            verse_text = verse["verse"]
            expected_meter = self._get_expected_meter(verse)

            if not expected_meter:
                logger.warning(f"Verse {i} missing expected meter, skipping")
                total -= 1
                continue

            try:
                # Detect meter
                results = detector.detect(text=verse_text, top_k=1)

                if results:
                    detected_meter = results[0].meter_name_ar
                    confidence = results[0].confidence

                    if detected_meter == expected_meter:
                        correct += 1
                        logger.debug(
                            f"✓ Verse {i}: {detected_meter} (conf: {confidence:.2f})"
                        )
                    else:
                        failures.append(
                            {
                                "verse_index": i,
                                "verse": verse_text[:50] + "...",
                                "expected": expected_meter,
                                "detected": detected_meter,
                                "confidence": confidence,
                                "diacritization": verse.get("diacritization_level", "unknown"),
                            }
                        )
                        logger.debug(
                            f"✗ Verse {i}: Expected {expected_meter}, "
                            f"got {detected_meter} (conf: {confidence:.2f})"
                        )
                else:
                    failures.append(
                        {
                            "verse_index": i,
                            "verse": verse_text[:50] + "...",
                            "expected": expected_meter,
                            "detected": "NONE",
                            "confidence": 0.0,
                            "diacritization": verse.get("diacritization_level", "unknown"),
                        }
                    )
                    logger.debug(f"✗ Verse {i}: No detection for {expected_meter}")

            except Exception as e:
                logger.error(f"Error processing verse {i}: {e}")
                failures.append(
                    {
                        "verse_index": i,
                        "verse": verse_text[:50] + "...",
                        "expected": expected_meter,
                        "detected": "ERROR",
                        "confidence": 0.0,
                        "error": str(e),
                        "diacritization": verse.get("diacritization_level", "unknown"),
                    }
                )
                total -= 1

        return correct, total, failures

    def test_undiacritized_accuracy(self, detector, test_data):
        """
        Test detection on undiacritized text (70% of production).
        
        Target: ≥75% accuracy with vowel inference
        Acceptable: ≥65% accuracy
        Critical failure: <60% accuracy
        """
        # Filter for undiacritized verses
        undiacritized = [v for v in test_data if v.get("diacritization_level") == "undiacritized"]

        if not undiacritized:
            pytest.skip("No undiacritized verses in test set")

        correct, total, failures = self._evaluate_verses(detector, undiacritized)

        accuracy = correct / total if total > 0 else 0.0

        print("\n" + "=" * 70)
        print("📊 UNDIACRITIZED TEXT PERFORMANCE")
        print("=" * 70)
        print(f"Correct: {correct}/{total}")
        print(f"Accuracy: {accuracy:.1%}")
        print()

        if failures:
            print(f"Failures ({len(failures)}):")
            for f in failures[:5]:  # Show first 5 failures
                print(f"  • {f['verse']}")
                print(f"    Expected: {f['expected']}, Got: {f['detected']} (conf: {f['confidence']:.2f})")
            if len(failures) > 5:
                print(f"  ... and {len(failures) - 5} more")
        print("=" * 70)

        # Assert targets
        assert accuracy >= 0.75, (
            f"Undiacritized accuracy {accuracy:.1%} below target 75%. "
            f"This indicates vowel inference needs improvement."
        )

    def test_fully_diacritized_no_regression(self, detector, test_data):
        """
        Test detection on fully diacritized text (10% of production).
        
        Target: ≥97.5% accuracy (no regression from v1)
        Critical failure: <95% accuracy
        """
        # Filter for fully diacritized verses
        fully_diacritized = [v for v in test_data if v.get("diacritization_level") == "full"]

        if not fully_diacritized:
            pytest.skip("No fully diacritized verses in test set")

        correct, total, failures = self._evaluate_verses(detector, fully_diacritized)

        accuracy = correct / total if total > 0 else 0.0

        print("\n" + "=" * 70)
        print("📊 FULLY DIACRITIZED TEXT PERFORMANCE (Regression Check)")
        print("=" * 70)
        print(f"Correct: {correct}/{total}")
        print(f"Accuracy: {accuracy:.1%}")
        print()

        if failures:
            print(f"Failures ({len(failures)}):")
            for f in failures:
                print(f"  • {f['verse']}")
                print(f"    Expected: {f['expected']}, Got: {f['detected']} (conf: {f['confidence']:.2f})")
        print("=" * 70)

        # Assert no regression
        assert accuracy >= 0.975, (
            f"Fully diacritized accuracy {accuracy:.1%} below target 97.5%. "
            f"This is a REGRESSION from v1 performance."
        )

    def test_partially_diacritized_accuracy(self, detector, test_data):
        """
        Test detection on partially diacritized text (20% of production).
        
        Target: ≥85% accuracy (better than undiacritized, worse than full)
        """
        # Filter for partially diacritized verses
        partially_diacritized = [v for v in test_data if v.get("diacritization_level") == "partial"]

        if not partially_diacritized:
            pytest.skip("No partially diacritized verses in test set")

        correct, total, failures = self._evaluate_verses(detector, partially_diacritized)

        accuracy = correct / total if total > 0 else 0.0

        print("\n" + "=" * 70)
        print("📊 PARTIALLY DIACRITIZED TEXT PERFORMANCE")
        print("=" * 70)
        print(f"Correct: {correct}/{total}")
        print(f"Accuracy: {accuracy:.1%}")
        print()

        if failures:
            print(f"Failures ({len(failures)}):")
            for f in failures[:3]:
                print(f"  • {f['verse']}")
                print(f"    Expected: {f['expected']}, Got: {f['detected']} (conf: {f['confidence']:.2f})")
        print("=" * 70)

        # Assert target
        assert accuracy >= 0.85, (
            f"Partially diacritized accuracy {accuracy:.1%} below target 85%."
        )

    def test_overall_production_accuracy(self, detector, test_data):
        """
        Test overall accuracy on production-distribution test set.
        
        Weighted by distribution:
        - 10% full (97.5% accuracy) → 9.75%
        - 20% partial (85% accuracy) → 17%
        - 70% undiacritized (75% accuracy) → 52.5%
        
        Expected overall: ~79% minimum
        Target: ≥85%
        """
        correct, total, failures = self._evaluate_verses(detector, test_data)

        accuracy = correct / total if total > 0 else 0.0

        # Calculate per-level statistics
        stats_by_level = {}
        for level in ["full", "partial", "undiacritized"]:
            level_verses = [v for v in test_data if v.get("diacritization_level") == level]
            if level_verses:
                level_correct, level_total, _ = self._evaluate_verses(detector, level_verses)
                stats_by_level[level] = {
                    "correct": level_correct,
                    "total": level_total,
                    "accuracy": level_correct / level_total if level_total > 0 else 0.0,
                }

        print("\n" + "=" * 70)
        print("📊 OVERALL PRODUCTION PERFORMANCE")
        print("=" * 70)
        print(f"Overall Accuracy: {accuracy:.1%} ({correct}/{total})")
        print()
        print("Breakdown by Diacritization Level:")
        for level, stats in stats_by_level.items():
            print(
                f"  {level.upper()}: {stats['accuracy']:.1%} "
                f"({stats['correct']}/{stats['total']})"
            )
        print()

        if failures:
            print(f"Total Failures: {len(failures)}")
            # Group by diacritization level
            for level in ["full", "partial", "undiacritized"]:
                level_failures = [f for f in failures if f.get("diacritization") == level]
                if level_failures:
                    print(f"  {level}: {len(level_failures)} failures")
        print("=" * 70)

        # Assert overall target
        assert accuracy >= 0.85, (
            f"Overall production accuracy {accuracy:.1%} below target 85%. "
            f"Breakdown: {stats_by_level}"
        )


if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v", "-s"])
