#!/usr/bin/env python3
"""
Merge successful verses from v1.2 phase 1 into v1.1
Only merge verses with valid patterns (المقتضب and المضارع)
"""

import json
from pathlib import Path
from collections import Counter

def load_jsonl(filepath):
    """Load JSONL file."""
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
    v1_1_file = base_dir / "dataset" / "evaluation" / "golden_set_v1_1_merged.jsonl"
    v1_2_phase1_file = base_dir / "dataset" / "evaluation" / "golden_set_v1_2_expansion_phase1.jsonl"
    v1_2_partial_file = base_dir / "dataset" / "evaluation" / "golden_set_v1_2_partial.jsonl"

    print("\n" + "="*80)
    print("MERGING V1.2 PHASE 1 SUCCESSFUL VERSES INTO V1.1")
    print("="*80)
    print()

    # Load files
    print("📂 Loading files...")
    v1_1_verses = load_jsonl(v1_1_file)
    v1_2_phase1_verses = load_jsonl(v1_2_phase1_file)

    print(f"   v1.1: {len(v1_1_verses)} verses")
    print(f"   v1.2 phase 1: {len(v1_2_phase1_verses)} verses")

    # Filter only verses with valid patterns
    successful_verses = []
    failed_verses = []

    for verse in v1_2_phase1_verses:
        pattern = verse.get('prosody_precomputed', {}).get('pattern')
        if pattern and pattern != 'to be computed' and pattern is not None:
            successful_verses.append(verse)
        else:
            failed_verses.append(verse)

    print(f"\n✅ Successfully computed patterns: {len(successful_verses)} verses")
    print(f"❌ Failed pattern computation: {len(failed_verses)} verses")

    # Show what succeeded
    success_meters = Counter(v['meter'] for v in successful_verses)
    print(f"\n📊 Successful verses by meter:")
    for meter, count in sorted(success_meters.items(), key=lambda x: -x[1]):
        print(f"   {meter}: {count} verses")

    # Show what failed
    failed_meters = Counter(v['meter'] for v in failed_verses)
    print(f"\n⚠️  Failed verses by meter (new variant forms):")
    for meter, count in sorted(failed_meters.items(), key=lambda x: -x[1]):
        print(f"   {meter}: {count} verses")

    # Merge
    print(f"\n🔗 Merging successful verses...")
    all_verses = v1_1_verses + successful_verses

    # Sort by verse_id
    all_verses.sort(key=lambda v: int(v['verse_id'].replace('golden_', '')))

    print(f"   Total verses in v1.2 (partial): {len(all_verses)}")

    # Save
    print(f"\n💾 Saving to: {v1_2_partial_file}")
    save_jsonl(all_verses, v1_2_partial_file)

    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"✅ v1.1 verses: {len(v1_1_verses)}")
    print(f"✅ New verses added: {len(successful_verses)}")
    print(f"   - المقتضب: +{success_meters.get('المقتضب', 0)} (total: {sum(1 for v in all_verses if v['meter'] == 'المقتضب')})")
    print(f"   - المضارع: +{success_meters.get('المضارع', 0)} (total: {sum(1 for v in all_verses if v['meter'] == 'المضارع')})")
    print(f"✅ Total v1.2 (partial): {len(all_verses)} verses")
    print(f"\n⚠️  Variant forms (for future work): {len(failed_verses)} verses")
    print(f"   - مشطور forms: {sum(1 for v in failed_verses if 'مشطور' in v['meter'])}")
    print(f"   - New مجزوء forms: {sum(1 for v in failed_verses if 'مجزوء' in v['meter'])}")
    print("\n" + "="*80)

if __name__ == "__main__":
    main()
