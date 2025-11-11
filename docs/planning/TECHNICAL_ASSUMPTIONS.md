# 🔬 Technical Assumptions & Constraints
## Foundation for Implementation Decisions

---

## 📋 Purpose

This document explicitly states all **technical assumptions** made during planning. These assumptions inform architecture decisions, technology choices, and timeline estimates.

**Why this matters:**
- Prevents surprises during implementation
- Documents risks and dependencies
- Provides decision audit trail
- Helps identify when to revisit decisions

---

## 🎯 Core Assumptions

### 1. Arabic Text Input

#### Assumption 1.1: Text Encoding
```yaml
Assumption:
  - All input will be UTF-8 encoded
  - Arabic Unicode range (U+0600 to U+06FF) is sufficient
  - No legacy encodings (Windows-1256, ISO-8859-6)

Rationale:
  - UTF-8 is universal web standard
  - Modern browsers default to UTF-8
  - Simplifies text processing

Risk if wrong:
  - LOW - UTF-8 dominance is overwhelming

Mitigation:
  - Auto-detect and convert if non-UTF-8 detected
  - Validate encoding on input
```

#### Assumption 1.2: Diacritics Availability
```yaml
Assumption:
  - MVP: Most user input will LACK diacritics (حركات)
  - Classical poetry dataset: 80%+ fully diacritized
  - Modern poetry: < 20% diacritized

Rationale:
  - Arabic speakers rarely type diacritics (keyboard friction)
  - Classical texts are pre-diacritized (published works)

Risk if wrong:
  - MEDIUM - Affects prosody accuracy significantly

Mitigation:
  - Prosody engine works on NON-diacritized text (MVP)
  - Infer prosody from consonant patterns
  - Phase 2: Add optional diacritization tool
  - Accept lower accuracy (70-75%) for undiacritized text

Validation:
  - Week 2: Test with 20 undiacritized verses
  - Measure accuracy drop vs diacritized
  - If < 65%, implement emergency diacritizer
```

#### Assumption 1.3: Language Variety
```yaml
Assumption:
  - MVP focuses on Modern Standard Arabic (MSA) ONLY
  - Dialectal poetry (مصري، شامي، خليجي) deferred to Phase 2+
  - Classical Arabic (فصحى تراثية) treated as MSA variant

Rationale:
  - MSA is universally understood
  - Dialects have different prosody rules
  - Resource constraints (solo developer)

Risk if wrong:
  - LOW - Scope creep if users demand dialects

Mitigation:
  - Clearly label as "MSA only" in UI
  - Collect dialect requests for Phase 2 prioritization
  - Document: "Dialect support coming in Q3 2026"

Non-Negotiable:
  - DO NOT implement dialect analysis in MVP
  - Reject scope creep politely but firmly
```

---

### 2. Computational Resources

#### Assumption 2.1: Development Environment
```yaml
Assumption:
  - Development on MacBook Pro M1/M2 (ARM64 architecture)
  - 16GB RAM, 512GB SSD
  - macOS Sonoma or later

Rationale:
  - Developer's current hardware
  - Industry-standard for development

Risk if wrong:
  - HIGH - M1/M2 compatibility issues with Python libraries

Mitigation:
  - Day 1 Hour 1: Test CAMeL Tools compatibility
  - 3 fallback strategies:
    1. ARM64 native install
    2. Rosetta x86_64 emulation
    3. Docker linux/amd64 containers
  - Document which approach works

Validation Criteria:
  - CAMeL Tools imports without error
  - Basic diacritization works
  - Performance acceptable (< 500ms for simple normalization)

If all fail:
  - Emergency pivot: PyArabic-only implementation
  - Reduced accuracy (60-65%), but functional
  - Re-evaluate CAMeL Tools in Week 2 with Docker
```

#### Assumption 2.2: Production Environment
```yaml
Assumption:
  - Backend: 512MB RAM, 1 vCPU (Railway/DigitalOcean droplet)
  - Database: PostgreSQL 15 (managed service)
  - Cache: Redis 256MB (managed or Docker)
  - Frontend: Vercel (free tier, 100GB bandwidth)

Rationale:
  - Cost-effective for MVP (< $20/month total)
  - Scales to ~1000 DAU without changes
  - Industry-proven stack

Risk if wrong:
  - MEDIUM - Memory constraints may limit concurrency

Mitigation:
  - Week 6: Load test with 50 concurrent requests
  - If memory > 400MB: Optimize or upgrade to 1GB
  - Horizontal scaling: Add 2nd backend instance

Cost Contingency:
  - Budget: $20/month MVP
  - If exceeds $30: Optimize or seek funding
  - If exceeds $50: Re-architecture required
```

#### Assumption 2.3: Database Size
```yaml
Assumption:
  - Year 1: < 100,000 users
  - Analyses stored: ~1 million
  - Database size: < 10GB
  - Growth: 1-2GB/month

Rationale:
  - Realistic for MVP launch
  - Text data is small (avg 200 bytes/verse)
  - PostgreSQL free tier: 10GB (Railway) to 25GB (DigitalOcean)

Risk if wrong:
  - LOW - Easy to upgrade storage

Mitigation:
  - Monthly monitoring
  - Auto-archive analyses > 1 year old
  - Implement data retention policy (GDPR compliance)

Storage Plan:
  - Year 1: 10GB free tier ✅
  - Year 2: Upgrade to 50GB ($5/month) if needed
  - Year 3: Evaluate cold storage (S3 Glacier)
```

---

### 3. Data Availability

#### Assumption 3.1: Training Dataset Accessibility
```yaml
Assumption:
  - Can collect 100-200 verses from public domain sources (MVP)
  - Al-Diwan.net: Scraping allowed (robots.txt permissive)
  - Classical poetry: Public domain (pre-1900)
  - Modern poetry: Requires licensing or user-generated content

Rationale:
  - Classical poetry is public domain globally
  - Al-Diwan is the largest free Arabic poetry database
  - UNESCO archives freely accessible

Risk if wrong:
  - MEDIUM - Legal issues if copyright violated

Mitigation:
  - Week 1: Verify Al-Diwan.net Terms of Service
  - Only use pre-1900 works (definite public domain)
  - For modern poetry: Seek explicit permission or license
  - User-generated: Require content transfer agreement

Legal Checklist:
  - ☐ Read Al-Diwan ToS (Week 1 Day 1)
  - ☐ Consult copyright lawyer ($100-200 for 1-hour consult)
  - ☐ Draft user content agreement
  - ☐ Implement DMCA takedown process

If assumption fails:
  - Fallback: Use only معلقات + 100 manually collected verses
  - Lower accuracy expected (65-70%)
  - Gradual dataset growth from user submissions
```

#### Assumption 3.2: Dataset Quality
```yaml
Assumption:
  - 90%+ of collected classical poetry is correctly metered
  - 5-10% may have typos or OCR errors
  - Manual verification required for critical verses

Rationale:
  - Classical poets followed strict meter rules
  - OCR technology introduces errors
  - Human curation needed for gold standard

Risk if wrong:
  - HIGH - Garbage in = garbage out (poor model accuracy)

Mitigation:
  - Week 1-2: Manually curate "Golden Set" (20 perfect verses)
  - Week 2: Label 100 verses with triple-verification
  - Week 4: Expert review (hire Arabic literature grad student, $200)
  - Week 6: Expand to 500 verses (crowdsource validation)

Quality Criteria:
  - Golden Set: 100% accuracy (use معلقات)
  - Training Set: > 95% accuracy
  - Test Set: > 98% accuracy (manually verified)

Red Flag:
  - If accuracy on golden set < 80% → algorithm bug or bad assumptions
```

---

### 4. User Behavior

#### Assumption 4.1: Input Length
```yaml
Assumption:
  - 80% of inputs: 1-2 verses (< 200 characters)
  - 15% of inputs: 3-10 verses (200-1000 characters)
  - 5% of inputs: Full poem (> 1000 characters)

Rationale:
  - Most users want quick meter check
  - Learning use case: analyze single verse from textbook
  - Edge case: Full qasida analysis

Risk if wrong:
  - LOW - Easy to handle longer inputs

Mitigation:
  - Input limit: 2000 characters (hard cap)
  - For longer texts: Batch analysis API (split into verses)
  - UI hint: "Best results with 1-2 verses at a time"

Performance Impact:
  - 1 verse: < 100ms target
  - 10 verses: < 1s target
  - 100 verses: Use async job queue (Celery + Redis)
```

#### Assumption 4.2: Usage Patterns
```yaml
Assumption:
  - Peak usage: Evenings (8-11 PM Gulf time)
  - Weekday: 60% of traffic
  - Weekend: 40% of traffic
  - Exam season (April-May): 3x normal traffic

Rationale:
  - Target users: Students, teachers, hobbyists
  - Arabic poetry taught in schools (exam-driven traffic)

Risk if wrong:
  - MEDIUM - Under-provisioned infrastructure

Mitigation:
  - Auto-scaling: 1-3 backend instances
  - Caching: 1-hour TTL for repeat analyses
  - CDN: Vercel handles frontend traffic spikes

Capacity Planning:
  - Normal: 100 requests/hour (1 instance OK)
  - Peak: 500 requests/hour (2-3 instances)
  - Exam season: 1500 requests/hour (5 instances + aggressive caching)

Cost:
  - Auto-scale cost: $0.002/instance/minute
  - Peak hour cost: $0.30
  - Exam season month: +$50
```

---

### 5. Accuracy & Performance

#### Assumption 5.1: Acceptable Accuracy Targets
```yaml
Assumption:
  - MVP acceptable accuracy: 70-75%
  - Good accuracy (6 months): 80-85%
  - Excellent accuracy (1 year+): 90%+

Rationale:
  - Rule-based systems plateau at 70-80%
  - ML approaches needed for 85%+
  - Human experts: 95%+ (not 100%, poetry is ambiguous)

Risk if wrong:
  - MEDIUM - Users expect higher accuracy

Mitigation:
  - Transparent communication: "Beta - 70% accurate"
  - Show confidence scores (not just binary correct/wrong)
  - Collect user feedback: "Was this correct?" thumbs up/down
  - Iterative improvement: +2-3% accuracy every 2 weeks

User Expectation Management:
  - UI: Display confidence % (e.g., "75% confident: الطويل")
  - Help text: "Accuracy improves with diacritics"
  - Roadmap: "90% accuracy by Q2 2026"

Pivot Point:
  - Week 5: If accuracy < 65% on test set
  - Decision: Reduce from 16 meters to 8 most common
  - Communicate: "Focused on quality over quantity"
```

#### Assumption 5.2: Response Time Requirements
```yaml
Assumption:
  - P50 (median): < 200ms
  - P95: < 500ms
  - P99: < 1000ms
  - Timeout: 5 seconds

Rationale:
  - Users expect instant feedback (< 1s feels immediate)
  - Complex analyses may take longer
  - 5s timeout prevents hung requests

Risk if wrong:
  - MEDIUM - Slow response = poor UX = churn

Mitigation:
  - Week 3: Benchmark all algorithm components
  - Optimize hot paths (normalization, syllabification)
  - Redis caching: 80%+ cache hit rate
  - If slow: Profile with py-spy, optimize or parallelize

Performance Budget:
  - Normalization: 10ms
  - Syllabification: 30ms
  - Pattern matching: 50ms
  - Meter detection: 50ms
  - Database write: 20ms
  - Total: 160ms (40ms buffer)
```

---

### 6. Security & Privacy

#### Assumption 6.1: Threat Model
```yaml
Assumption:
  - Primary threats: XSS, SQL injection, credential stuffing
  - Secondary threats: DDoS, data breach
  - Low threat: Nation-state actors (not a target)

Rationale:
  - Educational platform, low-value data
  - Standard web app threats apply
  - Not handling payments (Phase 1)

Risk if wrong:
  - HIGH if wrong - Reputation damage, legal liability

Mitigation:
  - Week 1: Implement security baseline (see SECURITY.md)
    - bcrypt password hashing (cost 12)
    - JWT tokens (30min access, 7day refresh)
    - SQL injection prevention (ORM only, no raw SQL)
    - XSS protection (escape all user input)
    - Rate limiting (100 req/hour per IP)
  - Week 8: Security audit (OWASP Top 10 checklist)
  - Week 12: Penetration testing (hire freelancer, $500)

Red Lines:
  - NEVER store passwords in plain text
  - NEVER trust user input
  - NEVER skip input validation
  - NEVER disable HTTPS in production
```

#### Assumption 6.2: Data Privacy
```yaml
Assumption:
  - Users expect basic privacy (GDPR-compliant)
  - OK to store analyses for improving model
  - Anonymized data sharing acceptable for research

Rationale:
  - European users require GDPR compliance
  - Data is key to improving accuracy
  - Academic research boosts credibility

Risk if wrong:
  - HIGH - GDPR fines (up to 4% revenue or €20M)

Mitigation:
  - Week 1: Privacy policy draft (consult lawyer, $300)
  - Implement:
    - Data export (user can download all their data)
    - Data deletion (right to be forgotten)
    - Consent checkboxes (opt-in for research use)
  - Privacy by design:
    - Don't collect data not needed
    - Anonymous analytics (no PII)
    - Encrypt backups (AES-256)

GDPR Checklist:
  - ☐ Privacy policy published
  - ☐ Cookie consent banner
  - ☐ Data export endpoint
  - ☐ Account deletion endpoint
  - ☐ Data retention policy (1 year, then anonymize)
```

---

## 🔄 Assumption Validation Schedule

```yaml
Week 1 Day 1:
  - M1/M2 compatibility (CAMeL Tools)
  - Al-Diwan.net Terms of Service

Week 2:
  - Accuracy on undiacritized text (golden set)
  - Backend memory usage (< 512MB?)

Week 5:
  - Overall accuracy (> 65% pivot point)
  - Response time (< 500ms P95?)

Week 8:
  - Security audit results
  - Database size growth rate

Week 12:
  - User behavior patterns (actual vs assumed)
  - Cost per user (< $0.10?)
```

---

## 📝 Updating This Document

**When to update:**
- Assumption proven wrong during development
- New information changes risk assessment
- Pivot decisions made

**How to update:**
1. Add strikethrough to wrong assumption
2. Add new section: "Revised Assumption X.X (Date)"
3. Document reason for change
4. Update docs/project-management/PROGRESS_LOG_CURRENT.md with reference

**Example:**
```markdown
#### ~~Assumption 1.2: Diacritics Availability~~ ❌ REVISED (Week 2)

**Original Assumption:**
- MVP: Most user input will LACK diacritics

**Reality:**
- Week 2 testing: 60% of users added diacritics (higher than expected)

**Revised Assumption 1.2b:**
- Hybrid approach: Support both diacritized and undiacritized
- Adjust accuracy targets: 80% with diacritics, 70% without

**Impact:**
- No code changes needed (already designed for both)
- Update marketing: "Best accuracy with tashkeel"
```

---

## ✅ Pre-Week-1 Validation Checklist

Before starting development, verify:

```yaml
☐ All assumptions read and understood
☐ High-risk assumptions identified (highlighted above)
☐ Mitigation plans ready for top 5 risks
☐ Week 1 Day 1 validation tasks scheduled (M1/M2 test, ToS review)
☐ Acceptance criteria defined for pivot decisions (65% accuracy)
☐ Budget allocated for contingencies (lawyer, security audit)
☐ Comfort level with 70-75% MVP accuracy (not 85%)
☐ Agreement: If assumption fails, pivot not panic
```

---

**Last Updated:** November 8, 2025
**Status:** ✅ Baseline assumptions documented
**Next Review:** Week 5 (Pivot decision point)

**Remember:** Assumptions are not facts. Validate early, pivot gracefully when wrong.
