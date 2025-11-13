# المتقارب (al-Mutaqārib) - "The Convergent"

## Metadata
- **Meter ID:** 11
- **Frequency Tier:** 1
- **Frequency Rank:** 11 out of 16
- **Estimated Frequency:** 3-4% of poetry
- **Genres:** Narrative, storytelling

## Base Pattern

**Taqṭīʿ:** فعولن فعولن فعولن فعولن

**Pattern:** `/o//o /o//o /o//o /o//o`

**Note:** All 4 positions use same taf'ila (فعولن)

## Position Analysis

### All Positions (1-4): فَعُولُنْ

**Pattern:** `/o//o`
**Ziḥāف:** قَبْض (QABD)

**Test Result:** ✅ **WORKS CORRECTLY**
- Input: `/o//o`
- Output: `/o//`
- Status: PASS

## Status Assessment

**✅ POTENTIALLY WORKING METER**

This is one of the few meters that may work correctly because:
1. Uses only فعولن (simple pattern)
2. QABD transformation accidentally works for this pattern
3. No complex tafāʿīl with problematic transformations

**Estimated Accuracy:** 70-80% (much better than other meters)

## Code

```python
AL_MUTAQARIB = Meter(
    id=11,
    base_tafail=[
        TAFAIL_BASE["فعولن"],
        TAFAIL_BASE["فعولن"],
        TAFAIL_BASE["فعولن"],
        TAFAIL_BASE["فعولن"],
    ],
    rules_by_position={
        1: MeterRules(allowed_zihafat=[QABD]),
        2: MeterRules(allowed_zihafat=[QABD]),
        3: MeterRules(allowed_zihafat=[QABD]),
        4: MeterRules(allowed_zihafat=[QABD], allowed_ilal=[HADHF, QAT], is_final=True),
    },
)
```

**Status:** ✅ LIKELY WORKING
**Version:** 1.0 - 2025-11-13
