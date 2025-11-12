# Evaluation Protocol for 100% Meter Detection Accuracy

**Version:** 1.0
**Date:** 2025-11-12
**Purpose:** Define comprehensive testing protocol to certify 100% accuracy across all 20 Arabic meters
**Scope:** From current 19/20 meters (95%) to complete 20/20 coverage (100%)

---

## 🎯 Executive Summary

**Current Status:**
- ✅ 182 verses tested (v0.102 golden set)
- ✅ 100% accuracy on 19/20 meters
- ❌ المتدارك: 0 test verses (blind spot)

**Target Status:**
- 🎯 200+ verses tested (expanded golden set)
- 🎯 100% accuracy on 20/20 meters
- 🎯 المتدارك: 15 test verses minimum
- 🎯 External expert validation
- 🎯 Published certification report

**Evaluation Philosophy:**
> **"Not merely 100% on tested verses, but provable confidence that all 20 meters are comprehensively covered with representative samples across difficulty levels and variants."**

---

## 📊 Evaluation Framework

### 1. Multi-Dimensional Accuracy Metrics

**Primary Metrics (MUST achieve 100%):**
1. **Per-Meter Accuracy**
   - Calculation: `correct_detections_per_meter / total_verses_per_meter`
   - Requirement: 100% for EACH of 20 meters independently
   - No averaging allowed

2. **Overall Accuracy**
   - Calculation: `total_correct / total_verses`
   - Requirement: 100% (200/200 or higher)

3. **Confusion Matrix Purity**
   - All off-diagonal elements MUST be 0
   - No misclassifications between any meter pairs

**Secondary Metrics (Diagnostic):**
4. **Macro F1-Score**
   - Unweighted average F1 across all 20 meters
   - Ensures rare meters aren't penalized
   - Target: 1.00

5. **Weighted F1-Score**
   - Weighted by meter frequency in classical poetry
   - Should also be 1.00 given primary metrics

6. **Confidence Calibration**
   - Mean confidence: ≥ 0.90
   - Minimum confidence: ≥ 0.80
   - Confidence-accuracy correlation: ≥ 0.95

---

### 2. Coverage Requirements

**Minimum Test Set Size Per Meter:**

| Meter Tier | Frequency | Min Verses | Recommended | Rationale |
|------------|-----------|------------|-------------|-----------|
| **Tier 1** (9 meters) | 85% of poetry | 10 | 15-30 | High coverage needed for common cases |
| **Tier 2** (2 meters) | 10% of poetry | 8 | 10-15 | Adequate variant coverage |
| **Tier 3** (5 meters) | 5% of poetry | 10 | 15 | Higher per-meter to cover edge cases |
| **Variants** (4 forms) | Variable | 5 | 5-10 | Sufficient for variant validation |

**المتدارك Specific:**
- **Minimum:** 15 verses (higher than typical Tier 3 due to historical gaps)
- **Distribution:**
  - Canonical: 5 verses
  - With khabn: 4 verses
  - With ḥadhf: 3 verses
  - With qaṣr: 2 verses
  - Edge cases: 1 verse
- **Difficulty:**
  - Easy: 3 (20%)
  - Medium: 6 (40%)
  - Hard: 6 (40%)

---

### 3. Stratified Testing Protocol

#### 3.1 Difficulty Stratification

**Tier 1 - Easy (Target: 20% of test set)**
- Canonical forms (no ziḥāfāt or ʿilal)
- Clear, unambiguous meter patterns
- High-confidence detections expected (≥ 0.95)

**Tier 2 - Medium (Target: 50% of test set)**
- 1-2 ziḥāfāt applied
- Common variants
- Standard classical poetry
- Confidence: 0.85-0.95

**Tier 3 - Hard (Target: 30% of test set)**
- 3+ ziḥāfāt applied
- Rare ʿilal combinations
- Boundary cases with other meters
- Ambiguous contexts
- Confidence: 0.80-0.90

**Rationale:**
- Real-world poetry is NOT all "easy" - must handle complexity
- Hard cases prevent overfitting to simple patterns
- 30% hard cases ensures robustness

---

#### 3.2 Variant Coverage

**Required Variants Per Meter:**
Each meter must have examples of:
1. Base canonical form (صحيح)
2. Common ziḥāfāt variants (at least 2 types)
3. Common ʿilal variants (at least 2 types)
4. Combined transformations (ziḥāf + ʿilal)

**Example - الطويل:**
- ✅ Canonical: فعولن مفاعيلن (×4)
- ✅ With qabd: فعولن مفاعلن
- ✅ With kaff: فعول مفاعيلن
- ✅ With ḥadhf: فعولن مفاعي (final)
- ✅ Combined: فعول مفاعلن مفاعي (qabd + kaff + ḥadhf)

---

#### 3.3 Confusion Matrix Testing

**High-Risk Pairs (MUST test explicitly):**

| Meter 1 | Meter 2 | Confusion Risk | Required Boundary Tests |
|---------|---------|----------------|-------------------------|
| **المتدارك** | **المتقارب** | **CRITICAL** | 5+ verses at exact boundary |
| **المتدارك** | **الرجز** | **HIGH** | 4+ verses differentiating |
| **الكامل** | **الرجز** | MEDIUM | 3+ verses |
| **البسيط** | **المديد** | MEDIUM | 3+ verses |
| **السريع** | **المنسرح** | LOW | 2+ verses |

**Boundary Test Protocol:**
1. Create verses that COULD match both meters
2. Verify detector chooses correct meter
3. Document distinguishing features
4. Confidence for correct meter must be > incorrect meter
5. Example: If verse is المتدارك, detector must return:
   - المتدارك: 0.92 confidence (1st)
   - المتقارب: 0.45 confidence (2nd or lower)

---

### 4. Test Set Composition

#### 4.1 Current Golden Set (v0.102)

```
Total verses: 182
Meters covered: 19/20 (95%)
Missing: المتدارك (0 verses)

Distribution:
- Tier 1 meters: 150 verses (82%)
- Tier 2 meters: 11 verses (6%)
- Tier 3 meters: 13 verses (7%)
- Variants: 8 verses (4%)
```

**Gap Analysis:**
- ❌ المتدارك: Completely missing
- ⚠️ السريع: Only 1 verse (need 9 more)
- ⚠️ المديد: Only 1 verse (need 7 more)
- ⚠️ Tier 3 meters: Under-represented (need 40+ more)

---

#### 4.2 Target Golden Set (v0.103+)

```
Total verses: 250 (target)
Meters covered: 20/20 (100%)

Additions needed:
+ 15 المتدارك verses (PRIORITY)
+  9 السريع verses
+  7 المديد verses
+  5 المنسرح verses
+  2 المجتث verses
+  2 المقتضب verses
+  2 المضارع verses
+  5 Variant expansions
+  5 Boundary confusion tests
= ~52 verses minimum
```

**Recommended: 250 verses total (182 + 68 new)**
- Provides buffer for edge cases
- Comprehensive variant coverage
- Statistical confidence

---

### 5. Evaluation Execution Protocol

#### 5.1 Testing Workflow

```
┌─────────────────────────────────────┐
│ 1. GOLDEN SET PREPARATION           │
│    - Finalize 15 المتدارك verses   │
│    - Add to golden_set_v0_103.jsonl │
│    - Validate schema compliance     │
└─────────┬───────────────────────────┘
          ↓
┌─────────────────────────────────────┐
│ 2. PRE-TEST VALIDATION              │
│    - Run schema validator           │
│    - Check for duplicates           │
│    - Verify taqṭīʿ annotations      │
│    - Ensure all metadata present    │
└─────────┬───────────────────────────┘
          ↓
┌─────────────────────────────────────┐
│ 3. AUTOMATED EVALUATION             │
│    - Run: test_golden_set_v2.py     │
│    - Detector: BahrDetectorV2       │
│    - Record all results             │
│    - Generate confusion matrix      │
└─────────┬───────────────────────────┘
          ↓
┌─────────────────────────────────────┐
│ 4. RESULTS ANALYSIS                 │
│    - Per-meter accuracy             │
│    - Overall accuracy               │
│    - Confidence distributions       │
│    - Failure analysis (if any)      │
└─────────┬───────────────────────────┘
          ↓
┌─────────────────────────────────────┐
│ 5. EXPERT VALIDATION (Blind)        │
│    - 2+ external prosodists         │
│    - Annotate same test set         │
│    - Compare with detector output   │
│    - Calculate inter-rater κ        │
└─────────┬───────────────────────────┘
          ↓
┌─────────────────────────────────────┐
│ 6. STATISTICAL VALIDATION           │
│    - Chi-square test (no meter bias)│
│    - Bootstrap confidence intervals │
│    - Cross-validation (if applicable)│
└─────────┬───────────────────────────┘
          ↓
┌─────────────────────────────────────┐
│ 7. CERTIFICATION REPORT             │
│    - Document all metrics           │
│    - Expert attestations            │
│    - Methodology description        │
│    - Dataset publication            │
└─────────────────────────────────────┘
```

---

#### 5.2 Evaluation Script Enhancement

**Current:** `test_golden_set_v2.py`
**Enhancements Needed:**

1. **Confusion Matrix Generation**
```python
def generate_confusion_matrix(results):
    """
    Create 20×20 confusion matrix
    Rows: True meter
    Cols: Detected meter
    All off-diagonal elements MUST be 0 for certification
    """
    # Implementation
```

2. **Per-Meter Detailed Report**
```python
def generate_meter_report(meter_id, results):
    """
    Detailed report for each meter:
    - Accuracy (must be 100%)
    - Verse count and difficulty distribution
    - Confidence statistics (mean, min, max, std)
    - Variant coverage
    - Edge case results
    """
    # Implementation
```

3. **Statistical Tests**
```python
def chi_square_meter_bias_test(results):
    """
    Test null hypothesis: No significant difference in
    accuracy across meters (should NOT reject - all meters equal)
    """
    # Implementation

def bootstrap_confidence_intervals(results, n_iterations=10000):
    """
    Calculate 95% CI for overall accuracy
    Target: [99.5%, 100%] for 250 verses
    """
    # Implementation
```

4. **Certification Checklist**
```python
def certification_checklist(results):
    """
    Auto-generate pass/fail checklist:
    [ ] Overall accuracy = 100%
    [ ] Per-meter accuracy = 100% (all 20 meters)
    [ ] Confusion matrix diagonal (no off-diagonal)
    [ ] Mean confidence ≥ 0.90
    [ ] Min confidence ≥ 0.80
    [ ] All meters have ≥ min verses
    [ ] Expert validation κ ≥ 0.85
    [ ] No statistical meter bias
    """
    # Implementation
```

---

### 6. Expert Validation Protocol

#### 6.1 External Expert Review

**Purpose:** Independent verification that detector accuracy is genuine, not overfitted

**Protocol:**
1. **Recruit 2-3 prosody experts** NOT involved in golden set creation
2. **Blind annotation:** Provide verses WITHOUT gold labels or detector outputs
3. **Independent work:** Experts don't see each other's annotations initially
4. **Consensus meeting:** Resolve disagreements for final labels
5. **Comparison:** Calculate agreement between experts and detector

**Metrics:**
- **Inter-expert agreement (κ):** ≥ 0.85 (shows test set is reliable)
- **Detector-expert agreement (κ):** ≥ 0.90 (shows detector matches experts)
- **Disagreement analysis:** Document ALL cases where detector ≠ expert consensus

**Acceptance Criteria:**
- If κ(detector, experts) ≥ 0.90 AND detector accuracy = 100%: ✅ PASS
- If κ < 0.90: Investigate disagreements; may indicate test set issues
- If detector wrong but experts agree: 🐛 BUG in detector
- If experts disagree (κ < 0.85): ⚠️ Verse is ambiguous; may need removal

---

#### 6.2 Expert Attestation Form

**Required for certification:**

```
EXPERT VALIDATION ATTESTATION

I, [Expert Name], [Credentials], hereby attest that:

1. I have independently reviewed [N] verses from the BAHR golden set
2. I have compared my prosodic analysis with the BahrDetectorV2 output
3. The detector achieved [X]% agreement with my expert annotations
4. I have reviewed all disagreement cases and confirm:
   - [ ] Detector was correct, I made an error
   - [ ] Detector was incorrect (documented in error report)
   - [ ] Verse is genuinely ambiguous (documented)
5. To the best of my professional judgment, the BAHR detector demonstrates
   gold-standard accuracy on Arabic meter detection across all 20 classical meters

Specifically for المتدارك:
6. I have reviewed [N] المتدارك verses in the test set
7. All [N] verses are authentic المتدارك (not misclassified other meters)
8. The detector correctly identified [N/N = 100%] of these verses

Date: _______________
Signature: _______________
Affiliation: _______________
```

**Minimum:** 2 signed attestations required for certification

---

### 7. Certification Criteria

#### 7.1 Technical Requirements (All MUST Pass)

| # | Criterion | Threshold | Status |
|---|-----------|-----------|--------|
| 1 | Overall accuracy | 100% (no errors) | ⬜ |
| 2 | Per-meter accuracy | 100% on each of 20 meters | ⬜ |
| 3 | Confusion matrix | All off-diagonal = 0 | ⬜ |
| 4 | Mean confidence | ≥ 0.90 | ⬜ |
| 5 | Min confidence | ≥ 0.80 | ⬜ |
| 6 | Test set size | ≥ 200 verses | ⬜ |
| 7 | المتدارك coverage | ≥ 15 verses | ⬜ |
| 8 | All meters coverage | ≥ 5 verses each | ⬜ |
| 9 | Difficulty distribution | 20% easy, 50% medium, 30% hard | ⬜ |
| 10 | Variant coverage | All major variants tested | ⬜ |

#### 7.2 Validation Requirements (All MUST Pass)

| # | Criterion | Threshold | Status |
|---|-----------|-----------|--------|
| 11 | Inter-annotator κ (experts) | ≥ 0.85 | ⬜ |
| 12 | Detector-expert κ | ≥ 0.90 | ⬜ |
| 13 | Expert attestations | ≥ 2 signed | ⬜ |
| 14 | المتدارك expert validation | ≥ 2 prosodists confirm all 15 verses | ⬜ |
| 15 | External blind review | ≥ 1 independent review | ⬜ |

#### 7.3 Documentation Requirements (All MUST Be Complete)

| # | Deliverable | Status |
|---|-------------|--------|
| 16 | Test methodology document | ⬜ |
| 17 | Golden set with full metadata (JSONL) | ⬜ |
| 18 | Evaluation results report (JSON + PDF) | ⬜ |
| 19 | Confusion matrix visualization | ⬜ |
| 20 | Expert attestation forms (signed) | ⬜ |
| 21 | Statistical analysis report | ⬜ |
| 22 | Reproducible test harness (code) | ⬜ |
| 23 | Dataset publication (Zenodo/HuggingFace) | ⬜ |

**Certification Status:** ✅ CERTIFIED only when ALL 23 criteria are met

---

### 8. Reporting & Documentation

#### 8.1 Evaluation Report Structure

**File:** `BAHR_100_PERCENT_CERTIFICATION_REPORT.pdf`

**Sections:**

```
1. EXECUTIVE SUMMARY
   - Current accuracy: 100%
   - Meters tested: 20/20
   - Total verses: [N]
   - Certification date
   - Certifying experts

2. METHODOLOGY
   - Test set construction
   - Stratified sampling approach
   - Validation protocols
   - Expert review process

3. RESULTS
   3.1 Overall Metrics
       - Accuracy: 100%
       - Macro F1: 1.00
       - Weighted F1: 1.00
   3.2 Per-Meter Results
       - Table: 20 rows, each meter 100%
   3.3 Confusion Matrix
       - 20×20 matrix (all off-diagonal = 0)
   3.4 Confidence Analysis
       - Distribution plots
       - Statistics per meter

4. المتدارك VALIDATION (Special Section)
   4.1 Historical Context
   4.2 Corpus Sourcing
   4.3 Expert Validation
   4.4 Disambiguation from المتقارب/الرجز
   4.5 Results: 15/15 correct (100%)

5. EXPERT VALIDATION
   5.1 Expert Qualifications
   5.2 Blind Annotation Protocol
   5.3 Inter-Annotator Agreement (κ = X.XX)
   5.4 Detector-Expert Agreement (κ = X.XX)
   5.5 Attestation Letters (Appendix)

6. STATISTICAL ANALYSIS
   6.1 Chi-Square Test (no meter bias)
   6.2 Bootstrap Confidence Intervals
   6.3 Cross-Validation Results (if applicable)

7. DATASET DESCRIPTION
   7.1 Composition by Meter
   7.2 Composition by Difficulty
   7.3 Composition by Era
   7.4 Variant Coverage
   7.5 Source Distribution

8. REPRODUCIBILITY
   8.1 Test Harness Usage
   8.2 Dataset Access (Zenodo DOI)
   8.3 Code Repository (GitHub)
   8.4 Dependencies and Versions

9. LIMITATIONS & FUTURE WORK
   9.1 Current Scope
   9.2 Out-of-Scope Patterns
   9.3 Recommendations for Extensions

10. CERTIFICATION STATEMENT
    "The BAHR detection engine (BahrDetectorV2) has achieved
     gold-standard accuracy on all 20 classical Arabic meters
     as validated by independent expert prosodists and comprehensive
     testing protocols."

11. APPENDICES
    A. Complete Test Set (JSONL)
    B. Expert Attestation Forms
    C. Confusion Matrix (Full)
    D. Per-Verse Results
    E. Statistical Test Output
```

---

#### 8.2 Dataset Publication

**Platform:** Zenodo (DOI registration) + HuggingFace (accessibility)

**Files to Publish:**
1. `golden_set_v0_103_complete.jsonl` - Full test set
2. `golden_set_schema.json` - Data schema
3. `golden_set_metadata.json` - Statistics
4. `BAHR_100_PERCENT_CERTIFICATION_REPORT.pdf` - Full report
5. `test_golden_set_v2.py` - Evaluation script
6. `evaluation_results.json` - Raw results
7. `confusion_matrix.csv` - Confusion matrix data
8. `README.md` - Dataset documentation

**License:** CC BY-SA 4.0 (allows academic use with attribution)

**Citation:**
```bibtex
@dataset{bahr_golden_set_2025,
  author = {BAHR Detection Engine Team},
  title = {Gold-Standard Arabic Poetry Meter Test Set: 20 Meters},
  year = {2025},
  publisher = {Zenodo},
  doi = {10.5281/zenodo.XXXXXXX},
  url = {https://doi.org/10.5281/zenodo.XXXXXXX}
}
```

---

### 9. Failure Response Protocol

**IF any criterion is NOT met:**

#### 9.1 Accuracy < 100%

**Response:**
1. **Identify failures:** Which verses were misclassified?
2. **Root cause analysis:**
   - Detector bug?
   - Incorrect gold label?
   - Genuinely ambiguous verse?
3. **Categorize errors:**
   - Type 1: Detector error → Fix detection logic
   - Type 2: Gold label error → Correct annotation, re-test
   - Type 3: Ambiguous verse → Remove from golden set OR resolve with expert panel
4. **Re-test after fixes**
5. **Document all changes**

---

#### 9.2 Low Expert Agreement (κ < 0.85)

**Response:**
1. **Calibration session:** Convene experts to discuss disagreements
2. **Reference materials:** Provide classical prosody references
3. **Consensus building:** Resolve ambiguous cases
4. **Verse quality review:** Remove genuinely ambiguous verses
5. **Re-annotation:** Repeat with calibrated experts
6. **Accept:** κ ≥ 0.85 OR acknowledge limitations in ambiguous cases

---

#### 9.3 Insufficient Coverage

**Response:**
1. **Identify gaps:** Which meters/variants/difficulty levels under-represented?
2. **Targeted sourcing:** Use MUTADARIK_CORPUS_SOURCING_GUIDE.md
3. **Add verses:** Expand golden set
4. **Re-test:** Full evaluation with expanded set

---

### 10. Timeline & Milestones

| Week | Milestone | Deliverable |
|------|-----------|-------------|
| 1-2 | المتدارك corpus sourcing | 20 candidate verses |
| 3-4 | Expert annotation & validation | 15 verified المتدارك verses |
| 5 | Golden set expansion | v0.103 with 200+ verses |
| 6 | Automated evaluation | Full test run, results analysis |
| 7 | Expert blind validation | External review, attestations |
| 8 | Statistical analysis | Chi-square, bootstrap, reports |
| 9 | Documentation | Certification report draft |
| 10 | Peer review | External feedback, revisions |
| 11 | Dataset publication | Zenodo/HuggingFace upload |
| 12 | Certification | Final sign-off, announcement |

**Total:** ~12 weeks from start to certification

---

## ✅ Success Indicators

**We will have achieved 100% certification when:**

1. ✅ BahrDetectorV2 correctly classifies ALL 200+ verses (100%)
2. ✅ Each of 20 meters individually shows 100% accuracy
3. ✅ Confusion matrix has ZERO off-diagonal elements
4. ✅ 2+ independent prosody experts attest to accuracy
5. ✅ المتدارك specifically validated with 15 verses
6. ✅ Statistical tests confirm no meter bias
7. ✅ Complete documentation published
8. ✅ Dataset openly available with DOI
9. ✅ Reproducible test harness provided
10. ✅ Peer review (if applicable) completed

---

**Document Owner:** BAHR Detection Engine Team
**Status:** Ready for implementation
**Next Steps:** Execute المتدارك corpus sourcing → annotation → evaluation
