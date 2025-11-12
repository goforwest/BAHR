# BAHR API V2 - User Guide
## Enhanced Prosodic Analysis with Complete Explainability

### 🎯 What's New in V2?

BAHR API V2 brings **complete transparency and explainability** to Arabic poetry analysis. Unlike traditional "black box" AI systems, V2 shows you exactly how it arrived at its conclusions using classical Arabic prosody rules.

---

## ✨ Key Features

### 1. **Complete Explainability**
See exactly which prosodic variations (Zihafat and 'Ilal) were applied at each position:
```json
{
  "transformations": ["base", "قبض", "base", "حذف"]
}
```
This tells you: *"The verse uses the base form in positions 1 and 3, قبض (qabd) in position 2, and حذف (hadhf) at the end."*

### 2. **Match Quality Indicators**
Understand how confident the detection is:
- **`exact`** - Perfect match with the base pattern (no variations)
- **`strong`** - Match with common, well-attested variations
- **`moderate`** - Match with rare or multiple variations
- **`weak`** - Match with very rare combinations

### 3. **Bilingual Explanations**
Get explanations in both Arabic and English:
```json
{
  "explanation_ar": "مطابقة مع زحافات: قبض في الموضع الثاني",
  "explanation_en": "Match with variations: qabd at position 2"
}
```

### 4. **Phonetic Pattern Visualization**
See the exact phonetic pattern that matched:
```json
{
  "matched_pattern": "/o////o/o/o/o//o//o/o/o"
}
```
Where:
- `/` = haraka (short vowel) - moving syllable
- `o` = sukun (no vowel/long vowel) - still syllable

### 5. **Rule-Based Detection**
- **365+ valid patterns** generated from classical prosody rules
- Covers **all 16 classical Arabic meters**
- Not memorization - actual understanding of prosodic rules

---

## 🚀 Getting Started

### Endpoint

```
POST /api/v1/analyze-v2/
```

### Basic Request

```json
{
  "text": "قِفا نَبْكِ مِن ذِكرى حَبيبٍ ومَنْزِلِ",
  "detect_bahr": true,
  "suggest_corrections": true,
  "analyze_rhyme": true
}
```

### Response Structure

```json
{
  "text": "قِفا نَبْكِ مِن ذِكرى حَبيبٍ ومَنْزِلِ",
  "taqti3": "فَعُولُنْ مَفَاعِيلُنْ فَعُولُنْ مَفَاعِلُنْ",
  "bahr": {
    "id": 1,
    "name_ar": "الطويل",
    "name_en": "at-Tawil",
    "confidence": 0.97,

    // 🆕 NEW: Explainability fields
    "match_quality": "strong",
    "matched_pattern": "/o//o//o/o/o/o//o//o//o",
    "transformations": ["base", "base", "base", "قبض"],
    "explanation_ar": "مطابقة مع زحافات: قبض في الموضع الرابع",
    "explanation_en": "Match with variations: qabd at position 4"
  },
  "rhyme": {
    "rawi": "ل",
    "rawi_vowel": "i",
    "rhyme_types": ["مطلقة", "مجردة"],
    "description_ar": "القافية: روي:ل (مطلقة, مجردة)",
    "description_en": "Qafiyah: rawi=ل"
  },
  "errors": [],
  "suggestions": [
    "✓ التقطيع جيد مع زحاف واحد معتاد: قبض"
  ],
  "score": 97.0
}
```

---

## 📚 Understanding the Response

### Meter Detection Fields

#### `confidence` (0.0 - 1.0)
How confident the system is about the meter detection:
- **0.95+**: Very confident - this is almost certainly correct
- **0.85-0.95**: Confident - likely correct with minor variations
- **0.75-0.85**: Moderate - several variations present
- **< 0.75**: Low - unusual pattern or multiple rare variations

#### `match_quality`
Quality indicator for the match:
- **`exact`**: ✅ Perfect match - no prosodic variations applied
- **`strong`**: ✅ Good match - common variations (1-2 زحافات)
- **`moderate`**: ⚠️ Fair match - rare variations or multiple changes
- **`weak`**: ⚠️ Weak match - very rare combinations

#### `transformations`
Array showing what was applied at each taf'ila position:
```json
["base", "قبض", "base", "حذف"]
```
Means:
- **Position 1**: Base form (no variation)
- **Position 2**: قبض (qabd) applied
- **Position 3**: Base form
- **Position 4**: حذف (hadhf) applied at the end

Common transformations:
- **`base`**: No variation - original form
- **`قبض`** (qabd): Remove 5th sakin - very common in الطويل
- **`خبن`** (khabn): Remove 2nd sakin - common in many meters
- **`حذف`** (hadhf): Remove last sabab - end variation
- **`طي`** (tayy): Remove 4th sakin
- And more...

#### `matched_pattern`
The exact phonetic pattern that matched:
```
/o//o//o/o/o/o//o//o/o/o
```
Notation:
- `/` = haraka (متحرك) - consonant + short vowel
- `o` = sukun (ساكن) - consonant with sukun or long vowel

Example breakdown for `/o//o`:
1. `/` - consonant + short vowel (e.g., فَ)
2. `o` - sakin consonant (e.g., عْ)
3. `/` - consonant + short vowel (e.g., لُ)
4. `o` - sakin/long (e.g., ـن)
= **فَعُولُنْ** (fa'ūlun)

#### `explanation_ar` / `explanation_en`
Human-readable explanation of the match in both languages.

---

## 🎓 Educational Use Cases

### 1. **Learning Arabic Prosody**
Students can see exactly which variations are being applied:
```json
{
  "transformations": ["base", "قبض", "base", "base"],
  "explanation_ar": "مطابقة مع زحافات: قبض في الموضع الثاني"
}
```
This teaches: *"In this verse, the poet used قبض (removing the 5th sakin) in the second taf'ila, which is a common and acceptable variation in الطويل."*

### 2. **Poetry Composition Assistance**
Writers can understand if their verses follow proper meter:
```json
{
  "match_quality": "exact",
  "suggestions": ["✓ التقطيع دقيق ومتسق مع بحر الطويل (الصيغة الأساسية)"]
}
```

### 3. **Research and Analysis**
Scholars can analyze large corpora and see patterns:
```json
{
  "transformations": ["base", "قبض", "خبن", "حذف"],
  "match_quality": "moderate"
}
```
This might indicate: *"This poet frequently uses multiple zihafat in combination."*

---

## 🆚 V2 vs V1 Comparison

| Feature | V1 (Original) | V2 (Enhanced) |
|---------|---------------|---------------|
| **Meters Supported** | 9 common | All 16 classical |
| **Explainability** | ❌ None | ✅ Complete |
| **Pattern Coverage** | 111 hardcoded | 365+ rule-generated |
| **Transformations Shown** | ❌ No | ✅ Yes |
| **Match Quality** | ❌ No | ✅ Yes |
| **Bilingual Explanations** | ❌ No | ✅ Yes |
| **Educational Value** | Basic | High |
| **Confidence Scoring** | ✅ Yes | ✅ Yes (enhanced) |

---

## 💡 Best Practices

### 1. **Include Diacritics (Tashkeel)**
For best results, include diacritical marks:
```
✅ GOOD: "قِفا نَبْكِ مِن ذِكرى"
❌ LESS ACCURATE: "قفا نبك من ذكرى"
```

### 2. **One Verse Per Request**
Analyze one hemistich (شطر) or verse (بيت) at a time for accurate results.

### 3. **Check Match Quality**
Pay attention to `match_quality`:
- **`exact`** or **`strong`**: Trust the result highly
- **`moderate`**: Consider the suggestions
- **`weak`**: Review the verse for potential errors

### 4. **Use Transformations for Learning**
Review the `transformations` array to understand which prosodic variations were applied.

### 5. **Enable Suggestions**
Set `suggest_corrections: true` to get helpful feedback:
```json
{
  "suggest_corrections": true
}
```

---

## 📖 Supported Meters (All 16 Classical Arabic Meters)

### Tier 1: Common Meters (9)
1. **الطويل** (at-Tawil) - Most frequent
2. **الكامل** (al-Kamil) - Very common
3. **البسيط** (al-Basit) - Common
4. **الوافر** (al-Wafir) - Common
5. **الرجز** (al-Rajaz) - Very common
6. **الرمل** (ar-Ramal) - Common
7. **الخفيف** (al-Khafif) - Common
8. **المتقارب** (al-Mutaqarib) - Common
9. **الهزج** (al-Hazaj) - Common

### Tier 2: Medium Frequency (2)
10. **السريع** (as-Sari') - Medium
11. **المديد** (al-Madid) - Medium

### Tier 3: Rare Meters (5)
12. **المنسرح** (al-Munsarih) - Rare
13. **المجتث** (al-Mujtathth) - Rare
14. **المقتضب** (al-Muqtadab) - Rare
15. **المضارع** (al-Mudari') - Rare
16. **المتدارك** (al-Mutadarik) - Rare

---

## 🔧 Technical Details

### Detection Algorithm
1. **Pattern Generation**: Creates all theoretically valid patterns from Zihafat rules
2. **Exact Matching**: Checks if input matches any valid pattern exactly
3. **Approximate Matching**: Finds close matches (≥90% similarity) for robustness
4. **Tier-Based Tie-Breaking**: Prefers more common meters when patterns match multiple
5. **Confidence Scoring**: Based on match quality, meter frequency, and approximation

### Zihafat Coverage
- **10 types of Zihafat** (prosodic variations)
- **6 types of 'Ilal** (end-of-verse variations)
- **Position-specific rules** for each meter
- **Combination support** (Zahaf + 'Ilah)

---

## 🐛 Troubleshooting

### Low Confidence Score
**Possible causes:**
- Missing diacritics (tashkeel)
- Verse doesn't follow classical meters
- Multiple rare zihafat applied

**Solutions:**
- Add diacritical marks
- Check `transformations` to see what was detected
- Review `suggestions` for guidance

### No Detection
**Possible causes:**
- Text too short
- Not Arabic poetry
- Very unusual pattern

**Solutions:**
- Ensure text is at least 5 characters
- Verify it's Arabic script
- Check if it follows classical prosody

### Unexpected Meter
**Possible causes:**
- Similar meters (e.g., المتدارك vs المتقارب)
- Pattern collision

**Solutions:**
- Check `transformations` to understand the match
- Review `explanation` for details
- Consider `match_quality` indicator

---

## 📞 Support & Feedback

For issues, questions, or feedback about the API:
- **GitHub**: [anthropics/claude-code/issues](https://github.com/anthropics/claude-code/issues)
- **Documentation**: Check API docs at `/docs` endpoint

---

## 📜 License & Attribution

BAHR (البحر) - Arabic Poetry Prosody Analysis
- Based on classical Arabic prosody (علم العروض)
- Khalil ibn Ahmad al-Farahidi's system (الخليل بن أحمد الفراهيدي)
- Modern implementation with rule-based AI

---

## 🎓 Further Learning

To understand the prosody terms:
- **Zihafat (زحافات)**: Systematic variations in meter
- **'Ilal (علل)**: End-of-verse variations
- **Taf'ila (تفعيلة)**: Prosodic foot (basic unit)
- **Bahr (بحر)**: Meter (overall pattern)
- **Sabab (سبب)**: Two-letter unit
- **Watad (وتد)**: Three-letter unit

---

*Built with complete transparency and explainability in mind.*
*Every detection decision is traceable and understandable.*
