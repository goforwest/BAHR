# Poetry Database Expansion - Getting Started Guide

**Status:** Ready to begin collection  
**Target:** 1,520 additional verses (80 per meter × 19 meters)  
**Current:** 380 verses (20 per meter)  
**Timeline:** 3 weeks

---

## ✅ SETUP COMPLETE

### Tools Created
- ✅ `verse_collection_tracker.py` - Track progress
- ✅ `prosodic_verifier.py` - Verify verses prosodically
- ✅ `poet_distribution_checker.py` - Check poet balance
- ✅ `duplicate_checker.py` - Prevent duplication

### Staging Areas Created
```
expansion_staging/
├── raw/           # Raw verses from sources (before verification)
├── verified/      # Verses that passed prosodic verification
├── rejected/      # Verses that failed verification
└── by_meter/      # Verified verses organized by meter
```

---

## 📚 RECOMMENDED SOURCES (Public Domain)

### 1. Digital Archives (Free Access)

**الديوان - موسوعة الشعر العربي**
- URL: https://www.aldiwan.net
- Coverage: 1000+ classical poets
- Format: Web scraping needed
- Quality: High, authenticated sources

**المكتبة الشاملة (Shamela)**
- Coverage: Complete classical diwans
- Format: Downloadable databases
- Quality: Very high, scholarly editions

**مشروع الموسوعة الشعرية**
- Coverage: Major classical poets
- Format: Structured database
- Quality: High

### 2. Major Poets by Meter

#### For الطويل (80 needed):
1. **امرؤ القيس** - ديوان امرئ القيس (20-30 verses available)
2. **المتنبي** - ديوان المتنبي (30-40 verses in الطويل)
3. **البحتري** - ديوان البحتري (20-30 verses)
4. **الفرزدق** - ديوان الفرزدق (10-15 verses)
5. **جرير** - ديوان جرير (10-15 verses)

**Total potential:** 90-130 verses → Select best 80

#### For الكامل (80 needed):
1. **البحتري** - Specializes in الكامل (40-50 verses)
2. **ابن زيدون** - ديوان ابن زيدون (15-20 verses)
3. **أبو تمام** - ديوان أبو تمام (15-20 verses)
4. **المتنبي** - ديوان المتنبي (10-15 verses)

**Total potential:** 80-105 verses → Select best 80

#### For الوافر (80 needed):
1. **النابغة الذبياني** - Famous for الوافر (25-30 verses)
2. **علقمة الفحل** - ديوان علقمة (15-20 verses)
3. **ابن الرومي** - ديوان ابن الرومي (20-25 verses)
4. **أبو نواس** - ديوان أبو نواس (10-15 verses)

**Total potential:** 70-90 verses → Need creative sourcing

---

## 🔄 COLLECTION WORKFLOW

### Step 1: Source Selection (Daily Target: 30-40 verses)

1. **Choose a meter** (start with الطويل - easiest)
2. **Identify 3-4 poets** who excel in that meter
3. **Access their diwans** (digital or physical)
4. **Extract 8-12 verses** per poet

### Step 2: Raw Collection

**Create JSON file:** `expansion_staging/raw/tawil_batch_001.json`

```json
[
  {
    "text": "بِمَ التَّعَلُّلُ لا أَهْلٌ وَلا وَطَنُ",
    "poet": "أبو تمام",
    "poem": "ديوان أبو تمام",
    "era": "Abbasid",
    "source": "aldiwan.net",
    "meter": "الطويل"
  },
  {
    "text": "next verse here...",
    "poet": "poet name",
    ...
  }
]
```

### Step 3: Prosodic Verification

```bash
cd /Users/hamoudi/Desktop/Personal/BAHR/ml_dataset

# Verify verses
python prosodic_verifier.py \
  --input expansion_staging/raw/tawil_batch_001.json \
  --meter الطويل \
  --export-verified expansion_staging/verified/tawil_batch_001.json \
  --export-report expansion_staging/verified/tawil_batch_001_report.json
```

**Expected output:**
```
Loading verses from expansion_staging/raw/tawil_batch_001.json...
✅ Loaded 30 verses
Verifying verses...
Processed 30/30 verses...

======================================================================
PROSODIC VERIFICATION REPORT
======================================================================
Total verses:   30
✅ Valid:       28 (93.3%)
❌ Invalid:     2 (6.7%)
⚠️  Errors:      0 (0.0%)
======================================================================

✅ Exported 28 verified verses to expansion_staging/verified/tawil_batch_001.json
```

### Step 4: Duplicate Check

```bash
# Check against existing database
python duplicate_checker.py \
  --new expansion_staging/verified/tawil_batch_001.json \
  --export-clean expansion_staging/by_meter/tawil_verified.json
```

**Expected output:**
```
Loading new verses from expansion_staging/verified/tawil_batch_001.json...
✅ Loaded 28 new verses
Loading existing poetry database...
✅ Loaded 380 existing verses

Checking for duplicates...

======================================================================
DUPLICATE DETECTION REPORT
======================================================================
Exact duplicates:    0
Fuzzy duplicates:    0
Internal duplicates: 0
Total issues:        0
======================================================================

✅ No duplicates found - all verses are unique!

Removed 0 duplicate verses
✅ Exported 28 clean verses to expansion_staging/by_meter/tawil_verified.json
```

### Step 5: Poet Balance Check

```bash
# Simulate adding these verses to الطويل
python poet_distribution_checker.py --meter الطويل
```

### Step 6: Track Progress

```bash
# See overall progress
python verse_collection_tracker.py

# See specific meter
python verse_collection_tracker.py --meter الطويل

# Export progress data
python verse_collection_tracker.py --export expansion_progress.json
```

---

## 📊 DAILY ROUTINE

### Morning (1-2 hours)
1. Check progress: `python verse_collection_tracker.py`
2. Select meter to work on (rotate through meters)
3. Identify 2-3 poets for that meter
4. Access their diwans

### Afternoon (2-3 hours)
1. Extract 30-40 verses into JSON file
2. Run prosodic verification
3. Run duplicate check
4. Move verified verses to `by_meter/` folder

### Evening (30 minutes)
1. Update progress tracker
2. Log any issues in `EXPANSION_LOG.md`
3. Plan next day's work

### Weekly Review (Friday)
1. Run comprehensive checks on week's collection
2. Review poet distribution across all meters
3. Adjust strategy if needed

---

## 📝 VERSE COLLECTION TEMPLATE

Save this as `verse_template.json` for quick copying:

```json
[
  {
    "text": "VERSE_TEXT_HERE",
    "poet": "POET_NAME",
    "poem": "POEM_OR_DIWAN_NAME",
    "era": "pre-Islamic|Umayyad|Abbasid|Andalusian|etc",
    "source": "SOURCE_REFERENCE",
    "meter": "METER_NAME"
  }
]
```

**Required fields:**
- `text` - Full verse text (with diacritics if available)
- `poet` - Poet's name in Arabic
- `poem` - Source poem or diwan name
- `era` - Historical era
- `source` - Where you found it
- `meter` - Target meter for verification

---

## 🎯 WEEK 1 TARGETS

### Day 1 (Today): الطويل
- Target: 30 verses
- Poets: المتنبي، البحتري، أبو تمام
- Goal: Get comfortable with workflow

### Day 2: الطويل (continued)
- Target: 30 verses
- Poets: امرؤ القيس، زهير، طرفة
- Goal: Reach 60/80 for الطويل

### Day 3: الطويل (finish) + الكامل (start)
- Target: 20 (الطويل) + 20 (الكامل)
- Complete الطويل ✅
- Start الكامل with البحتري

### Day 4: الكامل
- Target: 40 verses
- Poets: ابن زيدون، أبو تمام، المتنبي

### Day 5: الكامل (finish) + الوافر (start)
- Target: 20 (الكامل) + 20 (الوافر)
- Complete الكامل ✅
- Start الوافر

### Day 6-7: الوافر + البسيط
- Target: 60 verses (finish الوافر, start البسيط)
- End of Week 1: 260 verses collected ✅

---

## ⚠️ QUALITY CHECKLIST

Before considering a batch "done":

- [ ] All verses prosodically verified (100% valid)
- [ ] No duplicates (exact or fuzzy)
- [ ] No poet exceeds 5% in that meter
- [ ] All required fields present
- [ ] Sources documented
- [ ] Moved to `by_meter/` folder
- [ ] Progress tracker updated

---

## 🚨 COMMON ISSUES & SOLUTIONS

### Issue: Prosodic verification fails
**Solution:** 
- Double-check verse text for typos
- Verify meter is correct (may be different meter)
- Check for missing/extra words
- Move to `rejected/` folder with reason

### Issue: Too many verses from one poet
**Solution:**
- Select only 5 best verses from that poet
- Find more poets who write in that meter
- Use poet distribution checker to monitor

### Issue: Can't find enough verses for rare meter
**Solution:**
- Lower target to 60 verses for that meter
- Search for variant forms (مجزوء، محذوف)
- Consult specialized collections
- Flag for review in EXPANSION_LOG.md

---

## 📈 PROGRESS TRACKING

Use these commands regularly:

```bash
# Quick status
python verse_collection_tracker.py

# Detailed meter view
python verse_collection_tracker.py --meter الطويل

# Check poet balance
python poet_distribution_checker.py

# Export progress
python verse_collection_tracker.py --export progress.json
```

---

## 🎓 TIPS FOR SUCCESS

1. **Start with common meters** (الطويل، الكامل، الوافر) - more sources available
2. **Batch collect by poet** - easier to extract 10 verses from one diwan than 1 from 10 diwans
3. **Verify early and often** - don't collect 100 verses before verifying
4. **Document sources** - you may need to go back
5. **Take breaks** - quality over speed
6. **Rotate meters** - prevents burnout
7. **Celebrate milestones** - each completed meter is an achievement!

---

## 📞 READY TO START?

### Immediate Next Steps:

1. **Choose starting meter:** الطويل (recommended)
2. **Access a diwan:** Start with المتنبي (abundant in الطويل)
3. **Extract 10-15 verses** into `raw/tawil_batch_001.json`
4. **Run verification:** `python prosodic_verifier.py ...`
5. **Check duplicates:** `python duplicate_checker.py ...`
6. **Update tracker:** `python verse_collection_tracker.py`

### First Command:

```bash
cd /Users/hamoudi/Desktop/Personal/BAHR/ml_dataset

# Create your first batch file
touch expansion_staging/raw/tawil_batch_001.json

# Open in VS Code and start adding verses!
code expansion_staging/raw/tawil_batch_001.json
```

---

**Let's build a world-class Arabic prosody dataset! 🚀**
