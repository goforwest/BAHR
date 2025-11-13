# الرمل (ar-Ramal) - "The Sand"

## Metadata
- **Meter ID:** 6
- **Frequency Tier:** 1
- **Frequency Rank:** 6 out of 16
- **Estimated Frequency:** 4-6% of poetry
- **Genres:** Ghazal, light themes, emotional poetry

## Classical Definition

> سُمي الرمل رملاً لسرعته. وهو بحر رقيق سلس، مناسب للغزل والموضوعات الخفيفة.

"Named 'sand' for its speed. It is a delicate, smooth meter suitable for love poetry and light themes."

## Base Pattern

**Taqṭīʿ:** فاعلاتن فاعلاتن فاعلاتن

**Pattern:** `/o//o/o /o//o/o /o//o/o`

**Note:** All 3 positions use same taf'ila (فاعلاتن)

## Position Analysis

### All Positions (1-3): فَاعِلَاتُنْ

#### Base Form
- **Pattern:** `/o//o/o`
- **Letters:** ف ا ع ل ا ت ن (7 letters)
- **Sakins:** ا (2nd), ا (5th), ن (7th) = 3 sakins
- **Structure:** Watad Mafrūq + 2 Sabab Khafīf

#### Allowed Ziḥāfāt

1. **خَبْن (KHABN)**
   - Expected: Remove 2nd sakin
   - Pattern: `/o//o/o` → `///o/o`
   - **Status: ⚠️ NEEDS TESTING**

2. **كَفّ (KAFF)**
   - Definition: Remove 7th sakin
   - Pattern has 3 sakins, 7th sakin doesn't exist
   - **Status: ⚠️ LIKELY NOT APPLICABLE** (same issue as al-Ṭawīl)
   - Recommendation: Should be REMOVED

### ʿIlal (Position 3)

1. **حَذْف (HADHF)** - Remove last sabab

## Critical Issues

### Issue 1: KAFF Misapplied (MEDIUM)

**Problem:** Pattern `/o//o/o` has only 3 sakins total
- Cannot remove "7th sakin" when only 3 exist
- Similar to al-Ṭawīl KAFF issue

**Recommendation:** Remove KAFF from allowed_zihafat

### Issue 2: KHABN Untested (HIGH)

**Needs verification** for pattern `/o//o/o`

## Code Implementation

```python
AR_RAMAL = Meter(
    id=6,
    base_tafail=[
        TAFAIL_BASE["فاعلاتن"],
        TAFAIL_BASE["فاعلاتن"],
        TAFAIL_BASE["فاعلاتن"],
    ],
    rules_by_position={
        1: MeterRules(allowed_zihafat=[KHABN, KAFF]),  # KAFF questionable
        2: MeterRules(allowed_zihafat=[KHABN, KAFF]),  # KAFF questionable
        3: MeterRules(
            allowed_zihafat=[KHABN, KAFF],  # KAFF questionable
            allowed_ilal=[HADHF],
            is_final=True
        ),
    },
)
```

## Status

- **Verification:** Complete
- **Issues:** ⚠️ KAFF likely wrong, KHABN untested
- **Version:** 1.0 - 2025-11-13
