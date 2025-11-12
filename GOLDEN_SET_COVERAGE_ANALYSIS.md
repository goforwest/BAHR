# Golden Set Coverage Analysis

**Current Status:** 148 verses, 11/20 meters tested

## Coverage Gaps

### 🔴 CRITICAL GAPS - Missing Meters (0 examples)

#### Tier 3 - Rare Meters (5 meters missing)
1. **المنسرح** (al-Munsarih) - 0 verses
2. **المجتث** (al-Mujtathth) - 0 verses
3. **المقتضب** (al-Muqtadab) - 0 verses
4. **المضارع** (al-Mudari') - 0 verses
5. **المتدارك** (al-Mutadarik) - 0 verses

**Impact:** These are rare (<3% each) but we support them. Zero coverage means any bugs would go undetected.

#### Meter Variants (4 variants missing)
1. **الكامل (مجزوء)** - 0 verses (ID: 17)
2. **الهزج (مجزوء)** - 0 verses (ID: 18)
3. **الكامل (3 تفاعيل)** - 0 verses (ID: 19)
4. **السريع (مفعولات)** - 0 verses (ID: 20)

**Impact:** We added these variants to reach 100% accuracy, but have no explicit tests. They're only validated indirectly through variant matching logic.

### 🟡 UNDER-REPRESENTED - Needs More Examples

1. **السريع** - 1 verse (Tier 2, ~5% of poetry)
   - Need: +4-9 verses (target: 5-10 total)
   - Risk: Limited variant coverage

2. **المديد** - 1 verse (Tier 2, ~4% of poetry)
   - Need: +4-9 verses (target: 5-10 total)
   - Risk: Limited zihafat coverage

### ✅ WELL-COVERED (≥10 examples)

- الطويل: 30 verses ✓
- الكامل: 21 verses ✓
- البسيط: 20 verses ✓
- الوافر: 16 verses ✓
- الرمل: 16 verses ✓
- المتقارب: 12 verses ✓
- الرجز: 11 verses ✓
- الخفيف: 11 verses ✓

### 🟢 ADEQUATE (5-9 examples)

- الهزج: 9 verses (acceptable, could add more)

---

## Recommended Target Size

### Minimum Coverage (Robust Testing)

| Tier | Type | Meters | Examples/Meter | Total Verses |
|------|------|--------|----------------|--------------|
| 1 | Common | 9 | 10-15 | 90-135 |
| 2 | Medium | 2 | 5-10 | 10-20 |
| 3 | Rare | 5 | 3-5 | 15-25 |
| - | Variants | 4 | 3-5 | 12-20 |
| **TOTAL** | | **20** | | **127-200** |

### Current vs Target

**Current:** 148 verses, 11 meters
**Minimum Target:** 127-200 verses, 20 meters
**Status:** ✓ Size is good, but coverage is incomplete

---

## Recommendation

### Option 1: Minimal Addition (Robust Coverage)
**Add ~52-102 verses** to reach **200-250 total**

Additions needed:
- المنسرح: +5 verses
- المجتث: +3 verses
- المقتضب: +3 verses
- المضارع: +3 verses
- المتدارك: +5 verses
- السريع: +9 verses (to reach 10)
- المديد: +9 verses (to reach 10)
- مجزوء الكامل: +3 verses
- مجزوء الهزج: +3 verses
- الكامل (3 تفاعيل): +3 verses
- السريع (مفعولات): +4 verses (to reach 5)
- **Subtotal: 52 verses minimum**

**Benefit:** Complete coverage of all 20 supported meters with minimum viable examples.

### Option 2: Comprehensive Coverage
**Add ~100-150 verses** to reach **250-300 total**

Same as Option 1, but with:
- 5-10 examples per rare meter (instead of 3-5)
- 5 examples per variant (instead of 3)
- Additional edge cases per meter

**Benefit:** Deep coverage with multiple zihafat/ilal combinations per meter.

### Option 3: Keep Current Size (148) - NOT RECOMMENDED
**Risk:** 45% of supported meters have zero test coverage. Critical gaps for production deployment.

---

## Edge Cases to Add

Beyond just adding meters, we should ensure coverage of:

### 1. Heavy Zihafat (Multiple Transformations)
- Verses with 3+ zihafat applied
- Currently: mostly single zihaf examples

### 2. Rare 'Ilal (End Variations)
- **بتر** (batr)
- **حذذ** (hadhdhah)
- **كشف** (kashf)
- Currently: mostly حذف, قطع, قصر

### 3. Boundary Cases
- Very short verses (2 تفاعيل)
- Maximum length verses
- Unusual but valid prosody

### 4. Dialectal Variations
- Modern Standard Arabic prosody
- Contemporary variations (within classical rules)

### 5. Historical Variants
- Pre-Islamic vs Umayyad vs Abbasid patterns
- Andalusian variations

---

## Implementation Plan

### Phase 1: Fill Critical Gaps (Priority: HIGH)
**Target: +52 verses minimum**

1. Add 5 rare meters (19 verses)
2. Add 4 variants (13 verses)
3. Expand السريع and المديد (20 verses)
4. **Result: ~200 verses, 20/20 meters covered**

### Phase 2: Edge Cases (Priority: MEDIUM)
**Target: +30-50 verses**

1. Heavy zihafat examples
2. Rare 'ilal examples
3. Boundary cases
4. **Result: ~230-250 verses, comprehensive coverage**

### Phase 3: Dialectal & Historical (Priority: LOW)
**Target: +50 verses (optional)**

1. Modern variations
2. Historical patterns
3. Contemporary poetry variants
4. **Result: ~280-300 verses, exhaustive coverage**

---

## Answer to Your Question

### Is 148 a good size?

**Size:** ✓ Yes, 148 is a good size
**Coverage:** ✗ No, only 11/20 meters tested (55%)

### Will it perform 100% all the time?

**Current State:**
- ✓ 100% on tested meters (11 meters)
- ✗ Unknown on 9 untested meters (45% blind spots)

**To ensure 100% all the time:**
- **Minimum:** Add 52 verses to cover all 20 meters (Option 1)
- **Recommended:** Add 100+ verses for comprehensive coverage (Option 2)
- **Target size:** 200-250 verses minimum

### Bottom Line

**148 is adequate in size but incomplete in coverage.** You need to add examples of the 9 missing meters (especially the 5 rare ones and 4 variants) to confidently claim the engine won't miss edge cases.

**Recommended action:** Proceed with Phase 1 (add 52 verses) to reach ~200 verses with complete 20/20 meter coverage.
