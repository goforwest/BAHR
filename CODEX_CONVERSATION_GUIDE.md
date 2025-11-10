# BAHR Platform - Codex Conversation Guide
## Exact Prompts to Use with ChatGPT Codex or Claude

---

## How to Use This Guide

This document provides **copy-paste ready prompts** for each phase of development. Each prompt:
- References the correct documentation files
- Specifies exact tasks and acceptance criteria
- Includes context for Codex to understand the goal
- Follows a consistent format for clarity

---

## Phase 0: Pre-Development Setup

### Conversation 1: Initialize Project Structure

```
I'm building an Arabic poetry analysis platform called BAHR using FastAPI (backend)
and Next.js (frontend). I need to set up the initial project structure.

Please create the complete directory structure for both backend and frontend following
the specifications in PROJECT_STARTER_TEMPLATE.md, Sections 1-3 for backend and
Section 8 for frontend.

For the backend:
- Create app/ directory with subdirectories: core/, api/v1/endpoints/, models/,
  schemas/, db/, services/, utils/
- Create tests/ directory with subdirectories: core/, api/v1/, fixtures/
- Create all necessary __init__.py files
- Create requirements.txt with the exact dependencies listed in
  PROJECT_STARTER_TEMPLATE.md Section 7

For the frontend:
- Initialize Next.js 14 with TypeScript using the structure in
  PROJECT_STARTER_TEMPLATE.md Section 8
- Configure package.json with all dependencies from Section 9

Create all files as shown in the templates. I'll provide feedback once the structure
is ready.
```

**Expected Output:**
- Complete directory structure
- All `__init__.py` files
- `requirements.txt` and `package.json`

---

### Conversation 2: Setup Docker Environment

```
Now I need to set up the Docker development environment with PostgreSQL and Redis.

Using PROJECT_STARTER_TEMPLATE.md Section 10, create:
1. docker-compose.yml with services for:
   - PostgreSQL 15 (user: bahr_user, password: bahr_password, db: bahr_db)
   - Redis 7
   - Both should have health checks

2. Backend Dockerfile (Python 3.11-slim base)

3. Frontend Dockerfile (Node 18-alpine base)

Use the exact configuration from the template. After creation, I'll test by running
`docker-compose up -d`.
```

**Expected Output:**
- `docker-compose.yml`
- `backend/Dockerfile`
- `frontend/Dockerfile`

**Test Command:**
```bash
docker-compose up -d
docker-compose ps  # Should show services running
```

---

### Conversation 3: Create FastAPI Base Application

```
Create the base FastAPI application following PROJECT_STARTER_TEMPLATE.md Section 1.

Files to create:
1. backend/app/main.py - Main FastAPI app with:
   - CORS middleware configured for http://localhost:3000
   - Root endpoint returning Arabic greeting: "مرحباً بك في منصة بَحْر"
   - /health endpoint
   - Swagger docs at /docs

2. backend/app/config.py - Configuration management using Pydantic Settings with:
   - Database URL
   - Redis URL
   - JWT settings
   - Feature flags (ENABLE_AI_GENERATION, ENABLE_COMPETITIONS)

3. backend/.env.example - Template for environment variables

Use the exact code from the template. After creation, I'll test by running
`uvicorn app.main:app --reload` and checking http://localhost:8000/docs.
```

**Expected Output:**
- `app/main.py`
- `app/config.py`
- `.env.example`

**Test Command:**
```bash
cd backend
uvicorn app.main:app --reload
# Visit http://localhost:8000/docs
```

---

### Conversation 4: Setup Next.js with RTL Support

```
Create the Next.js frontend with RTL (right-to-left) support for Arabic.

Following PROJECT_STARTER_TEMPLATE.md Section 9, create:

1. tailwind.config.ts - Configure with:
   - Arabic fonts: Cairo (variable: --font-cairo), Amiri (variable: --font-amiri)
   - Custom color palette (primary blue shades)

2. app/layout.tsx - Root layout with:
   - HTML lang="ar" dir="rtl"
   - Cairo and Amiri fonts from next/font/google
   - Font variables applied to body

3. app/page.tsx - Home page with:
   - Gradient background (blue-50 to white)
   - Title: "بَحْر" in large Arabic font
   - Subtitle: "محلل الشعر العربي بالذكاء الاصطناعي"
   - CTA button linking to /analyze

4. .env.local - Set NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1

Use the exact code from the template. After creation, I'll test by running `npm run dev`
and verifying Arabic text displays correctly with RTL layout.
```

**Expected Output:**
- `tailwind.config.ts`
- `app/layout.tsx`
- `app/page.tsx`
- `.env.local`

**Test Command:**
```bash
cd frontend
npm run dev
# Visit http://localhost:3000
```

---

## Phase 1, Week 1-2: Prosody Engine Core

### Conversation 5: Implement Text Normalization Module

```
I'm implementing the prosody analysis engine for Arabic poetry. The first step is
text normalization.

Following PHASE_1_WEEK_1-2_SPEC.md Task 1, implement:

File: backend/app/core/normalization.py

Functions to implement:
1. remove_diacritics(text: str) -> str
   - Remove all Arabic diacritical marks (tashkeel)
   - Handle: fatha, damma, kasra, shadda, sukun, tanween

2. normalize_hamza(text: str) -> str
   - Normalize hamza variants: أ، إ، آ → ا
   - Normalize hamza on waw: ؤ → و
   - Normalize hamza on ya: ئ → ي

3. normalize_alef(text: str) -> str
   - Normalize alef variants
   - Convert: ى → ي

4. remove_tatweel(text: str) -> str
   - Remove Arabic tatweel character (ـ)

5. normalize_whitespace(text: str) -> str
   - Replace multiple spaces with single space
   - Strip leading/trailing whitespace

6. normalize_arabic_text(text: str, remove_tashkeel: bool = False, ...) -> str
   - Main normalization function combining all above
   - Validate text contains Arabic characters
   - Raise ValueError if empty or non-Arabic

7. has_diacritics(text: str) -> bool
   - Check if text contains diacritical marks

Include complete docstrings with examples. Use the exact implementation from the spec.

After implementation, I'll review the code and we'll move to unit tests.
```

**Expected Output:**
- Complete `app/core/normalization.py` with all 7 functions
- Docstrings with type hints
- Input validation

**Follow-up Prompt for Tests:**
```
Now create comprehensive unit tests for the normalization module.

File: backend/tests/core/test_normalization.py

Following PHASE_1_WEEK_1-2_SPEC.md Task 1, create test classes:
- TestRemoveDiacritics: Test removal of all diacritic types
- TestNormalizeHamza: Test all hamza normalization cases
- TestNormalizeAlef: Test alef normalization
- TestRemoveTatweel: Test tatweel removal
- TestNormalizeArabicText: Test main function with various scenarios
- TestHasDiacritics: Test diacritic detection

Include edge cases:
- Empty text (should raise ValueError)
- Non-Arabic text (should raise ValueError)
- Text with mixed Arabic and non-Arabic
- Already normalized text

Target: 80%+ code coverage

Use pytest framework and the exact test cases from the spec.
```

**Test Command:**
```bash
cd backend
pytest tests/core/test_normalization.py -v --cov=app.core.normalization
```

---

### Conversation 6: Implement Phonetic Analysis Module

```
Next step: Convert Arabic text to phonetic representation for prosodic analysis.

Following PHASE_1_WEEK_1-2_SPEC.md Task 2, implement:

File: backend/app/core/phonetics.py

1. Create Phoneme dataclass:
   - consonant: str
   - vowel: str (values: 'a', 'u', 'i', 'aa', 'uu', 'ii', '' for sukun)
   - has_shadda: bool
   - Methods: is_long_vowel(), is_sukun()

2. extract_phonemes(text: str, has_tashkeel: bool = False) -> List[Phoneme]
   - Extract phonemes from Arabic text
   - Map diacritics to vowels: fatha→'a', damma→'u', kasra→'i', sukun→''
   - Detect long vowels: ا→'aa', و→'uu', ي→'ii'
   - Handle shadda (gemination)
   - If no tashkeel, infer vowels (heuristic: assume 'a')

3. phonemes_to_pattern(phonemes: List[Phoneme]) -> str
   - Convert phonemes to prosodic pattern
   - Pattern: '/' = haraka (moving), 'o' = sukun (still)
   - Short vowel → '/'
   - Long vowel → '/o'
   - Sukun → 'o'

4. text_to_phonetic_pattern(text: str, has_tashkeel: bool = None) -> str
   - Convenience function combining above
   - Auto-detect tashkeel if not specified

Use the exact implementation from the spec with complete docstrings.
```

**Expected Output:**
- `app/core/phonetics.py` with Phoneme dataclass and 4 functions

**Follow-up for Tests:**
```
Create unit tests for the phonetics module.

File: backend/tests/core/test_phonetics.py

Test classes:
- TestPhoneme: Test dataclass methods (is_long_vowel, is_sukun)
- TestExtractPhonemes: Test phoneme extraction with various inputs
- TestPhonemesToPattern: Test pattern conversion
- TestTextToPhoneticPattern: Test end-to-end conversion

Test cases:
- Words with tashkeel (كَتَبَ → 3 phonemes with 'a')
- Words with sukun (كَتْبَ)
- Words with shadda (مُحَمَّد)
- Words with long vowels (كِتَاب → detect 'aa')
- Words without tashkeel (should infer vowels)

Use pytest and the test cases from PHASE_1_WEEK_1-2_SPEC.md Task 2.
```

---

### Conversation 7: Implement Taqti3 Algorithm

```
Now implement the core prosodic scansion algorithm (taqti3).

Following PHASE_1_WEEK_1-2_SPEC.md Task 3, implement:

File: backend/app/core/taqti3.py

1. Define BASIC_TAFAIL dictionary mapping patterns to tafa'il names:
   - "/o//o" → "فعولن" (fa'uulun)
   - "//o/o" → "مفاعيلن" (mafaa'iilun)
   - "///o" → "مفاعلتن" (mafaa'alatun)
   - "/o/o//o" → "مستفعلن" (mustaf'ilun)
   - "//o//o" → "فاعلاتن" (faa'ilaatun)
   - "/o/o/o" → "فاعلن" (faa'ilun)
   - "///" → "فعلن" (fa'lan)
   - "/o//" → "مفعولات" (maf'uulaatu)

2. pattern_to_tafail(pattern: str) -> List[str]
   - Convert phonetic pattern to list of tafa'il names
   - Use greedy matching (longest match first)
   - Iterate through pattern, match substrings to BASIC_TAFAIL

3. perform_taqti3(verse: str, normalize: bool = True) -> str
   - Main function: verse → tafa'il string
   - Steps:
     a. Normalize text (using normalize_arabic_text)
     b. Convert to phonetic pattern (using text_to_phonetic_pattern)
     c. Convert pattern to tafa'il (using pattern_to_tafail)
     d. Join with spaces
   - Validate verse is not empty
   - Return string like "فعولن مفاعيلن فعولن مفاعيلن"

Import from: app.core.normalization, app.core.phonetics

Use exact implementation from spec.
```

**Expected Output:**
- `app/core/taqti3.py` with dictionary and 2 functions

**Follow-up for Tests:**
```
Create unit tests for taqti3.

File: backend/tests/core/test_taqti3.py

Test classes:
- TestPatternToTafail: Test pattern matching
- TestPerformTaqti3: Test end-to-end taqti3

Test cases:
- Empty verse (should raise ValueError)
- Known patterns matching tafa'il
- Real verses (add 3-5 test verses once we have test data)

Note: Full accuracy testing will come later with the test dataset.

Use pytest and tests from PHASE_1_WEEK_1-2_SPEC.md Task 3.
```

---

### Conversation 8: Implement Bahr Detection

```
Implement the bahr (meter) detection algorithm.

Following PHASE_1_WEEK_1-2_SPEC.md Task 4, implement:

File: backend/app/core/bahr_detector.py

1. Create BahrInfo dataclass:
   - id: int
   - name_ar: str
   - name_en: str
   - pattern: str
   - confidence: float (0.0 to 1.0)
   - Method: to_dict() -> Dict

2. Define BAHRS_DATA list with at least 4 bahrs:
   - الطويل (at-Tawil): "فعولن مفاعيلن فعولن مفاعيلن"
   - الكامل (al-Kamil): "متفاعلن متفاعلن متفاعلن"
   - الوافر (al-Wafir): "مفاعلتن مفاعلتن فعولن"
   - الرمل (ar-Ramal): "فاعلاتن فاعلاتن فاعلاتن"

3. BahrDetector class:
   - __init__(): Load bahrs data
   - calculate_similarity(tafail1: str, tafail2: str) -> float
     * Use difflib.SequenceMatcher for fuzzy matching
     * Allow minor variations (zihafat)
   - detect_bahr(tafail_pattern: str) -> Optional[BahrInfo]
     * Compare input to all bahr patterns
     * Find best match
     * Return only if confidence ≥ 0.7
   - analyze_verse(verse: str) -> Optional[BahrInfo]
     * Perform taqti3 then detect bahr
     * End-to-end function

Import from: app.core.taqti3
Use difflib.SequenceMatcher for similarity calculation

Use exact implementation from spec with complete docstrings.
```

**Expected Output:**
- `app/core/bahr_detector.py` with BahrInfo and BahrDetector class

**Follow-up for Tests:**
```
Create unit tests for bahr detector.

File: backend/tests/core/test_bahr_detector.py

Test class: TestBahrDetector

Test methods:
- test_initialization: Verify bahrs loaded
- test_calculate_similarity_exact_match: Same pattern → 1.0
- test_calculate_similarity_different: Different patterns → <1.0
- test_detect_bahr_returns_bahrinfo: Valid pattern → BahrInfo object
- test_detect_bahr_returns_none_for_invalid: Invalid pattern → None

Note: Full accuracy testing with real verses will come in Conversation 10.

Use pytest and tests from PHASE_1_WEEK_1-2_SPEC.md Task 4.
```

---

### Conversation 9: Create Test Dataset

```
I need a test dataset of Arabic poetry verses for accuracy testing.

Following PHASE_1_WEEK_1-2_SPEC.md Task 5, create:

File: backend/tests/fixtures/test_verses.json

JSON structure:
{
  "verses": [
    {
      "text": "Arabic verse with diacritics",
      "poet": "Poet name",
      "bahr": "البحر name in Arabic",
      "expected_tafail": "Expected tafa'il pattern",
      "notes": "Any notes"
    },
    ...
  ]
}

Requirements:
- At least 50 verses total
- Cover all 4 implemented bahrs (الطويل، الكامل، الوافر، الرمل)
- Minimum 10 verses per bahr
- Use classical poetry (public domain)
- Include diacritics (tashkeel) for accurate testing
- Verify each verse manually before adding

Famous verses to include:
- "إذا غامَرتَ في شَرَفٍ مَرومِ" (المتنبي - الطويل)
- "أَلا لَيتَ الشَبابَ يَعودُ يَوماً" (أبو العتاهية - الكامل)

Search classical diwans for more verses. Ensure they are correctly attributed
and prosodically sound (no errors in meter).
```

**Expected Output:**
- `tests/fixtures/test_verses.json` with 50+ verses

**Note:** This task may require human verification of verses. Codex can help find and format verses, but accuracy should be double-checked.

---

### Conversation 10: Implement Accuracy Testing

```
Create comprehensive accuracy tests for the prosody engine.

Following PHASE_1_WEEK_1-2_SPEC.md Task 6, implement:

File: backend/tests/core/test_accuracy.py

1. Create pytest fixture to load test verses:
   - Load from tests/fixtures/test_verses.json
   - Return list of verse dictionaries

2. Test class: TestAccuracy

3. test_overall_accuracy(test_verses):
   - Iterate through all verses
   - Call detector.analyze_verse(verse['text'])
   - Compare detected bahr to expected bahr
   - Calculate accuracy = correct / total
   - Print accuracy percentage
   - Assert accuracy ≥ 0.90 (90% target)

4. test_accuracy_by_bahr(test_verses):
   - Group verses by bahr
   - Calculate accuracy for each bahr separately
   - Print per-bahr accuracy
   - Assert each bahr ≥ 0.80 (80% target)

Use pytest with the -s flag to print results:
pytest tests/core/test_accuracy.py -v -s

If accuracy is below target:
1. Identify which verses fail
2. Debug phonetic analysis
3. Improve pattern matching
4. Adjust similarity threshold in BahrDetector

Goal: Achieve 90%+ overall accuracy before proceeding to Week 3-4.

Use exact implementation from PHASE_1_WEEK_1-2_SPEC.md Task 6.
```

**Expected Output:**
- `tests/core/test_accuracy.py` with accuracy tests

**Test Command:**
```bash
pytest tests/core/test_accuracy.py -v -s
# Should print accuracy results and pass assertions
```

---

### Conversation 11: Optimize for 90% Accuracy (Iterative)

```
The accuracy test shows [X]% accuracy, which is below the 90% target.

Failed verses:
[List verses that failed detection]

Please analyze the failures and suggest optimizations:

1. Review phonetic analysis in app/core/phonetics.py:
   - Are diacritics being parsed correctly?
   - Are long vowels detected properly?
   - Is shadda handling correct?

2. Review pattern matching in app/core/taqti3.py:
   - Are all tafa'il patterns defined correctly?
   - Is greedy matching working as expected?
   - Should we add more tafa'il variations?

3. Review bahr detection in app/core/bahr_detector.py:
   - Is the similarity threshold (0.7) appropriate?
   - Should we adjust fuzzy matching parameters?
   - Do bahr patterns match classical definitions?

For each issue found, provide:
- Root cause analysis
- Proposed fix
- Expected impact on accuracy

After implementing fixes, I'll re-run the accuracy test.

Our goal: 90%+ overall accuracy, 80%+ per-bahr accuracy.
```

**Expected Output:**
- Analysis of failure modes
- Proposed code changes
- Explanation of improvements

**Iteration:** Repeat this conversation until 90% accuracy is achieved.

---

## Phase 1, Week 3-4: API & Database

### Conversation 12: Create Database Models

```
Now we'll create SQLAlchemy models for the database schema.

Following IMPLEMENTATION_PLAN_FOR_CODEX.md Section 3 and
PROJECT_STARTER_TEMPLATE.md Section 4, implement:

Files to create:

1. backend/app/models/user.py
   - User model with fields: id, email, username, password_hash, full_name, bio,
     avatar_url, level, xp, coins, is_active, is_verified, created_at, last_login

2. backend/app/models/bahr.py
   - Bahr model: id, name_ar, name_en, pattern, description, example_verse
   - Taf3ila model: id, name, pattern, variations (JSONB), bahr_id (FK)

3. backend/app/models/poem.py
   - Poem model: id, user_id (FK), title, full_text, bahr, is_complete, visibility,
     created_at, updated_at
   - Verse model: id, poem_id (FK), text, taqti3_pattern, bahr, line_number, hemisphere
   - Relationships: Poem.verses

4. backend/app/db/base.py
   - Import Base from SQLAlchemy
   - Import all models (for Alembic auto-detection)

5. backend/app/db/session.py
   - Create engine with DATABASE_URL from settings
   - Create SessionLocal
   - get_db() dependency function for FastAPI

All models should:
- Use proper data types (String lengths, Text for long content)
- Have __repr__ methods
- Include proper indexes (email, username unique)

Use exact code from PROJECT_STARTER_TEMPLATE.md Section 4.
```

**Expected Output:**
- 4 model files created
- `db/base.py` and `db/session.py` configured

---

### Conversation 13: Setup Alembic Migrations

```
Initialize Alembic for database migrations.

Steps:

1. Initialize Alembic in backend directory:
   cd backend
   alembic init migrations

2. Configure migrations/env.py:
   - Import Base from app.db.base
   - Set target_metadata = Base.metadata
   - Use DATABASE_URL from app.config.settings

3. Update alembic.ini:
   - Set sqlalchemy.url to use environment variable

4. Create initial migration:
   alembic revision --autogenerate -m "Initial schema"

5. Review generated migration in migrations/versions/

6. Apply migration:
   alembic upgrade head

7. Verify tables created:
   docker exec bahr_postgres psql -U bahr_user -d bahr_db -c "\dt"

Expected tables: users, bahrs, tafa3il, poems, verses

After completion, I'll verify the database schema.
```

**Expected Output:**
- Alembic configured
- Initial migration created
- Tables created in PostgreSQL

---

### Conversation 14: Create Seed Script for Bahrs

```
Create a script to populate the bahrs table with all 16 classical Arabic meters.

File: backend/scripts/seed_bahrs.py

Requirements:
- Use SQLAlchemy to insert bahrs into database
- Include all 16 bahrs with:
  * id (1-16)
  * name_ar (Arabic name)
  * name_en (English transliteration)
  * pattern (tafa'il pattern)
  * description (Arabic description)
  * example_verse (one example verse)

The 16 bahrs:
1. الطويل (at-Tawil)
2. الكامل (al-Kamil)
3. الوافر (al-Wafir)
4. الرمل (ar-Ramal)
5. البسيط (al-Basit)
6. الخفيف (al-Khafif)
7. المتقارب (al-Mutaqarib)
8. المتدارك (al-Mutadarik)
9. الهزج (al-Hazaj)
10. الرجز (ar-Rajaz)
11. السريع (as-Sari')
12. المنسرح (al-Munsarih)
13. المقتضب (al-Muqtadab)
14. المجتث (al-Mujtatth)
15. المضارع (al-Mudari')
16. المحدث (al-Muhdath)

Script should:
- Be idempotent (check if bahr exists before inserting)
- Print progress
- Handle errors gracefully

Run with: python scripts/seed_bahrs.py

Reference classical prosody resources for accurate patterns and descriptions.
```

**Expected Output:**
- `scripts/seed_bahrs.py` script
- All 16 bahrs in database after running

---

### Conversation 15: Implement Analyze API Endpoint

```
Create the main analysis API endpoint.

Following IMPLEMENTATION_PLAN_FOR_CODEX.md Section 4.2 and
PROJECT_STARTER_TEMPLATE.md Section 6, implement:

Files to create:

1. backend/app/schemas/analyze.py
   - AnalyzeRequest: text (str), detect_bahr (bool), suggest_corrections (bool)
   - BahrInfo: name_ar, name_en, confidence
   - AnalyzeResponse: text, taqti3, bahr, errors, suggestions, score
   - Include validators (text must have Arabic characters)
   - Add schema_extra with examples

2. backend/app/api/v1/endpoints/analyze.py
   - POST /analyze endpoint
   - Steps:
     a. Normalize text
     b. Check Redis cache (key: SHA256 hash of normalized text)
     c. If cache miss: perform taqti3, detect bahr
     d. Calculate score (confidence * 100)
     e. Build response
     f. Cache result (TTL: 24 hours)
     g. Return response
   - Error handling: 400 for invalid input, 500 for server errors
   - Logging with logger.info and logger.error

3. backend/app/api/v1/router.py
   - Import analyze router
   - Include in api_router with prefix="/analyze", tags=["Analysis"]

4. Update backend/app/main.py
   - Include api_router with prefix="/api/v1"

Dependencies: get_db (for future use), Redis cache functions

Use exact implementation from templates with proper async/await syntax.
```

**Expected Output:**
- 3 files created
- `app/main.py` updated
- Endpoint accessible at POST /api/v1/analyze

**Test Command:**
```bash
# Start server
uvicorn app.main:app --reload

# Test endpoint
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "إذا غامَرتَ في شَرَفٍ مَرومِ"}'

# Should return JSON with taqti3 and bahr
```

---

### Conversation 16: Implement Redis Caching

```
Add Redis caching to the analyze endpoint for performance.

Following PROJECT_STARTER_TEMPLATE.md Section 3, implement:

1. backend/app/db/redis.py
   - get_redis() -> Redis client
   - cache_set(key, value, ttl)
   - cache_get(key) -> value or None
   - cache_delete(key)
   - Use redis.asyncio for async support
   - JSON serialize values

2. Update backend/app/api/v1/endpoints/analyze.py
   - Import cache functions
   - Generate cache key: hashlib.sha256(normalized_text).hexdigest()
   - Check cache before analysis: cached = await cache_get(f"analysis:{cache_key}")
   - If cached, return immediately
   - After analysis, cache result: await cache_set(f"analysis:{cache_key}", response, 86400)

3. Update backend/app/main.py
   - Initialize Redis connection on startup
   - Close Redis on shutdown

Test caching:
- First request: should take ~500ms (analysis performed)
- Second identical request: should take <50ms (cache hit)

Use exact implementation from templates.
```

**Expected Output:**
- `app/db/redis.py` with cache functions
- `analyze.py` updated with caching
- Response time improved on repeated requests

---

## Phase 1, Week 5-6: Frontend Implementation

### Conversation 17: Create API Client and Types

```
Create the frontend API client for communicating with the backend.

Following PROJECT_STARTER_TEMPLATE.md Section 9, create:

1. frontend/src/types/analyze.ts
   - AnalyzeRequest interface
   - BahrInfo interface
   - AnalyzeResponse interface
   - Match backend Pydantic schemas exactly

2. frontend/src/lib/api.ts
   - Create axios instance with baseURL from env
   - Add request interceptor (add auth token if present)
   - Add response interceptor (handle 401 errors)
   - Function: analyzeVerse(data: AnalyzeRequest): Promise<AnalyzeResponse>
   - Function: getBahrs(): Promise<any>

3. frontend/src/hooks/useAnalyze.ts
   - Custom React Query hook
   - useMutation for analyze (POST request)
   - Return: { mutate, data, isLoading, error }

Use TypeScript for all files with proper types.
```

**Expected Output:**
- `types/analyze.ts`
- `lib/api.ts`
- `hooks/useAnalyze.ts`

---

### Conversation 18: Create Analyze Page UI

```
Build the analyze page where users input verses and see results.

Following IMPLEMENTATION_PLAN_FOR_CODEX.md Phase 1 Week 5-6, create:

1. frontend/src/app/analyze/page.tsx
   - Page title: "محلل الشعر"
   - Use AnalyzeForm and AnalyzeResults components
   - Manage state: result, loading
   - On form submit: call useAnalyze hook

2. frontend/src/components/AnalyzeForm.tsx
   - Textarea for verse input (RTL, font-poetry, 4 rows)
   - Placeholder: "إذا غامَرتَ في شَرَفٍ مَرومِ"
   - Submit button: "حلّل"
   - Use react-hook-form with Zod validation
   - Validation: min 5 chars, max 500 chars, contains Arabic
   - Loading state: disable button and show "جارٍ التحليل..."

3. frontend/src/components/AnalyzeResults.tsx
   - Display verse text (font-poetry, large)
   - Display taqti3 (monospace font)
   - Display bahr (name_ar, name_en, confidence %)
   - Display score (progress bar, 0-100)
   - Card layout with Tailwind (bg-white, shadow-lg, rounded-lg)

All text in Arabic, RTL layout, responsive design.

Use Tailwind CSS for styling.
```

**Expected Output:**
- `app/analyze/page.tsx`
- `components/AnalyzeForm.tsx`
- `components/AnalyzeResults.tsx`

**Test:**
- Visit http://localhost:3000/analyze
- Enter verse, click "حلّل"
- Should see results displayed

---

### Conversation 19: Add Loading and Error States

```
Improve UX with loading spinners and error handling.

Updates needed:

1. frontend/src/components/AnalyzeForm.tsx
   - Add loading spinner when isLoading
   - Disable textarea during loading
   - Show error message if error (in Arabic)

2. frontend/src/components/AnalyzeResults.tsx
   - Add animation with Framer Motion (fade in)
   - Add "تحليل جديد" button to reset

3. Create frontend/src/components/LoadingSpinner.tsx
   - Reusable spinner component
   - Use Tailwind for styling
   - Size variants: sm, md, lg

4. Error handling:
   - Network error: "خطأ في الاتصال، يرجى المحاولة مرة أخرى"
   - Invalid input: "يرجى إدخال بيت شعري صحيح"
   - Server error: "حدث خطأ في الخادم، يرجى المحاولة لاحقاً"

Use Framer Motion for smooth animations.
```

**Expected Output:**
- Updated components with loading/error states
- `LoadingSpinner.tsx` component
- Smooth UX transitions

---

## Phase 1, Week 7-8: Testing & Deployment

### Conversation 20: Write Integration Tests

```
Create integration tests for the analyze API endpoint.

File: backend/tests/api/v1/test_analyze.py

Using pytest and httpx.AsyncClient, create tests:

1. test_analyze_valid_verse:
   - POST valid verse
   - Assert 200 status
   - Assert response has taqti3, bahr, score

2. test_analyze_cached_response:
   - POST same verse twice
   - Second request should be faster
   - Responses should be identical

3. test_analyze_invalid_input_empty:
   - POST empty text
   - Assert 400 status
   - Assert error message

4. test_analyze_invalid_input_no_arabic:
   - POST English text
   - Assert 400 status

5. test_analyze_verse_without_diacritics:
   - POST verse without tashkeel
   - Should still work (infer vowels)

Setup:
- Use pytest fixtures for test client
- Use @pytest.mark.asyncio for async tests

Target: All tests passing, integration coverage >80%
```

**Expected Output:**
- `tests/api/v1/test_analyze.py` with 5+ tests

**Run:**
```bash
pytest tests/api/v1/test_analyze.py -v
```

---

### Conversation 21: Deploy to Staging

```
I need to deploy the BAHR platform to a staging environment for beta testing.

Platform choice: [Railway / Render / DigitalOcean]

Steps needed:

Backend deployment:
1. Create Procfile or equivalent for FastAPI
2. Configure environment variables:
   - DATABASE_URL (managed PostgreSQL)
   - REDIS_URL (managed Redis)
   - JWT_SECRET_KEY (generate secure random)
3. Setup database migrations (run alembic upgrade head)
4. Seed bahrs data

Frontend deployment:
1. Set NEXT_PUBLIC_API_URL to staging backend URL
2. Build Next.js app: npm run build
3. Deploy static/server files

Provide step-by-step instructions for deploying on [chosen platform].

After deployment, provide:
- Staging backend URL
- Staging frontend URL
- Health check command to verify deployment
```

**Expected Output:**
- Deployment instructions
- Configuration files (Procfile, railway.json, etc.)
- Staging URLs

---

## General Tips for Working with Codex

### 1. **Provide Context**
Always reference the documentation files:
```
"Following PHASE_1_WEEK_1-2_SPEC.md Task 3, implement..."
```

### 2. **Be Specific About Files**
State exact file paths:
```
"Create file: backend/app/core/normalization.py"
```

### 3. **Request Code First, Then Tests**
Do implementation and tests separately for clarity:
```
"First implement the function, then in the next prompt I'll ask for tests."
```

### 4. **Ask for Explanations**
If something is unclear:
```
"Explain how the fuzzy matching works in BahrDetector.calculate_similarity()"
```

### 5. **Iterate on Quality**
If output doesn't meet standards:
```
"The code works but lacks docstrings. Please add comprehensive docstrings
with type hints and examples for all functions."
```

### 6. **Validate Incrementally**
Test after each major component:
```
"Now let's test this. I'll run: pytest tests/core/test_normalization.py -v
[paste output]
[If tests fail]: The test failed with error X. Please fix..."
```

---

## Example Complete Workflow (Week 1)

```
DAY 1:
Conversation 1: Project structure ✅
Conversation 2: Docker setup ✅
Test: docker-compose up -d

DAY 2:
Conversation 3: FastAPI base ✅
Test: curl http://localhost:8000/
Conversation 4: Next.js setup ✅
Test: npm run dev

DAY 3:
Conversation 5: Normalization module ✅
Conversation 5b: Normalization tests ✅
Test: pytest tests/core/test_normalization.py -v

DAY 4:
Conversation 6: Phonetics module ✅
Conversation 6b: Phonetics tests ✅
Test: pytest tests/core/test_phonetics.py -v

DAY 5:
Conversation 7: Taqti3 algorithm ✅
Conversation 7b: Taqti3 tests ✅
Test: pytest tests/core/ -v

WEEKEND:
Conversation 8: Bahr detector ✅
Conversation 8b: Bahr tests ✅
Conversation 9: Create test dataset (may need human help) ✅

DAY 8:
Conversation 10: Accuracy testing ✅
Test: pytest tests/core/test_accuracy.py -v -s
[If <90%]: Conversation 11: Optimize for accuracy (iterate)

Week 1 Complete! 🎉
```

---

## Success! 🚀

You now have **ready-to-use conversation prompts** for every step of Phase 1.

**How to proceed:**
1. Start with Conversation 1
2. Copy-paste prompt to Codex
3. Review output, test code
4. Move to next conversation
5. Iterate until phase complete

**Pro tips:**
- Keep context in conversation (Codex remembers previous messages)
- Start new conversation if context gets too long
- Always test code before moving to next step
- Document any deviations from the plan

Happy building! 🎭
