#!/usr/bin/env python3
"""
Integrate المتدارك corpus into golden set for Phase 4.

This script:
1. Loads the current golden set
2. Loads our validated المتدارك verses (5 classical + 8 synthetic)
3. Integrates them into the golden set
4. Creates golden_set_v1.0.jsonl with المتدارك coverage
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Paths
GOLDEN_SET_CURRENT = Path('/home/user/BAHR/dataset/evaluation/golden_set_v0_102_comprehensive.jsonl')
MUTADARIK_SHAMELA = Path('/home/user/BAHR/dataset/mutadarik_shamela_candidates.jsonl')
MUTADARIK_SYNTHETIC = Path('/home/user/BAHR/dataset/mutadarik_synthetic_final.jsonl')
GOLDEN_SET_NEW = Path('/home/user/BAHR/dataset/evaluation/golden_set_v1_0_mutadarik.jsonl')


def load_jsonl(file_path):
    """Load JSONL file."""
    verses = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                verses.append(json.loads(line))
    return verses


def save_jsonl(verses, file_path):
    """Save verses to JSONL file."""
    with open(file_path, 'w', encoding='utf-8') as f:
        for verse in verses:
            f.write(json.dumps(verse, ensure_ascii=False) + '\n')


def convert_mutadarik_to_golden_format(verse, verse_number, source_type):
    """Convert المتدارك verse to golden set format."""
    verse_id = f"golden_{verse_number:03d}"

    # Map confidence
    confidence = verse.get('confidence', 1.0)
    if isinstance(confidence, dict):
        confidence = confidence.get('confidence', 0.95)

    # Convert to float if needed
    try:
        confidence = float(confidence)
    except:
        confidence = 0.95

    # Build golden set entry
    golden_entry = {
        "verse_id": verse_id,
        "text": verse.get('text', ''),
        "normalized_text": verse.get('normalized_text', ''),
        "meter": "المتدارك",
        "poet": verse.get('poet', 'synthetic' if source_type == 'synthetic' else 'classical'),
        "source": verse.get('source', ''),
        "era": verse.get('era', source_type),
        "confidence": min(confidence, 1.0),  # Cap at 1.0
        "notes": verse.get('notes', ''),
        "taqti3": verse.get('taqti3', ''),
        "expected_tafail": verse.get('expected_tafail', []),
        "syllable_pattern": verse.get('phonetic_pattern', ''),
        "syllable_count": verse.get('syllable_count', 0),
        "edge_case_type": verse.get('edge_case_type', 'standard'),
        "difficulty_level": verse.get('difficulty_level', 'medium'),
        "validation": {
            "verified_by": "phase2_corpus_sourcing",
            "verified_date": "2025-11-12",
            "automated_check": "PASSED",
            "reference_sources": verse.get('validation', {}).get('reference_sources', [])
        },
        "metadata": {
            "version": "1.0",
            "created_at": "2025-11-12",
            "updated_at": datetime.now().strftime("%Y-%m-%d"),
            "original_id": verse.get('verse_id', ''),
            "integration_phase": "phase4_fast_track",
            "source_type": source_type
        }
    }

    return golden_entry


def main():
    print(f"\n{'='*80}")
    print(f"INTEGRATING المتدارك CORPUS INTO GOLDEN SET")
    print(f"{'='*80}\n")

    # Load current golden set
    print(f"Loading current golden set...")
    current_golden = load_jsonl(GOLDEN_SET_CURRENT)
    print(f"✅ Loaded {len(current_golden)} verses from golden set v0.102\n")

    # Count existing المتدارك verses
    existing_mutadarik = [v for v in current_golden if v.get('meter') == 'المتدارك']
    print(f"Existing المتدارك verses: {len(existing_mutadarik)}")

    # Load our المتدارك corpus
    print(f"\nLoading our المتدارك corpus...")

    shamela_verses = load_jsonl(MUTADARIK_SHAMELA)
    # Filter out the failed verse (verse_006 with only 2 tafail)
    shamela_verses = [v for v in shamela_verses if v.get('verse_id') != 'mutadarik_shamela_006']
    print(f"✅ Loaded {len(shamela_verses)} classical verses (Shamela)")

    synthetic_verses = load_jsonl(MUTADARIK_SYNTHETIC)
    print(f"✅ Loaded {len(synthetic_verses)} synthetic verses")

    total_new = len(shamela_verses) + len(synthetic_verses)
    print(f"\n📊 Total new المتدارك verses to integrate: {total_new}")

    # Convert to golden format
    print(f"\n{'='*80}")
    print(f"CONVERTING TO GOLDEN SET FORMAT")
    print(f"{'='*80}\n")

    new_golden_verses = []
    start_verse_number = len(current_golden) + 1

    # Add Shamela verses
    for i, verse in enumerate(shamela_verses):
        verse_num = start_verse_number + i
        golden_verse = convert_mutadarik_to_golden_format(verse, verse_num, 'classical')
        new_golden_verses.append(golden_verse)
        print(f"✅ {golden_verse['verse_id']}: {verse.get('verse_id')} (Shamela)")

    # Add synthetic verses
    for i, verse in enumerate(synthetic_verses):
        verse_num = start_verse_number + len(shamela_verses) + i
        golden_verse = convert_mutadarik_to_golden_format(verse, verse_num, 'synthetic')
        new_golden_verses.append(golden_verse)
        print(f"✅ {golden_verse['verse_id']}: {verse.get('verse_id')} (Synthetic)")

    # Merge with existing golden set
    print(f"\n{'='*80}")
    print(f"CREATING NEW GOLDEN SET")
    print(f"{'='*80}\n")

    merged_golden = current_golden + new_golden_verses

    print(f"Previous golden set size: {len(current_golden)}")
    print(f"New المتدارك verses: {len(new_golden_verses)}")
    print(f"New golden set size: {len(merged_golden)}")

    # Count meters
    meters = {}
    for verse in merged_golden:
        meter = verse.get('meter', 'unknown')
        meters[meter] = meters.get(meter, 0) + 1

    print(f"\n📊 METER COVERAGE:")
    for meter, count in sorted(meters.items(), key=lambda x: -x[1]):
        print(f"  {meter}: {count} verses")

    # Save new golden set
    print(f"\n{'='*80}")
    print(f"SAVING GOLDEN SET v1.0")
    print(f"{'='*80}\n")

    save_jsonl(merged_golden, GOLDEN_SET_NEW)
    print(f"✅ Saved to: {GOLDEN_SET_NEW}")
    print(f"✅ Total verses: {len(merged_golden)}")

    # Summary stats
    mutadarik_total = len([v for v in merged_golden if v.get('meter') == 'المتدارك'])
    print(f"\n🎯 المتدارك COVERAGE:")
    print(f"  Previous: {len(existing_mutadarik)} verses")
    print(f"  Added: {len(new_golden_verses)} verses")
    print(f"  Total: {mutadarik_total} verses")
    print(f"  Increase: +{len(new_golden_verses)/len(existing_mutadarik)*100:.1f}%")

    print(f"\n{'='*80}")
    print(f"✅ INTEGRATION COMPLETE")
    print(f"{'='*80}\n")

    print(f"Golden set v1.0 ready for evaluation!")
    print(f"Next step: Run detector evaluation")

    return merged_golden


if __name__ == '__main__':
    main()
