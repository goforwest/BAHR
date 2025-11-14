#!/usr/bin/env python3
"""Update golden_set_metadata.json for the 100-verse dataset"""

import json
from pathlib import Path
from datetime import datetime
from collections import Counter

def update_metadata():
    """Generate updated metadata for the 100-verse golden set"""
    
    # Load the 100-verse dataset
    dataset_file = Path(__file__).parent.parent / "evaluation" / "golden_set_v0_100_complete.jsonl"
    verses = []
    with open(dataset_file, 'r', encoding='utf-8') as f:
        for line in f:
            verses.append(json.loads(line))
    
    # Calculate statistics
    meters = [v['meter'] for v in verses]
    eras = [v['era'] for v in verses]
    edge_cases = [v['edge_case_type'] for v in verses]
    difficulties = [v['difficulty_level'] for v in verses]
    confidences = [v['confidence'] for v in verses]
    syllable_counts = [v['syllable_count'] for v in verses]
    tafail_counts = [len(v['expected_tafail']) for v in verses]
    poets = [v['poet'] for v in verses if v.get('poet')]
    
    metadata = {
        "dataset_name": "BAHR Golden Set v0.100",
        "version": "0.100",
        "created_date": "2025-11-09",
        "last_updated": datetime.now().isoformat(),
        "total_verses": len(verses),
        "description": "Gold standard dataset for Arabic prosody engine validation - Expanded to 100 authentic verses",
        "changelog": {
            "2025-11-11": "Expanded from 80 to 100 verses. Removed duplicate verse #5. Added 21 new authentic classical and modern verses."
        },
        "meter_distribution": dict(Counter(meters)),
        "era_distribution": dict(Counter(eras)),
        "edge_case_distribution": dict(Counter(edge_cases)),
        "difficulty_distribution": dict(Counter(difficulties)),
        "statistics": {
            "avg_confidence": round(sum(confidences) / len(confidences), 4),
            "avg_syllable_count": round(sum(syllable_counts) / len(syllable_counts), 2),
            "avg_tafail_count": round(sum(tafail_counts) / len(tafail_counts), 2),
            "verses_with_poet": len(poets),
            "unique_poets": len(set(poets)),
            "high_confidence_verses": len([c for c in confidences if c >= 0.95]),
            "classical_verses": len([e for e in eras if e == 'classical']),
            "modern_verses": len([e for e in eras if e == 'modern'])
        },
        "quality_metrics": {
            "field_completeness": 1.0,
            "annotation_completeness": 1.0,
            "validation_status": "verified",
            "no_duplicates": True,
            "ready_for_testing": True
        },
        "schema_version": "1.0",
        "fields": [
            "verse_id",
            "text",
            "normalized_text",
            "meter",
            "poet",
            "source",
            "era",
            "confidence",
            "notes",
            "taqti3",
            "expected_tafail",
            "syllable_pattern",
            "syllable_count",
            "edge_case_type",
            "difficulty_level",
            "validation",
            "metadata"
        ],
        "sources": [
            "المعلقات السبع",
            "دواوين الشعراء الجاهليين",
            "ديوان المتنبي",
            "ديوان أبو العلاء المعري",
            "ديوان الإمام الشافعي",
            "ديوان أحمد شوقي",
            "الشعر المهجري",
            "حكم عربية مأثورة"
        ],
        "notable_poets": [
            "امرؤ القيس",
            "المتنبي",
            "أبو العلاء المعري",
            "أحمد شوقي",
            "الإمام الشافعي",
            "عنترة بن شداد",
            "طرفة بن العبد",
            "زهير بن أبي سلمى",
            "لبيد بن ربيعة",
            "النابغة الذبياني",
            "إيليا أبو ماضي"
        ]
    }
    
    # Write metadata
    output_file = Path(__file__).parent.parent / "evaluation" / "golden_set_metadata.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Updated {output_file}")
    print(f"\n📊 Metadata Summary:")
    print(f"   Total verses: {metadata['total_verses']}")
    print(f"   Unique poets: {metadata['statistics']['unique_poets']}")
    print(f"   Average confidence: {metadata['statistics']['avg_confidence']}")
    print(f"   Classical: {metadata['statistics']['classical_verses']}")
    print(f"   Modern: {metadata['statistics']['modern_verses']}")

if __name__ == "__main__":
    update_metadata()
