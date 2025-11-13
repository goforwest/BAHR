# المقتضب (al-Muqtaḍab) - "The Condensed"

## Metadata
- **Meter ID:** 14
- **Frequency Tier:** 3 (Rare)
- **Frequency Rank:** 14 out of 16
- **Genres:** Rare

## Classical Definition

> المقتضب مقتضب من المنسرح

"Al-Muqtaḍab is 'condensed' from al-Munsariḥ"

## Base Pattern

**Taqṭīʿ:** مفعولات مستفعلن

**Pattern:** `/o/o/o/ /o/o//o`

## Position Analysis

### Position 1: مَفْعُولَاتُ
- **Pattern:** `/o/o/o/`
- **Ziḥāف:** طَيّ
- **Status:** ⚠️ Untested

### Position 2 (Final): مُسْتَفْعِلُنْ
- **Pattern:** `/o/o//o`
- **Ziḥāف:** خَبْن
- **ʿIlal:** قَطْع
- **Status:** ❌ KHABN BROKEN

## Critical Issues

**KHABN broken** on final position

## Code

```python
AL_MUQTADAB = Meter(
    id=14,
    base_tafail=[
        TAFAIL_BASE["مفعولات"],
        TAFAIL_BASE["مستفعلن"],
    ],
    rules_by_position={
        1: MeterRules(allowed_zihafat=[TAYY]),
        2: MeterRules(allowed_zihafat=[KHABN], allowed_ilal=[QAT], is_final=True),
    },
)
```

**Status:** ❌ KHABN broken
**Version:** 1.0 - 2025-11-13
