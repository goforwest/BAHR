#!/usr/bin/env python3
"""
Prosody Engine Testing on Golden Set v0.101

Tests the prosody engine's meter detection accuracy against the
118-verse Golden Set with authenticated Arabic poetry verses.

Usage:
    python test_prosody_golden_set.py
    
Output:
    - Overall accuracy metrics
    - Per-meter accuracy breakdown
    - Per-difficulty accuracy breakdown
    - Failed verse analysis
    - Detailed test report
"""

import sys
import json
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass
from datetime import datetime

# Add backend to path
backend_path = Path(__file__).parent.parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from app.core.bahr_detector import BahrDetector, BahrInfo


@dataclass
class TestResult:
    """Single verse test result."""
    verse_id: str
    text: str
    expected_meter: str
    predicted_meter: str | None
    confidence: float
    correct: bool
    difficulty: str
    edge_case_type: str
    poet: str


class ProsodyEngineTestSuite:
    """Test suite for prosody engine meter detection."""
    
    def __init__(self, golden_set_path: Path):
        """Initialize test suite with Golden Set data."""
        self.golden_set_path = golden_set_path
        self.detector = BahrDetector()
        self.results: List[TestResult] = []
        
    def load_golden_set(self) -> List[Dict]:
        """Load all verses from Golden Set JSONL file."""
        verses = []
        with open(self.golden_set_path, 'r', encoding='utf-8') as f:
            for line in f:
                verses.append(json.loads(line))
        return verses
    
    def test_single_verse(self, verse: Dict) -> TestResult:
        """Test meter detection on a single verse."""
        # Detect meter
        result = self.detector.analyze_verse(verse['text'])
        
        # Extract results
        predicted_meter = result.name_ar if result else None
        confidence = result.confidence if result else 0.0
        expected_meter = verse['meter']
        
        # Check correctness
        correct = (predicted_meter == expected_meter)
        
        return TestResult(
            verse_id=verse['verse_id'],
            text=verse['text'][:50] + "..." if len(verse['text']) > 50 else verse['text'],
            expected_meter=expected_meter,
            predicted_meter=predicted_meter,
            confidence=confidence,
            correct=correct,
            difficulty=verse['difficulty_level'],
            edge_case_type=verse['edge_case_type'],
            poet=verse['poet']
        )
    
    def run_all_tests(self) -> None:
        """Run meter detection on all Golden Set verses."""
        print("=" * 80)
        print("BAHR Prosody Engine Test Suite - Golden Set v0.101")
        print("=" * 80)
        print()
        
        verses = self.load_golden_set()
        print(f"Loaded {len(verses)} verses from Golden Set")
        print()
        
        # Test each verse
        print("Testing meter detection...")
        for i, verse in enumerate(verses, 1):
            result = self.test_single_verse(verse)
            self.results.append(result)
            
            # Progress indicator
            if i % 10 == 0:
                print(f"  Tested {i}/{len(verses)} verses...")
        
        print(f"  Tested {len(verses)}/{len(verses)} verses ✓")
        print()
    
    def calculate_overall_accuracy(self) -> Tuple[int, int, float]:
        """Calculate overall accuracy."""
        total = len(self.results)
        correct = sum(1 for r in self.results if r.correct)
        accuracy = correct / total if total > 0 else 0.0
        return correct, total, accuracy
    
    def calculate_meter_accuracy(self) -> Dict[str, Dict]:
        """Calculate accuracy per meter."""
        by_meter = {}
        
        for result in self.results:
            meter = result.expected_meter
            if meter not in by_meter:
                by_meter[meter] = {'correct': 0, 'total': 0}
            
            by_meter[meter]['total'] += 1
            if result.correct:
                by_meter[meter]['correct'] += 1
        
        # Calculate accuracy percentages
        for meter in by_meter:
            correct = by_meter[meter]['correct']
            total = by_meter[meter]['total']
            by_meter[meter]['accuracy'] = correct / total if total > 0 else 0.0
        
        return by_meter
    
    def calculate_difficulty_accuracy(self) -> Dict[str, Dict]:
        """Calculate accuracy per difficulty level."""
        by_difficulty = {}
        
        for result in self.results:
            difficulty = result.difficulty
            if difficulty not in by_difficulty:
                by_difficulty[difficulty] = {'correct': 0, 'total': 0}
            
            by_difficulty[difficulty]['total'] += 1
            if result.correct:
                by_difficulty[difficulty]['correct'] += 1
        
        # Calculate accuracy percentages
        for difficulty in by_difficulty:
            correct = by_difficulty[difficulty]['correct']
            total = by_difficulty[difficulty]['total']
            by_difficulty[difficulty]['accuracy'] = correct / total if total > 0 else 0.0
        
        return by_difficulty
    
    def get_failed_verses(self) -> List[TestResult]:
        """Get all verses where detection failed."""
        return [r for r in self.results if not r.correct]
    
    def print_summary(self) -> None:
        """Print comprehensive test summary."""
        print("=" * 80)
        print("TEST RESULTS SUMMARY")
        print("=" * 80)
        print()
        
        # Overall accuracy
        correct, total, accuracy = self.calculate_overall_accuracy()
        print(f"📊 Overall Accuracy: {correct}/{total} ({accuracy:.1%})")
        print()
        
        # Average confidence
        avg_confidence = sum(r.confidence for r in self.results) / len(self.results)
        print(f"📈 Average Confidence: {avg_confidence:.2f}")
        print()
        
        # Accuracy by meter
        print("-" * 80)
        print("📏 Accuracy by Meter:")
        print("-" * 80)
        by_meter = self.calculate_meter_accuracy()
        
        # Sort by total count (most common meters first)
        sorted_meters = sorted(by_meter.items(), 
                              key=lambda x: x[1]['total'], 
                              reverse=True)
        
        for meter, stats in sorted_meters:
            status = "✓" if stats['accuracy'] >= 0.80 else "✗"
            print(f"  {status} {meter:15s}: {stats['correct']:2d}/{stats['total']:2d} ({stats['accuracy']:5.1%})")
        print()
        
        # Accuracy by difficulty
        print("-" * 80)
        print("🎯 Accuracy by Difficulty:")
        print("-" * 80)
        by_difficulty = self.calculate_difficulty_accuracy()
        
        difficulty_order = ['easy', 'medium', 'hard']
        for difficulty in difficulty_order:
            if difficulty in by_difficulty:
                stats = by_difficulty[difficulty]
                status = "✓" if stats['accuracy'] >= 0.70 else "✗"
                print(f"  {status} {difficulty.capitalize():8s}: {stats['correct']:2d}/{stats['total']:2d} ({stats['accuracy']:5.1%})")
        print()
        
        # Failed verses
        failed = self.get_failed_verses()
        if failed:
            print("-" * 80)
            print(f"❌ Failed Verses ({len(failed)} total):")
            print("-" * 80)
            for result in failed[:10]:  # Show first 10
                print(f"  • {result.verse_id} ({result.poet})")
                print(f"    Expected: {result.expected_meter}")
                print(f"    Predicted: {result.predicted_meter or 'None'} (confidence: {result.confidence:.2f})")
                print(f"    Difficulty: {result.difficulty}, Type: {result.edge_case_type}")
                print(f"    Text: {result.text}")
                print()
            
            if len(failed) > 10:
                print(f"  ... and {len(failed) - 10} more failed verses")
                print()
        else:
            print("-" * 80)
            print("✅ All verses passed! Perfect accuracy!")
            print("-" * 80)
            print()
        
        # Performance targets
        print("-" * 80)
        print("🎯 Performance Target Assessment:")
        print("-" * 80)
        
        targets = [
            ("Overall Accuracy", accuracy, 0.80),
            ("Easy Verses", by_difficulty.get('easy', {}).get('accuracy', 0), 0.95),
            ("Medium Verses", by_difficulty.get('medium', {}).get('accuracy', 0), 0.85),
            ("Hard Verses", by_difficulty.get('hard', {}).get('accuracy', 0), 0.70),
        ]
        
        for name, actual, target in targets:
            if actual >= target:
                status = "✓ PASS"
                symbol = "✅"
            else:
                status = "✗ FAIL"
                symbol = "❌"
            print(f"  {symbol} {name:20s}: {actual:5.1%} (target: ≥{target:.0%}) {status}")
        print()
    
    def save_detailed_report(self, output_path: Path) -> None:
        """Save detailed test report to JSON file."""
        report = {
            "test_date": datetime.now().isoformat(),
            "golden_set_version": "0.100",
            "total_verses": len(self.results),
            "overall_accuracy": self.calculate_overall_accuracy()[2],
            "average_confidence": sum(r.confidence for r in self.results) / len(self.results),
            "by_meter": self.calculate_meter_accuracy(),
            "by_difficulty": self.calculate_difficulty_accuracy(),
            "failed_verses": [
                {
                    "verse_id": r.verse_id,
                    "text": r.text,
                    "expected": r.expected_meter,
                    "predicted": r.predicted_meter,
                    "confidence": r.confidence,
                    "difficulty": r.difficulty,
                    "edge_case_type": r.edge_case_type,
                    "poet": r.poet
                }
                for r in self.get_failed_verses()
            ],
            "all_results": [
                {
                    "verse_id": r.verse_id,
                    "expected": r.expected_meter,
                    "predicted": r.predicted_meter,
                    "confidence": r.confidence,
                    "correct": r.correct,
                    "difficulty": r.difficulty
                }
                for r in self.results
            ]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"📄 Detailed report saved to: {output_path}")
        print()


def main():
    """Main test execution."""
    # Paths
    dataset_dir = Path(__file__).parent.parent
    golden_set_path = dataset_dir / "evaluation" / "golden_set_v0_101_complete.jsonl"
    report_path = dataset_dir / "evaluation" / "prosody_test_report.json"
    
    # Check file exists
    if not golden_set_path.exists():
        print(f"❌ Error: Golden Set not found at {golden_set_path}")
        sys.exit(1)
    
    # Run tests
    suite = ProsodyEngineTestSuite(golden_set_path)
    suite.run_all_tests()
    suite.print_summary()
    suite.save_detailed_report(report_path)
    
    # Exit code based on overall accuracy
    _, _, accuracy = suite.calculate_overall_accuracy()
    if accuracy >= 0.80:
        print("✅ Test suite PASSED (≥80% accuracy)")
        sys.exit(0)
    else:
        print(f"❌ Test suite FAILED ({accuracy:.1%} < 80% target)")
        sys.exit(1)


if __name__ == "__main__":
    main()
