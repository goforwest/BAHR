#!/usr/bin/env python3
"""Analyze Golden Set completeness and distribution."""

import json
from collections import Counter

with open('/Users/hamoudi/Desktop/Personal/BAHR/dataset/evaluation/golden_set_v0_20.jsonl') as f:
    data = [json.loads(line) for line in f]

print('=== GOLDEN SET ANALYSIS ===\n')

print(f'Total verses: {len(data)}')
print()

print('Meter Distribution:')
meters = Counter(d.get('meter', 'N/A') for d in data)
for meter, count in sorted(meters.items(), key=lambda x: -x[1]):
    print(f'  {meter}: {count}')
print()

print('Field Completeness:')
print(f'  All have text: {all("text" in d and d["text"] for d in data)}')
print(f'  All have meter: {all("meter" in d and d["meter"] for d in data)}')
print(f'  All have source: {all("source" in d and d["source"] for d in data)}')
print(f'  All have era: {all("era" in d and d["era"] for d in data)}')
print(f'  All have confidence: {all("confidence" in d for d in data)}')
print(f'  All have notes: {all("notes" in d and d["notes"] for d in data)}')
print()

print('Missing Fields:')
print(f'  Missing taqti3: {sum(1 for d in data if "taqti3" not in d or not d.get("taqti3"))}')
print(f'  Missing pattern: {sum(1 for d in data if "pattern" not in d or not d.get("pattern"))}')
print(f'  Missing verse_id: {sum(1 for d in data if "verse_id" not in d or not d.get("verse_id"))}')
print(f'  Missing poet: {sum(1 for d in data if "poet" not in d or not d.get("poet"))}')
print(f'  Missing normalized_text: {sum(1 for d in data if "normalized_text" not in d)}')
print(f'  Missing expected_tafail: {sum(1 for d in data if "expected_tafail" not in d)}')
print(f'  Missing syllable_pattern: {sum(1 for d in data if "syllable_pattern" not in d)}')
print(f'  Missing validation info: {sum(1 for d in data if "validation" not in d)}')
print(f'  Missing metadata: {sum(1 for d in data if "metadata" not in d)}')
print()

print('Diacritics:')
diacritic_chars = '\u064B\u064C\u064D\u064E\u064F\u0650\u0651\u0652'
print(f'  With diacritics: {sum(1 for d in data if any(c in d["text"] for c in diacritic_chars))}')
print(f'  Without diacritics: {sum(1 for d in data if not any(c in d["text"] for c in diacritic_chars))}')
print()

print('Sample verse:')
print(json.dumps(data[0], ensure_ascii=False, indent=2))
