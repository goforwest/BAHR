# Arabic Prosody ML Dataset Construction Blueprint

**Document Version:** 1.0  
**Date:** November 14, 2025  
**Purpose:** Complete specification for constructing a high-quality Arabic poetry dataset for training a machine-learning-based prosody (ʿarūḍ) detection engine  
**Target:** Minimum 100 verified verses per classical Arabic meter

---

## Executive Summary

This document provides an explicit, step-by-step blueprint for constructing a production-grade Arabic poetry dataset suitable for training machine learning models to detect classical Arabic meters (البحور العروضية). The dataset will contain **at least 100 fully verified verses per meter**, totaling **minimum 2,000 verses** across 20 meter variants, with comprehensive metadata, prosodic annotations, and quality controls.

**Key Requirements:**
- Coverage: All 16 classical meters + 4 common variants (20 total)
- Minimum size: 100 verses per meter (2,000 total verses)
- Quality: 100% prosodic accuracy validated by rule-based engine
- Format: JSONL with complete metadata and pre-computed features
- Sources: Classical authenticated poetry from canonical collections

---

## 1. Meter Definition and Coverage Requirements

### 1.1 Complete Meter List (20 Meters)

The dataset MUST include all 16 classical Arabic meters (البحور الستة عشر) as defined by al-Khalīl ibn Aḥmad al-Farāhīdī, plus 4 widely-used shortened variants (مجزوء).

#### Tier 1: High-Frequency Meters (9 meters) - Priority Level: CRITICAL

| ID | Arabic Name | English Transliteration | Base Tafāʿīl | Est. Frequency | Min. Required | Target |
|----|-------------|------------------------|--------------|----------------|---------------|--------|
| 1  | الطويل | al-Ṭawīl | 4 | 35-40% | 100 | 150+ |
| 2  | الكامل | al-Kāmil | 4 | 15-20% | 100 | 150+ |
| 3  | البسيط | al-Basīṭ | 4 | 12-15% | 100 | 150+ |
| 4  | الوافر | al-Wāfir | 3 | 10-12% | 100 | 150+ |
| 5  | الرجز | al-Rajaz | 3 | 8-10% | 100 | 150+ |
| 6  | الرمل | ar-Ramal | 3 | 7-9% | 100 | 150+ |
| 7  | الخفيف | al-Khafīf | 3 | 6-8% | 100 | 150+ |
| 11 | المتقارب | al-Mutaqārib | 4 | 4-6% | 100 | 120+ |
| 12 | الهزج | al-Hazaj | 3 | 3-5% | 100 | 120+ |

#### Tier 2: Medium-Frequency Meters (2 meters) - Priority Level: HIGH

| ID | Arabic Name | English Transliteration | Base Tafāʿīl | Est. Frequency | Min. Required | Target |
|----|-------------|------------------------|--------------|----------------|---------------|--------|
| 8  | السريع | as-Sarīʿ | 3 | 2-3% | 100 | 120+ |
| 9  | المديد | al-Madīd | 4 | 2-3% | 100 | 120+ |

#### Tier 3: Rare Meters (5 meters) - Priority Level: MEDIUM

| ID | Arabic Name | English Transliteration | Base Tafāʿīl | Est. Frequency | Min. Required | Target |
|----|-------------|------------------------|--------------|----------------|---------------|--------|
| 10 | المنسرح | al-Munsariḥ | 4 | 1-2% | 100 | 100 |
| 13 | المجتث | al-Mujtathth | 3 | 1-2% | 100 | 100 |
| 14 | المقتضب | al-Muqtaḍab | 3 | <1% | 100 | 100 |
| 15 | المضارع | al-Muḍāriʿ | 3 | <1% | 100 | 100 |
| 16 | المتدارك | al-Mutadārik | 4 | <1% | 100 | 100 |

#### Common Variants (مجزوء) - Priority Level: MEDIUM

| ID | Arabic Name | English Transliteration | Base Tafāʿīl | Parent Meter | Min. Required | Target |
|----|-------------|------------------------|--------------|--------------|---------------|--------|
| 17 | الكامل (مجزوء) | al-Kāmil (majzūʾ) | 2 | الكامل | 100 | 120+ |
| 18 | الهزج (مجزوء) | al-Hazaj (majzūʾ) | 2 | الهزج | 100 | 120+ |
| 19 | الكامل (3 تفاعيل) | al-Kāmil (3 tafāʿīl) | 3 | الكامل | 100 | 120+ |
| 20 | السريع (مفعولات) | as-Sarīʿ (mafʿūlāt) | 3 | السريع | 100 | 120+ |

### 1.2 Dataset Size Requirements

**Total Minimum Verses:** 2,000 verses (100 per meter × 20 meters)  
**Recommended Target:** 2,400+ verses (120 average per meter)  
**Stretch Goal:** 3,000+ verses (150 average per meter)

**Distribution Strategy:**
- High-frequency meters (Tier 1): 150+ verses each (reflects natural distribution)
- Medium-frequency meters (Tier 2): 120+ verses each
- Rare meters (Tier 3): 100 verses each (minimum viable)
- Variants: 100-120 verses each

**Rationale for 100-verse minimum:**
- ML training requires sufficient examples per class (minimum 80 for stratified k-fold)
- 100 verses allow 80/20 train/test split with 80 training examples
- Captures prosodic variation (ziḥāfāt and ʿilal variations)
- Enables meaningful performance evaluation

---

## 2. Data Collection Procedures

### 2.1 Primary Source Selection Criteria

**Tier 1 Sources (Highest Priority - Use First):**

1. **المكتبة الشاملة (al-Maktaba al-Shāmila)**  
   - Status: Canonical digital library  
   - Coverage: 300,000+ verses from authenticated classical texts  
   - Access: Free desktop software (shamela.ws)  
   - Quality: Human-verified, diacritized, with attribution  
   - Extraction method: Database queries by meter tag

2. **الديوان (Aldiwan.net)**  
   - Status: Classical poetry repository  
   - Coverage: Complete diwans of major classical poets  
   - Access: Web scraping with robots.txt compliance  
   - Quality: Verified by Arabic literature scholars  
   - Extraction method: API or structured HTML parsing

3. **موسوعة الشعر العربي (Encyclopedia of Arabic Poetry)**  
   - Coverage: 10,000+ poems, 100+ poets  
   - Quality: Peer-reviewed entries  
   - Access: Institutional or subscription

**Tier 2 Sources (Supplement for Rare Meters):**

4. **Classical Diwans (Individual Poet Collections)**  
   - al-Mutanabbī, Imruʾ al-Qays, al-Buḥturī, Abū Nuwās, etc.  
   - Use printed editions with تحقيق (critical editions)  
   - Verify against multiple manuscripts

5. **Academic Prosody Corpora**  
   - University research datasets  
   - Annotated corpora from linguistics departments  
   - Require explicit permission and citation

**Tier 3 Sources (Last Resort for Rare Meters):**

6. **Synthetic Verse Generation (Only if <100 natural verses available)**  
   - Use rule-based generator with validated prosodic engine  
   - Ensure grammatical correctness  
   - Mark clearly as synthetic in metadata  
   - Maximum 20% synthetic per meter

### 2.2 Source Authentication Requirements

**For each verse, verify:**

1. **Poet Attribution**  
   - Cross-reference at least 2 independent sources  
   - Prefer authenticated diwans with scholarly تحقيق  
   - Document attribution confidence: certain / probable / uncertain

2. **Text Authenticity**  
   - Use critical editions (طبعات محققة)  
   - Check for variants (روايات) across manuscripts  
   - Select most reliable reading (القراءة المشهورة)

3. **Meter Classification**  
   - Verify meter label matches source metadata  
   - Validate with prosodic analysis engine  
   - Flag discrepancies for expert review

### 2.3 Verse Selection Filtering Criteria

**Inclusion Criteria (ALL must be satisfied):**

1. **Prosodic Validity**  
   - Passes automated prosodic analysis (100% pattern match)  
   - No forced scansion or ambiguous syllabification  
   - Standard ziḥāfāt and ʿilal only (no rare mutations)

2. **Completeness**  
   - Full hemistich pair (صدر + عجز)  
   - No ellipsis or missing words  
   - Diacritics present or reliably reconstructible

3. **Language Quality**  
   - Classical Arabic (فصحى) only  
   - No colloquial admixtures  
   - Standard orthography

4. **Uniqueness**  
   - No duplicates (check normalized text)  
   - No minor variants of same verse

**Exclusion Criteria (ANY triggers removal):**

1. **Prosodic Issues**  
   - Fails automated scansion  
   - Requires rare/disputed ziḥāfāt  
   - Meter ambiguity (could match multiple meters)

2. **Textual Issues**  
   - Corrupted or incomplete text  
   - Uncertain reading (textual crux)  
   - Missing or unreliable diacritics

3. **Content Issues**  
   - Extremely rare or archaic vocabulary (hinders ML generalization)  
   - Obvious scribal errors

4. **Ethical Issues**  
   - Offensive or harmful content  
   - Copyright restrictions

### 2.4 Prosodic Pattern Validation Procedure

**Step 1: Automated Scansion**

Use the BAHR prosodic engine (or equivalent) to:

1. **Normalize text:**
   - Remove tashkīl (diacritics) for pattern matching  
   - Normalize hamza forms (أ، إ، ء → ا)  
   - Normalize alif maqṣūra (ى → ي)

2. **Perform taqṭīʿ (syllabification):**
   - Convert to phonetic representation  
   - Generate syllable pattern (e.g., `//o///o//o/o`)  
   - Map to tafāʿīl sequence

3. **Match against meter rules:**
   - Compare with canonical meter patterns  
   - Identify ziḥāfāt (prosodic variations)  
   - Validate ʿilal (end-verse modifications)

4. **Confidence scoring:**
   - Pattern match score (0-100%)  
   - Require ≥95% confidence for inclusion  
   - Flag 90-95% for manual review

**Step 2: Manual Expert Review (For Flagged Cases)**

- Human prosody expert validates uncertain cases  
- Checks for rare ziḥāfāt not in automated rules  
- Final accept/reject decision

**Step 3: Cross-Validation**

- Run verse through independent prosody tool (e.g., Al-Khalil Meter Detector)  
- Compare results with BAHR engine  
- Require agreement between tools (≥90% match)

---

## 3. Dataset Format Specification

### 3.1 File Format: JSONL (JSON Lines)

**Format:** One JSON object per line (newline-delimited JSON)  
**Encoding:** UTF-8 (without BOM)  
**Filename Convention:** `{dataset_name}_v{version}_{meter_count}meters.jsonl`  
**Example:** `arabic_prosody_training_v1.0_20meters.jsonl`

**Rationale:**
- Streamable for large datasets (no need to load entire file)  
- Parseable line-by-line (memory efficient)  
- Compatible with ML frameworks (TensorFlow, PyTorch, Hugging Face)  
- Easy versioning and diffing

### 3.2 Schema Definition (Per Verse)

#### Required Fields (16 fields)

```json
{
  "verse_id": "string",
  "text": "string",
  "normalized_text": "string",
  "meter_id": "integer",
  "meter": "string",
  "meter_en": "string",
  "poet": "string",
  "source": "string",
  "source_type": "string",
  "timestamp": "string",
  "prosody_precomputed": {
    "pattern_phonetic": "string",
    "tafail_sequence": ["string"],
    "zihafat": ["object"],
    "ilal": ["object"],
    "confidence": "float"
  },
  "metadata": {
    "poem_title": "string",
    "era": "string",
    "genre": "string",
    "original_source": "string",
    "verification_status": "string"
  },
  "ml_features": {
    "pattern_length": "integer",
    "harakat_count": "integer",
    "sakin_count": "integer",
    "syllable_pattern": "string"
  }
}
```

#### Field Definitions and Constraints

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `verse_id` | string | ✅ | Format: `{meter_abbr}_{source}_{seq:04d}` | Unique identifier |
| `text` | string | ✅ | Length: 20-200 chars, Arabic script | Original verse with full diacritics |
| `normalized_text` | string | ✅ | Length: 20-200 chars, Arabic script | Verse without diacritics, normalized |
| `meter_id` | integer | ✅ | Range: 1-20 | Numeric meter ID (see table §1.1) |
| `meter` | string | ✅ | Arabic meter name | Meter name in Arabic (e.g., "الطويل") |
| `meter_en` | string | ✅ | Transliterated name | Meter name in English (e.g., "al-Ṭawīl") |
| `poet` | string | ✅ | Not empty | Poet name (Arabic or transliterated) |
| `source` | string | ✅ | Enum: classical/modern/synthetic | Verse origin category |
| `source_type` | string | ✅ | Free text | Specific source (e.g., "Shamela DB", "Diwan Imruʾ al-Qays") |
| `timestamp` | string | ✅ | ISO 8601 format | Date added to dataset |
| `prosody_precomputed` | object | ✅ | See §3.2.2 | Pre-computed prosodic analysis |
| `metadata` | object | ✅ | See §3.2.3 | Additional contextual information |
| `ml_features` | object | ✅ | See §3.2.4 | Pre-extracted ML features |

#### 3.2.2 Prosody Precomputed Object

```json
"prosody_precomputed": {
  "pattern_phonetic": "string",        // Syllable pattern: "//o///o//o/o"
  "tafail_sequence": ["string"],       // Tafāʿīl names: ["فعولن", "مفاعيلن", ...]
  "tafail_patterns": ["string"],       // Tafāʿīl syllable patterns: ["/oo/", "///o/", ...]
  "zihafat": [                         // Applied ziḥāfāt (prosodic variations)
    {
      "position": "integer",           // Tafīlah position (1-based)
      "type": "string",                // Ziḥāf type (e.g., "qabd", "khabn")
      "base_tafila": "string",         // Original tafīlah
      "modified_tafila": "string"      // Modified tafīlah after ziḥāf
    }
  ],
  "ilal": [                            // Applied ʿilal (end modifications)
    {
      "position": "integer",           // Final tafīlah position
      "type": "string",                // ʿIllah type (e.g., "qaṣr", "ḥadhf")
      "base_tafila": "string",         // Original tafīlah
      "modified_tafila": "string"      // Modified tafīlah after ʿillah
    }
  ],
  "confidence": "float",               // Scansion confidence (0.0-1.0)
  "engine_version": "string"           // Prosody engine version (e.g., "BAHR v2.1.0")
}
```

#### 3.2.3 Metadata Object

```json
"metadata": {
  "poem_title": "string",              // Title of the poem (if known)
  "era": "string",                     // Historical period: pre-Islamic/Umayyad/Abbasid/Modern
  "genre": "string",                   // Poetry type: ghazal/fakhr/madih/hijāʾ/etc.
  "original_source": "string",         // Original manuscript/book citation
  "verification_status": "string",     // validated/expert_reviewed/synthetic
  "diacritization_source": "string",   // original/auto-generated/reconstructed
  "notes": "string"                    // Any additional notes
}
```

#### 3.2.4 ML Features Object

Pre-extracted features for ML training (to avoid recomputation):

```json
"ml_features": {
  "pattern_length": "integer",         // Total syllable count
  "harakat_count": "integer",          // Number of vowel diacritics
  "sakin_count": "integer",            // Number of sukūn marks
  "mutaharrik_count": "integer",       // Number of vocalized consonants
  "word_count": "integer",             // Total words in verse
  "syllable_pattern": "string",        // Full syllable pattern
  "tafail_count": "integer",           // Number of tafāʿīl
  "zihafat_count": "integer",          // Number of applied ziḥāfāt
  "has_ilal": "boolean",               // Whether ʿilal present
  "pattern_diversity": "float"         // Pattern uniqueness score (0-1)
}
```

### 3.3 Example Record

```json
{
  "verse_id": "tawil_shamela_0042",
  "text": "قِفَا نَبْكِ مِنْ ذِكْرَى حَبِيبٍ وَمَنْزِلِ",
  "normalized_text": "قفا نبك من ذكرى حبيب ومنزل",
  "meter_id": 1,
  "meter": "الطويل",
  "meter_en": "al-Ṭawīl",
  "poet": "امرؤ القيس",
  "source": "classical",
  "source_type": "Shamela Database - Diwan Imru' al-Qays",
  "timestamp": "2025-01-15T10:30:00Z",
  "prosody_precomputed": {
    "pattern_phonetic": "//o///o//o///o",
    "tafail_sequence": ["فعولن", "مفاعيلن", "فعولن", "مفاعلن"],
    "tafail_patterns": ["/oo/", "///o/", "/oo/", "///o"],
    "zihafat": [
      {
        "position": 4,
        "type": "qabd",
        "base_tafila": "مفاعيلن",
        "modified_tafila": "مفاعلن"
      }
    ],
    "ilal": [],
    "confidence": 0.98,
    "engine_version": "BAHR v2.1.0"
  },
  "metadata": {
    "poem_title": "معلقة امرئ القيس",
    "era": "pre-Islamic",
    "genre": "ghazal",
    "original_source": "المعلقات السبع، تحقيق أحمد أمين وآخرون",
    "verification_status": "expert_reviewed",
    "diacritization_source": "original",
    "notes": "Opening verse of the most famous pre-Islamic mu'allaqa"
  },
  "ml_features": {
    "pattern_length": 14,
    "harakat_count": 11,
    "sakin_count": 7,
    "mutaharrik_count": 11,
    "word_count": 6,
    "syllable_pattern": "//o///o//o///o",
    "tafail_count": 4,
    "zihafat_count": 1,
    "has_ilal": false,
    "pattern_diversity": 0.75
  }
}
```

### 3.4 Verse ID Convention

**Format:** `{meter_abbr}_{source}_{sequence:04d}`

**Meter Abbreviations:**
- `tawil` = الطويل
- `kamil` = الكامل
- `basit` = البسيط
- `wafir` = الوافر
- `rajaz` = الرجز
- `ramal` = الرمل
- `khafif` = الخفيف
- `mutaqarib` = المتقارب
- `hazaj` = الهزج
- `sari` = السريع
- `madid` = المديد
- `munsarih` = المنسرح
- `mujtathth` = المجتث
- `muqtadab` = المقتضب
- `mudari` = المضارع
- `mutadarik` = المتدارك
- `kamil_majzu` = الكامل (مجزوء)
- `hazaj_majzu` = الهزج (مجزوء)
- `kamil_3` = الكامل (3 تفاعيل)
- `sari_mafoolat` = السريع (مفعولات)

**Source Codes:**
- `shamela` = المكتبة الشاملة
- `aldiwan` = الديوان
- `diwan_{poet}` = Individual diwan (e.g., `diwan_mutanabbi`)
- `synthetic` = AI-generated verse

**Examples:**
- `tawil_shamela_0001`
- `kamil_diwan_mutanabbi_0042`
- `mutadarik_synthetic_0007`

---

## 4. Quality Control and Validation Procedures

### 4.1 Deduplication Strategy

**Level 1: Exact Text Match**
- Normalize both `text` and `normalized_text` fields  
- Check for exact duplicates  
- Remove all but first occurrence  
- Log duplicate count per source

**Level 2: Fuzzy Matching (Edit Distance)**
- Compute Levenshtein distance on `normalized_text`  
- Flag pairs with edit distance ≤ 3 characters  
- Manual review to determine if variant or true duplicate  
- Keep variants with different prosodic patterns

**Level 3: Pattern-Based Detection**
- Compare `prosody_precomputed.pattern_phonetic` across verses  
- Flag identical patterns within same meter  
- Verify if different texts have identical scansion (suspicious)

**Implementation:**
```python
def deduplicate_dataset(verses: List[Dict]) -> List[Dict]:
    """Remove exact and near-duplicate verses."""
    seen_texts = set()
    seen_patterns = {}
    unique_verses = []
    
    for verse in verses:
        normalized = verse['normalized_text']
        pattern = verse['prosody_precomputed']['pattern_phonetic']
        meter = verse['meter']
        
        # Exact match check
        if normalized in seen_texts:
            continue
        
        # Pattern collision check (same meter + same pattern)
        key = f"{meter}:{pattern}"
        if key in seen_patterns:
            # Flag for review if texts differ significantly
            if edit_distance(normalized, seen_patterns[key]) > 5:
                print(f"Warning: Different texts with same pattern in {meter}")
        else:
            seen_patterns[key] = normalized
        
        seen_texts.add(normalized)
        unique_verses.append(verse)
    
    return unique_verses
```

### 4.2 Consistency Checking

**Field Validation:**

1. **meter_id ↔ meter consistency:**
   ```python
   METER_MAPPING = {
       1: "الطويل", 2: "الكامل", 3: "البسيط", ...
   }
   assert METER_MAPPING[verse['meter_id']] == verse['meter']
   ```

2. **Pattern length validation:**
   ```python
   assert len(verse['prosody_precomputed']['tafail_sequence']) == verse['ml_features']['tafail_count']
   ```

3. **Ziḥāfāt count consistency:**
   ```python
   assert len(verse['prosody_precomputed']['zihafat']) == verse['ml_features']['zihafat_count']
   ```

**Cross-Field Validation:**

- Verify `text` contains Arabic script only (no Latin characters)  
- Check `timestamp` is valid ISO 8601 date  
- Ensure `confidence` is in range [0.0, 1.0]  
- Validate `verification_status` is one of: validated/expert_reviewed/synthetic

### 4.3 Prosodic Accuracy Validation

**Automated Validation Pipeline:**

1. **Re-run prosodic analysis:**
   - Pass `text` through BAHR engine  
   - Compare output with `prosody_precomputed`  
   - Require 100% match (pattern, tafāʿīl, ziḥāfāt)

2. **Confidence thresholding:**
   - Require `confidence ≥ 0.95` for all verses  
   - Flag 0.90-0.95 for expert review  
   - Reject <0.90

3. **Meter consistency check:**
   - Verify detected meter matches `meter` field  
   - Flag discrepancies for review

**Expert Review Queue:**

Verses requiring human validation:
- Confidence 0.90-0.95  
- Rare ziḥāfāt not in standard rules  
- Pattern ambiguity (could match multiple meters)  
- Synthetic verses (all require review)

### 4.4 Bias Mitigation

**Poet Diversity:**
- Maximum 10% of any meter from a single poet  
- Include poets from different eras:
  - Pre-Islamic (جاهلي): 15-20%
  - Umayyad (أموي): 15-20%
  - Abbasid (عباسي): 30-40%
  - Modern (حديث): 20-30%

**Genre Diversity:**
- Ensure variety within each meter:
  - Ghazal (غزل): romantic/love poetry
  - Fakhr (فخر): pride/boasting
  - Madīḥ (مديح): praise
  - Hijāʾ (هجاء): satirical
  - Waṣf (وصف): descriptive
  - Ḥikma (حكمة): wisdom

**Syntactic Diversity:**
- Vary sentence structures (nominal vs. verbal)  
- Include different word orders  
- Mix short and long words

**Pattern Diversity:**
- Ensure coverage of all common ziḥāfāt for each meter  
- Include canonical (no ziḥāf) and modified versions  
- Cover all ʿilal variations for final tafīlah

### 4.5 Text Normalization Rules

**Diacritics Handling:**

1. **`text` field (with diacritics):**
   - Preserve original tashkīl from source  
   - If missing, use expert reconstruction  
   - Mark auto-generated diacritics in `metadata.diacritization_source`

2. **`normalized_text` field (without diacritics):**
   - Remove all ḥarakāt (فتحة، ضمة، كسرة)  
   - Remove shadda (شدة) and sukūn (سكون)  
   - Remove tanwīn (تنوين)  
   - Preserve hamza and basic letters

**Character Normalization:**

Apply the following transformations to `normalized_text`:

| Original | Normalized | Reason |
|----------|-----------|---------|
| أ، إ، آ، ء | ا | Hamza normalization |
| ى | ي | Alif maqṣūra → yāʾ |
| ة | ه | Tāʾ marbūṭa → hāʾ |
| ـ | (remove) | Taṭwīl (kashida) |
| Multiple spaces | Single space | Whitespace normalization |

**Implementation:**
```python
import re
from pyarabic.araby import strip_tashkeel, normalize_hamza

def normalize_arabic_text(text: str) -> str:
    """Normalize Arabic text for ML processing."""
    # Remove diacritics
    text = strip_tashkeel(text)
    
    # Normalize hamza
    text = normalize_hamza(text)
    
    # Alif maqsura → ya
    text = text.replace('ى', 'ي')
    
    # Ta marbuta → ha
    text = text.replace('ة', 'ه')
    
    # Remove tatweel
    text = text.replace('ـ', '')
    
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text
```

### 4.6 Script and Encoding Validation

**Encoding Requirements:**
- UTF-8 encoding (no BOM)  
- Validate all characters are in Unicode Arabic block (U+0600 to U+06FF)  
- Allow basic punctuation: space, comma, period

**Character Whitelist:**
```python
ALLOWED_CHARS = set(
    'ابتثجحخدذرزسشصضطظعغفقكلمنهويء'  # Basic Arabic letters
    'أإآؤئىة'  # Hamza variants
    'ًٌٍَُِّْ'  # Diacritics (for text field)
    ' ،.'  # Whitespace and punctuation
)

def validate_arabic_script(text: str) -> bool:
    """Ensure text contains only allowed Arabic characters."""
    return all(c in ALLOWED_CHARS for c in text)
```

---

## 5. Export Formats and Versioning

### 5.1 Export Formats

**Primary Format: JSONL**
- Filename: `arabic_prosody_training_v{major}.{minor}_{meter_count}meters.jsonl`
- Use: Training, streaming, data pipelines
- Example: `arabic_prosody_training_v1.0_20meters.jsonl`

**Secondary Format: Parquet**
- Filename: `arabic_prosody_training_v{major}.{minor}_{meter_count}meters.parquet`
- Use: Analytics, cloud storage (S3/BigQuery), Spark
- Schema: Auto-inferred from JSONL
- Compression: Snappy (default)

**Tertiary Format: CSV (Flattened)**
- Filename: `arabic_prosody_training_v{major}.{minor}_{meter_count}meters.csv`
- Use: Excel, simple analysis, non-technical users
- Note: JSON fields flattened or serialized as strings
- Limitation: Loss of nested structure

**Conversion Pipeline:**
```python
import pandas as pd
import json

# JSONL → Parquet
def jsonl_to_parquet(jsonl_path: str, parquet_path: str):
    verses = []
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            verses.append(json.loads(line))
    df = pd.DataFrame(verses)
    df.to_parquet(parquet_path, compression='snappy', index=False)

# JSONL → CSV (flattened)
def jsonl_to_csv(jsonl_path: str, csv_path: str):
    verses = []
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            verse = json.loads(line)
            # Flatten nested objects
            verse['pattern_phonetic'] = verse['prosody_precomputed']['pattern_phonetic']
            verse['confidence'] = verse['prosody_precomputed']['confidence']
            verse['poem_title'] = verse['metadata'].get('poem_title', '')
            # Remove nested fields
            del verse['prosody_precomputed']
            del verse['metadata']
            del verse['ml_features']
            verses.append(verse)
    df = pd.DataFrame(verses)
    df.to_csv(csv_path, index=False, encoding='utf-8')
```

### 5.2 Versioning Strategy

**Semantic Versioning: v{MAJOR}.{MINOR}.{PATCH}**

- **MAJOR:** Breaking changes (schema changes, meter redefinitions)
- **MINOR:** Backward-compatible additions (new verses, new meters)
- **PATCH:** Bug fixes (correction of errors, deduplication)

**Version Metadata File:**

Each dataset release includes a `version_metadata.json`:

```json
{
  "version": "1.0.0",
  "release_date": "2025-01-20",
  "total_verses": 2400,
  "meters_covered": 20,
  "schema_version": "1.0",
  "prosody_engine": "BAHR v2.1.0",
  "changes": [
    "Initial release",
    "100+ verses per meter",
    "Full prosodic annotation"
  ],
  "statistics": {
    "sources": {
      "classical": 2100,
      "modern": 200,
      "synthetic": 100
    },
    "verification": {
      "validated": 2200,
      "expert_reviewed": 150,
      "synthetic": 100
    },
    "average_confidence": 0.972
  },
  "known_issues": [],
  "next_version_plan": "Add 50 more verses for rare meters"
}
```

**Git Tagging:**
- Tag each release: `git tag v1.0.0`
- Include changelog in tag message
- Push tags to repository

**Changelog (CHANGELOG.md):**

```markdown
# Changelog

## [1.0.0] - 2025-01-20

### Added
- Initial dataset with 2,400 verses
- All 20 classical meters + variants covered
- 100+ verses per meter (minimum)
- Full prosodic annotations
- Pre-computed ML features

### Sources
- al-Maktaba al-Shāmila: 1,800 verses
- Aldiwan.net: 300 verses
- Classical diwans: 200 verses
- Synthetic generation: 100 verses

### Validation
- 100% prosodic accuracy
- Average confidence: 97.2%
- Expert review: 150 verses
```

### 5.3 Reproducibility Requirements

**Dataset Creation Script:**

Provide a Python script to regenerate dataset from raw sources:

```python
# scripts/build_dataset.py
"""
Dataset Construction Script

Reproduces the full dataset from source files.

Usage:
    python scripts/build_dataset.py \
        --sources data/raw/ \
        --output dataset/arabic_prosody_training_v1.0_20meters.jsonl \
        --min-per-meter 100 \
        --confidence-threshold 0.95
"""

import argparse
from pathlib import Path
from dataset_builder import (
    collect_verses_from_shamela,
    collect_verses_from_aldiwan,
    validate_prosody,
    deduplicate,
    export_jsonl
)

def main(args):
    verses = []
    
    # Step 1: Collect from sources
    verses.extend(collect_verses_from_shamela(args.sources / 'shamela'))
    verses.extend(collect_verses_from_aldiwan(args.sources / 'aldiwan'))
    
    # Step 2: Prosodic validation
    verses = validate_prosody(verses, confidence_threshold=args.confidence_threshold)
    
    # Step 3: Deduplication
    verses = deduplicate(verses)
    
    # Step 4: Ensure minimum per meter
    verses = ensure_minimum_per_meter(verses, min_count=args.min_per_meter)
    
    # Step 5: Export
    export_jsonl(verses, args.output)
    print(f"✅ Dataset built: {len(verses)} verses")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--sources', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--min-per-meter', type=int, default=100)
    parser.add_argument('--confidence-threshold', type=float, default=0.95)
    args = parser.parse_args()
    main(args)
```

**Dependencies File (requirements.txt):**
```
pandas==2.1.0
pyarrow==13.0.0
pyarabic==0.6.15
numpy==1.25.0
scikit-learn==1.3.0
```

**Docker Container (Optional):**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY scripts/ ./scripts/
COPY data/ ./data/
CMD ["python", "scripts/build_dataset.py"]
```

---

## 6. ML-Specific Requirements

### 6.1 Train/Test/Validation Split

**Recommended Split:**
- Training: 70% (1,680 verses)
- Validation: 15% (360 verses)
- Test: 15% (360 verses)

**Stratification:**
- Maintain meter distribution in all splits
- Ensure each meter has ≥10 examples in test set
- Use stratified k-fold for cross-validation

**Implementation:**
```python
from sklearn.model_selection import train_test_split

def split_dataset(verses, test_size=0.15, val_size=0.15, random_state=42):
    """Stratified split by meter."""
    meters = [v['meter'] for v in verses]
    
    # Train + (Val + Test)
    train_verses, temp_verses = train_test_split(
        verses, 
        test_size=(test_size + val_size),
        stratify=meters,
        random_state=random_state
    )
    
    # Val + Test
    temp_meters = [v['meter'] for v in temp_verses]
    val_verses, test_verses = train_test_split(
        temp_verses,
        test_size=(test_size / (test_size + val_size)),
        stratify=temp_meters,
        random_state=random_state
    )
    
    return train_verses, val_verses, test_verses
```

### 6.2 Feature Extraction Guidelines

**Pre-computed Features (Already in Dataset):**
- `ml_features` object contains basic features
- Ready for immediate use in ML pipelines

**Advanced Features (Compute During Training):**

1. **TF-IDF on normalized text:**
   ```python
   from sklearn.feature_extraction.text import TfidfVectorizer
   vectorizer = TfidfVectorizer(max_features=500, ngram_range=(1,2))
   tfidf_features = vectorizer.fit_transform([v['normalized_text'] for v in verses])
   ```

2. **Pattern embeddings:**
   - Use prosodic pattern as categorical feature
   - One-hot encode or embed tafāʿīl sequences

3. **Meter similarity features:**
   - Compute similarity to all 20 meter templates
   - Use edit distance on syllable patterns

### 6.3 Tafāʿīl Encoding for ML

**Categorical Encoding:**

Assign numeric IDs to all tafāʿīl:

| Tafīlah | Arabic | Pattern | ID |
|---------|--------|---------|-----|
| faʿūlun | فعولن | /oo/ | 1 |
| mafāʿīlun | مفاعيلن | ///o/ | 2 |
| mufāʿalatun | مفاعلتن | ///o/ | 3 |
| mutafāʿilun | متفاعلن | ///o/ | 4 |
| ... | ... | ... | ... |

**Sequence Encoding:**

For sequence models (LSTM, Transformer):
```python
tafail_sequence = ["فعولن", "مفاعيلن", "فعولن", "مفاعلن"]
tafail_ids = [1, 2, 1, 3]  # Convert to IDs
# Pad to max length (e.g., 4 for al-Tawil)
padded = pad_sequence(tafail_ids, max_len=4, padding_value=0)
```

### 6.4 Label Encoding

**Meter Labels:**

Use numeric IDs (1-20) as defined in §1.1.

```python
METER_TO_ID = {
    'الطويل': 1, 'الكامل': 2, 'البسيط': 3, ...
}
ID_TO_METER = {v: k for k, v in METER_TO_ID.items()}

# For training
y = [METER_TO_ID[verse['meter']] for verse in train_verses]
```

**Multi-label Setup (Optional):**

If a verse could match multiple meters (ambiguous cases):
```python
y_multilabel = np.zeros((n_samples, 20))
for i, verse in enumerate(verses):
    y_multilabel[i, verse['meter_id'] - 1] = 1
    # Add secondary meters if ambiguous
    for alt_meter_id in verse.get('alternative_meters', []):
        y_multilabel[i, alt_meter_id - 1] = 0.5
```

---

## 7. Detailed Step-by-Step Construction Timeline

### Phase 1: Setup and Infrastructure (Week 1)

**Day 1-2: Environment Setup**
- Install Shamela desktop software
- Set up web scraping tools (BeautifulSoup, Scrapy)
- Configure BAHR prosodic engine
- Create database schema for raw verses

**Day 3-4: Source Access**
- Download Shamela database exports
- Test Aldiwan.net API access
- Gather classical diwan PDFs/texts
- Set up version control (Git repository)

**Day 5-7: Validation Pipeline**
- Implement prosodic validation script
- Create deduplication logic
- Build quality control dashboard
- Test pipeline with 100-verse sample

### Phase 2: Data Collection - Tier 1 Meters (Weeks 2-4)

**Target:** 9 high-frequency meters, 150+ verses each (~1,350 verses total)

**Week 2: al-Ṭawīl, al-Kāmil, al-Basīṭ**
- Extract from Shamela tagged collections
- Target: 150 verses × 3 meters = 450 verses
- Focus on pre-Islamic and Abbasid poetry

**Week 3: al-Wāfir, ar-Ramal, al-Rajaz**
- Continue Shamela extraction
- Target: 150 verses × 3 meters = 450 verses
- Include Umayyad era poets

**Week 4: al-Khafīf, al-Mutaqārib, al-Hazaj**
- Complete Tier 1 collection
- Target: 150 verses × 3 meters = 450 verses
- Validate all 1,350 verses

### Phase 3: Data Collection - Tier 2 & 3 Meters (Weeks 5-7)

**Target:** 7 medium/rare meters, 100-120 verses each (~770 verses total)

**Week 5: Tier 2 (as-Sarīʿ, al-Madīd)**
- Shamela + Aldiwan sources
- Target: 120 verses × 2 meters = 240 verses

**Week 6: Tier 3 Part 1 (al-Munsariḥ, al-Mujtathth, al-Muqtaḍab)**
- Intensive search in classical diwans
- Target: 100 verses × 3 meters = 300 verses

**Week 7: Tier 3 Part 2 (al-Muḍāriʿ, al-Mutadārik)**
- Rare meter collection (most challenging)
- Target: 100 verses × 2 meters = 200 verses
- Prepare synthetic generation for gaps

### Phase 4: Variants Collection (Week 8)

**Target:** 4 common variants, 100-120 verses each (~440 verses total)

- al-Kāmil (majzūʾ): 120 verses
- al-Hazaj (majzūʾ): 120 verses
- al-Kāmil (3 tafāʿīl): 100 verses
- as-Sarīʿ (mafʿūlāt): 100 verses

### Phase 5: Quality Assurance (Weeks 9-10)

**Week 9: Validation and Gap Filling**
- Run full prosodic validation on all 2,560 verses
- Identify meters below 100-verse threshold
- Generate synthetic verses for gaps (max 20 per meter)
- Expert review of flagged cases

**Week 10: Metadata Enrichment**
- Complete all metadata fields
- Add poet biographical info
- Verify era/genre classifications
- Compute ML features

### Phase 6: Export and Documentation (Week 11)

**Day 1-3: Export Formats**
- Generate JSONL, Parquet, CSV exports
- Create train/val/test splits
- Validate all file formats

**Day 4-5: Documentation**
- Write dataset README
- Create version metadata
- Document statistics and limitations

**Day 6-7: Release Preparation**
- Create Git tags
- Upload to Hugging Face Hub (optional)
- Publish dataset card

---

## 8. Dataset Statistics and Reporting

### 8.1 Required Statistics

For each dataset release, compute and report:

**Overall Statistics:**
- Total verses
- Total meters
- Average verses per meter
- Min/max verses per meter
- Average confidence score
- Source breakdown (classical/modern/synthetic %)

**Per-Meter Statistics:**
```python
for meter_id in range(1, 21):
    meter_verses = [v for v in verses if v['meter_id'] == meter_id]
    print(f"{meter_name}:")
    print(f"  Total verses: {len(meter_verses)}")
    print(f"  Avg confidence: {np.mean([v['prosody_precomputed']['confidence'] for v in meter_verses]):.3f}")
    print(f"  Unique poets: {len(set(v['poet'] for v in meter_verses))}")
    print(f"  Era breakdown: {Counter(v['metadata']['era'] for v in meter_verses)}")
    print(f"  Pattern diversity: {len(set(v['prosody_precomputed']['pattern_phonetic'] for v in meter_verses))}")
```

**Poet Distribution:**
- Top 10 poets by verse count
- Era distribution
- Genre distribution

**Prosodic Coverage:**
- Ziḥāfāt frequency by type
- ʿIlal frequency by type
- Pattern variation count per meter

### 8.2 Visualization Examples

**Meter Distribution Bar Chart:**
```python
import matplotlib.pyplot as plt
meter_counts = Counter(v['meter'] for v in verses)
plt.barh(list(meter_counts.keys()), list(meter_counts.values()))
plt.xlabel('Verse Count')
plt.title('Dataset Meter Distribution')
plt.tight_layout()
plt.savefig('meter_distribution.png', dpi=300)
```

**Confidence Score Distribution:**
```python
confidences = [v['prosody_precomputed']['confidence'] for v in verses]
plt.hist(confidences, bins=20, edgecolor='black')
plt.xlabel('Confidence Score')
plt.ylabel('Frequency')
plt.title('Prosodic Analysis Confidence Distribution')
plt.savefig('confidence_distribution.png', dpi=300)
```

---

## 9. Limitations and Ethical Considerations

### 9.1 Known Limitations

1. **Historical Bias:**
   - Dataset over-represents classical/Abbasid era
   - Under-represents modern poetry (intentional for meter purity)

2. **Rare Meter Scarcity:**
   - Some meters (المضارع، المقتضب) are genuinely rare in corpus
   - May require synthetic supplementation

3. **Diacritization:**
   - Some verses require reconstructed diacritics (not original)
   - Auto-generated tashkīl may contain errors

4. **Genre Imbalance:**
   - Certain meters favor specific genres (e.g., الرجز for didactic)
   - May affect model generalization

### 9.2 Ethical Considerations

**Copyright:**
- Only use public domain or licensed sources
- Classical poetry (>70 years old) is public domain in most jurisdictions
- Respect modern poet copyrights

**Attribution:**
- Always cite original sources
- Credit manuscript editors (محققون)
- Acknowledge database providers (Shamela, Aldiwan)

**Cultural Sensitivity:**
- Arabic poetry is cultural heritage
- Avoid misrepresentation of content
- Respect religious and historical significance

**Offensive Content:**
- Some classical hijāʾ (satirical) poetry may contain harsh language
- Flag but do not censor (preserves literary authenticity)
- Document content warnings in metadata

### 9.3 Dataset Maintenance Plan

**Annual Updates:**
- Add new verified verses (target: +500/year)
- Incorporate rare meter discoveries
- Update prosodic annotations with engine improvements

**Error Reporting:**
- Provide GitHub Issues for error reports
- Maintain changelog of corrections
- Version bumps for error fixes

**Community Contributions:**
- Accept pull requests for new verses
- Require prosodic validation before merge
- Expert review for community submissions

---

## 10. Success Criteria and Validation

### 10.1 Dataset Completion Checklist

- [ ] All 20 meters have ≥100 verses
- [ ] Total verses ≥2,000
- [ ] Average confidence ≥0.95
- [ ] Deduplication complete (0 exact duplicates)
- [ ] All fields populated (no missing required data)
- [ ] Train/val/test splits created
- [ ] JSONL, Parquet, CSV exports generated
- [ ] Version metadata file created
- [ ] Documentation complete (README, CHANGELOG)
- [ ] Statistics report generated
- [ ] Expert review complete for synthetic verses

### 10.2 ML Validation Test

**Baseline Model Test:**

Train a simple Random Forest classifier on the dataset:

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# Extract features
X = np.array([v['ml_features']['pattern_length'], 
              v['ml_features']['tafail_count'], ...] 
             for v in train_verses)
y = np.array([v['meter_id'] for v in train_verses])

# Train
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Evaluate
X_test = ...  # Extract from test_verses
y_test = ...
y_pred = model.predict(X_test)

print(classification_report(y_test, y_pred))
```

**Expected Performance:**
- Overall accuracy: ≥60% (with basic features)
- Per-meter recall: ≥50% for all meters
- High-frequency meters (Tier 1): ≥70% accuracy

**Dataset Quality Indicators:**
- If accuracy <50%: Insufficient data or high noise
- If some meters at 0% recall: Need more diverse examples
- If confusion between meters: Need better prosodic features

---

## 11. Appendices

### Appendix A: Glossary of Technical Terms

| Term (Arabic) | Term (English) | Definition |
|---------------|---------------|------------|
| بحر (pl. بحور) | Baḥr (pl. Buḥūr) | Poetic meter |
| تفعيلة (pl. تفاعيل) | Tafʿīlah (pl. Tafāʿīl) | Prosodic foot |
| زحاف (pl. زحافات) | Zaḥaf (pl. Ziḥāfāt) | Metrical variation (internal) |
| علة (pl. علل) | ʿIllah (pl. ʿIlal) | Metrical variation (final position) |
| تقطيع | Taqṭīʿ | Syllabification/scansion |
| عروض | ʿArūḍ | Prosody/metrics |
| صدر | Ṣadr | First hemistich (verse half) |
| عجز | ʿAjz | Second hemistich (verse half) |
| قافية | Qāfiyah | Rhyme |
| روي | Rawī | Rhyme letter |

### Appendix B: Prosodic Symbols Reference

**Syllable Notation:**

| Symbol | Meaning | Arabic | Example |
|--------|---------|--------|---------|
| / | Short syllable (CV) | حركة + ساكن | قَـ |
| o | Long syllable (CVV or CVC) | حركة + مد أو حركة + ساكن | قا، قال |
| - | Movable (haraka) | متحرك | فَ |
| u | Sakin | ساكن | فْ |

**Tafāʿīl Patterns:**

| Tafīlah | Pattern | Syllables | Notation |
|---------|---------|-----------|----------|
| فعولن | /oo/ | fa-ʿū-lun | CVV-CV |
| مفاعيلن | ///o/ | ma-fā-ʿī-lun | CV-CVV-CV-CVC |
| مستفعلن | ///o/ | mus-taf-ʿi-lun | CVC-CVC-CV-CVC |

### Appendix C: Python Libraries and Tools

**Required Python Packages:**

```plaintext
# Core data processing
pandas>=2.1.0
numpy>=1.25.0
pyarrow>=13.0.0

# Arabic NLP
pyarabic>=0.6.15
camel-tools>=1.5.0

# Prosody engine
# (Assuming BAHR engine is local/private)

# Machine learning
scikit-learn>=1.3.0
torch>=2.0.0  # If using deep learning

# Utilities
tqdm>=4.65.0
python-dateutil>=2.8.0
```

**Installation:**
```bash
pip install -r requirements.txt
```

### Appendix D: Sample Data Collection Script

```python
#!/usr/bin/env python3
"""
Sample script for collecting verses from Shamela database.

This is a template - adapt to actual Shamela API/database structure.
"""

import sqlite3
import json
from pathlib import Path
from typing import List, Dict
from datetime import datetime

def extract_verses_from_shamela(
    db_path: Path,
    meter_name: str,
    min_verses: int = 100
) -> List[Dict]:
    """
    Extract verses for a specific meter from Shamela database.
    
    Args:
        db_path: Path to Shamela SQLite database
        meter_name: Arabic meter name (e.g., "الطويل")
        min_verses: Minimum number of verses to collect
    
    Returns:
        List of verse dictionaries
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Example query (adapt to actual Shamela schema)
    query = """
        SELECT 
            verses.text,
            verses.poet,
            verses.book_title,
            verses.meter
        FROM verses
        WHERE verses.meter = ?
        LIMIT ?
    """
    
    cursor.execute(query, (meter_name, min_verses * 2))  # Fetch extra for filtering
    rows = cursor.fetchall()
    
    verses = []
    for i, (text, poet, book, meter) in enumerate(rows):
        verse = {
            "verse_id": f"shamela_{meter}_{i:04d}",
            "text": text.strip(),
            "normalized_text": normalize_arabic_text(text),
            "meter": meter,
            "poet": poet,
            "source": "classical",
            "source_type": f"Shamela - {book}",
            "timestamp": datetime.utcnow().isoformat() + 'Z',
            "metadata": {
                "original_source": book,
                "verification_status": "validated"
            }
        }
        verses.append(verse)
        
        if len(verses) >= min_verses:
            break
    
    conn.close()
    return verses

def normalize_arabic_text(text: str) -> str:
    """Normalize Arabic text (simplified version)."""
    # Remove diacritics
    import re
    text = re.sub(r'[\u064B-\u0652]', '', text)  # Remove tashkeel
    # Add more normalization as needed
    return text.strip()

# Example usage
if __name__ == '__main__':
    shamela_db = Path('/path/to/shamela.db')
    verses = extract_verses_from_shamela(shamela_db, 'الطويل', min_verses=150)
    print(f"Collected {len(verses)} verses for الطويل")
```

---

## Summary and Next Steps

This blueprint provides a complete, actionable plan for constructing a high-quality Arabic prosody dataset with the following guarantees:

**Coverage:**
- ✅ All 20 meters defined (16 classical + 4 variants)
- ✅ Minimum 100 verses per meter (2,000 total)
- ✅ Target 2,400+ verses for balance

**Quality:**
- ✅ 100% prosodic validation (≥95% confidence threshold)
- ✅ Deduplication and consistency checks
- ✅ Expert review for edge cases

**ML-Readiness:**
- ✅ JSONL format with complete metadata
- ✅ Pre-computed features included
- ✅ Train/val/test splits specified
- ✅ Tafāʿīl sequences encoded

**Reproducibility:**
- ✅ Detailed collection procedures
- ✅ Versioning strategy
- ✅ Dataset creation scripts
- ✅ Comprehensive documentation

**Next Steps for Implementation:**

1. **Week 1:** Set up infrastructure (Shamela access, BAHR engine, database)
2. **Weeks 2-4:** Collect Tier 1 meters (1,350 verses)
3. **Weeks 5-7:** Collect Tier 2 & 3 meters (770 verses)
4. **Week 8:** Collect variants (440 verses)
5. **Weeks 9-10:** Quality assurance and gap filling
6. **Week 11:** Export, document, and release v1.0

**Total Timeline:** 11 weeks (approximately 3 months)

**Expected Deliverable:**  
A production-ready dataset of 2,400+ fully-validated Arabic poetry verses across 20 classical meters, suitable for training state-of-the-art prosody detection models.

---

**Document End**
