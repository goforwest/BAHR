"""
Retroactively enhance metadata for v1.0/v1.1 verses (356 verses)
Adds comprehensive historical metadata (era, region, dates, genre)
"""

import json
import sys
from pathlib import Path

# Add tools directory to path
sys.path.insert(0, str(Path(__file__).parent))
from poet_database import get_poet_metadata, infer_genre

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

def needs_metadata_enhancement(verse):
    """Check if verse needs metadata enhancement"""
    metadata = verse.get("metadata", {})

    # Check if it's already v1.2 (has phase field)
    if "phase" in metadata:
        return False

    # Check if it has the new metadata structure
    if "era" in metadata and "region" in metadata and "poem_genre" in metadata:
        return False

    return True

def enhance_verse_metadata(verse):
    """Add comprehensive metadata to a verse"""
    # Get existing metadata
    old_metadata = verse.get("metadata", {})

    # Get poet information
    poet_name = verse.get("poet", "")
    poet_data = get_poet_metadata(poet_name)

    # Infer genre from content
    text = verse.get("normalized_text", "")
    source = verse.get("source", "")
    notes = verse.get("notes", "")
    genre = infer_genre(text, source, notes)

    # Build enhanced metadata
    enhanced_metadata = {
        "version": old_metadata.get("version", "1.0"),
        "created_at": old_metadata.get("created_at", "2025-11-09"),
        "updated_at": "2025-11-12",  # Today
        "dataset_version": "1.2_enhanced",
        "phase": "retroactive_enhancement",
        "era": poet_data["era"],
        "era_dates": poet_data["era_dates"],
        "poet_birth_year": poet_data["poet_birth_year"],
        "poet_death_year": poet_data["poet_death_year"],
        "region": poet_data["region"],
        "poem_genre": genre,
        "enhancement_notes": "Metadata retroactively enhanced from poet database"
    }

    # Add poet notes if available
    if poet_data.get("notes"):
        enhanced_metadata["poet_notes"] = poet_data["notes"]

    # Update verse
    verse["metadata"] = enhanced_metadata

    return verse

def main():
    """Main execution"""
    print("=" * 60)
    print("METADATA ENHANCEMENT FOR V1.0/V1.1 VERSES")
    print("=" * 60)

    # Load v1.2 final dataset
    dataset_path = Path("dataset/evaluation/golden_set_v1_2_final.jsonl")
    print(f"\n1. Loading dataset: {dataset_path}")
    verses = load_jsonl(dataset_path)
    print(f"   Total verses: {len(verses)}")

    # Count verses needing enhancement
    verses_to_enhance = [v for v in verses if needs_metadata_enhancement(v)]
    print(f"   Verses needing enhancement: {len(verses_to_enhance)}")
    print(f"   Already enhanced (v1.2): {len(verses) - len(verses_to_enhance)}")

    if not verses_to_enhance:
        print("\n✓ All verses already have enhanced metadata!")
        return

    # Enhance metadata
    print(f"\n2. Enhancing metadata for {len(verses_to_enhance)} verses...")
    enhanced_count = 0

    for i, verse in enumerate(verses, 1):
        if needs_metadata_enhancement(verse):
            verse = enhance_verse_metadata(verse)
            enhanced_count += 1

            # Show progress every 50 verses
            if enhanced_count % 50 == 0:
                print(f"   Enhanced {enhanced_count}/{len(verses_to_enhance)} verses...")

    print(f"   ✓ Enhanced {enhanced_count} verses")

    # Show sample of enhanced metadata
    print("\n3. Sample enhanced verse:")
    sample_verse = next(v for v in verses if v["metadata"]["phase"] == "retroactive_enhancement")
    print(f"   Verse ID: {sample_verse['verse_id']}")
    print(f"   Poet: {sample_verse.get('poet', 'Unknown')}")
    print(f"   Meter: {sample_verse['meter']}")
    print(f"   Enhanced metadata:")
    for key, value in sample_verse['metadata'].items():
        print(f"     - {key}: {value}")

    # Save enhanced dataset
    output_path = Path("dataset/evaluation/golden_set_v1_2_final_enhanced.jsonl")
    print(f"\n4. Saving enhanced dataset: {output_path}")
    save_jsonl(verses, output_path)

    # Statistics
    print("\n" + "=" * 60)
    print("ENHANCEMENT STATISTICS")
    print("=" * 60)

    # Count by era
    era_counts = {}
    for verse in verses:
        era = verse["metadata"].get("era", "Unknown")
        era_counts[era] = era_counts.get(era, 0) + 1

    print("\nVerses by Era:")
    for era, count in sorted(era_counts.items(), key=lambda x: -x[1]):
        print(f"  {era:20s}: {count:3d} verses")

    # Count by region
    region_counts = {}
    for verse in verses:
        region = verse["metadata"].get("region", "Unknown")
        region_counts[region] = region_counts.get(region, 0) + 1

    print("\nVerses by Region:")
    for region, count in sorted(region_counts.items(), key=lambda x: -x[1]):
        print(f"  {region:20s}: {count:3d} verses")

    # Count by genre
    genre_counts = {}
    for verse in verses:
        genre = verse["metadata"].get("poem_genre", "Unknown")
        genre_counts[genre] = genre_counts.get(genre, 0) + 1

    print("\nVerses by Genre:")
    for genre, count in sorted(genre_counts.items(), key=lambda x: -x[1]):
        print(f"  {genre:20s}: {count:3d} verses")

    print("\n" + "=" * 60)
    print("✓ METADATA ENHANCEMENT COMPLETE!")
    print("=" * 60)
    print(f"\nOutput file: {output_path}")
    print(f"Total verses: {len(verses)}")
    print(f"Enhanced verses: {enhanced_count}")
    print(f"\nNext steps:")
    print("  1. Review sample verses to verify metadata accuracy")
    print("  2. Run evaluation to ensure no degradation")
    print("  3. Replace golden_set_v1_2_final.jsonl with enhanced version")

if __name__ == "__main__":
    main()
