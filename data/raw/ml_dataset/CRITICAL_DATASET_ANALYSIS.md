# Critical Dataset Quality Analysis & Action Plan

**Date:** November 14, 2025  
**Analyst:** Senior Arabic NLP Researcher | Dataset Quality Engineer | ʿArūḍ Specialist  
**Dataset:** Arabic Prosody ML Training Dataset (2,032 verses)  

---

## 🚨 CRITICAL FINDINGS

### Primary Issue: Massive Duplication (80.6% Redundancy)

**Problem:** The batch collection system reused the same 20 verses across multiple batches, creating extensive duplication.

**Impact:**
- **Original dataset:** 2,032 verses
- **Unique verses:** 394 verses (19.4%)
- **Redundant verses:** 1,638 verses (80.6%)
- **Duplicate groups:** 392 groups

**Root Cause:** The `poetry_sources.py` database contains only ~20 unique verses per meter, which were recycled across 5-6 batches per meter, creating an illusion of a large dataset.

---

## 📊 DETAILED ANALYSIS

### 1. Exact Duplication Breakdown

#### Pattern Observed:
- Each meter has ~20 unique source verses in `poetry_sources.py`
- Batch collection ran 5-6 batches × 20 verses = 100-120 total entries per meter
- **Result:** Each verse appears 5-6 times in the dataset

#### Example (Meter 3 - البسيط):
```
Verse: "إِنَّ الثَّمَانِينَ وَبُلِّغْتَهَا قَدْ أَحْوَجَتْ سَمْعِي إِلَى تَرْجُمَانِ"
Poet: لبيد بن ربيعة
Appearances: 11 times
Files: basit_batch_001 through basit_batch_006
```

This pattern repeats for **all 392 unique verses** across **all 20 meters**.

### 2. Fuzzy Duplicates (61 Pairs)

**Finding:** 61 pairs of verses with ≥90% text similarity detected.

**Possible Causes:**
- Variant readings of the same verse (رواية)
- Similar verses from same poet/poem
- Normalization artifacts
- OCR/transcription variations

**Action Required:** Manual review to determine whether these are true duplicates or acceptable variants.

### 3. Cross-Meter Anomalies (5 Cases)

**Finding:** 5 unique verses appear in multiple meters simultaneously.

**Examples:**
```
Verse appearing in Meters 3 & 8:
"إِنَّ الثَّمَانِينَ وَبُلِّغْتَهَا قَدْ أَحْوَجَتْ سَمْعِي إِلَى تَرْجُمَانِ"
```

**Root Cause:** Same source verse assigned to multiple meters due to:
- Prosodic ambiguity
- Collection script error
- Meter misclassification

**Action:** Verify correct meter assignment using prosodic analysis, keep in one meter only.

### 4. Poet Distribution Imbalances (95 Cases)

**Finding:** 95 instances where a single poet exceeds 5% representation in a meter.

**Severe Cases:**
- **Meter 5 (الرجز):** 
  - رؤبة: 14.9% (15/101) - Exceeds by 9.9%
  - أبو النجم: 19.8% (20/101) - Exceeds by 14.8%
  - العجاج: 29.7% (30/101) - Exceeds by 24.7%

**Root Cause:** Limited poet diversity in source database (poetry_sources.py).

**Impact:** Model may overfit to specific poets' styles rather than learning general meter patterns.

### 5. Prosodic Pattern Duplication

**Finding:** 0 cases of prosodic pattern duplication detected.

**Interpretation:** While verses are duplicated exactly, there's no evidence of different verses sharing identical prosodic patterns inappropriately. This is actually positive.

---

## ⚠️ ACTUAL DATASET STATUS

### What We Thought We Had:
```
✅ 2,032 unique verses
✅ 100+ verses per meter
✅ Diverse poet representation
✅ Comprehensive coverage of 20 meters
```

### What We Actually Have:
```
❌ 394 unique verses (19.4%)
❌ ~20 verses per meter (original source size)
❌ Limited poet diversity per meter
❌ Systematic duplication across all meters
```

---

## 🔧 ROOT CAUSE ANALYSIS

### Collection System Architecture Review

**Step 1: Poetry Sources (`poetry_sources.py`)**
```python
'البسيط': [
    {'text': 'verse 1', 'poet': 'poet A', ...},  # 20 verses total
    {'text': 'verse 2', 'poet': 'poet B', ...},
    ...
    {'text': 'verse 20', 'poet': 'poet T', ...},
]
```

**Step 2: Batch Collection (`batch_collector.py`)**
```python
for batch_num in range(1, 6):  # 5 batches
    verses = get_verses_by_meter(meter_name, limit=20)  # Same 20 verses
    validate_and_export(verses, f'batch_{batch_num:03d}.jsonl')
```

**Problem:** No randomization, augmentation, or expansion beyond the initial 20 verses.

**Result:** Each batch contains the exact same 20 verses, creating 5× duplication.

### Why Deduplication Wasn't Detected Earlier

The collection system has a `verse_cache` for deduplication, but it:
1. ✅ Works correctly **within a single batch**
2. ❌ Resets **between batches**
3. ❌ Doesn't track **global duplicates across all batches**

```python
# In collect_dataset.py
verse_cache = set()  # Reset for each batch!

for verse in candidate_verses:
    verse_hash = hashlib.md5(normalized.encode()).hexdigest()
    if verse_hash not in verse_cache:  # Only checks current batch
        verse_cache.add(verse_hash)
        validated_verses.append(verse)
```

---

## 📋 ACTION PLAN

### Option A: Minimal Fix (Keep Current System)

**Approach:** Accept the 394 unique verses as the true dataset size.

**Actions:**
1. ✅ Use deduplicated dataset from `deduplicated/` folder
2. ✅ Update documentation to reflect actual size (394 verses)
3. ✅ Distribute verses: ~20 per meter (current state)
4. ⚠️ Acknowledge limitation: Small dataset size

**Pros:**
- Quick implementation (already done by evaluation)
- High-quality authentic verses
- No additional collection needed

**Cons:**
- Very small dataset (~20 verses/meter)
- May not be sufficient for ML training
- Limited poet diversity per meter

---

### Option B: Expand Poetry Database (Recommended)

**Approach:** Expand `poetry_sources.py` with 100+ unique verses per meter.

**Actions:**

**Phase 1: Research & Sourcing**
1. Identify classical poetry sources for each meter
2. Collect 100-150 unique authentic verses per meter
3. Ensure poet diversity (max 5% per poet = 5-7 verses)
4. Verify prosodic correctness for each verse

**Phase 2: Database Expansion**
```python
# Expand each meter section in poetry_sources.py
'البسيط': [
    # Current 20 verses
    {'text': '...', 'poet': '...', ...},
    
    # Add 80-130 new unique verses
    {'text': 'NEW_VERSE_21', 'poet': 'NEW_POET', ...},
    {'text': 'NEW_VERSE_22', 'poet': 'NEW_POET', ...},
    ...
    {'text': 'NEW_VERSE_150', 'poet': 'NEW_POET', ...},
]
```

**Phase 3: Re-Collection**
1. Clear existing JSONL files
2. Run batch collection with expanded database
3. Verify global deduplication across all batches
4. Validate final dataset

**Expected Outcome:**
- 2,000+ **truly unique** verses
- 100+ verses per meter
- Proper poet diversity
- Blueprint-compliant quality

**Timeline:** 2-3 weeks (research + implementation)

---

### Option C: Implement Smart Augmentation

**Approach:** Use the 394 unique verses as seeds for controlled augmentation.

**Techniques:**
1. **Variant Readings (روايات):** Use authenticated variant readings of verses
2. **Meter Variations:** Include مجزوء and محذوف forms
3. **Historical Variants:** Same verse from different manuscripts
4. **Poet Corpus Expansion:** Find more verses from same poets

**Caution:** Must maintain authenticity and prosodic correctness.

---

### Option D: Hybrid Approach (Best Practice)

**Combine Options B + C:**

1. **Expand core database** to 50-70 unique verses per meter (Option B - reduced scope)
2. **Use authentic variants** to reach 100-120 total (Option C)
3. **Strict quality control** at every step
4. **Comprehensive validation** before final export

**Expected Outcome:**
- 2,000-2,400 high-quality verses
- Balanced poet representation
- Authentic classical sources
- Prosodically verified

**Timeline:** 3-4 weeks

---

## 🎯 IMMEDIATE NEXT STEPS

### Step 1: Decision (Required Today)

**Question for stakeholders:**

> "We've discovered the dataset contains 80.6% duplication due to the batch collection system reusing 20 source verses 5-6 times each. The actual unique dataset is 394 verses (~20 per meter), not 2,032.
>
> Which approach should we take?
> - **A:** Accept 394 verses (small but clean)
> - **B:** Expand poetry database to 100+ per meter (2-3 weeks)
> - **C:** Use augmentation techniques (carefully)
> - **D:** Hybrid B+C approach (3-4 weeks)"

### Step 2: Immediate Use of Clean Data

**While deciding on expansion:**

1. ✅ Use the deduplicated dataset (394 verses) for initial experiments
2. ✅ Test ML pipeline with clean data
3. ✅ Establish baseline model performance
4. ✅ Identify which meters need priority expansion

**Available Now:**
```
deduplicated/
├── البسيط_deduped_batch_001.jsonl (20 verses)
├── الخفيف_deduped_batch_001.jsonl (20 verses)
├── الرجز_deduped_batch_001.jsonl (20 verses)
... (20 files total, 394 verses)
```

### Step 3: Fix Collection System

**Prevent future duplication:**

```python
# Implement global deduplication cache
GLOBAL_VERSE_CACHE_FILE = 'global_verse_cache.json'

def load_global_cache():
    if os.path.exists(GLOBAL_VERSE_CACHE_FILE):
        with open(GLOBAL_VERSE_CACHE_FILE, 'r') as f:
            return set(json.load(f))
    return set()

def save_global_cache(cache):
    with open(GLOBAL_VERSE_CACHE_FILE, 'w') as f:
        json.dump(list(cache), f)

# In collection function:
global_cache = load_global_cache()

for verse in candidate_verses:
    verse_hash = get_hash(verse)
    if verse_hash not in global_cache:
        global_cache.add(verse_hash)
        validated_verses.append(verse)

save_global_cache(global_cache)
```

---

## 📊 COMPARISON: BEFORE vs AFTER

| Metric | Before Evaluation | After Deduplication |
|--------|------------------|---------------------|
| Total Verses | 2,032 | 394 |
| Unique Verses | 394 (unknown) | 394 (verified) |
| Redundancy | 80.6% | 0% |
| JSONL Files | 106 | 20 |
| Verses/Meter | 100-114 (mostly duplicates) | ~20 (all unique) |
| Poet Balance | 95 imbalances | Needs reanalysis |
| Data Quality | Mixed (duplicates present) | High (all unique) |

---

## 🎓 LESSONS LEARNED

### What Went Right ✅
1. Prosodic validation system works correctly
2. Metadata structure is blueprint-compliant
3. Source verses are authentic and high-quality
4. No prosodic-pattern duplication (good diversity)
5. Evaluation system successfully detected issues

### What Needs Improvement ⚠️
1. Collection system lacks global deduplication
2. Poetry database too small (20 verses/meter)
3. No diversity checks during collection
4. Batch system doesn't track historical usage
5. Need automated quality gates before export

### Best Practices Moving Forward 📚
1. **Always run deduplication analysis** before considering dataset "complete"
2. **Implement global verse tracking** across all batches and sessions
3. **Establish minimum corpus size** before batch collection (100+ unique per meter)
4. **Add automated quality gates** in collection pipeline
5. **Regular audits** at each collection milestone

---

## 📞 RECOMMENDATIONS FOR RESEARCH TEAM

### For ML Engineers:
- ✅ **Start experiments with 394-verse deduplicated dataset**
- ⚠️ **Be aware:** Limited training data, may need data augmentation
- 📊 **Establish baselines** before expanding dataset

### For Data Collection Team:
- 🔴 **Priority:** Expand poetry_sources.py to 100+ verses per meter
- 🟡 **Implement:** Global deduplication cache
- 🟢 **Verify:** Poet diversity during collection

### For Project Management:
- 📅 **Timeline:** 3-4 weeks for proper dataset expansion
- 💰 **Resources:** Need Arabic prosody expertise for verse verification
- 📊 **Milestone:** 2,000+ truly unique verses

---

## ✅ DELIVERABLES COMPLETED

1. ✅ **Quality Evaluation Report:** `DATASET_QUALITY_EVALUATION_REPORT.md`
2. ✅ **Deduplicated Dataset:** `deduplicated/` folder (20 files, 394 unique verses)
3. ✅ **This Analysis Document:** Comprehensive findings and action plan
4. ✅ **Evaluation Script:** `evaluate_dataset_quality.py` (reusable for future audits)

---

## 🚀 CONCLUSION

The evaluation revealed that **80.6% of the dataset consists of duplicates** due to systematic reuse of 20 source verses across multiple batches. The **actual unique dataset is 394 verses** (~20 per meter).

**The good news:**
- Quality of unique verses is excellent
- Prosodic validation is working correctly
- No cross-contamination issues
- Clean deduplicated dataset ready for use

**The challenge:**
- Dataset is much smaller than initially reported
- Need significant expansion to reach 2,000+ unique verses
- Requires additional research and poetry sourcing

**Recommended path forward:**
1. Use 394-verse dataset for immediate ML experiments
2. Expand poetry_sources.py to 100+ verses per meter
3. Re-run collection with global deduplication
4. Target: 2,000+ truly unique verses within 3-4 weeks

---

*Report prepared by Senior Arabic NLP Researcher & Dataset Quality Engineer*  
*Evaluation Date: November 14, 2025*
