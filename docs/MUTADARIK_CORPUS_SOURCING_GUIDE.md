# المتدارك Corpus Sourcing Guide

**Version:** 1.0
**Date:** 2025-11-12
**Purpose:** Practical guide for sourcing authenticated المتدارك verses
**Target:** 15 verified verses for golden set inclusion

---

## 📋 Executive Summary

**Objective:** Source 15 authenticated المتدارك verses to achieve 100% test coverage across all 20 Arabic meters.

**Distribution Target:**
- **Classical sources:** 5 verses (33%)
- **Modern poetry:** 8 verses (53%)
- **Synthetic/validated:** 2 verses (13%)

**Quality Requirements:**
- ✅ Expert verification (2+ prosodists)
- ✅ Source citation with page numbers
- ✅ Passes automated validation (mutadarik_validator.py)
- ✅ Inter-annotator agreement κ ≥ 0.85
- ✅ Confidence score ≥ 0.85

---

## 🎯 Target Distribution

### By Difficulty

| Level | Count | Percentage | Characteristics |
|-------|-------|------------|-----------------|
| Easy | 3 | 20% | Canonical form, no ziḥāfāt |
| Medium | 6 | 40% | 1-2 ziḥāfāt, clear المتدارك pattern |
| Hard | 6 | 40% | 3+ ziḥāfāt, boundary cases with المتقارب/الرجز |

### By Variant

| Variant | Count | Pattern | Description |
|---------|-------|---------|-------------|
| صحيح (canonical) | 5 | فاعلن×4 | Base form, no transformations |
| محذوف (maḥdhūf) | 5 | ...فاع (final) | With حذف in final position |
| مقطوع (maqṭūʿ) | 3 | ...فاعل (final) | With قصر in final position |
| With khabn | 2 | فعلن variants | Heavy خبن usage |

### By Era

| Era | Count | Time Period | Notes |
|-----|-------|-------------|-------|
| Classical | 5 | Pre-1900 | Authenticated by classical prosodists |
| Modern | 8 | 1900-present | Contemporary poets, free verse |
| Synthetic | 2 | 2025 | Composed for edge case testing |

---

## 📚 Source 1: Classical Poetry Collections

### 1.1 الموشحات الأندلسية (Andalusian Muwashshaḥāt)

**Why this source:**
- Andalusian poetry experimented with rare meters
- المتدارك appears in موشحات due to musical requirements
- Well-documented and authenticated

**Access:**
- **المكتبة الشاملة** (Shamela): https://shamela.ws/
- Search: "موشح" + "المتدارك"
- Alternate search: "الخبب" (alternative name for المتدارك)

**Recommended Collections:**
1. **جيش التوشيح** by لسان الدين بن الخطيب
   - Shamela Book ID: 11638
   - Contains prosodic annotations

2. **دار الطراز في عمل الموشحات** by ابن سناء الملك
   - Shamela Book ID: 39897
   - Includes meter analysis

**Search Protocol:**
```
1. Open Shamela advanced search
2. Search term: "المتدارك" OR "الخبب"
3. Filter: كتب الأدب → الشعر
4. Review results for موشحات
5. Extract verses with proper source citation
6. Verify with classical prosody references
```

**Expected Yield:** 2-3 authenticated verses

**Validation Steps:**
1. Cross-reference with printed editions (if available)
2. Check prosodic analysis in original source
3. Verify meter attribution in multiple references
4. Run through mutadarik_validator.py
5. If validation fails, REJECT (high false positive rate in classical sources)

---

### 1.2 المفضليات (al-Mufaḍḍalīyāt)

**Why this source:**
- Contains some disputed المتدارك attributions
- Well-studied by modern prosodists
- Multiple scholarly editions with annotations

**Access:**
- **al-Warraq**: https://www.alwaraq.net/
- **Dīwān al-ʿArab**: https://www.diwanalarab.com/
- Physical copies with prosodic analysis preferred

**Caveat:** Some verses attributed to المتدارك by later scholars may actually be other meters. MUST verify independently.

**Search Protocol:**
```
1. Access al-Warraq digital library
2. Browse: المفضليات للمفضل الضبي
3. Look for prosodic annotations or commentaries
4. Search keyword: "متدارك"
5. Extract candidate verses
6. Cross-check with modern prosodic analyses:
   - موسيقى الشعر (إبراهيم أنيس, 1952)
   - في البنية الإيقاعية للشعر العربي (كمال أبو ديب, 1974)
```

**Expected Yield:** 1-2 verified verses (after rejecting disputed cases)

**Validation Steps:**
1. Find 2+ modern scholarly sources confirming المتدارك attribution
2. Manual تقطيع by expert prosodist
3. Compare with validator output
4. Require 100% agreement between sources

---

### 1.3 Classical Prosody Textbooks

**Target Sources:**

1. **الكافي في العروض والقوافي** (al-Kāfī) - التبريزي
   - Best source for المتدارك examples
   - Includes explicit meter breakdown
   - Shamela Book ID: 26347

2. **القسطاس في علم العروض** - الزمخشري
   - Brief المتدارك section
   - Reliable but limited examples

3. **ميزان الذهب في صناعة شعر العرب** - السيوطي
   - Contains المتدارك examples with scansion
   - Cross-referenced with multiple classical sources

**Extraction Protocol:**
```
1. Navigate to المتدارك chapter/section
2. Extract example verses (usually 1-3 per book)
3. Copy full taqṭīʿ (prosodic scansion) if provided
4. Record page number and edition details
5. Verify example hasn't been duplicated across books
```

**Expected Yield:** 2-3 verses total across all textbooks

---

## 📖 Source 2: Modern Poetry (1900-Present)

### 2.1 بدر شاكر السياب (Badr Shakir al-Sayyab)

**Why this poet:**
- Pioneer of free verse (شعر التفعيلة)
- Explicitly used المتدارك in major works
- Well-documented and analyzed

**Key Collections:**
1. **أنشودة المطر** (Rain Song)
   - Contains multiple المتدارك poems
   - Published editions with prosodic analysis

2. **المعبد الغريق** (The Drowned Temple)
   - Experimental meters including المتدارك

**Access:**
- Physical copies recommended (most accurate diacritics)
- Digital: مكتبة نور (Noor Library)
- University libraries (prosodic study editions)

**Target Poems:**
- "أنشودة المطر" - Multiple stanzas in المتدارك
- "المومس العمياء" - Contains المتدارك sections

**Expected Yield:** 3-4 verses

**Annotation Protocol:**
1. Use edition with scholarly commentary
2. Verify meter attribution in academic analyses:
   - Search Google Scholar: "بدر شاكر السياب" + "المتدارك"
   - Reference PhD dissertations on السياب's prosody
3. Manual تقطيع required (modern poetry has irregular tashkeel)
4. Validate with 2+ prosody experts familiar with modern poetry

---

### 2.2 نزار قباني (Nizar Qabbani)

**Why this poet:**
- Used المتدارك for romantic/musical effect
- Large corpus with some prosodic analyses
- Accessible language (less archaic than classical)

**Key Collections:**
1. **قصائد** (Poems) - Various volumes
2. **الرسم بالكلمات** (Drawing with Words)

**Search Strategy:**
```
1. Access complete dīwān (collected works)
2. Look for musical/rhythmic poems (المتدارك has "galloping" rhythm)
3. Search for poems with 4 short feet per line
4. Extract candidates
5. Verify with prosodic analysis
```

**Expected Yield:** 2-3 verses

---

### 2.3 محمود درويش (Mahmoud Darwish)

**Why this poet:**
- Contemporary master of varied meters
- Some المتدارك usage in later works
- Extensively studied academically

**Target Collections:**
1. **لماذا تركت الحصان وحيداً** (Why Did You Leave the Horse Alone?)
2. **جدارية** (Mural)

**Access:**
- Physical editions preferred
- Academic analyses: Search "محمود درويش" + "عروض" + "المتدارك"

**Expected Yield:** 1-2 verses

---

### 2.4 صلاح عبد الصبور (Salah Abdel Sabour)

**Why this poet:**
- Egyptian poet who experimented with meters
- Documented المتدارك usage
- Well-preserved manuscripts with proper tashkeel

**Target Collections:**
1. **الناس في بلادي** (People in My Country)
2. **أحلام الفارس القديم** (Dreams of the Ancient Knight)

**Expected Yield:** 1-2 verses

---

## 🔬 Source 3: Academic Publications

### 3.1 Prosody Journals

**Target Publications:**
1. **مجلة الشعر** (Poetry Magazine) - Archives 1957-1964
   - Contains prosodic analyses of contemporary poetry
   - May cite المتدارك examples

2. **مجلة التراث العربي** (Arab Heritage Magazine)
   - Academic studies on rare meters
   - Search archives for "المتدارك" or "الخبب"

3. **مجلة جامعة دمشق** (Damascus University Journal)
   - Arabic literature section
   - PhD abstracts often include meter analysis

**Access:**
- University digital libraries
- JSTOR (limited Arabic content)
- ResearchGate (Arabic prosody papers)

**Search Protocol:**
```
1. Search: "المتدارك" + "شعر" + "عروض"
2. Filter: peer-reviewed journals (2000-present for modern analyses)
3. Extract example verses from papers
4. Record full citation (author, year, journal, page)
5. Verify examples aren't already in our classical sources (no duplicates)
```

**Expected Yield:** 1-2 verses from academic examples

---

### 3.2 PhD Dissertations

**Search Databases:**
- **دار المنظومة** (Dar Almandumah) - Arabic thesis database
- **ProQuest** - Some Arabic theses
- **University repositories** - Damascus, Cairo, Baghdad universities

**Search Terms:**
- "البحر المتدارك"
- "الخبب في الشعر العربي"
- "العروض والأوزان الشعرية"

**Expected Yield:** 2-3 verses from dissertation examples

---

## 🧪 Source 4: Synthetic Verses (Controlled Composition)

### 4.1 Purpose of Synthetic Verses

**Why create synthetic verses:**
- Test specific edge cases not found in natural poetry
- Control ziḥāfāt combinations precisely
- Create boundary cases for disambiguation testing
- Fill gaps in variant coverage

**Composition Requirements:**
- MUST follow classical المتدارك rules exactly
- Must be grammatically correct and semantically meaningful
- Must pass validation by 3+ expert prosodists
- Must be marked as "synthetic" in metadata

---

### 4.2 Synthetic Verse Types Needed

**Type 1: Maximal Khabn (Heavy Ziḥāfāt)**
```
Pattern: فعلن فعلن فعلن فعلن
Phonetic: ///o ///o ///o ///o
Purpose: Test all positions with khabn simultaneously
Status: TO BE COMPOSED
```

**Composition Protocol:**
1. Compose verse following phonetic pattern
2. Ensure semantic coherence (not gibberish)
3. Add proper tashkeel (diacritics)
4. Validate with mutadarik_validator.py
5. Submit to expert panel (3 prosodists)
6. Require unanimous approval
7. Mark: `"edge_case_type": "synthetic_maximal_khabn"`

---

**Type 2: Disambiguation Boundary (المتدارك vs المتقارب)**
```
Pattern: Ambiguous between المتدارك and المتقارب
Purpose: Test disambig

uation logic
Status: TO BE COMPOSED
```

**Composition Protocol:**
1. Create verse that COULD be interpreted as either meter
2. Include contextual cues favoring المتدارك:
   - 4 tafāʿīl count (not 5-6 like المتقارب)
   - Specific ziḥāfāt only allowed in المتدارك
3. Document why it's المتدارك
4. Require expert panel to reach consensus
5. Mark: `"edge_case_type": "synthetic_disambiguation"`

---

**Expected Yield:** 2 synthetic verses total

---

## ✅ Validation Workflow

### Step-by-Step Process for Each Verse

```
┌─────────────────────────────┐
│ 1. SOURCE IDENTIFICATION    │
│    - Record: book, page,    │
│      edition, poet, era     │
└──────────┬──────────────────┘
           ↓
┌─────────────────────────────┐
│ 2. INITIAL EXTRACTION       │
│    - Copy full verse text   │
│    - Verify tashkeel        │
│    - Note any variants      │
└──────────┬──────────────────┘
           ↓
┌─────────────────────────────┐
│ 3. MANUAL TAQṬĪʿ            │
│    - Expert prosodist       │
│      performs scansion      │
│    - Identify tafāʿīl       │
│    - Label ziḥāfāt/ʿilal    │
└──────────┬──────────────────┘
           ↓
┌─────────────────────────────┐
│ 4. AUTOMATED VALIDATION     │
│    - Run mutadarik_         │
│      validator.py           │
│    - Check all criteria     │
│    - Review warnings        │
└──────────┬──────────────────┘
           ↓
┌─────────────────────────────┐
│ 5. EXPERT REVIEW (×3)       │
│    - 3 independent experts  │
│    - Blind annotation       │
│    - Calculate κ agreement  │
└──────────┬──────────────────┘
           ↓
┌─────────────────────────────┐
│ 6. CONSENSUS RESOLUTION     │
│    - If κ < 0.85: Panel     │
│      discussion             │
│    - Document decision      │
│    - Resolve disagreements  │
└──────────┬──────────────────┘
           ↓
┌─────────────────────────────┐
│ 7. GOLDEN SET INCLUSION     │
│    - Create JSONL entry     │
│    - Add to golden set      │
│    - Update metadata        │
└─────────────────────────────┘
```

---

## 📝 Annotation Template

### JSONL Format for Each Verse

```json
{
  "verse_id": "mutadarik_001",
  "text": "[Full Arabic text with tashkeel]",
  "normalized_text": "[Normalized without diacritics]",
  "meter": "المتدارك",
  "poet": "[Poet name in Arabic]",
  "source": "[Book title, edition, page number]",
  "era": "classical|modern|synthetic",
  "confidence": 0.92,
  "taqti3": "[فاعلن فاعلن فاعلن فاع]",
  "expected_tafail": ["فاعلن", "فاعلن", "فاعلن", "فاع"],
  "syllable_pattern": "/o//o /o//o /o//o /o/",
  "syllable_count": 14,
  "zihafat_applied": {
    "position_1": null,
    "position_2": null,
    "position_3": null,
    "position_4": "حذف"
  },
  "edge_case_type": "hadhf_final|maximal_khabn|disambiguation|canonical",
  "difficulty_level": "easy|medium|hard",
  "validation": {
    "verified_by": ["Dr. [Name 1]", "Dr. [Name 2]", "Dr. [Name 3]"],
    "verified_date": "2025-11-12",
    "inter_annotator_agreement": 0.89,
    "automated_check": "PASSED",
    "disambiguation_notes": "[Why this is المتدارك and not المتقارب/الرجز]",
    "reference_sources": [
      "الكافي في العروض والقوافي - التبريزي، ص 145",
      "موسيقى الشعر - إبراهيم أنيس، ص 87"
    ]
  },
  "notes": "[Any special considerations]",
  "metadata": {
    "version": "0.103",
    "created_at": "2025-11-12",
    "updated_at": "2025-11-12",
    "curator": "[Name]"
  }
}
```

---

## 📊 Progress Tracking

### Tracking Spreadsheet Template

| # | Verse ID | Source | Poet | Era | Variant | Difficulty | Status | Validators | κ | Date |
|---|----------|--------|------|-----|---------|------------|--------|------------|---|------|
| 1 | mutadarik_001 | الكافي ص145 | - | classical | canonical | easy | ✅ VALIDATED | Dr. A, Dr. B, Dr. C | 0.92 | 2025-11-12 |
| 2 | mutadarik_002 | السياب - أنشودة المطر | السياب | modern | محذوف | medium | 🔍 REVIEW | Dr. A, Dr. B | 0.78 | 2025-11-12 |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

**Status Codes:**
- 🔍 REVIEW - Under expert review
- ⚠️ DISPUTED - Low inter-annotator agreement
- ❌ REJECTED - Failed validation
- ✅ VALIDATED - Ready for golden set
- 📝 PENDING - Not yet reviewed

---

## ⚠️ Common Pitfalls to Avoid

### 1. Accepting Unverified Classical Attributions
**Problem:** Medieval manuscripts may have incorrect meter labels
**Solution:** Cross-reference with 2+ modern prosodic analyses

### 2. Confusing المتدارك with المتقارب
**Problem:** Same phonetic pattern for base tafʿīla
**Solution:** Count tafāʿīl; check ziḥāfāt allowed; context analysis

### 3. Using Modern Poetry Without Tashkeel
**Problem:** Ambiguous scansion without diacritics
**Solution:** Add tashkeel manually with expert; validate multiple ways

### 4. Duplicating Examples Across Sources
**Problem:** Same verses cited in multiple books
**Solution:** Track verse first lines; check for duplicates before adding

### 5. Low Inter-Annotator Agreement
**Problem:** Experts disagree on meter attribution
**Solution:** REJECT verse if κ < 0.85; don't force consensus

---

## 🎯 Success Criteria

### Minimum Acceptance Thresholds

| Criterion | Threshold | Why |
|-----------|-----------|-----|
| Inter-annotator agreement (κ) | ≥ 0.85 | Ensures consensus on difficult meter |
| Automated validation confidence | ≥ 0.85 | Detector must agree with experts |
| Expert verifiers | ≥ 2 | Multiple independent confirmations |
| Source documentation | Complete citation | Reproducibility and verification |
| Variant coverage | All 4 types | Comprehensive testing |
| Difficulty distribution | 20/40/40 | Balance easy/medium/hard |

---

## 📅 Timeline Estimate

| Phase | Duration | Deliverable |
|-------|----------|-------------|
| Classical sourcing | 1 week | 5 candidate verses from Shamela/al-Warraq |
| Modern poetry extraction | 2 weeks | 8 verses from السياب, قباني, درويش |
| Synthetic composition | 1 week | 2 validated synthetic verses |
| Expert validation | 2-3 weeks | All 15 verses verified with κ ≥ 0.85 |
| Golden set integration | 1 week | JSONL entries, metadata update |
| **TOTAL** | **7-8 weeks** | **15 verified المتدارك verses** |

---

## 📚 Expert Recruitment

### Required Qualifications

**Minimum requirements:**
- PhD in Arabic linguistics OR 10+ years teaching العروض
- Published work on Arabic prosody
- Familiarity with both classical and modern poetry
- Ability to perform manual تقطيع

**Preferred:**
- Specialization in rare meters or المتدارك specifically
- Experience with modern free verse (شعر التفعيلة)
- Prior work with corpus annotation

**Compensation:**
- $50-100 per verse annotation (estimated 30-60 min per verse)
- Recognition in published dataset
- Co-authorship on methodology paper (if applicable)

### Recruitment Strategy

1. **University prosody departments:**
   - Contact faculty at: Damascus, Cairo, Baghdad, Amman universities
   - Arabic linguistics departments at Western universities (Georgetown, Harvard)

2. **Academic networks:**
   - Post to Arabic linguistics mailing lists
   - LinkedIn groups for Arabic prosody scholars

3. **Direct outreach:**
   - Authors of recent prosody publications
   - Editors of Arabic poetry journals

---

## 📞 Contact & Support

**Questions about sourcing?**
- Refer to: MUTADARIK_TECHNICAL_ANALYSIS.md (section 6.1-6.3)
- Tool documentation: tools/mutadarik_validator.py

**Validation issues?**
- Run: `python tools/mutadarik_validator.py --help`
- Check: MUTADARIK_TECHNICAL_ANALYSIS.md (section 5.1-5.3)

**Expert panel coordination:**
- Create shared annotation spreadsheet (Google Sheets)
- Use blind annotation (experts don't see each other's work initially)
- Schedule consensus meeting for disputed cases

---

**Document Owner:** BAHR Detection Engine Team
**Last Updated:** 2025-11-12
**Version:** 1.0
**Status:** Ready for implementation
