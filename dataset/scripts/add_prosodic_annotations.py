#!/usr/bin/env python3
"""
Add prosodic annotations (taqti3, tafa'il, syllable patterns) to Golden Set.

This script provides:
1. Helper functions to add taqti3, tafa'il, and syllable patterns
2. Standard meter patterns reference
3. Template for manual annotation

Usage:
    python3 add_prosodic_annotations.py
"""

import json
from pathlib import Path
from typing import List, Dict

# Standard Arabic prosodic meters and their tafa'il patterns
METER_PATTERNS = {
    "الطويل": {
        "tafail": ["فعولن", "مفاعيلن", "فعولن", "مفاعيلن"],
        "syllable_pattern": "- u - - | - u u - | - u - - | - u u -",
        "description": "فعولن مفاعيلن فعولن مفاعيلن (8 مرات في البيت الكامل)"
    },
    "البسيط": {
        "tafail": ["مستفعلن", "فاعلن", "مستفعلن", "فاعلن"],
        "syllable_pattern": "- - u - - | - u - | - - u - - | - u -",
        "description": "مستفعلن فاعلن مستفعلن فاعلن (8 مرات)"
    },
    "الكامل": {
        "tafail": ["متفاعلن", "متفاعلن", "متفاعلن"],
        "syllable_pattern": "- - u - - | - - u - - | - - u - -",
        "description": "متفاعلن متفاعلن متفاعلن (6 مرات)"
    },
    "الوافر": {
        "tafail": ["مفاعلتن", "مفاعلتن", "فعولن"],
        "syllable_pattern": "- u u - - | - u u - - | - u - -",
        "description": "مفاعلتن مفاعلتن فعولن (6 مرات)"
    },
    "الرجز": {
        "tafail": ["مستفعلن", "مستفعلن", "مستفعلن"],
        "syllable_pattern": "- - u - - | - - u - - | - - u - -",
        "description": "مستفعلن مستفعلن مستفعلن (6 مرات)"
    },
    "الرمل": {
        "tafail": ["فاعلاتن", "فاعلاتن", "فاعلاتن"],
        "syllable_pattern": "- u - u - | - u - u - | - u - u -",
        "description": "فاعلاتن فاعلاتن فاعلاتن (6 مرات)"
    },
    "الخفيف": {
        "tafail": ["فاعلاتن", "مستفع لن", "فاعلاتن"],
        "syllable_pattern": "- u - u - | - - u - | - u - u -",
        "description": "فاعلاتن مستفع لن فاعلاتن (6 مرات)"
    },
    "المتقارب": {
        "tafail": ["فعولن", "فعولن", "فعولن", "فعولن"],
        "syllable_pattern": "- u - - | - u - - | - u - - | - u - -",
        "description": "فعولن فعولن فعولن فعولن (8 مرات)"
    },
    "الهزج": {
        "tafail": ["مفاعيلن", "مفاعيلن", "مفاعيلن"],
        "syllable_pattern": "- u u - | - u u - | - u u -",
        "description": "مفاعيلن مفاعيلن مفاعيلن (6 مرات)"
    },
    "المديد": {
        "tafail": ["فاعلاتن", "فاعلن", "فاعلاتن"],
        "syllable_pattern": "- u - u - | - u - | - u - u -",
        "description": "فاعلاتن فاعلن فاعلاتن (6 مرات)"
    },
    "السريع": {
        "tafail": ["مستفعلن", "مستفعلن", "فاعلن"],
        "syllable_pattern": "- - u - - | - - u - - | - u -",
        "description": "مستفعلن مستفعلن فاعلن (6 مرات)"
    },
    "المنسرح": {
        "tafail": ["مستفعلن", "مفعولات", "مستفعلن"],
        "syllable_pattern": "- - u - - | - u u - - | - - u - -",
        "description": "مستفعلن مفعولات مستفعلن (6 مرات)"
    },
    "المضارع": {
        "tafail": ["مفاعيلن", "فاعلاتن"],
        "syllable_pattern": "- u u - | - u - u -",
        "description": "مفاعيل فاعلاتن (متكرر)"
    },
    "المقتضب": {
        "tafail": ["مفعولات", "مستعلن"],
        "syllable_pattern": "- u u - - | - - u -",
        "description": "مفعولات مستعلن (متكرر)"
    },
    "المجتث": {
        "tafail": ["مستفع لن", "فاعلاتن"],
        "syllable_pattern": "- - u - | - u - u -",
        "description": "مستفع لن فاعلاتن (متكرر)"
    },
    "المتدارك": {
        "tafail": ["فاعلن", "فاعلن", "فاعلن", "فاعلن"],
        "syllable_pattern": "- u - | - u - | - u - | - u -",
        "description": "فاعلن فاعلن فاعلن فاعلن (8 مرات)"
    }
}


def extract_tafail_from_taqti3(taqti3: str) -> List[str]:
    """
    Extract tafa'il array from taqti3 string.
    
    Example:
        "فَعُولُنْ مَفَاعِيلُنْ فَعُولُنْ مَفَاعِيلُنْ"
        -> ["فعولن", "مفاعيلن", "فعولن", "مفاعيلن"]
    """
    # Remove diacritics and split
    tafail = taqti3.split()
    
    # Remove diacritics from each taf'ila
    diacritics = ['\u064B', '\u064C', '\u064D', '\u064E', '\u064F', 
                  '\u0650', '\u0651', '\u0652', '\u0653', '\u0654', 
                  '\u0655', '\u0656', '\u0657', '\u0658']
    
    clean_tafail = []
    for tafila in tafail:
        clean = tafila
        for diacritic in diacritics:
            clean = clean.replace(diacritic, '')
        clean_tafail.append(clean)
    
    return clean_tafail


def tafail_to_syllable_pattern(tafail: List[str]) -> str:
    """
    Convert tafa'il to syllable pattern notation.
    
    Mapping:
        فعولن -> - u - -
        مفاعيلن -> - u u -
        متفاعلن -> - - u - -
        مستفعلن -> - - u - -
        فاعلاتن -> - u - u -
        فاعلن -> - u -
        مفاعلتن -> - u u - -
        مستفع لن -> - - u -
        مفاعلن -> - u - - (زحاف of مفاعيلن - القبض)
        فعلن -> - - (زحاف of فاعلن - الحذف)
        مستفعلن -> - - u - - (with space removed)
    """
    patterns = {
        "فعولن": "- u - -",
        "مفاعيلن": "- u u -",
        "متفاعلن": "- - u - -",
        "مستفعلن": "- - u - -",
        "فاعلاتن": "- u - u -",
        "فاعلن": "- u -",
        "مفاعلتن": "- u u - -",
        "مفعولات": "- u u - -",
        "مستعلن": "- - u -",
        # Zihafat (variations)
        "مفاعلن": "- u - -",  # القبض (قبض مفاعيلن)
        "فعلن": "- -",  # الحذف (حذف فاعلن)
        "مستفعلن": "- - u - -",  # variant
    }
    
    syllable_parts = []
    for tafila in tafail:
        # Remove spaces that might be in "مستفع لن"
        tafila_clean = tafila.replace(" ", "")
        if tafila_clean in patterns:
            syllable_parts.append(patterns[tafila_clean])
        else:
            # Debug: print unmapped
            print(f"DEBUG: Unmapped taf'ila: '{tafila}' -> '{tafila_clean}'")
            syllable_parts.append("???")
    
    return " | ".join(syllable_parts)


def count_syllables(pattern: str) -> int:
    """Count syllables in a pattern."""
    return pattern.count('-') + pattern.count('u')


def create_annotation_template():
    """Create a template JSON file for manual annotation."""
    
    template = {
        "instructions": "Fill in taqti3 for each verse. The script will auto-generate tafa'il and syllable patterns.",
        "reference": METER_PATTERNS,
        "verses": []
    }
    
    # Load enriched verses
    input_file = Path(__file__).parent.parent / "evaluation" / "golden_set_v0_20_enriched.jsonl"
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            verse = json.loads(line)
            
            # Get expected pattern from meter
            meter_info = METER_PATTERNS.get(verse['meter'], {})
            
            verse_template = {
                "verse_id": verse['verse_id'],
                "text": verse['text'],
                "meter": verse['meter'],
                "poet": verse.get('poet', ''),
                
                # TO FILL MANUALLY:
                "taqti3": "",  # ADD THIS: e.g., "فَعُولُنْ مَفَاعِيلُنْ فَعُولُنْ مَفَاعِيلُنْ"
                
                # AUTO-GENERATED (will be filled after taqti3 is added):
                "expected_tafail": [],
                "syllable_pattern": "",
                "syllable_count": 0,
                
                # Reference for this meter:
                "meter_reference": meter_info.get('description', ''),
                "expected_pattern_example": meter_info.get('syllable_pattern', '')
            }
            
            template['verses'].append(verse_template)
    
    # Save template
    output_file = Path(__file__).parent / "prosodic_annotations_template.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(json.dumps(template, ensure_ascii=False, indent=2))
    
    print(f"✅ Template created: {output_file}")
    print(f"\n📝 Next steps:")
    print(f"   1. Open prosodic_annotations_template.json")
    print(f"   2. Fill in the 'taqti3' field for each verse")
    print(f"   3. Run: python3 add_prosodic_annotations.py --apply")
    print(f"   4. Script will auto-generate tafa'il and syllable patterns")
    
    return str(output_file)


def apply_annotations(template_file: str, output_file: str):
    """Apply manual annotations and auto-generate derived fields."""
    
    print("🚀 Applying prosodic annotations...")
    
    # Load template with manual annotations
    with open(template_file, 'r', encoding='utf-8') as f:
        template = json.load(f)
    
    # Load original enriched data
    enriched_file = Path(__file__).parent.parent / "evaluation" / "golden_set_v0_20_enriched.jsonl"
    enriched_verses = []
    with open(enriched_file, 'r', encoding='utf-8') as f:
        for line in f:
            enriched_verses.append(json.loads(line))
    
    # Apply annotations
    fully_annotated = []
    for verse_template in template['verses']:
        # Find matching enriched verse
        verse = next((v for v in enriched_verses if v['verse_id'] == verse_template['verse_id']), None)
        if not verse:
            continue
        
        # Add taqti3 (manual)
        taqti3 = verse_template.get('taqti3', '').strip()
        
        if taqti3:
            # Auto-generate tafa'il
            tafail = extract_tafail_from_taqti3(taqti3)
            
            # Auto-generate syllable pattern
            syllable_pattern = tafail_to_syllable_pattern(tafail)
            
            # Count syllables
            syllable_count = count_syllables(syllable_pattern)
            
            verse['taqti3'] = taqti3
            verse['expected_tafail'] = tafail
            verse['syllable_pattern'] = syllable_pattern
            verse['syllable_count'] = syllable_count
            
            print(f"  ✅ {verse['verse_id']}: {len(tafail)} tafa'il, {syllable_count} syllables")
        else:
            print(f"  ⚠️  {verse['verse_id']}: No taqti3 provided, skipping")
        
        fully_annotated.append(verse)
    
    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        for verse in fully_annotated:
            f.write(json.dumps(verse, ensure_ascii=False) + '\n')
    
    print(f"\n✅ Fully annotated data written to: {output_file}")
    
    # Stats
    annotated_count = sum(1 for v in fully_annotated if 'taqti3' in v and v['taqti3'])
    print(f"📊 Annotated: {annotated_count}/{len(fully_annotated)} verses")
    
    return fully_annotated


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--apply':
        # Apply annotations from template
        template_file = Path(__file__).parent / "prosodic_annotations_template.json"
        output_file = Path(__file__).parent.parent / "evaluation" / "golden_set_v0_20_fully_annotated.jsonl"
        
        apply_annotations(str(template_file), str(output_file))
    else:
        # Create template for manual annotation
        create_annotation_template()
        
        print("\n" + "="*60)
        print("📚 METER PATTERNS REFERENCE:")
        print("="*60)
        for meter, info in METER_PATTERNS.items():
            print(f"\n{meter}:")
            print(f"  {info['description']}")
            print(f"  Pattern: {info['syllable_pattern']}")
