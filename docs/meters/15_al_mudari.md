# المضارع (al-Muḍāriʿ) - "The Resembling"

## Metadata
- **Meter ID:** 15
- **Frequency Tier:** 3 (Rare)
- **Frequency Rank:** 15 out of 16
- **Genres:** Rare

## Classical Definition

> المضارع يضارع الهزج في إيقاعه

"Al-Muḍāriʿ resembles al-Hazaj in its rhythm"

## Base Pattern

**Taqṭīʿ:** مفاعيلن فاعلاتن

**Pattern:** `//o/o/o /o//o/o`

## Position Analysis

### Position 1: مَفَاعِيلُنْ
- **Pattern:** `//o/o/o`
- **Ziḥāف:** قَبْض
- **Status:** ❌ **QABD BROKEN** (same as al-Ṭawīl)

### Position 2 (Final): فَاعِلَاتُنْ
- **Pattern:** `/o//o/o`
- **Ziḥāف:** خَبْن
- **ʿIlal:** حَذْف
- **Status:** ⚠️ KHABN untested

## Critical Issues

**QABD on مفاعيلن broken** (position 1)
- Same bug affecting al-Ṭawīl and al-Hazaj
- Returns `//o/o/` instead of `//o//o`

## Code

```python
AL_MUDARI = Meter(
    id=15,
    base_tafail=[
        TAFAIL_BASE["مفاعيلن"],
        TAFAIL_BASE["فاعلاتن"],
    ],
    rules_by_position={
        1: MeterRules(allowed_zihafat=[QABD]),
        2: MeterRules(allowed_zihafat=[KHABN], allowed_ilal=[HADHF], is_final=True),
    },
)
```

**Status:** ❌ QABD broken
**Version:** 1.0 - 2025-11-13
