# الوافر (al-Wāfir) - "The Abundant"

## Metadata
- **Meter ID:** 4
- **Frequency Tier:** 1 (Common)
- **Frequency Rank:** 4 out of 16
- **Common Usage:** Classical through modern, popular in contemporary poetry
- **Poetic Genres:** All genres, especially ghazal (love poetry), description
- **Estimated Frequency:** 5-7% of classical Arabic poetry

---

## Classical Definition

**Original Arabic:**
> سُمي الوافر وافراً لوفور حركاته. وهو من أكثر البحور استعمالاً في الشعر الحديث.

**Translation:**
> It is called "al-Wāfir" (abundant) for the abundance of its movements. It is among the most used meters in modern poetry.

**Classical Notes:**
- Fourth most common classical meter
- Very popular in modern/contemporary Arabic poetry
- Known for musical, flowing rhythm
- Suitable for emotional, descriptive themes

---

## Prosodic Structure

### Base Pattern

**Full Taqṭīʿ:**
```
مُفَاعَلَتُنْ مُفَاعَلَتُنْ فَعُولُنْ
Position 1   Position 2   Position 3
```

**Phonetic Pattern:**
```
//o///o //o///o /o//o
```

**Note:** Al-Wāfir is a **3-taf'ila meter** (unlike most others with 4)

---

## Position-by-Position Analysis

### Position 1: مُفَاعَلَتُنْ (mufāʿalatun)

#### Base Form
- **Arabic:** مُفَاعَلَتُنْ
- **Transliteration:** mufāʿalatun
- **Pattern:** `//o///o`
- **Prosodic Structure:**
  - Sabab Thaqīl: مُفَا = `//o`
  - Sabab Thaqīl: عَلَ = `//` (no explicit sakin)
  - Sabab Khafīf: تُنْ = `/o`

#### Letter-Level Breakdown
| Position | Letter | Ḥarakat | Type | Phonetic |
|----------|--------|---------|------|----------|
| 1 | م | Ḍamma | Mutaḥarrik | / |
| 2 | ف | Fatḥa | Mutaḥarrik | / |
| 3 | ا | Madd | Madd-sākin | o |
| 4 | ع | Fatḥa | Mutaḥarrik | / |
| 5 | ل | Fatḥa | Mutaḥarrik | / |
| 6 | ت | Ḍamma | Mutaḥarrik | / |
| 7 | ن | Sukūn | Sākin | o |

**Letter Count:** 7
**Sākin Count:** 2 (ا، ن)
**Mutaḥarrik Count:** 5

#### Allowed Ziḥāfāt

##### 1. عَصْب (ʿAṣb) - Remove 5th Mutaḥarrik

**Classical Definition:**
> العَصْب هو حذف الخامس المتحرك

"ʿAṣb is removal of the 5th mutaḥarrik letter"

**Application to مُفَاعَلَتُنْ:**
- Mutaḥarrik letters: م (1st), ف (2nd), ع (4th), ل (5th), ت (6th)
- Remove 5th mutaḥarrik (ل): م-ُ ف-َ ا ع-َ ت-ُ ن-ْ
- **Result:** مُفَاعَتُنْ (mufāʿatun) - Note: This is unusual
- **OR** Classical: Remove position 5 → م-ُ ف-َ ا ع-َ ت-ُ ن-ْ = مُفَاعِتُنْ (mufāʿitun)
- **Pattern change:** `//o///o` → `//o//o`

**Frequency:** Common in al-Wāfir

**Code Verification:**
```
Location: meters.py:286, zihafat.py:326-336
Status: ⚠️ NEEDS TESTING
Pattern //o///o has 5 '/' characters
Expected to remove 5th '/' → //o//o
Actual behavior: UNTESTED
```

**⚠️ REQUIRES TESTING**

---

### Position 2: مُفَاعَلَتُنْ (mufāʿalatun)

**[Same as Position 1]**

- عَصْب (ʿAṣb): Allowed, needs testing

---

### Position 3 (FINAL): فَعُولُنْ (faʿūlun)

#### Base Form
- **Arabic:** فَعُولُنْ
- **Pattern:** `/o//o`
- **[Full details same as al-Ṭawīl Position 1]**

#### Allowed Ziḥāfāt

##### 1. قَبْض (Qabḍ) - Remove 5th/Last Sākin

**Application to فَعُولُنْ:**
- **Result:** فَعُولُ
- **Pattern change:** `/o//o` → `/o//`

**Code Verification:**
```
Test Result: /o//o → /o// ✅ PASS
Status: Works correctly (accidentally)
```

#### Allowed ʿIlal

##### 1. قَطْع (Qaṭʿ)

**Code Status:** Allowed in final position

**Verification:** Needs testing

---

## Summary Statistics

### Code Implementation
```python
AL_WAFIR = Meter(
    id=4,
    name_ar="الوافر",
    name_en="al-Wafir",
    tier=MeterTier.TIER_1,
    frequency_rank=4,
    base_tafail=[
        TAFAIL_BASE["مفاعلتن"],
        TAFAIL_BASE["مفاعلتن"],
        TAFAIL_BASE["فعولن"],
    ],
    rules_by_position={
        1: MeterRules(allowed_zihafat=[ASB]),
        2: MeterRules(allowed_zihafat=[ASB]),
        3: MeterRules(allowed_zihafat=[QABD], allowed_ilal=[QAT], is_final=True),
    },
    description="بحر موسيقي جميل، كثير الاستعمال في العصر الحديث",
)
```

### Verification Results

**Total Rules Checked:** 8
**Issues Found:**
- ✅ QABD on فعولن: Works
- ⚠️ ʿAṣB on مفاعلتن: UNTESTED
- ⚠️ QAṬ ʿillah: UNTESTED

**Status:** ⚠️ **PARTIALLY VERIFIED** - Main ziḥāf (ʿAṣb) needs testing

---

## Critical Issues

### Issue 1: ʿAṢB Transformation Untested (MEDIUM)

**Pattern:** `//o///o` (5 '/' characters)
**Expected:** Remove 5th '/' → `//o//o`
**Actual:** **UNKNOWN - NEEDS TESTING**

**Test Required:**
```python
result = asb_transform("//o///o")
expected = "//o//o"
# Does it work?
```

**If broken:** Would severely impact al-Wāfir detection

---

## Example Verses

**Verse:**
```
سَلامٌ مِن صَبا بَرَدى أَرَقُّ ** وَدَمعٌ لا يُكَفكَفُ يا دِمَشقُ
```

**Poet:** أحمد شوقي (Aḥmad Shawqī)
**Era:** Modern (20th century)
**Note:** Al-Wāfir very popular in modern Arabic poetry

---

## Recommendations

### IMMEDIATE
1. **Test ʿAṢB transformation** on pattern `//o///o`
2. **Test QAṬ ʿillah** application

### If ʿAṢB is broken:
3. **Implement fix** following same pattern-level workaround approach

---

## Document Metadata

- **Version:** 1.0
- **Date:** 2025-11-13
- **Status:** ⚠️ **NEEDS TESTING** - Primary ziḥāf not verified
- **Next:** الرجز (al-Rajaz) - Meter 5
