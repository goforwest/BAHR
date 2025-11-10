#!/usr/bin/env python3
"""
Golden Set Usage Examples

Demonstrates common patterns for loading and using the BAHR Golden Set dataset.
"""

import json
from pathlib import Path
from typing import List, Dict, Any
from collections import defaultdict


class GoldenSetLoader:
    """Helper class for loading and querying the Golden Set."""
    
    def __init__(self, jsonl_path: str):
        """
        Initialize the loader with path to golden set JSONL file.
        
        Args:
            jsonl_path: Path to golden_set_v0_20_complete.jsonl
        """
        self.jsonl_path = Path(jsonl_path)
        self.verses = self._load_verses()
    
    def _load_verses(self) -> List[Dict[str, Any]]:
        """Load all verses from JSONL file."""
        verses = []
        with open(self.jsonl_path, 'r', encoding='utf-8') as f:
            for line in f:
                verses.append(json.loads(line))
        return verses
    
    def get_by_id(self, verse_id: str) -> Dict[str, Any]:
        """Get a specific verse by ID."""
        for verse in self.verses:
            if verse['verse_id'] == verse_id:
                return verse
        raise KeyError(f"Verse {verse_id} not found")
    
    def get_by_meter(self, meter: str) -> List[Dict[str, Any]]:
        """Get all verses in a specific meter."""
        return [v for v in self.verses if v['meter'] == meter]
    
    def get_by_difficulty(self, level: str) -> List[Dict[str, Any]]:
        """Get verses by difficulty level."""
        return [v for v in self.verses if v['difficulty_level'] == level]
    
    def get_by_edge_case(self, edge_type: str) -> List[Dict[str, Any]]:
        """Get verses by edge case type."""
        return [v for v in self.verses if v['edge_case_type'] == edge_type]
    
    def get_high_confidence(self, threshold: float = 0.95) -> List[Dict[str, Any]]:
        """Get verses with confidence >= threshold."""
        return [v for v in self.verses if v['confidence'] >= threshold]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get dataset statistics."""
        return {
            'total_verses': len(self.verses),
            'meter_distribution': self._count_by_field('meter'),
            'difficulty_distribution': self._count_by_field('difficulty_level'),
            'edge_case_distribution': self._count_by_field('edge_case_type'),
            'average_confidence': sum(v['confidence'] for v in self.verses) / len(self.verses),
            'average_syllable_count': sum(v['syllable_count'] for v in self.verses) / len(self.verses),
            'unique_poets': len(set(v.get('poet') for v in self.verses if v.get('poet')))
        }
    
    def _count_by_field(self, field: str) -> Dict[str, int]:
        """Count occurrences of each value in a field."""
        counts = defaultdict(int)
        for verse in self.verses:
            value = verse.get(field)
            if value:
                counts[value] += 1
        return dict(counts)


# ============================================================================
# EXAMPLE 1: Basic Loading and Statistics
# ============================================================================

def example_basic_usage():
    """Basic usage: load dataset and get statistics."""
    print("=" * 70)
    print("EXAMPLE 1: Basic Usage")
    print("=" * 70)
    
    # Load the golden set
    loader = GoldenSetLoader('../evaluation/golden_set_v0_20_complete.jsonl')
    
    # Get statistics
    stats = loader.get_statistics()
    
    print(f"\nDataset Statistics:")
    print(f"  Total verses: {stats['total_verses']}")
    print(f"  Average confidence: {stats['average_confidence']:.3f}")
    print(f"  Average syllable count: {stats['average_syllable_count']:.1f}")
    print(f"  Unique poets: {stats['unique_poets']}")
    
    print(f"\nMeter Distribution:")
    for meter, count in sorted(stats['meter_distribution'].items()):
        print(f"  {meter}: {count}")
    
    print(f"\nDifficulty Distribution:")
    for level, count in stats['difficulty_distribution'].items():
        print(f"  {level}: {count}")


# ============================================================================
# EXAMPLE 2: Testing Meter Detection
# ============================================================================

def example_test_meter_detection(engine):
    """Test a meter detection engine against the golden set."""
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Testing Meter Detection Engine")
    print("=" * 70)
    
    loader = GoldenSetLoader('../evaluation/golden_set_v0_20_complete.jsonl')
    
    results = {
        'total': 0,
        'correct': 0,
        'incorrect': 0,
        'by_difficulty': defaultdict(lambda: {'total': 0, 'correct': 0}),
        'errors': []
    }
    
    for verse in loader.verses:
        results['total'] += 1
        difficulty = verse['difficulty_level']
        results['by_difficulty'][difficulty]['total'] += 1
        
        # Run your engine (placeholder)
        predicted_meter = engine.detect_meter(verse['text'])
        expected_meter = verse['meter']
        
        if predicted_meter == expected_meter:
            results['correct'] += 1
            results['by_difficulty'][difficulty]['correct'] += 1
        else:
            results['incorrect'] += 1
            results['errors'].append({
                'verse_id': verse['verse_id'],
                'text': verse['text'][:50] + '...',
                'expected': expected_meter,
                'predicted': predicted_meter,
                'confidence': verse['confidence']
            })
    
    # Print results
    overall_acc = results['correct'] / results['total']
    print(f"\nOverall Accuracy: {overall_acc:.1%} ({results['correct']}/{results['total']})")
    
    print(f"\nAccuracy by Difficulty:")
    for level in ['easy', 'medium', 'hard']:
        if level in results['by_difficulty']:
            stats = results['by_difficulty'][level]
            acc = stats['correct'] / stats['total'] if stats['total'] > 0 else 0
            print(f"  {level.capitalize()}: {acc:.1%} ({stats['correct']}/{stats['total']})")
    
    if results['errors']:
        print(f"\nErrors ({len(results['errors'])}):")
        for err in results['errors'][:5]:  # Show first 5
            print(f"  {err['verse_id']}: Expected '{err['expected']}', got '{err['predicted']}'")


# ============================================================================
# EXAMPLE 3: Syllable Pattern Verification
# ============================================================================

def example_verify_syllable_patterns(syllable_segmenter):
    """Verify syllable segmentation against golden set patterns."""
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Verify Syllable Segmentation")
    print("=" * 70)
    
    loader = GoldenSetLoader('../evaluation/golden_set_v0_20_complete.jsonl')
    
    matches = 0
    mismatches = []
    
    for verse in loader.verses:
        # Generate pattern from your segmenter
        generated_pattern = syllable_segmenter.segment(verse['normalized_text'])
        expected_pattern = verse['syllable_pattern']
        
        if generated_pattern == expected_pattern:
            matches += 1
        else:
            mismatches.append({
                'verse_id': verse['verse_id'],
                'expected': expected_pattern,
                'generated': generated_pattern,
                'meter': verse['meter']
            })
    
    total = len(loader.verses)
    accuracy = matches / total
    
    print(f"\nSyllable Pattern Accuracy: {accuracy:.1%} ({matches}/{total})")
    
    if mismatches:
        print(f"\nMismatches ({len(mismatches)}):")
        for mm in mismatches[:3]:  # Show first 3
            print(f"\n  {mm['verse_id']} ({mm['meter']}):")
            print(f"    Expected:  {mm['expected']}")
            print(f"    Generated: {mm['generated']}")


# ============================================================================
# EXAMPLE 4: Filtering by Characteristics
# ============================================================================

def example_filtering():
    """Filter verses by various characteristics."""
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Filtering Verses")
    print("=" * 70)
    
    loader = GoldenSetLoader('../evaluation/golden_set_v0_20_complete.jsonl')
    
    # Get easy verses for initial testing
    easy_verses = loader.get_by_difficulty('easy')
    print(f"\nEasy verses: {len(easy_verses)}")
    for v in easy_verses[:3]:
        print(f"  - {v['verse_id']}: {v['meter']}")
    
    # Get perfect match cases (no variations)
    perfect = loader.get_by_edge_case('perfect_match')
    print(f"\nPerfect match verses: {len(perfect)}")
    
    # Get high-confidence verses
    high_conf = loader.get_high_confidence(0.95)
    print(f"\nHigh confidence (≥0.95) verses: {len(high_conf)}")
    
    # Get specific meter
    tawil = loader.get_by_meter('الطويل')
    print(f"\nالطويل meter verses: {len(tawil)}")


# ============================================================================
# EXAMPLE 5: Prosodic Feature Extraction
# ============================================================================

def example_prosodic_features():
    """Extract and analyze prosodic features."""
    print("\n" + "=" * 70)
    print("EXAMPLE 5: Prosodic Feature Analysis")
    print("=" * 70)
    
    loader = GoldenSetLoader('../evaluation/golden_set_v0_20_complete.jsonl')
    
    # Analyze taf'ilah patterns
    tafail_usage = defaultdict(int)
    
    for verse in loader.verses:
        for taf in verse['expected_tafail']:
            tafail_usage[taf] += 1
    
    print("\nMost Common Taf'ilah:")
    for taf, count in sorted(tafail_usage.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {taf}: {count} occurrences")
    
    # Analyze syllable counts
    syllable_counts = defaultdict(int)
    for verse in loader.verses:
        syllable_counts[verse['syllable_count']] += 1
    
    print("\nSyllable Count Distribution:")
    for count in sorted(syllable_counts.keys()):
        print(f"  {count} syllables: {syllable_counts[count]} verses")


# ============================================================================
# EXAMPLE 6: Validation Report Generation
# ============================================================================

def example_generate_report(test_results: List[Dict]):
    """Generate a validation report from test results."""
    print("\n" + "=" * 70)
    print("EXAMPLE 6: Generate Validation Report")
    print("=" * 70)
    
    loader = GoldenSetLoader('../evaluation/golden_set_v0_20_complete.jsonl')
    
    report = {
        'dataset_info': {
            'version': '0.20',
            'total_verses': len(loader.verses),
            'test_date': '2025-11-09'
        },
        'results': {
            'overall_accuracy': 0.0,
            'by_meter': {},
            'by_difficulty': {},
            'confusion_matrix': defaultdict(lambda: defaultdict(int))
        }
    }
    
    # Calculate metrics from test_results
    # (placeholder - would use actual test results)
    
    # Save report
    output_path = Path('validation_report_custom.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Report saved to: {output_path}")


# ============================================================================
# MAIN: Run all examples
# ============================================================================

def main():
    """Run all examples (some require mock implementations)."""
    print("\n🎯 BAHR Golden Set - Usage Examples\n")
    
    # Example 1: Basic usage (works standalone)
    example_basic_usage()
    
    # Example 4: Filtering (works standalone)
    example_filtering()
    
    # Example 5: Prosodic features (works standalone)
    example_prosodic_features()
    
    print("\n" + "=" * 70)
    print("ℹ️  Examples 2, 3, and 6 require implementing:")
    print("  - engine.detect_meter(text)")
    print("  - syllable_segmenter.segment(text)")
    print("  - test_results data structure")
    print("=" * 70 + "\n")


if __name__ == '__main__':
    # Run from: dataset/scripts/
    # Adjust paths if running from elsewhere
    main()
