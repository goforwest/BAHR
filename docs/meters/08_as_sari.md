# السريع (as-Sarīʿ) - "The Fast"

## Metadata
- **Meter ID:** 8
- **Frequency Tier:** 2
- **Frequency Rank:** 8 out of 16
- **Estimated Frequency:** 2-3% of poetry
- **Genres:** Wisdom, heroism, varied

## Base Pattern

**Taqṭīʿ:** مستفعلن مستفعلن فاعلن

**Pattern:** `/o/o//o /o/o//o /o//o`

## Positions

### Positions 1-2: مُسْتَفْعِلُنْ
- **Ziḥāfāt:** خَبْن، طَيّ، خَبْل
- **Status:** ❌ KHABN BROKEN

### Position 3 (Final): فَاعِلُنْ
- **Ziḥāفāت:** خَبْن
- **ʿIlal:** كَشْف، قَصْر
- **Status:** ✅ KHABN works (special case)

## Critical Issues

**KHABN broken** in positions 1-2 (66% of meter)

## Code

```python
AS_SARI = Meter(
    id=8,
    base_tafail=[
        TAFAIL_BASE["مستفعلن"],
        TAFAIL_BASE["مستفعلن"],
        TAFAIL_BASE["فاعلن"],
    ],
    rules_by_position={
        1: MeterRules(allowed_zihafat=[KHABN, TAYY, KHABL]),
        2: MeterRules(allowed_zihafat=[KHABN, TAYY, KHABL]),
        3: MeterRules(allowed_zihafat=[KHABN], allowed_ilal=[KASHF, QASR], is_final=True),
    },
)
```

**Status:** ❌ CRITICAL - KHABN broken
**Version:** 1.0 - 2025-11-13
