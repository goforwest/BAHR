# Prompt for AI Agent: Implement Zihafat Rules Engine (BAHR v2.0)

## Context

I'm working on the BAHR Arabic poetry prosody engine. We've achieved 97.5% accuracy on our Golden Set (118 verses) but only 80% on completely new verses, indicating overfitting to known patterns.

## Current State

- **Version:** 0.101 (MVP - Production)
- **Approach:** Pattern matching with 111 hardcoded phonetic patterns
- **Problem:** Pattern explosion - الطويل has 54 theoretical variations but we only store 25 (46% coverage)
- **Limitation:** No understanding of WHY patterns are valid, just memorization

## Your Task

Implement a **rule-based Zihafat (زحافات) engine** to replace pattern matching with classical Arabic prosody rules.

## Implementation Plan

**Full detailed plan is here:** `/Users/hamoudi/Desktop/Personal/BAHR/docs/planning/ZIHAFAT_IMPLEMENTATION_PLAN.md`

Please read this plan carefully - it contains:
- Complete technical architecture (3-tier system)
- Data structures (Tafila, Zahaf, Meter classes)
- 7 implementation phases with deliverables
- Algorithm pseudocode
- Testing strategy
- Success metrics (≥95% generalization)

## Key Requirements

1. **Maintain backward compatibility** - v1 API must still work
2. **Achieve ≥95% generalization** (currently 80%)
3. **Maintain ≥97.5% Golden Set accuracy** (don't regress)
4. **Add explainability** - tell users which Zihafat were applied
5. **Complete coverage** - generate all theoretical patterns from rules

## Start With

**Phase 1 (Week 1):** Research & Data Collection
- Study classical prosody references in the plan
- Document all Zihafat rules for 9 meters
- Create reference tables

**Phase 2 (Week 1-2):** Core Data Structures
- Implement `Tafila`, `Zahaf`, `Meter` classes
- See detailed specs in plan Section 6 "Data Structures"

## Testing

- Golden Set: `/Users/hamoudi/Desktop/Personal/BAHR/dataset/evaluation/golden_set_v0_101_complete.jsonl`
- Test script: `/Users/hamoudi/Desktop/Personal/BAHR/dataset/scripts/test_prosody_golden_set.py`
- Must pass: 97.5% on Golden Set, 95% on generalization test

## Success Criteria

✅ Golden Set accuracy ≥ 97.5%  
✅ Generalization accuracy ≥ 95%  
✅ All 9 meters with complete rule sets  
✅ Detection time < 20ms per verse  
✅ Full explainability (list which Zihafat applied)

## Questions?

Refer to:
- **Implementation Plan:** `docs/planning/ZIHAFAT_IMPLEMENTATION_PLAN.md` (complete roadmap)
- **Current Limitations:** `docs/technical/PROSODY_ENGINE_LIMITATIONS.md` (what we're fixing)
- **Golden Set Summary:** `archive/dataset/GOLDEN_SET_V0_101_COMPLETION_SUMMARY.md` (current results)

## Let's Begin!

Please confirm you've read the implementation plan, then start with Phase 1: Research & Data Collection. Create the initial data structures and let's build a scientifically accurate prosody engine! 🚀
