#!/usr/bin/env python3
"""
Schema Validator for BAHR Golden Set

Validates verses in golden_set_v0_20_complete.jsonl against the JSON schema.
"""

import json
import sys
from pathlib import Path

try:
    from jsonschema import validate, ValidationError, Draft7Validator
except ImportError:
    print("ERROR: jsonschema library not installed")
    print("Install with: pip3 install jsonschema")
    sys.exit(1)


def load_schema(schema_path: Path) -> dict:
    """Load JSON schema from file."""
    with open(schema_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_verses(jsonl_path: Path) -> list:
    """Load verses from JSONL file."""
    verses = []
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            try:
                verse = json.loads(line)
                verses.append((line_num, verse))
            except json.JSONDecodeError as e:
                print(f"⚠️  Line {line_num}: Invalid JSON - {e}")
    return verses


def validate_verses(verses: list, schema: dict) -> dict:
    """
    Validate all verses against schema.
    
    Returns:
        dict: Validation results summary
    """
    validator = Draft7Validator(schema)
    
    results = {
        'total': len(verses),
        'valid': 0,
        'invalid': 0,
        'errors': []
    }
    
    for line_num, verse in verses:
        errors = list(validator.iter_errors(verse))
        
        if errors:
            results['invalid'] += 1
            verse_id = verse.get('verse_id', f'line_{line_num}')
            
            for error in errors:
                results['errors'].append({
                    'verse_id': verse_id,
                    'line': line_num,
                    'field': '.'.join(str(p) for p in error.path),
                    'message': error.message,
                    'validator': error.validator
                })
        else:
            results['valid'] += 1
    
    return results


def print_validation_report(results: dict):
    """Print formatted validation report."""
    print("\n" + "="*70)
    print("📋 GOLDEN SET SCHEMA VALIDATION REPORT")
    print("="*70)
    
    print(f"\n✅ Valid verses: {results['valid']}/{results['total']}")
    print(f"❌ Invalid verses: {results['invalid']}/{results['total']}")
    
    if results['errors']:
        print(f"\n⚠️  {len(results['errors'])} VALIDATION ERRORS FOUND:\n")
        
        # Group errors by verse
        by_verse = {}
        for error in results['errors']:
            vid = error['verse_id']
            if vid not in by_verse:
                by_verse[vid] = []
            by_verse[vid].append(error)
        
        for verse_id, errors in by_verse.items():
            print(f"  {verse_id}:")
            for err in errors:
                field = err['field'] or '(root)'
                print(f"    • Field '{field}': {err['message']}")
            print()
    else:
        print("\n🎉 All verses passed schema validation!")
    
    print("="*70 + "\n")


def main():
    """Main validation function."""
    script_dir = Path(__file__).parent
    eval_dir = script_dir.parent / 'evaluation'
    
    schema_path = eval_dir / 'golden_set_schema.json'
    data_path = eval_dir / 'golden_set_v0_20_complete.jsonl'
    
    # Check files exist
    if not schema_path.exists():
        print(f"❌ Schema file not found: {schema_path}")
        sys.exit(1)
    
    if not data_path.exists():
        print(f"❌ Data file not found: {data_path}")
        sys.exit(1)
    
    print(f"📂 Loading schema from: {schema_path.name}")
    schema = load_schema(schema_path)
    
    print(f"📂 Loading verses from: {data_path.name}")
    verses = load_verses(data_path)
    
    if not verses:
        print("❌ No verses found in data file")
        sys.exit(1)
    
    print(f"✅ Loaded {len(verses)} verses\n")
    print("🔍 Validating verses against schema...")
    
    results = validate_verses(verses, schema)
    print_validation_report(results)
    
    # Exit with error code if validation failed
    if results['invalid'] > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
