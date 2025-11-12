#!/usr/bin/env python3
"""
Analyze the expansion file for duplicates and coverage.
"""

import json
from collections import Counter, defaultdict
from pathlib import Path

def load_jsonl(filepath):
    """Load JSONL file and return list of records."""
    verses = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                verses.append(json.loads(line))
    return verses

def check_duplicates(expansion_verses, original_verses=None):
    """Check for duplicate verses by text and verse_id."""
    print("\n" + "="*80)
    print("DUPLICATE CHECK")
    print("="*80)

    # Check duplicate verse_ids
    verse_ids = [v['verse_id'] for v in expansion_verses]
    id_counts = Counter(verse_ids)
    duplicates_found = False

    if original_verses:
        original_ids = {v['verse_id'] for v in original_verses}
        overlap_ids = set(verse_ids) & original_ids
        if overlap_ids:
            print(f"\n❌ Found {len(overlap_ids)} verse_id(s) that overlap with original dataset:")
            for vid in sorted(overlap_ids):
                print(f"  - {vid}")
            duplicates_found = True

    duplicate_ids = [vid for vid, count in id_counts.items() if count > 1]
    if duplicate_ids:
        print(f"\n❌ Found {len(duplicate_ids)} duplicate verse_id(s) within expansion:")
        for vid in sorted(duplicate_ids):
            print(f"  - {vid} (appears {id_counts[vid]} times)")
        duplicates_found = True

    # Check duplicate normalized texts
    all_verses = expansion_verses + (original_verses if original_verses else [])
    text_to_verses = defaultdict(list)
    for v in all_verses:
        text_to_verses[v['normalized_text']].append(v['verse_id'])

    duplicate_texts = {text: verses for text, verses in text_to_verses.items() if len(verses) > 1}
    if duplicate_texts:
        print(f"\n❌ Found {len(duplicate_texts)} duplicate verse text(s):")
        for text, verse_ids in sorted(duplicate_texts.items())[:10]:  # Show first 10
            print(f"  - '{text[:60]}...' appears in: {', '.join(verse_ids)}")
        if len(duplicate_texts) > 10:
            print(f"  ... and {len(duplicate_texts) - 10} more")
        duplicates_found = True

    if not duplicates_found:
        print("\n✅ No duplicates found!")

    return not duplicates_found

def analyze_coverage(expansion_verses, original_verses=None):
    """Analyze meter coverage."""
    print("\n" + "="*80)
    print("METER COVERAGE ANALYSIS")
    print("="*80)

    # Count meters in expansion
    expansion_meters = Counter(v['meter'] for v in expansion_verses)

    print(f"\n📊 Expansion file contains {len(expansion_verses)} verses:")
    for meter, count in expansion_meters.most_common():
        print(f"  {meter}: {count} verses")

    if original_verses:
        original_meters = Counter(v['meter'] for v in original_verses)
        combined_meters = Counter()
        for meter in set(list(expansion_meters.keys()) + list(original_meters.keys())):
            combined_meters[meter] = expansion_meters.get(meter, 0) + original_meters.get(meter, 0)

        print(f"\n📊 Combined dataset would have {len(expansion_verses) + len(original_verses)} verses:")
        for meter, count in combined_meters.most_common():
            orig = original_meters.get(meter, 0)
            exp = expansion_meters.get(meter, 0)
            print(f"  {meter}: {count} verses (original: {orig}, expansion: +{exp})")

        # Identify underrepresented meters
        print("\n📋 Meters that still need more verses (target: 15+ each):")
        underrepresented = []
        for meter, count in sorted(combined_meters.items(), key=lambda x: x[1]):
            if count < 15:
                underrepresented.append((meter, count))
                print(f"  ⚠️  {meter}: {count} verses (need {15-count} more)")

        if not underrepresented:
            print("  ✅ All meters have at least 15 verses!")

        return combined_meters, underrepresented

    return expansion_meters, []

def check_schema_compliance(expansion_verses):
    """Check if all verses comply with the expected schema."""
    print("\n" + "="*80)
    print("SCHEMA COMPLIANCE CHECK")
    print("="*80)

    required_fields = ['verse_id', 'text', 'normalized_text', 'meter', 'poet',
                      'poem_title', 'source', 'prosody_precomputed', 'validation', 'metadata']

    issues = []
    for v in expansion_verses:
        for field in required_fields:
            if field not in v:
                issues.append(f"Verse {v.get('verse_id', 'UNKNOWN')} missing field: {field}")

    if issues:
        print(f"\n❌ Found {len(issues)} schema compliance issue(s):")
        for issue in issues[:20]:  # Show first 20
            print(f"  - {issue}")
        if len(issues) > 20:
            print(f"  ... and {len(issues) - 20} more")
    else:
        print("\n✅ All verses comply with the schema!")

    return len(issues) == 0

def main():
    base_dir = Path(__file__).parent.parent
    expansion_file = base_dir / "dataset" / "evaluation" / "golden_set_v1_1_expansion.jsonl"
    original_file = base_dir / "dataset" / "evaluation" / "golden_set_v1_0_with_patterns.jsonl"

    print("\n🔍 BAHR Golden Set Expansion Analysis")
    print("="*80)

    # Load files
    print(f"\n📂 Loading expansion file: {expansion_file}")
    expansion_verses = load_jsonl(expansion_file)
    print(f"   Loaded {len(expansion_verses)} verses")

    original_verses = None
    if original_file.exists():
        print(f"\n📂 Loading original file: {original_file}")
        original_verses = load_jsonl(original_file)
        print(f"   Loaded {len(original_verses)} verses")

    # Run checks
    schema_ok = check_schema_compliance(expansion_verses)
    no_duplicates = check_duplicates(expansion_verses, original_verses)
    combined_meters, underrepresented = analyze_coverage(expansion_verses, original_verses)

    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"✅ Schema compliance: {'PASS' if schema_ok else 'FAIL'}")
    print(f"✅ No duplicates: {'PASS' if no_duplicates else 'FAIL'}")
    print(f"📊 Expansion verses: {len(expansion_verses)}")
    if original_verses:
        print(f"📊 Original verses: {len(original_verses)}")
        print(f"📊 Total verses: {len(expansion_verses) + len(original_verses)}")
        print(f"📊 Meters needing work: {len(underrepresented)}")

    print("\n" + "="*80)

if __name__ == "__main__":
    main()
