# Pattern Normalization Layer - Technical Specification

**Status:** Medium-term solution proposal
**Priority:** Medium
**Estimated Effort:** 1-2 weeks
**Prerequisites:** Deep understanding of Arabic prosody (العروض)

---

## 🎯 **Objective**

Create a transformation layer that maps syllable-based phonetic patterns (extracted from text) to tafila-based prosodic patterns (used in meter detection cache), solving the fundamental architectural mismatch in the current system.

---

## 🔬 **Problem Statement**

### Current Architecture Mismatch

The system has two incompatible pattern generation systems:

#### System 1: Pattern Cache (Theoretical)
- **Source:** Generated from abstract tafila definitions
- **Method:** `backend/app/core/prosody/pattern_generator.py`
- **Pattern Type:** Theoretical prosodic structures
- **Example for الطويل:**
  ```
  Pattern: /o//o//o/o/o/o//o//o/o/o
  Length: 24 characters
  Structure: 4 tafa'il (feet)
  ```

#### System 2: Pattern Extraction (Actual Text)
- **Source:** Extracted from real Arabic text syllable-by-syllable
- **Method:** `backend/app/core/phonetics.py:text_to_phonetic_pattern()`
- **Pattern Type:** Actual syllable scansion
- **Example from Mu'allaqah:**
  ```
  Pattern: //o/o//o/o/o//o/o//o//
  Length: 22 characters
  Structure: Syllable-by-syllable scansion
  ```

### The Fundamental Issue

**These patterns don't align structurally.**

The extracted pattern `//o/o//o/o/o//o/o//o//` from a الطويل verse resembles الرجز patterns more than الطويل patterns in the cache, leading to incorrect detection.

This isn't a bug—it's an architectural limitation that requires a transformation layer.

---

## 💡 **Proposed Solution: Pattern Normalization Layer**

### Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    INPUT: Arabic Text                         │
│          "قفا نبك من ذكرى حبيب ومنزل"                        │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────┐
│               Syllable Extraction (Current)                   │
│         phonetics.py:extract_syllables()                      │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────┐
│          Raw Syllable Pattern (Current Output)                │
│              //o/o//o/o/o//o/o//o//                          │
│              (22 chars, syllable-based)                       │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────┐
│          ⭐ PATTERN NORMALIZATION LAYER (NEW) ⭐              │
│                                                               │
│  1. Identify syllable boundaries                             │
│  2. Group syllables into tafa'il (feet)                      │
│  3. Map to canonical tafila patterns                         │
│  4. Apply prosodic rules (رخص، زحافات، علل)                 │
│  5. Generate tafila-compatible pattern                        │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────┐
│      Normalized Tafila Pattern (Normalized Output)            │
│            /o//o//o/o/o/o//o//o/o/o                          │
│            (24 chars, tafila-based)                           │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────┐
│          Pattern Cache Matching (Existing Logic)              │
│           detector_v2.py:detect()                             │
│                                                               │
│  Match against: 365+ cached tafila patterns                   │
│  Result: الطويل (97% confidence) ✓                           │
└──────────────────────────────────────────────────────────────┘
```

---

## 🔧 **Implementation Approach**

### Step 1: Syllable-to-Tafila Grouping

**Challenge:** Determine where syllable boundaries map to tafila boundaries.

**Approach:**
1. Use known meter signatures (e.g., الطويل = فعولن مفاعيلن فعولن مفاعيلن)
2. For each meter, identify expected tafila lengths
3. Group syllables accordingly

**Example for الطويل:**
```python
# Input syllables (from pattern //o/o//o/o/o//o/o//o//)
syllables = [
    ('//', 'CV̄'),   # Long syllable
    ('/o', 'CVC'),  # Closed syllable
    ('/', 'CV'),    # Open syllable
    ('//', 'CV̄'),
    # ... etc
]

# Expected tafila for الطويل: فعولن (3 syllables) + مفاعيلن (4 syllables)
# Group accordingly:
tafila_1 = syllables[0:3]  # فعولن
tafila_2 = syllables[3:7]  # مفاعيلن
tafila_3 = syllables[7:10] # فعولن
tafila_4 = syllables[10:14] # مفاعيلن
```

### Step 2: Apply Prosodic Rules

**Classical Arabic Prosody Rules:**

#### الزحافات (Zihafat) - Permitted variations in non-final feet
- **قبض** (qabd): Dropping the fifth sakin letter (e.g., فعولن → فعولُ)
- **خبن** (khabn): Dropping the second sakin letter (e.g., مفاعيلن → مفاعلن)
- **طيّ** (tayy): Dropping the fourth sakin letter

#### العلل (Ilal) - Variations in final feet
- **حذف** (hadhf): Dropping the sakin and the haraka before it
- **قطع** (qat'): Dropping the sakin and making the letter before it sakin

**Implementation:**
```python
def normalize_tafila(tafila_pattern: str, position: str) -> str:
    """
    Normalize a tafila pattern by applying prosodic rules.

    Args:
        tafila_pattern: Raw syllable-based pattern for one tafila
        position: 'first', 'middle', or 'final'

    Returns:
        Normalized tafila pattern compatible with cache
    """
    # Check if pattern matches known variations
    # Apply appropriate transformation
    # Return canonical or valid variant pattern
    pass
```

### Step 3: Reconstruct Full Pattern

Concatenate normalized tafa'il to create full pattern:

```python
normalized_pattern = ''.join([
    normalize_tafila(tafila_1, 'first'),
    normalize_tafila(tafila_2, 'middle'),
    normalize_tafila(tafila_3, 'middle'),
    normalize_tafila(tafila_4, 'final')
])

# Result: /o//o//o/o/o/o//o//o/o/o (matches cache pattern for الطويل!)
```

---

## 📊 **Expected Impact**

### Before Normalization

| Verse | Extracted Pattern | Current Detection | Confidence | Correct? |
|-------|-------------------|-------------------|------------|----------|
| Mu'allaqah | `//o/o//o/o/o//o/o//o//` | **الرجز** | 95.81% | ❌ |
| البسيط example | `/o///o///o/o///o///o` | المتقارب (approx) | 87.21% | ❌ |

### After Normalization (Expected)

| Verse | Normalized Pattern | Expected Detection | Confidence | Correct? |
|-------|-------------------|-------------------|------------|----------|
| Mu'allaqah | `/o//o//o/o/o/o//o//o/o/` | **الطويل** | 97%+ | ✅ |
| البسيط example | `/o///o///o/o///o///o` | البسيط (exact) | 95%+ | ✅ |

**Estimated Accuracy Improvement:** 82% → 95%+ on real user input

---

## 🚧 **Implementation Challenges**

### Challenge 1: Ambiguity in Syllable Grouping

**Problem:** Without knowing the meter in advance, it's hard to know where to split syllables.

**Solutions:**
1. **Try all possibilities:** For a given pattern, try grouping as الطويل, الكامل, etc., and pick best match
2. **Heuristic-based:** Use pattern length and structure to narrow down likely meters
3. **Iterative refinement:** Use hybrid detection (current approach) to get initial guess, then refine

### Challenge 2: Prosodic Knowledge Requirements

**Problem:** Requires deep understanding of classical Arabic prosody rules.

**Solutions:**
1. Collaborate with Arabic prosody experts
2. Use existing academic resources (Al-Khalil's system)
3. Study classical poetry corpora to learn variation patterns

### Challenge 3: Performance Overhead

**Problem:** Normalization adds computational complexity.

**Solutions:**
1. Cache normalized patterns for common inputs
2. Optimize grouping algorithms (O(n) instead of O(n²))
3. Pre-compute normalization rules as lookup tables

---

## 🛠️ **Implementation Plan**

### Phase 1: Research & Design (3-5 days)
- [ ] Study Al-Khalil's prosody system in depth
- [ ] Analyze 100+ classical poetry examples across all 16 meters
- [ ] Document syllable→tafila mapping rules for each meter
- [ ] Create test cases with expected transformations

### Phase 2: Core Normalization Logic (5-7 days)
- [ ] Implement `PatternNormalizer` class
- [ ] Implement syllable grouping algorithm
- [ ] Implement prosodic rule application (زحافات، علل)
- [ ] Write unit tests for each meter

### Phase 3: Integration (2-3 days)
- [ ] Integrate with `phonetics.py:text_to_phonetic_pattern()`
- [ ] Add normalization option to `analyze_v2.py`
- [ ] Maintain backward compatibility (optional flag)
- [ ] Update API documentation

### Phase 4: Validation (2-3 days)
- [ ] Test on golden set (should maintain 100% accuracy)
- [ ] Test on Mu'allaqah and other problematic verses
- [ ] Run confusion analysis before/after
- [ ] Benchmark performance impact

### Phase 5: Deployment (1-2 days)
- [ ] Enable for real users
- [ ] Monitor accuracy metrics
- [ ] Collect new feedback
- [ ] Iterate based on results

---

## 📚 **Resources & References**

### Classical Prosody References
1. **Al-Khalil ibn Ahmad** (8th century): Founder of Arabic prosody
2. **الكافي في العروض والقوافي** (Al-Kafi fi al-Arud wa al-Qawafi)
3. **ميزان الذهب في صناعة شعر العرب** (Mizan al-Dhahab)

### Code References
- `backend/app/core/phonetics.py` - Current syllable extraction
- `backend/app/core/prosody/pattern_generator.py` - Tafila pattern generation
- `backend/app/core/prosody/detector_v2.py` - Pattern matching logic

### Related Documents
- `METER_DETECTION_INVESTIGATION.md` - Root cause analysis
- `UI_MULTI_CANDIDATE_SPEC.md` - Multi-candidate UI (short-term solution)

---

## ⚖️ **Trade-offs**

### Pros
✅ Solves root cause (pattern mismatch)
✅ Improves accuracy significantly (82% → 95%+)
✅ Maintains explainability (still rule-based)
✅ Compatible with existing cache system

### Cons
❌ High implementation complexity
❌ Requires prosody expertise
❌ Adds computational overhead
❌ May introduce new edge cases

---

## 🎯 **Recommendation**

**When to implement:**
- **Short-term:** Use multi-candidate UI (already implemented) to handle uncertainty
- **Medium-term:** Implement normalization if user feedback shows high demand for accuracy
- **Long-term:** Consider ML approach if normalization proves too complex

**Priority assessment:**
- If users tolerate multi-candidate UI: **Low priority**
- If users demand single correct answer: **High priority**
- If confusion rate > 30%: **Critical priority**

---

## 📈 **Success Metrics**

Track these metrics after implementation:

1. **Detection Accuracy:** Target 95%+ on real user input
2. **الطويل ↔ الرجز Confusion Rate:** Reduce from current ~50% to <5%
3. **Performance Impact:** Normalization overhead <100ms per request
4. **User Feedback:** Correction rate should drop significantly

---

**Document Version:** 1.0
**Last Updated:** 2025-11-12
**Author:** Claude (Anthropic)
**Status:** Proposal for review
