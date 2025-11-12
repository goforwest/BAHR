# المتدارك Corpus Sourcing - Progress Summary

**Last Updated:** 2025-11-12
**Overall Progress:** 7/15 verses (47%)
**Phase 2A Status:** 2/10 additional verses delivered

---

## 📊 Verse Collection Status

| # | Verse ID | Poet/Source | Era | Status | Pattern | Confidence | Next Action |
|---|----------|-------------|-----|--------|---------|------------|-------------|
| **PREVIOUS WORK (5 verses from Shamela)** |
| 1 | mutadarik_shamela_001 | التبريزي (الكافي) | Classical | ✅ VALIDATED | ///o///o///o///o | 0.95 | Ready for golden set |
| 2 | mutadarik_shamela_002 | التبريزي (الكافي) | Classical | ✅ VALIDATED | ///o///o///o///o | 0.95 | Ready for golden set |
| 3 | mutadarik_shamela_003 | التبريزي (الكافي) | Classical | ✅ VALIDATED | ///o///o///o///o | 0.95 | Ready for golden set |
| 4 | mutadarik_shamela_004 | محمود مصطفى (أهدى سبيل) | Classical | ✅ VALIDATED | /o//o/o//o/o//o/o//o | 0.95 | Ready for golden set |
| 5 | mutadarik_shamela_005 | ابن الفارض (Sufi) | Classical | ✅ VALIDATED | ///o///o///o///o | 0.90 | Ready for golden set |
| **CURRENT WORK (10 new verses - 2 delivered, 8 pending)** |
| 6 | mutadarik_synthetic_006 | Synthetic | Synthetic | ✅ CREATED | /o//o///o/o//o/o/ | 1.0 | Needs validation |
| 7 | mutadarik_synthetic_007 | Synthetic | Synthetic | ✅ CREATED | /o//o/o//o///o/o/ | 1.0 | Needs validation |
| 8 | mutadarik_darwish_001 | محمود درويش "جفاف" | Modern | 🔍 IDENTIFIED | TBD | 0.85 | Manual retrieval from aldiwan.net |
| 9 | mutadarik_darwish_002 | محمود درويش "جفاف" | Modern | 🔍 IDENTIFIED | TBD | 0.85 | Manual retrieval from aldiwan.net |
| 10 | mutadarik_darwish_003 | محمود درويش "المزمور..." | Modern | 🔍 IDENTIFIED | TBD | 0.85 | Manual retrieval from aldiwan.net |
| 11 | mutadarik_sayyab_001 | بدر شاكر السياب | Modern | 🔎 SEARCH NEEDED | TBD | 0.80 | Search academic papers + Shamela |
| 12 | mutadarik_sayyab_002 | بدر شاكر السياب | Modern | 🔎 SEARCH NEEDED | TBD | 0.80 | Search academic papers + Shamela |
| 13 | mutadarik_qabbani_001 | نزار قباني | Modern | 🔎 SEARCH NEEDED | TBD | 0.75 | Search poetry collections |
| 14 | mutadarik_bayati_001 | عبد الوهاب البياتي | Modern | 🔎 SEARCH NEEDED | TBD | 0.75 | Search Iraqi modernist studies |
| 15 | mutadarik_abdalsabur_001 | صلاح عبد الصبور | Modern | 🔎 SEARCH NEEDED | TBD | 0.75 | Search Egyptian poetry analysis |

---

## 📈 Progress Breakdown

### By Status

| Status | Count | Percentage |
|--------|-------|------------|
| ✅ Validated (Classical) | 5 | 33.3% |
| ✅ Created (Synthetic) | 2 | 13.3% |
| 🔍 Identified (Manual retrieval needed) | 3 | 20.0% |
| 🔎 Search Required | 5 | 33.3% |
| **TOTAL** | **15** | **100%** |

### By Era

| Era | Target | Completed | Remaining |
|-----|--------|-----------|-----------|
| Classical | 5 | 5 ✅ | 0 |
| Modern | 8 | 0 | 8 |
| Synthetic | 2 | 2 ✅ | 0 |
| **TOTAL** | **15** | **7** | **8** |

### By Confidence Level

| Confidence | Count | Notes |
|------------|-------|-------|
| 1.0 (Perfect) | 2 | Synthetic verses (pattern-guaranteed) |
| 0.95 (Excellent) | 4 | Classical sources with multiple confirmations |
| 0.90 (High) | 1 | Classical Sufi poetry (single strong source) |
| 0.85 (Good) | 3 | Identified modern poems (pending retrieval) |
| 0.75-0.80 (Medium) | 5 | Poets known to use المتدارك (search required) |

---

## 🎯 Priority Action Items

### HIGH PRIORITY (This Week)

1. **Manual Retrieval: Darwish Poems** 📅 ETA: 1-2 hours
   - [ ] Visit https://www.aldiwan.net/poem9121.html (جفاف)
   - [ ] Visit https://www.aldiwan.net/poem2341.html (المزمور...)
   - [ ] Extract 3 complete verses with diacritics
   - [ ] Add to JSONL with full citations
   - **Expected Yield:** 3 verses → Progress: 10/15 (67%)

2. **Validate Synthetic Verses** 📅 ETA: 2-3 hours
   - [ ] Run `/tools/mutadarik_validator.py` on verses 6-7
   - [ ] Native speaker review for naturalness
   - [ ] Adjust if validation fails
   - **Expected Yield:** 2 validated verses

---

### MEDIUM PRIORITY (Next 1-2 Weeks)

3. **Academic Paper Search: السياب** 📅 ETA: 2-3 hours
   - [ ] Google Scholar: "المتدارك في شعر السياب"
   - [ ] Download 2-3 prosodic analysis papers
   - [ ] Extract quoted المتدارك verses
   - [ ] Verify against original dīwān
   - **Expected Yield:** 2 verses → Progress: 12/15 (80%)

4. **Shamela Search: Modern Poets** 📅 ETA: 1-2 hours
   - [ ] Search for السياب dīwān on Shamela
   - [ ] Check prosody textbooks mentioning modern poets
   - [ ] Extract المتدارك examples
   - **Expected Yield:** 1-2 verses → Progress: 13-14/15 (87-93%)

---

### LOW PRIORITY (As Needed)

5. **Fill Remaining Gaps** 📅 ETA: 2-3 hours
   - [ ] Search قباني, البياتي, عبد الصبور collections
   - [ ] OR create 1-2 additional synthetic verses
   - [ ] OR return to Shamela for more classical examples
   - **Expected Yield:** 1-2 verses → Progress: 15/15 (100%) ✅

---

## 📋 Quality Checkpoints

### Before Marking Verse as "Complete"

- [ ] Full Arabic text with diacritics (or clearly marked if none)
- [ ] Complete JSONL metadata (all fields filled)
- [ ] At least 1 authoritative source citation
- [ ] Prosodic scansion (تقطيع) documented
- [ ] Automated validation passed (or documented failure reason)
- [ ] Confidence score justified
- [ ] Disambiguation notes (vs المتقارب)

### Before Progressing to Phase 3

- [ ] Minimum 15 total verses collected
- [ ] At least 12 verses validated by automated tool
- [ ] All verses have complete metadata
- [ ] Source diversity (not all from single poet/source)
- [ ] Pattern diversity (multiple ziḥāfāt combinations)
- [ ] Ready for expert blind annotation

---

## 🔄 Alternative Completion Paths

### Path A: Balanced Approach (Recommended)
- 5 Classical (Shamela) ✅
- 5-6 Modern (Darwish + السياب + others)
- 3-4 Synthetic (current 2 + additional edge cases)
- **Total:** 13-15 verses
- **Timeline:** 1-2 weeks

### Path B: Modern Poetry Focus
- 5 Classical (Shamela) ✅
- 8 Modern (Darwish + السياب + قباني + others)
- 2 Synthetic ✅
- **Total:** 15 verses
- **Timeline:** 2-3 weeks (requires more academic research)

### Path C: Synthetic Supplement
- 5 Classical (Shamela) ✅
- 4-5 Modern (Darwish + السياب)
- 5-6 Synthetic (expand edge case coverage)
- **Total:** 14-16 verses
- **Timeline:** 1 week (faster, but needs expert validation)

---

## 📊 Risk & Mitigation Matrix

| Risk | Impact | Mitigation Plan | Status |
|------|--------|----------------|--------|
| Cannot retrieve Darwish poems | Medium | Use academic papers with quoted verses | Ready |
| Synthetic verses fail validation | Low | Iterate with prosodist feedback | Prepared |
| Insufficient modern verses | Medium | Expand classical or synthetic collections | Backup ready |
| Copyright issues | Low | Fair use + minimal excerpts only | Documented |
| Expert validation unavailable | High | Use multi-source verification + automated tools | Multiple methods |

---

## 🎯 Success Criteria

### Minimum Viable Dataset (MVP)
- [ ] 15 total verses
- [ ] 10+ automated validation passes
- [ ] 3+ different sources (classical texts, modern poets, synthetic)
- [ ] Complete metadata for all verses
- ➡️ **Ready for Phase 3 expert annotation**

### Optimal Dataset
- [ ] 15+ total verses
- [ ] 13+ automated validation passes
- [ ] 5+ different sources
- [ ] Inter-annotator agreement κ ≥ 0.85
- [ ] Pattern diversity score ≥ 80%
- ➡️ **Ready for golden set integration**

---

## 📅 Timeline Estimate

| Milestone | Estimated Date | Dependencies |
|-----------|----------------|--------------|
| Retrieve Darwish verses | 2025-11-13 | Manual browser access |
| Validate synthetic verses | 2025-11-14 | Validator tool + native speaker |
| Find السياب verses | 2025-11-18 | Academic paper access |
| Complete 15 verses | 2025-11-20 | All above tasks |
| Expert validation | 2025-11-25 | Expert availability |
| Phase 3 ready | 2025-11-30 | All quality checks passed |

---

## 📈 Metrics Dashboard

**Current Metrics:**
- **Total Verses:** 7/15 (47%)
- **Validation Rate:** 5/7 (71%) - 5 classical validated, 2 synthetic pending
- **Source Diversity:** 3 sources (classical texts, synthetic, modern identified)
- **Pattern Diversity:** ~40% (need more ziḥāfāt variations)
- **Automated Validation:** 5/7 passed (71%)

**Target Metrics:**
- **Total Verses:** 15/15 (100%) ✅
- **Validation Rate:** 13/15 (87%) ✅
- **Source Diversity:** 5+ sources ✅
- **Pattern Diversity:** 80%+ ✅
- **Automated Validation:** 12/15 (80%) ✅

---

## 🚀 Immediate Next Steps

**Do Today:**
1. ✅ Review synthetic verses 6-7 (done - created)
2. 🔄 Manually retrieve Darwish poems (requires browser)

**Do This Week:**
3. Validate synthetic verses with tool
4. Search academic papers for السياب
5. Fill 2-3 more gaps

**Do Next Week:**
6. Complete final 1-2 verses
7. Prepare for expert annotation
8. Begin Phase 3 planning

---

**Summary Status:** 🟡 IN PROGRESS
**Blockers:** Manual retrieval required for modern poems
**Est. Completion:** 1-2 weeks with focused effort
**Next Critical Action:** Retrieve Darwish poems from aldiwan.net (1-2 hours)
