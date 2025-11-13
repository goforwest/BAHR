# المنسرح (al-Munsariḥ) - "The Flowing"

## Metadata
- **Meter ID:** 10
- **Frequency Tier:** 3 (Rare)
- **Frequency Rank:** 10 out of 16
- **Genres:** Rare, varied

## Base Pattern

**Taqṭīʿ:** مستفعلن مفعولات مفتعلن

**Pattern:** `/o/o//o /o/o/o/ /o/o//o`

**Note:** Uses 3 different tafāʿīl

## Positions

### Position 1: مُسْتَفْعِلُنْ
- **Ziḥāفāت:** خَبْن، طَيّ
- **Status:** ❌ KHABN BROKEN

### Position 2: مَفْعُولَاتُ
- **Pattern:** `/o/o/o/`
- **Ziḥāفāت:** طَيّ
- **Status:** ⚠️ Untested

### Position 3 (Final): مَفْتَعِلُنْ
- **Pattern:** `/o/o//o` (same structure as مستفعلن)
- **ʿIlal:** كَشْف
- **Status:** ❌ Likely same KHABN bug

## Critical Issues

**KHABN broken** on مستفعلن and likely مفتعلن

## Code

```python
AL_MUNSARIH = Meter(
    id=10,
    base_tafail=[
        TAFAIL_BASE["مستفعلن"],
        TAFAIL_BASE["مفعولات"],
        TAFAIL_BASE["مفتعلن"],
    ],
    rules_by_position={
        1: MeterRules(allowed_zihafat=[KHABN, TAYY]),
        2: MeterRules(allowed_zihafat=[TAYY]),
        3: MeterRules(allowed_zihafat=[], allowed_ilal=[KASHF], is_final=True),
    },
)
```

**Status:** ❌ KHABN broken
**Version:** 1.0 - 2025-11-13
