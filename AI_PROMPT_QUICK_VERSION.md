# Quick AI Prompt: Find 10 المتدارك Verses

**Copy-paste this concise version:**

---

## Mission
Find **10 authentic Arabic poetry verses** in المتدارك (al-Mutadārak) meter for ML training data.

## What is المتدارك?
- Also called: الخبب, المحدث
- Pattern: فاعلن فاعلن فاعلن فاعلن (4 feet)
- With خبن: فعلن فعلن فعلن فعلن → phonetic: `///o///o///o///o`
- Extremely rare: <1% of classical poetry

## Tasks

### 1. Modern Poetry (PRIORITY - Need 8 verses)

**Target poets who used المتدارك:**
- بدر شاكر السياب (most likely)
- نزار قباني
- محمود درويش
- عبد الوهاب البياتي
- صلاح عبد الصبور

**How to find:**
- Google Scholar: "المتدارك" + [poet name]
- Search: "الخبب في شعر السياب"
- Check dissertations on modern Arabic prosody
- Use: Dīwān al-ʿArab (https://www.diwanalarab.com/)

**Must have:**
- Full verse with diacritics
- Academic source confirming it's المتدارك
- Complete citation (book, page, year)

### 2. Synthetic Verses (Need 2 verses)

Create 2 grammatically correct verses following المتدارك pattern:

**Verse 1:** Mixed pattern
- فاعلن فعلن فاعلن فع
- Phonetic: `/o//o///o/o//o/o/`

**Verse 2:** Rare variant
- فاعلن فاعلن فعلن فاع
- Phonetic: `/o//o/o//o///o/o/`

## Output Format

```json
{
  "verse_id": "mutadarik_sayyab_001",
  "text": "[Arabic with tashkeel]",
  "normalized_text": "[Arabic without tashkeel]",
  "meter": "المتدارك",
  "poet": "[Name]",
  "source": "[Book, author, page]",
  "era": "modern",
  "expected_tafail": ["فاعلن", "فعلن", "فاعلن", "فاع"],
  "phonetic_pattern": "/o//o///o/o//o/o/",
  "notes": "[Why valuable]",
  "validation": {
    "verified_by": ["[Academic source]"],
    "verified_date": "2025-11-12",
    "reference_sources": ["[Full citation]"]
  }
}
```

## Validation Checklist
- [ ] 8 modern verses from named poets
- [ ] 2 synthetic verses (grammatically correct)
- [ ] All have diacritics or clear scansion
- [ ] Academic sources cited
- [ ] Not disputed as different meter

## Search Hints
- "المتدارك في الشعر الحديث"
- "بحر الخبب عند السياب"
- "prosodic analysis [poet name]"

**Deliver:** JSONL file with 10 verses, each on separate line.

**Time:** 3-5 hours | **Difficulty:** Moderate

---

Focus on **السياب** first - he's most likely to have المتدارك examples in modernist collections!
