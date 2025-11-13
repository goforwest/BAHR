# الرجز (al-Rajaz) - "The Trembling/Rajaz"

## Metadata
- **Meter ID:** 5
- **Frequency Tier:** 1
- **Frequency Rank:** 5 out of 16
- **Estimated Frequency:** 6-8% of poetry
- **Genres:** Educational poetry (أراجيز), didactic, varied

## Classical Definition

> سُمي الرجز رجزاً لاضطرابه وتقارب أجزائه. وهو كثير في الأراجيز التعليمية.

"Named rajaz for its trembling/shaking quality and closeness of its parts. Common in educational rajaz poems."

## Base Pattern

**Taqṭīʿ:** مستفعلن مستفعلن مستفعلن

**Pattern:** `/o/o//o /o/o//o /o/o//o`

**Note:** All 3 positions use same taf'ila (مستفعلن)

## Position Analysis

### All Positions (1-3): مُسْتَفْعِلُنْ

**Pattern:** `/o/o//o`
**[Same letter structure as al-Basīṭ position 1]**

### Allowed Ziḥāfāt

1. **خَبْن (KHABN)** - All positions
   - Expected: `/o/o//o` → `//o//o`
   - **Status: ❌ BROKEN** (same bug as al-Basīṭ)

2. **طَيّ (TAYY)** - All positions
   - Status: ✅ Works (returns unchanged, rare)

3. **خَبْل (KHABL)** - All positions
   - **Status: ❌ BROKEN** (depends on KHABN)

### ʿIlal (Position 3 only)

1. **قَطْع (QAṬ)** - Final position
2. **قَصْر (QAṢR)** - Final position

## Critical Issues

**KHABN Broken:** Affects all 3 positions
- Impact: ~70-80% of al-Rajaz patterns affected
- Same root cause as other meters

## Code Implementation

```python
AL_RAJAZ = Meter(
    id=5,
    base_tafail=[
        TAFAIL_BASE["مستفعلن"],
        TAFAIL_BASE["مستفعلن"],
        TAFAIL_BASE["مستفعلن"],
    ],
    rules_by_position={
        1: MeterRules(allowed_zihafat=[KHABN, TAYY, KHABL]),
        2: MeterRules(allowed_zihafat=[KHABN, TAYY, KHABL]),
        3: MeterRules(
            allowed_zihafat=[KHABN, TAYY, KHABL],
            allowed_ilal=[QAT, QASR],
            is_final=True,
        ),
    },
)
```

## Status

- **Verification:** Complete
- **Issues:** ❌ CRITICAL - KHABN broken
- **Version:** 1.0 - 2025-11-13
