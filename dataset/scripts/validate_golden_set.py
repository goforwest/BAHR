#!/usr/bin/env python3
"""Validate the fully annotated Golden Set."""

import json
from pathlib import Path
from collections import Counter

def validate_golden_set(filepath: str):
    """Validate completeness and quality of golden set."""
    
    print("🔍 GOLDEN SET VALIDATION REPORT")
    print("=" * 70)
    
    # Load data
    with open(filepath, 'r', encoding='utf-8') as f:
        verses = [json.loads(line) for line in f]
    
    print(f"\n📊 BASIC STATS:")
    print(f"   Total verses: {len(verses)}")
    
    # Required fields
    required_fields = [
        'verse_id', 'text', 'normalized_text', 'meter', 'poet', 'source',
        'era', 'confidence', 'notes', 'taqti3', 'expected_tafail',
        'syllable_pattern', 'syllable_count'
    ]
    
    print(f"\n✅ FIELD COMPLETENESS:")
    all_complete = True
    for field in required_fields:
        count = sum(1 for v in verses if field in v)
        status = "✅" if count == len(verses) else "❌"
        print(f"   {status} {field}: {count}/{len(verses)}")
        if count != len(verses):
            all_complete = False
    
    # Check for non-empty critical fields
    print(f"\n✅ NON-EMPTY CRITICAL FIELDS:")
    critical_fields = ['text', 'meter', 'taqti3', 'expected_tafail', 'syllable_pattern']
    for field in critical_fields:
        count = sum(1 for v in verses if field in v and v[field])
        status = "✅" if count == len(verses) else "❌"
        print(f"   {status} {field}: {count}/{len(verses)} non-empty")
        if count != len(verses):
            all_complete = False
    
    # Meter distribution
    print(f"\n📈 METER DISTRIBUTION:")
    meters = Counter(v['meter'] for v in verses)
    for meter, count in sorted(meters.items(), key=lambda x: -x[1]):
        print(f"   {meter}: {count} verses")
    
    # Syllable count distribution
    print(f"\n📏 SYLLABLE COUNT DISTRIBUTION:")
    syllables = Counter(v['syllable_count'] for v in verses if 'syllable_count' in v)
    for count, freq in sorted(syllables.items()):
        print(f"   {count} syllables: {freq} verses")
    
    # Tafa'il count distribution
    print(f"\n🔢 TAFA'IL COUNT DISTRIBUTION:")
    tafail_counts = Counter(len(v['expected_tafail']) for v in verses if 'expected_tafail' in v)
    for count, freq in sorted(tafail_counts.items()):
        print(f"   {count} tafa'il: {freq} verses")
    
    # Check for issues
    print(f"\n⚠️  POTENTIAL ISSUES:")
    issues_found = False
    
    # Check for "???" in syllable patterns
    verses_with_unknown = [v for v in verses if 'syllable_pattern' in v and '???' in v['syllable_pattern']]
    if verses_with_unknown:
        issues_found = True
        print(f"   ⚠️  {len(verses_with_unknown)} verses have unmapped syllable patterns (???)")
        for v in verses_with_unknown:
            print(f"      - {v['verse_id']}: {v['meter']} - {v['taqti3']}")
    
    # Check for empty poet names
    verses_without_poet = [v for v in verses if not v.get('poet', '').strip()]
    if verses_without_poet:
        print(f"   ℹ️  {len(verses_without_poet)} verses have no poet name (generic sources)")
    
    # Check confidence scores
    low_confidence = [v for v in verses if v.get('confidence', 1.0) < 0.9]
    if low_confidence:
        print(f"   ℹ️  {len(low_confidence)} verses have confidence < 0.9")
    
    if not issues_found and not verses_without_poet and not low_confidence:
        print(f"   ✅ No critical issues found!")
    
    # Overall status
    print(f"\n" + "=" * 70)
    if all_complete and not issues_found:
        print("✅ VALIDATION PASSED - Golden Set is ready for use!")
    elif all_complete:
        print("⚠️  VALIDATION PASSED WITH WARNINGS - Minor issues found")
    else:
        print("❌ VALIDATION FAILED - Missing required fields")
    print("=" * 70)
    
    return verses

if __name__ == "__main__":
    filepath = Path(__file__).parent.parent / "evaluation" / "golden_set_v0_20_fully_annotated.jsonl"
    validate_golden_set(str(filepath))
