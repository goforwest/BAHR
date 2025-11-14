# Dataset Expansion Prompt

Copy-paste this prompt to expand the BAHR Golden Set:

---

**Task:** Expand the BAHR Golden Set v1.0 Arabic poetry meter detection dataset.

**Current Status:**
- 258 verses across 20 meter variants
- 100% detection accuracy achieved
- Dataset location: `dataset/evaluation/golden_set_v1_0_with_patterns.jsonl`

**Expansion Goals:**
1. Add 10-20 verses per meter (balanced distribution)
2. Focus on underrepresented meters (currently <10 verses each):
   - المجتث (6 verses) → target 15-20
   - المقتضب (4 verses) → target 15-20
   - المضارع (4 verses) → target 15-20
   - السريع (مفعولات) (5 verses) → target 15
   - الكامل variants (5 each) → target 10-15 each
   - الهزج (مجزوء) (5 verses) → target 15

3. Add new meter variants:
   - المتقارب (مجزوء)
   - الرمل (مجزوء)
   - البسيط (مجزوء)
   - Other مجزوء and مشطور forms

**Requirements:**
- ✅ Fully diacritized (تشكيل كامل)
- ✅ Classical or modern Arabic poetry (avoid synthetic unless necessary)
- ✅ Source attribution (poet name, poem title, source)
- ✅ Diverse poets and eras
- ✅ Follow existing JSONL schema exactly

**JSONL Schema (match exactly):**
```json
{
  "verse_id": "golden_259",
  "text": "fully diacritized Arabic text",
  "normalized_text": "same text without diacritics",
  "meter": "المجتث",
  "poet": "poet name",
  "poem_title": "poem title",
  "source": "classical/modern",
  "prosody_precomputed": {
    "pattern": "to be computed",
    "fitness_score": 0.0,
    "method": "pending",
    "meter_verified": "المجتث"
  },
  "validation": {
    "verified_by": "expansion_phase",
    "verified_date": "YYYY-MM-DD",
    "automated_check": "PENDING"
  },
  "metadata": {
    "version": "1.1",
    "phase": "expansion",
    "notes": "optional notes"
  }
}
```

**Process:**
1. Source verses from المكتبة الشاملة (Shamela) or classical poetry databases
2. Verify meter classification manually or with expert
3. Add full diacritization if missing
4. Format as JSONL (one verse per line)
5. Start verse_id from `golden_259` onwards
6. Leave `prosody_precomputed.pattern` as "to be computed" (will be auto-generated)
7. Save to: `dataset/evaluation/golden_set_v1_1_expansion.jsonl`

**After Expansion:**
1. Run pattern pre-computation: `python tools/precompute_golden_patterns.py`
2. Evaluate accuracy: `python tools/evaluate_detector_v1.py`
3. Fix any errors detected
4. Merge into main golden set when 100% accuracy maintained

**Target Size:**
- Current: 258 verses
- Target: 400-500 verses (balanced across all meters)

**Priority Meters (add these first):**
1. المجتث (+14 verses)
2. المقتضب (+16 verses)
3. المضارع (+16 verses)
4. All مجزوء variants (+10 each)

**Quality Standards:**
- Maintain 100% accuracy on expanded set
- No synthetic verses unless absolutely necessary
- Prefer famous poets and well-known poems
- Ensure proper attribution and licensing

**Deliverable:**
- New JSONL file: `dataset/evaluation/golden_set_v1_1_expansion.jsonl`
- Evaluation report showing accuracy on expanded set
- Documentation of sources used
