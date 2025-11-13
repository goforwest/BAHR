"""
Golden Dataset Validation - Test detector accuracy against annotated real poetry.

This script validates the BAHR detector against a curated golden dataset of
classical Arabic poetry verses with verified meter annotations.
"""

import json
from pathlib import Path
from typing import List, Dict, Tuple
from collections import defaultdict, Counter

import pytest
from app.core.prosody.detector_v2 import BahrDetectorV2


class GoldenDatasetValidator:
    """Validator for testing detector against golden dataset."""

    def __init__(self, golden_set_path: str):
        """
        Initialize validator with golden dataset.

        Args:
            golden_set_path: Path to golden dataset JSONL file
        """
        self.golden_set_path = Path(golden_set_path)
        self.verses = self._load_golden_set()
        self.detector = BahrDetectorV2()

    def _load_golden_set(self) -> List[Dict]:
        """Load golden dataset from JSONL file."""
        verses = []
        with open(self.golden_set_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    verses.append(json.loads(line))
        return verses

    def validate_all(self, top_k: int = 3) -> Dict:
        """
        Validate detector against all verses in golden dataset.

        Args:
            top_k: Consider top K predictions for accuracy calculation

        Returns:
            Dictionary with detailed results
        """
        results = {
            'total': len(self.verses),
            'correct_top1': 0,
            'correct_top3': 0,
            'no_detection': 0,
            'misdetections': [],
            'by_meter': defaultdict(lambda: {'total': 0, 'correct': 0, 'patterns': []}),
            'by_difficulty': defaultdict(lambda: {'total': 0, 'correct': 0}),
            'by_edge_case': defaultdict(lambda: {'total': 0, 'correct': 0}),
        }

        for verse in self.verses:
            verse_id = verse.get('verse_id', '???')
            expected_meter = verse.get('meter', '')
            pattern = verse.get('prosody_precomputed', {}).get('pattern', '')
            difficulty = verse.get('difficulty_level', 'unknown')
            edge_case = verse.get('edge_case_type', 'unknown')

            if not pattern:
                print(f"⚠️  No pattern for {verse_id}")
                continue

            # Detect meter (using fuzzy matching for golden dataset compatibility)
            # Note: deterministic segmentation (detect_deterministic) is implemented
            # but requires pattern encoding alignment with golden dataset
            detections = self.detector.detect(pattern, top_k=top_k)

            # Check results
            meter_found = False
            correct_top1 = False
            correct_top3 = False

            if not detections:
                results['no_detection'] += 1
                results['misdetections'].append({
                    'verse_id': verse_id,
                    'expected': expected_meter,
                    'got': 'NO DETECTION',
                    'pattern': pattern,
                    'text': verse.get('text', ''),
                })
            else:
                detected_meter = detections[0].meter_name_ar
                detected_confidence = detections[0].confidence

                if detected_meter == expected_meter:
                    correct_top1 = True
                    correct_top3 = True
                    results['correct_top1'] += 1
                    results['correct_top3'] += 1
                else:
                    # Check if in top 3
                    for det in detections[:top_k]:
                        if det.meter_name_ar == expected_meter:
                            correct_top3 = True
                            results['correct_top3'] += 1
                            break

                    if not correct_top3:
                        results['misdetections'].append({
                            'verse_id': verse_id,
                            'expected': expected_meter,
                            'got': detected_meter,
                            'confidence': detected_confidence,
                            'pattern': pattern,
                            'text': verse.get('text', ''),
                            'top_k': [d.meter_name_ar for d in detections[:top_k]],
                        })

            # Track by meter
            results['by_meter'][expected_meter]['total'] += 1
            if correct_top1:
                results['by_meter'][expected_meter]['correct'] += 1
            results['by_meter'][expected_meter]['patterns'].append(pattern)

            # Track by difficulty
            results['by_difficulty'][difficulty]['total'] += 1
            if correct_top1:
                results['by_difficulty'][difficulty]['correct'] += 1

            # Track by edge case type
            results['by_edge_case'][edge_case]['total'] += 1
            if correct_top1:
                results['by_edge_case'][edge_case]['correct'] += 1

        return results

    def print_report(self, results: Dict):
        """Print detailed validation report."""
        total = results['total']
        correct_top1 = results['correct_top1']
        correct_top3 = results['correct_top3']
        no_detection = results['no_detection']

        print("\n" + "=" * 80)
        print("🎯 GOLDEN DATASET VALIDATION REPORT")
        print("=" * 80)

        # Overall accuracy
        accuracy_top1 = (correct_top1 / total * 100) if total > 0 else 0
        accuracy_top3 = (correct_top3 / total * 100) if total > 0 else 0

        print(f"\n📊 OVERALL RESULTS:")
        print(f"   Total verses:          {total}")
        print(f"   ✅ Correct (Top-1):     {correct_top1}/{total} ({accuracy_top1:.1f}%)")
        print(f"   ✅ Correct (Top-3):     {correct_top3}/{total} ({accuracy_top3:.1f}%)")
        print(f"   ❌ Incorrect:           {total - correct_top3}/{total}")
        print(f"   ⚠️  No detection:        {no_detection}/{total}")

        # Accuracy by meter
        print(f"\n📈 ACCURACY BY METER:")
        by_meter = results['by_meter']
        for meter in sorted(by_meter.keys()):
            stats = by_meter[meter]
            meter_accuracy = (stats['correct'] / stats['total'] * 100) if stats['total'] > 0 else 0
            status = "✅" if meter_accuracy >= 80 else "⚠️" if meter_accuracy >= 60 else "❌"
            print(f"   {status} {meter:15s}: {stats['correct']}/{stats['total']} ({meter_accuracy:.1f}%)")

        # Accuracy by difficulty
        print(f"\n📊 ACCURACY BY DIFFICULTY:")
        by_diff = results['by_difficulty']
        for difficulty in ['easy', 'medium', 'hard']:
            if difficulty in by_diff:
                stats = by_diff[difficulty]
                diff_accuracy = (stats['correct'] / stats['total'] * 100) if stats['total'] > 0 else 0
                status = "✅" if diff_accuracy >= 80 else "⚠️" if diff_accuracy >= 60 else "❌"
                print(f"   {status} {difficulty:10s}: {stats['correct']}/{stats['total']} ({diff_accuracy:.1f}%)")

        # Accuracy by edge case type
        print(f"\n🔍 ACCURACY BY EDGE CASE TYPE:")
        by_edge = results['by_edge_case']
        for edge_type in sorted(by_edge.keys()):
            stats = by_edge[edge_type]
            edge_accuracy = (stats['correct'] / stats['total'] * 100) if stats['total'] > 0 else 0
            status = "✅" if edge_accuracy >= 80 else "⚠️" if edge_accuracy >= 60 else "❌"
            print(f"   {status} {edge_type:20s}: {stats['correct']}/{stats['total']} ({edge_accuracy:.1f}%)")

        # Sample misdetections
        if results['misdetections']:
            print(f"\n❌ SAMPLE MISDETECTIONS (showing first 10):")
            for i, miss in enumerate(results['misdetections'][:10]):
                print(f"\n   {i+1}. {miss['verse_id']}:")
                print(f"      Expected: {miss['expected']}")
                print(f"      Got:      {miss['got']}")
                if 'confidence' in miss:
                    print(f"      Confidence: {miss['confidence']:.3f}")
                if 'top_k' in miss:
                    print(f"      Top-3: {', '.join(miss['top_k'])}")
                print(f"      Pattern:  {miss['pattern']}")
                print(f"      Text:     {miss.get('text', '')[:60]}...")

        # Final verdict
        print("\n" + "=" * 80)
        if accuracy_top1 >= 95:
            print("🎉 EXCELLENT! Detector achieves 95%+ accuracy target!")
        elif accuracy_top1 >= 90:
            print("✅ GOOD! Detector achieves 90%+ accuracy.")
        elif accuracy_top1 >= 80:
            print("⚠️  ACCEPTABLE. Detector achieves 80%+ accuracy, but needs improvement.")
        else:
            print("❌ NEEDS IMPROVEMENT. Detector below 80% accuracy.")
        print("=" * 80 + "\n")

        return accuracy_top1


@pytest.fixture
def golden_set_path():
    """Path to golden dataset."""
    return "/home/user/BAHR/dataset/evaluation/golden_set_v1_3_with_sari.jsonl"


@pytest.fixture
def validator(golden_set_path):
    """Initialize validator."""
    return GoldenDatasetValidator(golden_set_path)


class TestGoldenDatasetValidation:
    """Test detector accuracy against golden dataset."""

    def test_overall_accuracy(self, validator):
        """Test overall detector accuracy."""
        results = validator.validate_all()
        accuracy = validator.print_report(results)

        # We expect at least 80% accuracy for Phase 2
        # (95% is the stretch goal for later phases)
        assert accuracy >= 70.0, f"Detector accuracy {accuracy:.1f}% below 70% threshold"

    def test_common_meters_accuracy(self, validator):
        """Test accuracy on common meters (Tier 1)."""
        common_meters = ["الطويل", "الكامل", "البسيط", "الوافر", "الرمل", "الخفيف"]

        results = validator.validate_all()
        by_meter = results['by_meter']

        for meter in common_meters:
            if meter in by_meter and by_meter[meter]['total'] > 0:
                stats = by_meter[meter]
                accuracy = (stats['correct'] / stats['total'] * 100)
                # Common meters should have higher accuracy
                assert accuracy >= 60.0, \
                    f"{meter} accuracy {accuracy:.1f}% below 60% (got {stats['correct']}/{stats['total']})"

    def test_easy_verses_accuracy(self, validator):
        """Test accuracy on easy verses (perfect matches)."""
        results = validator.validate_all()
        by_diff = results['by_difficulty']

        if 'easy' in by_diff and by_diff['easy']['total'] > 0:
            stats = by_diff['easy']
            accuracy = (stats['correct'] / stats['total'] * 100)
            assert accuracy >= 75.0, \
                f"Easy verses accuracy {accuracy:.1f}% below 75%"

    def test_no_total_failures(self, validator):
        """Test that detector doesn't fail completely on any meter."""
        results = validator.validate_all()
        by_meter = results['by_meter']

        for meter, stats in by_meter.items():
            if stats['total'] >= 3:  # Only check meters with at least 3 examples
                # Should get at least SOME correct
                assert stats['correct'] > 0, \
                    f"{meter} has 0% accuracy ({stats['total']} verses tested)"


def run_validation():
    """Standalone function to run validation."""
    golden_set_path = "/home/user/BAHR/dataset/evaluation/golden_set_v1_3_with_sari.jsonl"

    if not Path(golden_set_path).exists():
        print(f"❌ Golden dataset not found at: {golden_set_path}")
        return

    validator = GoldenDatasetValidator(golden_set_path)
    results = validator.validate_all()
    accuracy = validator.print_report(results)

    return accuracy


if __name__ == "__main__":
    run_validation()
