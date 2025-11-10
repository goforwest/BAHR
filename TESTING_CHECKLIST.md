# BAHR Platform - Testing & Verification Checklist
## Comprehensive Quality Assurance for Each Phase

---

## How to Use This Checklist

- ✅ Check items as you complete them
- 🔄 Re-test if changes are made to related code
- ⚠️ Mark items that partially pass or need attention
- ❌ Note failures and track fixes

---

## Phase 0: Pre-Development Setup

### Project Structure
- [ ] Backend directory structure created with all subdirectories
- [ ] Frontend directory structure matches Next.js 14 conventions
- [ ] All `__init__.py` files present in Python packages
- [ ] `.gitignore` covers Python, Node, and IDE files
- [ ] `README.md` created with project overview

### Docker Environment
- [ ] `docker-compose.yml` file exists
- [ ] PostgreSQL service starts successfully
- [ ] Redis service starts successfully
- [ ] Health checks pass for both services
- [ ] Services restart after `docker-compose restart`

**Test Commands:**
```bash
cd BAHR
docker-compose up -d
docker-compose ps  # Both should show "Up"
docker exec bahr_postgres psql -U bahr_user -d bahr_db -c "SELECT 1;"  # Should return 1
docker exec bahr_redis redis-cli ping  # Should return PONG
```

### Backend Setup
- [ ] Virtual environment created
- [ ] All requirements installed from `requirements.txt`
- [ ] FastAPI imports successfully: `python -c "import fastapi"`
- [ ] SQLAlchemy imports successfully: `python -c "import sqlalchemy"`
- [ ] Pydantic imports successfully: `python -c "import pydantic"`
- [ ] `.env` file created from `.env.example`
- [ ] `JWT_SECRET_KEY` is set and not default value

**Test Commands:**
```bash
cd backend
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip list | grep fastapi  # Should show FastAPI version
python -c "from app.config import settings; print(settings.PROJECT_NAME)"
```

### Frontend Setup
- [ ] Node.js version is 18+: `node --version`
- [ ] All npm packages installed
- [ ] Next.js builds successfully: `npm run build`
- [ ] TypeScript compiles without errors: `npm run type-check`
- [ ] Tailwind CSS configured with RTL support
- [ ] Arabic fonts (Cairo, Amiri) configured
- [ ] `.env.local` file created with API URL

**Test Commands:**
```bash
cd frontend
node --version  # Should be v18+
npm list | grep next  # Should show Next.js version
npm run build  # Should complete without errors
```

### Base Application
- [ ] FastAPI server starts: `uvicorn app.main:app --reload`
- [ ] Root endpoint returns Arabic greeting: `curl http://localhost:8000/`
- [ ] Health endpoint returns healthy status
- [ ] Swagger UI accessible at `http://localhost:8000/docs`
- [ ] Next.js dev server starts: `npm run dev`
- [ ] Home page displays Arabic text correctly
- [ ] Home page shows RTL layout

**Visual Checks (Browser):**
- [ ] Arabic text renders correctly (not squares/question marks)
- [ ] Text flows right-to-left
- [ ] Cairo font loaded (check DevTools Network tab)
- [ ] Amiri font loaded
- [ ] No console errors in browser

---

## Phase 1, Week 1-2: Prosody Engine Core

### Text Normalization Module

**Unit Tests:**
- [ ] `test_removes_fatha` passes
- [ ] `test_removes_damma` passes
- [ ] `test_removes_kasra` passes
- [ ] `test_removes_shadda` passes
- [ ] `test_removes_sukun` passes
- [ ] `test_removes_tanween` passes
- [ ] `test_normalizes_hamza_on_alef` passes
- [ ] `test_normalizes_hamza_on_waw` passes
- [ ] `test_normalizes_hamza_on_ya` passes
- [ ] `test_normalizes_alef_maksura` passes
- [ ] `test_removes_tatweel` passes
- [ ] `test_raises_on_empty_text` passes
- [ ] `test_raises_on_non_arabic` passes

**Manual Tests:**
```python
from app.core.normalization import normalize_arabic_text

# Test 1: Diacritics removal
text = "مَرْحَبًا"
result = normalize_arabic_text(text, remove_tashkeel=True)
assert result == "مرحبا"  # ✅ or ❌

# Test 2: Hamza normalization
text = "أَحْمَد"
result = normalize_arabic_text(text)
assert "ا" in result  # ✅ or ❌

# Test 3: Preserves tashkeel by default
text = "كَتَبَ"
result = normalize_arabic_text(text, remove_tashkeel=False)
assert "َ" in result  # ✅ or ❌
```

**Code Quality:**
- [ ] All functions have docstrings
- [ ] All functions have type hints
- [ ] Code passes Black formatting
- [ ] Code passes Flake8 linting
- [ ] Test coverage ≥80%

**Coverage Check:**
```bash
pytest tests/core/test_normalization.py --cov=app.core.normalization --cov-report=term-missing
# Should show ≥80% coverage
```

---

### Phonetic Analysis Module

**Unit Tests:**
- [ ] `test_long_vowel_detection` passes
- [ ] `test_sukun_detection` passes
- [ ] `test_simple_word_with_tashkeel` passes
- [ ] `test_word_with_sukun` passes
- [ ] `test_word_with_shadda` passes
- [ ] `test_word_with_long_vowel` passes
- [ ] `test_all_short_vowels` passes
- [ ] `test_with_long_vowel` passes

**Manual Tests:**
```python
from app.core.phonetics import extract_phonemes, phonemes_to_pattern

# Test 1: Simple word
phonemes = extract_phonemes("كَتَبَ", has_tashkeel=True)
assert len(phonemes) == 3  # ✅ or ❌
assert all(p.vowel == 'a' for p in phonemes)  # ✅ or ❌

# Test 2: Pattern generation
pattern = phonemes_to_pattern(phonemes)
assert '/' in pattern  # ✅ or ❌

# Test 3: Long vowel
phonemes = extract_phonemes("كِتَاب", has_tashkeel=True)
long_vowels = [p for p in phonemes if p.is_long_vowel()]
assert len(long_vowels) >= 1  # ✅ or ❌
```

**Code Quality:**
- [ ] Phoneme dataclass has proper methods
- [ ] All functions have docstrings
- [ ] Type hints present
- [ ] Test coverage ≥80%

---

### Taqti3 Algorithm

**Unit Tests:**
- [ ] `test_simple_pattern` passes
- [ ] `test_empty_pattern` passes
- [ ] `test_raises_on_empty_verse` passes
- [ ] `test_returns_string` passes

**Manual Tests:**
```python
from app.core.taqti3 import perform_taqti3

# Test 1: Known verse (الطويل)
verse = "إذا غامَرتَ في شَرَفٍ مَرومِ"
result = perform_taqti3(verse)
print(f"Taqti3: {result}")
# Expected: Contains "فعولن" and "مفاعيلن"  # ✅ or ❌

# Test 2: Different bahr (الكامل)
verse = "أَلا لَيتَ الشَبابَ يَعودُ يَوماً"
result = perform_taqti3(verse)
print(f"Taqti3: {result}")
# Expected: Contains "متفاعلن"  # ✅ or ❌
```

**Integration Test:**
- [ ] Normalization → Phonetics → Taqti3 pipeline works end-to-end
- [ ] Handles verses with diacritics
- [ ] Handles verses without diacritics (infers vowels)

---

### Bahr Detection

**Unit Tests:**
- [ ] `test_initialization` passes
- [ ] `test_calculate_similarity_exact_match` passes
- [ ] `test_calculate_similarity_different` passes
- [ ] `test_detect_bahr_returns_bahrinfo` passes
- [ ] `test_detect_bahr_returns_none_for_invalid` passes

**Manual Tests:**
```python
from app.core.bahr_detector import BahrDetector

detector = BahrDetector()

# Test 1: الطويل
verse = "إذا غامَرتَ في شَرَفٍ مَرومِ"
result = detector.analyze_verse(verse)
assert result is not None  # ✅ or ❌
assert result.name_ar == "الطويل"  # ✅ or ❌
assert result.confidence >= 0.7  # ✅ or ❌
print(f"Detected: {result.name_ar} (confidence: {result.confidence})")

# Test 2: الكامل
verse = "أَلا لَيتَ الشَبابَ يَعودُ يَوماً"
result = detector.analyze_verse(verse)
assert result.name_ar == "الكامل"  # ✅ or ❌

# Test 3: الوافر
verse = "يَقولونَ لي فيكَ انقِباضٌ وإِنَّما"
result = detector.analyze_verse(verse)
assert result.name_ar == "الوافر"  # ✅ or ❌

# Test 4: الرمل
verse = "يا خَليلَيَّ اِصحَبا وَاِسمَعا"
result = detector.analyze_verse(verse)
assert result.name_ar == "الرمل"  # ✅ or ❌
```

**Code Quality:**
- [ ] BahrDetector class properly structured
- [ ] Similarity calculation uses difflib correctly
- [ ] Confidence threshold (0.7) is appropriate
- [ ] All 4 bahrs defined in BAHRS_DATA

---

### Accuracy Testing

**Prerequisites:**
- [ ] Test dataset created: `tests/fixtures/test_verses.json`
- [ ] At least 50 verses in dataset
- [ ] All 4 bahrs represented (10+ verses each)
- [ ] Verses have correct metadata (poet, bahr, expected_tafail)

**Accuracy Tests:**
- [ ] `test_overall_accuracy` passes (≥90%)
- [ ] `test_accuracy_by_bahr` passes (each bahr ≥80%)

**Run Accuracy Test:**
```bash
pytest tests/core/test_accuracy.py -v -s
```

**Expected Output:**
```
Accuracy: 92.0% (46/50)

Accuracy by Bahr:
  الطويل: 95.0% (19/20)
  الكامل: 90.0% (9/10)
  الوافر: 87.5% (7/8)
  الرمل: 91.7% (11/12)

PASSED
```

**If Accuracy <90%:**
- [ ] Identify failed verses
- [ ] Debug phonetic analysis
- [ ] Check tafa'il pattern matching
- [ ] Adjust similarity threshold
- [ ] Add missing tafa'il variations
- [ ] Re-run test until ≥90%

**Critical Checklist:**
- [ ] **Overall accuracy ≥90%** ✅ or ❌
- [ ] **Each bahr accuracy ≥80%** ✅ or ❌
- [ ] False positives <5% (wrong bahr detected)
- [ ] False negatives <5% (no bahr detected)

---

## Phase 1, Week 3-4: API & Database

### Database Schema

**Migration Tests:**
- [ ] Alembic initialized: `migrations/` directory exists
- [ ] Initial migration created
- [ ] Migration runs successfully: `alembic upgrade head`
- [ ] Tables created in PostgreSQL

**Verify Tables:**
```bash
docker exec bahr_postgres psql -U bahr_user -d bahr_db -c "\dt"
```

**Expected tables:**
- [ ] `users` table exists
- [ ] `bahrs` table exists
- [ ] `tafa3il` table exists
- [ ] `poems` table exists
- [ ] `verses` table exists
- [ ] `alembic_version` table exists

**Schema Validation:**
```sql
-- Check users table
docker exec bahr_postgres psql -U bahr_user -d bahr_db -c "\d users"
-- Should show: id, email, username, password_hash, level, xp, coins, etc.

-- Check bahrs table
docker exec bahr_postgres psql -U bahr_user -d bahr_db -c "\d bahrs"
-- Should show: id, name_ar, name_en, pattern, description, example_verse
```

**Foreign Keys:**
- [ ] `verses.poem_id` references `poems.id`
- [ ] `poems.user_id` references `users.id`
- [ ] `tafa3il.bahr_id` references `bahrs.id`

**Indexes:**
- [ ] `users.email` has unique index
- [ ] `users.username` has unique index
- [ ] `bahrs.name_ar` has unique index

---

### Seed Data

**Bahrs Seeding:**
- [ ] Seed script exists: `scripts/seed_bahrs.py`
- [ ] Script runs without errors
- [ ] All 16 bahrs inserted

**Verify Seeded Data:**
```sql
docker exec bahr_postgres psql -U bahr_user -d bahr_db -c "SELECT COUNT(*) FROM bahrs;"
-- Should return: 16

docker exec bahr_postgres psql -U bahr_user -d bahr_db -c "SELECT name_ar FROM bahrs ORDER BY id;"
-- Should list all 16 bahr names
```

**Data Quality:**
- [ ] All bahrs have `name_ar` (Arabic name)
- [ ] All bahrs have `name_en` (English name)
- [ ] All bahrs have `pattern` (tafa'il pattern)
- [ ] All bahrs have `description` (non-empty)
- [ ] All bahrs have `example_verse` (non-empty)

---

### Analyze API Endpoint

**Endpoint Tests:**
- [ ] Swagger UI shows `/api/v1/analyze` endpoint
- [ ] Endpoint accepts POST requests
- [ ] Request schema documented
- [ ] Response schema documented

**Manual API Tests:**
```bash
# Test 1: Valid verse
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "إذا غامَرتَ في شَرَفٍ مَرومِ"}' \
  | jq .
# Expected: 200 OK, JSON with taqti3, bahr, score

# Test 2: Invalid input (empty)
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": ""}' \
  | jq .
# Expected: 400 Bad Request, error message

# Test 3: Invalid input (no Arabic)
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello World"}' \
  | jq .
# Expected: 400 Bad Request, error about Arabic characters

# Test 4: Verse without diacritics
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "اذا غامرت في شرف مروم"}' \
  | jq .
# Expected: 200 OK, should still work (inferred vowels)
```

**Response Validation:**
- [ ] Response has `text` field (original verse)
- [ ] Response has `taqti3` field (tafa'il string)
- [ ] Response has `bahr` object (name_ar, name_en, confidence)
- [ ] Response has `score` field (0-100)
- [ ] Response has `errors` array (empty for valid verse)
- [ ] Response has `suggestions` array (empty for now)

**Performance:**
- [ ] First request completes in <500ms
- [ ] Cached request completes in <50ms
- [ ] No memory leaks (run 100 requests)

---

### Redis Caching

**Cache Functionality:**
- [ ] Redis connection established on startup
- [ ] Cache key generated correctly (SHA256 hash)
- [ ] First request caches result
- [ ] Second identical request retrieves from cache
- [ ] Cache TTL is 24 hours (86400 seconds)

**Cache Tests:**
```bash
# Test cache hit
# 1. Make first request (cache miss)
time curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "إذا غامَرتَ في شَرَفٍ مَرومِ"}'
# Note the time

# 2. Make second request (cache hit)
time curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "إذا غامَرتَ في شَرَفٍ مَرومِ"}'
# Should be significantly faster

# 3. Check Redis
docker exec bahr_redis redis-cli KEYS "analysis:*"
# Should show cached keys
```

**Cache Invalidation:**
- [ ] Different verse creates different cache key
- [ ] Same verse with/without diacritics uses same key (normalized)
- [ ] Cache expires after 24 hours (manually test with short TTL)

---

### Integration Tests

**Test Suite:**
- [ ] `test_analyze_valid_verse` passes
- [ ] `test_analyze_cached_response` passes
- [ ] `test_analyze_invalid_input_empty` passes
- [ ] `test_analyze_invalid_input_no_arabic` passes
- [ ] `test_analyze_verse_without_diacritics` passes

**Run Integration Tests:**
```bash
pytest tests/api/v1/test_analyze.py -v
```

**Coverage:**
- [ ] API endpoint coverage ≥80%
- [ ] All error cases tested
- [ ] All success cases tested

---

## Phase 1, Week 5-6: Frontend Implementation

### API Client & Types

**TypeScript Compilation:**
- [ ] `types/analyze.ts` compiles without errors
- [ ] `lib/api.ts` compiles without errors
- [ ] `hooks/useAnalyze.ts` compiles without errors

**Type Checking:**
```bash
cd frontend
npm run type-check
# Should complete with 0 errors
```

**API Client Tests:**
```typescript
// Test in browser console or create test file
import { analyzeVerse } from '@/lib/api';

// Test 1: Successful request
analyzeVerse({ text: "إذا غامَرتَ في شَرَفٍ مَرومِ" })
  .then(data => console.log('Success:', data))
  .catch(err => console.error('Error:', err));
// Should log success response

// Test 2: Invalid input
analyzeVerse({ text: "" })
  .then(data => console.log('Success:', data))
  .catch(err => console.error('Error:', err));
// Should log error
```

---

### Analyze Page UI

**Page Rendering:**
- [ ] Page accessible at `/analyze`
- [ ] Page title displays: "محلل الشعر"
- [ ] Form renders correctly
- [ ] No console errors
- [ ] No hydration errors

**Visual Checks:**
- [ ] Textarea displays with RTL layout
- [ ] Textarea uses Amiri font (poetry font)
- [ ] Placeholder text in Arabic
- [ ] Submit button displays "حلّل"
- [ ] Layout is responsive (test at 375px, 768px, 1024px widths)

**Form Functionality:**
- [ ] Can type Arabic text in textarea
- [ ] Submit button disabled when input empty
- [ ] Form validation shows errors
- [ ] Error: "الرجاء إدخال بيت شعري" if text too short
- [ ] Error cleared when valid input entered

**Form Submission:**
- [ ] Clicking "حلّل" calls API
- [ ] Loading state shows during API call
- [ ] Button text changes to "جارٍ التحليل..." during loading
- [ ] Button disabled during loading
- [ ] Results display after successful response

---

### Results Display

**Results Component:**
- [ ] Results card renders after successful analysis
- [ ] Verse text displayed in Amiri font (large size)
- [ ] Taqti3 pattern displayed in monospace font
- [ ] Bahr name (Arabic) displayed prominently
- [ ] Bahr name (English) displayed
- [ ] Confidence percentage displayed
- [ ] Quality score displayed (0-100)
- [ ] Progress bar shows score visually

**Visual Styling:**
- [ ] Card has shadow (shadow-lg)
- [ ] Card has rounded corners (rounded-lg)
- [ ] Card has white background
- [ ] Good spacing (padding, margins)
- [ ] Text hierarchy clear (sizes, weights)

**Edge Cases:**
- [ ] Low confidence (<70%): Warning message displayed
- [ ] No bahr detected: Appropriate message shown
- [ ] Very long verse: Text wraps correctly
- [ ] Very short verse: Still displays properly

---

### Loading & Error States

**Loading States:**
- [ ] Spinner shows when analyzing
- [ ] Textarea disabled during loading
- [ ] Submit button disabled during loading
- [ ] Loading text in Arabic
- [ ] Spinner size appropriate

**Error Handling:**
- [ ] Network error shows: "خطأ في الاتصال، يرجى المحاولة مرة أخرى"
- [ ] Invalid input error shows appropriate message
- [ ] Server error shows: "حدث خطأ في الخادم، يرجى المحاولة لاحقاً"
- [ ] Error message in red/warning color
- [ ] Error can be dismissed

**Animations:**
- [ ] Results fade in smoothly (Framer Motion)
- [ ] Loading spinner animates
- [ ] No janky/abrupt transitions

---

### Responsive Design

**Mobile (375px):**
- [ ] All text readable
- [ ] Buttons tappable (44px min)
- [ ] No horizontal scroll
- [ ] Textarea full width
- [ ] Results card full width

**Tablet (768px):**
- [ ] Layout adapts appropriately
- [ ] Good use of space
- [ ] Text sizes appropriate

**Desktop (1024px+):**
- [ ] Content centered (max-width container)
- [ ] Not too wide (max 800px for form)
- [ ] Good margins

---

## Phase 1, Week 7-8: Testing & Deployment

### Load Testing

**Setup:**
- [ ] Load testing tool installed (Locust or k6)
- [ ] Test script created
- [ ] Target: 100 concurrent users

**Run Load Test:**
```bash
# Using Locust
locust -f tests/load_test.py --host=http://localhost:8000

# Or using k6
k6 run tests/load_test.js
```

**Performance Metrics:**
- [ ] p50 response time <200ms
- [ ] p95 response time <500ms
- [ ] p99 response time <1000ms
- [ ] No errors under 100 concurrent users
- [ ] System stable during test
- [ ] Memory usage stable (no leaks)

**Bottleneck Identification:**
- [ ] Database queries optimized
- [ ] Cache hit rate >50%
- [ ] CPU usage reasonable (<80%)
- [ ] Memory usage reasonable

---

### Staging Deployment

**Backend Deployment:**
- [ ] Deployed to [Railway/Render/DigitalOcean]
- [ ] Environment variables configured
- [ ] Database connected (managed PostgreSQL)
- [ ] Redis connected (managed Redis)
- [ ] Migrations run: `alembic upgrade head`
- [ ] Bahrs seeded
- [ ] Health check passes

**Frontend Deployment:**
- [ ] Deployed to [Vercel/Netlify/same platform]
- [ ] `NEXT_PUBLIC_API_URL` set to staging backend
- [ ] Build successful
- [ ] Static files served correctly
- [ ] Arabic fonts load

**Staging URLs:**
- Backend: _________________________
- Frontend: _________________________
- API Docs: _________________________

**Staging Tests:**
```bash
# Backend health
curl https://[staging-backend-url]/health
# Should return: {"status": "healthy"}

# Frontend home
curl https://[staging-frontend-url]/
# Should return HTML

# Analyze endpoint
curl -X POST https://[staging-backend-url]/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "إذا غامَرتَ في شَرَفٍ مَرومِ"}'
# Should return analysis JSON
```

**Visual Tests (Browser):**
- [ ] Visit staging frontend URL
- [ ] Home page loads correctly
- [ ] Navigate to /analyze
- [ ] Submit verse analysis
- [ ] Results display correctly
- [ ] No console errors

---

### Beta Testing

**Beta Testers:**
- [ ] Recruited 10+ beta testers
- [ ] Testers include: students, poets, teachers
- [ ] Feedback form created (Google Forms / Typeform)
- [ ] Instructions sent to testers

**Feedback Collection:**
- [ ] Usability feedback gathered
- [ ] Accuracy feedback gathered
- [ ] Bug reports collected
- [ ] Feature requests noted

**Feedback Categories:**
- [ ] UI/UX issues
- [ ] Accuracy issues (false positives/negatives)
- [ ] Performance issues
- [ ] Mobile issues
- [ ] Suggestions for improvement

**Bug Prioritization:**
- [ ] P0 (critical): List bugs _________________________
- [ ] P1 (high): List bugs _________________________
- [ ] P2 (medium): List bugs _________________________

**Bug Fixes:**
- [ ] All P0 bugs fixed
- [ ] All P1 bugs fixed
- [ ] P2 bugs documented for future

---

## Final Phase 1 Checklist

### Code Quality
- [ ] All Python code passes Black formatting
- [ ] All Python code passes Flake8 linting
- [ ] All TypeScript code passes ESLint
- [ ] No TypeScript errors: `npm run type-check`
- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] Backend test coverage ≥80%
- [ ] Frontend has basic tests

### Functionality
- [ ] **Prosody engine achieves 90%+ accuracy**
- [ ] API endpoint works correctly
- [ ] Caching improves performance
- [ ] Frontend displays results correctly
- [ ] Mobile responsive design works
- [ ] Arabic RTL layout correct

### Performance
- [ ] API response time p95 <500ms
- [ ] Cached response time <50ms
- [ ] Load test passes (100 users)
- [ ] No memory leaks
- [ ] Database queries optimized

### Deployment
- [ ] Staging environment live
- [ ] All services healthy
- [ ] 10+ beta testers tested
- [ ] Critical bugs fixed
- [ ] Documentation updated

### Documentation
- [ ] API documented in Swagger
- [ ] README updated with setup instructions
- [ ] Architecture documented
- [ ] Known issues documented
- [ ] Future roadmap updated

---

## Phase 1 Sign-Off

**Date:** _________________________

**Overall Status:** ✅ Ready for Phase 2  /  ⚠️ Needs Work  /  ❌ Not Ready

**Critical Metrics:**
- Accuracy: _____%
- API p95: _____ms
- Test Coverage: _____%
- Beta Testers: _____/10
- Critical Bugs: _____

**Notes:**
_____________________________________________________________
_____________________________________________________________
_____________________________________________________________

**Next Steps:**
1. ___________________________________________________________
2. ___________________________________________________________
3. ___________________________________________________________

---

## Ongoing Maintenance Checklist

### Daily (During Active Development)
- [ ] Run tests: `pytest backend/tests/ -v`
- [ ] Check test coverage: `pytest --cov`
- [ ] Check for TypeScript errors: `npm run type-check`
- [ ] Review logs for errors
- [ ] Monitor staging uptime

### Weekly
- [ ] Review and triage new bug reports
- [ ] Update test dataset if needed
- [ ] Check accuracy with new verses
- [ ] Review performance metrics
- [ ] Update documentation

### Before Each Release
- [ ] Run full test suite
- [ ] Run accuracy tests
- [ ] Run load tests
- [ ] Test on staging
- [ ] Review all open issues
- [ ] Update changelog

---

## Troubleshooting Common Issues

### Accuracy Below 90%

**Steps to Debug:**
1. [ ] Run `pytest tests/core/test_accuracy.py -v -s` to see which verses fail
2. [ ] For each failed verse:
   - [ ] Manually perform taqti3
   - [ ] Compare to algorithm output
   - [ ] Identify where it diverges
3. [ ] Common issues:
   - [ ] Phonetic analysis not handling diacritics correctly
   - [ ] Missing tafa'il patterns
   - [ ] Similarity threshold too strict/loose
4. [ ] Fix identified issues
5. [ ] Re-run accuracy test
6. [ ] Repeat until ≥90%

### API Response Slow

**Steps to Debug:**
1. [ ] Check cache hit rate (should be >50% for repeated queries)
2. [ ] Profile slow requests:
   ```python
   import time
   start = time.time()
   result = perform_taqti3(verse)
   print(f"Taqti3 took: {time.time() - start}s")
   ```
3. [ ] Optimize bottlenecks:
   - [ ] Database query optimization
   - [ ] Pattern matching optimization
   - [ ] Consider caching tafa'il patterns
4. [ ] Re-test performance

### Frontend Not Displaying Arabic Correctly

**Steps to Debug:**
1. [ ] Check browser DevTools Network tab
   - [ ] Verify Cairo font loaded
   - [ ] Verify Amiri font loaded
2. [ ] Check browser DevTools Console for errors
3. [ ] Verify `dir="rtl"` on `<html>` element
4. [ ] Verify font-family CSS classes applied
5. [ ] Test in different browsers (Chrome, Firefox, Safari)

---

## Success Criteria Summary

**Phase 1 MVP is complete when:**

✅ **Accuracy:** Prosody engine ≥90% on test dataset
✅ **Performance:** API p95 <500ms, cached <50ms
✅ **Quality:** Test coverage ≥80%, no critical bugs
✅ **Deployment:** Staging live and stable
✅ **Validation:** 10+ beta testers, positive feedback
✅ **Documentation:** Complete and up-to-date

**Ready to move to Phase 2!** 🎉🚀
