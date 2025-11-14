# Golden Set Expansion Guide

Quick reference for expanding the BAHR Golden Set.

## Quick Start

```bash
# 1. Check current status
python tools/expansion_workflow.py status

# 2. See which meters need verses
python tools/expansion_workflow.py priority

# 3. Add verses interactively
python tools/expansion_helper.py add

# 4. Validate your additions
python tools/expansion_workflow.py validate

# 5. Run full cycle (validate→precompute→merge→evaluate)
python tools/expansion_workflow.py full-cycle
```

## Available Tools

### 1. `expansion_workflow.py` - Main Workflow Manager
Interactive workflow for the entire expansion process.

**Commands:**
- `status` - Show expansion progress
- `priority` - List meters needing verses
- `stats` - Detailed statistics
- `add` - Add new verse
- `validate` - Validate expansion file
- `precompute` - Precompute prosody patterns
- `merge` - Merge golden set + expansion
- `evaluate` - Test accuracy
- `full-cycle` - Complete workflow

**Usage:**
```bash
# Interactive mode
python tools/expansion_workflow.py

# Direct command
python tools/expansion_workflow.py status
```

### 2. `expansion_helper.py` - Verse Management
Helper for creating and managing verses.

**Commands:**
- `stats` - Meter distribution
- `next-id` - Get next verse ID
- `template` - Create verse template
- `add` - Add verse to expansion
- `validate` - Validate expansion file

**Usage:**
```bash
python tools/expansion_helper.py stats
python tools/expansion_helper.py add
```

### 3. `validate_expansion_verse.py` - Validation
Validate verse structure and diacritization.

**Usage:**
```bash
# Validate entire file
python tools/validate_expansion_verse.py --file dataset/evaluation/golden_set_v1_1_expansion.jsonl

# Validate single verse (JSON string)
python tools/validate_expansion_verse.py '{"verse_id": "golden_259", ...}'
```

## Priority Meters (Need Most Verses)

Based on current dataset (258 verses), these meters need the most additions:

| Current | Need | Meter |
|---------|------|-------|
| 4 | 11 | المقتضب |
| 4 | 11 | المضارع |
| 5 | 10 | السريع (مفعولات) |
| 5 | 10 | الكامل (3 تفاعيل) |
| 5 | 10 | الكامل (مجزوء) |
| 5 | 10 | الهزج (مجزوء) |
| 6 | 9 | المجتث |
| 7 | 8 | المنسرح |
| 9 | 6 | الهزج |

**Total needed to reach minimum (15): 98 verses**

## Verse Schema

Required structure for each verse:

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

## Quality Standards

✅ **Required:**
- Full diacritization (تشكيل كامل) - at least 70% coverage
- Verified meter classification
- Source attribution (poet, poem)
- Valid JSON format (one verse per line)

⚠️ **Avoid:**
- Synthetic verses (use real poetry)
- Incomplete diacritization
- Unknown/unverified meters
- Duplicate verses

## Workflow Steps

### Phase 1: Planning
1. Run `python tools/expansion_workflow.py status`
2. Identify priority meters
3. Research sources for those meters

### Phase 2: Adding Verses
1. Find diacritized verse from reputable source
2. Verify meter classification
3. Run `python tools/expansion_helper.py add`
4. Enter verse details interactively

### Phase 3: Validation
1. Run `python tools/expansion_workflow.py validate`
2. Fix any errors reported
3. Re-validate until clean

### Phase 4: Pattern Computation
1. Run `python tools/expansion_workflow.py precompute`
2. Patterns will be computed and added to verses

### Phase 5: Testing
1. Run `python tools/expansion_workflow.py merge`
2. Run `python tools/expansion_workflow.py evaluate`
3. Should maintain 100% accuracy

### Quick Cycle (All at once)
```bash
python tools/expansion_workflow.py full-cycle
```

## File Locations

- Golden Set v1.0: `dataset/evaluation/golden_set_v1_0_with_patterns.jsonl`
- Expansion file: `dataset/evaluation/golden_set_v1_1_expansion.jsonl`
- Merged output: `dataset/evaluation/golden_set_v1_1_merged.jsonl`

## Tips

1. **Start with priority meters** - Focus on المقتضب, المضارع, المجتث first
2. **Use classical sources** - المكتبة الشاملة (Shamela) is excellent
3. **Verify diacritization** - Use multiple sources if unsure
4. **Validate frequently** - Catch errors early
5. **Small batches** - Add 5-10 verses, then validate
6. **Test incrementally** - Don't wait until you have 100 verses

## Sources for Verses

### Classical Poetry Databases
- المكتبة الشاملة (Shamela): https://shamela.ws/
- الديوان (Aldiwan): https://www.aldiwan.net/
- أدب (Adab.com): https://www.adab.com/

### Books
- كتاب العروض للخليل
- الكافي في العروض والقوافي
- ميزان الذهب في صناعة شعر العرب

## Troubleshooting

**Q: Validation fails with "Not fully diacritized"**
- A: Add more diacritics (fatha, damma, kasra, sukun)
- Need at least 70% coverage

**Q: "Invalid verse_id format"**
- A: Use format `golden_XXX` with 3 digits
- Get next ID with: `python tools/expansion_helper.py next-id`

**Q: "Duplicate verse_id"**
- A: Check existing verses and use next available ID

**Q: Pattern precomputation fails**
- A: Ensure verse meter is correctly classified
- Check that text is properly diacritized

**Q: Accuracy drops below 100%**
- A: Review misclassified verses
- May need to adjust meter label or fix diacritization

## Example: Adding a Verse Manually

```bash
# 1. Get next ID
python tools/expansion_helper.py next-id
# Output: golden_259

# 2. Create verse JSON
cat >> dataset/evaluation/golden_set_v1_1_expansion.jsonl << 'EOF'
{"verse_id": "golden_259", "text": "مَنْ يَهُنْ يَسْهُلْ الهَوَانُ عَلَيْهِ", "normalized_text": "من يهن يسهل الهوان عليه", "meter": "المجتث", "poet": "المتنبي", "poem_title": "", "source": "classical", "prosody_precomputed": {"pattern": "to be computed", "fitness_score": 0.0, "method": "pending", "meter_verified": "المجتث"}, "validation": {"verified_by": "expansion_phase", "verified_date": "2025-11-12", "automated_check": "PENDING"}, "metadata": {"version": "1.1", "phase": "expansion"}}
EOF

# 3. Validate
python tools/expansion_workflow.py validate

# 4. Process
python tools/expansion_workflow.py full-cycle
```

## Interactive Example

```bash
$ python tools/expansion_helper.py add

Create Verse Template
==================================================
Next verse ID: golden_259

Diacritized text: مَنْ يَهُنْ يَسْهُلْ الهَوَانُ عَلَيْهِ
Meter: المجتث
Poet (optional): المتنبي
Poem title (optional):
Source (default: classical):
Notes (optional): High-quality verse from classical era

==================================================
Generated verse:
==================================================
{
  "verse_id": "golden_259",
  "text": "مَنْ يَهُنْ يَسْهُلْ الهَوَانُ عَلَيْهِ",
  ...
}

Save to expansion file? (y/n): y

✓ Saved to dataset/evaluation/golden_set_v1_1_expansion.jsonl
```

## Maintaining 100% Accuracy

The goal is to maintain 100% detection accuracy. If accuracy drops:

1. **Check misclassified verses** - Run evaluation to see errors
2. **Verify meter labels** - Ensure correct meter assigned
3. **Check diacritization** - May need adjustment
4. **Review edge cases** - Some meters are similar (e.g., variants)
5. **Consult references** - Use classical prosody books

## Progress Tracking

Check progress anytime:
```bash
python tools/expansion_workflow.py status
```

See detailed statistics:
```bash
python tools/expansion_helper.py stats
```

## Next Steps After Expansion

Once you've added verses and maintained 100% accuracy:

1. Update golden set version number
2. Replace v1.0 with merged v1.1
3. Update documentation
4. Commit changes with clear message
5. Run full evaluation suite

## Questions?

Check existing tools:
- `tools/precompute_golden_patterns.py` - Pattern computation
- `tools/evaluate_detector_v1.py` - Accuracy testing
- `tools/phase5_statistical_analysis.py` - Statistical analysis
