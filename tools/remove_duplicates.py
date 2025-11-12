#!/usr/bin/env python3
"""
Remove duplicate verses from the expansion file.
"""

import json
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

def save_jsonl(verses, filepath):
    """Save verses to JSONL file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        for verse in verses:
            f.write(json.dumps(verse, ensure_ascii=False) + '\n')

def remove_duplicates(expansion_verses, original_verses):
    """Remove verses from expansion that duplicate original dataset."""
    # Get all normalized texts from original
    original_texts = {v['normalized_text'] for v in original_verses}

    # Filter expansion verses
    unique_verses = []
    removed = []

    for verse in expansion_verses:
        if verse['normalized_text'] in original_texts:
            removed.append(verse)
            print(f"❌ Removing duplicate: {verse['verse_id']} - '{verse['normalized_text'][:50]}...'")
        else:
            unique_verses.append(verse)
            # Add to original_texts to avoid duplicates within expansion
            original_texts.add(verse['normalized_text'])

    print(f"\n✅ Removed {len(removed)} duplicate verse(s)")
    print(f"✅ Kept {len(unique_verses)} unique verse(s)")

    return unique_verses, removed

def main():
    base_dir = Path(__file__).parent.parent
    expansion_file = base_dir / "dataset" / "evaluation" / "golden_set_v1_1_expansion.jsonl"
    original_file = base_dir / "dataset" / "evaluation" / "golden_set_v1_0_with_patterns.jsonl"
    backup_file = base_dir / "dataset" / "evaluation" / "golden_set_v1_1_expansion.jsonl.backup"

    print("\n🧹 Removing Duplicates from Expansion File")
    print("="*80)

    # Load files
    print(f"\n📂 Loading files...")
    expansion_verses = load_jsonl(expansion_file)
    original_verses = load_jsonl(original_file)
    print(f"   Expansion: {len(expansion_verses)} verses")
    print(f"   Original: {len(original_verses)} verses")

    # Create backup
    print(f"\n💾 Creating backup at: {backup_file}")
    save_jsonl(expansion_verses, backup_file)

    # Remove duplicates
    print(f"\n🔍 Checking for duplicates...")
    unique_verses, removed = remove_duplicates(expansion_verses, original_verses)

    # Save cleaned file
    print(f"\n💾 Saving cleaned expansion file...")
    save_jsonl(unique_verses, expansion_file)

    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Original expansion verses: {len(expansion_verses)}")
    print(f"Removed duplicates: {len(removed)}")
    print(f"Final unique verses: {len(unique_verses)}")
    print(f"Backup saved to: {backup_file}")
    print("\n✅ Done!")
    print("="*80)

if __name__ == "__main__":
    main()
