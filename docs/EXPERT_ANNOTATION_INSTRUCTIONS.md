# Expert Annotation Instructions for المتدارك Corpus

**Thank you for participating in this research!**

Your expertise in Arabic prosody is crucial for validating a collection of verses in المتدارك (al-Mutadārak) meter for an automatic meter detection system.

---

## 📋 Task Overview

**What you'll do:** Annotate 13 Arabic poetry verses

**Time required:** 2-3 hours

**Deadline:** [To be specified]

**Format:** Complete the provided annotation spreadsheet

---

## 🎯 Your Annotation Task

For each verse, please provide:

### 1. Meter Identification

**Primary Meter:** Select the meter that best describes the verse

Options:
- المتدارك (al-Mutadārak)
- المتقارب (al-Mutaqārib)
- الرجز (al-Rajaz)
- الخفيف (al-Khafīf)
- الرمل (al-Ramal)
- الهزج (al-Hazaj)
- Other: [specify]
- Ambiguous (mark in notes)

**Confidence Level:** How confident are you in this identification?

Scale:
- 1 = Very uncertain (could be multiple meters)
- 2 = Somewhat uncertain (leaning toward this meter)
- 3 = Moderately confident (likely this meter)
- 4 = Confident (definitely this meter)
- 5 = Very confident (absolutely certain)

**Alternative Meter:** If the verse could plausibly be another meter, note it here

---

### 2. Prosodic Scansion (التقطيع)

**Tafāʿīl Breakdown:** Write the complete tafāʿīl sequence

Example:
```
Verse: مَا لِي حَبِيبٌ سِوَى الأَمَلْ يَأْتِي بِهِ اللَّيْلُ وَالْأَزَلْ
Scansion: فاعلن فعلن فاعلن فاعل
```

**Format:** Use Arabic prosodic foot names separated by spaces
- فاعلن, فعلن, فاع, فاعل, فعولن, مفاعيلن, etc.

---

### 3. Ziḥāfāt Identification

**Which positions have ziḥāfāt (prosodic variations)?**

Format: Position numbers with زحاف type

Example:
```
Position 2: خبن
Position 4: خبن
```

Common ziḥāfāt for المتدارك:
- خبن (khabn) - Most common
- طي (ṭayy)
- قبض (qabḍ)

If no ziḥāfāt: Write "None" or "Canonical"

---

### 4. ʿIlal Identification (if present)

**Final position ʿillah (ending variation)?**

Common ʿilal for المتدارك:
- حذف (ḥadhf) - Most common (فاعلن → فاعل)
- قصر (qaṣr) - Rare (فاعلن → فاع)
- None (canonical ending)

---

### 5. Disambiguation Notes

**If the verse is ambiguous or could be confused with another meter:**

Please explain:
- Why you chose this meter over the alternative
- What features distinguish it
- Any concerns about the classification

**Example:**
```
"This verse uses فاعلن pattern which is shared by both المتدارك and
المتقارب. I identified it as المتدارك because it has 4 tafāʿīl
(المتدارك standard) rather than the longer المتقارب form. However,
without musical context, there is some ambiguity."
```

---

### 6. Quality Assessment

**A. Is this a valid example of the identified meter?**
- Yes - This verse correctly exemplifies the meter
- No - This verse does not fit the meter
- Uncertain - Ambiguous or problematic

**B. Naturalness Rating (for synthetic/modern verses)**

Rate how natural the verse sounds (1-5):
- 1 = Very awkward/unnatural
- 2 = Somewhat awkward
- 3 = Acceptable but not ideal
- 4 = Natural and fluent
- 5 = Excellent, sounds like authentic poetry

**C. Additional Notes**

Any other observations, concerns, or comments about this verse.

---

## 📖 Annotation Examples

### Example 1: Clear المتدارك with خبن

**Verse:**
```
كَمْ مِنْ لَيَالٍ قَدْ مَضَتْ وَانْقَضَتْ وَالْعُمْرُ يَمْضِي سَرِيعًا لَا يَثْبُتْ
```

**Annotation:**

| Field | Your Answer |
|-------|-------------|
| Primary Meter | المتدارك |
| Confidence | 4 - Confident |
| Alternative Meter | None |
| Tafāʿīl | فعلن فعلن فعلن فعلن |
| Ziḥāfāt | All positions: خبن |
| ʿIlal | None (canonical ending) |
| Valid Example? | Yes |
| Naturalness | 4 - Natural |
| Notes | Clear المتدارك with maximal khabn throughout. Letter-based notation (فَعِلُنْ). Theme is philosophical (passage of time). |

---

### Example 2: Ambiguous Case

**Verse:**
```
يَا صَاحِبِي قَدْ جَاءَ وَقْتُ الرَّحِيلْ وَالْقَلْبُ لَمْ يَنْسَ الْحَبِيبَ الْجَمِيلْ
```

**Annotation:**

| Field | Your Answer |
|-------|-------------|
| Primary Meter | المتدارك |
| Confidence | 3 - Moderately confident |
| Alternative Meter | المتقارب |
| Tafāʿīl | فاعلن فاعلن فاعلن فاعلن |
| Ziḥāfāt | None (canonical) |
| ʿIlal | None |
| Valid Example? | Yes |
| Naturalness | 4 - Natural |
| Notes | Canonical فاعلن pattern could be either المتدارك or المتقارب. I lean toward المتدارك because it uses 4 tafāʿīl (standard for المتدارك تام). However, without performance/musical context, this is somewhat ambiguous. |

---

## 🔍 Guidelines for Ambiguous Cases

### المتدارك vs المتقارب

Both meters use فاعلن base pattern. Key distinguishing features:

**المتدارك characteristics:**
- Typically 4 tafāʿīl (تام) or 3 tafāʿīl (مجزوء)
- Often appears with خبن (→ فعلن or فَعِلُنْ)
- Fast, rhythmic feel (الخبب = "galloping")
- More common in modern poetry

**المتقارب characteristics:**
- Typically 8 tafāʿīl (longer)
- Pattern: فعولن with variations
- More flowing, slower rhythm
- Classical meter

**When ambiguous:**
- Mark confidence as 2-3
- Note both possible meters
- Explain your reasoning

### المتدارك vs الرجز

**Key distinction:**
- المتدارك: Uses فاعلن (4 syllables)
- الرجز: Uses مستفعلن (6 syllables)

If you see فاعلن pattern, it's likely المتدارك or المتقارب, not الرجز.

---

## ⚠️ Important Notes

### Blind Annotation

**Please annotate independently** without:
- Discussing with other annotators
- Looking up automated detection results
- Assuming what the "correct" answer should be

**Trust your expertise!** We want your genuine professional judgment.

### Synthetic vs. Classical Verses

Some verses may be:
- From classical prosody textbooks
- From modern poetry
- Synthetic (created for testing purposes)

**Please annotate all verses equally** based on their prosodic structure, regardless of source.

### Naturalness Ratings

For verses that seem synthetic or artificial:
- This is expected and valuable feedback
- Rate honestly based on how they sound
- Note any awkward phrasing or word choices
- Low ratings help us improve future verse generation

---

## 🤔 Frequently Asked Questions

### Q: What if I can't determine the meter?

**A:** Mark your confidence as 1 or 2, note possible alternatives, and explain your uncertainty in the notes field. It's okay to say "ambiguous" - that's valuable data.

### Q: What if the verse seems incorrect or problematic?

**A:** Mark "Valid Example?" as "No" or "Uncertain" and explain the issue in notes. We want to know if any verses are problematic.

### Q: Can I change my mind after submitting?

**A:** Yes, if you realize an error, please contact us immediately. We can accept revised annotations before the final analysis.

### Q: How long should this take per verse?

**A:** Typically 5-10 minutes per verse. Some may be quicker (clear-cut cases), others may take longer (ambiguous cases requiring careful analysis).

### Q: Should I use diacritics in my scansion?

**A:** Not required, but you may include them if helpful for clarity. Plain Arabic prosodic foot names are sufficient.

### Q: What if I recognize a verse from classical literature?

**A:** That's fine! Annotate based on its prosodic structure. If you know the source, you can mention it in notes, but it doesn't affect the annotation task.

---

## 📧 Contact Information

**Questions during annotation:**
- Email: [To be filled in]
- Expected response time: Within 24 hours

**Technical issues with spreadsheet:**
- Email: [To be filled in]

**Deadline concerns:**
- Contact us immediately if you need an extension

---

## 🙏 Thank You!

Your contribution to this research is invaluable. The validated dataset you help create will:

- Improve automatic Arabic meter detection
- Advance Arabic NLP research
- Preserve and promote understanding of classical prosody
- Support computational analysis of Arabic poetry

We greatly appreciate your time and expertise!

---

## 📋 Checklist Before Submitting

- [ ] All 13 verses annotated
- [ ] No blank fields (except "Alternative Meter" if not applicable)
- [ ] Confidence scores provided (1-5)
- [ ] Tafāʿīl scansion written for all verses
- [ ] Notes provided for ambiguous or low-confidence cases
- [ ] Spreadsheet saved with your name: `annotation_[YourLastName].csv`
- [ ] File emailed to: [To be filled in]

---

**Version:** 1.0
**Date:** 2025-11-12
**Estimated Time:** 2-3 hours
**Questions?** Contact [To be filled in]

Thank you for your participation! 🙏
