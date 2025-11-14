#!/usr/bin/env python3
"""
Build Consensus Labels from Expert Annotations

This script takes multiple expert annotations and creates consensus labels
using majority voting and confidence weighting.

Usage:
    python build_consensus.py --annotations expert1.csv expert2.csv expert3.csv
    python build_consensus.py --dir phase3_materials/annotations/ --output consensus.json
    python build_consensus.py --annotations *.csv --mapping verse_id_mapping_CONFIDENTIAL.json
"""

import argparse
import json
import csv
from pathlib import Path
from collections import Counter
from typing import List, Dict
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
                'confidence': int(row['confidence_1to5']) if row['confidence_1to5'] else 3,
                'alternative_meter': row['alternative_meter'].strip() if row['alternative_meter'] else None,
                'tafail': row['tafail_scansion'].strip() if row['tafail_scansion'] else None,
                'zihafat': row['zihafat_positions'].strip() if row['zihafat_positions'] else None,
                'ilal': row['ilal_final'].strip() if row['ilal_final'] else None,
                'valid_example': row['valid_example'].strip() if row['valid_example'] else None,
                'naturalness': int(row['naturalness_1to5']) if row['naturalness_1to5'] else None,
                'notes': row['disambiguation_notes'].strip() if row['disambiguation_notes'] else ''
            }
    return annotations


def build_consensus_simple_majority(annotations_by_expert: List[Dict], expert_names: List[str]) -> Dict:
    """Build consensus using simple majority voting."""
    verse_ids = sorted(annotations_by_expert[0].keys())
    consensus = {}

    for verse_id in verse_ids:
        # Collect all meters for this verse
        meters = [expert[verse_id]['primary_meter'] for expert in annotations_by_expert
                 if expert[verse_id]['primary_meter']]

        if not meters:
            consensus[verse_id] = {
                'consensus_meter': None,
                'agreement_type': 'no_annotations',
                'vote_distribution': {},
                'confidence': 0,
                'notes': 'No annotations provided'
            }
            continue

        # Count votes
        meter_counts = Counter(meters)
        most_common_meter, most_common_count = meter_counts.most_common(1)[0]

        # Calculate agreement
        agreement_rate = most_common_count / len(meters)

        # Determine agreement type
        if agreement_rate == 1.0:
            agreement_type = 'unanimous'
        elif agreement_rate >= 0.80:
            agreement_type = 'strong_majority'
        elif agreement_rate >= 0.60:
            agreement_type = 'majority'
        else:
            agreement_type = 'disputed'

        # Collect tafāʿīl from majority voters
        majority_tafail = []
        for i, expert in enumerate(annotations_by_expert):
            if expert[verse_id]['primary_meter'] == most_common_meter:
                if expert[verse_id]['tafail']:
                    majority_tafail.append(expert[verse_id]['tafail'])

        # Most common tafāʿīl among majority
        consensus_tafail = None
        if majority_tafail:
            tafail_counts = Counter(majority_tafail)
            consensus_tafail = tafail_counts.most_common(1)[0][0]

        # Average confidence from majority voters
        majority_confidences = [
            annotations_by_expert[i][verse_id]['confidence']
            for i, expert in enumerate(annotations_by_expert)
            if expert[verse_id]['primary_meter'] == most_common_meter
            and annotations_by_expert[i][verse_id]['confidence']
        ]
        avg_confidence = sum(majority_confidences) / len(majority_confidences) if majority_confidences else 3

        consensus[verse_id] = {
            'consensus_meter': most_common_meter,
            'agreement_type': agreement_type,
            'agreement_rate': round(agreement_rate, 3),
            'vote_distribution': dict(meter_counts),
            'confidence': round(avg_confidence, 2),
            'consensus_tafail': consensus_tafail,
            'n_voters': len(meters),
            'voters_agreeing': most_common_count
        }

    return consensus


def build_consensus_confidence_weighted(annotations_by_expert: List[Dict], expert_names: List[str]) -> Dict:
    """Build consensus using confidence-weighted voting."""
    verse_ids = sorted(annotations_by_expert[0].keys())
    consensus = {}

    for verse_id in verse_ids:
        # Collect meters with confidence weights
        weighted_votes = {}

        for expert in annotations_by_expert:
            meter = expert[verse_id]['primary_meter']
            confidence = expert[verse_id]['confidence'] or 3

            if meter:
                if meter not in weighted_votes:
                    weighted_votes[meter] = 0
                weighted_votes[meter] += confidence

        if not weighted_votes:
            consensus[verse_id] = {
                'consensus_meter': None,
                'method': 'confidence_weighted',
                'weighted_score': 0,
                'notes': 'No annotations provided'
            }
            continue

        # Find meter with highest weighted score
        best_meter = max(weighted_votes, key=weighted_votes.get)
        best_score = weighted_votes[best_meter]
        total_score = sum(weighted_votes.values())

        weighted_agreement = best_score / total_score if total_score > 0 else 0

        consensus[verse_id] = {
            'consensus_meter': best_meter,
            'method': 'confidence_weighted',
            'weighted_agreement': round(weighted_agreement, 3),
            'weighted_scores': weighted_votes,
            'total_weight': total_score
        }

    return consensus


def compare_with_expected(consensus: Dict, mapping_file: str) -> Dict:
    """Compare consensus labels with expected labels from dataset."""
    with open(mapping_file, 'r', encoding='utf-8') as f:
        mapping = json.load(f)

    comparison = {}

    for verse_id, cons_data in consensus.items():
        if verse_id not in mapping['mapping']:
            comparison[verse_id] = {
                'status': 'no_mapping',
                'notes': 'Verse not found in mapping file'
            }
            continue

        expected = mapping['mapping'][verse_id]['expected_meter']
        consensus_meter = cons_data.get('consensus_meter')

        match = (expected == consensus_meter)

        comparison[verse_id] = {
            'expected_meter': expected,
            'consensus_meter': consensus_meter,
            'match': match,
            'expected_tafail': mapping['mapping'][verse_id]['expected_tafail'],
            'source': mapping['mapping'][verse_id]['source'],
            'agreement_type': cons_data.get('agreement_type', 'unknown')
        }

    return comparison


def generate_consensus_report(
    annotations_by_expert: List[Dict],
    expert_names: List[str],
    mapping_file: str = None
) -> Dict:
    """Generate comprehensive consensus report."""

    print(f"\n{'='*80}")
    print(f"CONSENSUS LABEL BUILDING")
    print(f"{'='*80}\n")

    print(f"Experts: {', '.join(expert_names)}")
    verse_ids = sorted(annotations_by_expert[0].keys())
    print(f"Verses: {len(verse_ids)}\n")

    # Build consensus using simple majority
    print(f"{'='*80}")
    print(f"SIMPLE MAJORITY VOTING")
    print(f"{'='*80}\n")

    consensus_majority = build_consensus_simple_majority(annotations_by_expert, expert_names)

    # Summarize agreement types
    agreement_summary = Counter(c['agreement_type'] for c in consensus_majority.values())

    print(f"Agreement Distribution:")
    for agreement_type, count in sorted(agreement_summary.items()):
        pct = count / len(verse_ids) * 100
        print(f"  {agreement_type}: {count} ({pct:.1f}%)")
    print()

    # List disputed verses
    disputed = [v_id for v_id, c in consensus_majority.items()
               if c['agreement_type'] == 'disputed']

    if disputed:
        print(f"⚠️  DISPUTED VERSES (need discussion):")
        for v_id in disputed:
            cons = consensus_majority[v_id]
            print(f"  {v_id}: {cons['vote_distribution']} (confidence: {cons['confidence']:.2f})")
        print()
    else:
        print(f"✅ No disputed verses!\n")

    # Build consensus using confidence weighting
    print(f"{'='*80}")
    print(f"CONFIDENCE-WEIGHTED VOTING")
    print(f"{'='*80}\n")

    consensus_weighted = build_consensus_confidence_weighted(annotations_by_expert, expert_names)

    # Compare methods
    print(f"Comparing majority vs weighted methods:")
    differences = 0
    for v_id in verse_ids:
        maj_meter = consensus_majority[v_id].get('consensus_meter')
        wgt_meter = consensus_weighted[v_id].get('consensus_meter')

        if maj_meter != wgt_meter:
            differences += 1
            print(f"  {v_id}: Majority={maj_meter}, Weighted={wgt_meter}")

    if differences == 0:
        print(f"  ✅ Both methods agree on all verses!")
    else:
        print(f"  ⚠️  {differences} verses differ between methods")
    print()

    # Compare with expected if mapping provided
    comparison = None
    if mapping_file:
        print(f"{'='*80}")
        print(f"COMPARISON WITH EXPECTED LABELS")
        print(f"{'='*80}\n")

        comparison = compare_with_expected(consensus_majority, mapping_file)

        matches = sum(1 for c in comparison.values() if c.get('match', False))
        total = len(comparison)

        print(f"Matches: {matches}/{total} ({matches/total*100:.1f}%)")

        mismatches = [v_id for v_id, c in comparison.items() if not c.get('match', False)]

        if mismatches:
            print(f"\n❌ MISMATCHES:")
            for v_id in mismatches:
                comp = comparison[v_id]
                print(f"  {v_id}: Expected={comp['expected_meter']}, "
                     f"Consensus={comp['consensus_meter']} ({comp['agreement_type']})")
        print()

    # Build final report
    report = {
        'method': 'simple_majority',
        'n_experts': len(expert_names),
        'expert_names': expert_names,
        'n_verses': len(verse_ids),
        'agreement_summary': dict(agreement_summary),
        'consensus_labels': consensus_majority,
        'disputed_verses': disputed,
        'alternative_method': consensus_weighted,
        'comparison_with_expected': comparison
    }

    return report


def main():
    parser = argparse.ArgumentParser(
        description='Build consensus labels from expert annotations'
    )
    parser.add_argument(
        '--annotations',
        nargs='+',
        help='Annotation CSV files'
    )
    parser.add_argument(
        '--dir',
        help='Directory containing annotation CSV files'
    )
    parser.add_argument(
        '--mapping',
        help='Verse ID mapping file (CONFIDENTIAL) to compare with expected labels'
    )
    parser.add_argument(
        '--output',
        default='consensus_labels.json',
        help='Output file for consensus labels (JSON)'
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

        expert_name = Path(file_path).stem.replace('annotation_', '')
        expert_names.append(expert_name)

    # Generate consensus report
    report = generate_consensus_report(
        annotations_by_expert,
        expert_names,
        mapping_file=args.mapping
    )

    # Save report
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"{'='*80}")
    print(f"Consensus report saved to: {args.output}")
    print(f"{'='*80}\n")

    # Final summary
    n_disputed = len(report['disputed_verses'])
    if n_disputed == 0:
        print("✅ SUCCESS: All verses have consensus labels!")
    else:
        print(f"⚠️  {n_disputed} disputed verses need expert discussion")

    if report['comparison_with_expected']:
        comparison = report['comparison_with_expected']
        matches = sum(1 for c in comparison.values() if c.get('match', False))
        total = len(comparison)
        match_rate = matches / total * 100

        if match_rate >= 90:
            print(f"✅ Excellent match with expected labels: {match_rate:.1f}%")
        elif match_rate >= 80:
            print(f"✓ Good match with expected labels: {match_rate:.1f}%")
        else:
            print(f"⚠️  Moderate match with expected labels: {match_rate:.1f}%")


if __name__ == '__main__':
    main()
