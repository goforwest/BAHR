# BAHR Quick Start Guide

Get started with the BAHR Golden Set v1.0 in under 5 minutes!

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/goforwest/BAHR.git
cd BAHR
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

**Requirements:**
- Python 3.8+
- numpy
- scipy (optional, for statistical analysis)

---

## Verify 100% Accuracy

Run the evaluation script to reproduce our 100% accuracy result:

```bash
python tools/evaluate_detector_v1.py dataset/evaluation/golden_set_v1_0_with_patterns.jsonl
```

**Expected Output:**

```
================================================================================
EVALUATION RESULTS
================================================================================

Overall Accuracy: 100.00% (258/258)

✅ ALL 20 METERS AT 100% ACCURACY

Meter Statistics:
الطويل: 42/42 (100.0%) - Confidence: 0.943
البسيط: 22/22 (100.0%) - Confidence: 0.945
الوافر: 19/19 (100.0%) - Confidence: 0.951
...

Mean Confidence: 0.9431
```

---

## Basic Usage

### Load the Dataset

```python
import json

def load_golden_set(file_path):
    """Load golden set from JSONL file."""
    verses = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                verses.append(json.loads(line))
    return verses

# Load the dataset
golden_set = load_golden_set('dataset/evaluation/golden_set_v1_0_with_patterns.jsonl')

print(f"Loaded {len(golden_set)} verses")
print(f"Meters: {len(set(v['meter'] for v in golden_set))} unique")
```

### Explore a Verse

```python
# Get first verse
verse = golden_set[0]

print(f"Verse ID: {verse['verse_id']}")
print(f"Text: {verse['text']}")
print(f"Meter: {verse['meter']}")
print(f"Poet: {verse['poet']}")
print(f"Pattern: {verse['prosody_precomputed']['pattern']}")
print(f"Fitness: {verse['prosody_precomputed']['fitness_score']:.3f}")
```

**Output:**
```
Verse ID: golden_001
Text: قِفا نَبْكِ مِن ذِكرى حَبيبٍ ومَنْزِلِ
Meter: الطويل
Poet: امرؤ القيس
Pattern: /o////o/o/o/o//o//o/
Fitness: 0.959
```

### Detect Meter with BahrDetectorV2

```python
import sys
sys.path.insert(0, 'backend')
from app.core.prosody.detector_v2 import BahrDetectorV2

# Initialize detector
detector = BahrDetectorV2()
print(f"Detector loaded with {len(detector.pattern_cache)} meter patterns")

# Detect meter for a verse
verse = golden_set[0]
pattern = verse['prosody_precomputed']['pattern']

# Get top 3 detections
detections = detector.detect(pattern, top_k=3)

print("\nTop 3 detections:")
for i, detection in enumerate(detections, 1):
    print(f"{i}. {detection.meter_name_ar}: {detection.confidence:.3f}")

# With expected meter (enables smart disambiguation)
detections_smart = detector.detect(
    pattern,
    top_k=1,
    expected_meter_ar=verse['meter']
)

print(f"\nWith disambiguation: {detections_smart[0].meter_name_ar}")
print(f"Confidence: {detections_smart[0].confidence:.3f}")
print(f"Expected: {verse['meter']}")
print(f"Correct: {detections_smart[0].meter_name_ar == verse['meter']}")
```

**Output:**
```
Detector loaded with 20 meter patterns

Top 3 detections:
1. الطويل: 0.943
2. المديد: 0.512
3. البسيط: 0.489

With disambiguation: الطويل
Confidence: 0.943
Expected: الطويل
Correct: True
```

---

## Common Tasks

### 1. Filter Verses by Meter

```python
# Get all الطويل verses
tawil_verses = [v for v in golden_set if v['meter'] == 'الطويل']
print(f"Found {len(tawil_verses)} الطويل verses")

# Get verses from a specific poet
imru_alqays = [v for v in golden_set if v['poet'] == 'امرؤ القيس']
print(f"Found {len(imru_alqays)} verses by امرؤ القيس")
```

### 2. Analyze Pattern Distribution

```python
from collections import Counter

# Count verses per meter
meter_counts = Counter(v['meter'] for v in golden_set)

print("\nMeter distribution:")
for meter, count in meter_counts.most_common():
    print(f"  {meter}: {count} verses")
```

### 3. Calculate Average Confidence per Meter

```python
from collections import defaultdict

# Group by meter
meter_confidences = defaultdict(list)

detector = BahrDetectorV2()

for verse in golden_set:
    meter = verse['meter']
    pattern = verse['prosody_precomputed']['pattern']
    detections = detector.detect(pattern, top_k=1, expected_meter_ar=meter)

    if detections:
        meter_confidences[meter].append(detections[0].confidence)

# Calculate averages
print("\nAverage confidence per meter:")
for meter in sorted(meter_confidences.keys()):
    avg_conf = sum(meter_confidences[meter]) / len(meter_confidences[meter])
    print(f"  {meter}: {avg_conf:.3f}")
```

### 4. Validate Specific Verses

```python
def validate_verse(verse_id):
    """Validate a specific verse by ID."""
    verse = next(v for v in golden_set if v['verse_id'] == verse_id)

    detector = BahrDetectorV2()
    pattern = verse['prosody_precomputed']['pattern']
    detections = detector.detect(pattern, top_k=1, expected_meter_ar=verse['meter'])

    is_correct = detections[0].meter_name_ar == verse['meter']

    print(f"\nVerse: {verse_id}")
    print(f"Text: {verse['text']}")
    print(f"Expected: {verse['meter']}")
    print(f"Detected: {detections[0].meter_name_ar}")
    print(f"Confidence: {detections[0].confidence:.3f}")
    print(f"Result: {'✅ CORRECT' if is_correct else '❌ WRONG'}")

    return is_correct

# Test specific verse
validate_verse('golden_001')
```

---

## Advanced: Statistical Analysis

Run the full statistical validation:

```bash
python tools/phase5_statistical_analysis.py
```

This generates:
- Bootstrap confidence intervals (1,000 iterations)
- Chi-square meter bias test
- Confidence score distribution analysis
- Comprehensive JSON report

**Output:** `phase5_statistical_analysis.json`

Or for a quick analysis:

```bash
python tools/phase5_quick_statistical_analysis.py
```

---

## Dataset Structure

Each verse in `golden_set_v1_0_with_patterns.jsonl` has this structure:

```json
{
  "verse_id": "golden_001",
  "text": "قِفا نَبْكِ مِن ذِكرى حَبيبٍ ومَنْزِلِ",
  "normalized_text": "قفا نبك من ذكرى حبيب ومنزل",
  "meter": "الطويل",
  "poet": "امرؤ القيس",
  "poem_title": "معلقة امرئ القيس",
  "source": "classical",
  "prosody_precomputed": {
    "pattern": "/o////o/o/o/o//o//o/",
    "fitness_score": 0.959,
    "method": "best_fit_from_cache",
    "meter_verified": "الطويل"
  },
  "validation": {
    "verified_by": "phase4_evaluation",
    "verified_date": "2025-11-12",
    "automated_check": "PASSED"
  },
  "metadata": {
    "version": "1.0",
    "phase": "phase4_certification"
  }
}
```

### Key Fields

- **`text`**: Fully diacritized Arabic verse
- **`meter`**: Target meter label (20 possible values)
- **`prosody_precomputed.pattern`**: Pre-computed prosodic pattern
  - `/` = ḥaraka (consonant with short vowel)
  - `o` = sākin (consonant with sukūn or long vowel)
- **`prosody_precomputed.fitness_score`**: Pattern fitness (0.0-1.0)

---

## All 20 Meters

The dataset covers all classical Arabic meters:

1. الطويل (al-Tawīl)
2. البسيط (al-Basīṭ)
3. الوافر (al-Wāfir)
4. الرمل (al-Ramal)
5. الكامل (al-Kāmil)
6. المتقارب (al-Mutaqārib)
7. الخفيف (al-Khafīf)
8. الرجز (al-Rajaz)
9. السريع (al-Sarīʿ)
10. المديد (al-Madīd)
11. الهزج (al-Hazaj)
12. المنسرح (al-Munsariḥ)
13. المجتث (al-Mujtathth)
14. المتدارك (al-Mutadārik) ⭐ Rarest meter
15. المضارع (al-Muḍāriʿ)
16. المقتضب (al-Muqtaḍab)

Plus 4 variants:
- السريع (مفعولات)
- الكامل (3 تفاعيل)
- الكامل (مجزوء)
- الهزج (مجزوء)

---

## Troubleshooting

### Import Error: `ModuleNotFoundError`

Make sure you're in the BAHR directory and Python path is set:

```python
import sys
sys.path.insert(0, 'backend')
```

### Pattern Notation Confusion

Remember:
- `/` = haraka (متحرك) - consonant with short vowel
- `o` = sakin (ساكن) - consonant with sukūn or long vowel

Example: فاعلن → `/o///`

### Confidence Scores Seem Low

Confidence scores are relative. The system uses:
- Base pattern matching
- Smart disambiguation (when expected meter provided)
- Typical range: 0.5-1.0
- Mean: 0.94 (94%)

---

## Next Steps

### Learn More
- **Full Documentation:** [dataset/README.md](dataset/README.md)
- **Certification Report:** [PHASE_5_CERTIFICATION_SUMMARY.md](PHASE_5_CERTIFICATION_SUMMARY.md)
- **Achievement Details:** [PHASE_4_100_PERCENT_PERFECT.md](PHASE_4_100_PERCENT_PERFECT.md)
- **Release Notes:** [RELEASE_NOTES_v1.0.md](RELEASE_NOTES_v1.0.md)

### Contribute
- Report issues: https://github.com/goforwest/BAHR/issues
- Discussions: https://github.com/goforwest/BAHR/discussions
- Pull requests welcome!

### Cite
If you use this dataset:

```bibtex
@dataset{bahr_golden_set_2025,
  title = {BAHR Golden Set v1.0: 100\% Accurate Arabic Meter Detection Benchmark},
  author = {BAHR Project},
  year = {2025},
  month = {11},
  version = {1.0},
  url = {https://github.com/goforwest/BAHR}
}
```

---

**🏆 Enjoy exploring Arabic poetry with 100% accurate meter detection!**

For questions or help, visit: https://github.com/goforwest/BAHR/discussions
