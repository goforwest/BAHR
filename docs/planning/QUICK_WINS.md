# ✅ Quick Wins Checklist - Week 1-2
## High-Impact Low-Effort Tasks to Accelerate Development

---

## 🎯 Purpose

This document lists **quick wins** - small tasks that provide disproportionate value early in the project. Complete these in Week 1-2 to:
- Unblock parallel development
- Reduce debugging time later
- Build momentum
- Enable faster iteration

**Time Investment:** 2-4 hours total  
**Return:** Saves 10-20 hours in Weeks 3-6

---

## 📋 Week 1 Quick Wins

### 1️⃣ Create 20-Verse "Golden Set" ⭐⭐⭐

**Time:** 60 minutes  
**Value:** Unblocks testing immediately

```yaml
Task:
  - Select 20 perfect classical verses (varied meters)
  - Manually label with 100% accuracy
  - Include taqti3 patterns
  - Document source and poet
  - Save as tests/fixtures/golden_set.jsonl

Why This Matters:
  - Can start writing tests before full dataset ready
  - Serves as reference for ambiguous cases
  - Quality benchmark for automated labeling

Meters to Include:
  - الطويل (3 verses)
  - الكامل (3 verses)
  - الوافر (2 verses)
  - البسيط (2 verses)
  - الرجز (2 verses)
  - المتقارب (2 verses)
  - الرمل (2 verses)
  - الخفيف (2 verses)
  - السريع (1 verse)
  - المنسرح (1 verse)
```

**Acceptance Criteria:**
```python
# tests/test_golden_set.py
def test_golden_set_coverage():
    verses = load_golden_set()
    assert len(verses) == 20
    assert len(set(v['meter'] for v in verses)) >= 10  # 10+ different meters
    assert all(v['taqti3'] for v in verses)  # All have taqti3
    assert all(v['source'] for v in verses)  # All documented
```

---

### 2️⃣ Build Mock API Endpoint ⭐⭐⭐

**Time:** 45 minutes  
**Value:** Frontend development can start immediately

```python
# app/api/v1/endpoints/analyze.py (temporary mock)

from fastapi import APIRouter
from app.schemas.analysis import AnalysisRequest, AnalysisResponse
import random

router = APIRouter()

# Temporary mock data
MOCK_RESPONSES = {
    "الطويل": {
        "taqti3": "فَعُولُنْ مَفَاعِيلُنْ فَعُولُنْ مَفَاعِلُنْ",
        "pattern": "- u - - | - u u - | - u - - | - u -",
        "confidence": 0.95
    },
    "الكامل": {
        "taqti3": "مُتَفَاعِلُنْ مُتَفَاعِلُنْ مُتَفَاعِلُنْ",
        "pattern": "- u - - | - u - - | - u - -",
        "confidence": 0.92
    }
}

@router.post("/analyze/", response_model=AnalysisResponse)
async def analyze_poetry_mock(request: AnalysisRequest):
    """
    🚧 TEMPORARY MOCK ENDPOINT
    Returns fake analysis results for frontend testing
    DELETE when real prosody engine is ready (Week 5)
    """
    # Random meter selection
    detected_meter = random.choice(list(MOCK_RESPONSES.keys()))
    mock_data = MOCK_RESPONSES[detected_meter]
    
    return AnalysisResponse(
        success=True,
        data={
            "original_text": request.text,
            "normalized_text": request.text.replace('أ', 'ا'),
            "prosodic_analysis": {
                "taqti3": mock_data["taqti3"],
                "pattern": mock_data["pattern"],
                "syllable_count": 14
            },
            "meter_detection": {
                "detected_meter": detected_meter,
                "confidence": mock_data["confidence"],
                "alternative_meters": []
            },
            "quality_score": 0.88,
            "suggestions": ["تحليل تجريبي - قيد التطوير"]
        },
        processing_time_ms=50,
        request_id="mock-" + str(random.randint(1000, 9999))
    )
```

**Why This Matters:**
- Frontend dev doesn't wait for Week 5 backend
- Can test UI flows, loading states, error handling
- Identifies integration issues early

**Cleanup:** Delete mock in Week 5 when real engine ready

---

### 3️⃣ Write 100+ Normalization Test Cases ⭐⭐

**Time:** 90 minutes  
**Value:** Saves hours of debugging

```python
# tests/test_prosody/test_normalizer_comprehensive.py

import pytest
from app.core.prosody.normalizer import ArabicNormalizer

normalizer = ArabicNormalizer()

# Test suite: 100+ cases covering all edge cases
NORMALIZATION_CASES = [
    # Diacritics removal (10 cases)
    ("قِفَا نَبْكِ", "قفا نبك"),
    ("مِنْ ذِكْرَى حَبِيبٍ", "من ذكرى حبيب"),
    ("وَمَنْزِلِ بِسِقْطِ اللِّوَى", "ومنزل بسقط اللوى"),
    # ... 7 more
    
    # Hamza normalization (8 cases)
    ("أَلَا", "الا"),
    ("إِنَّ", "انّ"),
    ("آمَنَ", "امن"),
    ("أُمَّة", "امة"),
    ("إِيمَان", "ايمان"),
    # ... 3 more
    
    # Ta Marbuta (5 cases)
    ("قَصِيدَةٌ", "قصيده"),
    ("مَدْرَسَةً", "مدرسه"),
    # ... 3 more
    
    # Mixed Arabic/English (8 cases)
    ("Poetry الشعر", "poetry الشعر"),
    ("AI الذكاء الاصطناعي", "ai الذكاء الاصطناعي"),
    # ... 6 more
    
    # Special characters (10 cases)
    ("الله، رسول الله", "الله رسول الله"),
    ("هل؟ نعم!", "هل نعم"),
    ("'قال' \"الشاعر\"", "قال الشاعر"),
    # ... 7 more
    
    # Numbers (6 cases)
    ("القصيدة ١٢٣", "القصيدة 123"),
    ("الدرس الأول", "الدرس الاول"),
    # ... 4 more
    
    # Shadda decomposition (6 cases)
    ("الشَّعر", "الششعر"),  # Before normalization
    ("مُحَمَّد", "محممد"),
    # ... 4 more
    
    # Tanwīn pause (8 cases)
    ("كتاباً#", "كتابا"),  # Nasb becomes alef
    ("علمٌ#", "علم"),      # Dham/Kasr drops
    # ... 6 more
    
    # Edge cases (10 cases)
    ("", ""),  # Empty
    ("   ", ""),  # Only spaces
    ("a" * 10000, "a" * 10000),  # Very long
    # ... 7 more
]

@pytest.mark.parametrize("input_text,expected", NORMALIZATION_CASES)
def test_normalization(input_text, expected):
    result = normalizer.normalize(input_text)
    assert result == expected, f"Failed for: {input_text}"
```

**Why This Matters:**
- Catches 80% of bugs before they happen
- Documents expected behavior
- Enables confident refactoring

**Time Saved:** 5-10 hours of debugging in Weeks 3-5

---

## 📋 Week 2 Quick Wins

### 4️⃣ Setup Basic Monitoring Dashboard ⭐⭐

**Time:** 30 minutes  
**Value:** Catch issues early

```yaml
# monitoring/prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'bahr-backend'
    static_configs:
      - targets: ['localhost:8000']

# Simple Grafana dashboard with 3 panels:
# 1. Request rate
# 2. Error rate  
# 3. Response time P95
```

---

### 5️⃣ Create .env.example Template ⭐⭐

**Time:** 15 minutes  
**Value:** Prevents configuration errors

```bash
# .env.example
# Copy to .env and fill in values

# Application
PROJECT_NAME=BAHR Poetry Analysis
DEBUG=True
SECRET_KEY=generate-with-secrets-token-urlsafe-32

# Database
DATABASE_URL=postgresql://bahr:password@localhost:5432/bahr_dev

# Redis
REDIS_URL=redis://localhost:6379/0

# API
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_PERIOD=3600

# CORS
ALLOWED_ORIGINS=http://localhost:3000

# Optional
SENTRY_DSN=
LOG_LEVEL=INFO
```

---

### 6️⃣ Write Database Seeding Script ⭐⭐⭐

**Time:** 45 minutes  
**Value:** Consistent test data

```python
# scripts/seed_db.py
"""
Seed database with 16 classical meters + examples
Run: python scripts/seed_db.py
"""

from app.db.session import SessionLocal
from app.models.meter import Meter

METERS_DATA = [
    {
        "name": "الطويل",
        "english_name": "At-Taweel",
        "base_pattern": "فعولن مفاعيلن فعولن مفاعيلن",
        "example_verse": "قفا نبك من ذكرى حبيب ومنزل",
        "difficulty_score": 2.0
    },
    # ... 15 more
]

def seed_meters():
    db = SessionLocal()
    try:
        for meter_data in METERS_DATA:
            meter = Meter(**meter_data)
            db.add(meter)
        db.commit()
        print(f"✅ Seeded {len(METERS_DATA)} meters")
    finally:
        db.close()

if __name__ == "__main__":
    seed_meters()
```

---

### 7️⃣ Setup Pre-commit Hooks ⭐

**Time:** 20 minutes  
**Value:** Catch errors before commit

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
        args: ['--maxkb=1000']
  
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        language_version: python3.11
  
  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        args: ['--max-line-length=100']
```

```bash
# Install
pip install pre-commit
pre-commit install

# Run manually
pre-commit run --all-files
```

---

### 8️⃣ Create API Documentation Stubs ⭐

**Time:** 30 minutes  
**Value:** Clarifies API contract early

```python
# app/api/v1/endpoints/analyze.py

@router.post(
    "/analyze/",
    response_model=AnalysisResponse,
    summary="تحليل نص شعري",
    description="""
    يحلل نصاً شعرياً عربياً ويحدد البحر الشعري.
    
    **الاستخدام:**
    - أرسل نصاً عربياً (بيت أو أكثر)
    - اختر وضع التحليل (accurate/fast)
    - احصل على البحر والتقطيع والجودة
    
    **حدود:**
    - النص: 10-1000 كلمة
    - معدل الطلبات: 100 طلب/ساعة
    
    **أمثلة:**
    ```json
    {
      "text": "قفا نبك من ذكرى حبيب ومنزل",
      "options": {"analysis_mode": "accurate"}
    }
    ```
    """,
    responses={
        200: {"description": "تحليل ناجح"},
        422: {"description": "نص غير صالح"},
        429: {"description": "تجاوز حد الطلبات"}
    }
)
async def analyze_poetry(request: AnalysisRequest):
    pass
```

---

## 📊 Impact Summary

| Quick Win | Time | Impact | Week |
|-----------|------|--------|------|
| Golden Set (20 verses) | 60 min | ⭐⭐⭐ | 1 |
| Mock API Endpoint | 45 min | ⭐⭐⭐ | 1 |
| 100+ Normalization Tests | 90 min | ⭐⭐ | 1 |
| Monitoring Dashboard | 30 min | ⭐⭐ | 2 |
| .env.example Template | 15 min | ⭐⭐ | 2 |
| Database Seeding Script | 45 min | ⭐⭐⭐ | 2 |
| Pre-commit Hooks | 20 min | ⭐ | 2 |
| API Docs Stubs | 30 min | ⭐ | 2 |
| **Total** | **5.5 hours** | **High** | **1-2** |

---

## ✅ Completion Checklist

```yaml
Week 1:
  □ Golden set created (20 verses, varied meters)
  □ Mock API endpoint working
  □ Normalization tests written (100+ cases)
  □ Frontend can call mock API successfully

Week 2:
  □ Monitoring dashboard accessible
  □ .env.example committed
  □ Database seeding script tested
  □ Pre-commit hooks installed
  □ API documentation visible in /docs
```

---

## 🎯 Success Metrics

**You've succeeded when:**
- Frontend dev starts Week 2 (not Week 6)
- Normalization bugs caught in tests (not production)
- Database setup takes 5 minutes (not 2 hours)
- Monitoring shows issues before users report them

**ROI:** 5 hours invested → 15-20 hours saved = **3-4x return**

---

**Last Updated:** November 8, 2025  
**Review After:** Week 2 completion
