#!/usr/bin/env python3
"""
Enrich Golden Set with automated fields.
Phase A: Data Enrichment - Tasks A4, A5, A6
"""

import json
import re
from pathlib import Path

# Arabic diacritics to remove for normalization
ARABIC_DIACRITICS = [
    '\u064B',  # Tanween Fath
    '\u064C',  # Tanween Damm
    '\u064D',  # Tanween Kasr
    '\u064E',  # Fatha
    '\u064F',  # Damma
    '\u0650',  # Kasra
    '\u0651',  # Shadda
    '\u0652',  # Sukun
    '\u0653',  # Maddah
    '\u0654',  # Hamza above
    '\u0655',  # Hamza below
    '\u0656',  # Subscript Alef
    '\u0657',  # Inverted Damma
    '\u0658',  # Mark Noon Ghunna
]


def remove_diacritics(text: str) -> str:
    """Remove all Arabic diacritical marks."""
    for diacritic in ARABIC_DIACRITICS:
        text = text.replace(diacritic, '')
    return text


def normalize_hamza(text: str) -> str:
    """Normalize all hamza variants to base form."""
    text = text.replace('أ', 'ا')
    text = text.replace('إ', 'ا')
    text = text.replace('آ', 'ا')
    text = text.replace('ؤ', 'و')
    text = text.replace('ئ', 'ي')
    return text


def normalize_alef(text: str) -> str:
    """Normalize alef variants."""
    text = text.replace('ى', 'ي')  # Alef maksura → ya
    text = text.replace('أ', 'ا')
    text = text.replace('إ', 'ا')
    text = text.replace('آ', 'ا')
    return text


def remove_tatweel(text: str) -> str:
    """Remove Arabic tatweel (kashida) character."""
    return text.replace('\u0640', '')


def normalize_whitespace(text: str) -> str:
    """Normalize whitespace to single spaces."""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def normalize_arabic_text(text: str) -> str:
    """
    Main normalization function for Arabic text.
    Removes diacritics and normalizes characters.
    """
    # Normalize whitespace
    text = normalize_whitespace(text)
    # Remove tatweel
    text = remove_tatweel(text)
    # Normalize hamza
    text = normalize_hamza(text)
    # Normalize alef
    text = normalize_alef(text)
    # Remove diacritics
    text = remove_diacritics(text)
    
    return text


def parse_poet_and_source(source_field: str) -> tuple:
    """
    Parse combined source field into poet and source.
    
    Examples:
        "امرؤ القيس - المعلقة" -> ("امرؤ القيس", "المعلقة")
        "المتنبي" -> ("المتنبي", "")
        "العباسيون" -> ("", "العباسيون")
    """
    # Check if there's a dash separator
    if ' - ' in source_field:
        parts = source_field.split(' - ', 1)
        return parts[0].strip(), parts[1].strip()
    elif '-' in source_field:
        parts = source_field.split('-', 1)
        return parts[0].strip(), parts[1].strip()
    else:
        # Try to detect if it's a poet name or source
        # Common poet indicators: proper names
        # Common source indicators: "مثل عربي", "اختبار", "عام", "تعليمي", "مقتطف"
        source_indicators = ['مثل', 'اختبار', 'عام', 'تعليمي', 'مقتطف', 'العباسيون']
        
        if any(indicator in source_field for indicator in source_indicators):
            return "", source_field
        else:
            # Assume it's a poet name
            return source_field, ""


def enrich_golden_set(input_path: str, output_path: str):
    """
    Enrich golden set with automated fields:
    - verse_id (A5)
    - normalized_text (A4)
    - poet, source (split from combined source field) (A6)
    """
    
    print("🚀 Starting Golden Set Enrichment...")
    print(f"📖 Reading from: {input_path}")
    
    # Read all verses
    verses = []
    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                verses.append(json.loads(line))
    
    print(f"✅ Loaded {len(verses)} verses")
    
    # Enrich each verse
    enriched_verses = []
    for idx, verse in enumerate(verses, start=1):
        # A5: Add verse_id
        verse_id = f"golden_{idx:03d}"
        
        # A4: Add normalized_text
        normalized_text = normalize_arabic_text(verse['text'])
        
        # A6: Split poet and source
        original_source = verse.get('source', '')
        poet, source = parse_poet_and_source(original_source)
        
        # Create enriched verse
        enriched = {
            "verse_id": verse_id,
            "text": verse['text'],
            "normalized_text": normalized_text,
            "meter": verse['meter'],
            "poet": poet,
            "source": source,
            "era": verse['era'],
            "confidence": verse['confidence'],
            "notes": verse['notes']
        }
        
        enriched_verses.append(enriched)
        
        print(f"  [{verse_id}] {poet or source or 'Unknown'}: {verse['meter']}")
    
    # Write enriched data
    with open(output_path, 'w', encoding='utf-8') as f:
        for verse in enriched_verses:
            f.write(json.dumps(verse, ensure_ascii=False) + '\n')
    
    print(f"\n✅ Enriched data written to: {output_path}")
    print(f"📊 Summary:")
    print(f"   - Added verse_id to all {len(enriched_verses)} verses")
    print(f"   - Added normalized_text to all verses")
    print(f"   - Split poet and source fields")
    
    # Show sample
    print(f"\n📝 Sample enriched verse:")
    print(json.dumps(enriched_verses[0], ensure_ascii=False, indent=2))
    
    return enriched_verses


if __name__ == "__main__":
    # Paths
    input_file = Path(__file__).parent.parent / "evaluation" / "golden_set_v0_20.jsonl"
    output_file = Path(__file__).parent.parent / "evaluation" / "golden_set_v0_20_enriched.jsonl"
    
    # Enrich
    enrich_golden_set(str(input_file), str(output_file))
    
    print("\n" + "="*60)
    print("✅ PHASE A Tasks Completed (Automated):")
    print("   ✅ A4: Normalized text added")
    print("   ✅ A5: Verse IDs added (golden_001 to golden_020)")
    print("   ✅ A6: Poet and source fields split")
    print("\n⏳ PHASE A Tasks Remaining (Manual):")
    print("   ❌ A1: Taqti3 annotations (requires prosody expert)")
    print("   ❌ A2: Expected tafa'il arrays (after A1)")
    print("   ❌ A3: Syllable patterns (after A1)")
    print("="*60)
