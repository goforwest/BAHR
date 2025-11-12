# المتدارك (al-Mutadārak): Technical Analysis & Annotation Challenges

**Document Version:** 1.0
**Date:** 2025-11-12
**Status:** Draft for Expert Review
**Purpose:** Comprehensive analysis of المتدارك meter to guide gold-standard annotation

---

## 1. Executive Summary

**Current Status:**
- ✅ Meter definition implemented in detection engine (meters.py:535-555)
- ✅ Pattern generation working (36+ valid patterns)
- ❌ Golden set coverage: 0/182 verses (0%)
- ❌ Previous annotation attempts: 6 verses attempted, 6 removed due to errors

**Critical Gap:**
المتدارك is the ONLY meter (out of 20) with zero test coverage, making it impossible to verify detection accuracy. This represents a 5% blind spot in the system.

**Root Cause:**
All previous annotation attempts failed due to incorrect tafʿīla scansion, suggesting fundamental challenges in identifying authentic المتدارك verses and applying correct prosodic analysis.

---

## 2. Prosodic Definition

### 2.1 Classical Foundation

**Historical Context:**
- **NOT** included in الخليل بن أحمد الفراهيدي's original 15 meters (8th century)
- **ADDED** by الأخفش الأوسط (9th century) as the 16th meter
- **Name etymology:** "المتدارك" = "the overtaking/catching up" OR "المحدَث" = "the newly created"
- **Classical controversy:** Some prosodists disputed its status as an independent meter

**Base Pattern (التام - Full Form):**

```
Arabic:    فاعِلُنْ  فاعِلُنْ  فاعِلُنْ  فاعِلُنْ
Phonetic:  /o//o    /o//o    /o//o    /o//o
Structure: [WS]     [WS]     [WS]     [WS]

Where:
  W = watad majmūʿ (////o = 3 mutaḥarrik + sākin)
  S = sabab khafīf (/o = mutaḥarrik + sākin)
```

**Syllable Count:** 16 syllables (4 tafāʿīl × 4 syllables each)

**Alternative Names:**
- الخَبَب (al-khabab) - "galloping" (describes the rhythm)
- المُحدَث (al-muḥdath) - "the invented one"

### 2.2 Structural Characteristics

**Tafʿīla: فاعِلُنْ**

Pattern breakdown:
```
فا  = فَا  = /o   = sabab khafīf (light)
عِلُ = عِلُ = //   = start of watad
نْ  = نْ  = o    = end of watad

Full: /o//o
```

**Unique Features:**
1. **Uniform structure:** All 4 tafāʿīl are identical (unlike most meters)
2. **Rapid rhythm:** Short tafʿīla creates faster pace than الطويل or الكامل
3. **Watad-initial:** Starts with watad majmūʿ, unlike sabab-initial meters

### 2.3 Prosodic Transformations (Ziḥāfāt & ʿIlal)

**Allowed Ziḥāfāt (Non-Final Positions):**

| Name | Type | Transformation | Result | Frequency |
|------|------|---------------|---------|-----------|
| **خَبْن** (khabn) | Single | Remove 2nd sākin | فَعِلُنْ (///o) | Very Common |

Application:
```
Base:     فاعِلُنْ  (/o//o)  →  after khabn:  فَعِلُنْ  (///o)
          ↓ remove 2nd consonant (ا)
Result:   فَ + عِلُنْ = فَعِلُنْ
```

**Allowed ʿIlal (Final Position Only):**

| Name | Type | Transformation | Result | Usage |
|------|------|---------------|---------|--------|
| **حَذْف** (ḥadhf) | Terminal | Remove final sabab | فاعِ (/o/) | Common |
| **قَصْر** (qaṣr) | Terminal | Make last letter sākin | فاعِلْ (/o///) | Common |

**Pattern Examples:**

1. **Canonical (no transformations):**
   ```
   /o//o  /o//o  /o//o  /o//o
   فاعلن  فاعلن  فاعلن  فاعلن
   ```

2. **With khabn (positions 1-3):**
   ```
   ///o   /o//o  ///o   /o//o
   فعلن   فاعلن  فعلن   فاعلن
   ```

3. **With ḥadhf (final position):**
   ```
   /o//o  /o//o  /o//o  /o/
   فاعلن  فاعلن  فاعلن  فاع
   ```

4. **Combined (khabn + qaṣr):**
   ```
   ///o   /o//o  ///o   /o///
   فعلن   فاعلن  فعلن   فاعل
   ```

**Total Valid Patterns:** 36+ combinations (calculated by PatternGenerator)

---

## 3. Why Standard Annotations Fail

### 3.1 Analysis of Failed Attempts

**Removed Verses (6 total):**
From `removed_verses_log.json` (lines 70-99):

```json
{
  "id": "golden_170",
  "meter": "المتدارك",
  "text": "ما أَجوَدَ شِعريَ في خَبَبٍ وَالشِعرُ قَليلٌ جَيِّدُهُ"
}
// + 5 more (golden_171-175)
```

**Failure Reason:** "Incorrect tafail annotations - phonetic pattern doesn't match expected meter"

### 3.2 Root Cause Analysis

**Problem 1: Confusion with الرجز (al-Rajaz)**

Both meters share overlapping patterns after transformations:

| Meter | Base Tafʿīla | After Ziḥāfāt | Potential Conflict |
|-------|-------------|---------------|-------------------|
| **المتدارك** | فاعلن (/o//o) | فعلن (///o) after khabn | ✓ Identical |
| **الرجز** | مستفعلن (/o/o//o) | متفعلن (//o//o) → فعلن (///o) | ✓ Identical |

**Distinguishing factor:** Position count and pattern length
- الرجز: 3 tafāʿīl of مستفعلن
- المتدارك: 4 tafāʿīl of فاعلن

**Problem 2: Confusion with الكامل (al-Kāmil)**

After heavy transformations:

| Meter | Base | Shortened Form | Conflict |
|-------|------|---------------|----------|
| **المتدارك** | فاعلن × 4 | Can appear similar to 3-tafʿīla meters | ✓ |
| **الكامل** | متفاعلن × 4 | مجزوء variants with 2-3 tafāʿīl | ✓ |

**Problem 3: Modern vs. Classical Usage**

**Classical (pre-1900):**
- Extremely rare (<0.5% of classical poetry)
- Strict adherence to base pattern
- Limited ziḥāfāt application
- Often confused with other meters by medieval scribes

**Modern (20th century+):**
- Popularized by تفعيلة (free verse) poets: بدر شاكر السياب، نزار قباني
- Liberalized ziḥāfāt usage
- Mixed with other rhythmic patterns
- Variable tafʿīla counts (not always 4)

**Annotation challenge:** Classical references may have incorrect attributions; modern poetry may deviate from classical rules.

**Problem 4: Regional Variations**

Different prosodic traditions apply ziḥāfāt differently:

- **Hijazi (Arabian):** Conservative, minimal khabn
- **Iraqi (Mesopotamian):** Heavy khabn usage, especially in modern poetry
- **Andalusian (Maghrebi):** Mixed with موشحات patterns
- **Levantine:** Contemporary adaptations

**Problem 5: Scarcity Bias in Annotation**

**Psychological factor:** Annotators unfamiliar with المتدارك default to "closest common meter"

Decision tree (unconscious):
```
Unknown verse
  ↓
Scan tafāʿīl
  ↓
Pattern ambiguous?
  ├─ Yes → Default to الرجز (common)
  └─ No → Check next most common (الكامل, البسيط)
```

**Result:** Genuine المتدارك verses misclassified as الرجز or الكامل

### 3.3 Ziḥāf Cascade Errors

**Scenario:** Sequential ziḥāfāt create unrecognizable patterns

Example transformation chain:
```
1. Start: فاعلن فاعلن فاعلن فاعلن
2. Apply khabn to positions 1,3: فعلن فاعلن فعلن فاعلن
3. Apply ḥadhf to position 4: فعلن فاعلن فعلن فاع
4. Final: ///o /o//o ///o /o/
```

**Problem:** Final pattern `///o /o//o ///o /o/` could theoretically match:
- المتدارك with khabn + ḥadhf (CORRECT)
- الرجز variant with complex transformations (INCORRECT but plausible)

**Without expert knowledge:** Annotators cannot confidently distinguish.

### 3.4 Inadequate Reference Materials

**Classical prosody manuals vary:**

| Source | المتدارك Status | Reliability |
|--------|-----------------|-------------|
| الخليل's العروض | NOT included | ⚠️ Omits meter entirely |
| الأخفش's additions | Included as 16th meter | ✓ Original definition |
| التبريزي's الكافي في العروض | Included with variants | ✓ Good |
| الزمخشري's القسطاس | Brief mention | ⚠️ Limited examples |

**Modern compilations:**
- Often cite same 5-10 example verses repeatedly
- May perpetuate historical misattributions
- Limited coverage of ziḥāfāt variants

---

## 4. Detection Engine Implementation

### 4.1 Current Implementation (meters.py)

**Code Location:** `/home/user/BAHR/backend/app/core/prosody/meters.py` (Lines 535-555)

```python
AL_MUTADARIK = Meter(
    id=16,
    name_ar="المتدارك",
    name_en="al-Mutadarik",
    tier=MeterTier.TIER_3,  # Rare meter
    frequency_rank=16,
    base_tafail=[
        TAFAIL_BASE["فاعلن"],  # Position 1
        TAFAIL_BASE["فاعلن"],  # Position 2
        TAFAIL_BASE["فاعلن"],  # Position 3
        TAFAIL_BASE["فاعلن"],  # Position 4
    ],
    rules_by_position={
        1: MeterRules(allowed_zihafat=[KHABN]),
        2: MeterRules(allowed_zihafat=[KHABN]),
        3: MeterRules(allowed_zihafat=[KHABN]),
        4: MeterRules(
            allowed_zihafat=[KHABN],
            allowed_ilal=[HADHF, QASR],
            is_final=True
        ),
    },
    description='البحر السادس عشر، "استدركه الأخفش على الخليل"'
)
```

**Pattern Generation:**
- Base pattern: `/o//o/o//o/o//o/o//o` (16 syllables)
- With khabn variations: 2^4 = 16 ziḥāfāt combinations
- With ʿilal variations: ×3 (base, ḥadhf, qaṣr)
- **Total patterns:** 16 × 3 = 48 theoretical (36+ validated)

### 4.2 Detection Confidence

**Pattern matching logic (detector_v2.py):**

```python
def _match_meter(phonetic_pattern, meter):
    # Exact match: 100% confidence
    if pattern in meter.valid_patterns:
        return DetectionResult(confidence=1.0, ...)

    # Fuzzy match: 90%+ similarity
    close_match = self._find_close_match(pattern, meter)
    if close_match and similarity >= 0.90:
        return DetectionResult(confidence=0.85-0.95, ...)
```

**Expected confidence for المتدارك:**
- Canonical forms: 0.95-1.0
- With khabn: 0.90-0.95
- With ḥadhf/qaṣr: 0.85-0.90
- Ambiguous cases: <0.85 (should trigger human review)

### 4.3 Confusion Matrix Predictions

**Based on pattern analysis, المتدارك may be confused with:**

| Meter | Confusion Risk | Reason |
|-------|---------------|--------|
| الرجز | **HIGH** | فعلن pattern overlap |
| الكامل (مجزوء) | MEDIUM | Similar syllable count in shortened forms |
| الهزج | LOW | Different watad structure |

**Mitigation:** Test verses MUST include boundary cases that explicitly distinguish المتدارك from الرجز.

---

## 5. Annotation Requirements

### 5.1 Mandatory Validation Checks

**Before any المتدارك verse enters the golden set:**

1. **Tafʿīla count verification:**
   - Must have exactly 4 tafāʿīl (or 2/3 for مجزوء if applicable)
   - Each tafʿīla must parse as فاعلن or its ziḥāfāt variants

2. **Phonetic pattern validation:**
   - Generate phonetic transcription (IPA)
   - Match against 36+ valid patterns
   - Confidence score must be ≥0.85

3. **Ziḥāfāt compliance:**
   - Only خبن allowed in non-final positions
   - Only حذف/قصر allowed in final position
   - Flag any other transformations as invalid

4. **Disambiguation test:**
   - Verify verse does NOT match الرجز patterns with higher confidence
   - Document why it's المتدارك and not الرجز

5. **Expert verification:**
   - Minimum 2 prosodists must independently confirm
   - Include source citation from classical/modern reference

### 5.2 Annotation Schema (Extended)

**Required fields for المتدارك verses:**

```json
{
  "verse_id": "mutadarik_001",
  "text": "[Original Arabic text with full tashkeel]",
  "meter": "المتدارك",
  "taqti3": "[Manual prosodic scansion]",
  "expected_tafail": ["فاعلن", "فعلن", "فاعلن", "فاع"],
  "phonetic_pattern": "/o//o///o/o//o/o/",
  "zihafat_applied": {
    "position_2": "خبن",
    "position_4": "حذف"
  },
  "confidence": 0.92,
  "source": "ديوان بدر شاكر السياب، ص 145",
  "poet": "بدر شاكر السياب",
  "era": "modern",
  "validation": {
    "verified_by": ["Dr. [Name 1]", "Dr. [Name 2]"],
    "verified_date": "2025-11-12",
    "disambiguation_notes": "Clearly المتدارك - 4 tafāʿīl of فاعلن pattern, not الرجز (which would be 3 مستفعلن)",
    "automated_check": "PASSED",
    "reference_sources": [
      "الكافي في العروض والقوافي - التبريزي",
      "موسيقى الشعر - إبراهيم أنيس"
    ]
  },
  "edge_case_type": "khabn_boundary_test",
  "difficulty_level": "hard"
}
```

### 5.3 Quality Assurance Checklist

**Per verse:**
- [ ] Text has full tashkeel (diacritics)
- [ ] Manual taqṭīʿ completed by expert
- [ ] Phonetic pattern generated and validated
- [ ] Ziḥāfāt identified and named
- [ ] Source cited (book, page number, edition)
- [ ] 2+ experts verified independently
- [ ] Inter-annotator agreement κ ≥ 0.85
- [ ] Automated validation passed
- [ ] Disambiguation from الرجز documented
- [ ] Confidence score ≥ 0.85

---

## 6. Corpus Sourcing Strategy

### 6.1 Classical Sources (Target: 5-8 verses)

**Primary references:**

1. **الموشحات الأندلسية** (Andalusian Muwashshaḥāt)
   - Library: المكتبة الشاملة (Shamela)
   - Search term: "المتدارك" OR "الخبب"
   - Expected yield: 2-3 verses

2. **المفضليات** (al-Mufaḍḍalīyāt)
   - Some poems attributed to المتدارك by later prosodists
   - Requires expert verification (contested attributions)
   - Expected yield: 1-2 verses

3. **ديوان الأدب** (Dīwān al-Adab) by الفارابي
   - Contains prosody annotations
   - Expected yield: 1-2 verses

**Digital libraries:**
- [Shamela](https://shamela.ws/) - Keyword: "بحر المتدارك"
- [al-Warraq](https://www.alwaraq.net/) - Advanced prosody search
- [Dīwān al-ʿArab](https://www.diwanalarab.com/) - Filter by meter

### 6.2 Modern Sources (Target: 8-12 verses)

**Known المتدارك practitioners:**

1. **بدر شاكر السياب** (Badr Shakir al-Sayyab)
   - Collection: "أنشودة المطر" (Rain Song)
   - Known for المتدارك usage in free verse
   - Expected yield: 3-4 verses

2. **نزار قباني** (Nizar Qabbani)
   - Collection: "قصائد" (Poems)
   - Romantic poetry with المتدارك rhythm
   - Expected yield: 2-3 verses

3. **محمود درويش** (Mahmoud Darwish)
   - Collection: "لماذا تركت الحصان وحيداً" (Why Did You Leave the Horse Alone)
   - Contemporary المتدارك adaptations
   - Expected yield: 2-3 verses

4. **صلاح عبد الصبور** (Salah Abdel Sabour)
   - Collection: "الناس في بلادي" (People in My Country)
   - Expected yield: 1-2 verses

**Academic journals:**
- **مجلة الشعر** (Poetry Magazine) - Archives 1957-1964
- **آفاق عربية** (Arab Horizons) - Prosody analyses

### 6.3 Synthesized Edge Cases (Target: 3-5 verses)

**Purpose:** Test boundary conditions

**Creation protocol:**
1. Compose verses following المتدارك rules
2. Apply maximal ziḥāfāt (all 4 positions with khabn)
3. Apply rare ʿilal (qaṣr instead of common ḥadhf)
4. Create confusion set: verses at boundary with الرجز
5. Validate with 3+ prosodists
6. Mark as "synthetic" in metadata

**Example synthetic verse (to be composed):**
```
Meter: المتدارك
Pattern: فعلن فعلن فعلن فاع (khabn ×3, ḥadhf ×1)
Purpose: Maximal ziḥāfāt test
```

---

## 7. Validation Tools Required

### 7.1 Automated Validators

**Tool 1: Tafʿīla Pattern Checker**
```python
def validate_mutadarik_pattern(verse_text, expected_tafail):
    """
    Validates that tafāʿīl match المتدارك rules
    Returns: (is_valid, confidence, errors)
    """
    # 1. Check tafʿīla count (must be 4, or 2/3 for variants)
    # 2. Each tafʿīla must be فاعلن or variants (فعلن, فاع, etc.)
    # 3. Ziḥāfāt must be خبن only (non-final)
    # 4. ʿIlal must be حذف or قصر only (final)
    # 5. Pattern must match one of 36+ valid patterns
```

**Tool 2: Disambiguation Engine**
```python
def disambiguate_mutadarik_vs_rajaz(phonetic_pattern):
    """
    Determines if pattern is المتدارك or الرجز
    Returns: (meter, confidence, reasoning)
    """
    # 1. Count tafāʿīl
    # 2. Check tafʿīla types (فاعلن vs مستفعلن)
    # 3. Calculate pattern length
    # 4. Return most likely meter with explanation
```

**Tool 3: Inter-Annotator Agreement Calculator**
```python
def calculate_agreement(annotations):
    """
    Computes Fleiss' κ across multiple annotators
    Requires: κ ≥ 0.85 for gold standard inclusion
    """
```

### 7.2 Human Review Interface

**Annotation UI requirements:**
1. Side-by-side comparison: Original text vs. phonetic pattern
2. Tafʿīla-by-tafʿīla breakdown with ziḥāfāt highlighting
3. Confidence score visualization
4. Confusion warning: "This pattern also matches الرجز with 78% confidence"
5. Expert comment field for disambiguation notes
6. Source citation input
7. Approval workflow: Annotator 1 → Annotator 2 → Arbiter (if disagreement)

---

## 8. Success Criteria

### 8.1 Minimum Viable Coverage

**Target: 15 المتدارك verses**

Distribution:
- Classical: 5 verses (pre-1900)
- Modern: 8 verses (1900-present)
- Synthetic: 2 verses (edge cases)

Difficulty:
- Easy (canonical): 3 verses (20%)
- Medium (1-2 ziḥāfāt): 6 verses (40%)
- Hard (3+ ziḥāfāt, boundary cases): 6 verses (40%)

Variants:
- صحيح (canonical): 5 verses
- محذوف (with ḥadhf): 5 verses
- مقطوع (with qaṣr): 3 verses
- أبتر (rare variant): 2 verses

### 8.2 Validation Metrics

**Required:**
- 100% accuracy on test set (15/15 correct)
- Inter-annotator agreement: κ ≥ 0.85
- Confidence scores: mean ≥ 0.88, min ≥ 0.80
- Zero confusions with الرجز in final test
- 2+ expert sign-offs

### 8.3 Documentation Deliverables

**Upon completion:**
1. Annotated المتدارك corpus (15 verses, JSON)
2. Annotation methodology report
3. Expert validation certificates
4. Confusion matrix (المتدارك vs. all other meters)
5. Evaluation report showing 100% accuracy
6. Reproducible test harness

---

## 9. Risk Mitigation

### 9.1 Identified Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Insufficient authentic verses | MEDIUM | HIGH | Expand to modern poetry; accept synthetic verses with expert approval |
| Inter-annotator disagreement | MEDIUM | MEDIUM | 3-expert panel for contested cases; require 2/3 consensus |
| Pattern confusion with الرجز | HIGH | HIGH | Explicit disambiguation tests; boundary case coverage |
| Classical references have errors | MEDIUM | HIGH | Cross-reference multiple sources; prioritize modern scholarly analyses |
| Time to find expert annotators | LOW | MEDIUM | Start with university prosody departments; offer compensation |

### 9.2 Contingency Plans

**If authentic classical verses are insufficient:**
- Lower classical target to 3 verses
- Increase modern poetry to 10 verses
- Add 4 synthetic verses (with clear labeling)

**If inter-annotator agreement is low (<0.85):**
- Conduct calibration session with annotators
- Provide reference guide with examples
- Narrow scope to only canonical forms initially

**If detection accuracy <100%:**
- Analyze failure modes
- Augment ziḥāfāt rules if needed
- Add more training patterns to detection engine

---

## 10. Next Steps

### 10.1 Immediate Actions (Week 1-2)

1. **Build validation tools:**
   - Tafʿīla pattern checker
   - Disambiguation engine
   - Inter-annotator agreement calculator

2. **Recruit experts:**
   - Contact 3-5 Arabic prosody scholars
   - Provide compensation structure
   - Schedule calibration session

3. **Source initial verses:**
   - Search Shamela for "المتدارك"
   - Review بدر شاكر السياب collections
   - Identify 20 candidate verses (to select 15 final)

### 10.2 Annotation Phase (Week 3-6)

1. Blind annotation by 3 experts
2. Calculate inter-annotator agreement
3. Resolve disagreements via panel
4. Generate final annotated corpus

### 10.3 Validation Phase (Week 7-8)

1. Run detection engine on annotated corpus
2. Measure accuracy, confidence, confusion
3. Generate evaluation report
4. Obtain expert sign-offs

### 10.4 Certification (Week 9+)

1. External expert review (2+ scholars)
2. Peer review preparation
3. Dataset publication
4. Claim 100% coverage across all 20 meters

---

## 11. References

### 11.1 Classical Prosody Sources

1. **الخليل بن أحمد الفراهيدي** - "كتاب العروض" (Kitāb al-ʿArūḍ)
2. **الأخفش الأوسط** - Additions to الخليل's system (المتدارك definition)
3. **التبريزي** - "الكافي في العروض والقوافي" (Al-Kāfī fī al-ʿArūḍ wa-al-Qawāfī)
4. **الزمخشري** - "القسطاس في علم العروض" (Al-Qusṭās fī ʿIlm al-ʿArūḍ)

### 11.2 Modern Prosody Studies

1. **إبراهيم أنيس** - "موسيقى الشعر" (Mūsīqā al-Shiʿr, 1952)
2. **كمال أبو ديب** - "في البنية الإيقاعية للشعر العربي" (On the Rhythmic Structure of Arabic Poetry, 1974)
3. **محمد مندور** - "العروض والقافية" (Prosody and Rhyme, 1958)

### 11.3 Digital Resources

1. **Shamela Library** - https://shamela.ws/
2. **al-Warraq** - https://www.alwaraq.net/
3. **Dīwān al-ʿArab** - https://www.diwanalarab.com/

---

## Appendix A: Comparison Table (المتدارك vs. الرجز)

| Feature | المتدارك | الرجز |
|---------|----------|-------|
| **Base tafʿīla** | فاعلن (/o//o) | مستفعلن (/o/o//o) |
| **Tafʿīla count** | 4 | 3 |
| **After khabn** | فعلن (///o) | متفعلن (//o//o) |
| **After khabl** | — (khabl not allowed) | مفاعلن (/o///o) |
| **Total syllables** | 16 (full form) | 18-21 |
| **Rhythm** | Fast, galloping | Moderate, bouncing |
| **Classical usage** | Very rare (<0.5%) | Common (~8%) |
| **Diagnostic test** | Count tafāʿīl = 4? | Count tafāʿīl = 3? |

---

## Appendix B: Failed Annotation Examples

**Example 1: golden_170**
```
Text: "ما أَجوَدَ شِعريَ في خَبَبٍ وَالشِعرُ قَليلٌ جَيِّدُهُ"
Claimed meter: المتدارك
Actual meter: [Unknown - needs re-analysis]
Failure reason: Tafʿīla count didn't match expected 4×فاعلن pattern
```

**Lesson:** Must perform manual تقطيع before claiming المتدارك. Keyword "خَبَب" suggests المتدارك but doesn't guarantee correct scansion.

---

**Document Status:** Ready for expert review
**Next Update:** After validation tool implementation
**Owner:** BAHR Detection Engine Team
**Reviewers:** [To be assigned - 2 prosody experts]
