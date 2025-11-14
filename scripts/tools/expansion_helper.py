#!/usr/bin/env python3
"""
Helper tool for golden set expansion workflow.

Features:
- Generate next verse ID
- Create verse template with proper schema
- Add verse to expansion file
- Show meter statistics and gaps
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from collections import Counter
from typing import Optional

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
GOLDEN_SET_PATH = PROJECT_ROOT / "dataset/evaluation/golden_set_v1_0_with_patterns.jsonl"
EXPANSION_PATH = PROJECT_ROOT / "dataset/evaluation/golden_set_v1_1_expansion.jsonl"


def get_next_verse_id(expansion_file: Optional[Path] = None) -> tuple[str, int]:
    """Get the next available verse ID."""
    # Start from golden set
    with open(GOLDEN_SET_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        last_verse = json.loads(lines[-1])
        last_num = int(last_verse['verse_id'].split('_')[1])

    # Check expansion file if it exists
    if expansion_file and expansion_file.exists():
        with open(expansion_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    verse = json.loads(line)
                    verse_num = int(verse['verse_id'].split('_')[1])
                    last_num = max(last_num, verse_num)

    next_num = last_num + 1
    return f"golden_{next_num:03d}", next_num


def create_verse_template(
    text: str,
    meter: str,
    poet: str = "",
    poem_title: str = "",
    source: str = "classical",
    notes: str = ""
) -> dict:
    """Create a verse entry with proper schema."""
    verse_id, _ = get_next_verse_id(EXPANSION_PATH)

    # Remove diacritics for normalized_text
    arabic_diacritics = [
        '\u064B', '\u064C', '\u064D', '\u064E', '\u064F',
        '\u0650', '\u0651', '\u0652', '\u0653', '\u0654',
        '\u0655', '\u0656', '\u0657', '\u0658'
    ]
    normalized_text = text
    for diacritic in arabic_diacritics:
        normalized_text = normalized_text.replace(diacritic, '')

    today = datetime.now().strftime('%Y-%m-%d')

    return {
        "verse_id": verse_id,
        "text": text,
        "normalized_text": normalized_text,
        "meter": meter,
        "poet": poet,
        "poem_title": poem_title,
        "source": source,
        "prosody_precomputed": {
            "pattern": "to be computed",
            "fitness_score": 0.0,
            "method": "pending",
            "meter_verified": meter
        },
        "validation": {
            "verified_by": "expansion_phase",
            "verified_date": today,
            "automated_check": "PENDING"
        },
        "metadata": {
            "version": "1.1",
            "phase": "expansion",
            "notes": notes
        }
    }


def get_meter_statistics() -> dict:
    """Get meter distribution statistics from golden set and expansion."""
    meters = []

    # Read golden set
    with open(GOLDEN_SET_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            verse = json.loads(line)
            meters.append(verse['meter'])

    golden_count = len(meters)

    # Read expansion if exists
    expansion_count = 0
    if EXPANSION_PATH.exists():
        with open(EXPANSION_PATH, 'r', encoding='utf-8') as f:
            for line in f:
                verse = json.loads(line)
                meters.append(verse['meter'])
                expansion_count += 1

    counter = Counter(meters)

    return {
        'golden_count': golden_count,
        'expansion_count': expansion_count,
        'total_count': len(meters),
        'meter_distribution': counter,
        'sorted_meters': sorted(counter.items(), key=lambda x: x[1])
    }


def print_meter_statistics():
    """Print meter distribution and identify gaps."""
    stats = get_meter_statistics()

    print(f"\n{'='*70}")
    print(f"METER STATISTICS")
    print(f"{'='*70}")
    print(f"Golden set: {stats['golden_count']} verses")
    print(f"Expansion: {stats['expansion_count']} verses")
    print(f"Total: {stats['total_count']} verses")
    print(f"{'='*70}\n")

    # Target: 15-20 verses per meter
    TARGET_MIN = 15
    TARGET_MAX = 20

    print("PRIORITY METERS (need most verses):")
    print(f"{'Count':<6} {'Gap':<6} {'Meter'}")
    print("-" * 50)

    priority_meters = []
    for meter, count in stats['sorted_meters']:
        if count < TARGET_MIN:
            gap = TARGET_MIN - count
            priority_meters.append((meter, count, gap))
            print(f"{count:<6} {gap:<6} {meter}")

    print(f"\n{'='*70}")
    print(f"Total verses needed to reach {TARGET_MIN} minimum: {sum(g for _, _, g in priority_meters)}")
    print(f"{'='*70}\n")

    print("BALANCED METERS (10-14 verses):")
    for meter, count in stats['sorted_meters']:
        if 10 <= count < TARGET_MIN:
            print(f"  {count:3d} - {meter}")

    print("\nWELL-REPRESENTED METERS (15+ verses):")
    for meter, count in stats['sorted_meters']:
        if count >= TARGET_MIN:
            status = "✓" if count <= TARGET_MAX else "⚠️ (over target)"
            print(f"  {count:3d} - {meter} {status}")


def add_verse_to_expansion(verse: dict, validate: bool = True):
    """Add a verse to the expansion file."""
    if validate:
        # Simple validation
        required_fields = ['verse_id', 'text', 'normalized_text', 'meter']
        missing = [f for f in required_fields if f not in verse]
        if missing:
            raise ValueError(f"Missing required fields: {missing}")

    # Ensure directory exists
    EXPANSION_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Append to file
    with open(EXPANSION_PATH, 'a', encoding='utf-8') as f:
        f.write(json.dumps(verse, ensure_ascii=False) + '\n')

    print(f"✓ Added {verse['verse_id']} ({verse['meter']}) to expansion file")


def show_usage():
    """Show usage instructions."""
    print("""
Golden Set Expansion Helper
===========================

Commands:
  stats              Show meter statistics and gaps
  next-id            Show next available verse ID
  template           Create verse template (interactive)
  add                Add verse to expansion file (interactive)
  validate           Validate expansion file

Examples:
  python tools/expansion_helper.py stats
  python tools/expansion_helper.py next-id
  python tools/expansion_helper.py template
  python tools/expansion_helper.py add
""")


def interactive_template():
    """Create verse template interactively."""
    print("\nCreate Verse Template")
    print("=" * 50)

    verse_id, _ = get_next_verse_id(EXPANSION_PATH)
    print(f"Next verse ID: {verse_id}\n")

    text = input("Diacritized text: ").strip()
    if not text:
        print("Error: Text is required")
        return

    meter = input("Meter: ").strip()
    if not meter:
        print("Error: Meter is required")
        return

    poet = input("Poet (optional): ").strip()
    poem_title = input("Poem title (optional): ").strip()
    source = input("Source (default: classical): ").strip() or "classical"
    notes = input("Notes (optional): ").strip()

    verse = create_verse_template(
        text=text,
        meter=meter,
        poet=poet,
        poem_title=poem_title,
        source=source,
        notes=notes
    )

    print("\n" + "=" * 50)
    print("Generated verse:")
    print("=" * 50)
    print(json.dumps(verse, ensure_ascii=False, indent=2))

    save = input("\nSave to expansion file? (y/n): ").strip().lower()
    if save == 'y':
        add_verse_to_expansion(verse)
        print(f"\n✓ Saved to {EXPANSION_PATH}")


def main():
    if len(sys.argv) < 2:
        show_usage()
        return

    command = sys.argv[1]

    if command == 'stats':
        print_meter_statistics()

    elif command == 'next-id':
        verse_id, num = get_next_verse_id(EXPANSION_PATH)
        print(f"\nNext verse ID: {verse_id} (number: {num})")

    elif command == 'template':
        interactive_template()

    elif command == 'add':
        interactive_template()  # Same as template for now

    elif command == 'validate':
        if not EXPANSION_PATH.exists():
            print(f"No expansion file found at: {EXPANSION_PATH}")
            return

        print(f"Validating: {EXPANSION_PATH}")
        import subprocess
        result = subprocess.run([
            'python3',
            'tools/validate_expansion_verse.py',
            '--file',
            str(EXPANSION_PATH)
        ])
        sys.exit(result.returncode)

    else:
        print(f"Unknown command: {command}")
        show_usage()
        sys.exit(1)


if __name__ == '__main__':
    main()
