#!/usr/bin/env python3
"""
Extract empirical patterns for 7 missing meters from golden dataset.

This will restore the 50.3% Phase 2 baseline accuracy by adding patterns for:
- السريع (al-Sari')
- المديد (al-Madid)
- المجتث (al-Mujtathth)
- المنسرح (al-Munsarih)
- المقتضب (al-Muqtadab)
- المضارع (al-Mudari')
- المتدارك (al-Mutadarik)
"""

import sys
import json
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, 'backend')

from app.core.phonetics import text_to_phonetic_pattern

# The 7 missing meters (from your analysis)
MISSING_METERS = {
    "السريع": 8,
    "المديد": 9,
    "المجتث": 10,
    "المنسرح": 13,
    "المقتضب": 14,
    "المضارع": 15,
    "المتدارك": 16
}

def load_golden_dataset(filepath: str):
    """Load golden dataset JSONL."""
    verses = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                verses.append(json.loads(line))
    return verses

def extract_patterns_for_meter(verses, meter_name_ar):
    """Extract all unique patterns for a specific meter."""
    patterns = set()
    verse_count = 0

    for verse in verses:
        # Check if this verse belongs to the target meter
        verse_meter = verse.get('meter', verse.get('meter_ar', verse.get('bahr', '')))
        if verse_meter == meter_name_ar:
            verse_count += 1
            text = verse.get('text', verse.get('original', ''))

            if text:
                try:
                    # Extract phonetic pattern
                    pattern = text_to_phonetic_pattern(text)
                    if pattern:
                        patterns.add(pattern)
                except Exception as e:
                    print(f"  ⚠️  Error extracting pattern from: {text[:50]}... ({e})")

    return sorted(patterns), verse_count

def generate_empirical_patterns_code(meter_patterns):
    """Generate Python code for EMPIRICAL_PATTERNS dictionary."""
    lines = []
    lines.append("# Generated empirical patterns for missing meters")
    lines.append("# Source: Golden dataset extraction")
    lines.append("# Date: 2025-11-13")
    lines.append("")
    lines.append("MISSING_METERS_PATTERNS = {")

    for meter_id, (meter_name_ar, meter_name_en, patterns) in meter_patterns.items():
        lines.append(f"    # {meter_name_ar} ({meter_name_en})")
        lines.append(f"    {meter_id}: {{")
        lines.append(f"        'name_ar': '{meter_name_ar}',")
        lines.append(f"        'name_en': '{meter_name_en}',")
        lines.append(f"        'patterns': [")
        for pattern in patterns:
            lines.append(f"            '{pattern}',")
        lines.append(f"        ]")
        lines.append(f"    }},")

    lines.append("}")
    lines.append("")
    lines.append("# Usage: Add these to EMPIRICAL_PATTERNS in detector_v2_hybrid.py")
    lines.append("# EMPIRICAL_PATTERNS.update(MISSING_METERS_PATTERNS)")

    return "\n".join(lines)

def main():
    print("=" * 80)
    print("Extracting Empirical Patterns for 7 Missing Meters")
    print("=" * 80)
    print()

    # Find golden dataset
    golden_dataset_paths = [
        'dataset/evaluation/golden_set_v1_3_with_sari.jsonl',
        'dataset/evaluation/golden_set_v1_0_with_patterns.jsonl',
        'dataset/evaluation/golden_set_v1_0_with_patterns_fixed.jsonl'
    ]

    golden_dataset_path = None
    for path in golden_dataset_paths:
        if Path(path).exists():
            golden_dataset_path = path
            break

    if not golden_dataset_path:
        print("❌ ERROR: Could not find golden dataset!")
        print("   Searched paths:")
        for path in golden_dataset_paths:
            print(f"   - {path}")
        sys.exit(1)

    print(f"✅ Found golden dataset: {golden_dataset_path}")
    print()

    # Load golden dataset
    print("Loading golden dataset...")
    verses = load_golden_dataset(golden_dataset_path)
    print(f"✅ Loaded {len(verses)} verses")
    print()

    # Extract patterns for each missing meter
    meter_patterns = {}
    total_patterns = 0

    for meter_name_ar, meter_id in MISSING_METERS.items():
        print(f"📊 Extracting patterns for: {meter_name_ar} (meter_id={meter_id})")

        patterns, verse_count = extract_patterns_for_meter(verses, meter_name_ar)

        # Get English name (approximate mapping)
        meter_name_en_map = {
            "السريع": "al-Sari'",
            "المديد": "al-Madid",
            "المجتث": "al-Mujtathth",
            "المنسرح": "al-Munsarih",
            "المقتضب": "al-Muqtadab",
            "المضارع": "al-Mudari'",
            "المتدارك": "al-Mutadarik"
        }
        meter_name_en = meter_name_en_map.get(meter_name_ar, meter_name_ar)

        meter_patterns[meter_id] = (meter_name_ar, meter_name_en, patterns)
        total_patterns += len(patterns)

        print(f"   Verses: {verse_count}")
        print(f"   Unique patterns: {len(patterns)}")
        if patterns:
            print(f"   Sample: {patterns[0]}")
        print()

    # Generate Python code
    print("=" * 80)
    print("📝 Generated Python Code")
    print("=" * 80)
    print()

    code = generate_empirical_patterns_code(meter_patterns)
    print(code)
    print()

    # Save to file
    output_file = "missing_meters_patterns.py"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(code)

    print("=" * 80)
    print("✅ EXTRACTION COMPLETE")
    print("=" * 80)
    print(f"Total missing meters: {len(MISSING_METERS)}")
    print(f"Total unique patterns extracted: {total_patterns}")
    print(f"Output file: {output_file}")
    print()
    print("Next steps:")
    print("1. Review the generated patterns in missing_meters_patterns.py")
    print("2. Add them to detector_v2_hybrid.py:")
    print("   EMPIRICAL_PATTERNS.update(MISSING_METERS_PATTERNS)")
    print("3. Re-validate on golden dataset (expected: 50%+ accuracy)")
    print()

if __name__ == '__main__':
    main()
