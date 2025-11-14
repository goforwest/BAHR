#!/usr/bin/env python3
"""
Test prosody engine generalization with NEW verses not in Golden Set.

This validates whether our pattern matching generalizes beyond the training data,
or if we've just memorized the Golden Set.

New verses selected from classical Arabic poetry NOT in golden_set_v0_100_complete.jsonl
"""

import sys
import json
from pathlib import Path
from typing import Dict, List

# Add backend to path
backend_path = Path(__file__).parent.parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from app.core.bahr_detector import BahrDetector

# New test verses - authentic classical Arabic poetry NOT in Golden Set
NEW_TEST_VERSES = [
    {
        "verse_id": "test_001",
        "text": "قِفا نَبكِ مِن ذِكرى حَبيبٍ وَمَنزِلِ",
        "meter": "الطويل",
        "poet": "امرؤ القيس",
        "source": "معلقة امرؤ القيس",
        "notes": "Opening verse of Imru' al-Qais's famous mu'allaqah"
    },
    {
        "verse_id": "test_002", 
        "text": "أَرى كُلَّ حَيٍّ هالِكاً وَابنَ هالِكٍ",
        "meter": "الطويل",
        "poet": "لبيد بن ربيعة",
        "source": "معلقة لبيد",
        "notes": "Famous verse about mortality"
    },
    {
        "verse_id": "test_003",
        "text": "بَدَت مِثلَ قَرنِ الشَمسِ في رَونَقِ الضُحى",
        "meter": "الطويل",
        "poet": "امرؤ القيس",
        "source": "ديوان امرؤ القيس",
        "notes": "Describing beauty"
    },
    {
        "verse_id": "test_004",
        "text": "صَفا كُلُّ شَيءٍ لِلحَبيبِ المُحِبِّ",
        "meter": "الرمل",
        "poet": "ابن الفارض",
        "source": "الديوان",
        "notes": "Sufi mystical poetry"
    },
    {
        "verse_id": "test_005",
        "text": "أَلا لَيتَ الشَبابَ يَعودُ يَوماً",
        "meter": "البسيط",
        "poet": "أبو العتاهية",
        "source": "ديوان أبو العتاهية",
        "notes": "Famous lament for lost youth"
    },
    {
        "verse_id": "test_006",
        "text": "تَوَكَّلتُ في رِزقي عَلى اللَهِ خالِقي",
        "meter": "الكامل",
        "poet": "الإمام الشافعي",
        "source": "ديوان الشافعي",
        "notes": "About trust in God for provision"
    },
    {
        "verse_id": "test_007",
        "text": "يا مَن يَعِزُّ عَلَينا أَن نُفارِقَهُم",
        "meter": "الخفيف",
        "poet": "ابن زيدون",
        "source": "رسالة ابن زيدون",
        "notes": "Expression of longing"
    },
    {
        "verse_id": "test_008",
        "text": "قُل لِلَّذينَ تَفَرَّقوا أَينَ الوَفاءُ",
        "meter": "الكامل",
        "poet": "ابن الرومي",
        "source": "ديوان ابن الرومي",
        "notes": "About broken promises"
    },
    {
        "verse_id": "test_009",
        "text": "مَن يَهُن يَسهُل الهَوانُ عَلَيهِ",
        "meter": "الوافر",
        "poet": "المتنبي",
        "source": "ديوان المتنبي",
        "notes": "About dignity and honor"
    },
    {
        "verse_id": "test_010",
        "text": "وَإِنّي لَأَرجو اللَهَ حَتّى كَأَنَّني",
        "meter": "الطويل",
        "poet": "عنترة بن شداد",
        "source": "معلقة عنترة",
        "notes": "Expression of hope in God"
    },
    {
        "verse_id": "test_011",
        "text": "أَنا الَّذي نَظَرَ الأَعمى إِلى أَدَبي",
        "meter": "الكامل",
        "poet": "المتنبي",
        "source": "ديوان المتنبي",
        "notes": "Famous boast about his eloquence"
    },
    {
        "verse_id": "test_012",
        "text": "فَإِن تَفُق أَنا اِبنُ غَسّانَ فَاِعلَموا",
        "meter": "الطويل",
        "poet": "النابغة الذبياني",
        "source": "معلقة النابغة",
        "notes": "Pride in lineage"
    },
    {
        "verse_id": "test_013",
        "text": "لا تَسقِني ماءَ الحَياةِ بِذِلَّةٍ",
        "meter": "الكامل",
        "poet": "أبو فراس الحمداني",
        "source": "الديوان",
        "notes": "Preferring death to dishonor"
    },
    {
        "verse_id": "test_014",
        "text": "وَلَقَد ذَكَرتُكِ وَالرِماحُ نَواهِلٌ",
        "meter": "الطويل",
        "poet": "عنترة بن شداد",
        "source": "معلقة عنترة",
        "notes": "Remembering beloved during battle"
    },
    {
        "verse_id": "test_015",
        "text": "إِذا المَرءُ لَم يُدنَس مِنَ اللُؤمِ عِرضُهُ",
        "meter": "الطويل",
        "poet": "حاتم الطائي",
        "source": "ديوان حاتم",
        "notes": "About honor and character"
    },
    {
        "verse_id": "test_016",
        "text": "وَقَفتُ عَلى رَبعٍ لِمَيَّةَ ناقَتي",
        "meter": "الطويل",
        "poet": "ذو الرمة",
        "source": "ديوان ذو الرمة",
        "notes": "Standing at beloved's dwelling"
    },
    {
        "verse_id": "test_017",
        "text": "أَلَم تَرَ أَنَّ اللَهَ أَعطاكَ صورَةً",
        "meter": "البسيط",
        "poet": "أبو نواس",
        "source": "الديوان",
        "notes": "About divine gifts"
    },
    {
        "verse_id": "test_018",
        "text": "تَجَلَّدتُ وَالأَيّامُ تَجري عَلَيَّ",
        "meter": "الرمل",
        "poet": "أبو الطيب المتنبي",
        "source": "ديوان المتنبي",
        "notes": "Enduring hardship"
    },
    {
        "verse_id": "test_019",
        "text": "أَلا يا صَبا نَجدٍ مَتى هِجتَ مِن نَجدِ",
        "meter": "الطويل",
        "poet": "أحمد شوقي",
        "source": "الشوقيات",
        "notes": "Modern classical poetry - nostalgia"
    },
    {
        "verse_id": "test_020",
        "text": "فَسِرتُ إِلَيها وَالظَلامُ مُرَوَّعٌ",
        "meter": "الطويل",
        "poet": "امرؤ القيس",
        "source": "معلقة امرؤ القيس",
        "notes": "Night journey"
    },
]


def test_generalization():
    """Test prosody engine on completely new verses."""
    print("=" * 80)
    print("GENERALIZATION TEST - New Verses NOT in Golden Set")
    print("=" * 80)
    print()
    print(f"Testing with {len(NEW_TEST_VERSES)} authentic Arabic poetry verses")
    print("These verses were NOT used to build the phonetic patterns database")
    print()
    
    detector = BahrDetector()
    results = []
    
    # Test each verse
    print("Testing meter detection...")
    for verse_data in NEW_TEST_VERSES:
        result = detector.analyze_verse(verse_data['text'])
        
        predicted = result.name_ar if result else None
        expected = verse_data['meter']
        confidence = result.confidence if result else 0.0
        
        results.append({
            'verse_id': verse_data['verse_id'],
            'text': verse_data['text'],
            'poet': verse_data['poet'],
            'expected': expected,
            'predicted': predicted,
            'confidence': confidence,
            'correct': (predicted == expected)
        })
    
    print()
    print("=" * 80)
    print("RESULTS")
    print("=" * 80)
    print()
    
    # Calculate accuracy
    correct = sum(1 for r in results if r['correct'])
    total = len(results)
    accuracy = correct / total
    
    print(f"📊 Overall Accuracy: {correct}/{total} ({accuracy:.1%})")
    print()
    
    # By meter
    by_meter = {}
    for r in results:
        meter = r['expected']
        if meter not in by_meter:
            by_meter[meter] = {'correct': 0, 'total': 0}
        by_meter[meter]['total'] += 1
        if r['correct']:
            by_meter[meter]['correct'] += 1
    
    print("📏 Accuracy by Meter:")
    print("-" * 80)
    for meter in sorted(by_meter.keys()):
        stats = by_meter[meter]
        acc = stats['correct'] / stats['total'] if stats['total'] > 0 else 0
        status = "✓" if acc >= 0.80 else "✗"
        print(f"  {status} {meter:15s}: {stats['correct']:2d}/{stats['total']:2d} ({acc:5.1%})")
    print()
    
    # Show failures
    failures = [r for r in results if not r['correct']]
    if failures:
        print(f"❌ Failed Verses ({len(failures)} total):")
        print("-" * 80)
        for r in failures:
            print(f"  • {r['verse_id']} - {r['poet']}")
            print(f"    Expected: {r['expected']}")
            print(f"    Predicted: {r['predicted']} (confidence: {r['confidence']:.2f})")
            print(f"    Text: {r['text'][:60]}...")
            print()
    else:
        print("✅ All new verses passed! Perfect generalization!")
        print()
    
    # Assessment
    print("=" * 80)
    print("GENERALIZATION ASSESSMENT")
    print("=" * 80)
    print()
    
    if accuracy >= 0.90:
        print("✅ EXCELLENT: ≥90% accuracy on unseen data")
        print("   → Pattern database generalizes very well")
        print("   → Hardcoded patterns are representative")
        print("   → Safe for production deployment")
    elif accuracy >= 0.80:
        print("✓ GOOD: ≥80% accuracy on unseen data")
        print("   → Pattern database generalizes adequately")
        print("   → Some edge cases need attention")
        print("   → Acceptable for MVP deployment")
    elif accuracy >= 0.70:
        print("⚠️ MODERATE: 70-80% accuracy on unseen data")
        print("   → Pattern database has gaps")
        print("   → Consider implementing Levenshtein distance")
        print("   → May need more patterns or better algorithm")
    else:
        print("❌ POOR: <70% accuracy on unseen data")
        print("   → Overfitting detected!")
        print("   → Must implement proper fuzzy matching")
        print("   → Hardcoded patterns not sufficient")
    
    print()
    
    # Save results
    output_path = Path(__file__).parent.parent / "evaluation" / "generalization_test_results.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({
            'test_date': '2025-11-11',
            'total_verses': total,
            'correct': correct,
            'accuracy': accuracy,
            'by_meter': by_meter,
            'failures': failures,
            'all_results': results
        }, f, ensure_ascii=False, indent=2)
    
    print(f"📄 Detailed results saved to: {output_path}")
    print()
    
    return results, accuracy


def recommend_additions(results: List[Dict], accuracy: float):
    """Recommend which verses to add to Golden Set."""
    print("=" * 80)
    print("RECOMMENDATIONS FOR GOLDEN SET v0.101")
    print("=" * 80)
    print()
    
    if accuracy >= 0.95:
        print("✨ Excellent generalization! All test verses are unique and valuable.")
        print()
        print("💡 Recommendation: Add ALL 20 verses to Golden Set v0.101")
        print("   This will:")
        print("   - Increase coverage of classical poetry")
        print("   - Add more poet diversity")
        print("   - Strengthen the test dataset")
        print()
        
        # Group by meter for addition
        by_meter = {}
        for r in results:
            meter = r['expected']
            if meter not in by_meter:
                by_meter[meter] = []
            by_meter[meter].append(r)
        
        print("Verses to add (grouped by meter):")
        for meter in sorted(by_meter.keys()):
            verses = by_meter[meter]
            print(f"\n  {meter} ({len(verses)} verses):")
            for v in verses:
                status = "✓" if v['correct'] else "✗"
                print(f"    {status} {v['verse_id']}: {v['poet']}")
    
    else:
        print(f"⚠️ Only {accuracy:.1%} accuracy on new verses.")
        print()
        
        # Add only the failed ones to expose weaknesses
        failures = [r for r in results if not r['correct']]
        if failures:
            print(f"💡 Recommendation: Add {len(failures)} FAILED verses to Golden Set")
            print("   These expose weaknesses in current patterns:")
            print()
            for r in failures:
                print(f"    • {r['verse_id']}: {r['poet']} - {r['expected']}")
            print()
            print("   After adding, implement better similarity algorithm")


if __name__ == "__main__":
    results, accuracy = test_generalization()
    recommend_additions(results, accuracy)
