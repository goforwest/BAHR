#!/usr/bin/env python3
"""
Confusion Pattern Analysis Tool

Analyzes meter detection feedback to identify:
- Which meter pairs are most frequently confused
- Specific confusion patterns (e.g., الطويل ↔ الرجز)
- Common characteristics of confused verses
- Recommendations for improving detection

Usage:
    python -m app.tools.analyze_confusion_patterns [--feedback-file PATH] [--top N]
"""

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Tuple


class ConfusionAnalyzer:
    """Analyzes meter detection confusion patterns from feedback data."""

    def __init__(self, feedback_file: Path):
        """
        Initialize analyzer with feedback file.

        Args:
            feedback_file: Path to meter_feedback.jsonl file
        """
        self.feedback_file = feedback_file
        self.feedbacks: List[Dict] = []
        self.load_feedbacks()

    def load_feedbacks(self):
        """Load all feedback entries from JSONL file."""
        if not self.feedback_file.exists():
            print(f"⚠️  Feedback file not found: {self.feedback_file}")
            print("   No feedback data available for analysis.")
            return

        with open(self.feedback_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    self.feedbacks.append(json.loads(line))

        print(f"✓ Loaded {len(self.feedbacks)} feedback entries")

    def get_corrections_only(self) -> List[Dict]:
        """Get only correction feedbacks (where user changed the meter)."""
        return [
            fb
            for fb in self.feedbacks
            if fb.get("detected_meter") != fb.get("user_selected_meter")
        ]

    def analyze_confusion_pairs(self, top_n: int = 10) -> List[Tuple[str, int]]:
        """
        Analyze which meter pairs are most frequently confused.

        Args:
            top_n: Number of top confused pairs to return

        Returns:
            List of (pair_string, count) tuples, sorted by count descending
        """
        corrections = self.get_corrections_only()

        pair_counts = Counter()
        for fb in corrections:
            detected = fb.get("detected_meter", "Unknown")
            selected = fb.get("user_selected_meter", "Unknown")

            # Normalize pair order (alphabetically) to avoid duplicates
            pair = tuple(sorted([detected, selected]))
            pair_counts[pair] += 1

        # Format pairs as "A ↔ B"
        formatted_pairs = [
            (f"{p[0]} ↔ {p[1]}", count) for p, count in pair_counts.most_common(top_n)
        ]

        return formatted_pairs

    def analyze_specific_pair(self, meter1: str, meter2: str) -> Dict:
        """
        Analyze confusion between two specific meters.

        Args:
            meter1: First meter name (Arabic)
            meter2: Second meter name (Arabic)

        Returns:
            Dictionary with analysis results
        """
        corrections = self.get_corrections_only()

        # Find all cases where these two meters were confused
        confused_cases = []
        for fb in corrections:
            detected = fb.get("detected_meter")
            selected = fb.get("user_selected_meter")

            if {detected, selected} == {meter1, meter2}:
                confused_cases.append(fb)

        if not confused_cases:
            return {
                "pair": f"{meter1} ↔ {meter2}",
                "total_confusions": 0,
                "message": "No confusion found for this pair",
            }

        # Analyze directionality (A→B vs B→A)
        direction_counts = Counter()
        for fb in confused_cases:
            direction = f"{fb['detected_meter']} → {fb['user_selected_meter']}"
            direction_counts[direction] += 1

        # Analyze characteristics
        has_tashkeel_count = sum(1 for fb in confused_cases if fb.get("has_tashkeel"))
        avg_confidence = sum(
            fb.get("detected_confidence", 0) for fb in confused_cases
        ) / len(confused_cases)

        # Sample verses
        sample_verses = [
            {
                "text": fb.get("text", "")[:60] + "...",
                "detected": fb.get("detected_meter"),
                "user_selected": fb.get("user_selected_meter"),
                "confidence": fb.get("detected_confidence", 0),
                "has_tashkeel": fb.get("has_tashkeel", False),
                "comment": fb.get("user_comment", "")[:50],
            }
            for fb in confused_cases[:5]  # Top 5 examples
        ]

        return {
            "pair": f"{meter1} ↔ {meter2}",
            "total_confusions": len(confused_cases),
            "directionality": dict(direction_counts),
            "with_tashkeel": has_tashkeel_count,
            "without_tashkeel": len(confused_cases) - has_tashkeel_count,
            "avg_confidence": round(avg_confidence, 4),
            "sample_verses": sample_verses,
        }

    def get_most_corrected_meters(self, top_n: int = 10) -> List[Tuple[str, int]]:
        """
        Get meters that are most frequently corrected by users.

        Args:
            top_n: Number of top meters to return

        Returns:
            List of (meter_name, correction_count) tuples
        """
        corrections = self.get_corrections_only()

        detected_counts = Counter(
            fb.get("detected_meter", "Unknown") for fb in corrections
        )

        return detected_counts.most_common(top_n)

    def print_summary_report(self, top_n: int = 5):
        """Print a comprehensive summary report."""

        print("\n" + "=" * 80)
        print("METER DETECTION CONFUSION ANALYSIS - SUMMARY REPORT")
        print("=" * 80)

        # Overall statistics
        total = len(self.feedbacks)
        corrections = len(self.get_corrections_only())
        validations = total - corrections

        print(f"\n📊 OVERALL STATISTICS")
        print(f"   Total feedback entries: {total}")
        print(
            f"   Corrections (user changed meter): {corrections} ({corrections/total*100:.1f}%)"
            if total > 0
            else "   No data"
        )
        print(
            f"   Validations (user agreed): {validations} ({validations/total*100:.1f}%)"
            if total > 0
            else ""
        )

        # Most corrected meters
        print(f"\n🎯 MOST CORRECTED METERS (Top {top_n})")
        print("   These meters are frequently detected but then corrected by users:")
        most_corrected = self.get_most_corrected_meters(top_n)
        for i, (meter, count) in enumerate(most_corrected, 1):
            print(f"   {i}. {meter}: {count} corrections")

        # Most confused pairs
        print(f"\n🔀 MOST CONFUSED METER PAIRS (Top {top_n})")
        print("   These meter pairs are most frequently confused with each other:")
        confused_pairs = self.analyze_confusion_pairs(top_n)
        for i, (pair, count) in enumerate(confused_pairs, 1):
            print(f"   {i}. {pair}: {count} confusions")

        # Detailed analysis of top confused pair
        if confused_pairs:
            top_pair_str, top_count = confused_pairs[0]
            meters = top_pair_str.split(" ↔ ")

            print(f"\n🔍 DETAILED ANALYSIS: {top_pair_str}")
            print("=" * 80)

            analysis = self.analyze_specific_pair(meters[0], meters[1])

            print(f"\n   Total confusions: {analysis['total_confusions']}")
            print(f"   Average confidence: {analysis['avg_confidence']:.2%}")

            print("\n   Directionality:")
            for direction, count in analysis["directionality"].items():
                percentage = count / analysis["total_confusions"] * 100
                print(f"      {direction}: {count} times ({percentage:.1f}%)")

            print(f"\n   With diacritics: {analysis['with_tashkeel']}")
            print(f"   Without diacritics: {analysis['without_tashkeel']}")

            if analysis["sample_verses"]:
                print(f"\n   Sample verses:")
                for i, verse in enumerate(analysis["sample_verses"], 1):
                    print(f"\n      [{i}] {verse['text']}")
                    print(
                        f"          Detected: {verse['detected']} ({verse['confidence']:.2%})"
                    )
                    print(f"          User selected: {verse['user_selected']}")
                    print(f"          Has diacritics: {verse['has_tashkeel']}")
                    if verse["comment"]:
                        print(f"          Comment: {verse['comment']}")

        print("\n" + "=" * 80)
        print("END OF REPORT")
        print("=" * 80)

    def export_confusion_matrix(self, output_file: Path):
        """
        Export confusion matrix to JSON file.

        Args:
            output_file: Path to output JSON file
        """
        corrections = self.get_corrections_only()

        # Build confusion matrix
        matrix = defaultdict(lambda: defaultdict(int))
        for fb in corrections:
            detected = fb.get("detected_meter", "Unknown")
            selected = fb.get("user_selected_meter", "Unknown")
            matrix[detected][selected] += 1

        # Convert to regular dict for JSON serialization
        matrix_dict = {
            detected: dict(selected_counts)
            for detected, selected_counts in matrix.items()
        }

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(matrix_dict, f, ensure_ascii=False, indent=2)

        print(f"✓ Confusion matrix exported to: {output_file}")


def main():
    """Main entry point for CLI usage."""

    parser = argparse.ArgumentParser(
        description="Analyze meter detection confusion patterns from user feedback"
    )
    parser.add_argument(
        "--feedback-file",
        type=Path,
        default=Path("data/feedback/meter_feedback.jsonl"),
        help="Path to feedback JSONL file (default: data/feedback/meter_feedback.jsonl)",
    )
    parser.add_argument(
        "--top", type=int, default=5, help="Number of top results to show (default: 5)"
    )
    parser.add_argument(
        "--export-matrix", type=Path, help="Export confusion matrix to JSON file"
    )
    parser.add_argument(
        "--analyze-pair",
        nargs=2,
        metavar=("METER1", "METER2"),
        help="Analyze specific meter pair (e.g., --analyze-pair الطويل الرجز)",
    )

    args = parser.parse_args()

    # Initialize analyzer
    analyzer = ConfusionAnalyzer(args.feedback_file)

    if not analyzer.feedbacks:
        print("\n⚠️  No feedback data available. Exiting.")
        sys.exit(1)

    # Print summary report
    analyzer.print_summary_report(top_n=args.top)

    # Analyze specific pair if requested
    if args.analyze_pair:
        meter1, meter2 = args.analyze_pair
        print(f"\n{'=' * 80}")
        print(f"DETAILED ANALYSIS: {meter1} ↔ {meter2}")
        print("=" * 80)

        analysis = analyzer.analyze_specific_pair(meter1, meter2)

        if analysis["total_confusions"] == 0:
            print(f"\n⚠️  {analysis['message']}")
        else:
            print(f"\nTotal confusions: {analysis['total_confusions']}")
            print(f"Average confidence: {analysis['avg_confidence']:.2%}")

            print("\nDirectionality:")
            for direction, count in analysis["directionality"].items():
                print(f"  {direction}: {count} times")

            print(f"\nWith diacritics: {analysis['with_tashkeel']}")
            print(f"Without diacritics: {analysis['without_tashkeel']}")

    # Export confusion matrix if requested
    if args.export_matrix:
        analyzer.export_confusion_matrix(args.export_matrix)


if __name__ == "__main__":
    main()
