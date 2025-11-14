# Arabic Prosody Dataset Quality Evaluation Report
**Evaluation Date:** 2025-11-14 10:17:10
**Evaluator:** Senior Arabic NLP Researcher | Dataset Quality Engineer | ʿArūḍ Specialist
**Dataset Size:** 2032 verses
**Methodology:** 7-Phase Blueprint-Compliant Evaluation

---

## Executive Summary

- **Total Verses Evaluated:** 2032
- **Exact Duplicates:** 392 groups (1638 redundant verses)
- **Fuzzy Duplicates:** 61 pairs (≥90% similarity)
- **Prosodic Duplicates:** 0 pairs
- **Cross-Meter Anomalies:** 5 verses
- **Poet Imbalances:** 95 cases (>5% threshold)
- **Metadata Errors:** 0 issues

**Recommended Dataset Size After Deduplication:** 394 verses

---

## Phase 2: Deduplication Analysis

### Level A: Exact Duplicates

**Group 1:** 11 copies
- Text: `إِنَّ الثَّمَانِينَ وَبُلِّغْتَهَا قَدْ أَحْوَجَتْ سَمْعِي إِلَى تَرْجُمَانِ...`
- Verse IDs: basit_Classica_0001, basit_Classica_0001, basit_Classica_0001, basit_Classica_0001, basit_Classica_0001, basit_Classica_0001, sari_Classica_0003, sari_Classica_0003, sari_Classica_0003, sari_Classica_0003, sari_Classica_0003
- Meters: [3, 3, 3, 3, 3, 3, 8, 8, 8, 8, 8]
- Poets: {'لبيد بن ربيعة'}
- **Root Cause:** Same verse used multiple times in batch collection
- **Action:** Keep 1 copy, remove 10 duplicates

**Group 2:** 5 copies
- Text: `أَلا أَيُّها اللَّيْلُ الطَّويلُ أَلا انْجَلِ بِصُبْحٍ وَما الإِصْباحُ مِنْكَ بِأَمْثَلِ...`
- Verse IDs: basit_Classica_0002, basit_Classica_0002, basit_Classica_0002, basit_Classica_0002, basit_Classica_0002
- Meters: [3, 3, 3, 3, 3]
- Poets: {'امرؤ القيس'}
- **Root Cause:** Same verse used multiple times in batch collection
- **Action:** Keep 1 copy, remove 4 duplicates

**Group 3:** 5 copies
- Text: `أَلا لَيْتَ شِعْري هَلْ أَبِيتَنَّ لَيْلَةً بِجَنْبِ الغَضا أُزْجي القِلاصَ النَّواجِيا...`
- Verse IDs: basit_Classica_0003, basit_Classica_0003, basit_Classica_0003, basit_Classica_0003, basit_Classica_0003
- Meters: [3, 3, 3, 3, 3]
- Poets: {'الشماخ'}
- **Root Cause:** Same verse used multiple times in batch collection
- **Action:** Keep 1 copy, remove 4 duplicates

**Group 4:** 5 copies
- Text: `يا صاحِبَيَّ تَقَصَّيا نَظَراً يُقَصِّرُ البَصَرُ...`
- Verse IDs: basit_Classica_0004, basit_Classica_0004, basit_Classica_0004, basit_Classica_0004, basit_Classica_0004
- Meters: [3, 3, 3, 3, 3]
- Poets: {'عدي بن زيد'}
- **Root Cause:** Same verse used multiple times in batch collection
- **Action:** Keep 1 copy, remove 4 duplicates

**Group 5:** 5 copies
- Text: `أَصْبَحَ قَلْبي مِنْ سُلَيْمى كَأَنَّهُ غَزالٌ بِبُرْقَةِ ثَهْمَدَ مَذْعورُ...`
- Verse IDs: basit_Classica_0005, basit_Classica_0005, basit_Classica_0005, basit_Classica_0005, basit_Classica_0005
- Meters: [3, 3, 3, 3, 3]
- Poets: {'أبو ذؤيب الهذلي'}
- **Root Cause:** Same verse used multiple times in batch collection
- **Action:** Keep 1 copy, remove 4 duplicates

**Group 6:** 5 copies
- Text: `يا دارَ مَيَّةَ بِالعَلْياءِ فَالسَّنَدِ أَقْوَتْ وَطالَ عَلَيْها سالِفُ الأَبَدِ...`
- Verse IDs: basit_Classica_0006, basit_Classica_0006, basit_Classica_0006, basit_Classica_0006, basit_Classica_0006
- Meters: [3, 3, 3, 3, 3]
- Poets: {'ذو الرمة'}
- **Root Cause:** Same verse used multiple times in batch collection
- **Action:** Keep 1 copy, remove 4 duplicates

**Group 7:** 5 copies
- Text: `بانَتْ سُعادُ فَقَلْبي اليَوْمَ مَتْبولُ مُتَيَّمٌ إِثْرَها لَمْ يُفْدَ مَكْبولُ...`
- Verse IDs: basit_Classica_0007, basit_Classica_0007, basit_Classica_0007, basit_Classica_0007, basit_Classica_0007
- Meters: [3, 3, 3, 3, 3]
- Poets: {'كعب بن زهير'}
- **Root Cause:** Same verse used multiple times in batch collection
- **Action:** Keep 1 copy, remove 4 duplicates

**Group 8:** 5 copies
- Text: `أَرى الناسَ مَا بَقُوا في خُدْعَةٍ وَما يَنْجو مِنَ الدُّنْيا إِلّا مُتَيَقِّظُ...`
- Verse IDs: basit_Classica_0008, basit_Classica_0008, basit_Classica_0008, basit_Classica_0008, basit_Classica_0008
- Meters: [3, 3, 3, 3, 3]
- Poets: {'زهير بن أبي سلمى'}
- **Root Cause:** Same verse used multiple times in batch collection
- **Action:** Keep 1 copy, remove 4 duplicates

**Group 9:** 5 copies
- Text: `إِذا أَنْتَ لَمْ تَشْرَبْ مِراراً عَلى القَذى ظَمِئْتَ وَأَيُّ النّاسِ تَصْفو مَشارِبُهْ...`
- Verse IDs: basit_Classica_0009, basit_Classica_0009, basit_Classica_0009, basit_Classica_0009, basit_Classica_0009
- Meters: [3, 3, 3, 3, 3]
- Poets: {'طرفة بن العبد'}
- **Root Cause:** Same verse used multiple times in batch collection
- **Action:** Keep 1 copy, remove 4 duplicates

**Group 10:** 5 copies
- Text: `وَإِنّي لَأَمْضي الهَمَّ عِنْدَ احْتِضارِهِ بِعَوْجاءَ مِرْقالٍ تَروحُ وَتَغْتَدي...`
- Verse IDs: basit_Muʿallaq_0010, basit_Muʿallaq_0010, basit_Muʿallaq_0010, basit_Muʿallaq_0010, basit_Muʿallaq_0010
- Meters: [3, 3, 3, 3, 3]
- Poets: {'طرفة بن العبد'}
- **Root Cause:** Same verse used multiple times in batch collection
- **Action:** Keep 1 copy, remove 4 duplicates

*...and 382 more duplicate groups*

### Level B: Fuzzy Duplicates (≥90% similarity)

**Pair 1:** 96.49% similarity
- Verse IDs: basit_Classica_0002, ramal_Classica_0016
- Text 1: `أَلا أَيُّها اللَّيْلُ الطَّويلُ أَلا انْجَلِ بِصُبْحٍ وَما الإِصْباحُ مِنْكَ بِ...`
- Text 2: `أَلا أَيُّها اللَّيْلُ الطَّويلُ أَلا انْجَلِ بِصُبْحٍ وَما الإِصْباحُ فيكَ بِأَ...`
- **Action:** Review manually, likely remove one

**Pair 2:** 96.49% similarity
- Verse IDs: basit_Classica_0002, ramal_Classica_0016
- Text 1: `أَلا أَيُّها اللَّيْلُ الطَّويلُ أَلا انْجَلِ بِصُبْحٍ وَما الإِصْباحُ مِنْكَ بِ...`
- Text 2: `أَلا أَيُّها اللَّيْلُ الطَّويلُ أَلا انْجَلِ بِصُبْحٍ وَما الإِصْباحُ فيكَ بِأَ...`
- **Action:** Review manually, likely remove one

**Pair 3:** 96.49% similarity
- Verse IDs: basit_Classica_0002, ramal_Classica_0016
- Text 1: `أَلا أَيُّها اللَّيْلُ الطَّويلُ أَلا انْجَلِ بِصُبْحٍ وَما الإِصْباحُ مِنْكَ بِ...`
- Text 2: `أَلا أَيُّها اللَّيْلُ الطَّويلُ أَلا انْجَلِ بِصُبْحٍ وَما الإِصْباحُ فيكَ بِأَ...`
- **Action:** Review manually, likely remove one

**Pair 4:** 96.49% similarity
- Verse IDs: basit_Classica_0002, ramal_Classica_0016
- Text 1: `أَلا أَيُّها اللَّيْلُ الطَّويلُ أَلا انْجَلِ بِصُبْحٍ وَما الإِصْباحُ مِنْكَ بِ...`
- Text 2: `أَلا أَيُّها اللَّيْلُ الطَّويلُ أَلا انْجَلِ بِصُبْحٍ وَما الإِصْباحُ فيكَ بِأَ...`
- **Action:** Review manually, likely remove one

**Pair 5:** 96.49% similarity
- Verse IDs: basit_Classica_0002, ramal_Classica_0016
- Text 1: `أَلا أَيُّها اللَّيْلُ الطَّويلُ أَلا انْجَلِ بِصُبْحٍ وَما الإِصْباحُ مِنْكَ بِ...`
- Text 2: `أَلا أَيُّها اللَّيْلُ الطَّويلُ أَلا انْجَلِ بِصُبْحٍ وَما الإِصْباحُ فيكَ بِأَ...`
- **Action:** Review manually, likely remove one

*...and 56 more fuzzy pairs*

### Level C: Prosodic Duplicates

✅ No prosodic duplicates found

---

## Phase 3: Cross-Meter Anomalies

**Anomaly 1:** Verse in 2 meters
- Text: `إِنَّ الثَّمَانِينَ وَبُلِّغْتَهَا قَدْ أَحْوَجَتْ سَمْعِي إِلَى تَرْجُمَانِ...`
- Meters: [3, 8]
- Verse IDs: basit_Classica_0001, sari_Classica_0003
- **Root Cause:** Verse assigned to multiple meters incorrectly
- **Action:** Keep in correct meter only, remove from others

**Anomaly 2:** Verse in 2 meters
- Text: `قَدْ يُدْرِكُ الْمُتَأَنّي بَعْضَ حاجَتِهِ وَقَدْ يَكونُ مَعَ الْمُسْتَعْجِلِ الزَّلَلُ...`
- Meters: [7, 10]
- Verse IDs: munsarih_Classica_0010, khafif_Classica_0012
- **Root Cause:** Verse assigned to multiple meters incorrectly
- **Action:** Keep in correct meter only, remove from others

**Anomaly 3:** Verse in 3 meters
- Text: `أَلَا لَيْتَ شِعْرِي هَلْ أَبِيتَنَّ لَيْلَةً...`
- Meters: [2, 11, 17]
- Verse IDs: kāmil (majzūʾ)_Classica_0011, mutaqarib_Classica_0001, kamil_Classica_0017
- **Root Cause:** Verse assigned to multiple meters incorrectly
- **Action:** Keep in correct meter only, remove from others

**Anomaly 4:** Verse in 2 meters
- Text: `أَلا لَا أَرَى الأَحْدَاثَ حَمْدًا وَلَا ذَمَّا...`
- Meters: [4, 11]
- Verse IDs: mutaqarib_Classica_0008, wafir_Classica_0011
- **Root Cause:** Verse assigned to multiple meters incorrectly
- **Action:** Keep in correct meter only, remove from others

**Anomaly 5:** Verse in 2 meters
- Text: `وَمَا الدَّهْرُ إِلَّا تَارَتَانِ فَمِنْهُمَا...`
- Meters: [4, 11]
- Verse IDs: mutaqarib_Classica_0017, wafir_Classica_0012
- **Root Cause:** Verse assigned to multiple meters incorrectly
- **Action:** Keep in correct meter only, remove from others

---

## Phase 4: Poet Distribution Analysis

- **Meter 3:** Poet `لبيد بن ربيعة` = 10.9% (11/101 verses, exceeds threshold by 5.9%)
- **Meter 3:** Poet `طرفة بن العبد` = 9.9% (10/101 verses, exceeds threshold by 4.9%)
- **Meter 3:** Poet `النابغة الذبياني` = 9.9% (10/101 verses, exceeds threshold by 4.9%)
- **Meter 7:** Poet `حسان بن ثابت` = 5.9% (6/101 verses, exceeds threshold by 0.9%)
- **Meter 7:** Poet `المتنبي` = 24.8% (25/101 verses, exceeds threshold by 19.8%)
- **Meter 7:** Poet `أبو العتاهية` = 14.9% (15/101 verses, exceeds threshold by 9.9%)
- **Meter 7:** Poet `الشافعي` = 9.9% (10/101 verses, exceeds threshold by 4.9%)
- **Meter 5:** Poet `العجاج` = 19.8% (20/101 verses, exceeds threshold by 14.8%)
- **Meter 5:** Poet `حسان بن ثابت` = 9.9% (10/101 verses, exceeds threshold by 4.9%)
- **Meter 5:** Poet `أبو النجم` = 9.9% (10/101 verses, exceeds threshold by 4.9%)
- **Meter 5:** Poet `رؤبة` = 14.9% (15/101 verses, exceeds threshold by 9.9%)
- **Meter 6:** Poet `بشار بن برد` = 9.9% (10/101 verses, exceeds threshold by 4.9%)
- **Meter 6:** Poet `أبو العتاهية` = 14.9% (15/101 verses, exceeds threshold by 9.9%)
- **Meter 6:** Poet `ابن الفارض` = 9.9% (10/101 verses, exceeds threshold by 4.9%)
- **Meter 6:** Poet `قرآن كريم` = 9.9% (10/101 verses, exceeds threshold by 4.9%)

---

## Phase 5: Metadata Validation

✅ No metadata errors found


---

## Recommendations

### Immediate Actions

1. **Remove 1638 exact duplicate verses**
2. **Review and resolve 61 fuzzy duplicate pairs**
3. **Correct 5 cross-meter anomalies**
4. **Address 95 poet imbalance cases**
5. **Fix 0 metadata validation errors**

### Expected Outcomes

- **Clean Dataset Size:** ~394 unique verses
- **Quality Improvement:** Remove 80.6% redundancy
- **Meter Balance:** Ensure ≥95 unique verses per meter
- **Poet Diversity:** <5% concentration per poet per meter

