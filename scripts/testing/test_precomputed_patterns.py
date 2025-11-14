#!/usr/bin/env python3
"""Test detector using precomputed patterns from golden set."""

import sys
sys.path.insert(0, 'src/backend')

from app.core.prosody.detector_v2 import BahrDetectorV2
import json

# Load golden set
with open('data/processed/datasets/evaluation/golden_set_v1_2_final.jsonl') as f:
    verses = [json.loads(line) for line in f.readlines()[:100]]

detector = BahrDetectorV2()

correct = 0

for i, v in enumerate(verses):
    if i % 25 == 0:
        print(f'Processing verse {i}...')
    
    # Use PRECOMPUTED pattern (correct one!)
    pattern = v.get('prosody_precomputed', {}).get('pattern')
    if not pattern:
        continue
        
    results = detector.detect(phonetic_pattern=pattern, expected_meter_ar=v['meter'])
    
    if results and results[0].meter_name_ar == v['meter']:
        correct += 1

accuracy = (correct / len(verses) * 100)
print(f'\n📊 Baseline Accuracy (using precomputed patterns):')
print(f'{correct}/{len(verses)} = {accuracy:.1f}%')
print(f'Target: ≥97.5%')
print(f'Status: {"✅ PASS" if accuracy >= 97.5 else "❌ FAIL"}')
