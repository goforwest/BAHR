# Shamela Search Guide for المتدارك Verses

**Purpose:** Step-by-step instructions to find authentic المتدارك verses from classical sources
**Target:** 5-10 candidate verses for expert validation
**Estimated Time:** 2-4 hours

---

## 🔍 Search Strategy

### Option 1: Direct Meter Search (Recommended First)

**Access Shamela:** https://shamela.ws/

**Step 1: Advanced Search**
1. Go to advanced search
2. Search in: **كتب الأدب → الشعر** (Literature → Poetry)
3. Search terms to try:

```
Search Term 1: "بحر المتدارك"
Search Term 2: "المتدارك"
Search Term 3: "الخبب" (alternative name)
Search Term 4: "فاعلن فاعلن فاعلن فاعلن" (pattern)
```

**Step 2: Filter Results**
- Focus on prosody textbooks first (most reliable)
- Look for books with "العروض" or "الأوزان" in title
- Prioritize classical sources (pre-1900)

---

### Option 2: Prosody Textbook Search (Most Reliable)

**Target Books on Shamela:**

1. **الكافي في العروض والقوافي** - التبريزي
   - Shamela Book ID: 26347
   - Navigate to: المتدارك chapter
   - Usually has 2-3 example verses with full scansion

2. **القسطاس في علم العروض** - الزمخشري
   - Search within book for "المتدارك"
   - Extract example verses

3. **ميزان الذهب في صناعة شعر العرب** - السيوطي
   - Contains المتدارك examples
   - Cross-referenced with multiple sources

4. **العقد الفريد في علم العروض** - Various authors
   - Search for المتدارك section

**How to Access:**
```
1. Go to Shamela.ws
2. Click "البحث في كتاب معين" (Search within a specific book)
3. Enter book name or ID
4. Search for "المتدارك"
5. Navigate to relevant sections
```

---

### Option 3: Andalusian Muwashshaḥāt (Higher Yield)

**Why:** Andalusian poetry experimented with rare meters

**Search Strategy:**
```
1. Search: "موشح" + "المتدارك"
2. Alternative: "موشحات" + "خبب"
3. Filter: Andalusian period (800-1400 CE)
```

**Target Collections:**
- جيش التوشيح (لسان الدين بن الخطيب)
- دار الطراز في عمل الموشحات (ابن سناء الملك)

---

## 📝 Extraction Protocol

**For Each Candidate Verse:**

### Step 1: Record Source Information
```
Book Title: _______________________
Author: __________________________
Edition: __________________________
Page Number: ______________________
Shamela Book ID: __________________
Direct URL (if available): _________
```

### Step 2: Copy Full Verse
- Copy the complete verse text
- Include ALL diacritics (tashkeel)
- Note if diacritics are missing
- Copy the prosodic scansion (تقطيع) if provided

### Step 3: Record Prosodic Analysis
If the source provides analysis, record:
- Tafāʿīl breakdown: _______________________
- Ziḥāfāt applied: _________________________
- ʿIlal applied: ___________________________
- Variant type (صحيح، محذوف، etc.): __________

### Step 4: Cross-Reference
Search for the verse in:
- Google (first line in quotes)
- al-Warraq (if accessible)
- Other prosody textbooks

**Goal:** Confirm 2+ sources agree it's المتدارك

---

## ✅ Quality Checklist

**Before accepting a verse, verify:**

- [ ] Source is reputable (classical prosody textbook or authenticated anthology)
- [ ] Full diacritics (tashkeel) present OR can be added confidently
- [ ] Prosodic scansion provided in source OR can be verified
- [ ] At least 2 sources confirm it's المتدارك (not attributed to other meters elsewhere)
- [ ] Verse is complete (not fragmentary)
- [ ] Source provides page number / citation for reproducibility

---

## 🚩 Red Flags - DO NOT Accept If:

1. **Single source only** - Cannot verify authenticity
2. **No diacritics AND no scansion** - Too ambiguous
3. **Modern online forum** - Not authenticated
4. **Disputed attribution** - Some sources say المتدارك, others say different meter
5. **Incomplete verse** - Cannot validate full pattern
6. **Anonymous source** - No author/book citation

---

## 📊 Expected Yield

**Realistic expectations:**

| Source Type | Expected Verses | Time Required |
|-------------|-----------------|---------------|
| Prosody textbooks | 2-4 verses | 1-2 hours |
| Muwashshaḥāt | 2-3 verses | 2-3 hours |
| Classical anthologies | 1-2 verses | 2-4 hours |
| **TOTAL** | **5-9 verses** | **5-9 hours** |

**Note:** المتدارك is EXTREMELY rare - finding even 5 authentic verses is a success.

---

## 🔧 Validation After Extraction

**For each verse found:**

1. **Create JSONL entry** using template:
```json
{
  "verse_id": "mutadarik_shamela_001",
  "text": "[Full Arabic text with tashkeel]",
  "meter": "المتدارك",
  "source": "[Book name, author, page]",
  "shamela_book_id": "26347",
  "expected_tafail": ["فاعلن", "فاعلن", "فاعلن", "فاع"],
  "phonetic_pattern": "/o//o/o//o/o//o/o/",
  "era": "classical",
  "notes": "[Any observations]"
}
```

2. **Run validator:**
```bash
cd /home/user/BAHR/tools
python mutadarik_validator.py --verse "[text]" --tafail "فاعلن,فاعلن,فاعلن,فاع"
```

3. **Review validation results:**
   - Check confusion risk with المتقارب
   - Note confidence scores
   - Document disambiguation reasoning

4. **Track results:**
   - PASSED → Add to golden set candidates
   - FAILED → Document why, set aside for expert review
   - NEEDS_REVIEW → Flag for expert panel

---

## 📋 Recommended Workflow

### Session 1 (2 hours): Prosody Textbooks
- [ ] Access الكافي في العروض والقوافي on Shamela
- [ ] Find المتدارك chapter
- [ ] Extract 2-3 example verses
- [ ] Record full citations
- [ ] Run validator on each

### Session 2 (2-3 hours): Muwashshaḥāt
- [ ] Search for Andalusian poetry collections
- [ ] Filter for المتدارك or خبب mentions
- [ ] Extract 2-3 verses
- [ ] Cross-reference with other sources
- [ ] Validate

### Session 3 (2 hours): Cross-Validation
- [ ] For all candidates, verify with 2nd source
- [ ] Google search first lines
- [ ] Check al-Warraq if accessible
- [ ] Resolve any disputed attributions

---

## 💡 Pro Tips

1. **Start with textbooks** - Most reliable, already analyzed by experts
2. **Copy source metadata** - You'll need it for citations later
3. **Don't trust single sources** - Always cross-reference
4. **Expect low yield** - المتدارك is genuinely rare
5. **Document everything** - Even rejected verses teach us something
6. **Use validator liberally** - Better to reject than add bad data

---

## 🎯 Success Criteria

**Goal:** 5 verified classical المتدارك verses

**"Verified" means:**
- [ ] 2+ authoritative sources confirm المتدارك
- [ ] Full diacritics present
- [ ] Complete prosodic scansion available or derivable
- [ ] Source citation complete and reproducible
- [ ] Validator shows reasonable confidence (even if المتقارب also matches)
- [ ] Expert review scheduled for final confirmation

---

## 📞 Next Steps After Shamela Search

1. **Compile results** into structured JSONL
2. **Run batch validation** on all candidates
3. **Identify verses needing expert review**
4. **Move to modern poetry sources** (Phase 2B)
5. **Schedule expert annotation session** (Phase 3)

---

## 📚 Backup Resources If Shamela Insufficient

If Shamela yields < 3 verses:

1. **al-Warraq** (https://www.alwaraq.net/)
   - Similar strategy, different database

2. **Physical prosody textbooks**
   - University libraries
   - Scan relevant pages

3. **Academic papers**
   - Search Google Scholar: "المتدارك" + "أمثلة"
   - PhD dissertations on rare meters

4. **Accept lower classical count**
   - Proceed with 3 classical + increase modern to 10

---

**Document Owner:** BAHR Detection Engine Team
**Status:** Ready for execution
**Estimated Time:** 5-9 hours total searching
**Expected Yield:** 5 classical المتدارك verses
