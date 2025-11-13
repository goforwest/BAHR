# المديد (al-Madīd) - "The Extended"

## Metadata
- **Meter ID:** 9
- **Frequency Tier:** 2
- **Frequency Rank:** 9 out of 16
- **Estimated Frequency:** ~2% of poetry
- **Genres:** Ghazal, description

## Base Pattern

**Taqṭīʿ:** فاعلاتن فاعلن فاعلاتن

**Pattern:** `/o//o/o /o//o /o//o/o`

## Positions

### Position 1: فَاعِلَاتُنْ
- **Ziḥāفāت:** خَبْن، كَفّ
- **Status:** ⚠️ KHABN untested, KAFF likely wrong

### Position 2: فَاعِلُنْ
- **Ziḥāفāت:** خَبْن
- **Status:** ✅ Works

### Position 3 (Final): فَاعِلَاتُنْ
- **Ziḥāفāت:** خَبْن
- **ʿIlal:** حَذْف، قَصْر
- **Status:** ⚠️ KHABN untested

## Issues

**KAFF in positions 1**: Likely not applicable (insufficient sakins)

## Code

```python
AL_MADID = Meter(
    id=9,
    base_tafail=[
        TAFAIL_BASE["فاعلاتن"],
        TAFAIL_BASE["فاعلن"],
        TAFAIL_BASE["فاعلاتن"],
    ],
    rules_by_position={
        1: MeterRules(allowed_zihafat=[KHABN, KAFF]),  # KAFF questionable
        2: MeterRules(allowed_zihafat=[KHABN]),
        3: MeterRules(allowed_zihafat=[KHABN], allowed_ilal=[HADHF, QASR], is_final=True),
    },
)
```

**Status:** ⚠️ KAFF likely wrong
**Version:** 1.0 - 2025-11-13
