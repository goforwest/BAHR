#!/usr/bin/env python3
"""
Global Duplicate Checker

Checks for duplicate verses across the entire poetry database and new verses.
Prevents duplication before integration into poetry_sources.py.
"""

import sys
import json
import hashlib
from pathlib import Path
from typing import List, Dict, Set, Tuple
from difflib import SequenceMatcher

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

import poetry_sources


def normalize_text(text: str) -> str:
    """
    Normalize Arabic text for comparison.
    Uses same normalization as evaluate_dataset_quality.py.
    """
    # Remove diacritics
    diacritics = 'ًٌٍَُِّْ'
    for mark in diacritics:
        text = text.replace(mark, '')
    
    # Normalize hamza forms
    text = text.replace('إ', 'ا').replace('أ', 'ا').replace('آ', 'ا')
    
    # Normalize alif maqsura
    text = text.replace('ى', 'ي')
    
    # Normalize taa marbouta
    text = text.replace('ة', 'ه')
    
    # Normalize whitespace
    text = ' '.join(text.split())
    
    return text.strip()


def get_fingerprint(text: str) -> str:
    """Get unique fingerprint for verse text."""
    normalized = normalize_text(text)
    return hashlib.md5(normalized.encode('utf-8')).hexdigest()


def calculate_similarity(text1: str, text2: str) -> float:
    """Calculate similarity percentage between two texts."""
    norm1 = normalize_text(text1)
    norm2 = normalize_text(text2)
    return SequenceMatcher(None, norm1, norm2).ratio() * 100


def load_existing_verses() -> Dict[str, List[Dict]]:
    """Load all existing verses from poetry_sources.py."""
    meters = poetry_sources.list_available_meters()
    all_verses = {}
    
    for meter in meters:
        verses = poetry_sources.get_verses_by_meter(meter)
        all_verses[meter] = verses
    
    return all_verses


def build_fingerprint_index(verses_by_meter: Dict[str, List[Dict]]) -> Dict[str, List[Dict]]:
    """Build index of verse fingerprints for fast lookup."""
    fingerprint_index = {}
    
    for meter, verses in verses_by_meter.items():
        for verse in verses:
            text = verse.get('text', '')
            fingerprint = get_fingerprint(text)
            
            if fingerprint not in fingerprint_index:
                fingerprint_index[fingerprint] = []
            
            fingerprint_index[fingerprint].append({
                'meter': meter,
                'verse': verse
            })
    
    return fingerprint_index


def check_exact_duplicates(new_verses: List[Dict], 
                          fingerprint_index: Dict[str, List[Dict]]) -> List[Dict]:
    """Check for exact duplicates."""
    duplicates = []
    
    for i, verse in enumerate(new_verses):
        text = verse.get('text', '')
        fingerprint = get_fingerprint(text)
        
        if fingerprint in fingerprint_index:
            existing = fingerprint_index[fingerprint]
            duplicates.append({
                'new_verse_index': i,
                'new_verse': verse,
                'existing_matches': existing,
                'type': 'exact'
            })
    
    return duplicates


def check_fuzzy_duplicates(new_verses: List[Dict], 
                          all_existing: Dict[str, List[Dict]],
                          threshold: float = 90.0) -> List[Dict]:
    """Check for fuzzy duplicates (similar but not exact)."""
    fuzzy_duplicates = []
    
    # Flatten existing verses
    existing_verses = []
    for meter, verses in all_existing.items():
        for verse in verses:
            existing_verses.append({
                'meter': meter,
                'verse': verse
            })
    
    for i, new_verse in enumerate(new_verses):
        new_text = new_verse.get('text', '')
        
        # Compare with all existing
        for existing in existing_verses:
            existing_text = existing['verse'].get('text', '')
            similarity = calculate_similarity(new_text, existing_text)
            
            if similarity >= threshold:
                fuzzy_duplicates.append({
                    'new_verse_index': i,
                    'new_verse': new_verse,
                    'existing_verse': existing['verse'],
                    'existing_meter': existing['meter'],
                    'similarity': similarity,
                    'type': 'fuzzy'
                })
    
    return fuzzy_duplicates


def check_internal_duplicates(verses: List[Dict]) -> List[Dict]:
    """Check for duplicates within the new verse list itself."""
    internal_dupes = []
    fingerprints = {}
    
    for i, verse in enumerate(verses):
        text = verse.get('text', '')
        fingerprint = get_fingerprint(text)
        
        if fingerprint in fingerprints:
            internal_dupes.append({
                'verse_index_1': fingerprints[fingerprint],
                'verse_index_2': i,
                'verse': verse,
                'type': 'internal'
            })
        else:
            fingerprints[fingerprint] = i
    
    return internal_dupes


def load_new_verses(file_path: str) -> List[Dict]:
    """Load new verses from JSON file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Handle both list and dict formats
    if isinstance(data, list):
        return data
    elif isinstance(data, dict) and 'verses' in data:
        return data['verses']
    else:
        raise ValueError('JSON must be a list of verses or dict with "verses" key')


def print_duplicate_report(exact: List[Dict], fuzzy: List[Dict], internal: List[Dict]):
    """Print comprehensive duplicate report."""
    print(f'\n{"="*70}')
    print(f'DUPLICATE DETECTION REPORT')
    print(f'{"="*70}')
    print(f'Exact duplicates:    {len(exact)}')
    print(f'Fuzzy duplicates:    {len(fuzzy)}')
    print(f'Internal duplicates: {len(internal)}')
    print(f'Total issues:        {len(exact) + len(fuzzy) + len(internal)}')
    print(f'{"="*70}\n')
    
    # Show exact duplicates
    if exact:
        print(f'❌ Exact Duplicates ({len(exact)}):')
        print(f'{"-"*70}')
        for i, dup in enumerate(exact[:5], 1):  # Show first 5
            verse = dup['new_verse']
            matches = dup['existing_matches']
            print(f'{i}. New verse: {verse.get("text", "")[:60]}...')
            print(f'   Found in {len(matches)} location(s):')
            for match in matches:
                print(f'   - {match["meter"]}: {match["verse"].get("poet", "Unknown")}')
            print()
        
        if len(exact) > 5:
            print(f'... and {len(exact) - 5} more exact duplicates\n')
    
    # Show fuzzy duplicates
    if fuzzy:
        print(f'⚠️  Fuzzy Duplicates ({len(fuzzy)}):')
        print(f'{"-"*70}')
        for i, dup in enumerate(fuzzy[:5], 1):  # Show first 5
            new_verse = dup['new_verse']
            existing = dup['existing_verse']
            print(f'{i}. New verse: {new_verse.get("text", "")[:60]}...')
            print(f'   Similar to ({dup["similarity"]:.1f}%):')
            print(f'   {existing.get("text", "")[:60]}...')
            print(f'   Meter: {dup["existing_meter"]}, Poet: {existing.get("poet", "Unknown")}')
            print()
        
        if len(fuzzy) > 5:
            print(f'... and {len(fuzzy) - 5} more fuzzy duplicates\n')
    
    # Show internal duplicates
    if internal:
        print(f'🔄 Internal Duplicates ({len(internal)}):')
        print(f'{"-"*70}')
        for i, dup in enumerate(internal[:5], 1):  # Show first 5
            print(f'{i}. Indices {dup["verse_index_1"]} and {dup["verse_index_2"]} are duplicates')
            print(f'   {dup["verse"].get("text", "")[:60]}...')
            print()
        
        if len(internal) > 5:
            print(f'... and {len(internal) - 5} more internal duplicates\n')
    
    if not exact and not fuzzy and not internal:
        print(f'✅ No duplicates found - all verses are unique!\n')


def remove_duplicates(verses: List[Dict], 
                     exact: List[Dict], 
                     fuzzy: List[Dict], 
                     internal: List[Dict]) -> List[Dict]:
    """Remove all duplicate verses and return clean list."""
    # Collect indices to remove
    to_remove = set()
    
    # Exact duplicates
    for dup in exact:
        to_remove.add(dup['new_verse_index'])
    
    # Fuzzy duplicates (optional - user should review)
    # for dup in fuzzy:
    #     to_remove.add(dup['new_verse_index'])
    
    # Internal duplicates (keep first occurrence)
    for dup in internal:
        to_remove.add(dup['verse_index_2'])
    
    # Filter verses
    clean_verses = [v for i, v in enumerate(verses) if i not in to_remove]
    
    return clean_verses


def export_clean_verses(verses: List[Dict], output_file: str):
    """Export clean verses (duplicates removed)."""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(verses, f, ensure_ascii=False, indent=2)
    
    print(f'✅ Exported {len(verses)} clean verses to {output_file}')


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Check for duplicate verses')
    parser.add_argument('--new', '-n', type=str, 
                       help='JSON file with new verses to check')
    parser.add_argument('--fuzzy-threshold', '-t', type=float, default=90.0, 
                       help='Similarity threshold for fuzzy matching (default: 90.0)')
    parser.add_argument('--export-clean', '-c', type=str, 
                       help='Export clean verses (duplicates removed) to file')
    parser.add_argument('--check-database', '-d', action='store_true', 
                       help='Check for duplicates within poetry_sources.py itself')
    
    args = parser.parse_args()
    
    if args.check_database:
        # Check existing database for internal duplicates
        print('Loading existing poetry database...')
        all_verses = load_existing_verses()
        
        # Flatten and check
        all_flat = []
        for meter, verses in all_verses.items():
            all_flat.extend(verses)
        
        print(f'Checking {len(all_flat)} verses for duplicates...')
        internal = check_internal_duplicates(all_flat)
        
        if internal:
            print(f'\n❌ Found {len(internal)} duplicates in poetry_sources.py!')
            print_duplicate_report([], [], internal)
        else:
            print(f'\n✅ No duplicates found in poetry_sources.py')
        
        sys.exit(0 if not internal else 1)
    
    if not args.new:
        print('❌ Error: Must provide --new file or use --check-database')
        parser.print_help()
        sys.exit(1)
    
    # Load new verses
    print(f'Loading new verses from {args.new}...')
    try:
        new_verses = load_new_verses(args.new)
        print(f'✅ Loaded {len(new_verses)} new verses')
    except Exception as e:
        print(f'❌ Error loading new verses: {e}')
        sys.exit(1)
    
    # Load existing database
    print('Loading existing poetry database...')
    all_verses = load_existing_verses()
    fingerprint_index = build_fingerprint_index(all_verses)
    print(f'✅ Loaded {sum(len(v) for v in all_verses.values())} existing verses')
    
    # Check for duplicates
    print(f'\nChecking for duplicates...')
    exact = check_exact_duplicates(new_verses, fingerprint_index)
    fuzzy = check_fuzzy_duplicates(new_verses, all_verses, args.fuzzy_threshold)
    internal = check_internal_duplicates(new_verses)
    
    # Print report
    print_duplicate_report(exact, fuzzy, internal)
    
    # Export clean if requested
    if args.export_clean:
        clean = remove_duplicates(new_verses, exact, fuzzy, internal)
        removed = len(new_verses) - len(clean)
        print(f'\nRemoved {removed} duplicate verses')
        export_clean_verses(clean, args.export_clean)
    
    # Exit code
    total_issues = len(exact) + len(fuzzy) + len(internal)
    sys.exit(0 if total_issues == 0 else 1)


if __name__ == '__main__':
    main()
