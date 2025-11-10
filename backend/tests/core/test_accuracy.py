"""
Accuracy tests using real poetry dataset.

This module tests the end-to-end accuracy of the prosody analysis engine
using a curated dataset of classical Arabic poetry verses.
"""

import json
import pytest
from pathlib import Path
from collections import defaultdict
from typing import List, Dict

from app.core.bahr_detector import BahrDetector


@pytest.fixture
def test_verses():
    """
    Load test verses from JSON file.

    Returns:
        List of verse dictionaries with text, poet, bahr, etc.

    Example:
        >>> verses = test_verses()
        >>> verses[0]['text']
        "قِفا نَبْكِ مِن ذِكرى حَبيبٍ ومَنْزِلِ"
    """
    fixture_path = Path(__file__).parent.parent / "fixtures" / "test_verses.json"
    with open(fixture_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['verses']


class TestAccuracy:
    """
    Accuracy tests for the prosody engine.

    Tests overall accuracy and per-bahr accuracy against the test dataset.
    Target: 90%+ overall accuracy, 80%+ per-bahr accuracy.
    """

    def setup_method(self):
        """Initialize detector for each test."""
        self.detector = BahrDetector()

    def test_overall_accuracy(self, test_verses: List[Dict]):
        """
        Test accuracy across all test verses.

        Iterates through all verses in the test dataset, analyzes each verse,
        and compares detected bahr to expected bahr.

        Args:
            test_verses: List of verse dictionaries from fixture

        Asserts:
            Accuracy must be >= 90% (0.90)

        Example output:
            Accuracy: 92.3% (48/52)
        """
        correct = 0
        total = len(test_verses)
        failed_verses = []

        print(f"\n{'='*70}")
        print(f"OVERALL ACCURACY TEST")
        print(f"{'='*70}")
        print(f"Total verses to analyze: {total}\n")

        for i, verse_data in enumerate(test_verses, 1):
            verse_text = verse_data['text']
            expected_bahr = verse_data['bahr']

            try:
                result = self.detector.analyze_verse(verse_text)

                if result and result.name_ar == expected_bahr:
                    correct += 1
                    status = "✓"
                else:
                    detected = result.name_ar if result else "None"
                    failed_verses.append({
                        'text': verse_text,
                        'expected': expected_bahr,
                        'detected': detected,
                        'confidence': result.confidence if result else 0.0,
                        'poet': verse_data.get('poet', 'Unknown')
                    })
                    status = "✗"

                # Print progress every 10 verses
                if i % 10 == 0 or i == total:
                    print(f"Processed: {i}/{total} verses... ({status})")

            except Exception as e:
                print(f"ERROR on verse {i}: {e}")
                failed_verses.append({
                    'text': verse_text,
                    'expected': expected_bahr,
                    'detected': f'Error: {str(e)}',
                    'confidence': 0.0,
                    'poet': verse_data.get('poet', 'Unknown')
                })

        # Calculate accuracy
        accuracy = correct / total if total > 0 else 0.0

        # Print results
        print(f"\n{'='*70}")
        print(f"RESULTS")
        print(f"{'='*70}")
        print(f"Correct: {correct}/{total}")
        print(f"Accuracy: {accuracy*100:.1f}%")
        print(f"{'='*70}\n")

        # Print failed verses if any
        if failed_verses:
            print(f"\n{'='*70}")
            print(f"FAILED VERSES ({len(failed_verses)} total)")
            print(f"{'='*70}\n")

            for i, failure in enumerate(failed_verses, 1):
                print(f"{i}. Text: {failure['text'][:50]}...")
                print(f"   Poet: {failure['poet']}")
                print(f"   Expected: {failure['expected']}")
                print(f"   Detected: {failure['detected']}")
                if isinstance(failure['confidence'], float):
                    print(f"   Confidence: {failure['confidence']:.2f}")
                print()

        # Assertion: Must achieve 90%+ accuracy
        assert accuracy >= 0.90, (
            f"Accuracy {accuracy*100:.1f}% is below target 90%. "
            f"Failed on {len(failed_verses)} verses. "
            f"Review failed verses above and improve phonetic analysis, "
            f"pattern matching, or similarity threshold."
        )

    def test_accuracy_by_bahr(self, test_verses: List[Dict]):
        """
        Test accuracy for each bahr individually.

        Groups verses by bahr and calculates accuracy for each meter separately.
        This helps identify which bahrs need improvement.

        Args:
            test_verses: List of verse dictionaries from fixture

        Asserts:
            Each bahr must have >= 80% (0.80) accuracy

        Example output:
            Accuracy by Bahr:
              الطويل: 92.3% (12/13)
              الكامل: 84.6% (11/13)
              الوافر: 92.3% (12/13)
              الرمل: 100.0% (13/13)
        """
        results_by_bahr = defaultdict(lambda: {
            "correct": 0,
            "total": 0,
            "failed_verses": []
        })

        print(f"\n{'='*70}")
        print(f"ACCURACY BY BAHR TEST")
        print(f"{'='*70}\n")

        # Analyze each verse and group by expected bahr
        for verse_data in test_verses:
            verse_text = verse_data['text']
            expected_bahr = verse_data['bahr']

            results_by_bahr[expected_bahr]["total"] += 1

            try:
                result = self.detector.analyze_verse(verse_text)

                if result and result.name_ar == expected_bahr:
                    results_by_bahr[expected_bahr]["correct"] += 1
                else:
                    detected = result.name_ar if result else "None"
                    results_by_bahr[expected_bahr]["failed_verses"].append({
                        'text': verse_text,
                        'detected': detected,
                        'confidence': result.confidence if result else 0.0
                    })

            except Exception as e:
                results_by_bahr[expected_bahr]["failed_verses"].append({
                    'text': verse_text,
                    'detected': f'Error: {str(e)}',
                    'confidence': 0.0
                })

        # Print results by bahr
        print(f"{'Bahr':<15} {'Correct':<10} {'Total':<10} {'Accuracy':<15}")
        print(f"{'-'*70}")

        all_passed = True
        failed_bahrs = []

        for bahr in sorted(results_by_bahr.keys()):
            stats = results_by_bahr[bahr]
            accuracy = stats["correct"] / stats["total"] if stats["total"] > 0 else 0.0

            status = "✓" if accuracy >= 0.80 else "✗"
            print(f"{bahr:<15} {stats['correct']:<10} {stats['total']:<10} "
                  f"{accuracy*100:>5.1f}% {status}")

            # Check if this bahr meets the threshold
            if accuracy < 0.80:
                all_passed = False
                failed_bahrs.append({
                    'bahr': bahr,
                    'accuracy': accuracy,
                    'stats': stats
                })

        print(f"{'='*70}\n")

        # Print details for failed bahrs
        if failed_bahrs:
            print(f"\n{'='*70}")
            print(f"BAHRS BELOW 80% THRESHOLD")
            print(f"{'='*70}\n")

            for failure in failed_bahrs:
                bahr = failure['bahr']
                accuracy = failure['accuracy']
                stats = failure['stats']

                print(f"Bahr: {bahr}")
                print(f"Accuracy: {accuracy*100:.1f}% (below 80% target)")
                print(f"Correct: {stats['correct']}/{stats['total']}")
                print(f"\nFailed verses:")

                for i, verse_failure in enumerate(stats['failed_verses'][:5], 1):
                    print(f"  {i}. {verse_failure['text'][:50]}...")
                    print(f"     Detected: {verse_failure['detected']}")
                    if isinstance(verse_failure['confidence'], float):
                        print(f"     Confidence: {verse_failure['confidence']:.2f}")

                if len(stats['failed_verses']) > 5:
                    print(f"  ... and {len(stats['failed_verses']) - 5} more")
                print()

        # Assert each bahr meets threshold
        for bahr, stats in results_by_bahr.items():
            accuracy = stats["correct"] / stats["total"] if stats["total"] > 0 else 0.0
            assert accuracy >= 0.80, (
                f"{bahr} accuracy {accuracy*100:.1f}% is below 80% target. "
                f"Got {stats['correct']}/{stats['total']} correct. "
                f"Review pattern matching and similarity calculation for this bahr."
            )

    def test_dataset_validity(self, test_verses: List[Dict]):
        """
        Validate that the test dataset meets requirements.

        Checks:
        - At least 50 verses total
        - All verses have required fields
        - Coverage of all implemented bahrs

        Args:
            test_verses: List of verse dictionaries from fixture
        """
        print(f"\n{'='*70}")
        print(f"DATASET VALIDATION")
        print(f"{'='*70}\n")

        # Check total count
        total = len(test_verses)
        print(f"Total verses: {total}")
        assert total >= 50, f"Dataset has only {total} verses, need at least 50"

        # Check required fields
        required_fields = ['text', 'bahr']
        for i, verse in enumerate(test_verses, 1):
            for field in required_fields:
                assert field in verse, (
                    f"Verse {i} missing required field '{field}'"
                )
            assert isinstance(verse['text'], str) and verse['text'].strip(), (
                f"Verse {i} has empty or invalid text"
            )

        # Check bahr coverage
        bahrs_in_dataset = set(v['bahr'] for v in test_verses)
        implemented_bahrs = {b['name_ar'] for b in self.detector.bahrs}

        print(f"\nBahrs in dataset: {sorted(bahrs_in_dataset)}")
        print(f"Implemented bahrs: {sorted(implemented_bahrs)}")

        # All implemented bahrs should be in dataset
        for bahr in implemented_bahrs:
            assert bahr in bahrs_in_dataset, (
                f"Implemented bahr '{bahr}' not found in test dataset"
            )

        # Count verses per bahr
        bahr_counts = defaultdict(int)
        for verse in test_verses:
            bahr_counts[verse['bahr']] += 1

        print(f"\nVerses per bahr:")
        for bahr in sorted(bahr_counts.keys()):
            count = bahr_counts[bahr]
            print(f"  {bahr}: {count}")
            # Each bahr should have at least 10 verses for meaningful testing
            assert count >= 10, (
                f"Bahr '{bahr}' has only {count} verses, need at least 10"
            )

        print(f"\n{'='*70}")
        print(f"Dataset validation PASSED ✓")
        print(f"{'='*70}\n")
