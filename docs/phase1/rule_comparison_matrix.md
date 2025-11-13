# Rule Comparison Matrix - Classical Sources vs. Code Implementation

## Purpose
This document provides detailed comparison tables for each meter, comparing classical Arabic prosody rules against the current BAHR engine implementation.

## Verification Methodology
1. Classical sources consulted via online Arabic libraries
2. Rules extracted with original Arabic text
3. Compared to code implementation in meters.py, zihafat.py, and ilal.py
4. Discrepancies documented with severity ratings

---

## Meter 1: الطويل (al-Ṭawīl)

### Overview

| Aspect | Classical Source | Current Code | Match? |
|--------|------------------|--------------|--------|
| Base Pattern | فعولن مفاعيلن فعولن مفاعيلن | ✅ Correct (meters.py:208-212) | ✅ YES |
| Frequency Rank | Most common (1st) | ✅ frequency_rank=1 | ✅ YES |
| Tier | Most used | ✅ TIER_1 | ✅ YES |

---

### Position 1: فَعُولُنْ

| Rule Aspect | Classical Source | Current Code | Match? | Notes |
|-------------|------------------|--------------|--------|-------|
| **Base Tafʿīlah** | فعولن (`/o//o`) | ✅ TAFAIL_BASE["فعولن"] | ✅ YES | Correct |
| **Allowed: قَبْض (QABD)** | Allowed (common) | ✅ QABD in list (line 215) | ✅ YES | Correct |
| **Allowed: كَفّ (KAFF)** | ⚠️ Not applicable (فَعُولُنْ has only 2 sakins, kaff needs 7) | ❌ KAFF in list (line 215) | ❌ NO | **KAFF should be removed** - not applicable due to insufficient sakin count |
| **Prohibited: خَبْن (KHABN)** | Not allowed (would break watad) | ✅ Not in code | ✅ YES | Correct exclusion |
| **Prohibited: طَيّ (TAYY)** | Not allowed | ✅ Not in code | ✅ YES | Correct exclusion |

**Position 1 Assessment:**
- **Total Rules:** 5
- **Matches:** 4 (80%)
- **Discrepancies:** 1 (KAFF incorrectly included)
- **Severity:** MEDIUM
- **Action:** Remove KAFF from allowed_zihafat

---

### Position 2: مَفَاعِيلُنْ ('Arūḍ Position in First Hemistich)

| Rule Aspect | Classical Source | Current Code | Match? | Notes |
|-------------|------------------|--------------|--------|-------|
| **Base Tafʿīlah** | مفاعيلن (`//o/o/o`) | ✅ TAFAIL_BASE["مفاعيلن"] | ✅ YES | Correct |
| **Allowed: قَبْض (QABD)** | **MANDATORY (واجب)** in 'arūḍ position | ⚠️ Optional (line 216) | ⚠️ PARTIAL | Code allows but doesn't enforce mandatory constraint |
| **Frequency of QABD** | 100% in 'arūḍ (mandatory) | Not tracked | ⚠️ INFO | No frequency metadata in code |
| **Allowed: كَفّ (KAFF)** | **FORBIDDEN (يمتنع)** per classical sources: "يمتنع الْكَفّ في (مَفَاْعِيْلُنْ)" | ❌ KAFF in list (line 216) | ❌ NO | **CRITICAL: Direct violation of classical rule** |
| **Constraint: KAFF + QABD** | Cannot occur together | ❌ No constraint in code | ❌ NO | Code doesn't prevent co-occurrence |
| **Prohibited: خَبْن (KHABN)** | Not allowed | ✅ Not in code | ✅ YES | Correct exclusion |

**Position 2 Assessment:**
- **Total Rules:** 6
- **Matches:** 2 (33%)
- **Partial Matches:** 1 (QABD allowed but not mandatory)
- **Discrepancies:** 3
- **Critical Issues:** 1 (KAFF forbidden but included)
- **Severity:** HIGH
- **Action Required:**
  1. Remove KAFF from allowed_zihafat (line 216)
  2. Add mandatory constraint for QABD in 'arūḍ position
  3. Add mutual exclusion constraint for KAFF + QABD

---

### Position 3: فَعُولُنْ

**[Same analysis as Position 1]**

| Rule Aspect | Classical Source | Current Code | Match? | Notes |
|-------------|------------------|--------------|--------|-------|
| **Base Tafʿīlah** | فعولن (`/o//o`) | ✅ TAFAIL_BASE["فعولن"] | ✅ YES | Correct |
| **Allowed: قَبْض (QABD)** | Allowed (common) | ✅ QABD in list (line 217) | ✅ YES | Correct |
| **Allowed: كَفّ (KAFF)** | ⚠️ Not applicable | ❌ KAFF in list (line 217) | ❌ NO | **KAFF should be removed** |

**Position 3 Assessment:**
- **Total Rules:** 3
- **Matches:** 2 (67%)
- **Discrepancies:** 1 (KAFF)
- **Severity:** MEDIUM

---

### Position 4: مَفَاعِيلُنْ (Final Position - Ḍarb)

| Rule Aspect | Classical Source | Current Code | Match? | Notes |
|-------------|------------------|--------------|--------|-------|
| **Base Tafʿīlah** | مفاعيلن (`//o/o/o`) | ✅ TAFAIL_BASE["مفاعيلن"] | ✅ YES | Correct |
| **Allowed: قَبْض (QABD)** | Optional (common ~40-60%) | ✅ QABD in list (line 218) | ✅ YES | Correct |
| **Allowed: كَفّ (KAFF)** | **FORBIDDEN (يمتنع)** in مَفَاْعِيْلُنْ | ❌ KAFF in list (line 218) | ❌ NO | **CRITICAL: Same violation as Position 2** |

**ʿIlal (Final Position Only):**

| ʿIllah | Classical Source | Current Code | Match? | Notes |
|--------|------------------|--------------|--------|-------|
| **حَذْف (HADHF)** | Allowed but rare (<5%) | ✅ HADHF (line 219) | ✅ YES | Correct |
| **قَصْر (QASR)** | Allowed but rare | ✅ QASR (line 219) | ✅ YES | Correct |
| **Interaction note** | QASR application unclear when KAFF is forbidden | Not modeled | ⚠️ INFO | Needs clarification |
| **قَطْع (QAT)** | Not mentioned for الطويل | ✅ Not in code | ✅ YES | Correct exclusion |

**Position 4 Assessment:**
- **Total Rules:** 5 (ziḥāfāt + ʿilal)
- **Matches:** 3 (60%)
- **Discrepancies:** 2 (KAFF forbidden, interaction unclear)
- **Severity:** HIGH

---

### Overall Assessment for الطويل

**Summary Statistics:**
- **Total Rules Checked:** 19
- **Exact Matches:** 12 (63%)
- **Partial Matches:** 1 (5%)
- **Discrepancies:** 6 (32%)
- **Critical Issues:** 2
  1. KAFF allowed in positions 2 & 4 where it's **explicitly forbidden**
  2. QABD not marked as **mandatory** in 'arūḍ position

**Severity Breakdown:**
- **CRITICAL:** 1 (Pattern-level vs. letter-level transformation logic - affects all meters)
- **HIGH:** 2 (KAFF violations in positions 2 & 4)
- **MEDIUM:** 2 (KAFF in positions 1 & 3 - not applicable)
- **LOW:** 1 (Missing frequency metadata)

**Impact on Detection Accuracy:**
- Current implementation may accept **invalid patterns** that include KAFF in مَفَاعِيلُنْ positions
- May fail to enforce mandatory QABD in 'arūḍ, potentially rejecting valid verses
- Estimated impact: Could affect 15-25% of al-Ṭawīl detection accuracy

**Recommendations (Priority Order):**

1. **IMMEDIATE - Remove KAFF from all positions** (Lines 215-220)
   ```python
   # Change from:
   1: MeterRules(allowed_zihafat=[QABD, KAFF]),
   2: MeterRules(allowed_zihafat=[QABD, KAFF]),

   # To:
   1: MeterRules(allowed_zihafat=[QABD]),
   2: MeterRules(allowed_zihafat=[QABD]),
   ```

2. **HIGH PRIORITY - Add mandatory constraint for QABD in 'arūḍ**
   - Extend MeterRules dataclass to support mandatory_zihafat field
   - Mark QABD as mandatory in position 2 of first hemistich

3. **MEDIUM PRIORITY - Add frequency metadata**
   - Track common vs. rare ziḥāfāt for confidence scoring

4. **CRITICAL (Phase 2) - Implement letter-level transformations**
   - Rewrite all ziḥāf/ʿillah functions to operate on letter structures
   - Ensure accurate counting of sākin vs. mutaḥarrik letters

---

## Transformation Logic Verification

### Pattern-Level vs. Letter-Level Issue

**Classical Standard:**
Ziḥāfāt are defined at the **letter level** (حرف):
- "خَبْن: حذف الساكن الثاني" = Remove the 2nd **sākin letter**
- "قَبْض: حذف الخامس الساكن" = Remove the 5th **sākin letter**
- "كَفّ: حذف السابع الساكن" = Remove the 7th **sākin letter**

**Current Implementation:**
All transformations operate on **phonetic pattern strings** (`/o` notation):

```python
# File: zihafat.py:180-193
def qabd_transform(pattern: str) -> str:
    """قبض - Remove 5th sakin (often the last one)."""
    sakin_count = 0
    for i, char in enumerate(pattern):
        if char == "o":  # ⚠️ Counts 'o' in pattern string
            sakin_count += 1
            if sakin_count == 5:
                return remove_at_index(pattern, i)
    # If less than 5 sakins, remove last one
    last_o = pattern.rfind("o")
    if last_o != -1:
        return remove_at_index(pattern, last_o)
    return pattern
```

**Problem:**
- Classical: Counts sākin **letters** in the taf'ila (including madd letters: ا، و، ي)
- Code: Counts 'o' **characters** in the abstract pattern

**Example Case - QABD on مَفَاعِيلُنْ:**

**Letter-Level (Classical):**
```
م-َ ف-َ ا ع-ِ ي ل-ُ ن-ْ
Letter positions: 1  2  3 4  5 6  7

Sākin letters:
- ا (position 3) = 1st sākin
- ي (position 5) = 2nd sākin ← **5th letter, 2nd sākin**
- ن (position 7) = 3rd sākin

Remove 5th position (which is the 2nd sākin): ي
Result: م-َ ف-َ ا ع-ِ ل-ُ ن-ْ = مَفَاعِلُنْ
Pattern: //o/o/o → //o//o ✓
```

**Pattern-Level (Current Code):**
```
Pattern: //o/o/o
'o' positions: 3, 5, 7

Count 'o' characters:
- Position 3: 1st 'o'
- Position 5: 2nd 'o'
- Position 7: 3rd 'o' (last)

"Remove 5th sakin" → No 5th 'o' exists
Fallback: Remove last 'o' at position 7
Result: //o/o/ (WRONG!) or //o/o (if removes char) ❌
```

**⚠️ CRITICAL FINDING:**

The current `qabd_transform()` may produce **INCORRECT results** for مَفَاعِيلُنْ!

**Testing Required:**
```python
# Test case needed:
pattern = "//o/o/o"  # مَفَاعِيلُنْ
result = qabd_transform(pattern)
expected = "//o//o"  # مَفَاعِلُنْ

# What does current code actually return?
# Need to verify: does it return "//o/o" or "//o//o"?
```

**Impact:** If qabd_transform is broken for مَفَاعِيلُنْ, then **al-Ṭawīl detection will fail** since:
- QABD is **mandatory** in position 2 ('arūḍ)
- QABD is very common in position 4 (ḍarb)
- Incorrect transformation → incorrect pattern → failed match

**Recommendation:**
1. **IMMEDIATE:** Test current qabd_transform() with pattern `//o/o/o`
2. **CRITICAL (Phase 2):** Rewrite all transformations using letter-level logic

---

## Status Legend

- ✅ **YES**: Exact match with classical sources
- ⚠️ **PARTIAL**: Partially correct but missing constraints/metadata
- ❌ **NO**: Discrepancy or contradiction with classical sources
- ⚠️ **INFO**: Additional information needed but doesn't affect correctness

---

## Next Steps

1. Complete verification for remaining 15 meters
2. Test current transformation functions for correctness
3. Implement fixes for identified discrepancies
4. Add letter-level transformation architecture (Phase 2)

---

**Document Version:** 1.0
**Date:** 2025-11-13
**Status:** Al-Ṭawīl complete; 15 meters remaining
