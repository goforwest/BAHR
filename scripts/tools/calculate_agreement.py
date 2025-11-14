#!/usr/bin/env python3
"""
Calculate Inter-Annotator Agreement for المتدارك Expert Annotations

This script analyzes multiple expert annotations to calculate:
- Fleiss' Kappa (multi-rater agreement)
- Percentage agreement
- Confusion matrices
- Disputed verse identification

Usage:
    python calculate_agreement.py --annotations expert1.csv expert2.csv expert3.csv
    python calculate_agreement.py --dir phase3_materials/annotations/
    python calculate_agreement.py --annotations *.csv --output agreement_report.json
"""

import argparse
import json
import csv
from pathlib import Path
from collections import defaultdict, Counter
from typing import List, Dict, Tuple
import sys


def load_annotations(file_path: str) -> Dict:
    """Load annotations from CSV file."""
    annotations = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            verse_id = row['verse_id']
            annotations[verse_id] = {
                'primary_meter': row['primary_meter'].strip(),
                'confidence': int(row['confidence_1to5']) if row['confidence_1to5'] else None,
                'alternative_meter': row['alternative_meter'].strip() if row['alternative_meter'] else None,
                'tafail': row['tafail_scansion'].strip() if row['tafail_scansion'] else None,
                'valid_example': row['valid_example'].strip() if row['valid_example'] else None,
                'naturalness': int(row['naturalness_1to5']) if row['naturalness_1to5'] else None,
            }
    return annotations


def calculate_fleiss_kappa(annotations_by_expert: List[Dict]) -> float:
    """
    Calculate Fleiss' Kappa for multi-rater agreement.

    Formula: κ = (P_observed - P_expected) / (1 - P_expected)
    """
    # Get all verses
    verse_ids = sorted(annotations_by_expert[0].keys())
    n_verses = len(verse_ids)
    n_raters = len(annotations_by_expert)

    # Get all unique meter labels
    all_meters = set()
    for expert_annotations in annotations_by_expert:
        for v_id, annotation in expert_annotations.items():
            if annotation['primary_meter']:
                all_meters.add(annotation['primary_meter'])

    meters = sorted(all_meters)
    n_categories = len(meters)

    if n_categories < 2:
        return 1.0  # Perfect agreement if only one category

    # Build rating matrix
    # For each verse, count how many raters assigned each meter
    rating_matrix = []
    for verse_id in verse_ids:
        counts = Counter()
        for expert_annotations in annotations_by_expert:
            meter = expert_annotations[verse_id]['primary_meter']
            if meter:
                counts[meter] += 1

        # Convert to list in consistent order
        row = [counts[meter] for meter in meters]
        rating_matrix.append(row)

    # Calculate P_i (proportion of agreement for each verse)
    P_i_values = []
    for row in rating_matrix:
        # P_i = (sum of n_ij * (n_ij - 1)) / (n * (n - 1))
        # where n_ij is count of raters choosing category j for verse i
        numerator = sum(n_ij * (n_ij - 1) for n_ij in row)
        denominator = n_raters * (n_raters - 1)
        P_i = numerator / denominator if denominator > 0 else 0
        P_i_values.append(P_i)

    # P_observed = mean of P_i
    P_observed = sum(P_i_values) / n_verses

    # Calculate P_expected
    # P_expected = sum of (p_j)^2 where p_j is proportion of all assignments to category j
    total_assignments = n_verses * n_raters
    category_proportions = []

    for j, meter in enumerate(meters):
        count = sum(row[j] for row in rating_matrix)
        p_j = count / total_assignments
        category_proportions.append(p_j)

    P_expected = sum(p_j ** 2 for p_j in category_proportions)

    # Calculate Kappa
    if P_expected == 1.0:
        return 1.0  # Perfect agreement

    kappa = (P_observed - P_expected) / (1 - P_expected)

    return kappa


def calculate_percentage_agreement(annotations_by_expert: List[Dict]) -> float:
    """Calculate simple percentage agreement across all annotators."""
    verse_ids = sorted(annotations_by_expert[0].keys())

    agreements = 0
    total = 0

    for verse_id in verse_ids:
        meters = [expert[verse_id]['primary_meter'] for expert in annotations_by_expert
                 if expert[verse_id]['primary_meter']]

        if not meters:
            continue

        # Count most common meter
        meter_counts = Counter(meters)
        most_common_count = meter_counts.most_common(1)[0][1]

        # Agreement = proportion of raters who chose the most common
        agreement = most_common_count / len(meters)

        agreements += agreement
        total += 1

    return (agreements / total * 100) if total > 0 else 0


def identify_disputed_verses(annotations_by_expert: List[Dict], threshold: float = 0.8) -> List[str]:
    """
    Identify verses with low agreement (< threshold * n_raters agree).

    Args:
        threshold: Minimum proportion of raters that must agree (default 0.8 = 80%)
    """
    verse_ids = sorted(annotations_by_expert[0].keys())
    n_raters = len(annotations_by_expert)
    disputed = []

    for verse_id in verse_ids:
        meters = [expert[verse_id]['primary_meter'] for expert in annotations_by_expert
                 if expert[verse_id]['primary_meter']]

        if not meters:
            continue

        meter_counts = Counter(meters)
        most_common_count = meter_counts.most_common(1)[0][1]

        agreement_rate = most_common_count / len(meters)

        if agreement_rate < threshold:
            disputed.append(verse_id)

    return disputed


def build_confusion_matrix(annotations_by_expert: List[Dict]) -> Dict:
    """Build confusion matrix showing which meters are confused with each other."""
    verse_ids = sorted(annotations_by_expert[0].keys())

    # For each verse, if annotators disagree, track the pairs of meters confused
    confusion_pairs = defaultdict(int)

    for verse_id in verse_ids:
        meters = [expert[verse_id]['primary_meter'] for expert in annotations_by_expert
                 if expert[verse_id]['primary_meter']]

        if len(set(meters)) > 1:  # Disagreement
            # Count all pairwise disagreements
            for i, meter1 in enumerate(meters):
                for meter2 in meters[i+1:]:
                    if meter1 != meter2:
                        pair = tuple(sorted([meter1, meter2]))
                        confusion_pairs[pair] += 1

    return dict(confusion_pairs)


def calculate_confidence_correlation(annotations_by_expert: List[Dict]) -> Dict:
    """Analyze relationship between confidence scores and agreement."""
    verse_ids = sorted(annotations_by_expert[0].keys())
    n_raters = len(annotations_by_expert)

    confidence_vs_agreement = []

    for verse_id in verse_ids:
        # Get meters and confidences
        data = [(expert[verse_id]['primary_meter'], expert[verse_id]['confidence'])
                for expert in annotations_by_expert
                if expert[verse_id]['primary_meter'] and expert[verse_id]['confidence']]

        if not data:
            continue

        meters = [m for m, c in data]
        confidences = [c for m, c in data]

        # Calculate agreement
        meter_counts = Counter(meters)
        most_common_count = meter_counts.most_common(1)[0][1]
        agreement_rate = most_common_count / len(meters)

        # Average confidence
        avg_confidence = sum(confidences) / len(confidences)

        confidence_vs_agreement.append({
            'verse_id': verse_id,
            'agreement_rate': agreement_rate,
            'avg_confidence': avg_confidence,
            'meters': list(meter_counts.keys())
        })

    return confidence_vs_agreement


def generate_report(annotations_by_expert: List[Dict], expert_names: List[str]) -> Dict:
    """Generate comprehensive agreement analysis report."""

    print(f"\n{'='*80}")
    print(f"INTER-ANNOTATOR AGREEMENT ANALYSIS")
    print(f"{'='*80}\n")

    print(f"Number of experts: {len(expert_names)}")
    print(f"Expert names: {', '.join(expert_names)}")

    verse_ids = sorted(annotations_by_expert[0].keys())
    print(f"Number of verses: {len(verse_ids)}\n")

    # Calculate Fleiss' Kappa
    print(f"{'='*80}")
    print(f"FLEISS' KAPPA (Multi-Rater Agreement)")
    print(f"{'='*80}")

    kappa = calculate_fleiss_kappa(annotations_by_expert)
    print(f"κ = {kappa:.4f}")

    # Interpretation
    if kappa < 0.40:
        interpretation = "Poor agreement"
        recommendation = "❌ Major revision needed"
    elif kappa < 0.60:
        interpretation = "Moderate agreement"
        recommendation = "⚠️  Some verses need clarification"
    elif kappa < 0.80:
        interpretation = "Substantial agreement"
        recommendation = "✓ Minor adjustments needed"
    elif kappa < 0.90:
        interpretation = "Excellent agreement"
        recommendation = "✅ Proceed with confidence"
    else:
        interpretation = "Nearly perfect agreement"
        recommendation = "✅ High quality annotations"

    print(f"Interpretation: {interpretation}")
    print(f"Recommendation: {recommendation}\n")

    # Percentage agreement
    pct_agreement = calculate_percentage_agreement(annotations_by_expert)
    print(f"{'='*80}")
    print(f"PERCENTAGE AGREEMENT")
    print(f"{'='*80}")
    print(f"Average agreement: {pct_agreement:.2f}%\n")

    # Disputed verses
    disputed = identify_disputed_verses(annotations_by_expert, threshold=0.8)
    print(f"{'='*80}")
    print(f"DISPUTED VERSES (<80% agreement)")
    print(f"{'='*80}")
    print(f"Count: {len(disputed)}/{len(verse_ids)} ({len(disputed)/len(verse_ids)*100:.1f}%)")

    if disputed:
        print(f"\nDisputed verse IDs:")
        for v_id in disputed:
            print(f"  - {v_id}")
    else:
        print(f"\n✅ No disputed verses!")
    print()

    # Confusion matrix
    print(f"{'='*80}")
    print(f"CONFUSION MATRIX")
    print(f"{'='*80}")

    confusion = build_confusion_matrix(annotations_by_expert)

    if confusion:
        print(f"Meter pairs confused (count of disagreements):\n")
        for (meter1, meter2), count in sorted(confusion.items(), key=lambda x: -x[1]):
            print(f"  {meter1} ↔ {meter2}: {count} disagreements")
    else:
        print(f"✅ No confusion - perfect agreement!")
    print()

    # Confidence correlation
    print(f"{'='*80}")
    print(f"CONFIDENCE VS AGREEMENT")
    print(f"{'='*80}")

    conf_data = calculate_confidence_correlation(annotations_by_expert)

    # Group by agreement level
    high_agreement = [d for d in conf_data if d['agreement_rate'] >= 0.8]
    low_agreement = [d for d in conf_data if d['agreement_rate'] < 0.8]

    if high_agreement:
        avg_conf_high = sum(d['avg_confidence'] for d in high_agreement) / len(high_agreement)
        print(f"High agreement verses (≥80%): {len(high_agreement)}")
        print(f"  Average confidence: {avg_conf_high:.2f}/5")

    if low_agreement:
        avg_conf_low = sum(d['avg_confidence'] for d in low_agreement) / len(low_agreement)
        print(f"Low agreement verses (<80%): {len(low_agreement)}")
        print(f"  Average confidence: {avg_conf_low:.2f}/5")

    print()

    # Build report dict
    report = {
        'summary': {
            'n_experts': len(expert_names),
            'expert_names': expert_names,
            'n_verses': len(verse_ids),
            'fleiss_kappa': round(kappa, 4),
            'kappa_interpretation': interpretation,
            'kappa_recommendation': recommendation,
            'percentage_agreement': round(pct_agreement, 2),
            'n_disputed': len(disputed),
            'disputed_rate': round(len(disputed)/len(verse_ids)*100, 2)
        },
        'disputed_verses': disputed,
        'confusion_matrix': confusion,
        'confidence_correlation': conf_data
    }

    return report


def main():
    parser = argparse.ArgumentParser(
        description='Calculate inter-annotator agreement for المتدارك expert annotations'
    )
    parser.add_argument(
        '--annotations',
        nargs='+',
        help='Annotation CSV files (e.g., expert1.csv expert2.csv expert3.csv)'
    )
    parser.add_argument(
        '--dir',
        help='Directory containing annotation CSV files'
    )
    parser.add_argument(
        '--output',
        default='agreement_report.json',
        help='Output file for agreement report (JSON)'
    )

    args = parser.parse_args()

    # Collect annotation files
    annotation_files = []

    if args.annotations:
        annotation_files = args.annotations
    elif args.dir:
        dir_path = Path(args.dir)
        annotation_files = list(dir_path.glob('*.csv'))
    else:
        print("Error: Must provide either --annotations or --dir")
        sys.exit(1)

    if len(annotation_files) < 2:
        print(f"Error: Need at least 2 annotation files. Found {len(annotation_files)}")
        sys.exit(1)

    # Load all annotations
    annotations_by_expert = []
    expert_names = []

    for file_path in annotation_files:
        print(f"Loading: {file_path}")
        annotations = load_annotations(file_path)
        annotations_by_expert.append(annotations)

        # Extract expert name from filename
        expert_name = Path(file_path).stem.replace('annotation_', '')
        expert_names.append(expert_name)

    # Generate report
    report = generate_report(annotations_by_expert, expert_names)

    # Save report
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"{'='*80}")
    print(f"Report saved to: {args.output}")
    print(f"{'='*80}\n")

    # Final recommendation
    kappa = report['summary']['fleiss_kappa']
    if kappa >= 0.85:
        print("✅ SUCCESS: Excellent agreement achieved (κ ≥ 0.85)")
        print("✅ Corpus is ready for golden set integration")
    elif kappa >= 0.60:
        print("⚠️  MODERATE: Substantial agreement achieved")
        print("⚠️  Consider consensus discussion for disputed verses")
    else:
        print("❌ LOW AGREEMENT: Significant issues detected")
        print("❌ Expert discussion and re-annotation recommended")


if __name__ == '__main__':
    main()
