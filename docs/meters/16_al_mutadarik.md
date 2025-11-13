# المتدارك (al-Mutadārik) - "The Overtaking"

## Metadata
- **Meter ID:** 16
- **Frequency Tier:** 3 (Rare)
- **Frequency Rank:** 16 out of 16 (least common)
- **Genres:** Rare

## Classical Definition

> المتدارك هو البحر السادس عشر، استدركه الأخفش على الخليل

"Al-Mutadārik is the 16th meter, added by al-Akhfash to al-Khalīl's original 15"

## Base Pattern

**Taqṭīʿ:** فاعلن فاعلن فاعلن فاعلن

**Pattern:** `/o//o /o//o /o//o /o//o`

**Note:** All 4 positions use same taf'ila (فاعلن)

## Position Analysis

### All Positions (1-4): فَاعِلُنْ

**Pattern:** `/o//o`
**Ziḥāف:** خَبْن

**Application:**
- Result: فَعِلُنْ (faʿilun)
- Pattern: `/o//o` → `///o`

**Code Verification:**
```
Test Result: /o//o → ///o ✅ PASS
Status: Works correctly (special case hardcoded, line 156)
```

**Special Note:** Code has explicit handling:
```python
if pattern == "/o//o":
    return "///o"
```

## Status Assessment

**✅ POTENTIALLY WORKING METER**

This meter likely works correctly because:
1. Simple repeating pattern (فاعلن × 4)
2. KHABN has special case handling for `/o//o`
3. No complex transformations

**Estimated Accuracy:** 70-80%

## Code

```python
AL_MUTADARIK = Meter(
    id=16,
    base_tafail=[
        TAFAIL_BASE["فاعلن"],
        TAFAIL_BASE["فاعلن"],
        TAFAIL_BASE["فاعلن"],
        TAFAIL_BASE["فاعلن"],
    ],
    rules_by_position={
        1: MeterRules(allowed_zihafat=[KHABN]),
        2: MeterRules(allowed_zihafat=[KHABN]),
        3: MeterRules(allowed_zihafat=[KHABN]),
        4: MeterRules(allowed_zihafat=[KHABN], allowed_ilal=[HADHF, QASR], is_final=True),
    },
)
```

**Status:** ✅ LIKELY WORKING
**Version:** 1.0 - 2025-11-13
