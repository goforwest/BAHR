# Test Fixtures - Arabic Poetry Verses

This directory contains test data for accuracy testing of the BAHR prosody engine.

## Files

### `test_verses.json`
Gold standard dataset for prosody engine validation containing 52+ verses of classical Arabic poetry.

**Structure:**
```json
{
  "verses": [
    {
      "text": "Arabic verse with diacritics",
      "poet": "Poet name",
      "bahr": "البحر name in Arabic",
      "expected_tafail": "Expected tafa'il pattern",
      "notes": "Any notes"
    },
    ...
  ]
}
```

**Coverage:**
- **Total verses:** 52
- **الطويل (at-Tawil):** 13 verses
- **الكامل (al-Kamil):** 13 verses
- **الوافر (al-Wafir):** 13 verses
- **الرمل (ar-Ramal):** 13 verses

**Sources:**
1. **Golden Dataset**: 10 verses from `dataset/evaluation/golden_set_v0_20_complete.jsonl`
   - Manually verified and annotated
   - High confidence (avg 0.92)
   
2. **Classical Poetry**: 42 supplementary verses from:
   - Pre-Islamic poetry (Mu'allaqat)
   - Early Islamic poetry
   - Abbasid era classics
   - Andalusian poetry
   - Modern classical revival

**Poets Included:**
- امرؤ القيس (Imru' al-Qais)
- المتنبي (al-Mutanabbi)
- أبو العتاهية (Abu al-'Atahiya)
- بشار بن برد (Bashar ibn Burd)
- أحمد شوقي (Ahmad Shawqi)
- أبو نواس (Abu Nuwas)
- الخنساء (al-Khansa)
- And many more classical poets

## Generation

The dataset was generated using `convert_golden_to_test.py`:

```bash
python3 convert_golden_to_test.py
```

This script:
1. Loads verses from the golden dataset (`golden_set_v0_20_complete.jsonl`)
2. Filters for the 4 target bahrs (الطويل، الكامل، الوافر، الرمل)
3. Adds supplementary verses from classical Arabic poetry
4. Ensures minimum 10 verses per bahr
5. Outputs to `test_verses.json`

## Usage in Tests

```python
import json
from pathlib import Path

# Load test verses
fixtures_path = Path(__file__).parent / "fixtures" / "test_verses.json"
with open(fixtures_path, 'r', encoding='utf-8') as f:
    data = json.load(f)
    test_verses = data['verses']

# Use in tests
for verse in test_verses:
    result = detector.analyze_verse(verse['text'])
    assert result.name_ar == verse['bahr']
```

## Quality Assurance

All verses in this dataset:
- ✅ Are from public domain classical Arabic poetry
- ✅ Are prosodically sound (no meter errors)
- ✅ Include proper attribution to poets
- ✅ Have expected tafa'il patterns for validation
- ✅ Cover all 4 implemented bahrs evenly

## Notes

- Verses with diacritics (tashkeel) are preferred for accurate testing
- Some verses may have minor variations in expected patterns due to poetic license (zihafat)
- The dataset focuses on classical meters (بحور الشعر العربي)
- All poetry is in public domain

## Future Improvements

- [ ] Add more verses for edge cases (mixed meters, rare variations)
- [ ] Include verses with intentional meter violations for error detection
- [ ] Add verses from modern poetry
- [ ] Expand to cover all 16 classical Arabic meters
- [ ] Add difficulty levels (easy/medium/hard)

---

**Last Updated:** 2025-11-10
**Version:** 1.0
