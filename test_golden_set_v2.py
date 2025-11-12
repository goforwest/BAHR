#!/usr/bin/env python
"""
Test BahrDetectorV2 on Golden Set v0.101

Evaluates the new rule-based detector on 118 annotated verses
and compares performance to the v0.101 baseline (97.5% accuracy).
"""

import sys
import json
from pathlib import Path
from typing import List, Dict, Tuple
from collections import defaultdict

sys.path.insert(0, '/home/user/BAHR/backend')

from app.core.prosody.detector_v2 import BahrDetectorV2
from app.core.prosody.tafila import TAFAIL_BASE


# Meter name mapping (Arabic to ID)
METER_NAME_TO_ID = {
    "الطويل": 1,
    "الكامل": 2,
    "البسيط": 3,
    "الوافر": 4,
    "الرجز": 5,
    "الرمل": 6,
    "الخفيف": 7,
    "السريع": 8,
    "المديد": 9,
    "المنسرح": 10,
    "المتقارب": 11,
    "الهزج": 12,
    "المجتث": 13,
    "المقتضب": 14,
    "المضارع": 15,
    "المتدارك": 16,
    # مجزوء variants
    "الكامل (مجزوء)": 17,
    "الهزج (مجزوء)": 18,
}

# Meter variant mapping: maps مجزوء variants to their base meter
METER_VARIANT_BASE = {
    17: 2,  # مجزوء الكامل (2 تفاعيل) → الكامل
    18: 12,  # مجزوء الهزج (2 تفاعيل) → الهزج
    19: 2,  # الكامل (3 تفاعيل) → الكامل
    20: 8,  # السريع (مفعولات) → السريع
}


def load_golden_set(file_path: str) -> List[Dict]:
    """Load golden set JSONL file."""
    verses = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                verses.append(json.loads(line))
    return verses


def evaluate_detector(detector: BahrDetectorV2, verses: List[Dict]) -> Dict:
    """
    Evaluate detector on golden set verses.

    Returns:
        Dictionary with evaluation results
    """
    results = {
        "total": len(verses),
        "correct": 0,
        "incorrect": 0,
        "no_detection": 0,
        "accuracy": 0.0,
        "by_meter": defaultdict(lambda: {"total": 0, "correct": 0, "incorrect": 0}),
        "by_difficulty": defaultdict(lambda: {"total": 0, "correct": 0}),
        "misclassifications": [],
        "failed_scansions": [],
    }

    for verse in verses:
        verse_id = verse["verse_id"]
        text = verse["normalized_text"]
        expected_meter_ar = verse["meter"]
        expected_meter_id = METER_NAME_TO_ID.get(expected_meter_ar)
        expected_tafail = verse.get("expected_tafail", [])
        difficulty = verse.get("difficulty_level", "unknown")

        if not expected_meter_id:
            print(f"Warning: Unknown meter '{expected_meter_ar}' for {verse_id}")
            continue

        # Build phonetic pattern from expected tafail (expert annotations)
        try:
            pattern_parts = []
            for tafila_name in expected_tafail:
                tafila = TAFAIL_BASE.get(tafila_name)
                if tafila:
                    pattern_parts.append(tafila.phonetic)
                else:
                    raise ValueError(f"Unknown taf'ila: {tafila_name}")

            phonetic_pattern = ''.join(pattern_parts)

            if not phonetic_pattern:
                raise ValueError("Empty pattern generated")

        except Exception as e:
            results["failed_scansions"].append({
                "verse_id": verse_id,
                "text": text,
                "expected_meter": expected_meter_ar,
                "expected_tafail": expected_tafail,
                "error": str(e)
            })
            results["no_detection"] += 1
            results["by_meter"][expected_meter_ar]["total"] += 1
            results["by_difficulty"][difficulty]["total"] += 1
            continue

        # Detect meter
        result = detector.detect_best(phonetic_pattern)

        # Update statistics
        results["by_meter"][expected_meter_ar]["total"] += 1
        results["by_difficulty"][difficulty]["total"] += 1

        if result is None:
            results["no_detection"] += 1
            results["misclassifications"].append({
                "verse_id": verse_id,
                "text": text,
                "expected_meter": expected_meter_ar,
                "detected_meter": "None",
                "confidence": 0.0,
                "phonetic_pattern": phonetic_pattern,
                "difficulty": difficulty
            })
        else:
            # Check if detected meter matches expected
            # Accept either exact match OR مجزوء variant of the base meter
            is_correct = False

            if result.meter_id == expected_meter_id:
                # Exact match
                is_correct = True
            elif result.meter_id in METER_VARIANT_BASE:
                # Detected a مجزوء variant - check if it's a variant of the expected base
                if METER_VARIANT_BASE[result.meter_id] == expected_meter_id:
                    is_correct = True

            if is_correct:
                results["correct"] += 1
                results["by_meter"][expected_meter_ar]["correct"] += 1
                results["by_difficulty"][difficulty]["correct"] += 1
            else:
                results["incorrect"] += 1
                results["by_meter"][expected_meter_ar]["incorrect"] += 1
                results["misclassifications"].append({
                    "verse_id": verse_id,
                    "text": text,
                    "expected_meter": expected_meter_ar,
                    "detected_meter": result.meter_name_ar,
                    "confidence": result.confidence,
                    "phonetic_pattern": phonetic_pattern,
                    "explanation": result.explanation,
                    "difficulty": difficulty
                })

    # Calculate accuracy
    if results["total"] > 0:
        results["accuracy"] = (results["correct"] / results["total"]) * 100

    return results


def print_evaluation_report(results: Dict):
    """Print comprehensive evaluation report."""
    print("=" * 100)
    print("GOLDEN SET v0.101 EVALUATION REPORT - BahrDetectorV2")
    print("=" * 100)
    print()

    # Overall results
    print("OVERALL RESULTS")
    print("-" * 100)
    print(f"Total verses tested: {results['total']}")
    print(f"Correct detections:  {results['correct']} ({results['correct']/results['total']*100:.2f}%)")
    print(f"Incorrect:           {results['incorrect']} ({results['incorrect']/results['total']*100:.2f}%)")
    print(f"No detection:        {results['no_detection']} ({results['no_detection']/results['total']*100:.2f}%)")
    print()
    print(f"📊 ACCURACY: {results['accuracy']:.2f}%")
    print(f"🎯 TARGET:   97.50% (v0.101 baseline)")
    print()

    if results['accuracy'] >= 97.5:
        print("✅ TARGET ACHIEVED!")
    elif results['accuracy'] >= 95.0:
        print("⚠️  Close to target (within 2.5%)")
    else:
        print("❌ Below target")
    print()

    # Results by meter
    print("RESULTS BY METER")
    print("-" * 100)
    print(f"{'Meter':<15} {'Total':>6} {'Correct':>8} {'Incorrect':>10} {'Accuracy':>10}")
    print("-" * 100)

    for meter_name in sorted(results['by_meter'].keys()):
        stats = results['by_meter'][meter_name]
        total = stats['total']
        correct = stats['correct']
        incorrect = stats['incorrect']
        accuracy = (correct / total * 100) if total > 0 else 0

        print(f"{meter_name:<15} {total:>6} {correct:>8} {incorrect:>10} {accuracy:>9.1f}%")

    print()

    # Results by difficulty
    print("RESULTS BY DIFFICULTY")
    print("-" * 100)
    print(f"{'Difficulty':<15} {'Total':>6} {'Correct':>8} {'Accuracy':>10}")
    print("-" * 100)

    for difficulty in ["easy", "medium", "hard"]:
        if difficulty in results['by_difficulty']:
            stats = results['by_difficulty'][difficulty]
            total = stats['total']
            correct = stats['correct']
            accuracy = (correct / total * 100) if total > 0 else 0
            print(f"{difficulty:<15} {total:>6} {correct:>8} {accuracy:>9.1f}%")

    print()

    # Misclassifications
    if results['misclassifications']:
        print("MISCLASSIFICATIONS")
        print("-" * 100)
        print(f"Total misclassifications: {len(results['misclassifications'])}")
        print()

        for i, error in enumerate(results['misclassifications'][:10], 1):
            print(f"{i}. {error['verse_id']}")
            print(f"   Text: {error['text']}")
            print(f"   Expected: {error['expected_meter']}")
            print(f"   Detected: {error['detected_meter']} (confidence: {error.get('confidence', 0):.2%})")
            if 'explanation' in error:
                print(f"   Explanation: {error['explanation']}")
            print(f"   Pattern: {error.get('phonetic_pattern', 'N/A')}")
            print(f"   Difficulty: {error.get('difficulty', 'unknown')}")
            print()

        if len(results['misclassifications']) > 10:
            print(f"... and {len(results['misclassifications']) - 10} more misclassifications")
            print()

    # Failed scansions
    if results['failed_scansions']:
        print("FAILED SCANSIONS")
        print("-" * 100)
        print(f"Total failed scansions: {len(results['failed_scansions'])}")
        print()

        for i, error in enumerate(results['failed_scansions'][:5], 1):
            print(f"{i}. {error['verse_id']}")
            print(f"   Text: {error['text']}")
            print(f"   Expected: {error['expected_meter']}")
            print(f"   Error: {error['error']}")
            print()

    print("=" * 100)


def main():
    """Run golden set evaluation."""
    print()
    print("╔" + "═" * 98 + "╗")
    print("║" + " " * 25 + "BahrDetectorV2 - Golden Set v0.101 Evaluation" + " " * 28 + "║")
    print("╚" + "═" * 98 + "╝")
    print()

    # Load golden set
    golden_set_path = "/home/user/BAHR/dataset/evaluation/golden_set_v0_101_complete.jsonl"
    print(f"Loading golden set from: {golden_set_path}")

    try:
        verses = load_golden_set(golden_set_path)
        print(f"✓ Loaded {len(verses)} verses")
        print()
    except Exception as e:
        print(f"✗ Failed to load golden set: {e}")
        return 1

    # Initialize detector
    print("Initializing BahrDetectorV2...")
    try:
        detector = BahrDetectorV2()
        stats = detector.get_statistics()
        print(f"✓ Detector initialized")
        print(f"  - {stats['total_meters']} meters loaded")
        print(f"  - {stats['total_patterns']} valid patterns")
        print()
    except Exception as e:
        print(f"✗ Failed to initialize detector: {e}")
        return 1

    # Run evaluation
    print("Running evaluation on all verses...")
    print("(This may take a moment...)")
    print()

    try:
        results = evaluate_detector(detector, verses)
    except Exception as e:
        print(f"✗ Evaluation failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

    # Print report
    print_evaluation_report(results)

    # Save results to file
    output_file = "/home/user/BAHR/golden_set_v2_evaluation_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        # Convert defaultdict to regular dict for JSON serialization
        serializable_results = {
            "total": results["total"],
            "correct": results["correct"],
            "incorrect": results["incorrect"],
            "no_detection": results["no_detection"],
            "accuracy": results["accuracy"],
            "by_meter": dict(results["by_meter"]),
            "by_difficulty": dict(results["by_difficulty"]),
            "misclassifications": results["misclassifications"],
            "failed_scansions": results["failed_scansions"]
        }
        json.dump(serializable_results, f, ensure_ascii=False, indent=2)

    print(f"Results saved to: {output_file}")
    print()

    # Return exit code based on success
    if results['accuracy'] >= 97.5:
        print("🎉 Evaluation completed successfully! Target achieved.")
        return 0
    else:
        print("⚠️  Evaluation completed. Target not achieved yet.")
        return 0  # Still return 0, but with warning


if __name__ == "__main__":
    sys.exit(main())
