# 🧪 مصادر بيانات الاختبار والمعايير
## Testing Datasets & Ground Truth Sources

---

## 📋 نظرة عامة

مصادر موثوقة لبيانات الاختبار والقياس، مع استراتيجية بناء مجموعة بيانات مرجعية (Ground Truth).

**تم الإنشاء:** November 8, 2025  
**الأهمية:** حرجة - أساس قياس دقة المحلل

---

## 🎯 متطلبات مجموعة البيانات

### المواصفات الأساسية (مُنظّمة على مراحل):

```yaml
Stage 1 (Weeks 1-2 - Dev Start):
  Target: 100–200 verses (hand-verified)
  Purpose: Golden set + early evaluation and TDD

Stage 2 (By Week 6):
  Target: 500–800 verses total
  Distribution goal: ~50 per meter across 10–16 meters (as coverage allows)
  Notes: Balance classical focus; add a small portion of modern samples

Stage 3 (Weeks 9-12 - Pre/Beta):
  Target: 800–1000+ verses
  Purpose: Finalize accuracy reports, confusion matrix, calibration

Extended Dataset (Post-MVP):
  Target: 2000+ verses
  Classical: 60%
  Modern: 30%
  Contemporary: 10%
  Edge Cases: 100+ verses

Per Verse (all stages):
  - Original text (with diacritics if available)
  - Normalized text
  - Meter name (Arabic + English)
  - Confidence level (high/medium/low)
  - Era (classical/modern)
  - Poet name (optional)
  - Notes on variations (زحافات)
```

---

## 📚 مصادر البيانات الموثوقة

### 🎯 **CONCRETE SOURCES - Week 1 Priority**

Use these specific sources for dataset collection:

### 1️⃣ ديوان العرب (Al-Diwan) ⭐ **PRIMARY SOURCE**

```yaml
Source: https://www.aldiwan.net/
Type: Classical & Modern Arabic Poetry
Coverage: 100,000+ poems
Quality: High - verified by editors
License: Public domain (classical), varies (modern)

Week 1 Action Plan:
  - Manually copy 20 معلقات verses for Golden Set
  - URLs to bookmark:
    - https://www.aldiwan.net/poem1.html (قفا نبك - امرؤ القيس)
    - https://www.aldiwan.net/poet1.html (ديوان المتنبي)
    - https://www.aldiwan.net/cat104.html (الشعر الجاهلي)
  - Expected yield: 50-100 verses (Week 1-2)

Advantages:
  ✅ Comprehensive classical collection
  ✅ Organized by poet and era
  ✅ Search by meter functionality
  ✅ Free access, no login required
  ✅ Clean Arabic text (copy-paste ready)

Disadvantages:
  ⚠️ No API - requires manual copy or web scraping
  ⚠️ Meter labels sometimes inconsistent (verify manually)
  ⚠️ Modern poetry copyright restrictions

Recommended Use:
  - Week 1: 20 verses for Golden Set (معلقات + المتنبي)
  - Week 2: 50-80 verses for training set
  - Week 3-5: Additional 100-200 verses for evaluation
  - Total target: 300-400 verified classical verses

Scraping Strategy (if needed Week 3+):
  - Use requests + BeautifulSoup (Python)
  - Respect robots.txt
  - Rate limit: 1 request per 3 seconds
  - Store locally in JSONL format
```

### 1.5️⃣ أدب - مكتبة الشعر العربي (Adab App) ⭐ **MOBILE SOURCE**

```yaml
Platform: iOS App Store / Google Play
App Name: "أدب - مكتبة الشعر العربي"
Developer: Integrated Technology Group
Coverage: 50,000+ poems from 1,000+ poets
Quality: Very High - curated by Arabic literature experts
License: Free with ads, premium subscription available

Week 1 Action Plan:
  - Download app on iPhone/Android
  - Browse classical poets (الشعر الجاهلي، العباسي، الأموي)
  - Manually copy 10-20 verses to Golden Set
  - Cross-verify meter labels with Al-Diwan

Advantages:
  ✅ Mobile-friendly interface
  ✅ Meter labels included for most poems
  ✅ Audio recitations (helps with pronunciation verification)
  ✅ Save/bookmark feature
  ✅ Search by meter, poet, era

Disadvantages:
  ⚠️ No bulk export (manual copy required)
  ⚠️ Some poems require premium subscription
  ⚠️ No API access

Recommended Use:
  - Week 1: Quick access to verified classical poems
  - Cross-reference meter labels with other sources
  - Use audio to verify pronunciation for ambiguous cases
  - Supplement Al-Diwan collection

Data Collection Workflow:
  1. Search by meter (e.g., "الطويل")
  2. Filter by classical era
  3. Select well-known poets (امرؤ القيس، المتنبي، أبو تمام)
  4. Copy text to Notes app
  5. Paste into dataset JSONL file
  6. Add metadata (poet, meter, source: "Adab App")
```

### 2️⃣ المكتبة الشاملة (Al-Maktaba Al-Shamela)

```yaml
Source: https://shamela.ws/
Type: Comprehensive Islamic & Arabic texts
Coverage: 10,000+ books including poetry collections
Quality: Very High - scholarly verified
License: Free for research

Advantages:
  ✅ Extremely reliable sources
  ✅ Original classical texts
  ✅ Downloadable formats
  ✅ Scholar-verified content

Disadvantages:
  ⚠️ Requires local installation
  ⚠️ Arabic interface only
  ⚠️ Large file sizes (20GB+)
  ⚠️ Needs manual extraction

Recommended Use:
  - Primary source for classical poetry
  - Verify authenticity of verses
  - Extract 400-500 high-quality verses
```

### 3️⃣ Poetry Foundation - Arabic Section

```yaml
Source: https://www.poetryfoundation.org/collections/148954/arabic-poetry
Type: Curated anthology of Arabic poetry (English translations + Arabic text)
Coverage: 200+ carefully selected poems
Quality: Excellent - scholarly curated, peer-reviewed
License: Educational use permitted, check specific poem rights

Week 2-3 Action Plan:
  - Browse curated collections
  - Focus on classical era (pre-1900)
  - Download bilingual versions
  - Extract Arabic text for dataset

Advantages:
  ✅ High-quality scholarly curation
  ✅ Historical context provided
  ✅ Trusted source for authenticity
  ✅ Both Arabic and English available
  ✅ Well-formatted, clean text

Disadvantages:
  ⚠️ Limited coverage (200+ poems only)
  ⚠️ Focus on "greatest hits" (may miss meter diversity)
  ⚠️ Some modernist free verse (skip for MVP)
  ⚠️ Copyright varies by poem

Recommended Use:
  - Week 2-3: Supplement Golden Set with highly verified verses
  - Use for final evaluation set (30-50 verses)
  - Cross-reference when ambiguous meter labels from other sources
  - Expected yield: 30-50 classical verses

Quality Assurance:
  - All poems are academically verified
  - Use as "gold standard" for disputed meter classifications
  - Excellent for edge cases and rare meters
```

### 4️⃣ Academic Datasets (Licensed)

```yaml
Sources:
  1. Arabic Poetry Corpus (University of Leeds)
     - URL: Contact via research.leeds.ac.uk
     - Coverage: 2,000+ classical poems with prosodic annotations
     - License: Research license required (free for academic use)
     - Quality: Excellent - PhD-level annotations
  
  2. CAMeL Lab Resources (NYU Abu Dhabi)
     - URL: https://camel.abudhabi.nyu.edu/resources/
     - Coverage: Various Arabic NLP datasets (may include poetry)
     - License: Research license, cite properly
     - Quality: Top-tier academic standard
  
  3. Linguistic Data Consortium (LDC)
     - URL: https://catalog.ldc.upenn.edu/
     - Search: "Arabic poetry" OR "Arabic prosody"
     - License: Paid subscription ($$$) - DEFER to Post-MVP
     - Quality: Gold standard for NLP research

Week 3-4 Action Plan:
  - Apply for Leeds Arabic Poetry Corpus (if available)
  - Check CAMeL Lab resources for poetry datasets
  - Defer LDC to Post-MVP (costly, not critical for MVP)

Advantages:
  ✅ Highest quality annotations (expert-verified)
  ✅ Prosodic metadata included (taqti3, zihafat)
  ✅ Peer-reviewed datasets
  ✅ Standard benchmark for comparison

Disadvantages:
  ⚠️ Licensing requirements (paperwork, approval process)
  ⚠️ Limited commercial use
  ⚠️ Some datasets are paid ($500+ for LDC)
  ⚠️ May take 2-4 weeks to obtain access

Recommended Use:
  - Post-MVP: Expand to 2,000+ verses
  - Use for final accuracy benchmarking
  - Publish research paper comparing BAHR to academic baselines
  - Expected yield: 500-2,000 verses (Post-MVP)

Licensing Strategy:
  - Week 3: Apply for free academic licenses (Leeds, CAMeL)
  - Document in README.md under "Data Sources"
  - Include proper citations in any publications
  - Defer paid datasets (LDC) until funding available
```

### 5️⃣ الموسوعة الشعرية (Poetry Encyclopedia)

```yaml
Source: http://www.adab.com/
Type: Organized poetry database
Coverage: 50,000+ poems
Quality: High - curated collection
License: Fair use for research

Advantages:
  ✅ Well-organized by meter
  ✅ Audio recordings available
  ✅ Biographical information
  ✅ User-friendly interface

Disadvantages:
  ⚠️ Limited API access
  ⚠️ Some ads and clutter
  ⚠️ Inconsistent formatting

Recommended Use:
  - Supplement classical verses
  - Modern poetry examples
  - Audio for future features
  - Expected yield: 100-200 verses
```

### 6️⃣ ديوان الشعر النبطي (Nabati Poetry) - **DEFERRED**

```yaml
Source: Various (specialized sites)
Type: Dialectal Gulf/Bedouin poetry
Coverage: Varies
Quality: Medium - community-driven
License: Varies

Advantages:
  ✅ Unique dialectal patterns
  ✅ Different meter variations
  ✅ Contemporary relevance

Disadvantages:
  ⚠️ Less standardized
  ⚠️ Harder to verify
  ⚠️ Different prosody rules

Recommended Use:
  - Phase 2+ (after classical mastery)
  - Edge case testing
  - 50-100 verses for variety
```

### 5️⃣ Academic Corpora

```yaml
Quranic Arabic Corpus:
  Source: http://corpus.quran.com/
  Use: Morphological analysis reference
  Quality: Extremely high
  Note: Not poetry, but excellent for Arabic NLP

KACST Arabic Corpus:
  Source: King Abdulaziz City for Science and Technology
  Size: 700+ million words
  Use: General Arabic NLP training
  Access: Research license required

CAMeL Lab Datasets:
  Source: NYU Abu Dhabi
  Focus: Modern Standard Arabic
  Quality: Very high
  Use: Benchmarking NLP tools
```

---

## 🗂️ Dataset Structure

### File Format (JSON):

```json
{
  "dataset_version": "1.0",
  "created_date": "2025-11-08",
  "total_verses": 800,
  "description": "BAHR Prosody Analysis Ground Truth Dataset",
  
  "verses": [
    {
      "id": "verse_001",
      "text_original": "قِفا نَبكِ مِن ذِكرى حَبيبٍ وَمَنزِلِ",
      "text_normalized": "قفا نبك من ذكرى حبيب ومنزل",
      "meter": {
        "name_ar": "الطويل",
        "name_en": "Al-Taweel",
        "pattern": "فَعُولُنْ مَفَاعِيلُنْ فَعُولُنْ مَفَاعِلُنْ",
        "confidence": "high"
      },
      "poet": {
        "name": "امرؤ القيس",
        "name_en": "Imru' al-Qays",
        "era": "pre-islamic"
      },
      "prosodic_analysis": {
        "taqti3": "قِ فا نَب كِ مِن ذِك رى حَ بي بِن وَ مَن زِ لي",
        "pattern_symbols": "- u - - | - u u - | - u - - | - u - -",
        "syllable_count": 16,
        "hemistichs": {
          "first": "قِفا نَبكِ مِن ذِكرى حَبيبٍ",
          "second": "وَمَنزِلٍ بِسِقطِ اللِوى"
        }
      },
      "metadata": {
        "source": "المعلقات",
        "verified_by": "manual",
        "verified_date": "2025-11-08",
        "variations": [],
        "notes": "Opening verse of Imru' al-Qays Mu'allaqa"
      },
      "labels": {
        "era": "classical",
        "difficulty": "medium",
        "clarity": "high",
        "educational_value": "high"
      }
    },
    {
      "id": "verse_002",
      "text_original": "أَلا في سَبيلِ المَجدِ ما أَنا فاعِلُ",
      "text_normalized": "الا في سبيل المجد ما انا فاعل",
      "meter": {
        "name_ar": "الكامل",
        "name_en": "Al-Kamil",
        "pattern": "مُتَفَاعِلُنْ مُتَفَاعِلُنْ مُتَفَاعِلُنْ",
        "confidence": "high"
      },
      "poet": {
        "name": "أبو فراس الحمداني",
        "name_en": "Abu Firas al-Hamdani",
        "era": "abbasid"
      },
      "prosodic_analysis": {
        "taqti3": "أَ لا في سَ بي لِل مَج دِ ما أَ نا فا عِ لو",
        "pattern_symbols": "u - u - - | u - u - - | u - u - -",
        "syllable_count": 15
      },
      "metadata": {
        "source": "ديوان أبي فراس",
        "verified_by": "manual",
        "verified_date": "2025-11-08"
      },
      "labels": {
        "era": "classical",
        "difficulty": "easy",
        "clarity": "very_high"
      }
    }
  ],
  
  "meters_distribution": {
    "الطويل": 50,
    "الكامل": 50,
    "البسيط": 50,
    "الوافر": 50,
    "الرجز": 50,
    "الرمل": 50,
    "الخفيف": 50,
    "المتقارب": 50,
    "السريع": 50,
    "المنسرح": 50,
    "الهزج": 50,
    "المجتث": 50,
    "المضارع": 50,
    "المديد": 50,
    "المقتضب": 50,
    "المحدث": 50
  }
}
```

### CSV Format (Alternative):

```csv
id,text_original,text_normalized,meter_ar,meter_en,poet,era,confidence,taqti3,notes
verse_001,"قِفا نَبكِ مِن ذِكرى حَبيبٍ وَمَنزِلِ","قفا نبك من ذكرى حبيب ومنزل","الطويل","Al-Taweel","امرؤ القيس","pre-islamic","high","قِ فا نَب كِ مِن ذِك رى حَ بي بِن","Opening of Mu'allaqa"
verse_002,"أَلا في سَبيلِ المَجدِ ما أَنا فاعِلُ","الا في سبيل المجد ما انا فاعل","الكامل","Al-Kamil","أبو فراس","abbasid","high","أَ لا في سَ بي لِل مَج دِ ما أَ نا فا عِ لو",""
```

---

## 📊 Data Collection Strategy

### Phase 1: Seed Dataset (Week 1-2)

```yaml
Goal: 100 verses for initial testing
Sources:
  - Al-Diwan: 60 verses (famous poems)
  - Manual curation: 40 verses
  
Selection Criteria:
  - Famous, easily verifiable verses
  - Clear meter (high confidence)
  - Diverse poets and eras
  - Educational value

Verification Process:
  1. Cross-reference with 2+ sources
  2. Manual prosodic analysis
  3. Expert review (if available)
  4. Document any ambiguities
```

### Phase 2: MVP Dataset (Week 3-6)

```yaml
Goal: 800 verses (50 per meter)
Timeline: 1 week for collection + 1 week for verification

Per Meter Requirements:
  Classical Examples: 35 verses
  Modern Examples: 10 verses
  Edge Cases: 5 verses
  
Process:
  Week 3: Collect from Al-Diwan (400 verses)
  Week 4: Collect from Al-Maktaba (300 verses)
  Week 5: Manual collection (100 verses)
  Week 6: Verification and labeling
```

### Phase 3: Extended Dataset (Week 7-12)

```yaml
Goal: 2000+ verses
Focus:
  - Increase modern poetry representation
  - Add dialectal variations
  - Include "difficult" cases
  - Expand edge case coverage

Continuous Improvement:
  - User contributions (verified)
  - Failed analyses → new test cases
  - Expert corrections
```

---

## 🧪 Test Sets Division

### Training vs Testing Split:

```yaml
Development Set (60%): 480 verses
  Use: Algorithm development
  Access: Frequent during coding
  
Validation Set (20%): 160 verses
  Use: Hyperparameter tuning
  Access: Weekly during development
  
Test Set (20%): 160 verses
  Use: Final accuracy measurement
  Access: ONLY at major milestones
  Note: NEVER use for development decisions
```

### Edge Cases Collection (100 verses):

```yaml
Ambiguous Meters:
  - Verses that could match 2+ meters
  - Different scholarly interpretations
  - Modern variations
  
Rare Meters:
  - المحدث (uncommon)
  - المقتضب (rare)
  - البحور المهملة
  
Problematic Cases:
  - Mixed dialects
  - Intentional meter breaks
  - Incomplete verses
  - Heavily modified meters (زحافات متعددة)
  
Non-Poetry:
  - Prose (should fail meter detection)
  - Free verse (should return low confidence)
  - Religious texts (Quran - not poetry)
  - Modern song lyrics
```

---

## 🔍 Quality Assurance Process

### Manual Verification Checklist:

```markdown
For Each Verse:
  
□ Text Accuracy
  - Verify against original source
  - Check diacritics (if available)
  - Confirm no typos or corruption
  
□ Meter Identification
  - Perform manual taqti3 (التقطيع)
  - Identify pattern
  - Match to classical meter
  - Note confidence level
  - Document any variations
  
□ Metadata Completeness
  - Poet name verified
  - Era/period confirmed
  - Source documented
  - Context noted (if relevant)
  
□ Edge Cases Flagged
  - Mark if ambiguous
  - Note alternative interpretations
  - Document unusual features
  
□ Cross-Reference
  - Check 2+ independent sources
  - Resolve conflicts
  - Document discrepancies
```

### Automated Validation:

```python
# scripts/validate_dataset.py
"""
Validate ground truth dataset quality
"""

import json
from typing import List, Dict

def validate_dataset(dataset_path: str) -> Dict[str, any]:
    """Comprehensive dataset validation"""
    
    with open(dataset_path) as f:
        data = json.load(f)
    
    errors = []
    warnings = []
    
    # Check structure
    required_fields = ['id', 'text_original', 'meter', 'metadata']
    for verse in data['verses']:
        for field in required_fields:
            if field not in verse:
                errors.append(f"Verse {verse.get('id', '?')} missing field: {field}")
    
    # Check meter distribution
    meter_counts = {}
    for verse in data['verses']:
        meter = verse['meter']['name_ar']
        meter_counts[meter] = meter_counts.get(meter, 0) + 1
    
    for meter, count in meter_counts.items():
        if count < 40:
            warnings.append(f"Meter '{meter}' has only {count} verses (target: 50)")
        elif count > 60:
            warnings.append(f"Meter '{meter}' has {count} verses (may be over-represented)")
    
    # Check for duplicates
    texts = [v['text_normalized'] for v in data['verses']]
    duplicates = [t for t in texts if texts.count(t) > 1]
    if duplicates:
        errors.append(f"Found {len(set(duplicates))} duplicate verses")
    
    # Check Arabic content
    for verse in data['verses']:
        text = verse['text_original']
        arabic_chars = sum(1 for c in text if '\u0600' <= c <= '\u06FF')
        if arabic_chars < len(text) * 0.8:
            warnings.append(f"Verse {verse['id']} has low Arabic content ratio")
    
    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings,
        'statistics': {
            'total_verses': len(data['verses']),
            'meters_covered': len(meter_counts),
            'meter_distribution': meter_counts
        }
    }

if __name__ == "__main__":
    result = validate_dataset('data/ground_truth.json')
    
    print(f"✅ Valid: {result['valid']}")
    print(f"📊 Total verses: {result['statistics']['total_verses']}")
    
    if result['errors']:
        print(f"\n❌ Errors ({len(result['errors'])}):")
        for error in result['errors']:
            print(f"  - {error}")
    
    if result['warnings']:
        print(f"\n⚠️  Warnings ({len(result['warnings'])}):")
        for warning in result['warnings']:
            print(f"  - {warning}")
```

---

## 📈 Benchmarking Strategy

### Accuracy Metrics:

```python
# tests/benchmarks/meter_detection_accuracy.py
"""
Calculate meter detection accuracy on test set
"""

from sklearn.metrics import accuracy_score, classification_report
import json

def calculate_accuracy(predictions_file: str, ground_truth_file: str):
    """Calculate comprehensive accuracy metrics"""
    
    with open(predictions_file) as f:
        predictions = json.load(f)
    
    with open(ground_truth_file) as f:
        ground_truth = json.load(f)
    
    y_true = [v['meter']['name_ar'] for v in ground_truth['verses']]
    y_pred = [p['detected_meter'] for p in predictions]
    
    # Overall accuracy
    accuracy = accuracy_score(y_true, y_pred)
    
    # Per-meter breakdown
    report = classification_report(
        y_true, y_pred,
        target_names=sorted(set(y_true)),
        output_dict=True
    )
    
    # Confidence calibration
    confidences = [p['confidence'] for p in predictions]
    correct = [1 if t == p else 0 for t, p in zip(y_true, y_pred)]
    
    # High confidence should → high accuracy
    high_conf_correct = [
        c for c, conf in zip(correct, confidences)
        if conf > 0.85
    ]
    
    return {
        'overall_accuracy': accuracy,
        'per_meter_accuracy': report,
        'high_confidence_accuracy': sum(high_conf_correct) / len(high_conf_correct) if high_conf_correct else 0,
        'avg_confidence': sum(confidences) / len(confidences)
    }
```

---

## 🎯 Success Criteria

```yaml
Week 6 (Initial Release):
  Accuracy on Test Set: > 70%
  Per-Meter Coverage: All 16 meters
  High Confidence Accuracy: > 85%
  False Positive Rate: < 10%

Week 12 (MVP Launch):
  Accuracy on Test Set: > 80%
  High Confidence Accuracy: > 90%
  Edge Case Handling: > 50%
  False Positive Rate: < 5%

6 Months Post-Launch:
  Accuracy on Test Set: > 90%
  All Metrics: Production-grade
  User Verification: Integrated
```

---

## 📝 Dataset Maintenance

```yaml
Weekly:
  - Add failed analyses to review queue
  - User reports → verification
  - Fix labeling errors

Monthly:
  - Expand test set with new verses
  - Re-evaluate accuracy metrics
  - Update difficulty ratings

Quarterly:
  - Major dataset version release
  - Comprehensive re-verification
  - Publication for research community
```

---

**Last Updated:** November 8, 2025  
**Next Review:** Week 3 (after initial data collection)  
**Dataset Location:** `data/ground_truth/`
