"""
Merge السريع expansion verses into main golden set
"""

import json
from pathlib import Path

def load_jsonl(file_path):
    """Load JSONL file"""
    verses = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                verses.append(json.loads(line))
    return verses

def save_jsonl(verses, file_path):
    """Save verses to JSONL file"""
    with open(file_path, 'w', encoding='utf-8') as f:
        for verse in verses:
            f.write(json.dumps(verse, ensure_ascii=False) + '\n')
    print(f"✓ Saved {len(verses)} verses to {file_path}")

def main():
    """Main execution"""
    print("=" * 60)
    print("MERGING السريع EXPANSION INTO MAIN DATASET")
    print("=" * 60)

    # Load main dataset (enhanced version)
    main_path = Path("dataset/evaluation/golden_set_v1_2_final_enhanced.jsonl")
    print(f"\n1. Loading main dataset: {main_path}")
    main_verses = load_jsonl(main_path)
    print(f"   Total verses: {len(main_verses)}")

    # Count السريع in main dataset
    sari_count = sum(1 for v in main_verses if v['meter'] == 'السريع')
    print(f"   السريع verses: {sari_count}")

    # Load السريع expansion
    expansion_path = Path("dataset/evaluation/golden_set_v1_3_sari_expansion_precomputed.jsonl")
    print(f"\n2. Loading السريع expansion: {expansion_path}")
    expansion_verses = load_jsonl(expansion_path)
    print(f"   New السريع verses: {len(expansion_verses)}")

    # Check all have precomputed patterns
    with_patterns = sum(1 for v in expansion_verses if 'prosody_precomputed' in v)
    print(f"   With patterns: {with_patterns}/{len(expansion_verses)}")

    # Merge
    print(f"\n3. Merging datasets...")
    merged_verses = main_verses + expansion_verses
    print(f"   Total verses: {len(merged_verses)}")

    # Count السريع in merged dataset
    sari_merged = sum(1 for v in merged_verses if v['meter'] == 'السريع')
    print(f"   السريع verses: {sari_merged}")

    # Save merged dataset
    output_path = Path("dataset/evaluation/golden_set_v1_3_with_sari.jsonl")
    print(f"\n4. Saving merged dataset: {output_path}")
    save_jsonl(merged_verses, output_path)

    # Statistics by meter
    print("\n" + "=" * 60)
    print("METER DISTRIBUTION")
    print("=" * 60)

    meter_counts = {}
    for verse in merged_verses:
        meter = verse['meter']
        meter_counts[meter] = meter_counts.get(meter, 0) + 1

    for meter, count in sorted(meter_counts.items(), key=lambda x: -x[1]):
        print(f"  {meter:30s}: {count:3d} verses")

    print("\n" + "=" * 60)
    print("✓ MERGE COMPLETE!")
    print("=" * 60)
    print(f"\nOutput: {output_path}")
    print(f"Total verses: {len(merged_verses)}")
    print(f"السريع verses: {sari_count} → {sari_merged} (+{len(expansion_verses)})")
    print("\nNext step: Run evaluation to check accuracy")

if __name__ == "__main__":
    main()
