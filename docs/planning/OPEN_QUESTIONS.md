# ❓ Open Questions & Decisions Needed
## Pre-Week-1 Critical Decision Log

---

## 📋 Purpose

This document tracks **unresolved questions** that must be answered before or during implementation. Each question has:
- Decision deadline
- Decision owner
- Available options
- Recommendation
- Impact if delayed

**Status Tracking:**
- 🔴 BLOCKING - Must resolve before Week 1
- 🟡 HIGH PRIORITY - Decide by Week 2
- 🟢 MEDIUM PRIORITY - Decide by Week 5
- ⚪ LOW PRIORITY - Can defer to Phase 2

---

## 🔴 BLOCKING QUESTIONS (Resolve Before Week 1)

### Q1: CAMeL Tools Compatibility on M1/M2 Mac

**Question:**
Which installation method works for CAMeL Tools on Apple Silicon?

**Options:**
1. **ARM64 Native Install**
   - Command: `arch -arm64 pip install camel-tools==1.5.2`
   - Pros: Best performance, native execution
   - Cons: May not work (ARM64 support uncertain)

2. **Rosetta x86_64 Emulation**
   - Command: `arch -x86_64 pip install camel-tools==1.5.2`
   - Pros: Higher compatibility, minimal performance loss
   - Cons: Adds complexity, slower than native

3. **Docker linux/amd64 Container**
   - Command: `docker run --platform=linux/amd64 python:3.11`
   - Pros: 100% compatible, matches production
   - Cons: Docker overhead, more complex dev setup

4. **Fallback: PyArabic Only** (If all fail)
   - Remove CAMeL Tools, use PyArabic for basic normalization
   - Pros: Lightweight, guaranteed compatibility
   - Cons: Lower accuracy (60-65%), missing features

**Recommendation:** Test in order 1 → 2 → 3, document which works

**Decision By:** Week 1 Day 1 Hour 1 (CRITICAL PATH)

**Decision Owner:** Developer

**Impact if Delayed:**
- Complete blocker for NLP functionality
- Cannot proceed with prosody engine development
- Week 1 timeline slips

**Validation Criteria:**
```python
# Test must pass:
from camel_tools.utils.normalize import normalize_unicode
text = "أَهْلاً بِكُمْ"
result = normalize_unicode(text)
assert result is not None
# If passes: Document method in PROGRESS_LOG.md
```

**Status:** ⏳ UNRESOLVED - Test on Day 1

---

### Q2: Diacritics Handling Strategy

**Question:**
Should the MVP require diacritics (tashkeel) or work without them?

**Context:**
- With diacritics: 85%+ accuracy possible
- Without diacritics: 65-70% accuracy likely
- Most users don't type diacritics (keyboard friction)

**Options:**
1. **Require Diacritics (Strict)**
   - Reject undiacritized input with error message
   - Provide diacritizer tool in UI
   - Pros: Higher accuracy, simpler algorithm
   - Cons: Poor UX, barrier to entry

2. **Accept Both (Hybrid)** ✅ RECOMMENDED
   - Algorithm works with or without diacritics
   - Show confidence score reflecting quality
   - UI hint: "Add tashkeel for better accuracy"
   - Pros: Best UX, flexible
   - Cons: More complex algorithm

3. **Auto-Diacritize (Advanced)**
   - Use CAMeL Tools to add diacritics automatically
   - Pros: Best accuracy + good UX
   - Cons: 10-15% diacritization error rate → wrong meter
   - Cost: +100ms latency

**Recommendation:** Option 2 (Hybrid) for MVP

**Decision By:** Week 1 (before coding normalization module)

**Decision Owner:** Developer

**Impact if Delayed:**
- Algorithm design affected
- May need refactoring if decision changes

**Validation Criteria:**
- Week 2: Test with 10 diacritized + 10 undiacritized verses
- Measure accuracy difference
- If undiacritized < 60%: Consider auto-diacritization

**Status:** ⏳ UNRESOLVED - Decide Week 1

---

### Q3: Database Hosting Choice

**Question:**
Where to host PostgreSQL database?

**Options:**
1. **Railway (Free Tier)**
   - 500MB database, 500 hours/month
   - Pros: Free, easy setup, $5/month for more
   - Cons: Sleep after inactivity, shared resources

2. **DigitalOcean Managed Database**
   - $15/month minimum (1GB RAM, 10GB storage)
   - Pros: Always-on, dedicated resources, backups
   - Cons: Cost, overkill for MVP

3. **Supabase (Free Tier)**
   - 500MB database, built-in auth & API
   - Pros: Free, generous limits, nice UI
   - Cons: Vendor lock-in, PostgreSQL only

4. **Self-Hosted Docker**
   - PostgreSQL in Docker on VPS
   - Pros: Full control, cheapest ($5/month VPS)
   - Cons: Manual backups, maintenance burden

**Recommendation:** Railway for MVP (free), migrate to DigitalOcean at 1000 users

**Decision By:** Week 1 Day 3 (database setup day)

**Decision Owner:** Developer

**Impact if Delayed:**
- Cannot set up database schema
- Cannot test backend API
- Timeline slips

**Validation Criteria:**
- Successful database connection
- < 50ms query latency
- Automatic backups configured

**Status:** ⏳ UNRESOLVED - Decide Week 1 Day 2

---

## 🟡 HIGH PRIORITY QUESTIONS (Decide by Week 2)

### Q4: Accuracy Target for MVP

**Question:**
What meter detection accuracy is acceptable for MVP launch?

**Context:**
- Rule-based systems typically achieve 70-80%
- ML-based systems can reach 85-90%+
- Human experts: 95% (poetry is sometimes ambiguous)

**Options:**
1. **Conservative: 70-75%**
   - Achievable with rule-based approach
   - Honest communication: "Beta accuracy"
   - Pros: Realistic, attainable in 14 weeks
   - Cons: May disappoint users expecting perfection

2. **Ambitious: 80-85%**
   - Requires hybrid approach (rules + ML hints)
   - More development time needed
   - Pros: Competitive, impressive
   - Cons: Risk of not achieving, timeline pressure

3. **Aspirational: 90%+**
   - Requires ML model (Phase 2)
   - Not feasible for MVP
   - Pros: World-class
   - Cons: Unrealistic for 14-week timeline

**Recommendation:** Option 1 (70-75%) with roadmap to 85% in 6 months

**Decision By:** Week 2 (after golden set testing)

**Decision Owner:** Developer

**Impact if Delayed:**
- Unclear success criteria
- May over-engineer unnecessarily
- Burnout risk from unrealistic goals

**Validation Criteria:**
- Week 2: Test on 20-verse golden set
- Calculate accuracy
- If 70-75%: Proceed with MVP
- If < 65%: Trigger fallback (reduce to 8 meters)

**Status:** ⏳ UNRESOLVED - Test Week 2

---

### Q5: Meter Scope (16 vs 8 Meters)

**Question:**
Should MVP support all 16 classical meters or focus on 8 most common?

**Context:**
- All 16 meters: Comprehensive, academically sound
- 8 common meters: Covers 80% of usage, faster to implement

**Options:**
1. **All 16 Meters (Comprehensive)**
   - الطويل، المديد، البسيط، الوافر، الكامل، الهزج، الرجز، الرمل، السريع، المنسرح، الخفيف، المضارع، المقتضب، المجتث، المتقارب، المحدث
   - Pros: Complete coverage, marketing advantage
   - Cons: More complex, lower accuracy per meter

2. **8 Common Meters (Focused)** ✅ FALLBACK OPTION
   - الطويل، البسيط، الكامل، الوافر، الرجز، الرمل، الخفيف، المتقارب
   - Pros: Higher accuracy, faster implementation, easier testing
   - Cons: Incomplete, users may request missing meters

**Recommendation:** Start with 16, pivot to 8 if accuracy < 65% by Week 5

**Decision By:** Week 5 (pivot decision point)

**Decision Owner:** Developer

**Impact if Delayed:**
- Wasted effort if wrong choice
- Timeline risk

**Validation Criteria:**
- Week 5: Measure accuracy on all 16 meters
- If overall accuracy > 70%: Keep 16 ✅
- If < 65%: Reduce to 8 🔄
- Document decision in PROGRESS_LOG.md

**Pivot Plan:**
```yaml
If accuracy < 65%:
  - Remove 8 rare meters (keep common 8)
  - Re-test accuracy (expect +5-10% improvement)
  - Update documentation and UI
  - Communicate: "Focused on quality over quantity"
  - Estimate saved time: 1-2 weeks
```

**Status:** ⏳ UNRESOLVED - Decide Week 5

---

### Q6: Frontend Framework: Next.js vs Simpler Alternative?

**Question:**
Is Next.js 14 (App Router) the right choice or overkill for MVP?

**Context:**
- Next.js 14: Modern, powerful, but complex
- Alternatives: React (Vite), Vue, even vanilla JS

**Options:**
1. **Next.js 14 with App Router** (Current Plan)
   - Pros: SSR, SEO, modern, Vercel deployment
   - Cons: Learning curve, complexity

2. **React + Vite (Simpler)**
   - Pros: Faster dev, simpler, lightweight
   - Cons: No SSR, manual routing

3. **Vue 3 + Vite**
   - Pros: Easier than React, good Arabic support
   - Cons: Less ecosystem, less familiarity

**Recommendation:** Stick with Next.js 14 (already planned, good long-term)

**Decision By:** Week 1 (before frontend setup)

**Decision Owner:** Developer

**Impact if Delayed:**
- Frontend development blocked
- Timeline slips

**Validation Criteria:**
- If comfortable with Next.js: Proceed
- If struggling Week 2: Consider pivot to Vite

**Status:** ✅ RESOLVED - Next.js 14 (confirmed)

---

## 🟢 MEDIUM PRIORITY QUESTIONS (Decide by Week 5)

### Q7: Authentication: JWT vs Session Cookies?

**Question:**
Which authentication method for MVP?

**Options:**
1. **JWT (Stateless)**
   - Pros: Scalable, API-friendly, mobile-ready
   - Cons: Cannot revoke tokens easily, larger size

2. **Session Cookies (Stateful)**
   - Pros: Easy revocation, secure, smaller
   - Cons: Requires Redis/DB, less scalable

**Recommendation:** JWT for MVP (stateless, simpler backend)

**Decision By:** Week 1 (before auth implementation)

**Status:** ✅ RESOLVED - JWT (30min access, 7day refresh)

---

### Q8: Rate Limiting Strategy

**Question:**
How strict should rate limits be?

**Options:**
1. **Lenient: 100 requests/hour per IP**
   - Good for users, may allow abuse
2. **Moderate: 50 requests/hour per IP**
   - Balanced
3. **Strict: 20 requests/hour per IP**
   - Prevents abuse, may frustrate legitimate users

**Recommendation:** 100/hour for MVP, monitor and adjust

**Decision By:** Week 1 (security baseline implementation)

**Status:** ✅ RESOLVED - 100/hour (see BACKEND_API.md)

---

### Q9: Error Messages: Arabic vs English vs Both?

**Question:**
What language for error messages?

**Options:**
1. **Arabic Only** - Target audience is Arabic speakers
2. **English Only** - Developer convenience, international appeal
3. **Both (i18n)** - Best UX, more complex

**Recommendation:** Both (JSON response with `message_ar` and `message_en`)

**Decision By:** Week 2 (API development)

**Status:** ⏳ UNRESOLVED - Decide Week 2

---

## ⚪ LOW PRIORITY QUESTIONS (Can Defer to Phase 2)

### Q10: Analytics Tool Choice

**Question:**
Google Analytics vs Plausible vs self-hosted?

**Recommendation:** Defer to Week 8 (not critical for MVP functionality)

**Status:** ⏳ DEFERRED

---

### Q11: Email Service for Notifications

**Question:**
SendGrid vs AWS SES vs Resend?

**Recommendation:** Defer to Phase 2 (email not needed for MVP)

**Status:** ⏳ DEFERRED

---

### Q12: Payment Gateway (Phase 2+)

**Question:**
Stripe vs local payment providers (Telr, Payfort)?

**Recommendation:** Research in Month 6 (not MVP feature)

**Status:** ⏳ DEFERRED

---

## 📊 Decision Log

| Question | Status | Decision | Date | Notes |
|----------|--------|----------|------|-------|
| Q6: Next.js vs alternatives | ✅ RESOLVED | Next.js 14 | Nov 8 | Confirmed in planning |
| Q7: JWT vs Sessions | ✅ RESOLVED | JWT | Nov 8 | See SECURITY.md |
| Q8: Rate limiting | ✅ RESOLVED | 100/hour | Nov 8 | See BACKEND_API.md |
| Q1: M1/M2 compatibility | ⏳ PENDING | TBD | Day 1 Hour 1 | CRITICAL |
| Q2: Diacritics | ⏳ PENDING | TBD | Week 1 | Lean toward hybrid |
| Q3: Database hosting | ⏳ PENDING | TBD | Week 1 Day 2 | Lean toward Railway |
| Q4: Accuracy target | ⏳ PENDING | TBD | Week 2 | Test golden set first |
| Q5: Meter scope | ⏳ PENDING | TBD | Week 5 | Start with 16, pivot if needed |
| Q9: Error language | ⏳ PENDING | TBD | Week 2 | Lean toward both |
| Q10-Q12 | ⏳ DEFERRED | N/A | Phase 2+ | Not MVP-critical |

---

## 🎯 Decision-Making Framework

When answering open questions, use this framework:

```yaml
1. Gather Data:
   - Test/prototype if possible
   - Research best practices
   - Check community feedback

2. Evaluate Options:
   - Pros/cons list
   - Impact on timeline
   - Cost (money, time, complexity)
   - Reversibility (can we change later?)

3. Make Decision:
   - Choose based on MVP goals (not long-term perfection)
   - Document rationale
   - Set success criteria
   - Plan pivot if wrong

4. Validate:
   - Test decision with real usage
   - Measure against criteria
   - Be willing to reverse if data shows mistake
```

**Key Principle:** Prefer **reversible decisions** early. Avoid **one-way doors** until necessary.

---

## 📝 How to Use This Document

**Before Week 1:**
1. Read all BLOCKING (🔴) questions
2. Schedule time to resolve them (Day 1-2)
3. Prepare for contingencies (all options documented)

**During Week 1-2:**
1. Resolve HIGH PRIORITY (🟡) questions
2. Document decisions in this file
3. Update affected documentation (PROSODY_ENGINE.md, etc.)

**Week 5:**
1. Review MEDIUM PRIORITY (🟢) questions
2. Make pivot decisions if needed (Q5)
3. Update roadmap

**Adding New Questions:**
```markdown
### Q##: Question Title

**Question:** Clear, concise question?

**Context:** Why is this important?

**Options:**
1. Option A
   - Pros:
   - Cons:
2. Option B
   - Pros:
   - Cons:

**Recommendation:** X because Y

**Decision By:** Week #

**Decision Owner:** Name

**Impact if Delayed:** ...

**Validation Criteria:** ...

**Status:** ⏳ UNRESOLVED
```

---

**Last Updated:** November 8, 2025
**Next Review:** Week 1 Day 1 (Resolve blocking questions)

**Remember:** It's better to make a good decision quickly than to delay for a perfect decision. Document, test, and iterate.
