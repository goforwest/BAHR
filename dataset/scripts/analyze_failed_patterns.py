#!/usr/bin/env python3
"""
Analyze failed verses to extract their actual phonetic patterns.

This script helps improve the prosody engine by showing what patterns
the failed verses actually have, so we can add them to BAHRS_DATA.

Usage:
    python analyze_failed_patterns.py
"""

import sys
import json
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from app.core.normalization import normalize_arabic_text, has_diacritics
from app.core.phonetics import text_to_phonetic_pattern


def analyze_failed_verses():
    """Analyze phonetic patterns of failed verses."""
    
    # Load test report
    report_path = Path(__file__).parent.parent / "evaluation" / "prosody_test_report.json"
    with open(report_path, 'r', encoding='utf-8') as f:
        report = json.load(f)
    
    # Load golden set
    golden_set_path = Path(__file__).parent.parent / "evaluation" / "golden_set_v0_100_complete.jsonl"
    verses = {}
    with open(golden_set_path, 'r', encoding='utf-8') as f:
        for line in f:
            verse = json.loads(line)
            verses[verse['verse_id']] = verse
    
    print("=" * 80)
    print("FAILED VERSES PHONETIC PATTERN ANALYSIS")
    print("=" * 80)
    print()
    
    # Group by meter
    by_meter = {}
    for failed in report['failed_verses']:
        meter = failed['expected']
        if meter not in by_meter:
            by_meter[meter] = []
        
        verse_id = failed['verse_id']
        verse = verses[verse_id]
        
        # Extract phonetic pattern
        normalized = normalize_arabic_text(verse['text'])
        has_tash = has_diacritics(verse['text'])
        phonetic_pattern = text_to_phonetic_pattern(normalized, has_tash)
        
        by_meter[meter].append({
            'verse_id': verse_id,
            'text': verse['text'],
            'phonetic_pattern': phonetic_pattern,
            'predicted': failed['predicted'],
            'confidence': failed['confidence']
        })
    
    # Print by meter
    for meter, failed_verses in sorted(by_meter.items()):
        print(f"\n{'=' * 80}")
        print(f"Meter: {meter}")
        print(f"Failed: {len(failed_verses)} verses")
        print(f"{'=' * 80}\n")
        
        for v in failed_verses:
            print(f"Verse: {v['verse_id']}")
            print(f"Text: {v['text'][:60]}...")
            print(f"Pattern: {v['phonetic_pattern']}")
            print(f"Predicted as: {v['predicted']} (confidence: {v['confidence']:.2f})")
            print()
        
        # Show patterns to add
        print(f"PATTERNS TO ADD TO BAHRS_DATA for '{meter}':")
        print('"phonetic_patterns": [')
        for v in failed_verses:
            print(f'    "{v["phonetic_pattern"]}",  # {v["verse_id"]}')
        print('],')
        print()
    
    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print()
    print(f"Total failed verses: {len(report['failed_verses'])}")
    print(f"Meters needing improvement:")
    for meter, failed_verses in sorted(by_meter.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"  - {meter}: {len(failed_verses)} failed verses")
    print()


if __name__ == "__main__":
    analyze_failed_verses()
