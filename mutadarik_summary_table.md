# المتدارك Verses Summary Table

## Current Status: 2/10 verses delivered

| Verse ID | Poet | Era | Source | Confidence | Status | Notes |
|----------|------|-----|--------|------------|--------|-------|
| mutadarik_synthetic_001 | Synthetic | Synthetic | Generated - Mixed ziḥāfāt | 0.85 | ✅ DELIVERED | Needs expert validation. Pattern: فاعلن فعلن فاعلن فع |
| mutadarik_synthetic_002 | Synthetic | Synthetic | Generated - Rare variant | 0.85 | ✅ DELIVERED | Needs expert validation. Pattern: فاعلن فاعلن فعلن فاع |
| mutadarik_darwish_001 | محمود درويش | Modern | "جفاف" - aldiwan.net/poem9121.html | 0.95 | ⏳ IDENTIFIED | Requires manual retrieval |
| mutadarik_darwish_002 | محمود درويش | Modern | "المزمور الحادي والخمسون" - aldiwan.net/poem2341.html | 0.95 | ⏳ IDENTIFIED | Requires manual retrieval |
| mutadarik_sayyab_001 | بدر شاكر السياب | Modern | Collections: "أنشودة المطر", "المعبد الغريق" | 0.85 | 🔍 SEARCH NEEDED | Known experimenter with المتدارك/الخبب |
| mutadarik_qabbani_001 | نزار قباني | Modern | Review of 35 poetry collections needed | 0.80 | 🔍 SEARCH NEEDED | Moved to free verse, likely used المتدارك |
| mutadarik_bayati_001 | عبد الوهاب البياتي | Modern | Identified in khabab poets list | 0.85 | 🔍 SEARCH NEEDED | Access specific poems needed |
| mutadarik_abdalsabur_001 | صلاح عبد الصبور | Modern | General identification | 0.80 | 🔍 SEARCH NEEDED | Review collections for examples |
| mutadarik_modern_003 | TBD | Modern | Academic sources / dissertations | TBD | 🔍 SEARCH NEEDED | Additional modern examples |
| mutadarik_modern_004 | TBD | Modern | Academic sources / dissertations | TBD | 🔍 SEARCH NEEDED | Additional modern examples |

---

## Legend
- ✅ DELIVERED: Verse text created/extracted and in JSONL file
- ⏳ IDENTIFIED: Poem/poet confirmed, specific URL provided, awaiting manual retrieval
- 🔍 SEARCH NEEDED: Poet known to use meter, specific poem needs identification
- TBD: To be determined through further research

---

## By Status

### Delivered (2)
1. Synthetic verse 1 - Mixed ziḥāfāt pattern
2. Synthetic verse 2 - Rare variant pattern

### Identified & Ready for Manual Retrieval (2)
3. Mahmoud Darwish - "جفاف"
4. Mahmoud Darwish - "المزمور الحادي والخمسون بعد المئة"

### Requires Additional Search (6)
5. Badr Shakir al-Sayyab - From collections
6. Nizar Qabbani - From 35 collections
7. Abd al-Wahhab al-Bayati - From identified sources
8. Salah Abd al-Sabur - From collections
9-10. Additional modern poets - From academic sources

---

## Recommended Priority Order for Completion

### High Priority (Can complete quickly - 1-2 hours)
1. **Manually retrieve Darwish poems** (⏳ → ✅)
   - Visit URLs with browser
   - Copy 2-3 complete verses from each poem
   - Add diacritics if needed
   - Create JSONL entries
   - **Expected yield:** 4-6 verses total from 2 poems

### Medium Priority (Moderate effort - 2-3 hours)
2. **Search Shamela for classical/modern examples**
   - Direct website access: https://shamela.ws/
   - Search books on العروض
   - May find modern examples in prosody textbooks
   - **Expected yield:** 2-3 verses

3. **Review academic papers**
   - Google Scholar searches
   - Focus on dissertations about modern prosody
   - Look for quoted examples
   - **Expected yield:** 2-3 verses

### Lower Priority (Time-intensive - 3-4 hours)
4. **Search poet collections manually**
   - Access al-Sayyab, Qabbani, al-Bayati collections
   - Read/scan for المتدارك patterns
   - Verify with prosodic analysis
   - **Expected yield:** 2-4 verses

---

## Quality Metrics

### Current Dataset Quality
- **Diversity:** 2 edge case patterns (mixed ziḥāfāt, rare variant)
- **Verification:** Synthetic only (needs expert review)
- **Era coverage:** Synthetic only (needs modern examples)
- **Poet coverage:** N/A yet

### Target Dataset Quality (When Complete)
- **Diversity:** Mix of canonical, khabn, ḥadhf, qaṣr variations
- **Verification:** 2+ sources for modern, expert review for synthetic
- **Era coverage:** 0 classical (already have 5), 8 modern, 2 synthetic
- **Poet coverage:** 3-5 different modern poets

---

## Risk Assessment

### Risks to Completion
1. **Access barriers** (HIGH)
   - Many sites block automated access
   - Requires manual effort
   - Mitigation: Use browser, allow more time

2. **Copyright restrictions** (MEDIUM)
   - Cannot reproduce full poems
   - Must select individual verses
   - Mitigation: Fair use for research, cite properly

3. **Verification difficulty** (MEDIUM)
   - المتدارك rare and sometimes disputed
   - May find conflicting analyses
   - Mitigation: Require 2+ sources, prefer academic

4. **Insufficient examples** (LOW-MEDIUM)
   - May not find 8 quality modern verses
   - Meter genuinely rare
   - Mitigation: Consider expanding poet list, or creating more synthetic

---

## Alternative Approaches (If Current Path Stalls)

### Option A: Expand Synthetic Verse Creation
- Create 6-8 synthetic verses instead of 2
- Cover more ziḥāfāt variations systematically
- Pros: Complete control, systematic coverage
- Cons: Not authentic poetry, needs extensive validation

### Option B: Include Classical Verses
- Use additional classical verses beyond the 5 already collected
- Search Shamela more extensively
- Pros: Better documented, easier to verify
- Cons: Doesn't help with modern poetry patterns

### Option C: Expand Poet List
- Include poets beyond the 5 listed
- Search for contemporary poets (21st century)
- Consider Andalusian muwashshaḥāt (historical but uses المتدارك more)
- Pros: Broader net, may find less-known examples
- Cons: More research time, verification complexity

### Option D: Collaborate with Domain Expert
- Partner with Arabic prosody scholar
- Get access to their databases/analyses
- Have them create/validate synthetic verses
- Pros: Higher quality, faster validation
- Cons: Requires finding and coordinating with expert

---

## Success Criteria Checklist

### Minimum Acceptable (Target: 10 verses)
- [ ] 2 synthetic verses delivered ✅
- [ ] 8 modern verses with proper citations (0/8 ⏳)
- [ ] All verses in JSONL format (2/10 ✅)
- [ ] Complete metadata for each verse (2/10 ✅)
- [ ] Prosodic scansion for each verse (2/10 ✅)

### Excellent Result (Stretch Goal)
- [ ] 10+ modern verses (allows selection of best)
- [ ] 3+ different poets represented
- [ ] Diverse ziḥāfāt patterns across verses
- [ ] 2+ sources for each modern verse
- [ ] Expert validation of synthetic verses
- [ ] Academic papers cited for verification

---

## Estimated Completion Effort

### If continuing current approach:
- **Minimum:** 5-7 hours additional work
- **Realistic:** 8-10 hours total
- **With challenges:** 12-15 hours

### If using Alternative Option A (More synthetic):
- **Time:** 2-3 hours (create verses + validation)
- **Trade-off:** Less authentic, more validation needed

### Recommended Approach:
1. Spend 2 hours on manual Darwish retrieval (high confidence)
2. Spend 2-3 hours on academic paper searches
3. Assess progress: if at 6-7 verses, push for 8
4. If at 4-5 verses, create 2-3 more synthetic (easier than finding rare modern examples)
5. Total time: 5-8 hours to minimum acceptable completion

---

**Last Updated:** 2025-11-12
**Next Review:** After manual retrieval of Darwish poems
