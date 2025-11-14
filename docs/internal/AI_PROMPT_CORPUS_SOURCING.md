# AI Prompt: Source المتدارك Verses for BAHR Detection Engine

**Copy this prompt to give to an AI assistant with web access:**

---

## Mission

I need your help sourcing **10 authentic Arabic poetry verses** in the المتدارك (al-Mutadārak) meter for a machine learning dataset. This meter is extremely rare (<1% of classical poetry) and critical for achieving 100% accuracy in Arabic prosody detection.

## Context

**Current Progress:**
- ✅ 5 classical verses validated from Shamela
- 🎯 Need: 10 more verses (0 classical, 8 modern, 2 synthetic)
- 📊 Total target: 15 verses minimum

**Why المتدارك is challenging:**
- Also called الخبب or المحدث
- Base pattern: فاعلن فاعلن فاعلن فاعلن (4 tafāʿīl)
- Phonetic: `/o//o/o//o/o//o/o//o`
- Most commonly appears with خبن (khabn): فعلن فعلن فعلن فعلن
- Phonetic with khabn: `///o///o///o///o`
- Easily confused with المتقارب meter

## Your Tasks

### Task 1: Shamela Search (0 more classical verses needed)

**Status:** ✅ Sufficient classical verses obtained (5/5)

**If you want to find more as backup:**
1. Go to https://shamela.ws/
2. Search in these books:
   - **ميزان الذهب في صناعة شعر العرب** (السيوطي)
   - **العقد الفريد في علم العروض**
   - **جيش التوشيح** (لسان الدين بن الخطيب) - Andalusian muwashshaḥāt
   - **دار الطراز في عمل الموشحات** (ابن سناء الملك)

3. Search terms: "المتدارك" OR "الخبب" OR "فاعلن فاعلن فاعلن"

4. For each verse found:
   - Copy full Arabic text with diacritics
   - Record: Book title, author, page number, Shamela URL
   - Note the prosodic scansion (تقطيع) if provided
   - Verify at least 2 sources confirm it's المتدارك

### Task 2: Modern Poetry (PRIORITY - Need 8 verses)

**Target Poets Known for المتدارك:**

1. **بدر شاكر السياب** (Badr Shakir al-Sayyab, 1926-1964)
   - Known for experimenting with المتدارك/الخبب
   - Search: "السياب" + "المتدارك" OR "السياب" + "الخبب"
   - Look for poems with fast, rhythmic meter
   - Check collections: "أنشودة المطر", "المعبد الغريق"

2. **نزار قباني** (Nizar Qabbani, 1923-1998)
   - Used المتدارك in some modernist poems
   - Search: "نزار قباني" + "المتدارك"
   - Focus on shorter, lyrical pieces

3. **محمود درويش** (Mahmoud Darwish, 1941-2008)
   - Experimented with various meters including المتدارك
   - Search: "محمود درويش" + "المتدارك"
   - Check: "أحد عشر كوكباً", "لماذا تركت الحصان وحيداً"

4. **عبد الوهاب البياتي** (Abd al-Wahhab al-Bayati, 1926-1999)
   - Iraqi modernist who used المتدارك
   - Search: "البياتي" + "الخبب"

5. **صلاح عبد الصبور** (Salah Abd al-Sabur, 1931-1981)
   - Egyptian modernist
   - Search: "صلاح عبد الصبور" + "المتدارك"

**Search Strategy:**
- Use Google Scholar: "المتدارك" + [poet name] + "ديوان"
- Check academic papers analyzing these poets' prosody
- Look for dissertations on modern Arabic meter usage
- Search poetry databases: Dīwān al-ʿArab (https://www.diwanalarab.com/)

**Quality Requirements for Modern Verses:**
- ✅ Verse has clear prosodic structure
- ✅ At least one academic source identifies it as المتدارك
- ✅ Complete verse (not fragment)
- ✅ You can provide citation: Book/collection name, page, year
- ⚠️ Avoid verses where prosody is disputed

### Task 3: Create 2 Synthetic Verses

**Purpose:** Test edge cases and ziḥāfāt variations

**Requirements:**

**Synthetic Verse 1: Mixed Ziḥāfāt**
- Pattern: فاعلن فعلن فاعلن فع (canonical + khabn + canonical + ḥadhf)
- Phonetic: `/o//o///o/o//o/o/`
- Must be grammatically correct Arabic
- Should make semantic sense
- Theme: Nature, love, wisdom, or classical poetry themes

**Synthetic Verse 2: Rare Variant**
- Pattern: فاعلن فاعلن فعلن فاع (2 canonical + khabn + qaṣr)
- Phonetic: `/o//o/o//o///o/o/`
- Must be grammatically correct Arabic
- Should sound natural
- Theme: Any classical theme

**How to Create Synthetic Verses:**
1. Choose the tafāʿīl pattern
2. Map syllables to Arabic words following the pattern
3. Ensure grammatical correctness
4. Verify the verse scans correctly
5. Test readability (would a native speaker understand it?)

**Syllable Mapping Guide:**
- `/o` = CV̄ (long syllable): فَا, مَا, لِي, etc.
- `/` = CV (short syllable): بِ, تَ, نَ, etc.
- `/o` = CVC: فَعْ, لَنْ, بِنْ, etc.

## Output Format

For **EACH verse** found, provide in JSONL format:

```json
{
  "verse_id": "mutadarik_[source]_[number]",
  "text": "[Full Arabic text with tashkeel]",
  "normalized_text": "[Text without tashkeel]",
  "meter": "المتدارك",
  "poet": "[Poet name or 'synthetic']",
  "source": "[Book/collection name, author, page]",
  "era": "[classical/modern/synthetic]",
  "confidence": [0.80-1.0],
  "taqti3": "[فاعلن فعلن فاعلن فاع - prosodic scansion]",
  "expected_tafail": ["فاعلن", "فعلن", "فاعلن", "فاع"],
  "phonetic_pattern": "/o//o///o/o//o/o/",
  "syllable_count": [number],
  "zihafat_applied": {
    "position_2": "خبن",
    "position_4": "حذف"
  },
  "edge_case_type": "[canonical/khabn_multiple/hadhf_final/etc]",
  "difficulty_level": "[easy/medium/hard]",
  "notes": "[Any observations about why this verse is valuable]",
  "validation": {
    "verified_by": ["[Source 1]", "[Source 2]"],
    "verified_date": "2025-11-12",
    "automated_check": "PENDING",
    "disambiguation_notes": "[How to distinguish from المتقارب]",
    "reference_sources": ["[Full citation]"]
  }
}
```

## Validation Checklist

Before submitting each verse, verify:

- [ ] Full Arabic text with diacritics (or clearly marked if missing)
- [ ] At least 1 authoritative source (2+ for classical)
- [ ] Complete verse (not fragmentary)
- [ ] Prosodic scansion matches المتدارك (4 tafāʿīl typical)
- [ ] Not disputed as different meter elsewhere
- [ ] Full citation provided for reproducibility
- [ ] Confidence score reflects source quality (0.8-1.0)

## Red Flags - DO NOT Include

❌ Verses from online forums without academic backing
❌ Disputed attributions (some say المتدارك, others say المتقارب)
❌ Incomplete verses
❌ No diacritics AND no prosodic scansion
❌ Single uncorroborated source
❌ Modern verses without scholarly prosodic analysis
❌ Verses shorter than 3 tafāʿīl (too short to validate properly)

## Priority Order

1. **HIGHEST PRIORITY:** Modern poetry (need 8 verses)
   - Focus on السياب first (most likely to have المتدارك)
   - Then قباني, درويش, البياتي

2. **MEDIUM PRIORITY:** Synthetic verses (need 2 verses)
   - Create after understanding patterns from real verses

3. **LOW PRIORITY:** Additional classical (optional backup)
   - Only if you find exceptional sources

## Success Criteria

**Minimum acceptable:**
- 8 modern verses (verified by academic sources)
- 2 synthetic verses (grammatically correct, prosodically valid)
- All verses in proper JSONL format
- Complete citations for all sources

**Excellent result:**
- 10+ modern verses with diverse ziḥāfāt patterns
- 2 synthetic verses testing edge cases
- Multiple sources for each modern verse
- Academic papers or dissertations cited

## Tips for Success

**Finding Modern Verses:**
1. Search Google Scholar with Arabic terms: "المتدارك في الشعر الحديث"
2. Look for PhD dissertations on meter in modern poetry
3. Check poetry analysis journals (مجلة فصول، مجلة الموقف الأدبي)
4. Search for "دراسة عروضية" + [poet name]

**Verifying Authenticity:**
1. Cross-reference first line on Google (in quotes)
2. Check multiple sources agree on meter
3. Look for scholarly prosodic analysis
4. Verify poet actually used المتدارك in their work

**Creating Quality Synthetic Verses:**
1. Study the 5 existing classical verses for patterns
2. Use common Arabic words that fit syllable structure
3. Make verses semantically coherent
4. Test by reading aloud - should sound natural
5. Have a native speaker review if possible

## Resources

**Digital Libraries:**
- Shamela: https://shamela.ws/
- Dīwān al-ʿArab: https://www.diwanalarab.com/
- al-Warraq: https://www.alwaraq.net/ (if accessible)

**Search Terms (Arabic):**
- "المتدارك في الشعر العربي الحديث"
- "بحر الخبب عند [poet name]"
- "دراسة عروضية لديوان [poet name]"
- "الأوزان الشعرية الحديثة"

**Search Terms (English):**
- "al-mutadarak meter modern arabic poetry"
- "al-khabab rhythm contemporary poets"
- "[poet name] prosodic analysis"

## Deliverable

Provide **one JSONL file** with 10 verses (8 modern + 2 synthetic), each on a separate line. Include a summary table showing:

| Verse ID | Poet | Era | Source | Confidence | Notes |
|----------|------|-----|--------|------------|-------|
| ... | ... | ... | ... | ... | ... |

---

**Estimated Time:** 3-6 hours
**Expected Yield:** 10 verses minimum
**Difficulty:** Moderate (المتدارك is rare, but modern poets used it more)

**Good luck! This work is critical for achieving 100% Arabic meter detection accuracy.**
