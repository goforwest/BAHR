# Poetry Database Expansion Plan
## Target: 100+ Unique Verses per Meter

**Start Date:** November 14, 2025  
**Target Completion:** December 5, 2025 (3 weeks)  
**Current Status:** 380 verses total (20 per meter)  
**Target:** 2,000+ verses (100+ per meter)  
**Shortfall:** 1,520 verses needed

---

## 📊 CURRENT STATE ANALYSIS

### Verses per Meter (Current)
```
الطويل              : 20 verses → Need 80 more
الكامل              : 20 verses → Need 80 more
الوافر              : 20 verses → Need 80 more
البسيط              : 20 verses → Need 80 more
الرجز               : 20 verses → Need 80 more
الرمل               : 20 verses → Need 80 more
الخفيف              : 20 verses → Need 80 more
السريع              : 20 verses → Need 80 more
المنسرح             : 20 verses → Need 80 more
المقتضب             : 20 verses → Need 80 more
المديد              : 20 verses → Need 80 more
المضارع             : 20 verses → Need 80 more
المتقارب            : 20 verses → Need 80 more
المجتث              : 20 verses → Need 80 more
الهزج               : 20 verses → Need 80 more
الكامل (مجزوء)      : 20 verses → Need 80 more
الهزج (مجزوء)       : 20 verses → Need 80 more
الكامل (3 تفاعيل)   : 20 verses → Need 80 more
السريع (مفعولات)    : 20 verses → Need 80 more
```

**Total Needed:** 1,520 additional unique verses

---

## 🎯 EXPANSION STRATEGY

### Phase 1: Research & Source Identification (Week 1)
**Target:** Identify authenticated sources for 1,520 verses

#### Primary Sources (Public Domain)
1. **الدواوين الشعرية الكلاسيكية (Classical Diwans)**
   - ديوان المتنبي (المتقارب، الكامل، الطويل)
   - ديوان أبو نواس (مختلف البحور)
   - ديوان البحتري (الطويل، الكامل، البسيط)
   - ديوان ابن الرومي (متنوع)
   - ديوان أبو تمام (الطويل، البسيط)
   - ديوان ابن زيدون (الكامل، البسيط)

2. **المعلقات والشعر الجاهلي**
   - المعلقات العشر (already partially included)
   - شعراء المفضليات
   - الأصمعيات

3. **العصر الأموي**
   - جرير (الطويل، الكامل)
   - الفرزدق (الطويل)
   - الأخطل (الطويل، البسيط)
   - عمر بن أبي ربيعة (الخفيف، الكامل)

4. **العصر العباسي**
   - أبو العتاهية (الرجز، الخفيف، الكامل)
   - أبو فراس الحمداني (الطويل، الكامل)
   - ابن المعتز (متنوع)

5. **الشعر الأندلسي**
   - ابن زيدون (الكامل، البسيط)
   - ابن خفاجة (الطويل، الكامل)
   - ابن حمديس (الطويل)

6. **Digital Archives (Public Domain)**
   - مشروع المكتبة الشاملة (Shamela)
   - موسوعة الشعر العربي (aldiwan.net)
   - مكتبة الشعر العربي الكلاسيكي

#### Quality Criteria
- ✅ Authenticated classical sources only
- ✅ Public domain or Creative Commons
- ✅ Prosodically verified (correct tafāʿīl)
- ✅ Complete verses (no fragments)
- ✅ Diverse poet representation (max 5 verses per poet per meter)

---

### Phase 2: Data Collection & Verification (Week 2)
**Target:** Collect and verify 1,520 verses

#### Collection Process

**Step 1: Systematic Extraction**
```python
# For each meter:
# 1. Identify 5-10 major poets known for that meter
# 2. Extract 8-12 verses per poet
# 3. Verify prosodic correctness
# 4. Ensure diversity
```

**Step 2: Prosodic Verification**
- Use existing `analyze_verse()` function from `bahr_api.py`
- Verify each verse matches target meter
- Document any ambiguous cases

**Step 3: Poet Distribution**
- Maximum 5 verses per poet per meter (to maintain 5% threshold)
- Aim for 15-20 different poets per meter
- Prioritize major classical poets

#### Tools Created

1. **`verse_collection_tracker.py`** - Track collection progress
2. **`prosodic_verifier.py`** - Batch verify verses
3. **`poet_distribution_checker.py`** - Ensure balance
4. **`duplicate_checker.py`** - Prevent duplication

---

### Phase 3: Database Integration (Week 3)
**Target:** Integrate and validate 1,520 new verses

#### Integration Process

**Step 1: Expand `poetry_sources.py`**
```python
# For each meter section:
'الطويل': [
    # Existing 20 verses
    {...},
    
    # NEW: Add 80 verified verses
    {
        'text': 'verse_text',
        'poet': 'poet_name',
        'poem': 'poem_title',
        'era': 'era_name',
        'source': 'source_reference'
    },
    # ... (80 more)
]
```

**Step 2: Run Quality Validation**
```bash
# 1. Check for duplicates across all meters
python duplicate_checker.py

# 2. Verify poet distribution
python poet_distribution_checker.py

# 3. Validate prosody
python prosodic_verifier.py

# 4. Run comprehensive evaluation
python evaluate_dataset_quality.py
```

**Step 3: Re-collect Dataset**
```bash
# Clear old batches
rm -rf batches/*.jsonl

# Reset global cache
rm -f global_verse_cache.json

# Collect with expanded database
python batch_collector.py --target 2000

# Verify results
python evaluate_dataset_quality.py
```

---

## 📅 WEEKLY MILESTONES

### Week 1 (Nov 14-20): Research & Planning
- [ ] **Day 1-2:** Identify top 50 poets across all eras
- [ ] **Day 3-4:** Map poets to meters (which poets excel in which meters)
- [ ] **Day 4-5:** Source digital copies of diwans/collections
- [ ] **Day 6-7:** Create extraction tools and verification scripts

**Deliverable:** Database of 50 poets with meter specialties

---

### Week 2 (Nov 21-27): Collection & Verification
- [ ] **Day 1-3:** Extract verses for common meters (الطويل، الكامل، الوافر، البسيط)
- [ ] **Day 4-5:** Extract verses for medium-frequency meters (الخفيف، الرمل، السريع)
- [ ] **Day 6-7:** Extract verses for rare meters (المقتضب، المضارع، الهزج)

**Deliverable:** 1,520 verified verses in staging area

---

### Week 3 (Nov 28 - Dec 5): Integration & Validation
- [ ] **Day 1-2:** Integrate new verses into `poetry_sources.py`
- [ ] **Day 3:** Run comprehensive quality checks
- [ ] **Day 4:** Fix any issues (duplicates, prosody errors, imbalances)
- [ ] **Day 5:** Re-collect full dataset with expanded database
- [ ] **Day 6:** Final validation and evaluation
- [ ] **Day 7:** Documentation and handoff

**Deliverable:** 2,000+ verse dataset with 100+ per meter

---

## 🛠️ TOOLS TO CREATE

### 1. `verse_collection_tracker.py`
**Purpose:** Track collection progress per meter

**Features:**
- Current count per meter
- Target progress (0-100%)
- Poet distribution visualization
- Remaining verses needed

**Usage:**
```bash
python verse_collection_tracker.py --meter الطويل
# Output: الطويل: 45/100 (45%) - Need 55 more verses
```

---

### 2. `prosodic_verifier.py`
**Purpose:** Batch verify verses against target meters

**Features:**
- Load verses from CSV/JSON
- Verify each verse using `analyze_verse()`
- Report mismatches
- Export verified verses

**Usage:**
```bash
python prosodic_verifier.py --input new_verses.csv --meter الطويل
# Output: 80/80 verses verified ✓
```

---

### 3. `poet_distribution_checker.py`
**Purpose:** Ensure no poet exceeds 5% per meter

**Features:**
- Calculate poet percentages
- Flag violations
- Suggest removals if needed
- Generate balance report

**Usage:**
```bash
python poet_distribution_checker.py
# Output: Warning: المتنبي has 8 verses (8%) in الكامل - exceeds 5%
```

---

### 4. `duplicate_checker.py`
**Purpose:** Global deduplication across all meters

**Features:**
- Check against existing verses
- Check against new verses
- Fuzzy matching (90% threshold)
- Generate duplicate report

**Usage:**
```bash
python duplicate_checker.py --new new_verses.json
# Output: Found 3 duplicates - verses removed
```

---

### 5. `batch_integration_script.py`
**Purpose:** Semi-automated integration of verified verses

**Features:**
- Read verified verses from staging
- Format for `poetry_sources.py`
- Insert at correct meter section
- Preserve existing verses
- Validate syntax

**Usage:**
```bash
python batch_integration_script.py --meter الطويل --input verified_tawil.json
# Output: Added 80 verses to الطويل section
```

---

## 📚 METER-SPECIFIC SOURCING STRATEGY

### High-Frequency Meters (Need 80 each)

#### 1. الطويل (Most Common)
**Best Sources:**
- المعلقات السبع (already have some)
- ديوان المتنبي (rich in الطويل)
- ديوان البحتري
- شعر الفرزدق وجرير
- **Target Poets:** امرؤ القيس، المتنبي، البحتري، الفرزدق، جرير، زهير، طرفة، عنترة

#### 2. الكامل (Very Common)
**Best Sources:**
- ديوان البحتري
- ديوان المتنبي
- شعر ابن زيدون
- **Target Poets:** البحتري، المتنبي، ابن زيدون، أبو تمام، أبو نواس

#### 3. الوافر (Common)
**Best Sources:**
- الشعر الجاهلي
- ديوان ابن الرومي
- **Target Poets:** النابغة الذبياني، علقمة الفحل، ابن الرومي

#### 4. البسيط (Common)
**Best Sources:**
- ديوان أبو تمام
- ديوان ابن زيدون
- **Target Poets:** أبو تمام، ابن زيدون، أبو فراس

---

### Medium-Frequency Meters (Need 80 each)

#### 5-7. الخفيف، الرمل، السريع
**Best Sources:**
- ديوان أبو العتاهية (الرجز والخفيف)
- الشعر العباسي
- الموشحات الأندلسية (الرمل)

---

### Rare Meters (Need 80 each)

#### 8-15. المقتضب، المضارع، الهزج، etc.
**Strategy:**
- Search specialized collections
- Focus on عصر العباسي (more experimental)
- May need lower target (60-80 instead of 100)

---

## 🚨 QUALITY CONTROL CHECKPOINTS

### Checkpoint 1: After 500 Verses
- Run `duplicate_checker.py`
- Run `poet_distribution_checker.py`
- Run `prosodic_verifier.py`
- **Decision Point:** Proceed or adjust strategy

### Checkpoint 2: After 1000 Verses
- Run comprehensive evaluation
- Check meter balance (some meters may be harder to source)
- **Decision Point:** Adjust targets for rare meters if needed

### Checkpoint 3: Before Integration
- Final deduplication check
- Final prosodic verification
- Final poet balance check
- **Decision Point:** Go/No-go for integration

---

## 📊 SUCCESS METRICS

### Quantitative
- ✅ **Total verses:** 2,000+ (target: 2,000-2,200)
- ✅ **Per meter:** 100+ (minimum acceptable: 80)
- ✅ **Poet diversity:** 15-20 poets per meter
- ✅ **Max poet percentage:** <5% per poet per meter
- ✅ **Duplication rate:** 0%
- ✅ **Prosodic accuracy:** 100%

### Qualitative
- ✅ All sources authenticated and public domain
- ✅ Classical poets (pre-1900) preferred
- ✅ Complete verses (no fragments)
- ✅ Diverse eras represented
- ✅ High literary quality

---

## 🎯 IMMEDIATE NEXT STEPS (Today)

### Step 1: Create Collection Tools (2 hours)
```bash
cd /Users/hamoudi/Desktop/Personal/BAHR/ml_dataset

# Create tracking and verification tools
python create_collection_tools.py
```

**Creates:**
- `verse_collection_tracker.py`
- `prosodic_verifier.py`
- `poet_distribution_checker.py`
- `duplicate_checker.py`
- `batch_integration_script.py`

### Step 2: Create Staging Area (5 minutes)
```bash
# Create directories for organized collection
mkdir -p expansion_staging/{raw,verified,rejected}
mkdir -p expansion_staging/by_meter
```

### Step 3: Identify Top Sources (1 hour)
- Download or access digital diwans
- Create source reference list
- Document access methods

### Step 4: Start Collection (Rest of Day)
- Begin with الطويل (easiest, most sources)
- Target: 30-40 verses today
- Verify and stage

---

## 📝 DOCUMENTATION

### Files to Maintain
1. **`EXPANSION_LOG.md`** - Daily progress log
2. **`SOURCES_REFERENCE.md`** - Bibliography of all sources used
3. **`POET_CATALOG.md`** - All poets with verse counts
4. **`ISSUES_LOG.md`** - Problems encountered and solutions

---

## ⚠️ RISK MITIGATION

### Risk 1: Insufficient Sources for Rare Meters
**Mitigation:** 
- Lower target to 60-80 for rare meters
- Use variant forms (مجزوء، محذوف)
- Consult specialized collections

### Risk 2: Poet Imbalance
**Mitigation:**
- Monitor distribution daily
- Set hard limit: max 5 verses per poet per meter
- Diversify sources continuously

### Risk 3: Prosodic Errors
**Mitigation:**
- Verify EVERY verse before staging
- Double-check rare meters
- Maintain rejected verse log for learning

### Risk 4: Timeline Slip
**Mitigation:**
- Focus on high-frequency meters first
- Accept lower targets for rare meters if needed
- Parallel processing where possible

---

## 🎓 LEARNING OBJECTIVES

By end of this expansion:
1. Deep understanding of poet-meter relationships
2. Comprehensive knowledge of classical Arabic poetry sources
3. Expertise in prosodic verification
4. Mastery of dataset quality control

---

**Ready to begin?** Let's create the collection tools first! 🚀
