#!/usr/bin/env python3
"""
Extract missing phonetic patterns from failed verses.

Analyzes failed verses to identify what patterns need to be added.
"""

import sys
import json
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from app.core.phonetics import text_to_phonetic_pattern

# Failed verses from test
FAILED_VERSES = [
    ("golden_101", "قِفا نَبكِ مِن ذِكرى حَبيبٍ وَمَنزِلِ", "الطويل"),
    ("golden_102", "أَرى كُلَّ حَيٍّ هالِكاً وَابنَ هالِكٍ", "الطويل"),
    ("golden_103", "بَدَت مِثلَ قَرنِ الشَمسِ في رَونَقِ الضُحى", "الطويل"),
    ("golden_104", "صَفا كُلُّ شَيءٍ لِلحَبيبِ المُحِبِّ", "الرمل"),
    ("golden_105", "أَلا لَيتَ الشَبابَ يَعودُ يَوماً", "البسيط"),
    ("golden_108", "قُل لِلَّذينَ تَفَرَّقوا أَينَ الوَفاءُ", "الكامل"),
    ("golden_109", "مَن يَهُن يَسهُل الهَوانُ عَلَيهِ", "الوافر"),
    ("golden_110", "وَإِنّي لَأَرجو اللَهَ حَتّى كَأَنَّني", "الطويل"),
    ("golden_111", "أَنا الَّذي نَظَرَ الأَعمى إِلى أَدَبي", "الكامل"),
    ("golden_112", "فَإِن تَفُق أَنا اِبنُ غَسّانَ فَاِعلَموا", "الطويل"),
    ("golden_113", "لا تَسقِني ماءَ الحَياةِ بِذِلَّةٍ", "الكامل"),
    ("golden_114", "وَلَقَد ذَكَرتُكِ وَالرِماحُ نَواهِلٌ", "الطويل"),
    ("golden_115", "إِذا المَرءُ لَم يُدنَس مِنَ اللُؤمِ عِرضُهُ", "الطويل"),
    ("golden_116", "وَقَفتُ عَلى رَبعٍ لِمَيَّةَ ناقَتي", "الطويل"),
    ("golden_117", "أَلَم تَرَ أَنَّ اللَهَ أَعطاكَ صورَةً", "البسيط"),
    ("golden_118", "تَجَلَّدتُ وَالأَيّامُ تَجري عَلَيَّ", "الرمل"),
]

print("=" * 80)
print("EXTRACTING MISSING PHONETIC PATTERNS")
print("=" * 80)
print()

patterns_by_meter = {}

for verse_id, text, expected_meter in FAILED_VERSES:
    print(f"{verse_id}: {text[:50]}...")
    print(f"  Expected meter: {expected_meter}")
    
    # Get phonetic pattern
    phonetic = text_to_phonetic_pattern(text)
    
    if phonetic:
        print(f"  Phonetic: {phonetic}")
        
        if expected_meter not in patterns_by_meter:
            patterns_by_meter[expected_meter] = []
        patterns_by_meter[expected_meter].append(phonetic)
    else:
        print(f"  ⚠️  Could not extract phonetic pattern")
    
    print()

print("=" * 80)
print("PATTERNS TO ADD BY METER")
print("=" * 80)
print()

for meter, patterns in sorted(patterns_by_meter.items()):
    print(f"\n{meter}:")
    print(f"  Count: {len(patterns)} new patterns")
    print(f"  Patterns:")
    for pattern in patterns:
        print(f'    "{pattern}",')

print()
print("=" * 80)
print(f"TOTAL: {sum(len(p) for p in patterns_by_meter.values())} patterns to add across {len(patterns_by_meter)} meters")
print("=" * 80)
