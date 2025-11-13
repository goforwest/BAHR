# المجتث (al-Mujtathth) - "The Uprooted"

## Metadata
- **Meter ID:** 13
- **Frequency Tier:** 3 (Rare)
- **Frequency Rank:** 13 out of 16
- **Genres:** Rare, limited use

## Classical Definition

> المجتث مجتث من البسيط

"Al-Mujtathth is 'uprooted' from al-Basīṭ"

## Base Pattern

**Taqṭīʿ:** مستفعلن فاعلاتن

**Pattern:** `/o/o//o /o//o/o`

**Note:** Only 2 tafāʿīl (shortest meter)

## Position Analysis

### Position 1: مُسْتَفْعِلُنْ
- **Pattern:** `/o/o//o`
- **Ziḥāف:** خَبْن
- **Status:** ❌ BROKEN

### Position 2 (Final): فَاعِلَاتُنْ
- **Pattern:** `/o//o/o`
- **Ziḥāف:** خَبْن
- **ʿIlal:** حَذْف
- **Status:** ⚠️ Untested

## Critical Issues

**KHABN on مستفعلن broken** (position 1)
- 50% of meter affected

## Code

```python
AL_MUJTATHTH = Meter(
    id=13,
    base_tafail=[
        TAFAIL_BASE["مستفعلن"],
        TAFAIL_BASE["فاعلاتن"],
    ],
    rules_by_position={
        1: MeterRules(allowed_zihafat=[KHABN]),
        2: MeterRules(allowed_zihafat=[KHABN], allowed_ilal=[HADHF], is_final=True),
    },
)
```

**Status:** ❌ KHABN broken
**Version:** 1.0 - 2025-11-13
