# 🚨 WEEK 1 CRITICAL CHECKLIST - Read Before Starting!
## Expert Review Feedback Integration Summary

**Date:** November 8, 2025  
**Status:** Documentation Updated Post-Review  
**Action Required:** Review this file before beginning Week 1 implementation

---

## ⚡ TOP 5 CRITICAL ACTIONS (Week 1 Day 1)

### 1️⃣ **TEST CAMeL Tools on M1/M2 IMMEDIATELY** 🔴

**Priority:** CRITICAL - First hour of Day 1  
**Risk:** Complete blocker if incompatible

```bash
# Test 3 approaches in order (30-60 minutes):

# Approach 1: ARM64 native (try first)
arch -arm64 python3.11 -m pip install camel-tools==1.5.2
python3 -c "from camel_tools.utils.normalize import normalize_unicode; print('✅ ARM64 works!')"

# Approach 2: Rosetta x86_64 (if ARM64 fails)
arch -x86_64 python3.11 -m pip install camel-tools==1.5.2  
python3 -c "from camel_tools.utils.normalize import normalize_unicode; print('✅ Rosetta works!')"

# Approach 3: Docker linux/amd64 (fallback)
docker run --platform=linux/amd64 -it python:3.11-slim bash
pip install camel-tools==1.5.2
python -c "from camel_tools.utils.normalize import normalize_unicode; print('✅ Docker works!')"
```

**If all fail:** Use PyArabic only for MVP, defer CAMeL Tools to Phase 2  
**Document:** Which approach worked in `PROGRESS_LOG.md`

---

### 2️⃣ **START DATASET LABELING (Week 1 Evenings)** 📝

**Why:** Frontload time-consuming manual work  
**Goal:** 10-20 gold standard verses by end of Week 1

```yaml
Week 1 Evening Schedule (2 hours/evening):
  Monday Eve: Collect 5 verses from معلقات (Mu'allaqat)
  Tuesday Eve: Collect 5 verses from ديوان المتنبي
  Wednesday Eve: Label 10 verses (meter, taqti', source)
  Thursday Eve: Verify labels (cross-reference with عروض books)
  Friday Eve: Document labeling decisions in DATASET_SPEC.md

Quality Over Quantity:
  - Focus on well-known classical poems
  - Triple-verify meter labels
  - These 10-20 will be your regression test set
```

---

### 3️⃣ **ACCEPT REALISTIC ACCURACY TARGETS** 🎯

**Changed:** 85%+ → 70-75% for MVP  
**Reason:** Classical Arabic prosody has 100+ edge cases

```yaml
Revised Accuracy Goals:
  Week 5 (Initial Engine): > 65% ✅
  Week 7 (After Tuning): > 75% ✅  
  Week 12 (Beta): > 80% ✅
  6 Months: > 90% 🎯 (with ML model)

Pivot Point (Week 5):
  IF accuracy < 65%:
    THEN reduce scope from 16 meters → 8 meters
    Focus: طويل، بسيط، كامل، وافر، رجز، رمل، خفيف، متقارب
```

**See:** `docs/technical/PERFORMANCE_TARGETS.md` (updated)

---

### 4️⃣ **IMPLEMENT SECURITY FROM DAY 1** 🔒

**Priority:** HIGH - Week 1 setup  
**Risk:** Technical debt if deferred

```yaml
Week 1 Security Checklist:
  - ✅ Password hashing with bcrypt (cost factor 12)
  - ✅ JWT tokens with 30-min expiration
  - ✅ SQL injection prevention (use SQLAlchemy ORM)
  - ✅ XSS protection (escape Arabic text)
  - ✅ Rate limiting (100 req/hour per IP)
  - ✅ Environment variables (.env, never commit secrets)

Week 6-7 Security (Deferred):
  - Content Security Policy headers
  - HSTS (production only)
  - Backup encryption
  - Audit logging
```

**See:** `docs/technical/SECURITY.md` (NEW FILE)

---

### 5️⃣ **WRITE TESTS DURING DEVELOPMENT (TDD)** ✅

**Priority:** HIGH - Prevents Week 9-10 crunch  
**Strategy:** Test as you build, not after

```yaml
Daily Testing Habit:
  After writing each function:
    1. Write 2-3 unit tests (happy path + edge case)
    2. Run tests locally
    3. Commit with passing tests
  
  Example (Week 3 - Normalization):
    - Write normalize_text() function
    - Immediately write test_normalize_text()
    - Test cases: standard text, with diacritics, with shadda, edge cases
    - Target: 70%+ coverage from Day 1

Benefits:
  - Week 9-10 becomes "integration + E2E" not "write all tests"
  - Catch bugs early (easier to fix)
  - Refactor with confidence
```

---

## 📊 TIMELINE ADJUSTMENT: 14 → 15 Weeks (Conservative)

**Rationale:** Prosody engine is the unknown unknown

```yaml
Conservative Timeline (Recommended for Solo Dev):
  Week 1-2: Setup + Dataset ✅ (unchanged)
  Week 3-6: Prosody Engine ⚠️ (+1 week from original)
    - Week 3: Normalization + Segmentation
    - Week 4: Pattern Matching + 100 edge cases
    - Week 5: Meter Detection + confidence scoring
    - Week 6: Polish + optimization
  Week 7: API Integration ✅
  Week 8-9: Polish + Optimization ✅
  Week 10-11: Testing ✅
  Week 12-13: Beta ✅
  Week 14-15: Launch + Buffer ✅

Your Original 14-Week Plan:
  - Still achievable IF:
    ✅ CAMeL Tools works Day 1 (no M1/M2 issues)
    ✅ Accept 70-75% accuracy (not 85%)
    ✅ Write tests during development (not after)
    ✅ Work 6+ hours/day consistently

Decision Point:
  - Start with 14-week plan
  - Week 5 pivot: If behind, extend to 15 weeks
  - Use Week 14/15 as buffer (don't panic if needed)
```

**See:** `docs/planning/PROJECT_TIMELINE.md` (will update)

---

## 🛠️ NEW TECHNICAL SPECIFICATIONS

### Prosody Engine - Regex Patterns Required

**Must create in Week 3 Day 1:**

```python
# backend/app/core/prosody/prosody_patterns.py

import re

# Syllable patterns (مقاطع)
PATTERNS = {
    'CV': r'[consonant][short_vowel]',          # مقطع قصير مفتوح
    'CVC': r'[consonant][short_vowel][consonant]',  # مقطع متوسط مغلق
    'CVV': r'[consonant][long_vowel]',          # مقطع طويل مفتوح (madd)
    'CVVC': r'[consonant][long_vowel][consonant]',  # مقطع طويل مغلق
}

# Shadda decomposition
SHADDA_PATTERN = r'([^\u0640-\u064F])\u0651'  # حرف + شدة
SHADDA_REPLACEMENT = r'\1\u0652\1'  # حرف ساكن + حرف متحرك

# Tanween pause (end of verse)
TANWEEN_FATHA = r'([^\u0640-\u064F])\u064B'  # ـً
TANWEEN_PAUSE_FATHA = r'\1\u0627'  # → alef
TANWEEN_DAMMA_KASRA = r'([^\u0640-\u064F])[\u064C\u064D]'  # ـٌ or ـٍ
TANWEEN_PAUSE_OTHER = r'\1\u0652'  # → sukun

# Madd (long vowels)
MADD_ALEF = r'[\u064E]\u0627'  # فتحة + ا
MADD_WAW = r'[\u064F]\u0648'   # ضمة + و
MADD_YA = r'[\u0650]\u064A'    # كسرة + ي
```

**See:** `docs/technical/PROSODY_ENGINE.md` (will update with full spec)

---

### Era Detection Strategy (MVP)

**Decision:** Manual user input for MVP, auto-detection in Phase 2

```python
# MVP Approach (Week 3):
class ProsodyAnalyzer:
    def analyze(self, text: str, era: str = "classical"):
        """
        era: "classical" or "modern"
        User must specify via API parameter
        """
        if era == "classical":
            return self.classical_analysis(text)
        else:
            return self.modern_analysis(text)  # Phase 2

# Phase 2 Approach (Future):
def detect_era(text: str) -> str:
    """
    Auto-detect based on:
    - Vocabulary (classical words like قفا، نبك)
    - Meter strictness
    - Diacritics presence
    """
    pass  # Implement later
```

---

### Diacritics Handling (Two Scenarios)

**Challenge:** Input might have diacritics OR not

```python
# Scenario 1: User input WITHOUT diacritics (common)
input_text = "قفا نبك من ذكرى حبيب ومنزل"
# → Use CAMeL Tools to add diacritics
# → Then analyze

# Scenario 2: Classical text WITH diacritics (from books)
input_text = "قِفا نَبْكِ مِنْ ذِكْرى حَبيبٍ وَمَنْزِلِ"
# → Remove diacritics
# → Normalize
# → Re-apply for display (optional)

# Your normalize() function must handle BOTH!
```

---

## 📦 RESOURCE CONSTRAINTS (Production)

### Backend Memory Budget:

```yaml
Target: 512MB container ✅ MVP acceptable
Breakdown:
  - Python runtime: ~150MB
  - CAMeL Tools models: ~200MB
  - Per-request overhead: ~10MB
  - Headroom: ~150MB

Action:
  - Pre-load CAMeL Tools models at startup
  - Avoid lazy loading (spikes memory)
  - Monitor memory with Prometheus
  - Alert if > 700MB (75% of 1GB safety limit)
```

### Frontend Bundle Size:

```yaml
Target: < 300KB (gzipped) ✅ MVP acceptable
Ideal: < 200KB 🎯

Breakdown:
  - React + Next.js: ~100KB
  - UI components: ~50KB
  - Arabic utils: ~20KB
  - API client: ~30KB
  - Budget for features: ~100KB

Optimization:
  - Code splitting (Next.js automatic)
  - Dynamic imports for heavy components
  - Tree-shaking
  - Font subsetting (use only needed Arabic glyphs)
```

### Database Query Limits:

```yaml
Analysis Lookup (by ID): < 10ms ✅
User Auth Query: < 20ms ✅
JOIN (user + analysis): < 50ms ✅
Full-text Search (Arabic): < 500ms ⚠️

Must Index:
  - All foreign keys
  - created_at (DESC) for pagination
  - JSONB columns (GIN index)
  - Arabic full-text (GIN to_tsvector)
```

**See:** `docs/technical/PERFORMANCE_TARGETS.md` (updated)

---

## 🧪 FRONTEND RTL TESTING (Week 7)

**Create RTL Stress Test Page:**

```tsx
// Week 7 Day 1: Create pages/test/rtl-stress.tsx

const RTLStressTest = () => {
  return (
    <div dir="rtl">
      {/* Test Case 1: Long verses with diacritics */}
      <p className="text-2xl">
        قِفَا نَبْكِ مِنْ ذِكْرَىٰ حَبِيبٍ وَمَنْزِلِ بِسِقْطِ اللِّوَىٰ بَيْنَ الدَّخُولِ فَحَوْمَلِ
      </p>
      
      {/* Test Case 2: Mixed AR/EN */}
      <p>
        This is English then العربية then back to English
      </p>
      
      {/* Test Case 3: Input fields */}
      <input type="text" placeholder="اكتب شعراً هنا" dir="rtl" />
      
      {/* Test Case 4: Absolute positioning */}
      <div className="relative">
        <span className="absolute right-0">يمين</span>
      </div>
    </div>
  );
};

// Test on: Safari, Chrome, Firefox (macOS)
```

**See:** `docs/technical/FRONTEND_GUIDE.md` (will update)

---

## 🗄️ REDIS CACHING STRATEGY

**Configuration:**

```yaml
What to Cache:
  - Meter definitions: TTL = ∞ (static data, use PERSIST)
  - Analysis results: TTL = 7 days
  - User sessions: TTL = 30 minutes
  - Rate limiting counters: TTL = 1 hour

Cache Invalidation:
  - Algorithm version change: FLUSHALL
  - User logout: DEL user:{id}:session
  - Manual: Admin endpoint to clear specific keys

Memory:
  - Limit: 256MB (MVP)
  - Eviction: allkeys-lru
  - Monitor: Cache hit ratio (target > 80%)
```

**Implementation:**

```python
# backend/app/core/cache/redis_cache.py

class RedisCache:
    def __init__(self, redis_client):
        self.redis = redis_client
    
    async def cache_analysis(self, text_hash: str, result: dict, ttl: int = 604800):
        """Cache analysis result for 7 days"""
        key = f"analysis:{text_hash}"
        await self.redis.setex(key, ttl, json.dumps(result))
    
    async def get_cached_analysis(self, text_hash: str) -> Optional[dict]:
        """Retrieve cached analysis"""
        key = f"analysis:{text_hash}"
        cached = await self.redis.get(key)
        return json.loads(cached) if cached else None
    
    async def cache_meter_definitions(self, meters: list[dict]):
        """Cache meter definitions (permanent)"""
        key = "meters:all"
        await self.redis.set(key, json.dumps(meters))
        await self.redis.persist(key)  # Never expire
```

**See:** `docs/technical/BACKEND_API.md` (will update)

---

## 🔐 ARABIC FULL-TEXT SEARCH NORMALIZATION

**Issue:** PostgreSQL's `arabic` text search config is basic

**Solution (MVP):**

```sql
-- Pre-normalize all searchable text
CREATE INDEX idx_analyses_search_normalized ON analyses 
  USING GIN(to_tsvector('arabic', 
    -- Normalize before indexing:
    regexp_replace(  -- Remove diacritics
      translate(  -- Normalize hamza
        original_text,
        'أإآؤئء', 'اااووي'
      ),
      '[\u064B-\u0652]', '', 'g'
    )
  ));

-- Query must also normalize input:
SELECT * FROM analyses 
WHERE to_tsvector('arabic', normalized_text) @@ 
      plainto_tsquery('arabic', normalize(user_query));
```

**Phase 2:** Consider Elasticsearch for advanced Arabic search

**See:** `docs/technical/DATABASE_SCHEMA.md` (will update)

---

## 📁 NEW FILES CREATED

```
docs/technical/
└── SECURITY.md ✨ NEW
    - Password hashing (bcrypt, cost 12)
    - JWT security (rotation, blacklist)
    - SQL injection prevention
    - XSS protection for Arabic text
    - Rate limiting strategy
    - CSP headers
    - Backup encryption
```

## 📝 FILES UPDATED

```
docs/technical/
├── PERFORMANCE_TARGETS.md ✅ UPDATED
│   - Revised accuracy targets (65% → 75% → 80%)
│   - Backend memory limits (512MB MVP)
│   - CAMeL Tools memory profile (~200MB)
│   - Database query benchmarks (< 50ms)
│   - Frontend bundle size (< 300KB)
│   - Redis caching details
│
└── DEPLOYMENT_GUIDE.md ✅ UPDATED
    - Disaster recovery section
    - Backup strategy (daily, 7-day retention)
    - RTO: 4 hours (MVP), 1 hour (production)
    - RPO: 24 hours (MVP), 1 hour (production)
    - Restore procedures
    - Monitoring alerts
```

## 📝 FILES TO UPDATE (In Progress)

```
docs/planning/
└── PROJECT_TIMELINE.md ⏳ PENDING
    - Add 15-week conservative option
    - Frontload dataset labeling to Week 1
    - Emphasize TDD approach
    - Week 5 pivot point

docs/technical/
├── PROSODY_ENGINE.md ⏳ PENDING
│   - Add prosody_patterns.py specification
│   - Era detection strategy (MVP vs Phase 2)
│   - Dual diacritics handling
│
├── BACKEND_API.md ⏳ PENDING
│   - Redis caching strategy
│   - Cache TTL values
│   - Eviction policy
│
├── FRONTEND_GUIDE.md ⏳ PENDING
│   - RTL stress testing checklist
│   - Browser testing matrix
│   - Diacritics overflow handling
│
└── DATABASE_SCHEMA.md ⏳ PENDING
    - Arabic full-text search normalization
    - Elasticsearch note for Phase 2

docs/phases/
├── PHASE_0_SETUP.md ⏳ PENDING
│   - M1/M2 CAMeL Tools testing (Day 1 priority)
│   - Week 1 evening dataset labeling
│
└── PHASE_1_MVP.md ⏳ PENDING
    - Revised accuracy targets (70-75%)
    - 8-meter fallback option
    - Week 5 pivot point
```

---

## ⚠️ CRITICAL REMINDERS

### Week 1 Priorities:

1. ✅ Test CAMeL Tools compatibility (Day 1, Hour 1)
2. ✅ Start dataset labeling (10-20 verses by end of week)
3. ✅ Implement basic security (password hashing, JWT, rate limiting)
4. ✅ Set up monitoring (Grafana + Prometheus basics)
5. ✅ Create `.env.example` file (document all env vars)

### Mindset Adjustments:

1. **Accept 70-75% accuracy for MVP** - Don't chase perfection
2. **Write tests as you code** - TDD saves time later
3. **Document as you go** - Future you will thank you
4. **Use Week 14 buffer without guilt** - It's built in for a reason
5. **Pivot at Week 5 if needed** - Reduce from 16 → 8 meters is OK

### Red Flags to Watch:

1. Week 3: Normalization taking > 2 days → simplify edge cases
2. Week 5: Accuracy < 65% → reduce meter scope
3. Week 7: API integration taking > 3 days → use mock data first
4. Week 10: Test coverage < 60% → you skipped TDD, catch up now
5. Any week: Working < 5 hours/day → timeline will slip

---

## 📞 WHAT TO DO IF STUCK

### CAMeL Tools Won't Install (Day 1):
```bash
# Emergency fallback: Use PyArabic only
pip install pyarabic
# Defer CAMeL Tools to Phase 2
# Document decision in PROGRESS_LOG.md
```

### Accuracy Stuck at 60% (Week 5):
```yaml
Actions:
  1. Check dataset quality (are labels correct?)
  2. Reduce scope to 8 meters (most common)
  3. Focus on classical poetry only (ignore modern)
  4. Document known limitations
  5. Plan ML model for Phase 2
```

### Running Behind Schedule (Any Week):
```yaml
Options:
  1. Use Week 14 buffer (built in for this)
  2. Reduce features (check DEFERRED_FEATURES.md)
  3. Accept lower accuracy (70% vs 75%)
  4. Skip nice-to-haves (pretty visualizations can wait)
  5. Extend to Week 15 (still within reasonable range)
```

---

## ✅ FINAL PRE-WEEK-1 CHECKLIST

```yaml
Before starting Day 1:
  - [ ] Read this entire document
  - [ ] Review SECURITY.md (new file)
  - [ ] Review updated PERFORMANCE_TARGETS.md
  - [ ] Review updated DEPLOYMENT_GUIDE.md
  - [ ] Understand revised accuracy targets (70-75%)
  - [ ] Accept 14-week timeline (15-week backup plan)
  - [ ] Mental prep: TDD from Day 1
  - [ ] Mental prep: Manual labeling is part of Week 1
  - [ ] Hardware ready: Mac, 8GB+ RAM, 20GB disk space
  - [ ] Tools installed: Homebrew, Git, Python, Node, Docker

Day 1 Hour 1:
  - [ ] Test CAMeL Tools installation (3 approaches)
  - [ ] Document which approach worked
  - [ ] If all fail, pivot to PyArabic-only plan

Day 1 Evening:
  - [ ] Collect first 5 classical verses
  - [ ] Start labeling (meter, source, poet)
```

---

**YOU ARE READY! 🚀**

Your documentation is excellent. The 14-week plan is ambitious but achievable with the adjustments above. Remember:

- **Progress > Perfection**
- **Test as you code**
- **Document as you go**
- **Pivot when needed**

Good luck with Week 1! Update `PROGRESS_LOG.md` daily to track progress.

**Last Updated:** November 8, 2025 (Post Expert Review)
