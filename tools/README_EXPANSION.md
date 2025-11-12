# Golden Set Expansion Toolkit

Complete toolkit for expanding the BAHR Arabic poetry meter detection golden set from 258 to 400-500 verses.

## 🎯 Current Status

- **Golden Set v1.0**: 258 verses
- **Target**: 400-500 verses (balanced across all meters)
- **Verses Needed**: ~98 minimum to balance all meters
- **Next Verse ID**: golden_259

## 📊 Priority Meters

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

## 🚀 Quick Start

```bash
# 1. Check current status
python tools/expansion_workflow.py status

# 2. See priority meters
python tools/expansion_workflow.py priority

# 3. Add verses interactively
python tools/expansion_helper.py add

# 4. Validate and test
python tools/expansion_workflow.py full-cycle
```

## 🛠️ Available Tools

### 1. Main Workflow Manager
**File**: [expansion_workflow.py](expansion_workflow.py)

Interactive tool for the complete expansion process.

```bash
python tools/expansion_workflow.py
```

**Commands**:
- `status` - Expansion progress
- `priority` - Priority meters list
- `validate` - Validate expansion file
- `precompute` - Compute prosody patterns
- `merge` - Merge golden + expansion
- `evaluate` - Test accuracy
- `full-cycle` - Complete workflow

### 2. Verse Management Helper
**File**: [expansion_helper.py](expansion_helper.py)

Create and manage verses.

```bash
python tools/expansion_helper.py add
```

**Commands**:
- `stats` - Meter statistics
- `next-id` - Next verse ID
- `add` - Add verse interactively
- `validate` - Validate file

### 3. Validation Tool
**File**: [validate_expansion_verse.py](validate_expansion_verse.py)

Validate verse structure and diacritization.

```bash
python tools/validate_expansion_verse.py --file <jsonl_file>
```

## 📖 Documentation

- **[EXPANSION_GUIDE.md](EXPANSION_GUIDE.md)** - Complete guide with workflow, tips, and troubleshooting
- **[example_verses.md](example_verses.md)** - Example verses and templates for each meter
- **[DATASET_EXPANSION_PROMPT.md](../DATASET_EXPANSION_PROMPT.md)** - Original expansion prompt

## 📁 File Structure

```
dataset/evaluation/
├── golden_set_v1_0_with_patterns.jsonl    # Original golden set (258 verses)
├── golden_set_v1_1_expansion.jsonl        # Your additions (new verses)
└── golden_set_v1_1_merged.jsonl           # Merged result (for testing)

tools/
├── expansion_workflow.py                   # Main workflow manager
├── expansion_helper.py                     # Verse management
├── validate_expansion_verse.py             # Validation
├── precompute_golden_patterns.py          # Pattern computation
├── evaluate_detector_v1.py                # Accuracy testing
├── EXPANSION_GUIDE.md                     # Complete guide
├── example_verses.md                      # Examples
└── README_EXPANSION.md                    # This file
```

## 🔄 Workflow

### Phase 1: Setup ✅
- [x] Analysis complete
- [x] Tools created
- [x] Documentation ready

### Phase 2: Manual Expansion (Next!)
1. Research verses from classical sources
2. Add to expansion file with proper diacritization
3. Validate entries
4. Test accuracy

**Recommended starting order**:
1. المجتث (need 9) - Most accessible
2. المنسرح (need 8) - Common meter
3. الهزج (need 6) - Available in folk poetry
4. Then tackle rarer meters

### Phase 3: Semi-Automation (Future)
- After gaining experience, we can build smarter tools
- Potential features:
  - Shamela API integration
  - Automatic diacritization suggestions
  - Meter verification helpers

## 📝 Verse Schema

Each verse must follow this structure:

```json
{
  "verse_id": "golden_259",
  "text": "fully diacritized Arabic text",
  "normalized_text": "text without diacritics",
  "meter": "meter name",
  "poet": "poet name",
  "poem_title": "poem title",
  "source": "classical/modern",
  "prosody_precomputed": {
    "pattern": "to be computed",
    "fitness_score": 0.0,
    "method": "pending",
    "meter_verified": "meter name"
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

## ✅ Quality Standards

**Required**:
- ✅ Full diacritization (70%+ coverage)
- ✅ Verified meter classification
- ✅ Source attribution
- ✅ Valid JSON format (one verse per line)
- ✅ Real poetry (no synthetic verses)

## 🎯 Goals

**Minimum Target**: 15 verses per meter
- Total: ~350 verses
- Balanced distribution
- 100% accuracy maintained

**Optimal Target**: 20 verses per meter
- Total: ~400-500 verses
- Excellent coverage
- Statistical significance

## 📚 Recommended Sources

1. **المكتبة الشاملة (Shamela)**: https://shamela.ws/
   - Comprehensive classical poetry
   - Well-organized by poet and era
   - Usually includes diacritics

2. **الديوان (Aldiwan)**: https://www.aldiwan.net/
   - Modern interface
   - Good search functionality
   - Mixed classical/modern

3. **أدب (Adab.com)**: https://www.adab.com/
   - Large collection
   - Modern poetry included

4. **Classical References**:
   - كتاب العروض للخليل
   - الكافي في العروض والقوافي
   - Academic prosody textbooks

## 🧪 Testing

After adding verses:

```bash
# Quick validation
python tools/expansion_workflow.py validate

# Full test cycle
python tools/expansion_workflow.py full-cycle
```

**Success criteria**:
- ✅ All verses validate
- ✅ Patterns computed successfully
- ✅ 100% accuracy maintained
- ✅ Distribution improved

## 💡 Tips

1. **Start small**: Add 5-10 verses, validate, test
2. **Verify carefully**: Meter classification is critical
3. **Use batches**: Research → Add → Test → Repeat
4. **Document sources**: Attribution is important
5. **Test frequently**: Catch errors early

## 🐛 Troubleshooting

**Validation fails**:
- Check diacritization (70%+ required)
- Verify verse_id format: `golden_XXX`
- Ensure all required fields present

**Pattern computation fails**:
- Verify meter classification is correct
- Check diacritization quality
- Ensure text is valid Arabic

**Accuracy drops**:
- Review misclassified verses
- Check meter labels carefully
- May need to adjust problematic verses

**See**: [EXPANSION_GUIDE.md](EXPANSION_GUIDE.md) for detailed troubleshooting

## 📞 Support

- **Documentation**: Check EXPANSION_GUIDE.md
- **Examples**: See example_verses.md
- **Validation**: Run tools with --help flag

## 🎉 Getting Started

Ready to begin? Here's your first task:

```bash
# 1. Check the current status
python tools/expansion_workflow.py status

# 2. See what needs work
python tools/expansion_workflow.py priority

# 3. Start adding verses for المجتث (easiest)
python tools/expansion_helper.py add
```

Good luck with the expansion! 🚀

---

**Maintainer**: BAHR Project
**Version**: 1.1
**Last Updated**: 2025-11-12
