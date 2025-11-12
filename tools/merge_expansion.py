#!/usr/bin/env python3
"""
Merge the expansion file into the main golden set.
"""

import json
from pathlib import Path
from collections import Counter

def load_jsonl(filepath):
    """Load JSONL file and return list of records."""
    verses = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                verses.append(json.loads(line))
    return verses

def save_jsonl(verses, filepath):
    """Save verses to JSONL file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        for verse in verses:
            f.write(json.dumps(verse, ensure_ascii=False) + '\n')

def main():
    base_dir = Path(__file__).parent.parent
    expansion_file = base_dir / "dataset" / "evaluation" / "golden_set_v1_1_expansion.jsonl"
    original_file = base_dir / "dataset" / "evaluation" / "golden_set_v1_0_with_patterns.jsonl"
    merged_file = base_dir / "dataset" / "evaluation" / "golden_set_v1_1_merged.jsonl"
    backup_file = base_dir / "dataset" / "evaluation" / "golden_set_v1_0_with_patterns.jsonl.backup"

    print("\n🔗 Merging Expansion into Main Golden Set")
    print("="*80)

    # Load files
    print(f"\n📂 Loading files...")
    expansion_verses = load_jsonl(expansion_file)
    original_verses = load_jsonl(original_file)
    print(f"   Original: {len(original_verses)} verses")
    print(f"   Expansion: {len(expansion_verses)} verses")

    # Backup original
    print(f"\n💾 Creating backup of original file...")
    save_jsonl(original_verses, backup_file)
    print(f"   Backup saved to: {backup_file}")

    # Merge
    print(f"\n🔗 Merging verses...")
    all_verses = original_verses + expansion_verses
    print(f"   Total verses: {len(all_verses)}")

    # Sort by verse_id to maintain order
    all_verses.sort(key=lambda v: int(v['verse_id'].replace('golden_', '')))

    # Update version metadata
    for verse in all_verses:
        if 'metadata' not in verse:
            verse['metadata'] = {}
        verse['metadata']['dataset_version'] = '1.1'

    # Analyze meter distribution
    print(f"\n📊 Meter distribution in merged dataset:")
    meter_counts = Counter(v['meter'] for v in all_verses)
    for meter, count in sorted(meter_counts.items(), key=lambda x: -x[1]):
        print(f"   {meter}: {count} verses")

    # Save merged file
    print(f"\n💾 Saving merged golden set to: {merged_file}")
    save_jsonl(all_verses, merged_file)

    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"✅ Original verses: {len(original_verses)}")
    print(f"✅ Expansion verses: {len(expansion_verses)}")
    print(f"✅ Total merged verses: {len(all_verses)}")
    print(f"✅ Unique meters: {len(meter_counts)}")
    print(f"✅ Output file: {merged_file}")
    print(f"✅ Backup file: {backup_file}")
    print("\n✅ Merge completed successfully!")
    print("="*80)

if __name__ == "__main__":
    main()
