# الخفيف (al-Khafīf) - "The Light"

## Metadata
- **Meter ID:** 7
- **Frequency Tier:** 1
- **Frequency Rank:** 7 out of 16
- **Estimated Frequency:** 3-5% of poetry
- **Genres:** Light themes, muwashshaḥāt, varied

## Classical Definition

> سُمي الخفيف خفيفاً لخفة وزنه وسرعة النطق به. وهو مناسب للموشحات.

"Named 'light' for lightness of its weight and speed of pronunciation. Suitable for muwashshaḥāt."

## Base Pattern

**Taqṭīʿ:** فاعلاتن مستفعلن فاعلاتن

**Pattern:** `/o//o/o /o/o//o /o//o/o`

**Note:** Alternating pattern (فاعلاتن / مستفعلن / فاعلاتن)

## Position Analysis

### Position 1: فَاعِلَاتُنْ
- **Pattern:** `/o//o/o`
- **Ziḥāfāt:** خَبْن (KHABN)
- **Status:** ⚠️ Needs testing

### Position 2: مُسْتَفْعِلُنْ
- **Pattern:** `/o/o//o`
- **Ziḥāfāt:** خَبْن (KHABN), طَيّ (TAYY)
- **Status:** ❌ KHABN BROKEN (confirmed)

### Position 3 (Final): فَاعِلَاتُنْ
- **Pattern:** `/o//o/o`
- **Ziḥāfāt:** خَبْن (KHABN)
- **ʿIlal:** حَذْف (HADHF)
- **Status:** ⚠️ Needs testing

## Critical Issues

**KHABN on مستفعلن Broken** (Position 2)
- Same bug as other meters
- Impact: 33% of meter positions affected

## Code Implementation

```python
AL_KHAFIF = Meter(
    id=7,
    base_tafail=[
        TAFAIL_BASE["فاعلاتن"],
        TAFAIL_BASE["مستفعلن"],
        TAFAIL_BASE["فاعلاتن"],
    ],
    rules_by_position={
        1: MeterRules(allowed_zihafat=[KHABN]),
        2: MeterRules(allowed_zihafat=[KHABN, TAYY]),  # KHABN broken
        3: MeterRules(allowed_zihafat=[KHABN], allowed_ilal=[HADHF], is_final=True),
    },
)
```

## Status

- **Verification:** Complete
- **Issues:** ❌ KHABN broken in position 2
- **Version:** 1.0 - 2025-11-13
