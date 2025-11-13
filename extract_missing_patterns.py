#!/usr/bin/env python3
"""
Extract empirical patterns for missing meters from golden dataset.
"""

import sys
import json
from collections import defaultdict

sys.path.insert(0, '/home/user/BAHR/backend')

from app.core.phonetics import text_to_phonetic_pattern

# Missing meter IDs and names
MISSING_METERS = {
    8: ('السريع', 'al-Sari'),
    9: ('المديد', 'al-Madid'),
    10: ('المنسرح', 'al-Munsarih'),
    13: ('المجتث', 'al-Mujtathth'),
    14: ('المقتضب', 'al-Muqtadab'),
    15: ('المضارع', 'al-Mudari'),
    16: ('المتدارك', 'al-Mutadarik'),
}


def load_verses(filepath: str):
    """Load verses from JSONL file."""
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
        verse_meter = verse.get('meter', '')
        if verse_meter == meter_name_ar:
            text = verse.get('text', '')
            if text:
                try:
                    pattern = text_to_phonetic_pattern(text, has_tashkeel=True)
                    patterns.add(pattern)
                    verse_count += 1
                except Exception as e:
                    print(f"  Warning: Failed to extract pattern for verse: {text[:50]}... Error: {e}")

    return sorted(patterns), verse_count


def generate_patterns_file(patterns_by_meter, output_path):
    """Generate Python file with extracted patterns."""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('"""\n')
        f.write('Empirical patterns for missing meters.\n')
        f.write('Extracted from golden dataset.\n')
        f.write('"""\n\n')

        f.write('MISSING_METERS_PATTERNS = {\n')

        for meter_id in sorted(patterns_by_meter.keys()):
            meter_data = patterns_by_meter[meter_id]
            name_ar = meter_data['name_ar']
            name_en = meter_data['name_en']
            patterns = meter_data['patterns']
            verse_count = meter_data['verse_count']

            f.write(f'    {meter_id}: {{  # {name_ar}\n')
            f.write(f"        'name_ar': '{name_ar}',\n")
            f.write(f"        'name_en': '{name_en}',\n")
            f.write(f'        \'patterns\': [\n')

            for pattern in patterns:
                f.write(f"            '{pattern}',\n")

            f.write('        ],\n')
            f.write(f'        # Extracted from {verse_count} verses\n')
            f.write('    },\n')

        f.write('}\n')


def main():
    """Main extraction."""
    dataset_path = '/home/user/BAHR/dataset/evaluation/golden_set_v1_3_with_sari.jsonl'
    output_path = '/home/user/BAHR/missing_meters_patterns.py'

    print("=" * 80)
    print("EXTRACTING EMPIRICAL PATTERNS FOR MISSING METERS")
    print("=" * 80)
    print()

    print(f"Loading dataset: {dataset_path}")
    verses = load_verses(dataset_path)
    print(f"✓ Loaded {len(verses)} verses")
    print()

    patterns_by_meter = {}
    total_patterns = 0
    total_verses = 0

    print("Extracting patterns for missing meters:")
    print("-" * 80)

    for meter_id, (name_ar, name_en) in MISSING_METERS.items():
        print(f"\nMeter {meter_id}: {name_ar} ({name_en})")

        patterns, verse_count = extract_patterns_for_meter(verses, name_ar)

        print(f"  Verses: {verse_count}")
        print(f"  Unique patterns: {len(patterns)}")

        if len(patterns) > 0:
            print(f"  Sample pattern: {patterns[0]}")

        patterns_by_meter[meter_id] = {
            'name_ar': name_ar,
            'name_en': name_en,
            'patterns': patterns,
            'verse_count': verse_count,
        }

        total_patterns += len(patterns)
        total_verses += verse_count

    print()
    print("-" * 80)
    print(f"TOTAL: {total_patterns} unique patterns from {total_verses} verses")
    print()

    print(f"Generating patterns file: {output_path}")
    generate_patterns_file(patterns_by_meter, output_path)
    print(f"✓ Generated: {output_path}")
    print()

    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Missing meters: {len(MISSING_METERS)}")
    print(f"Total patterns extracted: {total_patterns}")
    print(f"Total verses processed: {total_verses}")
    print(f"Output file: {output_path}")
    print()
    print("✓ Extraction complete!")
    print()

    return 0


if __name__ == '__main__':
    sys.exit(main())
