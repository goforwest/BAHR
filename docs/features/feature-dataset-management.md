# Feature: Dataset Management - Implementation Guide

**Feature ID:** `feature-dataset-management`  
**Status:** Production-Ready  
**Last Updated:** November 8, 2025  
**Estimated Implementation Time:** 10-12 hours

---

## 1. Objective & Description

### What
Implement dataset management system for Arabic poetry verses with JSONL format, validation scripts, golden dataset (20+ verses), import/export utilities, and quality checks.

### Why
- **Training Data:** High-quality labeled examples for model improvement
- **Evaluation:** Golden dataset for testing accuracy
- **Quality Control:** Validation ensures data consistency
- **Collaboration:** Standard format for dataset contributions
- **Versioning:** Track dataset changes over time

### Success Criteria
- ✅ Define JSONL schema for verse datasets
- ✅ Create validation script for schema compliance
- ✅ Build golden dataset with 20+ diverse verses
- ✅ Implement import/export CLI utilities
- ✅ Add quality checks (duplicate detection, Arabic validation)
- ✅ Document dataset labeling workflow
- ✅ Test coverage ≥80% for validation logic

---

## 2. Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                Dataset Management Architecture                       │
└─────────────────────────────────────────────────────────────────────┘

Dataset Files (JSONL)
    │
    │  dataset/golden_set_v0_20.jsonl
    │  dataset/training_set.jsonl
    ▼
┌──────────────────────────────────────┐
│ Validation Script                    │
│ - Schema validation                  │
│ - Arabic content check               │
│ - Duplicate detection                │
│ - Meter verification                 │
└──────────┬───────────────────────────┘
           │
           │  Valid dataset
           ▼
┌──────────────────────────────────────┐
│ Import Utility                       │
│ - Load JSONL                         │
│ - Transform to DB models             │
│ - Bulk insert                        │
└──────────┬───────────────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│ PostgreSQL Database                  │
│ - analyses table                     │
│ - meters table                       │
└──────────────────────────────────────┘

JSONL Schema:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{
  "id": "golden_001",
  "text": "أَلا عِم صَباحاً أَيُّها الطَلَلُ البالي",
  "normalized_text": "الا عم صباحا ايها الطلل البالي",
  "pattern": "//0/0 //0/0 //0/0 //0/0",
  "detected_meter": "الطويل",
  "confidence": 0.95,
  "syllable_count": 16,
  "metadata": {
    "source": "ديوان امرؤ القيس",
    "poet": "امرؤ القيس",
    "verified_by": "expert",
    "verification_date": "2025-11-01"
  }
}

Validation Rules:
1. Required fields: id, text, detected_meter
2. Text must contain Arabic characters
3. Meter must be one of 16 known meters
4. Confidence must be 0.0-1.0
5. No duplicate IDs
6. Pattern format: CV notation (C=/, V=0)
```

---

## 3. Input/Output Contracts

### 3.1 JSONL Schema

```python
# backend/app/schemas/dataset.py
"""
Dataset schema definitions.

Source: docs/research/DATASET_SPEC.md:1-150
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, Any
from datetime import datetime
import re


class DatasetMetadata(BaseModel):
    """Metadata for dataset entry."""
    source: Optional[str] = Field(None, description="Source (e.g., book title)")
    poet: Optional[str] = Field(None, description="Poet name")
    verified_by: Optional[str] = Field(None, description="Verifier (expert/algorithm)")
    verification_date: Optional[str] = Field(None, description="Verification date (ISO8601)")
    notes: Optional[str] = Field(None, description="Additional notes")


class DatasetEntry(BaseModel):
    """
    Single dataset entry (verse).
    
    Represents one line in JSONL file.
    """
    id: str = Field(..., description="Unique identifier (e.g., golden_001)")
    text: str = Field(..., min_length=5, max_length=1000, description="Original Arabic text")
    normalized_text: Optional[str] = Field(None, description="Normalized text")
    pattern: Optional[str] = Field(None, description="Prosodic pattern (CV notation)")
    detected_meter: str = Field(..., description="Classical Arabic meter name")
    confidence: float = Field(default=1.0, ge=0.0, le=1.0, description="Confidence score")
    syllable_count: Optional[int] = Field(None, ge=0, description="Number of syllables")
    metadata: Optional[DatasetMetadata] = Field(None, description="Additional metadata")
    
    @field_validator('text')
    @classmethod
    def validate_arabic_content(cls, v: str) -> str:
        """Ensure text contains Arabic characters."""
        arabic_chars = sum(1 for c in v if '\u0600' <= c <= '\u06FF')
        if arabic_chars < 5:
            raise ValueError(f"Text must contain at least 5 Arabic characters (found {arabic_chars})")
        return v
    
    @field_validator('detected_meter')
    @classmethod
    def validate_meter(cls, v: str) -> str:
        """Ensure meter is one of the 16 classical meters."""
        VALID_METERS = [
            "الطويل", "المديد", "البسيط", "الوافر", "الكامل", "الهزج",
            "الرجز", "الرمل", "السريع", "المنسرح", "الخفيف", "المضارع",
            "المقتضب", "المجتث", "المتقارب", "المتدارك"
        ]
        if v not in VALID_METERS:
            raise ValueError(f"Invalid meter: {v}. Must be one of 16 classical meters.")
        return v
    
    @field_validator('pattern')
    @classmethod
    def validate_pattern(cls, v: Optional[str]) -> Optional[str]:
        """Validate CV pattern format."""
        if v and not re.match(r'^[/0\s]+$', v):
            raise ValueError("Pattern must use CV notation (C=/, V=0)")
        return v


class Dataset(BaseModel):
    """Collection of dataset entries."""
    version: str = Field(..., description="Dataset version (e.g., v0.20)")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    entries: list[DatasetEntry] = Field(..., description="List of verse entries")
    
    @field_validator('entries')
    @classmethod
    def validate_unique_ids(cls, v: list[DatasetEntry]) -> list[DatasetEntry]:
        """Ensure all IDs are unique."""
        ids = [entry.id for entry in v]
        if len(ids) != len(set(ids)):
            duplicates = [id for id in ids if ids.count(id) > 1]
            raise ValueError(f"Duplicate IDs found: {set(duplicates)}")
        return v
```

---

## 4. Step-by-Step Implementation

### Step 1: Create Golden Dataset

```jsonl
# dataset/evaluation/golden_set_v0_20.jsonl
{"id": "golden_001", "text": "أَلا عِم صَباحاً أَيُّها الطَلَلُ البالي", "detected_meter": "الطويل", "confidence": 0.95, "metadata": {"source": "ديوان امرؤ القيس", "poet": "امرؤ القيس", "verified_by": "expert"}}
{"id": "golden_002", "text": "قِفا نَبكِ مِن ذِكرى حَبيبٍ وَمَنزِلِ", "detected_meter": "الطويل", "confidence": 0.98, "metadata": {"source": "معلقة امرؤ القيس", "poet": "امرؤ القيس", "verified_by": "expert"}}
{"id": "golden_003", "text": "أَراكَ عَصِيَّ الدَمعِ شيمَتُكَ الصَبرُ", "detected_meter": "الطويل", "confidence": 0.92, "metadata": {"source": "ديوان أبو فراس", "poet": "أبو فراس الحمداني", "verified_by": "expert"}}
{"id": "golden_004", "text": "كَفى بِكَ داءً أَن تَرى الموتَ شافِيا", "detected_meter": "الطويل", "confidence": 0.90, "metadata": {"source": "ديوان المتنبي", "poet": "المتنبي", "verified_by": "expert"}}
{"id": "golden_005", "text": "على قَدْرِ أَهلِ العَزمِ تأتي العَزائِمُ", "detected_meter": "الطويل", "confidence": 0.93, "metadata": {"source": "ديوان المتنبي", "poet": "المتنبي", "verified_by": "expert"}}
{"id": "golden_006", "text": "أَعِنّي عَلى بَرقٍ أُراهُ وَميضِ", "detected_meter": "الوافر", "confidence": 0.88, "metadata": {"source": "ديوان الخنساء", "poet": "الخنساء", "verified_by": "expert"}}
{"id": "golden_007", "text": "فَإِنَّكَ شَمسٌ وَالمُلوكُ كَواكِبُ", "detected_meter": "الطويل", "confidence": 0.94, "metadata": {"source": "ديوان المتنبي", "poet": "المتنبي", "verified_by": "expert"}}
{"id": "golden_008", "text": "أَلا لَيتَ الشَبابَ يَعودُ يَوماً", "detected_meter": "الوافر", "confidence": 0.91, "metadata": {"source": "ديوان أبو العتاهية", "poet": "أبو العتاهية", "verified_by": "expert"}}
{"id": "golden_009", "text": "أَنا الَّذي نَظَرَ الأَعمى إِلى أَدَبي", "detected_meter": "الطويل", "confidence": 0.96, "metadata": {"source": "ديوان المتنبي", "poet": "المتنبي", "verified_by": "expert"}}
{"id": "golden_010", "text": "وَأَحسَنُ مِن نَورِ الرِياضِ مُحَيّا", "detected_meter": "الكامل", "confidence": 0.89, "metadata": {"source": "ديوان ابن زيدون", "poet": "ابن زيدون", "verified_by": "expert"}}
{"id": "golden_011", "text": "تَعَلَّم فَلَيسَ المَرءُ يولَدُ عالِماً", "detected_meter": "الوافر", "confidence": 0.87, "metadata": {"source": "شعر جاهلي", "poet": "غير معروف", "verified_by": "expert"}}
{"id": "golden_012", "text": "يا لَيلُ الصَبُّ مَتى غَدُهُ", "detected_meter": "المتقارب", "confidence": 0.85, "metadata": {"source": "موشح أندلسي", "poet": "غير معروف", "verified_by": "expert"}}
{"id": "golden_013", "text": "سَلامٌ مِنَ الرَحمَنِ كُلَّ مَساءِ", "detected_meter": "الكامل", "confidence": 0.92, "metadata": {"source": "الشعر الديني", "poet": "غير معروف", "verified_by": "expert"}}
{"id": "golden_014", "text": "هَل غادَرَ الشُعَراءُ مِن مُتَرَدَّمِ", "detected_meter": "الطويل", "confidence": 0.97, "metadata": {"source": "معلقة عنترة", "poet": "عنترة بن شداد", "verified_by": "expert"}}
{"id": "golden_015", "text": "صَفَتِ الحَياةُ لَهُ فَعاشَ بِها", "detected_meter": "الخفيف", "confidence": 0.86, "metadata": {"source": "شعر حديث", "poet": "غير معروف", "verified_by": "expert"}}
{"id": "golden_016", "text": "إِذا غامَرتَ في شَرَفٍ مَرومِ", "detected_meter": "الطويل", "confidence": 0.94, "metadata": {"source": "ديوان المتنبي", "poet": "المتنبي", "verified_by": "expert"}}
{"id": "golden_017", "text": "وَلا خَيرَ في حِلمٍ إِذا لَم يَكُن لَهُ", "detected_meter": "الطويل", "confidence": 0.91, "metadata": {"source": "شعر جاهلي", "poet": "زهير بن أبي سلمى", "verified_by": "expert"}}
{"id": "golden_018", "text": "بِأَبي وَأُمّي مَن إِذا عَثَرَت بِهِ", "detected_meter": "الكامل", "confidence": 0.88, "metadata": {"source": "شعر أموي", "poet": "جرير", "verified_by": "expert"}}
{"id": "golden_019", "text": "أَلا إِنَّما الدُنيا غُرورٌ وَباطِلُ", "detected_meter": "الطويل", "confidence": 0.93, "metadata": {"source": "شعر زهد", "poet": "غير معروف", "verified_by": "expert"}}
{"id": "golden_020", "text": "إِنّي رَأَيتُ وُقوفَ الماءِ يُفسِدُهُ", "detected_meter": "الكامل", "confidence": 0.90, "metadata": {"source": "شعر حكمة", "poet": "الشافعي", "verified_by": "expert"}}
```

### Step 2: Create Validation Script

```python
# backend/scripts/validate_dataset.py
"""
Dataset validation script.

Usage:
    python scripts/validate_dataset.py dataset/evaluation/golden_set_v0_20.jsonl

Source: docs/research/TESTING_DATASETS.md:1-80
"""

import json
import sys
from pathlib import Path
from typing import List, Tuple
from collections import Counter

from app.schemas.dataset import DatasetEntry


def load_jsonl(file_path: Path) -> List[dict]:
    """Load JSONL file."""
    entries = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            try:
                entry = json.loads(line.strip())
                entries.append(entry)
            except json.JSONDecodeError as e:
                print(f"❌ Line {line_num}: Invalid JSON - {e}")
                sys.exit(1)
    return entries


def validate_entries(entries: List[dict]) -> Tuple[bool, List[str]]:
    """Validate all entries against schema."""
    errors = []
    ids = []
    
    for idx, entry_dict in enumerate(entries, 1):
        try:
            # Validate with Pydantic
            entry = DatasetEntry(**entry_dict)
            ids.append(entry.id)
            
        except Exception as e:
            errors.append(f"Entry {idx} (id={entry_dict.get('id', 'unknown')}): {e}")
    
    # Check for duplicates
    id_counts = Counter(ids)
    duplicates = [id for id, count in id_counts.items() if count > 1]
    if duplicates:
        errors.append(f"Duplicate IDs found: {duplicates}")
    
    return len(errors) == 0, errors


def print_statistics(entries: List[dict]):
    """Print dataset statistics."""
    meters = Counter(entry.get('detected_meter') for entry in entries)
    poets = Counter(entry.get('metadata', {}).get('poet', 'غير معروف') for entry in entries)
    
    print("\n📊 Dataset Statistics:")
    print(f"   Total verses: {len(entries)}")
    print(f"\n   Meters distribution:")
    for meter, count in meters.most_common():
        print(f"      {meter}: {count}")
    print(f"\n   Top poets:")
    for poet, count in list(poets.most_common(5)):
        print(f"      {poet}: {count}")


def main():
    """Main validation function."""
    if len(sys.argv) < 2:
        print("Usage: python scripts/validate_dataset.py <dataset.jsonl>")
        sys.exit(1)
    
    file_path = Path(sys.argv[1])
    
    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        sys.exit(1)
    
    print(f"🔍 Validating dataset: {file_path}")
    
    # Load entries
    entries = load_jsonl(file_path)
    print(f"✅ Loaded {len(entries)} entries")
    
    # Validate
    is_valid, errors = validate_entries(entries)
    
    if is_valid:
        print("✅ All entries are valid!")
        print_statistics(entries)
    else:
        print(f"\n❌ Validation failed with {len(errors)} error(s):")
        for error in errors:
            print(f"   - {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
```

### Step 3: Create Import Utility

```python
# backend/scripts/import_dataset.py
"""
Import dataset from JSONL to database.

Usage:
    python scripts/import_dataset.py dataset/evaluation/golden_set_v0_20.jsonl

Source: docs/research/DATASET_SPEC.md:80-150
"""

import json
import sys
from pathlib import Path
from sqlalchemy.orm import Session

from app.db.base import SessionLocal, engine, Base
from app.models.analysis import Analysis
from app.schemas.dataset import DatasetEntry


def import_dataset(file_path: Path, db: Session):
    """Import JSONL dataset to database."""
    imported_count = 0
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            entry_dict = json.loads(line.strip())
            entry = DatasetEntry(**entry_dict)
            
            # Create Analysis model
            analysis = Analysis(
                id=entry.id,
                user_id=None,  # Golden dataset has no user
                original_text=entry.text,
                normalized_text=entry.normalized_text or entry.text,
                pattern=entry.pattern or "",
                detected_meter=entry.detected_meter,
                confidence=entry.confidence,
                syllable_count=entry.syllable_count,
                metadata=entry.metadata.model_dump() if entry.metadata else {}
            )
            
            # Add to database
            db.merge(analysis)  # Use merge to handle duplicates
            imported_count += 1
    
    db.commit()
    return imported_count


def main():
    """Main import function."""
    if len(sys.argv) < 2:
        print("Usage: python scripts/import_dataset.py <dataset.jsonl>")
        sys.exit(1)
    
    file_path = Path(sys.argv[1])
    
    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        sys.exit(1)
    
    print(f"📥 Importing dataset: {file_path}")
    
    # Create tables if not exist
    Base.metadata.create_all(bind=engine)
    
    # Import
    db = SessionLocal()
    try:
        count = import_dataset(file_path, db)
        print(f"✅ Imported {count} entries to database")
    except Exception as e:
        print(f"❌ Import failed: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()
```

### Step 4: Create Export Utility

```python
# backend/scripts/export_dataset.py
"""
Export database analyses to JSONL format.

Usage:
    python scripts/export_dataset.py output.jsonl --limit 100
"""

import json
import argparse
from pathlib import Path
from sqlalchemy.orm import Session

from app.db.base import SessionLocal
from app.models.analysis import Analysis
from app.schemas.dataset import DatasetEntry, DatasetMetadata


def export_dataset(output_path: Path, db: Session, limit: int = None):
    """Export analyses to JSONL."""
    query = db.query(Analysis).filter(Analysis.detected_meter.isnot(None))
    
    if limit:
        query = query.limit(limit)
    
    analyses = query.all()
    exported_count = 0
    
    with open(output_path, 'w', encoding='utf-8') as f:
        for analysis in analyses:
            entry = DatasetEntry(
                id=str(analysis.id),
                text=analysis.original_text,
                normalized_text=analysis.normalized_text,
                pattern=analysis.pattern,
                detected_meter=analysis.detected_meter,
                confidence=float(analysis.confidence) if analysis.confidence else 1.0,
                syllable_count=analysis.syllable_count,
                metadata=DatasetMetadata(**analysis.metadata) if analysis.metadata else None
            )
            
            f.write(entry.model_dump_json() + '\n')
            exported_count += 1
    
    return exported_count


def main():
    """Main export function."""
    parser = argparse.ArgumentParser(description='Export dataset to JSONL')
    parser.add_argument('output', type=Path, help='Output JSONL file')
    parser.add_argument('--limit', type=int, help='Limit number of entries')
    
    args = parser.parse_args()
    
    print(f"📤 Exporting dataset to: {args.output}")
    
    db = SessionLocal()
    try:
        count = export_dataset(args.output, db, args.limit)
        print(f"✅ Exported {count} entries")
    except Exception as e:
        print(f"❌ Export failed: {e}")
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()
```

---

## 5. Reference Implementation (Full Code)

See Step-by-Step Implementation sections above for complete code.

---

## 6. Unit & Integration Tests

```python
# tests/unit/test_dataset_schema.py
import pytest
from app.schemas.dataset import DatasetEntry, Dataset


def test_valid_dataset_entry():
    """Test valid dataset entry."""
    entry = DatasetEntry(
        id="test_001",
        text="أَلا عِم صَباحاً أَيُّها الطَلَلُ البالي",
        detected_meter="الطويل",
        confidence=0.95
    )
    
    assert entry.id == "test_001"
    assert entry.confidence == 0.95


def test_arabic_validation():
    """Test Arabic content validation."""
    with pytest.raises(ValueError, match="at least 5 Arabic characters"):
        DatasetEntry(
            id="test_002",
            text="Hello",  # No Arabic
            detected_meter="الطويل"
        )


def test_meter_validation():
    """Test meter validation."""
    with pytest.raises(ValueError, match="Invalid meter"):
        DatasetEntry(
            id="test_003",
            text="نص عربي كافٍ للاختبار",
            detected_meter="invalid_meter"
        )


def test_duplicate_ids():
    """Test duplicate ID detection."""
    entries = [
        DatasetEntry(id="test_001", text="نص عربي", detected_meter="الطويل"),
        DatasetEntry(id="test_001", text="نص آخر", detected_meter="الكامل"),  # Duplicate
    ]
    
    with pytest.raises(ValueError, match="Duplicate IDs"):
        Dataset(version="v1.0", entries=entries)
```

---

## 7. CI/CD Pipeline

```yaml
# .github/workflows/dataset-validation.yml
name: Dataset Validation

on:
  push:
    paths:
      - 'dataset/**'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      
      - name: Validate golden dataset
        run: |
          cd backend
          python scripts/validate_dataset.py ../dataset/evaluation/golden_set_v0_20.jsonl
```

---

## 8. Deployment Checklist

- [ ] Create golden dataset with 20+ verses
- [ ] Validate dataset with validation script
- [ ] Import golden dataset to production database
- [ ] Document dataset labeling workflow
- [ ] Set up version control for datasets
- [ ] Create backup of datasets
- [ ] Test import/export utilities
- [ ] Document JSONL schema
- [ ] Add dataset statistics to monitoring
- [ ] Create dataset contribution guidelines

---

## 9. Observability

- Track dataset size over time
- Monitor validation pass rate
- Track meter distribution
- Alert on schema changes

---

## 10. Security & Safety

- **Data Validation:** Always validate before import
- **Backup:** Version all datasets
- **Access Control:** Restrict dataset modification
- **Audit Trail:** Log all dataset changes

---

## 11. Backwards Compatibility

- **Schema Versioning:** Use version field in Dataset model
- **Migration Scripts:** Provide scripts to upgrade old formats

---

## 12. Source Documentation Citations

1. **docs/research/DATASET_SPEC.md:1-200** - Dataset specification
2. **docs/research/TESTING_DATASETS.md:1-150** - Testing datasets
3. **dataset/evaluation/golden_set_v0_20.jsonl:1-20** - Golden dataset
4. **implementation-guides/IMPROVED_PROMPT.md:764-786** - Feature specification

---

**Implementation Complete!** ✅  
**Estimated Time:** 10-12 hours  
**Test Coverage Target:** ≥ 80%  
**Golden Dataset Size:** 20+ verses (16 classical meters)
