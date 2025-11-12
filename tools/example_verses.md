# Example Verses for Expansion

Properly formatted example verses for each priority meter. Use these as templates.

## المجتث (6→15, need 9 more)

التفعيلات: مُسْتَفْعِلُنْ فَاعِلاتُنْ

```jsonl
{"verse_id": "golden_259", "text": "مَنْ يَهُنْ يَسْهُلْ الهَوَانُ عَلَيْهِ", "normalized_text": "من يهن يسهل الهوان عليه", "meter": "المجتث", "poet": "المتنبي", "poem_title": "", "source": "classical", "prosody_precomputed": {"pattern": "to be computed", "fitness_score": 0.0, "method": "pending", "meter_verified": "المجتث"}, "validation": {"verified_by": "expansion_phase", "verified_date": "2025-11-12", "automated_check": "PENDING"}, "metadata": {"version": "1.1", "phase": "expansion", "notes": "Classical verse with clear meter"}}
```

## المقتضب (4→15, need 11 more)

التفعيلات: مُفْتَعِلُنْ مُفْتَعِلُنْ

Example verses to source:
- Search Shamela for: "مقتضب"
- Look for short verses (6-8 syllables)
- Verify meter with classical references

Template:
```json
{
  "verse_id": "golden_XXX",
  "text": "[diacritized text]",
  "normalized_text": "[text without diacritics]",
  "meter": "المقتضب",
  "poet": "[poet name]",
  "poem_title": "[poem name]",
  "source": "classical",
  "prosody_precomputed": {
    "pattern": "to be computed",
    "fitness_score": 0.0,
    "method": "pending",
    "meter_verified": "المقتضب"
  },
  "validation": {
    "verified_by": "expansion_phase",
    "verified_date": "2025-11-12",
    "automated_check": "PENDING"
  },
  "metadata": {
    "version": "1.1",
    "phase": "expansion"
  }
}
```

## المضارع (4→15, need 11 more)

التفعيلات: مَفَاعِيلُنْ فَاعِلاتُنْ

Rare meter - may be challenging to source. Consider:
- Modern poetry collections
- Specialized عروض (prosody) books
- Academic dissertations on rare meters

## السريع (مفعولات) (5→15, need 10 more)

التفعيلات variant with مفعولات

Search for السريع verses, then identify which use مفعولات pattern.

## Meter-Specific Tips

### For مجزوء variants:
- Look for shorter verses
- Usually 2-3 تفاعيل instead of full 4-6
- Common in modern poetry

### For rare meters (المقتضب, المضارع):
- Check specialized prosody references
- May need to use modern poetry
- Verify carefully with expert if possible

### For الكامل variants:
- 3 تفاعيل: shorter form
- مجزوء: specific truncation pattern
- Distinguish carefully from regular الكامل

## Sources by Meter

### المجتث:
- المتنبي - various poems
- ابو نواس - lighter poems
- Modern poets - common in contemporary work

### المقتضب:
- Very rare in classical
- Check: ابن الرومي
- Modern experimental poetry

### المضارع:
- Extremely rare
- Check academic collections
- المكتبة الشاملة specialized section

### الهزج (مجزوء):
- Children's poetry
- Songs and lyrics
- Folk poetry collections

## Quality Checklist

Before adding any verse:
- ✅ Found in reputable source
- ✅ Fully diacritized (can add diacritics if source is trusted)
- ✅ Meter verified against عروض rules
- ✅ Poet attribution confirmed
- ✅ Not already in dataset (check duplicates)

## Diacritization Tips

If source lacks full diacritics:
1. Use classical Arabic grammar rules
2. Cross-reference with other poems by same poet
3. Check متن (text) editions with scholarly tashkeel
4. When in doubt, choose natural pronunciation

Essential diacritics:
- Fatha (فَتْحَة): َ
- Kasra (كَسْرَة): ِ
- Damma (ضَمَّة): ُ
- Sukun (سُكُون): ْ
- Shadda (شَدَّة): ّ

## Batch Addition Workflow

For efficient expansion:

1. **Research phase** (1-2 hours):
   - Identify 10-20 candidate verses
   - Verify sources
   - Prepare diacritized versions

2. **Entry phase** (30-60 min):
   - Add all verses to expansion file
   - Use template for consistency

3. **Validation phase** (5-10 min):
   - Run validation
   - Fix any errors

4. **Testing phase** (10-15 min):
   - Run full cycle
   - Check accuracy maintained

5. **Iterate**:
   - Repeat for next batch

## Common Mistakes to Avoid

❌ **Don't:**
- Copy verses without verifying meter
- Use insufficient diacritization
- Mix up meter variants (e.g., الكامل vs الكامل مجزوء)
- Add synthetic/made-up verses
- Use unclear sources

✅ **Do:**
- Verify meter classification carefully
- Add complete diacritics
- Document source clearly
- Use classical poetry when possible
- Test after each batch

## Testing Strategy

After adding verses:

1. **Validation test** - Check format/structure
2. **Pattern test** - Ensure patterns can be computed
3. **Accuracy test** - Verify 100% maintained
4. **Statistical test** - Check distribution improved

Run all:
```bash
python tools/expansion_workflow.py full-cycle
```

## Progress Milestones

Track your progress:

- ⬜ Phase 1: Add 50 verses (priority meters)
- ⬜ Phase 2: Add 50 more (balance distribution)
- ⬜ Milestone: 358 verses (100 added)
- ⬜ Phase 3: Continue to 400 verses
- ⬜ Target: 400-500 verses (balanced)

Update after each session:
```bash
python tools/expansion_workflow.py status
```

## Sample Session

```bash
# Morning session
python tools/expansion_workflow.py status
# Plan: Add 10 verses for المجتث

# Research on Shamela (30 min)
# Found 10 good verses from various poets

# Add verses (30 min)
python tools/expansion_helper.py add
# [repeat 10 times]

# Validate and test (10 min)
python tools/expansion_workflow.py full-cycle

# Check results
python tools/expansion_workflow.py stats

# Result: 268 verses (+10), المجتث now at 16 ✓
```

## Next Steps

1. Start with **المجتث** (easiest, only need 9 more)
2. Then **المنسرح** (8 needed, relatively common)
3. Then **الهزج** (6 needed)
4. Save rare meters (المقتضب, المضارع) for later

Good luck with the expansion! 🎯
