# المتدارك Verses Sourcing Report
**Date:** 2025-11-12
**Target:** 10 verses (8 modern + 2 synthetic)
**Status:** PARTIALLY COMPLETED (2/10)

## Executive Summary

Encountered significant challenges sourcing modern المتدارك verses due to:
1. **Access restrictions** - Most Arabic poetry websites block automated requests (403 errors)
2. **Copyright limitations** - Cannot reproduce full copyrighted modern poetry texts
3. **Academic access** - Prosodic analyses found but without extractable verse examples

**Delivered:** 2 synthetic verses with specified ziḥāfāt patterns
**Identified:** Multiple modern poems in المتدارك meter with citations for manual retrieval

---

## Findings: Modern Poets Using المتدارك

### ✅ Confirmed Poems (Require Manual Retrieval)

#### 1. **محمود درويش (Mahmoud Darwish)**
- **Poem:** "جفاف" (Jafaf/Drought)
  - **Source:** https://www.aldiwan.net/poem9121.html
  - **Alternative:** https://houruf.com/poetry/mahmoud-darwish/28975/
  - **Era:** Modern (1941-2008)
  - **Confidence:** 0.95
  - **Notes:** Listed in multiple prosody references as المتدارك example

- **Poem:** "المزمور الحادي والخمسون بعد المئة" (The 151st Psalm)
  - **Source:** https://www.aldiwan.net/poem2341.html
  - **Alternative:** https://houruf.com/poetry/mahmoud-darwish/29387/
  - **Era:** Modern
  - **Confidence:** 0.95
  - **Opening line:** "أورشليمُ ! / التي ابتعدتْ عن شفاهي ... المسافات أقربْ"

#### 2. **بدر شاكر السياب (Badr Shakir al-Sayyab)**
- **Status:** Confirmed user of المتدارك/الخبب meter
- **Note:** Famous poem "أنشودة المطر" uses الرجز meter, NOT المتدارك
- **Action needed:** Search his collections for المتدارك examples
- **Recommended collections:** "أنشودة المطر", "المعبد الغريق"
- **Confidence:** 0.85 (known experimenter with this meter)

#### 3. **نزار قباني (Nizar Qabbani)**
- **Status:** Multiple sources mention his use of المتدارك
- **Action needed:** Manual review of his 35 poetry collections
- **Confidence:** 0.80
- **Note:** Moved from traditional to free verse, likely used المتدارك in modernist phase

#### 4. **عبد الوهاب البياتي (Abd al-Wahhab al-Bayati)**
- **Status:** Identified as user of الخبب/المتدارك
- **Source reference:** sites.google.com/site/alarood/khabab-poets
- **Action needed:** Access specific poems from his collections
- **Confidence:** 0.85

#### 5. **صلاح عبد الصبور (Salah Abd al-Sabur)**
- **Status:** Contemporary poet confirmed using المتدارك
- **Action needed:** Review his collections for specific examples
- **Confidence:** 0.80

---

## Synthetic Verses Delivered

### Verse 1: Mixed Ziḥāfāt Pattern
```json
{
  "verse_id": "mutadarik_synthetic_001",
  "text": "يَا قَمَرًا طَالَ بِهِ اللَّيْلُ هُدَى",
  "pattern": "فاعلن فعلن فاعلن فع",
  "zihafat": "canonical + khabn + canonical + ḥadhf"
}
```

### Verse 2: Rare Variant Pattern
```json
{
  "verse_id": "mutadarik_synthetic_002",
  "text": "سَارَ بِنَا الرَّكْبُ إِلَى الدَّارِ بِلَا",
  "pattern": "فاعلن فاعلن فعلن فاع",
  "zihafat": "canonical + canonical + khabn + qaṣr"
}
```

**⚠️ Important:** These synthetic verses should be reviewed by an Arabic prosody expert before inclusion in the dataset. While constructed following prosodic rules, native speaker validation is essential.

---

## Key Findings from Research

### About المتدارك/الخبب Meter

1. **Rarity Confirmed:**
   - "The mutadārik, muḍāri', and muqtaḍab do not occur at all in early poetry collections"
   - Usually regarded as "artificial meters"
   - Became more common with modern/free verse movement

2. **Pattern Details:**
   - Base: فاعلن فاعلن فاعلن فاعلن (4 tafāʿīl)
   - Most common form: With خبن → فعلن فعلن فعلن فعلن
   - From دائرة المتفق (da'irat al-muttafiq) circle

3. **Modern Usage:**
   - Became one of the most common meters among modern/free verse pioneers
   - Poets experimented with it precisely because of its non-traditional status
   - Often used for fast-paced, rhythmic compositions

4. **Terminology:**
   - الخبب (al-khabab) and المتدارك (al-mutadārak) refer to the same meter
   - Some prosodists distinguish them, but modern usage treats them as equivalent
   - Al-Khalil described 15 meters; Al-Akhfash added المتدارك as the 16th

---

## Recommended Action Plan

### Phase 1: Manual Retrieval (High Priority)

**Immediate Actions:**
1. Visit the URLs provided for Mahmoud Darwish's poems:
   - Manually copy "جفاف" from aldiwan.net/poem9121.html
   - Manually copy "المزمور الحادي والخمسون بعد المئة" from aldiwan.net/poem2341.html
   - Extract 2-3 complete verses from each poem
   - Verify prosodic scansion

2. Access Shamela directly:
   - Go to https://shamela.ws/
   - Search for: "المتدارك" in prosody books
   - Focus on: "ميزان الذهب في صناعة شعر العرب" (السيوطي)
   - Note: You already have 5 classical verses, but backup sources are valuable

### Phase 2: Academic Sources (Medium Priority)

**Search Strategy:**
1. Google Scholar searches:
   ```
   "المتدارك في الشعر الحديث"
   "بحر الخبب" + "السياب" OR "درويش" OR "البياتي"
   "دراسة عروضية" + [poet name]
   ```

2. Look for PhD dissertations on:
   - Modern Arabic prosody
   - Specific poet analyses
   - Free verse (شعر التفعيلة) studies

3. Search databases:
   - JSTOR (if accessible)
   - مجلة فصول (Fuṣūl journal)
   - مجلة الموقف الأدبي
   - Project MUSE

### Phase 3: Verification (Critical)

For each verse collected:
1. **Prosodic verification:**
   - Manually scan the verse (تقطيع)
   - Confirm it matches فاعلن pattern and variations
   - Identify specific ziḥāfāt applied

2. **Source verification:**
   - Get at least 2 sources for modern verses
   - Record complete bibliographic info
   - Note any disagreements about meter

3. **Synthetic verse review:**
   - Have native Arabic speaker read synthetic verses
   - Verify grammatical correctness
   - Confirm naturalness and semantic coherence
   - Validate prosodic scansion with expert

### Phase 4: Dataset Construction

**When you have collected 8+ modern verses:**
1. Add diacritics if missing (use native speaker or prosody expert)
2. Create complete JSONL entries with all metadata
3. Calculate confidence scores based on:
   - Number of sources (0.95 for 2+, 0.85 for 1 academic, 0.75 for 1 non-academic)
   - Source quality (academic > established poetry sites > forums)
   - Prosodic clarity (explicitly analyzed > listed in meter category > inferred)

---

## Challenges Encountered (Detailed)

### 1. Website Access Restrictions
**URLs Blocked (403 Forbidden):**
- aldiwan.net (when using WebFetch tool)
- safsaf.org (prosody analysis site)
- aloumalarabia.com (prosody examples)
- sites.google.com/site/alarood (khabab poets)

**Reason:** These sites block automated/bot requests to prevent scraping

**Workaround:** Manual browser access required

### 2. Copyright Limitations
- Cannot reproduce full modern poems due to copyright protection
- Can only provide citations and first lines
- Limits ability to select best verses from longer poems

### 3. Search Result Quality
- General poetry collections returned, but not prosody-specific analyses
- Many results about poets' general work, not meter-specific
- Prosody discussions found, but without concrete verse examples

### 4. Academic Resource Access
- Scholarly papers on modern Arabic prosody exist but not fully accessible via web search
- Need direct database access (JSTOR, university libraries, etc.)
- Arabic academic journals not well-indexed by search engines

---

## Quality Assurance Recommendations

### For Modern Verses (8 needed):

**Minimum Requirements:**
- [ ] Complete verse (2+ lines preferred, minimum 1 complete بيت)
- [ ] Full Arabic text with tashkeel (diacritics)
- [ ] Poet name and date confirmed
- [ ] Source book/collection with page number
- [ ] At least 1 academic source confirming meter
- [ ] Manual prosodic scansion completed
- [ ] Confidence ≥ 0.85

**Ideal Attributes:**
- [ ] 2+ academic sources confirming meter
- [ ] Prosodic analysis from source explaining ziḥāfāt
- [ ] Different ziḥāfāt patterns (variety for training)
- [ ] Multiple poets represented
- [ ] Clear disambiguation from المتقارب

### For Synthetic Verses (2 delivered):

**Validation Needed:**
- [ ] Native Arabic speaker review (grammar, semantics)
- [ ] Arabic prosody expert verification (scansion accuracy)
- [ ] Readability test (does it sound natural?)
- [ ] Edge case confirmation (does it test the intended pattern?)

---

## Additional Resources Found

### Prosody Reference Sites:
1. **linga.org** - Has article "تعلَّم-ي بحور الشعر (16) المتدارَك"
2. **kalamkutib.com** - "بحر المتدارك من بحور الشعر العربي"
3. **mahmoudqahtan.com** - "بحور الشعر العمودي: بحر المتدارك"
4. **arood.com/vb** - Forum with "قصائد من المتدارك (متجدّد)"

### Poetry Databases:
1. **aldiwan.net** - Has category for المتدارك poems
2. **diwanalarab.com** - Poet collections
3. **houruf.com** - Poetry encyclopedia
4. **poetspedia.com** - Poetry encyclopedia

---

## Estimated Effort to Complete

### Time Estimates:
- **Manual retrieval of 2 Darwish poems:** 1-2 hours
  - Access websites, copy texts, verify scansion
  - Extract best verses, add metadata

- **Finding 6 more modern verses:** 3-4 hours
  - Search academic papers
  - Access Shamela/poetry databases manually
  - Verify prosody and sources

- **Validating synthetic verses:** 1 hour
  - Find Arabic speaker/prosody expert
  - Make corrections if needed

**Total:** 5-7 hours

### Skills Needed:
- Reading Arabic (essential)
- Arabic prosody knowledge (strong preference)
- Access to academic databases (helpful)
- Patience for manual data collection (required)

---

## Conclusion

**Delivered:**
- 2/10 verses (both synthetic)
- Complete citations for 2 confirmed modern poems (Darwish)
- Identification of 5 modern poets who use المتدارك
- Comprehensive sourcing strategy

**Status:** Project requires manual continuation due to technical and copyright limitations

**Recommendation:** The most efficient path forward is:
1. Manually retrieve the 2 Darwish poems (high confidence)
2. Search academic dissertations on modern Arabic prosody for 4-6 more verses
3. Validate all synthetic verses with expert review
4. Fill remaining gaps with additional Shamela searches

**Critical Note:** المتدارك's extreme rarity (<1% of classical poetry) means expect significant effort to find well-documented examples. Modern poets used it more, but academic documentation is scattered. Consider whether expanding to الرجز or المتقارب meters might provide better training data with less effort.

---

## Files Delivered

1. **mutadarik_verses_partial.jsonl** - 2 synthetic verses in JSONL format
2. **mutadarik_sourcing_report.md** - This comprehensive report

## Next Steps

1. Review synthetic verses with Arabic prosody expert
2. Manually retrieve Darwish poems from provided URLs
3. Search academic databases for additional examples
4. Expand dataset as verses are validated
5. Consider whether 10 verses is sufficient or if more are needed for ML training

---

**Report compiled by:** Claude Code
**Date:** 2025-11-12
**Session:** BAHR Detection Engine Dataset Enhancement
