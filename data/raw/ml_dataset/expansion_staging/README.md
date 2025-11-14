# Poetry Database Expansion - Staging Area

**Purpose:** Organize verse collection workflow  
**Status:** Ready for use  
**Target:** 1,520 additional verified verses  

---

## 📁 DIRECTORY STRUCTURE

```
expansion_staging/
├── raw/              # Raw verses from sources (Step 1)
├── verified/         # Prosodically verified verses (Step 2)
├── rejected/         # Verses that failed verification
└── by_meter/         # Final verified verses ready for integration (Step 3)
```

---

## 🔄 WORKFLOW

### Step 1: Raw Collection → `raw/`

**What goes here:** 
- Verses extracted from digital sources
- Not yet verified prosodically
- May contain duplicates
- JSON format

**Example:** `raw/tawil_batch_001.json`

```json
[
  {
    "text": "بِمَ التَّعَلُّلُ لا أَهْلٌ وَلا وَطَنُ",
    "poet": "أبو تمام",
    "poem": "ديوان أبو تمام",
    "era": "Abbasid",
    "source": "aldiwan.net",
    "meter": "الطويل"
  }
]
```

**Command to verify:**
```bash
cd /Users/hamoudi/Desktop/Personal/BAHR/ml_dataset

python prosodic_verifier.py \
  --input expansion_staging/raw/tawil_batch_001.json \
  --meter الطويل \
  --export-verified expansion_staging/verified/tawil_batch_001.json \
  --export-report expansion_staging/verified/tawil_batch_001_report.json
```

---

### Step 2: Prosodic Verification → `verified/`

**What goes here:**
- Verses that passed prosodic verification
- Confirmed to match target meter
- Still may contain duplicates
- JSON format

**Example:** `verified/tawil_batch_001.json`

**Command to check duplicates:**
```bash
python duplicate_checker.py \
  --new expansion_staging/verified/tawil_batch_001.json \
  --export-clean expansion_staging/by_meter/tawil_clean_001.json
```

---

### Step 3: Final Clean Verses → `by_meter/`

**What goes here:**
- Prosodically verified ✅
- No duplicates ✅
- Ready for integration into poetry_sources.py
- Organized by meter
- JSON format

**Example:** `by_meter/tawil_clean_001.json`

**These are your gold standard verses ready for database integration!**

---

### Rejected Verses → `rejected/`

**What goes here:**
- Verses that failed prosodic verification
- Duplicates (for reference)
- Verses with errors

**Keep for reference and learning.**

---

## 📋 NAMING CONVENTIONS

### Raw Files
```
raw/
├── tawil_batch_001.json
├── tawil_batch_002.json
├── kamil_batch_001.json
├── wafir_batch_001.json
└── ...
```

### Verified Files
```
verified/
├── tawil_batch_001.json
├── tawil_batch_001_report.json  # Verification report
├── tawil_batch_002.json
├── kamil_batch_001.json
└── ...
```

### Clean Final Files
```
by_meter/
├── tawil_clean_001.json    # 30 verses
├── tawil_clean_002.json    # 30 verses
├── tawil_clean_003.json    # 20 verses (total 80)
├── kamil_clean_001.json
└── ...
```

---

## 🎯 DAILY WORKFLOW

### Morning: Raw Collection
1. Choose meter to work on
2. Extract verses from sources
3. Save to `raw/METER_batch_XXX.json`
4. Target: 30-40 verses per batch

### Afternoon: Verification
1. Run prosodic verifier on raw batches
2. Review verification report
3. Move verified verses to `verified/`
4. Move rejected verses to `rejected/` with notes

### Evening: Final Cleaning
1. Run duplicate checker on verified batches
2. Export clean verses to `by_meter/`
3. Update progress tracker
4. Log progress in EXPANSION_LOG.md

---

## 🛠️ USEFUL COMMANDS

### Quick Status Check
```bash
# Count raw verses
find raw -name "*.json" -exec wc -l {} + | tail -1

# Count verified verses
find verified -name "*.json" ! -name "*_report.json" -exec wc -l {} + | tail -1

# Count clean final verses
find by_meter -name "*.json" -exec wc -l {} + | tail -1
```

### Batch Process Multiple Files
```bash
# Verify all raw files for a specific meter
for file in raw/tawil_batch_*.json; do
    base=$(basename "$file" .json)
    python ../prosodic_verifier.py \
        --input "$file" \
        --meter الطويل \
        --export-verified "verified/${base}.json"
done
```

---

## 📊 PROGRESS TRACKING

### By Meter Status
```bash
# Count verses per meter in by_meter/
for meter in tawil kamil wafir basit; do
    count=$(find by_meter -name "${meter}_*.json" -exec cat {} \; | grep -c '"text"')
    echo "$meter: $count verses"
done
```

---

## ⚠️ IMPORTANT NOTES

### Before Integration
- ✅ All verses must be in `by_meter/` folder
- ✅ Run final duplicate check across all meters
- ✅ Verify poet distribution
- ✅ Ensure 100% prosodic accuracy

### Backup Policy
- Keep `raw/` files even after verification (source of truth)
- Keep verification reports for audit trail
- Don't delete rejected verses (learning reference)

### Quality Gates
- Every verse in `by_meter/` has passed:
  1. Prosodic verification (100% meter match)
  2. Duplicate check (0% duplication)
  3. Source authentication (documented origin)

---

## 🗂️ FILE ORGANIZATION TIPS

### As You Collect
```bash
# Create dated batches
raw/tawil_batch_2025_11_14.json
raw/tawil_batch_2025_11_15.json

# Or numbered sequentially
raw/tawil_batch_001.json
raw/tawil_batch_002.json
```

### Keep It Organized
- One meter at a time
- Batch sizes: 20-40 verses
- Clear naming
- Document sources in filename or metadata

---

## 📈 METRICS TO TRACK

### Weekly Totals
```bash
# Total verses in by_meter/
find by_meter -name "*.json" -exec cat {} \; | grep -c '"text"'

# Verification success rate
# (verified / raw) × 100
```

### Quality Metrics
- Prosodic accuracy: Should be 100%
- Duplication rate: Should be 0%
- Poet diversity: Track in EXPANSION_LOG.md

---

## 🎉 MILESTONES

- [ ] First batch verified (30 verses)
- [ ] First meter complete (80 verses)
- [ ] 250 verses collected (1/6 complete)
- [ ] 500 verses collected (1/3 complete)
- [ ] 750 verses collected (1/2 complete)
- [ ] 1,000 verses collected (2/3 complete)
- [ ] 1,250 verses collected (5/6 complete)
- [ ] 1,520 verses collected ✅ TARGET ACHIEVED

---

## 📞 QUICK REFERENCE

### Essential Commands
```bash
# Verify batch
python ../prosodic_verifier.py --input raw/FILE.json --meter METER --export-verified verified/FILE.json

# Check duplicates
python ../duplicate_checker.py --new verified/FILE.json --export-clean by_meter/FILE_clean.json

# Track progress
python ../verse_collection_tracker.py

# Check poet balance
python ../poet_distribution_checker.py --meter METER
```

### Directory Navigation
```bash
cd /Users/hamoudi/Desktop/Personal/BAHR/ml_dataset/expansion_staging

# See what's in each stage
ls -lh raw/
ls -lh verified/
ls -lh by_meter/
ls -lh rejected/
```

---

**Remember:** Quality over quantity! Every verse in `by_meter/` is gold. 🌟
