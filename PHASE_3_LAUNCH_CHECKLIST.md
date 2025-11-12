# 🚀 Phase 3 Launch Checklist

**Status:** Ready to begin expert recruitment
**Created:** 2025-11-12
**Estimated Duration:** 2-3 weeks

---

## ✅ Pre-Launch (Complete)

- [x] Phase 2 corpus collection complete (13/15 verses = 87%)
- [x] All verses validated (100% pass rate)
- [x] Expert annotation protocol designed
- [x] Annotation instructions written
- [x] Annotation template created (CSV)
- [x] Analysis scripts developed (agreement + consensus)
- [x] Materials tested and ready
- [x] Documentation complete
- [x] All files committed to repository

---

## 📋 Week 1: Expert Recruitment (Days 1-5)

### Day 1: Prepare Outreach

- [ ] **Fill in contact information**
  - Update email address in EXPERT_ANNOTATION_INSTRUCTIONS.md
  - Update contact in PHASE_3_EXPERT_ANNOTATION_PROTOCOL.md
  - Update recruitment email template

- [ ] **Create expert target list** (10-15 potential experts)
  - Search Arabic Studies departments
  - Check prosody researchers on ResearchGate
  - Review recent publications on علم العروض
  - Identify conference contacts (MESA, AIDA, etc.)

- [ ] **Prepare compensation details**
  - Decide: Academic acknowledgment only OR monetary
  - If monetary: Set amount ($100-300 suggested)
  - Prepare gift cards/payment method if needed

### Day 2-3: Send Recruitment Emails

- [ ] **Send initial outreach** (batch 1: 5 experts)
  - Use template from PHASE_3_EXPERT_ANNOTATION_PROTOCOL.md
  - Personalize each email
  - Attach or link to task description

- [ ] **Track responses**
  - Create spreadsheet: Expert name, affiliation, response date, status
  - Set reminders for follow-ups (3 days)

### Day 4-5: Confirm Experts

- [ ] **Follow up with non-responders**
  - Send batch 2 if needed (5 more experts)
  - Continue until 3-5 experts confirmed

- [ ] **Collect expert information**
  - Full name
  - Affiliation
  - Email
  - Qualifications (for documentation)

- [ ] **Set deadline** (1 week from materials receipt)

**Goal:** 3-5 confirmed expert annotators by end of Week 1

---

## 📧 Week 1-2: Send Materials (Day 5-6)

### Day 5: Prepare Personalized Packages

For each confirmed expert:

- [ ] **Create customized email**
  - Thank them for participating
  - Attach expert_annotation_template.csv
  - Attach or link to EXPERT_ANNOTATION_INSTRUCTIONS.md
  - Specify deadline (7 days)
  - Provide contact for questions

- [ ] **Test materials**
  - Verify CSV opens correctly
  - Check all links work
  - Ensure instructions are clear

### Day 6: Send Materials

- [ ] **Email all experts** (same day to ensure fair timeline)

- [ ] **Send confirmation reminders**
  - "Please confirm receipt" request
  - Estimate 2-3 hours for completion

- [ ] **Create tracking spreadsheet**
  - Expert name | Sent date | Confirmed receipt | Submitted date | Status

**Goal:** All materials sent to 3-5 experts

---

## ⏳ Week 2: Annotation Period (Days 7-13)

### Days 7-11: Monitoring

- [ ] **Check for questions daily**
  - Respond within 24 hours
  - Document common questions for FAQ

- [ ] **Track progress**
  - Mark when experts confirm receipt
  - Note any issues or delays

### Day 11: Reminder Email

- [ ] **Send reminder** (2 days before deadline)
  - Friendly reminder of deadline
  - Offer to answer any questions
  - Offer extension if needed (reasonable requests)

### Day 13: Collection

- [ ] **Collect annotations**
  - Download and save: `phase3_materials/annotations/annotation_[Name].csv`
  - Send thank you confirmation
  - Ask for brief feedback (optional)

- [ ] **Quality check each annotation**
  - All 13 verses completed?
  - All fields filled?
  - Confidence scores valid (1-5)?
  - File format correct?

- [ ] **Follow up on missing submissions**
  - Email any non-responders
  - Offer brief extension if needed
  - Activate backup experts if necessary

**Goal:** Receive 3-5 complete annotations

---

## 📊 Week 3: Analysis & Consensus (Days 14-21)

### Days 14-15: Agreement Analysis

- [ ] **Run agreement analysis**
  ```bash
  python tools/calculate_agreement.py \
      --annotations phase3_materials/annotations/*.csv \
      --output phase3_materials/agreement_report.json
  ```

- [ ] **Review results**
  - Check Fleiss' κ score
  - Identify disputed verses (<80% agreement)
  - Review confusion matrix
  - Analyze confidence patterns

- [ ] **Interpret results**
  - κ ≥ 0.85: ✅ Excellent - proceed to consensus
  - κ = 0.60-0.84: ⚠️ Good - discuss disputed verses
  - κ < 0.60: ❌ Low - plan re-annotation

### Days 16-17: Consensus Building

- [ ] **Run consensus script**
  ```bash
  python tools/build_consensus.py \
      --annotations phase3_materials/annotations/*.csv \
      --mapping phase3_materials/verse_id_mapping_CONFIDENTIAL.json \
      --output phase3_materials/consensus_labels.json
  ```

- [ ] **Review consensus labels**
  - Check agreement types (unanimous, majority, disputed)
  - Compare with expected labels
  - Calculate match percentage

- [ ] **Document findings**
  - Which verses have strong agreement?
  - Which need discussion?
  - Any surprising results?

### Days 18-19: Expert Discussion (if needed)

**If disputed verses exist (agreement < 80%):**

- [ ] **Organize discussion session**
  - Video call or email discussion
  - Share annotations for disputed verses only
  - Facilitate structured discussion

- [ ] **Build consensus**
  - Allow experts to explain reasoning
  - Vote on final labels
  - Document consensus notes

- [ ] **Update consensus file**
  - Add discussion notes
  - Record final agreed labels

### Days 20-21: Finalization

- [ ] **Prepare final validated corpus**
  - Create `mutadarik_golden_set_validated.jsonl`
  - Include consensus labels
  - Add expert validation metadata
  - Document confidence scores

- [ ] **Update golden set**
  - Integrate المتدارك verses into main golden set
  - Update metadata (expert-validated flag)
  - Version control (golden_set_v2.0)

- [ ] **Thank experts**
  - Send thank you email with preliminary results
  - Offer to share final publication
  - Process compensation if applicable

**Goal:** Complete validated المتدارك corpus ready for integration

---

## ✅ Phase 3 Completion Checklist

### Required Deliverables

- [ ] Agreement analysis report (JSON + summary)
- [ ] Consensus labels for all 13 verses
- [ ] Expert validation documentation
- [ ] Updated golden set with المتدارك verses
- [ ] Expert feedback summary

### Quality Metrics Achieved

- [ ] Fleiss' κ ≥ 0.85 (excellent agreement)
- [ ] ≥90% agreement on meter identification
- [ ] <10% of verses disputed
- [ ] 100% of verses have consensus labels
- [ ] Expert feedback positive

### Documentation Complete

- [ ] Annotation methodology documented
- [ ] Expert qualifications recorded
- [ ] Agreement calculations documented
- [ ] Consensus notes written
- [ ] Lessons learned captured

---

## 🎯 Success Criteria

**Phase 3 is complete when:**

1. ✅ 3+ expert annotations collected
2. ✅ Fleiss' κ ≥ 0.85 achieved
3. ✅ 100% consensus labels assigned
4. ✅ Golden set updated with validated verses
5. ✅ Documentation complete
6. ✅ Ready for Phase 4 (System Integration)

---

## 🚨 Troubleshooting

### Low Agreement (κ < 0.60)

**Actions:**
1. Review instructions - were they clear?
2. Check if specific verses are problematic
3. Consider expert discussion session
4. May need to clarify task and re-annotate
5. Consult with experts on ambiguous cases

### Expert Dropout

**Actions:**
1. Activate backup expert from reserve list
2. Extend deadline if reasonable excuse
3. Proceed with remaining experts if ≥3
4. Document dropout in methodology

### Disputed Verses

**Actions:**
1. This is expected for some verses
2. Document which verses and why
3. Facilitate expert discussion
4. May indicate genuine meter ambiguity
5. Mark as "ambiguous" if no consensus

---

## 📈 Timeline Summary

| Week | Activities | Key Milestones |
|------|-----------|----------------|
| **1** | Recruitment, Send materials | 3-5 experts confirmed |
| **2** | Annotation period | All annotations received |
| **3** | Analysis & consensus | Validated corpus complete |

**Total:** 2-3 weeks from start to completion

---

## 📧 Key Contacts

**Research Lead:** [Your name/email]
**Technical Support:** [Support contact]
**Questions:** [Primary contact]

---

## 📚 Reference Materials

**All materials ready in:**
- `/docs/PHASE_3_EXPERT_ANNOTATION_PROTOCOL.md`
- `/docs/EXPERT_ANNOTATION_INSTRUCTIONS.md`
- `/phase3_materials/README.md`

**Scripts ready at:**
- `/tools/calculate_agreement.py`
- `/tools/build_consensus.py`

---

**Checklist Version:** 1.0
**Created:** 2025-11-12
**Status:** 🚀 Ready to Launch

**Good luck with Phase 3! 🎉**
