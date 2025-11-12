# BAHR Golden Set v1.2 Expansion Plan

**Target:** Expand from 356 verses (v1.1) to 400-500 verses (v1.2)
**Focus Areas:** Rare meters, variant forms, metadata enhancement

## Expansion Goals

### 1. Verse Count Targets (Total: ~450 verses)

**Current Coverage (v1.1):**
- Total: 356 verses
- Target for v1.2: 450 verses (+94 verses)

**Distribution Strategy:**

#### Priority 1: Rare Meters (Need Better Detection)
- **المقتضب**: 15 → 25 verses (+10) ⭐
  - Current accuracy: 73.3%
  - Add clearer, more canonical examples
  - Focus on well-known poets (المتنبي, أبو نواس, etc.)

- **المضارع**: 15 → 25 verses (+10)
  - Already at 100% accuracy
  - Add more examples to maintain robustness

#### Priority 2: Variant Forms (New Meters)

**مشطور Forms (Split/Half forms):**
- الطويل (مشطور): 0 → 10 verses (+10) 🆕
- الكامل (مشطور): 0 → 10 verses (+10) 🆕
- البسيط (مشطور): 0 → 10 verses (+10) 🆕
- الوافر (مشطور): 0 → 10 verses (+10) 🆕

**Additional مجزوء Forms:**
- المتقارب (مجزوء): 0 → 10 verses (+10) 🆕
- الرمل (مجزوء): 0 → 10 verses (+10) 🆕
- البسيط (مجزوء): 0 → 10 verses (+10) 🆕
- الوافر (مجزوء): 0 → 5 verses (+5) 🆕

#### Priority 3: Balance Existing Meters (15 → 20 each)
- All current meters: +5 verses each = +100 verses
- This provides better robustness for edge cases

### 2. Metadata Enhancement

**Add Historical Context:**
```json
"metadata": {
  "version": "1.2",
  "phase": "expansion_v1.2",
  "era": "Abbasid" | "Umayyad" | "Pre-Islamic" | "Modern" | "Contemporary",
  "era_dates": "750-1258 CE",
  "region": "Iraq" | "Hijaz" | "Andalus" | "Egypt" | "Levant" | "Modern",
  "poet_birth_year": "915 CE",
  "poet_death_year": "965 CE",
  "poem_genre": "wisdom" | "praise" | "satire" | "love" | "elegy" | "religious",
  "notes": "..."
}
```

**Era Classification:**
1. **Pre-Islamic (الجاهلية)**: Before 622 CE
   - Poets: امرؤ القيس, عنترة, طرفة, الأعشى
2. **Early Islamic (الإسلام المبكر)**: 622-661 CE
   - Poets: حسان بن ثابت, كعب بن زهير
3. **Umayyad (الأموي)**: 661-750 CE
   - Poets: جرير, الفرزدق, ذو الرمة
4. **Abbasid (العباسي)**: 750-1258 CE
   - Poets: أبو نواس, المتنبي, أبو العتاهية, ابن الرومي
5. **Andalusian (الأندلسي)**: 711-1492 CE
   - Poets: ابن زيدون, ابن حزم, لسان الدين بن الخطيب
6. **Ottoman/Mamluk**: 1250-1918 CE
7. **Modern Revival (النهضة)**: 1850-1950 CE
   - Poets: أحمد شوقي, حافظ إبراهيم, البارودي
8. **Contemporary (المعاصر)**: 1950-present
   - Poets: محمود درويش, نزار قباني, أدونيس

### 3. Quality Standards

**For المقتضب Improvement:**
- ✅ Only use verses from famous, reliable sources
- ✅ Ensure full, accurate diacritization
- ✅ Verify meter with multiple prosody references
- ✅ Test each verse with detector before adding
- ✅ Target 90%+ accuracy on المقتضب

**For Variant Forms:**
- ✅ Clearly distinguish مشطور vs مجزوء
- ✅ Document the variant pattern structure
- ✅ Use canonical examples from classical prosody texts

### 4. Implementation Steps

**Phase 1: Create v1.2 Expansion File (50 verses)**
- 10 المقتضب (high quality)
- 10 المضارع
- 10 مشطور forms (mix)
- 10 مجزوء forms (new variants)
- 10 balance existing meters

**Phase 2: Validate and Test**
- Run precomputation
- Run evaluation (target: maintain 95%+ overall)
- Fix any detection issues

**Phase 3: Create v1.3 Expansion File (44 verses)**
- Fill remaining gaps
- Balance all meters to 20+ verses
- Add final مشطور/مجزوء examples

**Phase 4: Merge and Document**
- Create golden_set_v1_2_merged.jsonl (450 verses)
- Update all metadata with era/region
- Generate comprehensive documentation

### 5. Success Metrics

- ✅ Total verses: 400-500 (target: 450)
- ✅ Overall accuracy: 95%+ maintained
- ✅ المقتضب accuracy: 85%+ (up from 73.3%)
- ✅ All meters: 20+ verses each
- ✅ New variant forms: 4 مشطور + 4 مجزوء
- ✅ 100% metadata completeness (era, region)

### 6. Timeline

- **Phase 1**: Create 50-verse expansion (~2 hours)
- **Phase 2**: Validate and test (~1 hour)
- **Phase 3**: Create 44-verse expansion (~2 hours)
- **Phase 4**: Merge and document (~1 hour)

**Total Estimated Time**: ~6 hours of focused work

---

**Next Action**: Start Phase 1 with creating the first 50-verse expansion focused on rare meters and new variant forms.
