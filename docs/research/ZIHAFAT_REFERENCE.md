# Zihafat Reference - Complete 16 Classical Arabic Meters

**Purpose:** Authoritative reference for Zihafat (زحافات) and 'Ilal (علل) rules across all 16 classical Arabic meters.

**Version:** 1.0 (16 meters)
**Date:** November 12, 2025
**Source:** Classical Arabic prosody (الخليل بن أحمد, ابن عبد ربه) + Golden Set analysis

---

## Table of Contents

1. [Introduction](#introduction)
2. [Notation System](#notation-system)
3. [Tier 1: Common Meters (9)](#tier-1-common-meters)
4. [Tier 2: Medium Frequency Meters (2)](#tier-2-medium-frequency-meters)
5. [Tier 3: Rare Meters (5)](#tier-3-rare-meters)
6. [Cross-Meter Zihafat Summary](#cross-meter-zihafat-summary)
7. [Implementation Notes](#implementation-notes)

---

## Introduction

### What are Zihafat?

**Zihafat (زحافات)** are permitted prosodic variations that transform base tafa'il (prosodic feet) into valid variations. They follow strict linguistic rules defined by classical Arabic prosody scholars.

**Key Principles:**
1. **Zihafat** apply to non-final tafa'il (optional, meter-dependent)
2. **'Ilal (علل)** apply to final tafa'il only (end-of-verse changes)
3. Not all zihafat are allowed in all positions or meters
4. Some zihafat are common (frequent), others rare

### Types of Zihafat

#### Single Zihafat (زحافات مفردة)
- **خَبْن (Khabn):** Remove 2nd sakin letter
- **طَيّ (Tayy):** Remove 4th sakin letter
- **قَبْض (Qabd):** Remove 5th sakin letter
- **كَفّ (Kaff):** Remove 7th sakin letter
- **وَقْص (Waqs):** Remove 2nd mutaharrik letter
- **عَصْب ('Asb):** Remove 5th mutaharrik letter
- **عَقْل ('Aql):** Remove 5th sakin letter (in some meters)
- **إضمار (Idmar):** Make 2nd letter sakin

#### Double Zihafat (زحافات مزدوجة)
- **خَبْل (Khabl):** Khabn + Tayy
- **خَزْل (Khazl):** Idmar + Tayy
- **شَكْل (Shakl):** Khabn + Kaff

#### 'Ilal (Final Position Only)
- **حَذْف (Hadhf):** Remove last sabab
- **قَطْع (Qat'):** Make last letter sakin + remove preceding letter
- **قَصْر (Qasr):** Make last letter sakin
- **بَتْر (Batr):** Remove last sabab + make sakin

---

## Notation System

### Phonetic Patterns
- `/` = haraka (short vowel: fatha, damma, kasra)
- `o` = sakin (sukun or long vowel continuation)
- Example: `/o//o` = "فَعُولُنْ" (fa-'ū-lun)

### Prosodic Structure
- **Sabab Khafif (ب خ):** Two letters, first mutaharrik, second sakin (e.g., "فَعْ")
- **Sabab Thaqil (ب ث):** Two mutaharrik letters (e.g., "فَعَ")
- **Watad Majmu' (و م):** Three letters: mut., mut., sakin (e.g., "فَعُولْ")
- **Watad Mafruq (و ف):** Three letters: mut., sakin, mut. (e.g., "فَاعِ")

---

## Tier 1: Common Meters

### 1. الطويل (al-Tawil) - "The Long"

**Frequency Rank:** 1 (Most common)
**Usage:** ~30% of classical poetry

#### Base Pattern
```
فَعُولُنْ مَفَاعِيلُنْ فَعُولُنْ مَفَاعِيلُنْ
/o//o   //o/o/o   /o//o   //o/o/o
```

#### Allowed Zihafat

**Position 1: فَعُولُنْ**
| Zahaf | Type | Result | Phonetic | Frequency |
|-------|------|--------|----------|-----------|
| Base | - | فَعُولُنْ | `/o//o` | Very Common |
| قَبْض | Single | فَعُولُ | `/o//` | Common |
| كَفّ | Single | فَعُلُنْ | `/o/o` | Rare |

**Position 2: مَفَاعِيلُنْ**
| Zahaf | Type | Result | Phonetic | Frequency |
|-------|------|--------|----------|-----------|
| Base | - | مَفَاعِيلُنْ | `//o/o/o` | Common |
| قَبْض | Single | مَفَاعِلُنْ | `///o/o` | Very Common |
| كَفّ | Single | مَفَاعِيلُ | `//o/o/` | Rare |

**Position 3: فَعُولُنْ** (same as Position 1)

**Position 4: مَفَاعِيلُنْ** (final position)
| Zahaf/'Ilal | Type | Result | Phonetic | Frequency |
|-------------|------|--------|----------|-----------|
| Base | - | مَفَاعِيلُنْ | `//o/o/o` | Common |
| قَبْض | Single | مَفَاعِلُنْ | `///o/o` | Very Common |
| قَصْر | 'Ilah | مَفَاعِيلُ | `//o/o/` | Common |
| حَذْف | 'Ilah | مَفَاعِي | `//o/o` | Rare |

#### Valid Pattern Count
- Theoretical: 3 × 2 × 3 × 4 = **72 valid patterns**
- Commonly observed: ~25-30 patterns

#### Classical Sources
- الخليل بن أحمد: "أصل الطويل وأشرف البحور"
- Evidence: معلقات (all 7 use الطويل or variations)

---

### 2. الكامل (al-Kamil) - "The Perfect"

**Frequency Rank:** 2
**Usage:** ~20% of classical poetry

#### Base Pattern
```
مُتَفَاعِلُنْ مُتَفَاعِلُنْ مُتَفَاعِلُنْ
///o//o   ///o//o   ///o//o
```

#### Allowed Zihafat

**Positions 1, 2: مُتَفَاعِلُنْ**
| Zahaf | Type | Result | Phonetic | Frequency |
|-------|------|--------|----------|-----------|
| Base | - | مُتَفَاعِلُنْ | `///o//o` | Common |
| إضمار | Single | مُتْفَاعِلُنْ | `//o//o` | Very Common |
| وَقْص | Single | مُفَاعِلُنْ | `///o/o` | Rare |

**Position 3: مُتَفَاعِلُنْ** (final position)
| Zahaf/'Ilal | Type | Result | Phonetic | Frequency |
|-------------|------|--------|----------|-----------|
| Base | - | مُتَفَاعِلُنْ | `///o//o` | Common |
| إضمار | Single | مُتْفَاعِلُنْ | `//o//o` | Very Common |
| حَذْف | 'Ilah | مُتَفَاعِلْ | `///o//` | Common |
| قَطْع | 'Ilah | مُتَفَاعِلانْ | `///o//oo` | Rare |

#### Valid Pattern Count
- Theoretical: 3 × 3 × 4 = **36 valid patterns**
- Commonly observed: ~16 patterns

#### Classical Sources
- "الكامل في القوة والجزالة"
- Famous users: البحتري, أبو تمام, محمود درويش

---

### 3. البسيط (al-Basit) - "The Simple"

**Frequency Rank:** 3
**Usage:** ~12% of classical poetry

#### Base Pattern
```
مُسْتَفْعِلُنْ فَاعِلُنْ مُسْتَفْعِلُنْ فَاعِلُنْ
/o/o//o    /o//o   /o/o//o    /o//o
```

#### Allowed Zihafat

**Positions 1, 3: مُسْتَفْعِلُنْ**
| Zahaf | Type | Result | Phonetic | Frequency |
|-------|------|--------|----------|-----------|
| Base | - | مُسْتَفْعِلُنْ | `/o/o//o` | Common |
| خَبْن | Single | مُتَفْعِلُنْ | `//o//o` | Common |
| طَيّ | Single | مَفَاعِلُنْ | `///o/o` | Rare |
| خَبْل | Double | فَاعِلُنْ | `/o//o` | Very Rare |

**Positions 2, 4: فَاعِلُنْ**
| Zahaf/'Ilal | Type | Result | Phonetic | Frequency |
|-------------|------|--------|----------|-----------|
| Base | - | فَاعِلُنْ | `/o//o` | Common |
| خَبْن | Single | فَعِلُنْ | `///o` | Very Common |
| قَطْع (final) | 'Ilah | فَاعِلانْ | `/o//oo` | Rare |

#### Valid Pattern Count
- Theoretical: 4 × 2 × 4 × 2 = **64 valid patterns**
- Commonly observed: ~15 patterns

---

### 4. الوافر (al-Wafir) - "The Abundant"

**Frequency Rank:** 4
**Usage:** ~10% of classical poetry

#### Base Pattern
```
مُفَاعَلَتُنْ مُفَاعَلَتُنْ فَعُولُنْ
//o///o    //o///o    /o//o
```

#### Allowed Zihafat

**Positions 1, 2: مُفَاعَلَتُنْ**
| Zahaf | Type | Result | Phonetic | Frequency |
|-------|------|--------|----------|-----------|
| Base | - | مُفَاعَلَتُنْ | `//o///o` | Common |
| عَصْب | Single | مُفَاعَلْتُنْ | `//o//o` | Very Common |
| عَقْل | Single | مُفَاعَتُنْ | `//o//o` | Rare (variant) |

**Position 3: فَعُولُنْ** (final)
| Zahaf/'Ilal | Type | Result | Phonetic | Frequency |
|-------------|------|--------|----------|-----------|
| Base | - | فَعُولُنْ | `/o//o` | Very Common |
| قَبْض | Single | فَعُولُ | `/o//` | Common |
| قَطْع | 'Ilah | فَعُولانْ | `/o//oo` | Rare |

#### Valid Pattern Count
- Theoretical: 3 × 3 × 3 = **27 valid patterns**
- Commonly observed: ~13 patterns

---

### 5. الرجز (al-Rajaz) - "The Trembling"

**Frequency Rank:** 5
**Usage:** ~8% of classical poetry (higher in urjūza)

#### Base Pattern
```
مُسْتَفْعِلُنْ مُسْتَفْعِلُنْ مُسْتَفْعِلُنْ
/o/o//o    /o/o//o    /o/o//o
```

#### Allowed Zihafat

**Positions 1, 2: مُسْتَفْعِلُنْ**
| Zahaf | Type | Result | Phonetic | Frequency |
|-------|------|--------|----------|-----------|
| Base | - | مُسْتَفْعِلُنْ | `/o/o//o` | Common |
| خَبْن | Single | مُتَفْعِلُنْ | `//o//o` | Very Common |
| طَيّ | Single | مَفَاعِلُنْ | `///o/o` | Common |
| خَبْل | Double | فَعِلُنْ | `///o` | Rare |

**Position 3: مُسْتَفْعِلُنْ** (final)
| Zahaf/'Ilal | Type | Result | Phonetic | Frequency |
|-------------|------|--------|----------|-----------|
| Base | - | مُسْتَفْعِلُنْ | `/o/o//o` | Common |
| خَبْن | Single | مُتَفْعِلُنْ | `//o//o` | Very Common |
| قَطْع | 'Ilah | مُسْتَفْعِلانْ | `/o/o//oo` | Rare |
| قَصْر | 'Ilah | مُسْتَفْعِلُ | `/o/o//` | Common |

#### Valid Pattern Count
- Theoretical: 4 × 4 × 5 = **80 valid patterns**
- Commonly observed: ~8 patterns (very consistent meter)

---

### 6. الرمل (ar-Ramal) - "The Sand"

**Frequency Rank:** 6
**Usage:** ~7% of classical poetry

#### Base Pattern
```
فَاعِلَاتُنْ فَاعِلَاتُنْ فَاعِلَاتُنْ
/o//o/o    /o//o/o    /o//o/o
```

#### Allowed Zihafat

**Positions 1, 2: فَاعِلَاتُنْ**
| Zahaf | Type | Result | Phonetic | Frequency |
|-------|------|--------|----------|-----------|
| Base | - | فَاعِلَاتُنْ | `/o//o/o` | Common |
| خَبْن | Single | فَعِلَاتُنْ | `///o/o` | Common |
| كَفّ | Single | فَاعِلَاتُ | `/o//o/` | Rare |
| شَكْل | Double | فَعِلَاتُ | `///o/` | Very Rare |

**Position 3: فَاعِلَاتُنْ** (final)
| Zahaf/'Ilal | Type | Result | Phonetic | Frequency |
|-------------|------|--------|----------|-----------|
| Base | - | فَاعِلَاتُنْ | `/o//o/o` | Common |
| خَبْن | Single | فَعِلَاتُنْ | `///o/o` | Common |
| حَذْف | 'Ilah | فَاعِلُنْ | `/o//o` | Very Common |
| حَذْف+خَبْن | Combined | فَعِلُنْ | `///o` | Common |

#### Valid Pattern Count
- Theoretical: 4 × 4 × 5 = **80 valid patterns**
- Commonly observed: ~13 patterns

---

### 7. الخفيف (al-Khafif) - "The Light"

**Frequency Rank:** 7
**Usage:** ~6% of classical poetry

#### Base Pattern
```
فَاعِلَاتُنْ مُسْتَفْعِلُنْ فَاعِلَاتُنْ
/o//o/o    /o/o//o    /o//o/o
```

#### Allowed Zihafat

**Position 1: فَاعِلَاتُنْ**
| Zahaf | Type | Result | Phonetic | Frequency |
|-------|------|--------|----------|-----------|
| Base | - | فَاعِلَاتُنْ | `/o//o/o` | Common |
| خَبْن | Single | فَعِلَاتُنْ | `///o/o` | Common |

**Position 2: مُسْتَفْعِلُنْ**
| Zahaf | Type | Result | Phonetic | Frequency |
|-------|------|--------|----------|-----------|
| Base | - | مُسْتَفْعِلُنْ | `/o/o//o` | Common |
| خَبْن | Single | مُتَفْعِلُنْ | `//o//o` | Common |
| طَيّ | Single | مَفَاعِلُنْ | `///o/o` | Rare |

**Position 3: فَاعِلَاتُنْ** (final)
| Zahaf/'Ilal | Type | Result | Phonetic | Frequency |
|-------------|------|--------|----------|-----------|
| Base | - | فَاعِلَاتُنْ | `/o//o/o` | Common |
| خَبْن | Single | فَعِلَاتُنْ | `///o/o` | Common |
| حَذْف | 'Ilah | فَاعِلُنْ | `/o//o` | Very Common |
| حَذْف+خَبْن | Combined | فَعِلُنْ | `///o` | Common |

#### Valid Pattern Count
- Theoretical: 2 × 3 × 4 = **24 valid patterns**
- Commonly observed: ~9 patterns

---

### 8. المتقارب (al-Mutaqarib) - "The Convergent"

**Frequency Rank:** 11
**Usage:** ~3% of classical poetry

#### Base Pattern
```
فَعُولُنْ فَعُولُنْ فَعُولُنْ فَعُولُنْ
/o//o   /o//o   /o//o   /o//o
```

#### Allowed Zihafat

**Positions 1-3: فَعُولُنْ**
| Zahaf | Type | Result | Phonetic | Frequency |
|-------|------|--------|----------|-----------|
| Base | - | فَعُولُنْ | `/o//o` | Very Common |
| قَبْض | Single | فَعُولُ | `/o//` | Common |

**Position 4: فَعُولُنْ** (final)
| Zahaf/'Ilal | Type | Result | Phonetic | Frequency |
|-------------|------|--------|----------|-----------|
| Base | - | فَعُولُنْ | `/o//o` | Common |
| قَبْض | Single | فَعُولُ | `/o//` | Common |
| حَذْف | 'Ilah | فَعُو | `/o/` | Common |
| قَطْع | 'Ilah | فَعُولانْ | `/o//oo` | Rare |

#### Valid Pattern Count
- Theoretical: 2 × 2 × 2 × 4 = **32 valid patterns**
- Commonly observed: ~10 patterns

---

### 9. الهزج (al-Hazaj) - "The Rhythmic"

**Frequency Rank:** 12
**Usage:** ~2% of classical poetry

#### Base Pattern
```
مَفَاعِيلُنْ مَفَاعِيلُنْ (فَعُولُنْ)
//o/o/o    //o/o/o    (/o//o)
```

*Note: فَعُولُنْ at end is optional*

#### Allowed Zihafat

**Positions 1, 2: مَفَاعِيلُنْ**
| Zahaf | Type | Result | Phonetic | Frequency |
|-------|------|--------|----------|-----------|
| Base | - | مَفَاعِيلُنْ | `//o/o/o` | Common |
| قَبْض | Single | مَفَاعِلُنْ | `///o/o` | Common |
| كَفّ | Single | مَفَاعِيلُ | `//o/o/` | Rare |

**Position 3 (optional): فَعُولُنْ**
| Zahaf/'Ilal | Type | Result | Phonetic | Frequency |
|-------------|------|--------|----------|-----------|
| Base | - | فَعُولُنْ | `/o//o` | Common |
| قَبْض | Single | فَعُولُ | `/o//` | Common |
| حَذْف | 'Ilah | فَعُو | `/o/` | Rare |
| *Omitted* | - | - | - | Very Common |

#### Valid Pattern Count
- Theoretical: 3 × 3 × 5 = **45 valid patterns** (with optional foot)
- Commonly observed: ~7 patterns

---

## Tier 2: Medium Frequency Meters

### 10. السريع (as-Sari') - "The Fast"

**Frequency Rank:** 8
**Usage:** ~5% of classical poetry

#### Base Pattern
```
مُسْتَفْعِلُنْ مُسْتَفْعِلُنْ فَاعِلُنْ
/o/o//o    /o/o//o    /o//o
```

#### Allowed Zihafat

**Positions 1, 2: مُسْتَفْعِلُنْ**
| Zahaf | Type | Result | Phonetic | Frequency |
|-------|------|--------|----------|-----------|
| Base | - | مُسْتَفْعِلُنْ | `/o/o//o` | Common |
| خَبْن | Single | مُتَفْعِلُنْ | `//o//o` | Very Common |
| طَيّ | Single | مَفَاعِلُنْ | `///o/o` | Common |
| خَبْل | Double | فَعِلُنْ | `///o` | Rare |

**Position 3: فَاعِلُنْ** (final)
| Zahaf/'Ilal | Type | Result | Phonetic | Frequency |
|-------------|------|--------|----------|-----------|
| Base | - | فَاعِلُنْ | `/o//o` | Common |
| خَبْن | Single | فَعِلُنْ | `///o` | Common |
| كَشْف | 'Ilah | فَاعِلا | `/o///` | Rare |
| قَصْر | 'Ilah | فَاعِلْ | `/o//` | Common |

#### Valid Pattern Count
- Theoretical: 4 × 4 × 4 = **64 valid patterns**
- Estimated: ~20 patterns

#### Classical Sources
- أبو العلاء المعري (frequent user)
- Used in wisdom poetry and maxims

---

### 11. المديد (al-Madid) - "The Extended"

**Frequency Rank:** 9
**Usage:** ~4% of classical poetry

#### Base Pattern
```
فَاعِلَاتُنْ فَاعِلُنْ فَاعِلَاتُنْ
/o//o/o    /o//o   /o//o/o
```

#### Allowed Zihafat

**Positions 1, 3: فَاعِلَاتُنْ**
| Zahaf | Type | Result | Phonetic | Frequency |
|-------|------|--------|----------|-----------|
| Base | - | فَاعِلَاتُنْ | `/o//o/o` | Common |
| خَبْن | Single | فَعِلَاتُنْ | `///o/o` | Very Common |
| كَفّ | Single | فَاعِلَاتُ | `/o//o/` | Rare |

**Position 2: فَاعِلُنْ**
| Zahaf | Type | Result | Phonetic | Frequency |
|-------|------|--------|----------|-----------|
| Base | - | فَاعِلُنْ | `/o//o` | Common |
| خَبْن | Single | فَعِلُنْ | `///o` | Common |

**Position 3 (final): فَاعِلَاتُنْ**
| Zahaf/'Ilal | Type | Result | Phonetic | Frequency |
|-------------|------|--------|----------|-----------|
| Base | - | فَاعِلَاتُنْ | `/o//o/o` | Common |
| خَبْن | Single | فَعِلَاتُنْ | `///o/o` | Very Common |
| حَذْف | 'Ilah | فَاعِلُنْ | `/o//o` | Common |
| قَصْر | 'Ilah | فَاعِلَاتْ | `/o//o/` | Rare |

#### Valid Pattern Count
- Theoretical: 3 × 2 × 4 = **24 valid patterns**
- Estimated: ~15 patterns

#### Classical Sources
- البحتري, أبو نواس
- Popular in غزل (love poetry)

---

## Tier 3: Rare Meters

### 12. المنسرح (al-Munsarih) - "The Flowing"

**Frequency Rank:** 10
**Usage:** ~3% of classical poetry

#### Base Pattern
```
مُسْتَفْعِلُنْ مَفْعُولَاتُ مُفْتَعِلُنْ
/o/o//o    /o/o//o   /o/o//o
```

*Note: Complex meter with مَفْعُولَاتُ (maf'ūlātu) - watad mafruq structure*

#### Allowed Zihafat

**Position 1: مُسْتَفْعِلُنْ**
| Zahaf | Type | Result | Phonetic | Frequency |
|-------|------|--------|----------|-----------|
| Base | - | مُسْتَفْعِلُنْ | `/o/o//o` | Common |
| خَبْن | Single | مُتَفْعِلُنْ | `//o//o` | Common |
| طَيّ | Single | مَفَاعِلُنْ | `///o/o` | Rare |

**Position 2: مَفْعُولَاتُ**
| Zahaf | Type | Result | Phonetic | Frequency |
|-------|------|--------|----------|-----------|
| Base | - | مَفْعُولَاتُ | `/o/o//o` | Common |
| طَيّ | Single | مَفْعُلَاتُ | `/o///o` | Rare |

**Position 3: مُفْتَعِلُنْ** (final)
| Zahaf/'Ilal | Type | Result | Phonetic | Frequency |
|-------------|------|--------|----------|-----------|
| Base | - | مُفْتَعِلُنْ | `/o/o//o` | Common |
| كَشْف | 'Ilah | مُفْتَعِلا | `/o/o///` | Rare |

#### Valid Pattern Count
- Theoretical: 3 × 2 × 2 = **12 valid patterns**
- Very rare in practice

#### Classical Sources
- المتنبي (rare usage)
- "منساح السياق" - flowing rhythm

---

### 13. المجتث (al-Mujtathth) - "The Uprooted"

**Frequency Rank:** 13
**Usage:** <2% of classical poetry

#### Base Pattern
```
مُسْتَفْعِلُنْ فَاعِلَاتُنْ
/o/o//o    /o//o/o
```

*Note: "Uprooted" from البسيط*

#### Allowed Zihafat

**Position 1: مُسْتَفْعِلُنْ**
| Zahaf | Type | Result | Phonetic | Frequency |
|-------|------|--------|----------|-----------|
| Base | - | مُسْتَفْعِلُنْ | `/o/o//o` | Common |
| خَبْن | Single | مُتَفْعِلُنْ | `//o//o` | Common |

**Position 2: فَاعِلَاتُنْ** (final)
| Zahaf/'Ilal | Type | Result | Phonetic | Frequency |
|-------------|------|--------|----------|-----------|
| Base | - | فَاعِلَاتُنْ | `/o//o/o` | Common |
| خَبْن | Single | فَعِلَاتُنْ | `///o/o` | Common |
| حَذْف | 'Ilah | فَاعِلُنْ | `/o//o` | Common |

#### Valid Pattern Count
- Theoretical: 2 × 3 = **6 valid patterns**
- Very limited usage

---

### 14. المقتضب (al-Muqtadab) - "The Condensed"

**Frequency Rank:** 14
**Usage:** <2% of classical poetry

#### Base Pattern
```
مَفْعُولَاتُ مُسْتَفْعِلُنْ
/o/o//o   /o/o//o
```

#### Allowed Zihafat

**Position 1: مَفْعُولَاتُ**
| Zahaf | Type | Result | Phonetic | Frequency |
|-------|------|--------|----------|-----------|
| Base | - | مَفْعُولَاتُ | `/o/o//o` | Common |
| طَيّ | Single | مَفْعُلَاتُ | `/o///o` | Rare |

**Position 2: مُسْتَفْعِلُنْ** (final)
| Zahaf/'Ilal | Type | Result | Phonetic | Frequency |
|-------------|------|--------|----------|-----------|
| Base | - | مُسْتَفْعِلُنْ | `/o/o//o` | Common |
| خَبْن | Single | مُتَفْعِلُنْ | `//o//o` | Common |
| قَطْع | 'Ilah | مُسْتَفْعِلانْ | `/o/o//oo` | Rare |

#### Valid Pattern Count
- Theoretical: 2 × 3 = **6 valid patterns**
- Extremely rare

---

### 15. المضارع (al-Mudari') - "The Resembling"

**Frequency Rank:** 15
**Usage:** <1% of classical poetry

#### Base Pattern
```
مَفَاعِيلُنْ فَاعِلَاتُنْ
//o/o/o   /o//o/o
```

*Note: Resembles الهزج*

#### Allowed Zihafat

**Position 1: مَفَاعِيلُنْ**
| Zahaf | Type | Result | Phonetic | Frequency |
|-------|------|--------|----------|-----------|
| Base | - | مَفَاعِيلُنْ | `//o/o/o` | Common |
| قَبْض | Single | مَفَاعِلُنْ | `///o/o` | Common |

**Position 2: فَاعِلَاتُنْ** (final)
| Zahaf/'Ilal | Type | Result | Phonetic | Frequency |
|-------------|------|--------|----------|-----------|
| Base | - | فَاعِلَاتُنْ | `/o//o/o` | Common |
| خَبْن | Single | فَعِلَاتُنْ | `///o/o` | Common |
| حَذْف | 'Ilah | فَاعِلُنْ | `/o//o` | Rare |

#### Valid Pattern Count
- Theoretical: 2 × 3 = **6 valid patterns**
- Almost never used

---

### 16. المتدارك (al-Mutadarik) - "The Overtaking"

**Frequency Rank:** 16
**Usage:** <1% of classical poetry

#### Base Pattern
```
فَاعِلُنْ فَاعِلُنْ فَاعِلُنْ فَاعِلُنْ
/o//o   /o//o   /o//o   /o//o
```

*Note: 16th meter, discovered by الأخفش*

#### Allowed Zihafat

**Positions 1-3: فَاعِلُنْ**
| Zahaf | Type | Result | Phonetic | Frequency |
|-------|------|--------|----------|-----------|
| Base | - | فَاعِلُنْ | `/o//o` | Common |
| خَبْن | Single | فَعِلُنْ | `///o` | Very Common |

**Position 4: فَاعِلُنْ** (final)
| Zahaf/'Ilal | Type | Result | Phonetic | Frequency |
|-------------|------|--------|----------|-----------|
| Base | - | فَاعِلُنْ | `/o//o` | Common |
| خَبْن | Single | فَعِلُنْ | `///o` | Very Common |
| حَذْف | 'Ilah | فَاعِ | `/o/` | Rare |
| قَصْر | 'Ilah | فَاعِلْ | `/o//` | Rare |

#### Valid Pattern Count
- Theoretical: 2 × 2 × 2 × 4 = **32 valid patterns**
- Very rare meter

#### Classical Sources
- "استدركه الأخفش على الخليل"
- Also called "الخبب" or "المحدث"

---

## Cross-Meter Zihafat Summary

### Most Common Zihafat (Across All Meters)

| Zahaf | Arabic | Frequency | Meters |
|-------|--------|-----------|--------|
| **خَبْن** | Khabn | Very High | البسيط, الرجز, الخفيف, الرمل, المديد, السريع, المتدارك, المجتث |
| **قَبْض** | Qabd | High | الطويل, الهزج, المضارع, المتقارب |
| **إضمار** | Idmar | High | الكامل |
| **عَصْب** | 'Asb | Medium | الوافر |
| **طَيّ** | Tayy | Medium | البسيط, الرجز, الخفيف, السريع, المنسرح |
| **كَفّ** | Kaff | Low | الطويل, الهزج, الرمل, المديد |

### Most Common 'Ilal (Final Position)

| 'Ilah | Arabic | Frequency | Meters |
|-------|--------|-----------|--------|
| **حَذْف** | Hadhf | Very High | الرمل, الخفيف, المتقارب, الهزج, المديد, المضارع, المتدارك |
| **قَصْر** | Qasr | High | الطويل, الرجز, السريع, المديد, المتدارك |
| **قَطْع** | Qat' | Low | البسيط, الوافر, المتقارب, المقتضب |
| **كَشْف** | Kashf | Low | السريع, المنسرح |

---

## Implementation Notes

### Priority for Implementation

**Phase 1 (Weeks 1-2): Tier 1 - 9 Common Meters**
- Covers 85% of actual poetry
- Well-documented Zihafat
- Abundant test data available

**Phase 2 (Weeks 3-4): Tier 2 - 2 Medium Meters**
- Adds السريع, المديد
- Increases coverage to 95%
- Moderate test data available

**Phase 3 (Weeks 5-6): Tier 3 - 5 Rare Meters**
- Completes all 16 classical meters
- Limited test data (may require synthesis)
- Accept lower accuracy (≥75%) for <1% usage meters

### Data Structure Mapping

```python
# Example for الطويل
AL_TAWIL = Meter(
    id=1,
    name_ar="الطويل",
    base_tafail=[
        Tafila("فعولن", "/o//o", structure="sabab+watad"),
        Tafila("مفاعيلن", "//o/o/o", structure="sabab+sabab+watad"),
        Tafila("فعولن", "/o//o", structure="sabab+watad"),
        Tafila("مفاعيلن", "//o/o/o", structure="sabab+sabab+watad"),
    ],
    allowed_zihafat={
        "فعولن": {
            "allowed": [
                Zahaf("قبض", target="last_sakin", result="/o//"),
                Zahaf("كف", target="watad_vowel", result="/o/o"),
            ],
            "positions": [1, 3]
        },
        "مفاعيلن": {
            "allowed": [
                Zahaf("قبض", target="5th_sakin", result="///o/o"),
                Zahaf("كف", target="7th_sakin", result="//o/o/"),
            ],
            "positions": [2, 4]
        }
    },
    allowed_ilal={
        4: [
            Ilah("قصر", result="//o/o/"),
            Ilah("حذف", result="//o/o"),
        ]
    }
)
```

### Testing Strategy

**Tier 1 (9 meters):**
- Golden Set: 118 verses
- Target accuracy: ≥97.5%
- Generalization: ≥95%

**Tier 2 (2 meters):**
- Golden Set: 20+ verses (to collect)
- Target accuracy: ≥85%
- Generalization: ≥80%

**Tier 3 (5 meters):**
- Test Set: 10-30 verses (synthetic + authentic)
- Target accuracy: ≥75%
- Generalization: ≥70%

---

## Classical References

### Primary Sources
1. **الخليل بن أحمد الفراهيدي** - كتاب العروض (foundational text)
2. **ابن عبد ربه** - العقد الفريد (العروض section)
3. **الأخفش الأوسط** - discovered المتدارك (16th meter)

### Modern References
4. **Dr. إبراهيم أنيس** - موسيقى الشعر
5. **Dr. عبد العزيز عتيق** - علم العروض والقافية
6. **Dr. غازي يموت** - بحور الشعر العربي

### Digital Sources
7. **المكتبة الشاملة** - Comprehensive poetry corpus
8. **الموسوعة الشعرية** - 200,000+ verses with meter tags

---

**Document Version:** 1.0
**Completion Status:** ✅ All 16 meters documented
**Last Updated:** November 12, 2025
**Next Steps:** Implement data structures (Phase 2)

---

## Appendix: Quick Reference Table

| # | Meter | Arabic | Base Tafa'il Count | Zihafat Count | Pattern Variations | Frequency |
|---|-------|--------|--------------------|---------------|-------------------|-----------|
| 1 | الطويل | al-Tawil | 4 | 6 | ~72 | 30% |
| 2 | الكامل | al-Kamil | 3 | 4 | ~36 | 20% |
| 3 | البسيط | al-Basit | 4 | 6 | ~64 | 12% |
| 4 | الوافر | al-Wafir | 3 | 6 | ~27 | 10% |
| 5 | الرجز | al-Rajaz | 3 | 8 | ~80 | 8% |
| 6 | الرمل | ar-Ramal | 3 | 9 | ~80 | 7% |
| 7 | الخفيف | al-Khafif | 3 | 9 | ~24 | 6% |
| 8 | السريع | as-Sari' | 3 | 8 | ~64 | 5% |
| 9 | المديد | al-Madid | 3 | 7 | ~24 | 4% |
| 10 | المنسرح | al-Munsarih | 3 | 5 | ~12 | 3% |
| 11 | المتقارب | al-Mutaqarib | 4 | 6 | ~32 | 3% |
| 12 | الهزج | al-Hazaj | 2-3 | 7 | ~45 | 2% |
| 13 | المجتث | al-Mujtathth | 2 | 5 | ~6 | <2% |
| 14 | المقتضب | al-Muqtadab | 2 | 5 | ~6 | <2% |
| 15 | المضارع | al-Mudari' | 2 | 5 | ~6 | <1% |
| 16 | المتدارك | al-Mutadarik | 4 | 6 | ~32 | <1% |

**Total Theoretical Patterns:** ~600+ across all 16 meters
**MVP Coverage (9 meters):** ~450 patterns (85% of poetry)
**Full Coverage (16 meters):** ~600 patterns (100% of poetry)
