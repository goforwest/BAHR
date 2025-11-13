# الهزج (al-Hazaj) - "The Rhythmic/Trilling"

## Metadata
- **Meter ID:** 12
- **Frequency Tier:** 1
- **Frequency Rank:** 12 out of 16
- **Estimated Frequency:** 2-3% of poetry
- **Genres:** Light, musical themes

## Base Pattern (3-tafila تام version)

**Taqṭīʿ:** مفاعيلن مفاعيلن فعولن

**Pattern:** `//o/o/o //o/o/o /o//o`

## Position Analysis

### Positions 1-2: مَفَاعِيلُنْ
- **Pattern:** `//o/o/o`
- **Ziḥāفāت:** قَبْض، كَفّ
- **Status:** ❌ **QABD BROKEN** (same as al-Ṭawīl)
- **Status:** ❌ KAFF likely forbidden

### Position 3 (Final): فَعُولُنْ
- **Pattern:** `/o//o`
- **Ziḥāف:** قَبْض
- **ʿIlal:** حَذْف
- **Status:** ✅ QABD works for this pattern

## Critical Issues

**QABD on مفاعيلن broken** (positions 1-2)
- Same bug as al-Ṭawīl meter
- Returns `//o/o/` instead of `//o//o`
- Impact: 66% of meter affected

**KAFF**: Should likely be removed (forbidden in مفاعيلن per classical sources)

## Code

```python
AL_HAZAJ = Meter(
    id=12,
    base_tafail=[
        TAFAIL_BASE["مفاعيلن"],
        TAFAIL_BASE["مفاعيلن"],
        TAFAIL_BASE["فعولن"],
    ],
    rules_by_position={
        1: MeterRules(allowed_zihafat=[QABD, KAFF]),  # Both problematic
        2: MeterRules(allowed_zihafat=[QABD, KAFF]),  # Both problematic
        3: MeterRules(allowed_zihafat=[QABD], allowed_ilal=[HADHF], is_final=True),
    },
)
```

**Status:** ❌ CRITICAL - QABD broken
**Version:** 1.0 - 2025-11-13
