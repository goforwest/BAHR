# Zihafat Implementation Plan - BAHR v2.0

**Target Version:** 2.0  
**Priority:** High  
**Status:** Planning  
**Estimated Effort:** 3-4 weeks  
**Expected Impact:** Generalization 80% → 95%+

---

## Executive Summary

This document outlines the plan to implement **Zihafat (زحافات)** and **'Ilal (علل)** rules in the BAHR prosody engine, transitioning from pattern-matching to rule-based meter detection.

**Goal:** Achieve ≥95% accuracy on both known and unseen classical Arabic poetry by implementing the actual prosodic rules that govern Arabic meters.

---

## Table of Contents

1. [Background](#background)
2. [Current Limitations](#current-limitations)
3. [Proposed Solution](#proposed-solution)
4. [Technical Architecture](#technical-architecture)
5. [Implementation Phases](#implementation-phases)
6. [Data Structures](#data-structures)
7. [Algorithm Design](#algorithm-design)
8. [Testing Strategy](#testing-strategy)
9. [Migration Path](#migration-path)
10. [Success Metrics](#success-metrics)

---

## Background

### What are Zihafat?

**Zihafat (زحافات)** are systematic prosodic variations allowed in Arabic poetry meters. They are **rule-based transformations** of the base tafa'il (prosodic feet).

**Example:**

**Base taf'ila:** `فَعُولُنْ` (fa'ūlun)
- Phonetic: `/o//o`
- Structure: watad + sabab

**Allowed Zihafat:**
1. **قبض (Qabd)** - Remove ن → `فَعُولُ` → `/o//`
2. **كف (Kaff)** - Remove و → `فَعُلُنْ` → `/o/o`
3. **خبن (Khabn)** - Remove second ع → `فَعْلُنْ` → `//o`

**Key Insight:** These aren't random variations—they follow **strict linguistic rules** defined by classical Arabic prosody scholars (الخليل بن أحمد).

### Why Implement Zihafat?

**Current Problem:**
```python
# Pattern matching approach
patterns = [
    "/o//o",     # Base: فعولن
    "/o//",      # With قبض
    "/o/o",      # With كف
    "//o",       # With خبن
    # ... must store all variations
]
```

**With Zihafat Rules:**
```python
# Rule-based approach
base_tafila = Tafila("فعولن", "/o//o")
zihafat_rules = [
    Zahaf("قبض", remove_last_letter),
    Zahaf("كف", remove_vowel_from_watad),
    Zahaf("خبن", remove_second_consonant)
]
# Generate all variations dynamically
```

**Benefits:**
- ✅ Store 1 base pattern instead of 16+ variations
- ✅ Understand WHY a pattern is valid
- ✅ Generate new valid patterns on the fly
- ✅ Explain detection results to users
- ✅ Better generalization to unseen verses

---

## Current Limitations

### Pattern Explosion Problem

**الطويل meter example:**

**Base pattern:**
```
فَعُولُنْ مَفَاعِيلُنْ فَعُولُنْ مَفَاعِيلُنْ
```

**Each taf'ila can have 2-3 variations:**
- Position 1: فَعُولُنْ (3 variations)
- Position 2: مَفَاعِيلُنْ (2 variations)
- Position 3: فَعُولُنْ (3 variations)
- Position 4: مَفَاعِيلُنْ (3 variations - different 'ilal for final position)

**Total possible valid patterns:** 3 × 2 × 3 × 3 = **54 patterns**

**Currently stored in v0.101:** 25 patterns (46% coverage)

**Missing:** 29 valid patterns (54% coverage gap) ← This is why generalization is only 80%!

### Code Maintainability

**Current approach:**
```python
BAHRS_DATA = {
    1: {  # الطويل
        "patterns": [
            "//o/o////o///o/o////o/o///o",  # Which variations? Unknown!
            "//o////o///o//o/o/////",        # What rules applied? Unknown!
            # ... 23 more patterns
            # No documentation of what variation each represents
        ]
    }
}
```

**Problems:**
- ❌ Cannot explain why a pattern belongs to الطويل
- ❌ Cannot validate if a new pattern is theoretically valid
- ❌ Cannot generate missing valid patterns
- ❌ Must manually discover and add each pattern

---

## Proposed Solution

### Three-Tier Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   TIER 1: Base Patterns                  │
│  Store canonical form of each meter (1 pattern/meter)   │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                  TIER 2: Zihafat Rules                   │
│   Define allowed transformations per taf'ila position    │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                TIER 3: Pattern Generation                │
│    Dynamically generate all valid variations on demand   │
└─────────────────────────────────────────────────────────┘
```

### Example: الطويل

**Tier 1 - Base Pattern:**
```python
AL_TAWIL = {
    "name_ar": "الطويل",
    "base_pattern": [
        Tafila("فعولن", "/o//o"),
        Tafila("مفاعيلن", "//o///o"),
        Tafila("فعولن", "/o//o"),
        Tafila("مفاعيلن", "//o///o")
    ]
}
```

**Tier 2 - Zihafat Rules:**
```python
ZIHAFAT_AL_TAWIL = {
    "فعولن": {
        "allowed": [
            Zahaf("قبض", pattern="/o//"),    # Remove last ن
            Zahaf("كف", pattern="/o/o"),     # Remove و
        ],
        "positions": [1, 3]  # Can apply to positions 1 and 3
    },
    "مفاعيلن": {
        "allowed": [
            Zahaf("كف", pattern="//o//o"),   # Remove ي
            Zahaf("قصر", pattern="//o///"),  # Remove last ن (in final position)
        ],
        "positions": [2, 4]
    }
}
```

**Tier 3 - Generated Patterns:**
```python
# Runtime generation
def generate_patterns(base_pattern, zihafat_rules):
    patterns = []
    for combo in combinations(zihafat_rules):
        pattern = apply_zihafat(base_pattern, combo)
        patterns.append(pattern)
    return patterns

# Result: 54 valid patterns generated from rules
```

---

## Technical Architecture

### New Core Modules

```
backend/app/core/
├── prosody/
│   ├── __init__.py
│   ├── tafila.py           # Taf'ila data structures
│   ├── zihafat.py          # Zihafat rules and transformations
│   ├── ilal.py             # 'Ilal rules (end-of-verse variations)
│   ├── meters.py           # Meter definitions with rules
│   ├── pattern_generator.py  # Generate valid patterns
│   ├── validator.py        # Validate pattern against rules
│   └── explainer.py        # Explain why pattern matches meter
└── bahr_detector_v2.py     # New rule-based detector
```

### Data Models

#### 1. Taf'ila Model

```python
@dataclass
class Tafila:
    """Represents a prosodic foot (تفعيلة)."""
    
    name: str              # Arabic name (e.g., "فعولن")
    phonetic: str          # Phonetic pattern (e.g., "/o//o")
    structure: str         # Prosodic structure (e.g., "watad+sabab")
    
    # Phonetic components
    watad: Optional[str]   # Peg (e.g., "/o/")
    sabab: Optional[str]   # Cord (e.g., "/o")
    
    def to_phonetic(self) -> str:
        """Convert to phonetic pattern."""
        return self.phonetic
    
    def __str__(self) -> str:
        return self.name
```

#### 2. Zahaf Model

```python
@dataclass
class Zahaf:
    """Represents a prosodic variation (زحاف)."""
    
    name: str              # Arabic name (e.g., "قبض")
    name_en: str           # English name (e.g., "qabd")
    type: str              # "single" or "double" (مفرد أو مزدوج)
    
    # What it does
    target_tafila: str     # Which taf'ila it applies to
    transformation: Callable  # Function to apply
    result_pattern: str    # Resulting phonetic pattern
    
    # Where it's allowed
    allowed_positions: List[int]  # Which positions in verse
    allowed_meters: List[int]     # Which meters allow it
    
    def apply(self, tafila: Tafila) -> Tafila:
        """Apply this zahaf to a taf'ila."""
        return self.transformation(tafila)
```

#### 3. Meter Model (Enhanced)

```python
@dataclass
class Meter:
    """Represents a classical Arabic meter (بحر)."""
    
    id: int
    name_ar: str
    name_en: str
    
    # Base pattern
    base_tafail: List[Tafila]  # Canonical form
    
    # Allowed variations
    allowed_zihafat: Dict[str, List[Zahaf]]  # Per taf'ila type
    allowed_ilal: Dict[int, List[Ilah]]      # Per position
    
    # Generated cache
    _valid_patterns: Optional[Set[str]] = None
    
    def get_valid_patterns(self) -> Set[str]:
        """Generate all valid phonetic patterns for this meter."""
        if self._valid_patterns is None:
            self._valid_patterns = generate_all_patterns(
                self.base_tafail,
                self.allowed_zihafat,
                self.allowed_ilal
            )
        return self._valid_patterns
    
    def validate_pattern(self, pattern: str) -> ValidationResult:
        """Check if pattern is valid for this meter and explain why."""
        return validate_against_rules(pattern, self)
```

#### 4. Validation Result Model

```python
@dataclass
class ValidationResult:
    """Result of validating a pattern against meter rules."""
    
    is_valid: bool
    confidence: float      # 0.0 to 1.0
    
    # Explanation
    matched_tafail: List[Tafila]  # Which tafa'il matched
    applied_zihafat: List[Zahaf]  # Which zihafat were applied
    applied_ilal: List[Ilah]      # Which 'ilal were applied
    
    # Alternatives
    closest_valid_pattern: Optional[str]  # If invalid
    alternative_meters: List[Tuple[int, float]]  # Other possible meters
    
    def explain(self) -> str:
        """Human-readable explanation."""
        if self.is_valid:
            return f"Valid pattern using: {', '.join(z.name for z in self.applied_zihafat)}"
        else:
            return f"Invalid. Closest valid: {self.closest_valid_pattern}"
```

---

## Implementation Phases

### Phase 1: Data Collection & Research (Week 1)

**Goal:** Compile comprehensive reference data for all 9 meters

**Tasks:**
1. ✅ Research classical prosody texts
   - الخليل بن أحمد الفراهيدي (العروض)
   - ابن عبد ربه (العقد الفريد - كتاب العروض)
   - Modern references (Dr. إبراهيم أنيس, Dr. غازي يموت)

2. ✅ Document all Zihafat
   - Create comprehensive table of all زحافات
   - Map to meters where allowed
   - Define transformation rules

3. ✅ Document all 'Ilal
   - End-of-verse variations
   - Position-specific rules
   - Meter-specific constraints

4. ✅ Create reference dataset
   - Each zahaf with examples
   - Each meter with all valid variations
   - Edge cases and rare combinations

**Deliverables:**
- `docs/research/ZIHAFAT_REFERENCE.md`
- `docs/research/ILAL_REFERENCE.md`
- `docs/research/METER_VARIATIONS.md`

### Phase 2: Core Data Structures (Week 1-2)

**Goal:** Implement data models and basic transformations

**Tasks:**
1. ✅ Implement `Tafila` class
   - Phonetic representation
   - Prosodic structure (watad/sabab)
   - String representations

2. ✅ Implement `Zahaf` class
   - Transformation functions
   - Position validation
   - Meter compatibility

3. ✅ Implement `Ilah` class
   - End-of-verse rules
   - Application logic

4. ✅ Create transformation engine
   - Apply zahaf to taf'ila
   - Validate combinations
   - Generate phonetic patterns

**Deliverables:**
- `backend/app/core/prosody/tafila.py`
- `backend/app/core/prosody/zihafat.py`
- `backend/app/core/prosody/ilal.py`
- Unit tests for each module

### Phase 3: Rule Database (Week 2)

**Goal:** Define all meters with their rules

**Tasks:**
1. ✅ Define base patterns for all 9 meters
   ```python
   AL_TAWIL_BASE = [
       Tafila("فعولن", "/o//o"),
       Tafila("مفاعيلن", "//o///o"),
       Tafila("فعولن", "/o//o"),
       Tafila("مفاعيلن", "//o///o")
   ]
   ```

2. ✅ Map Zihafat to meters
   ```python
   AL_TAWIL_ZIHAFAT = {
       "فعولن": {
           "allowed": [QABD, KAFF],
           "positions": [1, 3]
       },
       # ...
   }
   ```

3. ✅ Map 'Ilal to final positions
   ```python
   AL_TAWIL_ILAL = {
       4: [QASR, HADHF]  # Final position variations
   }
   ```

4. ✅ Create meter registry
   ```python
   METERS = {
       1: Meter(id=1, name_ar="الطويل", ...),
       2: Meter(id=2, name_ar="الكامل", ...),
       # ... all 9 meters
   }
   ```

**Deliverables:**
- `backend/app/core/prosody/meters.py`
- `backend/app/core/prosody/meter_data.json` (serialized)
- Validation tests

### Phase 4: Pattern Generator (Week 2-3)

**Goal:** Generate all valid patterns from rules

**Tasks:**
1. ✅ Implement pattern generation algorithm
   ```python
   def generate_all_patterns(
       base_tafail: List[Tafila],
       zihafat_rules: Dict,
       ilal_rules: Dict
   ) -> Set[str]:
       """Generate all valid phonetic patterns."""
       patterns = set()
       
       # For each combination of zihafat
       for combo in valid_combinations(zihafat_rules):
           # Apply to base pattern
           modified = apply_transformations(base_tafail, combo)
           
           # Apply 'ilal to final position
           for ilah in ilal_rules.get(final_position, []):
               final = apply_ilah(modified, ilah)
               patterns.add(to_phonetic(final))
       
       return patterns
   ```

2. ✅ Optimize generation
   - Cache results
   - Lazy generation
   - Pruning invalid combinations

3. ✅ Validate generated patterns
   - Cross-check with Golden Set
   - Verify all observed patterns are generated
   - Check no invalid patterns generated

**Deliverables:**
- `backend/app/core/prosody/pattern_generator.py`
- Performance benchmarks
- Validation report

### Phase 5: Rule-Based Detector (Week 3)

**Goal:** Implement new detection algorithm

**Tasks:**
1. ✅ Implement `BahrDetectorV2`
   ```python
   class BahrDetectorV2:
       def __init__(self):
           self.meters = load_meters()
           self.pattern_cache = {}
       
       def detect(self, verse: str) -> DetectionResult:
           # Convert to phonetic
           phonetic = text_to_phonetic_pattern(verse)
           
           # Try each meter
           results = []
           for meter in self.meters.values():
               validation = meter.validate_pattern(phonetic)
               results.append((meter, validation))
           
           # Return best match with explanation
           best = max(results, key=lambda x: x[1].confidence)
           return DetectionResult(
               meter=best[0],
               validation=best[1],
               alternatives=[r for r in results if r != best]
           )
   ```

2. ✅ Implement pattern segmentation
   - Break phonetic pattern into tafa'il
   - Match against known tafa'il
   - Identify applied zihafat

3. ✅ Implement confidence scoring
   - Perfect match: 1.0
   - Close match with rare zahaf: 0.9
   - Ambiguous (multiple meters): 0.7
   - No valid match: 0.0

**Deliverables:**
- `backend/app/core/bahr_detector_v2.py`
- Segmentation algorithm
- Confidence calibration

### Phase 6: Testing & Validation (Week 3-4)

**Goal:** Ensure v2 matches or exceeds v1 performance

**Tasks:**
1. ✅ Run on Golden Set v0.101
   - Target: ≥97.5% (match v1)
   - Measure: Accuracy per meter
   - Compare: v1 vs v2 results

2. ✅ Run on Generalization Test
   - Target: ≥95% (improve from 80%)
   - Analyze: Where v2 improves
   - Document: Remaining failures

3. ✅ Create new test sets
   - Generated patterns test (all theoretical variations)
   - Edge cases test (rare zihafat)
   - Ambiguous patterns test

4. ✅ Performance benchmarks
   - Detection speed
   - Memory usage
   - Pattern cache efficiency

**Deliverables:**
- Test results comparison report
- Performance benchmarks
- Failure analysis document

### Phase 7: Migration & Deployment (Week 4)

**Goal:** Smooth transition from v1 to v2

**Tasks:**
1. ✅ Create migration guide
   - API compatibility
   - Breaking changes
   - Migration script

2. ✅ Implement fallback mechanism
   - If v2 fails, try v1
   - Log discrepancies
   - Gradual rollout

3. ✅ Update documentation
   - API docs
   - User guides
   - Technical docs

4. ✅ Deploy v2 as default
   - Keep v1 available as `bahr_detector_v1.py`
   - Monitor production metrics
   - Iterate based on feedback

**Deliverables:**
- Migration script
- Updated documentation
- Deployment checklist

---

## Algorithm Design

### Core Algorithm: Rule-Based Validation

```python
def validate_pattern_against_meter(
    phonetic_pattern: str,
    meter: Meter
) -> ValidationResult:
    """
    Validate if a phonetic pattern belongs to a meter using rules.
    
    Algorithm:
    1. Segment pattern into candidate tafa'il
    2. Match each segment against meter's allowed tafa'il
    3. Identify which zihafat were applied
    4. Validate combination is legal
    5. Return confidence based on match quality
    """
    
    # Step 1: Segment pattern
    segments = segment_into_tafail(phonetic_pattern, meter.base_tafail)
    
    if not segments:
        return ValidationResult(is_valid=False, confidence=0.0)
    
    # Step 2: Match each segment
    matched_tafail = []
    applied_zihafat = []
    
    for i, segment in enumerate(segments):
        # What taf'ila should be here?
        expected_tafila = meter.base_tafail[i]
        
        # Does it match base form?
        if segment == expected_tafila.phonetic:
            matched_tafail.append(expected_tafila)
            continue
        
        # Try matching with zihafat
        match_found = False
        for zahaf in meter.allowed_zihafat.get(expected_tafila.name, []):
            # Is this zahaf allowed at this position?
            if i not in zahaf.allowed_positions:
                continue
            
            # Apply zahaf and check
            modified = zahaf.apply(expected_tafila)
            if segment == modified.phonetic:
                matched_tafail.append(modified)
                applied_zihafat.append(zahaf)
                match_found = True
                break
        
        if not match_found:
            return ValidationResult(is_valid=False, confidence=0.0)
    
    # Step 3: Validate zihafat combination
    if not validate_zihafat_combination(applied_zihafat, meter):
        return ValidationResult(is_valid=False, confidence=0.5)
    
    # Step 4: Calculate confidence
    confidence = calculate_confidence(
        matched_tafail, 
        applied_zihafat,
        meter
    )
    
    return ValidationResult(
        is_valid=True,
        confidence=confidence,
        matched_tafail=matched_tafail,
        applied_zihafat=applied_zihafat
    )


def calculate_confidence(
    matched_tafail: List[Tafila],
    applied_zihafat: List[Zahaf],
    meter: Meter
) -> float:
    """Calculate confidence score based on match quality."""
    
    base_confidence = 1.0
    
    # Perfect match (no zihafat) = 1.0
    if not applied_zihafat:
        return base_confidence
    
    # Deduct for each zahaf (common zihafat deduct less)
    for zahaf in applied_zihafat:
        if zahaf.is_common():
            base_confidence -= 0.02
        else:
            base_confidence -= 0.05
    
    # Deduct for unusual combinations
    if has_unusual_combination(applied_zihafat):
        base_confidence -= 0.1
    
    return max(0.0, min(1.0, base_confidence))
```

### Segmentation Algorithm

```python
def segment_into_tafail(
    phonetic: str,
    expected_tafail: List[Tafila]
) -> Optional[List[str]]:
    """
    Segment phonetic pattern into tafa'il.
    
    Strategy: Dynamic programming to find best segmentation
    that matches expected tafa'il count and approximate positions.
    """
    
    n_tafail = len(expected_tafail)
    pattern_len = len(phonetic)
    
    # Estimate segment boundaries
    avg_len = pattern_len // n_tafail
    
    segments = []
    start = 0
    
    for i, expected in enumerate(expected_tafail):
        # Expected length for this taf'ila
        expected_len = len(expected.phonetic)
        
        # Try different lengths around expected
        best_match = None
        best_score = 0
        
        for length in range(expected_len - 2, expected_len + 3):
            if start + length > pattern_len:
                break
            
            segment = phonetic[start:start + length]
            score = similarity(segment, expected.phonetic)
            
            if score > best_score:
                best_score = score
                best_match = segment
        
        if best_match is None:
            return None
        
        segments.append(best_match)
        start += len(best_match)
    
    # Check we consumed whole pattern
    if start != pattern_len:
        return None
    
    return segments
```

---

## Testing Strategy

### Test Suites

#### 1. Unit Tests

```python
# Test individual zihafat
def test_qabd_on_faulun():
    tafila = Tafila("فعولن", "/o//o")
    zahaf = QABD
    result = zahaf.apply(tafila)
    assert result.phonetic == "/o//"
    assert result.name == "فعول"

# Test pattern generation
def test_generate_al_tawil_patterns():
    patterns = generate_all_patterns(AL_TAWIL)
    assert len(patterns) == 54  # Expected count
    assert "//o/o////o///o/o////o/o///o" in patterns  # Base
```

#### 2. Integration Tests

```python
# Test full detection pipeline
def test_detect_with_zihafat():
    verse = "قفا نبك من ذكرى حبيب ومنزل"
    result = detector_v2.detect(verse)
    
    assert result.meter.name_ar == "الطويل"
    assert result.validation.is_valid
    assert len(result.validation.applied_zihafat) > 0
```

#### 3. Regression Tests

```python
# Ensure v2 performs as well as v1
def test_golden_set_regression():
    results_v1 = run_golden_set_v1()
    results_v2 = run_golden_set_v2()
    
    assert results_v2.accuracy >= results_v1.accuracy
    assert results_v2.accuracy >= 0.975  # 97.5% minimum
```

#### 4. Generalization Tests

```python
# Test on unseen patterns
def test_generated_patterns():
    """Test on theoretically valid patterns not in training."""
    for meter in METERS.values():
        generated = meter.get_valid_patterns()
        
        for pattern in random.sample(generated, 100):
            result = detector_v2.detect_from_phonetic(pattern)
            assert result.meter.id == meter.id
```

### Test Coverage Targets

| Component | Coverage Target |
|-----------|----------------|
| Taf'ila classes | 100% |
| Zahaf transformations | 100% |
| Pattern generation | 95% |
| Segmentation | 90% |
| Detection algorithm | 95% |
| Overall | 95%+ |

---

## Success Metrics

### Primary Metrics

| Metric | v1.0 (Current) | v2.0 (Target) | Status |
|--------|----------------|---------------|--------|
| **Golden Set Accuracy** | 97.5% | ≥97.5% | Must maintain |
| **Generalization Accuracy** | 80% | ≥95% | Primary goal |
| **Detection Speed** | ~10ms | <20ms | Acceptable slowdown |
| **Pattern Coverage** | 46% (25/54) | 100% | Complete coverage |

### Secondary Metrics

| Metric | v1.0 | v2.0 Target |
|--------|------|-------------|
| Confidence calibration | Poor (1.0 on errors) | Good (<0.9 on errors) |
| Explainability | None | Full (list zihafat) |
| Code maintainability | Low | High |
| Pattern database size | 111 patterns | ~9 base + rules |
| Test coverage | 75% | 95% |

### Acceptance Criteria

✅ **Must Have (Required for v2.0 release):**
1. Golden Set accuracy ≥ 97.5%
2. Generalization accuracy ≥ 95%
3. All 9 meters fully defined with rules
4. Detection time < 20ms per verse
5. Comprehensive test suite (95%+ coverage)
6. Full API compatibility with v1

🎯 **Should Have (Nice to have):**
1. Explanation feature (which zihafat applied)
2. Confidence calibration (realistic scores)
3. Pattern generation tool for analysis
4. Migration utility from v1 to v2

💡 **Could Have (Future enhancements):**
1. Interactive zihafat explorer
2. Verse composer (generate valid verses)
3. Comparative analysis tool (v1 vs v2)
4. Performance optimization (pattern cache, etc.)

---

## Migration Path

### Backward Compatibility

**Strategy:** Maintain both v1 and v2, gradual migration

```python
# API stays the same
class BahrDetector:
    def __init__(self, version: str = "v2"):
        if version == "v1":
            self._impl = BahrDetectorV1()
        elif version == "v2":
            self._impl = BahrDetectorV2()
        else:
            raise ValueError(f"Unknown version: {version}")
    
    def analyze_verse(self, text: str) -> BahrInfo:
        return self._impl.analyze_verse(text)
```

### Migration Steps

**Week 1-2:**
- ✅ Release v2 as opt-in (`BahrDetector(version="v2")`)
- ✅ Run A/B testing in production
- ✅ Collect metrics on both versions

**Week 3:**
- ✅ Make v2 default, keep v1 available
- ✅ Monitor error rates and performance
- ✅ Fix any regressions

**Week 4:**
- ✅ Deprecate v1 (still available but warn)
- ✅ Update all documentation
- ✅ Archive v1 code

**Month 2:**
- ✅ Remove v1 entirely
- ✅ Clean up codebase
- ✅ Final optimization

---

## Risk Assessment

### Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Generalization doesn't reach 95% | Medium | High | Keep v1 as fallback, iterate on rules |
| Performance regression (>20ms) | Low | Medium | Optimize pattern cache, lazy generation |
| Implementation bugs in rules | Medium | High | Comprehensive testing, expert review |
| Incomplete zihafat database | Low | High | Research phase, expert consultation |

### Schedule Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Research takes longer | Medium | Low | Start with 3 most common meters, expand |
| Complex edge cases discovered | Medium | Medium | Prioritize common cases, document edge cases |
| Testing reveals issues | High | Medium | Buffer week in schedule, iterative approach |

---

## Resources Required

### Personnel

- **Arabic Prosody Expert:** 10 hours (research validation)
- **Senior Engineer:** 80 hours (core implementation)
- **QA Engineer:** 20 hours (testing)
- **Tech Writer:** 10 hours (documentation)

### Reference Materials

- ✅ العروض (الخليل بن أحمد الفراهيدي)
- ✅ كتاب العقد الفريد - العروض (ابن عبد ربه)
- ✅ موسيقى الشعر (Dr. إبراهيم أنيس)
- ✅ علم العروض والقافية (Dr. عبد العزيز عتيق)
- ✅ Modern digital resources (المكتبة الشاملة)

### Infrastructure

- ✅ Development environment (existing)
- ✅ Testing framework (pytest)
- ✅ CI/CD pipeline (GitHub Actions)
- ✅ Production monitoring (existing)

---

## Expected Outcomes

### Quantitative

- **Generalization:** 80% → 95% (+15 percentage points)
- **Pattern coverage:** 46% → 100% (complete)
- **Code size:** 111 hardcoded patterns → 9 base + rules (~90% reduction)
- **Maintainability:** 10x improvement (rule changes vs. pattern additions)

### Qualitative

- ✅ **Scientific accuracy:** Based on classical prosody rules
- ✅ **Explainability:** Can explain why pattern matches
- ✅ **Extensibility:** Easy to add new meters or rules
- ✅ **Educational value:** Tool teaches prosody concepts
- ✅ **Research potential:** Enables prosody analysis studies

---

## Next Steps

### Immediate (This Week)

1. ✅ Get stakeholder approval on plan
2. ✅ Begin research phase (collect zihafat references)
3. ✅ Set up v2 development branch
4. ✅ Create initial data structures

### Short Term (Month 1)

1. ✅ Complete research and documentation
2. ✅ Implement core data structures
3. ✅ Build rule database for 3 meters (الطويل, الكامل, الوافر)
4. ✅ Test on subset of Golden Set

### Medium Term (Month 2)

1. ✅ Complete all 9 meters
2. ✅ Implement full detection algorithm
3. ✅ Comprehensive testing
4. ✅ Performance optimization

### Long Term (Month 3+)

1. ✅ Production deployment
2. ✅ Monitor and iterate
3. ✅ Deprecate v1
4. ✅ Add educational features

---

## Appendix

### Zihafat Reference (Sample)

| Zahaf Name | Arabic | Type | Transformation | Example |
|------------|--------|------|----------------|---------|
| قبض | Qabd | Single | Remove ن from end | فعولن → فعول |
| كف | Kaff | Single | Remove vowel from watad | فعولن → فعلن |
| خبن | Khabn | Single | Remove 2nd consonant | فعولن → فعلن |
| طي | Tayy | Single | Remove 4th consonant | مفاعيلن → مفاعلن |
| خبل | Khabl | Double | خبن + طي | مفاعيلن → مفاعلن |
| قصر | Qasr | 'Ilah | Remove last letter (final) | مفاعيلن → مفاعيل |
| حذف | Hadhf | 'Ilah | Remove sabab (final) | فعولن → فع |

### Meters Quick Reference

| Meter | Base Pattern | Common Zihafat | Coverage (v1) |
|-------|--------------|----------------|---------------|
| الطويل | فعولن مفاعيلن فعولن مفاعيلن | قبض، كف | 25/54 (46%) |
| الكامل | متفاعلن متفاعلن متفاعلن | إضمار | 16/27 (59%) |
| الوافر | مفاعلتن مفاعلتن فعولن | عصب، عقل | 13/18 (72%) |
| الرمل | فاعلاتن فاعلاتن فاعلاتن | خبن، كف | 13/27 (48%) |
| البسيط | مستفعلن فاعلن مستفعلن فاعلن | خبن، طي | 15/36 (42%) |

---

**Document Status:** Planning  
**Last Updated:** November 11, 2025  
**Version:** 1.0  
**Next Review:** Start of Phase 1

---

**Approval Required From:**
- [ ] Technical Lead
- [ ] Product Manager
- [ ] Arabic Linguistics Expert
- [ ] QA Lead

**Approved for Implementation:** ___________
