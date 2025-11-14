#!/usr/bin/env python3
"""
Fix Golden Set data to match JSON schema requirements.

Updates:
1. Add reference_sources to validation object
2. Rename added_date to created_at in metadata
3. Rename last_updated to updated_at in metadata
4. Convert version from integer to string
"""

import json
from datetime import datetime
from pathlib import Path


def fix_verse(verse: dict) -> dict:
    """Fix a single verse to match schema."""
    
    # Fix validation object
    if 'validation' in verse:
        val = verse['validation']
        
        # Add reference_sources if missing
        if 'reference_sources' not in val:
            val['reference_sources'] = [
                "كتاب العروض للخليل",
                "الكافي في العروض والقوافي"
            ]
        
        # Remove non-schema fields
        if 'confidence' in val:
            del val['confidence']
        if 'verification_method' in val:
            del val['verification_method']
    
    # Fix metadata object
    if 'metadata' in verse:
        meta = verse['metadata']
        
        # Rename added_date to created_at
        if 'added_date' in meta:
            meta['created_at'] = meta.pop('added_date')
        elif 'created_at' not in meta:
            meta['created_at'] = "2025-11-09"
        
        # Rename last_updated to updated_at
        if 'last_updated' in meta:
            # Extract just the date part if it's a datetime
            updated = meta.pop('last_updated')
            if 'T' in updated:
                meta['updated_at'] = updated.split('T')[0]
            else:
                meta['updated_at'] = updated
        elif 'updated_at' not in meta:
            meta['updated_at'] = "2025-11-09"
        
        # Convert version to string
        if 'version' in meta:
            if isinstance(meta['version'], (int, float)):
                meta['version'] = "0.20"
        else:
            meta['version'] = "0.20"
        
        # Remove non-schema fields
        if 'annotation_phase' in meta:
            del meta['annotation_phase']
    
    return verse


def main():
    """Fix all verses in the golden set."""
    script_dir = Path(__file__).parent
    eval_dir = script_dir.parent / 'evaluation'
    
    input_path = eval_dir / 'golden_set_v0_20_complete.jsonl'
    output_path = eval_dir / 'golden_set_v0_20_complete_fixed.jsonl'
    
    print(f"📂 Reading from: {input_path}")
    
    verses = []
    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            verse = json.loads(line)
            fixed_verse = fix_verse(verse)
            verses.append(fixed_verse)
    
    print(f"✅ Fixed {len(verses)} verses")
    
    # Write fixed verses
    print(f"💾 Writing to: {output_path}")
    with open(output_path, 'w', encoding='utf-8') as f:
        for verse in verses:
            f.write(json.dumps(verse, ensure_ascii=False) + '\n')
    
    print("✅ Done! Now replacing original file...")
    
    # Replace original
    output_path.replace(input_path)
    
    print(f"✅ Updated {input_path}")
    print("\n🎉 All verses fixed and ready for schema validation!")


if __name__ == '__main__':
    main()
