# Phase 3: Expert Annotation Materials

This directory contains all materials needed for expert annotation of المتدارك verses.

---

## 📁 Contents

### For Experts (Send these files)

1. **expert_annotation_template.csv**
   - Blank annotation spreadsheet
   - Pre-formatted with 13 verses
   - Experts fill in their annotations

2. **EXPERT_ANNOTATION_INSTRUCTIONS.md** (in `/docs`)
   - Complete instructions for annotators
   - Examples and guidelines
   - FAQ and contact information

### For Internal Use Only (DO NOT share with experts)

3. **verse_id_mapping_CONFIDENTIAL.json**
   - Maps anonymized verse IDs (V001-V013) to actual dataset IDs
   - Shows expected meters and patterns
   - Used for final analysis only

### Analysis Scripts (in `/tools`)

4. **calculate_agreement.py**
   - Calculates Fleiss' Kappa
   - Generates confusion matrices
   - Identifies disputed verses

5. **build_consensus.py**
   - Creates consensus labels from multiple annotations
   - Majority voting and confidence weighting
   - Compares with expected labels

---

## 🚀 Quick Start

### Step 1: Recruit Experts

Use the recruitment email template in `/docs/PHASE_3_EXPERT_ANNOTATION_PROTOCOL.md`

Target: 3-5 Arabic prosody experts with PhD or equivalent experience

### Step 2: Send Materials to Experts

**Email each expert:**
1. `expert_annotation_template.csv`
2. Link to `/docs/EXPERT_ANNOTATION_INSTRUCTIONS.md`
3. Deadline (recommend 1 week)

**Important:** Do NOT send the mapping file or expected labels!

### Step 3: Collect Annotations

**When expert completes annotation:**
- They save as: `annotation_[TheirLastName].csv`
- They email it back to you
- Store in: `phase3_materials/annotations/` (create this directory)

### Step 4: Analyze Agreement

**After receiving 3+ annotations:**

```bash
# Calculate inter-annotator agreement
python tools/calculate_agreement.py \
    --annotations phase3_materials/annotations/*.csv \
    --output phase3_materials/agreement_report.json

# Build consensus labels
python tools/build_consensus.py \
    --annotations phase3_materials/annotations/*.csv \
    --mapping phase3_materials/verse_id_mapping_CONFIDENTIAL.json \
    --output phase3_materials/consensus_labels.json
```

### Step 5: Review Results

**Check Fleiss' Kappa:**
- κ ≥ 0.85: ✅ Excellent - proceed
- κ = 0.60-0.84: ⚠️ Moderate - discuss disputed verses
- κ < 0.60: ❌ Low - re-annotation needed

**If there are disputed verses:**
1. Organize expert discussion session
2. Share annotations for disputed verses only
3. Facilitate consensus building
4. Update consensus labels

### Step 6: Finalize Golden Set

**Once consensus achieved:**
- Update golden set with validated المتدارك verses
- Document consensus notes
- Proceed to Phase 4 (System Integration)

---

## 📊 Expected Timeline

| Stage | Duration | Deliverable |
|-------|----------|-------------|
| Expert recruitment | 3-5 days | 3+ confirmed |
| Blind annotation | 1 week | All annotations |
| Agreement analysis | 1-2 days | κ report |
| Consensus building | 2-3 days | Final labels |
| **Total** | **2-3 weeks** | **Validated corpus** |

---

## ⚠️ Important Notes

### Confidentiality

**NEVER share with experts:**
- `verse_id_mapping_CONFIDENTIAL.json`
- Expected meter labels
- Other experts' annotations (during blind phase)
- Automated detector results

### Quality Control

**Before sending to experts:**
- [ ] Check CSV format is correct
- [ ] Verify all verses are anonymized (V001-V013)
- [ ] Remove any hint of expected answers
- [ ] Test that experts can open/edit the file

**After receiving annotations:**
- [ ] Check all fields completed
- [ ] Verify expert used correct verse IDs
- [ ] Ensure confidence scores are 1-5
- [ ] Check for any obvious errors

---

## 📧 Sample Email to Expert

```
Subject: Expert Annotation Request - المتدارك Meter Validation

Dear Dr. [Name],

Thank you for agreeing to participate in this research!

Attached Materials:
- expert_annotation_template.csv (your annotation spreadsheet)
- Instructions: [link or attach EXPERT_ANNOTATION_INSTRUCTIONS.md]

Task: Annotate 13 Arabic verses (meter + prosodic scansion)
Time Required: 2-3 hours
Deadline: [1 week from today]

Instructions:
1. Open the CSV file in Excel or text editor
2. For each verse (V001-V013), provide:
   - Primary meter identification
   - Confidence level (1-5)
   - Prosodic scansion (تقطيع)
   - Ziḥāfāt and ʿilal identification
   - Quality assessment

3. Save as: annotation_[YourLastName].csv
4. Email back to: [your email]

Please annotate independently without discussing with others.
Your expert judgment is what we need!

Questions? Reply to this email anytime.

Best regards,
[Your name]
```

---

## 🔧 Troubleshooting

### Expert can't open CSV file

**Solution:** Send Excel version or Google Sheets link

**Alternative:** Create online form (Google Forms, Qualtrics)

### Expert confused about task

**Solution:** Provide additional example annotations

**Resource:** See examples in EXPERT_ANNOTATION_INSTRUCTIONS.md

### Low agreement (κ < 0.60)

**Possible causes:**
- Instructions unclear
- Verses genuinely ambiguous
- Experts misunderstood task

**Actions:**
1. Review disputed verses
2. Clarify instructions
3. Consider expert discussion
4. May need re-annotation

### Expert dropped out

**Mitigation:**
- Recruit 5 experts (buffer)
- Have backup list ready
- Set clear expectations upfront

---

## 📈 Success Metrics

- [ ] ≥3 expert annotations collected
- [ ] Fleiss' κ ≥ 0.85
- [ ] ≥90% agreement on meter identification
- [ ] <10% disputed verses
- [ ] 100% consensus labels assigned
- [ ] Expert feedback positive

---

## 📚 References

**Protocol Details:**
- `/docs/PHASE_3_EXPERT_ANNOTATION_PROTOCOL.md`

**Instructions for Experts:**
- `/docs/EXPERT_ANNOTATION_INSTRUCTIONS.md`

**Analysis Scripts:**
- `/tools/calculate_agreement.py`
- `/tools/build_consensus.py`

---

**Status:** Ready for expert recruitment
**Created:** 2025-11-12
**Contact:** [To be filled in]
