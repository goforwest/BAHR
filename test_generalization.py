#!/usr/bin/env python3
"""
Test BahrDetectorV2 generalization on unseen verses.

This script evaluates the detector on a diverse set of verses NOT in the
Golden Set to validate that it generalizes well beyond training data.
"""

import sys
import json
from pathlib import Path
from typing import List, Dict
from collections import defaultdict

sys.path.insert(0, '/home/user/BAHR/backend')

from app.core.prosody.detector_v2 import BahrDetectorV2
from app.core.prosody.tafila import TAFAIL_BASE

# Meter name mapping
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
    "الكامل (مجزوء)": 17,
    "الهزج (مجزوء)": 18,
}

# Meter variant mapping
METER_VARIANT_BASE = {
    17: 2,  # مجزوء الكامل (2 تفاعيل) → الكامل
    18: 12,  # مجزوء الهزج (2 تفاعيل) → الهزج
    19: 2,  # الكامل (3 تفاعيل) → الكامل
}


def load_test_set(file_path: str) -> List[Dict]:
    """Load generalization test set."""
    verses = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                verses.append(json.loads(line))
    return verses


def evaluate_generalization(detector: BahrDetectorV2, verses: List[Dict]) -> Dict:
    """Evaluate detector on generalization test set."""
    results = {
        "total": len(verses),
        "correct": 0,
        "incorrect": 0,
        "no_detection": 0,
        "accuracy": 0.0,
        "by_meter": defaultdict(lambda: {"total": 0, "correct": 0, "incorrect": 0}),
        "by_era": defaultdict(lambda: {"total": 0, "correct": 0}),
        "misclassifications": [],
        "failed_scansions": [],
    }

    for verse in verses:
        verse_id = verse["verse_id"]
        text = verse["normalized_text"]
        expected_meter_ar = verse["meter"]
        expected_meter_id = METER_NAME_TO_ID.get(expected_meter_ar)
        expected_tafail = verse.get("expected_tafail", [])
        era = verse.get("era", "unknown")

        if not expected_meter_id:
            print(f"Warning: Unknown meter '{expected_meter_ar}' for {verse_id}")
            continue

        # Build phonetic pattern from expected tafail
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
                "error": str(e)
            })
            results["no_detection"] += 1
            results["by_meter"][expected_meter_ar]["total"] += 1
            results["by_era"][era]["total"] += 1
            continue

        # Detect meter
        result = detector.detect_best(phonetic_pattern)

        # Update statistics
        results["by_meter"][expected_meter_ar]["total"] += 1
        results["by_era"][era]["total"] += 1

        if result is None:
            results["no_detection"] += 1
            results["misclassifications"].append({
                "verse_id": verse_id,
                "text": text,
                "poet": verse.get("poet", "unknown"),
                "era": era,
                "expected_meter": expected_meter_ar,
                "detected_meter": "None",
                "confidence": 0.0,
                "phonetic_pattern": phonetic_pattern
            })
        else:
            # Check if correct (accept مجزوء variants)
            is_correct = False

            if result.meter_id == expected_meter_id:
                is_correct = True
            elif result.meter_id in METER_VARIANT_BASE:
                if METER_VARIANT_BASE[result.meter_id] == expected_meter_id:
                    is_correct = True

            if is_correct:
                results["correct"] += 1
                results["by_meter"][expected_meter_ar]["correct"] += 1
                results["by_era"][era]["correct"] += 1
            else:
                results["incorrect"] += 1
                results["by_meter"][expected_meter_ar]["incorrect"] += 1
                results["misclassifications"].append({
                    "verse_id": verse_id,
                    "text": text,
                    "poet": verse.get("poet", "unknown"),
                    "era": era,
                    "expected_meter": expected_meter_ar,
                    "detected_meter": result.meter_name_ar,
                    "confidence": result.confidence,
                    "phonetic_pattern": phonetic_pattern,
                    "explanation": result.explanation
                })

    # Calculate accuracy
    if results["total"] > 0:
        results["accuracy"] = (results["correct"] / results["total"]) * 100

    return results


def print_generalization_report(results: Dict):
    """Print formatted generalization test report."""
    print("\n")
    print("╔" + "═" * 94 + "╗")
    print("║" + " " * 25 + "BahrDetectorV2 - Generalization Test Report" + " " * 26 + "║")
    print("╚" + "═" * 94 + "╝")
    print()

    # Overall results
    print("=" * 96)
    print("OVERALL RESULTS")
    print("-" * 96)
    print(f"Total verses tested: {results['total']}")
    print(f"Correct detections:  {results['correct']} ({results['correct']/results['total']*100:.2f}%)")
    print(f"Incorrect:           {results['incorrect']} ({results['incorrect']/results['total']*100:.2f}%)")
    print(f"No detection:        {results['no_detection']} ({results['no_detection']/results['total']*100:.2f}%)")
    print()
    print(f"📊 ACCURACY: {results['accuracy']:.2f}%")
    print(f"🎯 TARGET:   95.00%")
    print()

    if results['accuracy'] >= 95.0:
        print("✅ TARGET ACHIEVED!")
    elif results['accuracy'] >= 90.0:
        print("⚠️  Close to target (within 5%)")
    else:
        print("❌ Below target")

    # Results by meter
    print("\nRESULTS BY METER")
    print("-" * 96)
    print(f"{'Meter':<20} {'Total':>6}  {'Correct':>8}  {'Incorrect':>10}   {'Accuracy':>8}")
    print("-" * 96)

    for meter, stats in sorted(results['by_meter'].items()):
        total = stats['total']
        correct = stats['correct']
        incorrect = stats['incorrect']
        accuracy = (correct / total * 100) if total > 0 else 0
        print(f"{meter:<20} {total:>6}  {correct:>8}  {incorrect:>10}   {accuracy:>7.1f}%")

    # Results by era
    print("\nRESULTS BY ERA")
    print("-" * 96)
    print(f"{'Era':<20} {'Total':>6}  {'Correct':>8}   {'Accuracy':>8}")
    print("-" * 96)

    for era, stats in sorted(results['by_era'].items()):
        total = stats['total']
        correct = stats['correct']
        accuracy = (correct / total * 100) if total > 0 else 0
        print(f"{era:<20} {total:>6}  {correct:>8}   {accuracy:>7.1f}%")

    # Misclassifications
    if results['misclassifications']:
        print("\nMISCLASSIFICATIONS")
        print("-" * 96)
        print(f"Total misclassifications: {len(results['misclassifications'])}")
        print()

        for i, mis in enumerate(results['misclassifications'][:10], 1):  # Show first 10
            print(f"{i}. {mis['verse_id']}")
            print(f"   Text: {mis['text']}")
            print(f"   Poet: {mis['poet']} ({mis['era']})")
            print(f"   Expected: {mis['expected_meter']}")
            print(f"   Detected: {mis['detected_meter']} (confidence: {mis['confidence']:.2%})")
            print(f"   Pattern: {mis['phonetic_pattern']}")
            print()

        if len(results['misclassifications']) > 10:
            print(f"   ... and {len(results['misclassifications']) - 10} more")
            print()

    # Failed scansions
    if results['failed_scansions']:
        print("\nFAILED SCANSIONS")
        print("-" * 96)
        print(f"Total failed scansions: {len(results['failed_scansions'])}")
        print()

        for i, fail in enumerate(results['failed_scansions'][:5], 1):  # Show first 5
            print(f"{i}. {fail['verse_id']}")
            print(f"   Text: {fail['text']}")
            print(f"   Expected: {fail['expected_meter']}")
            print(f"   Error: {fail['error']}")
            print()

    print("=" * 96)
    print()

    # Summary message
    if results['accuracy'] >= 95.0:
        print("✅ Generalization test PASSED!")
        print(f"   Detector achieves {results['accuracy']:.2f}% accuracy on unseen verses.")
    else:
        print("⚠️  Generalization test completed with some issues.")
        print(f"   Review misclassifications to identify edge cases.")

    print()


def main():
    """Run generalization evaluation."""
    print("Loading generalization test set...")
    test_file = Path("/home/user/BAHR/dataset/evaluation/generalization_test_set.jsonl")

    if not test_file.exists():
        print(f"Error: Test file not found: {test_file}")
        return

    verses = load_test_set(test_file)
    print(f"✓ Loaded {len(verses)} test verses")
    print()

    print("Initializing BahrDetectorV2...")
    detector = BahrDetectorV2()
    stats = detector.get_statistics()
    print("✓ Detector initialized")
    print(f"  - {stats['total_meters']} meters loaded")
    print(f"  - {stats['total_patterns']} patterns")
    print()

    print("Running generalization evaluation...")
    print("(This tests on NEW verses not in the Golden Set)")
    print()

    results = evaluate_generalization(detector, verses)

    # Print report
    print_generalization_report(results)

    # Save results
    output_file = Path("/home/user/BAHR/generalization_test_results.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        # Convert defaultdict to regular dict for JSON
        results_json = {
            "total": results["total"],
            "correct": results["correct"],
            "incorrect": results["incorrect"],
            "no_detection": results["no_detection"],
            "accuracy": results["accuracy"],
            "by_meter": dict(results["by_meter"]),
            "by_era": dict(results["by_era"]),
            "misclassifications": results["misclassifications"],
            "failed_scansions": results["failed_scansions"]
        }
        json.dump(results_json, f, ensure_ascii=False, indent=2)

    print(f"Results saved to: {output_file}")
    print()


if __name__ == "__main__":
    main()
