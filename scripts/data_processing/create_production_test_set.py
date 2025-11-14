#!/usr/bin/env python3
"""
Create production-distribution test set for BAHR prosody engine.

This script addresses the critical test/production distribution mismatch:
- Current Golden Set: 100% fully diacritized
- Production Reality: 90% undiacritized input

Output distribution:
- 10% fully diacritized (academic users with high-quality input)
- 20% partially diacritized (educated users, some diacritics)
- 70% undiacritized (typical users, no diacritics)

This mirrors real-world usage and validates production performance.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "backend"))

from app.core.normalization import ARABIC_DIACRITICS


def remove_all_diacritics(text: str) -> str:
    """Remove all Arabic diacritical marks."""
    result = text
    for diacritic in ARABIC_DIACRITICS:
        result = result.replace(diacritic, "")
    return result


def remove_partial_diacritics(text: str) -> str:
    """
    Remove some diacritics to simulate partially diacritized text.
    
    Keeps: Short vowels (fatha, kasra, damma) - most important for meter
    Removes: Sukun, shadda, tanween - less critical
    
    This simulates educated users who know to add basic vowels
    but may skip auxiliary marks.
    """
    import re

    result = text
    
    # Remove sukun (0652)
    result = result.replace("\u0652", "")
    
    # Remove shadda (0651)
    result = result.replace("\u0651", "")
    
    # Remove tanween (064b-064d)
    result = re.sub("[\u064b\u064c\u064d]", "", result)
    
    # Keep short vowels (fatha 064e, kasra 0650, damma 064f)
    
    return result


def create_production_distribution_test_set(
    input_file: Path,
    output_file: Path,
    full_ratio: float = 0.10,
    partial_ratio: float = 0.20,
) -> Dict[str, int]:
    """
    Create test set matching production distribution.
    
    Args:
        input_file: Path to golden set (fully diacritized)
        output_file: Path to output file
        full_ratio: Ratio of fully diacritized verses (default: 10%)
        partial_ratio: Ratio of partially diacritized verses (default: 20%)
        
    Returns:
        Statistics dictionary
    """
    # Load original golden set
    verses = []
    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                verses.append(json.loads(line))

    total = len(verses)
    
    # Calculate split points
    full_count = int(total * full_ratio)
    partial_count = int(total * partial_ratio)
    undiac_count = total - full_count - partial_count
    
    print(f"📊 Creating production-distribution test set:")
    print(f"   Total verses: {total}")
    print(f"   Fully diacritized: {full_count} ({full_ratio:.0%})")
    print(f"   Partially diacritized: {partial_count} ({partial_ratio:.0%})")
    print(f"   Undiacritized: {undiac_count} ({1-full_ratio-partial_ratio:.0%})")
    print()
    
    # Create test sets
    output_verses = []
    
    for i, verse in enumerate(verses):
        verse_copy = verse.copy()
        
        # Handle different field names for verse text
        verse_text = verse.get('verse') or verse.get('text') or ''
        if not verse_text:
            continue
        
        if i < full_count:
            # Keep fully diacritized
            verse_copy["diacritization_level"] = "full"
            verse_copy["original_verse"] = verse_text
            if 'verse' not in verse_copy:
                verse_copy['verse'] = verse_text
            
        elif i < full_count + partial_count:
            # Partial diacritics
            verse_copy["diacritization_level"] = "partial"
            verse_copy["original_verse"] = verse_text
            verse_copy["verse"] = remove_partial_diacritics(verse_text)
            
        else:
            # Fully undiacritized
            verse_copy["diacritization_level"] = "undiacritized"
            verse_copy["original_verse"] = verse_text
            verse_copy["verse"] = remove_all_diacritics(verse_text)
        
        output_verses.append(verse_copy)
    
    # Save
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, "w", encoding="utf-8") as f:
        for verse in output_verses:
            f.write(json.dumps(verse, ensure_ascii=False) + "\n")
    
    print(f"✅ Created production-distribution test set:")
    print(f"   Output: {output_file}")
    print()
    
    # Show examples
    print("📝 Examples:")
    print()
    
    for level in ["full", "partial", "undiacritized"]:
        example = next((v for v in output_verses if v["diacritization_level"] == level), None)
        if not example:
            continue
        verse_text = example.get('verse') or example.get('text', '')
        meter = example.get('meter', example.get('expected_meter', 'N/A'))
        print(f"{level.upper()}:")
        print(f"   Verse: {verse_text[:60]}...")
        print(f"   Meter: {meter}")
        print()
    
    stats = {
        "total": total,
        "full": full_count,
        "partial": partial_count,
        "undiacritized": undiac_count,
    }
    
    return stats


def main():
    """Main execution."""
    # Paths
    project_root = Path(__file__).parent.parent.parent
    
    # Find golden set - try multiple locations
    golden_set_paths = [
        project_root / "data" / "processed" / "datasets" / "evaluation" / "golden_set_v1_2_final.jsonl",
        project_root / "data" / "processed" / "datasets" / "evaluation" / "golden_set_v0_102_comprehensive.jsonl",
        project_root / "archive" / "duplicates" / "golden_set_v0_80_complete.backup.jsonl",
        project_root / "data" / "golden_set_v0_80_complete.backup.jsonl",
        project_root / "data" / "processed" / "datasets" / "golden_set_v0_80_complete.backup.jsonl",
    ]
    
    input_file = None
    for path in golden_set_paths:
        if path.exists():
            input_file = path
            break
    
    if not input_file:
        print("❌ Error: Could not find golden set file")
        print("   Searched:")
        for path in golden_set_paths:
            print(f"   - {path}")
        sys.exit(1)
    
    output_file = project_root / "data" / "test" / "golden_set_production_distribution.jsonl"
    
    print("🚀 BAHR Production-Distribution Test Set Generator")
    print("=" * 70)
    print()
    print(f"Input:  {input_file}")
    print(f"Output: {output_file}")
    print()
    
    # Create test set
    stats = create_production_distribution_test_set(input_file, output_file)
    
    print("=" * 70)
    print("✅ COMPLETE")
    print()
    print("Next steps:")
    print("1. Run validation tests: pytest tests/evaluation/test_production_distribution.py")
    print("2. Check undiacritized accuracy (target: ≥75%)")
    print("3. Verify no regression on diacritized text (≥97.5%)")


if __name__ == "__main__":
    main()
