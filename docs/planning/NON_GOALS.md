# 🚫 Non-Goals: Explicitly Out of Scope
## What We Are NOT Building (And Why)

---

## 📋 Purpose

This document explicitly lists features, capabilities, and use cases that are **OUT OF SCOPE** for the BAHR project (at least for MVP and near-term phases).

**Why This Matters:**
- Prevents scope creep ("wouldn't it be cool if...")
- Keeps team focused on core value proposition
- Sets realistic user expectations
- Provides clear "No" with rationale (not just "later")

**Golden Rule:** If a feature isn't listed in the MVP plan AND isn't here as explicitly deferred, **IT SHOULD BE ADDED HERE BEFORE BEING BUILT**.

---

## 🎯 MVP Scope Reminder

### ✅ What We ARE Building (MVP - Phase 1)

```yaml
Core Features:
  - Prosodic meter detection (16 classical meters)
  - Text normalization and syllabification
  - Confidence scoring
  - Analysis history (authenticated users)
  - Basic user authentication
  - Simple, clean UI

Success Criteria:
  - 70-75% meter detection accuracy
  - < 500ms analysis response time
  - 1000+ registered users by Month 3
  - Positive user feedback (> 70% satisfied)
```

---

## 🚫 Non-Goals by Category

### 1. Language Support

#### ❌ Non-Arabic Languages
```yaml
Out of Scope:
  - Persian/Farsi poetry (فارسی)
  - Urdu poetry (اردو)
  - Turkish poetry (Türkçe)
  - English/French/other languages

Rationale:
  - Different prosodic systems
  - Different linguistic rules
  - Resource constraints (solo developer)
  - Market focus: Arabic speakers

User Request Response:
  "BAHR is focused exclusively on Arabic poetry. For Persian/Urdu,
   we recommend [competitor tool]. We may expand to other languages
   in 2026 based on demand."

Future Possibility: LOW (Year 3+ if at all)
```

#### ❌ Arabic Dialect Poetry (MVP)
```yaml
Out of Scope (Phase 1):
  - Egyptian dialect (عامية مصرية)
  - Levantine dialect (شامي)
  - Gulf dialect (خليجي)
  - Maghrebi dialect (مغربي)
  - Any non-MSA poetry

Rationale:
  - Different prosodic patterns
  - Requires separate rule sets
  - Smaller market per dialect
  - MVP complexity budget exhausted

User Request Response:
  "MVP supports Modern Standard Arabic (MSA) only. Dialect support
   (مصري، شامي، خليجي) is planned for Phase 3 (Q3 2026)."

Deferred To: Phase 3 (Month 9+)
Priority: MEDIUM (high user demand, but complex)

Requirements Before Implementation:
  - 5000+ MAU (proven market demand)
  - Hire Arabic linguist for each dialect (3+ months)
  - Collect 1000+ verses per dialect
  - Budget: $5k+ per dialect
```

---

### 2. Advanced Literary Analysis

#### ❌ Rhyme Scheme Analysis (MVP)
```yaml
Out of Scope (Phase 1):
  - Qāfiyah (قافية) detection
  - Rhyme letter (حرف الروي) identification
  - Rhyme types (مطلقة، مقيدة، etc.)
  - Internal rhyme (جناس داخلي)

Rationale:
  - MVP focuses on meter detection ONLY
  - Rhyme analysis requires additional algorithm complexity
  - Lower user priority (meter is #1 request)
  - Can be added later without major refactoring

User Request Response:
  "Rhyme analysis is a planned feature for Phase 2 (Month 6).
   Current MVP focuses on prosodic meter detection."

Deferred To: Phase 2 (Month 6+)
Priority: HIGH (common user request)

See: docs/planning/DEFERRED_FEATURES.md for full specification
```

#### ❌ Rhetorical Devices (البديع)
```yaml
Out of Scope (All Phases):
  - Jinās (جناس) - pun/paronomasia
  - Ṭibāq (طباق) - antithesis
  - Tawriya (تورية) - double entendre
  - Muqābala (مقابلة) - juxtaposition
  - Other rhetorical figures

Rationale:
  - Requires advanced NLP (sentiment analysis, semantic similarity)
  - Very low accuracy without ML (< 40%)
  - PhD-level complexity
  - Diminishing returns (nice-to-have, not need-to-have)

User Request Response:
  "Rhetorical device analysis requires AI/ML capabilities beyond
   our current scope. Consider using specialized tools like [X]."

Deferred To: Never (not core value proposition)
Priority: VERY LOW
```

#### ❌ Stylistic Fingerprinting
```yaml
Out of Scope:
  - Poet identification ("This sounds like المتنبي")
  - Era classification (Jahili vs Abbasid vs Modern)
  - Authorship attribution
  - Stylistic comparison

Rationale:
  - Requires large corpus (10k+ verses per poet)
  - ML/AI necessary (not rule-based)
  - Academic research problem, not user need
  - BAHR is a tool, not a research platform

Deferred To: Phase 4+ (Year 2+, if ever)
Priority: LOW (interesting but not valuable)
```

---

### 3. Content Creation

#### ❌ AI Poetry Generation (MVP)
```yaml
Out of Scope (Phase 1):
  - Generate original Arabic poetry
  - "الشاعر الذكي" (AI Poet) feature
  - Auto-complete verses
  - Poetry suggestions

Rationale:
  - Requires fine-tuned LLM (Jais-13B or similar)
  - Training cost: $100-500
  - Inference cost: $0.01-0.05 per generation
  - Complex to do well (meter + meaning + beauty)
  - MVP is ANALYSIS not CREATION

User Request Response:
  "AI poetry generation is planned for Phase 2 (Month 6+) after
   we perfect the analysis engine. Stay tuned!"

Deferred To: Phase 2 (Month 6+)
Priority: HIGH (strong user demand, monetization opportunity)

See: docs/technical/AI_MODEL_ARCHITECTURE.md for full design
```

#### ❌ Poetry Editing Tools
```yaml
Out of Scope:
  - Text editor with meter validation
  - Real-time meter checking while typing
  - Auto-correction suggestions ("change this word to...")
  - Synonym suggestions to fix meter

Rationale:
  - Complex UI/UX requirements
  - Requires extensive Arabic NLP (synonyms, word embeddings)
  - MVP is batch analysis, not interactive editing

Deferred To: Phase 3 (Month 9+)
Priority: MEDIUM
```

---

### 4. Social & Community Features

#### ❌ Social Network Features (MVP)
```yaml
Out of Scope (Phase 1):
  - User profiles (beyond basic auth)
  - Follow/followers system
  - Activity feeds
  - Comments and discussions
  - Likes and reactions
  - Sharing to social media
  - Poet leaderboards

Rationale:
  - MVP is a tool, not a social platform
  - Social features are a distraction from core value
  - Requires moderation (time-consuming)
  - "Build it and they will come" fallacy

User Request Response:
  "We're focused on building the best prosody analyzer first.
   Social features may come later based on user feedback."

Deferred To: Phase 3+ (Month 9+, if demand is proven)
Priority: LOW-MEDIUM (users may want it, but not core)

Requirements Before Implementation:
  - 5000+ MAU
  - Proven engagement (> 50% weekly active users)
  - Content moderation strategy
  - Budget for moderation staff or AI tools
```

#### ❌ Competition System (MVP)
```yaml
Out of Scope (Phase 1):
  - Poetry competitions/contests
  - Judging system
  - Prize distribution
  - Voting mechanisms
  - Competition discovery feed

Rationale:
  - Complex feature set (6-8 weeks development)
  - Requires payment integration (Stripe, etc.)
  - Legal complexity (prize regulations vary by country)
  - Moderation burden (cheating, disputes)

Deferred To: Phase 2 (Month 6+)
Priority: MEDIUM (nice-to-have, community engagement)

See: docs/planning/DEFERRED_FEATURES.md
```

---

### 5. Educational Features

#### ❌ Prosody Learning Platform
```yaml
Out of Scope:
  - Interactive lessons on علم العروض
  - Quizzes and exercises
  - Progress tracking
  - Certificates of completion
  - Gamification (badges, levels)

Rationale:
  - Education is a separate product vertical
  - Requires curriculum design (hire educator)
  - Content creation burden (100+ hours)
  - Different user persona (learners vs practitioners)

User Request Response:
  "BAHR is an analysis tool, not a learning platform.
   For prosody education, we recommend [academic resource]."

Deferred To: Phase 4+ (Year 2+) OR separate product
Priority: LOW (adjacent market, not core)
```

#### ❌ Teacher Dashboard
```yaml
Out of Scope:
  - Classroom management
  - Student assignments
  - Grading tools
  - Analytics for teachers

Rationale:
  - Enterprise/education market requires different approach
  - B2B sales and support complexity
  - Compliance requirements (FERPA, student data privacy)

Deferred To: Year 2+ (if pursuing education market)
Priority: LOW
```

---

### 6. Technical Capabilities

#### ❌ OCR / Image-to-Text
```yaml
Out of Scope:
  - Upload image of Arabic text
  - Extract text via OCR
  - Analyze scanned poetry books
  - Handwriting recognition

Rationale:
  - OCR is a solved problem (use Google Cloud Vision, Tesseract)
  - Not core differentiation
  - Error-prone (OCR errors → wrong analysis)
  - Mobile camera integration complexity

User Workaround:
  "Use Google Lens or any OCR app to extract text,
   then paste into BAHR for analysis."

Deferred To: Phase 3+ (low priority)
Priority: LOW (workaround available)
```

#### ❌ Audio / Speech-to-Text
```yaml
Out of Scope:
  - Record voice reading poetry
  - Convert to text
  - Analyze prosody from speech
  - Pronunciation feedback

Rationale:
  - Speech recognition is complex (especially Arabic)
  - Different problem domain (phonetics vs text analysis)
  - Low user demand (most users have text)

Deferred To: Not planned
Priority: VERY LOW
```

#### ❌ PDF / Book Analysis
```yaml
Out of Scope:
  - Upload PDF of poetry book
  - Extract and analyze all poems
  - Batch processing of documents
  - Export analysis reports

Rationale:
  - Complex PDF parsing (especially Arabic PDF issues)
  - Large file uploads (infrastructure cost)
  - Different use case (bulk analysis vs interactive)

Deferred To: Phase 3+ (enterprise feature)
Priority: LOW
```

---

### 7. Monetization & Business

#### ❌ Payment & Subscriptions (MVP)
```yaml
Out of Scope (Phase 1):
  - Premium tiers
  - Stripe integration
  - Subscription management
  - Usage limits
  - Billing history

Rationale:
  - MVP should be free to maximize adoption
  - Monetization requires proven value first
  - Payment integration complexity (2-3 weeks)
  - Legal/tax compliance burden

Deferred To: Phase 2 (Month 6+) after proving value
Priority: HIGH (required for sustainability)

Pricing Strategy (Future):
  - Free tier: 20 analyses/day
  - Premium: $4.99/month (unlimited analyses + AI poet)
  - Enterprise: Custom pricing (API access, SLA)
```

#### ❌ API Access / Developer Platform
```yaml
Out of Scope (MVP):
  - Public API with API keys
  - Rate limiting per API key
  - API documentation portal
  - SDKs (Python, JavaScript)
  - Webhooks

Rationale:
  - MVP has API (internal only)
  - Public API requires support burden
  - Pricing model complexity
  - Documentation effort (3-4 weeks)

Deferred To: Phase 3+ (Month 9+)
Priority: MEDIUM (B2B opportunity)

Requirements:
  - 10,000+ MAU (proves demand)
  - Developer interest (validated)
  - Support resources (documentation, forum)
```

---

### 8. Performance & Scale

#### ❌ Real-Time Collaboration
```yaml
Out of Scope:
  - Multiple users editing same verse
  - Live cursor positions
  - WebSocket connections
  - Operational transforms (like Google Docs)

Rationale:
  - Complex distributed systems problem
  - Low value (poetry analysis is solo activity)
  - Infrastructure cost (WebSockets don't scale cheaply)

Deferred To: Never (not needed)
Priority: NONE
```

#### ❌ Offline Mode / PWA
```yaml
Out of Scope (MVP):
  - Progressive Web App
  - Offline analysis capability
  - Service Workers
  - Desktop app (Electron)

Rationale:
  - MVP is web-only
  - Prosody engine runs server-side (can't be fully offline)
  - PWA adds complexity for minimal benefit

Deferred To: Phase 3+ (if mobile usage > 60%)
Priority: LOW-MEDIUM
```

---

## ✅ How to Use This Document

### When a Feature Is Requested:

```yaml
Step 1: Check if it's in NON_GOALS.md
  - If YES: Politely decline with rationale from this doc
  - If NO: Go to Step 2

Step 2: Check if it's in MVP plan (BAHR_AI_POET_MASTER_PLAN.md)
  - If YES: Confirm it's scheduled and provide timeline
  - If NO: Go to Step 3

Step 3: Evaluate the feature request
  - Impact: High / Medium / Low
  - Effort: Days / Weeks / Months
  - Alignment: Core / Adjacent / Unrelated
  - User demand: Proven / Speculative

Step 4: Make decision
  - If Core + High Impact + < 1 week: Consider adding to current phase
  - If Adjacent + Medium Impact: Add to DEFERRED_FEATURES.md with estimated phase
  - If Unrelated OR > 1 month effort: Add to NON_GOALS.md
  - Always document decision and rationale

Step 5: Communicate decision
  - GitHub issue: Link to relevant doc
  - User email: Polite explanation + alternative if available
  - Public roadmap: Show what IS being built instead
```

### Reviewing This Document:

**Frequency:** Every 3 months or after major milestone

**Questions to Ask:**
- Has market changed? (e.g., sudden demand for dialect analysis)
- Has technology changed? (e.g., better OCR makes it feasible)
- Has competition changed? (e.g., competitor launches feature we said "never")
- Have user needs changed? (e.g., 80% of requests are for X)

**If Yes to Any:**
- Re-evaluate the non-goal
- Move to DEFERRED_FEATURES.md if now viable
- Update rationale and priority

---

## 📊 Feature Request Statistics (Track Post-Launch)

Use this section to track how often non-goals are requested:

```yaml
# Update monthly after launch

Most Requested Non-Goals:
  1. AI Poetry Generation: [X requests]
  2. Dialect Support: [X requests]
  3. Rhyme Analysis: [X requests]
  4. Social Features: [X requests]
  5. Mobile App: [X requests]

Re-Evaluation Triggers:
  - If any non-goal gets > 100 requests: Consider moving to roadmap
  - If any non-goal is 50%+ of feedback: High priority for Phase 2+
```

---

## 💡 The "What About..." Response Template

When users ask: "What about [feature X]?"

**Good Response:**
```
Thank you for the suggestion! [Feature X] is currently out of scope
for our MVP because [rationale from this doc]. We're focused on
delivering the best prosody analysis experience first.

[Feature X] is tracked in our roadmap as a potential Phase
[2/3/4] addition, planned for [rough timeframe].

In the meantime, you can [workaround/alternative if available].

We appreciate your feedback and will re-evaluate based on user demand!
```

**Bad Response:**
```
"Maybe later."
"Good idea, we'll think about it."
"Not planned."  <-- No explanation, user feels dismissed
```

---

## 🎯 The Scope Discipline Mantra

**Repeat daily during development:**

> "Every feature deferred is time saved for the features that matter most.
> Saying no to good ideas makes room for great execution of essential ideas."

**Remember:**
- Shipped 10 features at 50% quality = Failure
- Shipped 5 features at 95% quality = Success
- **BAHR MVP = 1 feature (prosody analysis) at 95% quality**

---

**Last Updated:** November 8, 2025
**Next Review:** Month 3 (Post-Launch) or after 1000 users
**Version:** 1.0

**Reminder to Future Self:** You documented these non-goals for a reason. Trust past you. Focus on shipping the MVP.
