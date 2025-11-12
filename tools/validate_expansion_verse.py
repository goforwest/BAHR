#!/usr/bin/env python3
"""
Validate verses for golden set expansion.

Usage:
    python tools/validate_expansion_verse.py <verse_json_string>
    python tools/validate_expansion_verse.py --file <path_to_jsonl>
"""

import json
import sys
import re
from pathlib import Path
from datetime import datetime

# Arabic diacritics
ARABIC_DIACRITICS = [
    '\u064B',  # Fathatan
    '\u064C',  # Dammatan
    '\u064D',  # Kasratan
    '\u064E',  # Fatha
    '\u064F',  # Damma
    '\u0650',  # Kasra
    '\u0651',  # Shadda
    '\u0652',  # Sukun
    '\u0653',  # Maddah
    '\u0654',  # Hamza above
    '\u0655',  # Hamza below
    '\u0656',  # Subscript alef
    '\u0657',  # Inverted damma
    '\u0658',  # Mark noon ghunna
]

REQUIRED_FIELDS = [
    'verse_id', 'text', 'normalized_text', 'meter', 'poet',
    'poem_title', 'source', 'prosody_precomputed', 'validation', 'metadata'
]

VALID_METERS = [
    'الطويل', 'المديد', 'البسيط', 'الوافر', 'الكامل', 'الهزج', 'الرجز',
    'الرمل', 'السريع', 'المنسرح', 'الخفيف', 'المضارع', 'المقتضب',
    'المجتث', 'المتقارب', 'المتدارك',
    'الكامل (مجزوء)', 'الكامل (3 تفاعيل)', 'الرمل (مجزوء)',
    'المتقارب (مجزوء)', 'البسيط (مجزوء)', 'الهزج (مجزوء)',
    'السريع (مفعولات)', 'الوافر (مجزوء)', 'الطويل (مجزوء)',
    'المنسرح (مجزوء)', 'الخفيف (مجزوء)', 'الرجز (مجزوء)',
]


def has_diacritics(text: str) -> bool:
    """Check if text contains Arabic diacritics."""
    return any(diacritic in text for diacritic in ARABIC_DIACRITICS)


def count_diacritics(text: str) -> int:
    """Count number of diacritics in text."""
    return sum(text.count(diacritic) for diacritic in ARABIC_DIACRITICS)


def is_fully_diacritized(text: str) -> tuple[bool, str]:
    """
    Check if text is fully diacritized.
    Returns (is_valid, message)
    """
    # Remove spaces and punctuation for counting
    arabic_letters = re.findall(r'[\u0600-\u06FF]', text)
    arabic_letters = [c for c in arabic_letters if c not in ARABIC_DIACRITICS]

    diacritic_count = count_diacritics(text)
    letter_count = len(arabic_letters)

    if diacritic_count == 0:
        return False, "No diacritics found"

    # Heuristic: at least 70% of letters should have diacritics
    ratio = diacritic_count / letter_count if letter_count > 0 else 0

    if ratio < 0.7:
        return False, f"Insufficient diacritics: {diacritic_count}/{letter_count} ({ratio:.1%})"

    return True, f"Well diacritized: {diacritic_count} diacritics for {letter_count} letters ({ratio:.1%})"


def normalize_text(text: str) -> str:
    """Remove diacritics from text."""
    normalized = text
    for diacritic in ARABIC_DIACRITICS:
        normalized = normalized.replace(diacritic, '')
    return normalized


def validate_verse(verse: dict, existing_ids: set = None) -> dict:
    """
    Validate a verse entry.
    Returns dict with 'valid': bool, 'errors': list, 'warnings': list
    """
    errors = []
    warnings = []

    # Check required fields
    for field in REQUIRED_FIELDS:
        if field not in verse:
            errors.append(f"Missing required field: {field}")

    if errors:  # Don't continue if missing required fields
        return {'valid': False, 'errors': errors, 'warnings': warnings}

    # Validate verse_id format
    if not re.match(r'^golden_\d{3}$', verse['verse_id']):
        errors.append(f"Invalid verse_id format: {verse['verse_id']} (expected: golden_XXX)")

    # Check for duplicate verse_id
    if existing_ids and verse['verse_id'] in existing_ids:
        errors.append(f"Duplicate verse_id: {verse['verse_id']}")

    # Validate meter
    if verse['meter'] not in VALID_METERS:
        warnings.append(f"Unusual meter name: {verse['meter']} (not in standard list)")

    # Check diacritization
    is_diacritized, diacritic_msg = is_fully_diacritized(verse['text'])
    if not is_diacritized:
        errors.append(f"Text not fully diacritized: {diacritic_msg}")
    else:
        warnings.append(diacritic_msg)

    # Validate normalized_text
    expected_normalized = normalize_text(verse['text'])
    if verse['normalized_text'] != expected_normalized:
        warnings.append(f"normalized_text mismatch (expected: {expected_normalized})")

    # Check prosody_precomputed structure
    prosody = verse.get('prosody_precomputed', {})
    required_prosody_fields = ['pattern', 'fitness_score', 'method', 'meter_verified']
    for field in required_prosody_fields:
        if field not in prosody:
            errors.append(f"Missing prosody_precomputed field: {field}")

    # Check validation structure
    validation = verse.get('validation', {})
    required_validation_fields = ['verified_by', 'verified_date', 'automated_check']
    for field in required_validation_fields:
        if field not in validation:
            errors.append(f"Missing validation field: {field}")

    # Validate date format
    if 'verified_date' in validation:
        try:
            datetime.strptime(validation['verified_date'], '%Y-%m-%d')
        except ValueError:
            errors.append(f"Invalid date format: {validation['verified_date']} (expected: YYYY-MM-DD)")

    # Check metadata structure
    metadata = verse.get('metadata', {})
    required_metadata_fields = ['version', 'phase']
    for field in required_metadata_fields:
        if field not in metadata:
            errors.append(f"Missing metadata field: {field}")

    # Check for empty strings
    if not verse.get('text', '').strip():
        errors.append("Empty text field")
    if not verse.get('poet', '').strip():
        warnings.append("Empty poet field")
    if not verse.get('poem_title', '').strip():
        warnings.append("Empty poem_title field")

    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings
    }


def validate_jsonl_file(filepath: Path) -> dict:
    """Validate all verses in a JSONL file."""
    results = {
        'total': 0,
        'valid': 0,
        'invalid': 0,
        'verses': []
    }

    existing_ids = set()

    with open(filepath, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue

            try:
                verse = json.loads(line)
                validation = validate_verse(verse, existing_ids)

                results['total'] += 1
                if validation['valid']:
                    results['valid'] += 1
                else:
                    results['invalid'] += 1

                results['verses'].append({
                    'line': line_num,
                    'verse_id': verse.get('verse_id', 'unknown'),
                    'validation': validation
                })

                existing_ids.add(verse.get('verse_id'))

            except json.JSONDecodeError as e:
                results['total'] += 1
                results['invalid'] += 1
                results['verses'].append({
                    'line': line_num,
                    'verse_id': 'parse_error',
                    'validation': {
                        'valid': False,
                        'errors': [f"JSON parse error: {e}"],
                        'warnings': []
                    }
                })

    return results


def print_validation_results(results: dict):
    """Print validation results in a readable format."""
    print(f"\n{'='*70}")
    print(f"VALIDATION RESULTS")
    print(f"{'='*70}")
    print(f"Total verses: {results['total']}")
    print(f"Valid: {results['valid']}")
    print(f"Invalid: {results['invalid']}")
    print(f"{'='*70}\n")

    for verse_result in results['verses']:
        validation = verse_result['validation']

        if not validation['valid'] or validation['warnings']:
            print(f"Line {verse_result['line']}: {verse_result['verse_id']}")

            if validation['errors']:
                print("  ❌ ERRORS:")
                for error in validation['errors']:
                    print(f"     - {error}")

            if validation['warnings']:
                print("  ⚠️  WARNINGS:")
                for warning in validation['warnings']:
                    print(f"     - {warning}")

            print()


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python tools/validate_expansion_verse.py <verse_json_string>")
        print("  python tools/validate_expansion_verse.py --file <path_to_jsonl>")
        sys.exit(1)

    if sys.argv[1] == '--file':
        if len(sys.argv) < 3:
            print("Error: --file requires a path argument")
            sys.exit(1)

        filepath = Path(sys.argv[2])
        if not filepath.exists():
            print(f"Error: File not found: {filepath}")
            sys.exit(1)

        results = validate_jsonl_file(filepath)
        print_validation_results(results)

        if results['invalid'] > 0:
            sys.exit(1)
    else:
        # Validate single verse from JSON string
        try:
            verse = json.loads(sys.argv[1])
            validation = validate_verse(verse)

            print(f"\nValidation result for: {verse.get('verse_id', 'unknown')}")
            print(f"Valid: {validation['valid']}")

            if validation['errors']:
                print("\n❌ ERRORS:")
                for error in validation['errors']:
                    print(f"  - {error}")

            if validation['warnings']:
                print("\n⚠️  WARNINGS:")
                for warning in validation['warnings']:
                    print(f"  - {warning}")

            if not validation['valid']:
                sys.exit(1)

        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON: {e}")
            sys.exit(1)


if __name__ == '__main__':
    main()
