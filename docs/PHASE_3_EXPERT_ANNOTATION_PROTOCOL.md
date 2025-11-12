# Phase 3: Expert Annotation Protocol for المتدارك Corpus

**Date:** 2025-11-12
**Branch:** `claude/arabic-meter-accuracy-roadmap-011CV3HQ6Di2z8bNdcnz4jQR`
**Status:** 🚀 ACTIVE

---

## 🎯 Objective

Validate 13 المتدارك verses through independent expert annotation to ensure:
- Correct meter identification (المتدارك vs other meters)
- Accurate prosodic scansion (تقطيع)
- High inter-annotator agreement (Fleiss' κ ≥ 0.85)
- Consensus on disputed cases

---

## 📋 Phase 3 Overview

### Timeline: 2-3 Weeks

| Stage | Duration | Deliverable |
|-------|----------|-------------|
| **3.1** Expert Recruitment | 3-5 days | 3+ experts confirmed |
| **3.2** Blind Annotation | 1 week | All verses annotated |
| **3.3** Agreement Analysis | 2-3 days | Fleiss' κ calculated |
| **3.4** Consensus Building | 3-5 days | Disputes resolved |
| **3.5** Golden Set Integration | 1-2 days | Final labels confirmed |

### Success Criteria

- [ ] Minimum 3 independent expert annotators
- [ ] All 13 verses annotated by each expert
- [ ] Fleiss' κ ≥ 0.85 (excellent agreement)
- [ ] 100% consensus on final labels
- [ ] Complete documentation of methodology

---

## 👥 Expert Requirements

### Minimum Qualifications

**Required:**
- PhD in Arabic linguistics/literature OR
- Master's degree + 5+ years teaching Arabic prosody OR
- Published research on Arabic meter (العروض)

**Expertise Areas:**
- Classical Arabic prosody (علم العروض)
- Knowledge of all 16 classical meters
- Experience with المتدارك meter specifically
- Familiarity with modern Arabic poetry (preferred)

### Ideal Expert Profile

- University professor/researcher in Arabic studies
- Native Arabic speaker
- Published work on prosody or poetic analysis
- Experience with rare meters (المتدارك, المتقارب)
- Available for 2-3 weeks commitment

### Expert Pool Target

**Minimum:** 3 experts
**Optimal:** 5 experts (allows for robust agreement analysis)
**Maximum:** 7 experts (diminishing returns beyond this)

---

## 📝 Annotation Protocol

### Blind Annotation Process

**Key Principle:** Each expert annotates independently without knowing:
- Other experts' annotations
- Automated detector results
- Expected meter labels from dataset

**Process:**
1. Each expert receives randomized verse list
2. Experts annotate verses in their own order
3. No communication between experts during annotation
4. Annotations collected independently
5. Results analyzed only after all submissions received

### Annotation Task

For each verse, experts must provide:

1. **Meter Identification**
   - Primary meter name (e.g., المتدارك)
   - Confidence level (1-5 scale)
   - Alternative meter if ambiguous

2. **Prosodic Scansion (تقطيع)**
   - Complete tafāʿīl breakdown
   - Example: `فاعلن فعلن فاعلن فاعل`

3. **Ziḥāfāt Identification**
   - Which positions have ziḥāfāt applied
   - Type of ziḥāf (e.g., خبن, طي, etc.)

4. **ʿIlal Identification**
   - Final position ʿillah if present
   - Type (e.g., حذف, قصر, etc.)

5. **Disambiguation Notes**
   - If ambiguous with other meter (e.g., المتقارب)
   - Reasoning for final judgment

6. **Quality Assessment**
   - Is this a valid example of the meter? (Yes/No)
   - Naturalness rating (1-5 for synthetic verses)
   - Any concerns or notes

---

## 📊 Inter-Annotator Agreement

### Metrics to Calculate

**1. Fleiss' Kappa (κ)**
- Primary metric for multi-rater agreement
- Target: κ ≥ 0.85 (excellent agreement)
- Formula: κ = (P_observed - P_expected) / (1 - P_expected)

**2. Percentage Agreement**
- Simple agreement rate across annotators
- Target: ≥90% for meter identification

**3. Confusion Matrix**
- Where do disagreements occur?
- Which meters are commonly confused?

**4. Confidence Correlation**
- Do low-confidence annotations predict disagreement?

### Agreement Interpretation

| Kappa Value | Interpretation | Action |
|-------------|----------------|--------|
| < 0.40 | Poor | Major revision needed |
| 0.40-0.59 | Moderate | Some verses need clarification |
| 0.60-0.79 | Substantial | Minor adjustments needed |
| 0.80-0.90 | Excellent | Proceed with confidence |
| > 0.90 | Nearly perfect | High quality annotations |

---

## 🔧 Dispute Resolution Protocol

### For Disagreements (κ < 0.85 or specific verses)

**Step 1: Identify Disputed Verses**
- Flag any verse with <80% agreement
- Flag verses with confidence <3/5 average

**Step 2: Expert Discussion Session**
- Share all annotations for disputed verses only
- Facilitate structured discussion
- Allow experts to present reasoning

**Step 3: Consensus Building**
- Vote on final label (majority or supermajority)
- Document reasoning in consensus notes
- If no consensus: seek additional expert opinion

**Step 4: Re-annotation (if needed)**
- Experts re-annotate with full context
- Calculate new agreement metrics
- Iterate until κ ≥ 0.85

---

## 📄 Materials Prepared

### For Experts

1. **Annotation Instructions** (`EXPERT_ANNOTATION_INSTRUCTIONS.md`)
   - Detailed task description
   - Example annotations
   - Guidelines for ambiguous cases

2. **Annotation Spreadsheet** (`expert_annotation_template.xlsx`)
   - Pre-formatted for easy data entry
   - One row per verse
   - Dropdown menus for meter names

3. **Verse Collection** (anonymized)
   - Plain text verses without metadata
   - Randomized order
   - No hints about expected meter

4. **Reference Materials**
   - Classical prosody quick reference
   - المتدارك meter characteristics
   - Common ziḥāfāt and ʿilal guide

### For Analysis

5. **Agreement Analysis Script** (`tools/calculate_agreement.py`)
   - Fleiss' κ calculation
   - Confusion matrix generation
   - Visualization of disagreements

6. **Consensus Builder** (`tools/build_consensus.py`)
   - Aggregate expert annotations
   - Identify disputed verses
   - Generate consensus labels

---

## 📧 Expert Recruitment

### Outreach Strategy

**Target Institutions:**
- Arabic Studies departments at major universities
- Islamic Studies centers
- Middle Eastern literature programs
- Poetry research institutes

**Outreach Methods:**
1. Direct email to known prosody researchers
2. Academic network (ResearchGate, Academia.edu)
3. Arabic linguistics mailing lists
4. Conference contacts (MESA, AIDA, etc.)
5. University department chairs for recommendations

### Compensation

**Recommended:**
- Academic acknowledgment in publications
- Co-authorship on resulting papers (if significant contribution)
- Monetary compensation: $100-300 per expert (optional)
- Gift cards or honorarium (if funding available)

**Minimum:**
- Clear acknowledgment in documentation
- Access to final research results
- Citation in any publications

### Sample Recruitment Email

```
Subject: Expert Annotation Request - Arabic Prosody Research (المتدارك Meter)

Dear Dr. [Name],

I am conducting research on automatic detection of Arabic poetic meters
(علم العروض) and would greatly appreciate your expertise in validating
a collection of verses in المتدارك meter.

Task: Annotate 13 Arabic verses (meter identification + prosodic scansion)
Time Required: 2-3 hours
Deadline: [2 weeks from contact]
Compensation: [Academic acknowledgment / $XXX honorarium]

Your expertise in Arabic prosody would be invaluable for ensuring the
quality of this research dataset. All annotation will be conducted
independently (blind protocol) with other experts for reliability analysis.

Would you be interested in participating? I can provide full details
and materials upon your confirmation.

Best regards,
[Your name]
[Affiliation]
```

---

## 🔄 Workflow Timeline

### Week 1: Recruitment & Setup

**Days 1-3:**
- [ ] Send recruitment emails to 10-15 potential experts
- [ ] Follow up with interested candidates
- [ ] Confirm 3-5 experts

**Days 4-5:**
- [ ] Send annotation materials to confirmed experts
- [ ] Answer any clarification questions
- [ ] Set deadline (1 week from receipt)

### Week 2: Annotation Period

**Days 6-12:**
- [ ] Experts conduct independent annotations
- [ ] Monitor for questions/issues
- [ ] Send reminders 2 days before deadline

**Day 13:**
- [ ] Collect all annotations
- [ ] Preliminary agreement analysis
- [ ] Identify disputed verses

### Week 3: Analysis & Consensus

**Days 14-16:**
- [ ] Calculate Fleiss' κ and agreement metrics
- [ ] Generate confusion matrices
- [ ] Identify verses needing discussion

**Days 17-19:**
- [ ] Conduct expert discussion session (if needed)
- [ ] Build consensus on disputed cases
- [ ] Re-calculate agreement if re-annotation needed

**Days 20-21:**
- [ ] Finalize golden set labels
- [ ] Document consensus notes
- [ ] Thank experts and share preliminary results

---

## 📊 Quality Control

### Validation Checks

**During Annotation:**
- [ ] All verses annotated by each expert
- [ ] No missing data fields
- [ ] Tafāʿīl counts match verse length
- [ ] Confidence scores within valid range

**During Analysis:**
- [ ] Agreement metrics calculated correctly
- [ ] Disputed verses properly identified
- [ ] Expert feedback incorporated
- [ ] Final labels justified with evidence

### Red Flags

Watch for:
- ⚠️ Expert annotating too quickly (<5 min/verse)
- ⚠️ All annotations with 5/5 confidence (may not be careful)
- ⚠️ Systematic disagreement from one expert (may need training)
- ⚠️ Low agreement on synthetic verses (may indicate quality issues)

---

## 📈 Success Metrics

### Quantitative

- [ ] Fleiss' κ ≥ 0.85
- [ ] ≥90% agreement on meter identification
- [ ] Average expert confidence ≥4/5
- [ ] <10% of verses require consensus discussion
- [ ] 100% of verses receive final validated labels

### Qualitative

- [ ] Experts report clear, unambiguous instructions
- [ ] No systematic confusion about task
- [ ] Reasonable time to complete (2-4 hours)
- [ ] Experts willing to participate in future work
- [ ] High quality feedback on verse naturalness

---

## 🎯 Deliverables

### End of Phase 3

1. **Annotated Dataset**
   - All 13 verses with expert-validated labels
   - Consensus meter identification
   - Validated prosodic scansions
   - Quality ratings

2. **Agreement Analysis Report**
   - Fleiss' κ and confidence intervals
   - Confusion matrices
   - Disagreement analysis
   - Consensus notes for disputed cases

3. **Expert Feedback Summary**
   - Naturalness ratings for synthetic verses
   - Suggestions for improvement
   - Ambiguity notes for المتدارك/المتقارب cases

4. **Updated Golden Set**
   - Integration of validated المتدارك verses
   - Updated to 20/20 meters with ≥1 test case each
   - Ready for detector evaluation

5. **Methodology Documentation**
   - Complete annotation protocol
   - Expert qualifications and backgrounds
   - Agreement calculation methods
   - Lessons learned for future annotation

---

## 🚨 Risk Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Cannot recruit 3 experts | Medium | High | Start recruitment early; offer compensation; expand search internationally |
| Low agreement (κ < 0.60) | Low | High | Pre-test with 1 expert; provide clear examples; ensure ambiguous verses have notes |
| Expert dropout mid-annotation | Low | Medium | Recruit 5 experts (buffer); have backup list; set clear expectations upfront |
| Disagreement on synthetic verses | Medium | Medium | Expect this; document as limitation; use for improvement; may need revision |
| Timeline delays | Medium | Low | Build in buffer; flexible deadlines; rolling recruitment |

---

## 📚 Reference Materials for Experts

### Provided to Annotators

1. **Prosody Quick Reference**
   - All 16 classical meters overview
   - المتدارك meter details
   - Common ziḥāfāt chart

2. **Annotation Examples**
   - 3 annotated example verses
   - Shows expected format
   - Demonstrates confidence scoring

3. **Ambiguity Guidelines**
   - How to handle المتدارك vs المتقارب
   - When to mark as ambiguous
   - Use of confidence scores

4. **FAQ Document**
   - Common questions anticipated
   - Contact information for questions

---

## 🎉 Phase 3 Ready Checklist

### Prerequisites ✅

- [x] Corpus complete (13 verses)
- [x] Automated validation done (100% pass rate)
- [x] Documentation prepared
- [x] Annotation protocol designed

### Ready to Launch

- [ ] Expert recruitment materials finalized
- [ ] Annotation spreadsheet created
- [ ] Analysis scripts tested
- [ ] Timeline confirmed
- [ ] Recruitment emails sent

---

## 📍 Current Status

**Phase:** 3.0 - Protocol Design ✅ COMPLETE

**Next Step:** 3.1 - Expert Recruitment (Ready to begin)

**Estimated Completion:** 2-3 weeks from expert confirmation

---

**Protocol Prepared By:** Claude (Sonnet 4.5)
**Date:** 2025-11-12
**Status:** Ready for expert recruitment
**Contact:** [To be filled in by user]
