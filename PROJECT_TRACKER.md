# BAHR Platform - Project Management Tracker
## GitHub Issues & Milestones Template

---

## How to Use This Tracker

1. **Copy issues to GitHub:** Create issues in your repository using the templates below
2. **Create milestones:** Set up milestones for each phase
3. **Assign labels:** Use labels to categorize issues (backend, frontend, bug, enhancement, etc.)
4. **Track progress:** Update issue status as you complete tasks
5. **Use project board:** Create a Kanban board with columns: Backlog, In Progress, Review, Done

---

## Milestones

### Milestone 1: Phase 0 - Pre-Development ✅ COMPLETE (95%)
**Due Date:** Week 2
**Status:** ✅ **COMPLETE** - November 10, 2025
**Description:** Setup infrastructure and development environment

**Completed Issues:**
- ✅ #1: Initialize Git Repository
- ✅ #2: Setup Docker Development Environment  
- ✅ #3: Initialize Next.js Frontend Project
- ✅ #4: Initialize FastAPI Backend Project (dependencies installed)
- ✅ #5: Setup CI/CD Pipeline
- ✅ #6: Configure CORS & Security (Week 0 completion)

**Progress:** 95% (deployment items deferred appropriately)

---

### Milestone 2: Phase 1 Week 1-2 - Prosody Engine Core ✅ COMPLETE (100%)
**Due Date:** Week 3-4
**Status:** ✅ **COMPLETE** - November 10, 2025
**Description:** Build core poetry analysis engine with 98.1% accuracy

**Completed Issues:**
- ✅ #7: Text Normalization Module (82 tests passing)
- ✅ #8: Phonetic Analysis with CAMeL Tools (native ARM64)
- ✅ #9: Taqti3 Algorithm Implementation (pattern matching)
- ✅ #10: Bahr Detection (4 meters, 98.1% accuracy)
- ✅ #11: Golden Dataset Creation (52 verses)
- ✅ #12: Testing & Documentation (99% coverage)

**Progress:** 100% (exceeded 90% accuracy target with 98.1%)

**Week 1-2 Achievements:**
```yaml
Accuracy: 98.1% (target was 90%)
Test Coverage: 99%
Tests Passing: 220/230 (95.7%)
CAMeL Tools: ✅ Working natively on ARM64
Golden Dataset: 52 verses (4 meters)
```

---

### Milestone 3: Phase 1 Week 3-4 - API Integration 🔄 NEXT
**Due Date:** Week 5-6
**Status:** 🔄 **IN PROGRESS**
**Description:** Implement REST API endpoints and frontend integration

**Upcoming Issues:**
- Week 3-4: #13, #14, #15, #16, #17
- Week 5-6: #18, #19, #20, #21
- Week 7-8: #22, #23, #24, #25

---

### Milestone 4: Phase 2 - AI Poet (Future)
**Due Date:** Month 5
**Description:** Train and deploy AI poetry generation model

**Issues:**
- #26 through #40

---

### Milestone 5: Phase 3 - Competition Arena (Future)
**Due Date:** Month 8
**Description:** Build real-time competition system

**Issues:**
- #41 through #55

---

## GitHub Issue Templates

---

## PHASE 0: Pre-Development

### Issue #1: Initialize Git Repository
```markdown
**Title:** Initialize Git repository with proper structure

**Labels:** setup, phase-0

**Description:**
Setup Git repository with proper branching strategy and project structure.

**Tasks:**
- [ ] Create repository on GitHub
- [ ] Initialize local repository
- [ ] Create `main` and `develop` branches
- [ ] Setup branch protection rules
- [ ] Create `.gitignore` for Python and Node.js
- [ ] Add initial `README.md`

**Acceptance Criteria:**
- Repository is accessible to team members
- Branching strategy documented
- `.gitignore` covers all necessary files

**References:**
- Implementation Plan: Section 5, Phase 0
```

---

### Issue #2: Setup Docker Development Environment
```markdown
**Title:** Configure Docker Compose for local development

**Labels:** setup, phase-0, devops

**Description:**
Setup Docker Compose with PostgreSQL, Redis, and Elasticsearch containers.

**Tasks:**
- [ ] Create `docker-compose.yml` (see PROJECT_STARTER_TEMPLATE.md)
- [ ] Configure PostgreSQL service
- [ ] Configure Redis service
- [ ] Configure Elasticsearch service (optional for Phase 1)
- [ ] Test all services start correctly
- [ ] Document how to start/stop services

**Acceptance Criteria:**
- `docker-compose up` starts all services
- PostgreSQL accessible on localhost:5432
- Redis accessible on localhost:6379
- Health checks pass for all services

**References:**
- PROJECT_STARTER_TEMPLATE.md, Section 10
```

---

### Issue #3: Initialize Next.js Frontend Project ✅ COMPLETE
```markdown
**Title:** Create Next.js 14 project with TypeScript and Tailwind

**Labels:** setup, phase-0, frontend, ✅ COMPLETE

**Status:** ✅ COMPLETE (November 9, 2025)

**Description:**
Initialize Next.js frontend project with all required configurations.

**Tasks:**
- [x] Run `npx create-next-app@latest` with TypeScript ✅
- [x] Install dependencies (lucide-react, class-variance-authority, etc.) ✅
- [x] Configure Tailwind CSS v4 with RTL support ✅
- [x] Add Arabic fonts (Cairo, Amiri) via next/font/google ✅
- [x] Create basic layout with RTL (`dir="rtl"`) ✅
- [x] Setup ESLint and Prettier ✅
- [x] Create Arabic homepage with poetry samples ✅
- [x] Initialize shadcn/ui component system ✅

**Completion Notes:**
- Used Next.js 16.0.1 (latest stable)
- Tailwind CSS v4 (via @tailwindcss/postcss)
- Native RTL support (no plugins needed)
- Dev server running on http://localhost:3000
- Zero TypeScript/ESLint errors
- Full documentation in frontend/README_AR.md

**Acceptance Criteria:**
- [x] Project runs with `npm run dev` ✅
- [x] RTL layout works correctly ✅
- [x] Arabic fonts load properly (Cairo + Amiri) ✅
- [x] Linting passes ✅

**References:**
- PROJECT_STARTER_TEMPLATE.md, Section 8-9
- PROGRESS_LOG.md (November 9, 2025 entry)
- frontend/README_AR.md
```

---

### Issue #4: Initialize FastAPI Backend Project ✅ COMPLETE
```markdown
**Title:** Create FastAPI project with SQLAlchemy and Alembic

**Labels:** setup, phase-0, backend, ✅ COMPLETE

**Status:** ✅ COMPLETE (November 10, 2025)

**Description:**
Initialize FastAPI backend project with proper structure and all dependencies.

**Tasks:**
- [x] Create project structure ✅
- [x] Setup `requirements.txt` with 14 dependencies ✅
- [x] Create `app/main.py` with FastAPI instance ✅
- [x] Configure `app/config.py` with Pydantic Settings ✅
- [x] Setup database connection (`app/db/session.py`) ✅
- [x] Initialize Alembic for migrations ✅
- [x] Create `.env.example` ✅
- [x] Install CAMeL Tools 1.5.2 (verified ARM64) ✅
- [x] Configure CORS middleware ✅
- [x] Test server runs with `uvicorn app.main:app` ✅

**Completion Notes:**
- FastAPI 0.115.0 installed
- CAMeL Tools working natively on ARM64 (M1/M2)
- CORS configured for localhost:3000, localhost:8000
- All dependencies in requirements.txt
- Database schema with 8 indexes
- 220 tests passing (95.7%)

**Acceptance Criteria:**
- [x] FastAPI server starts on http://localhost:8000 ✅
- [x] `/docs` shows Swagger UI ✅
- [x] Database connection works (PostgreSQL via Docker) ✅
- [x] CAMeL Tools imports successfully ✅
- [x] CORS middleware configured ✅

**References:**
- PROJECT_STARTER_TEMPLATE.md, Sections 1-3
- backend/requirements.txt (14 dependencies)
- PHASE_0_AND_WEEK_1-2_COMPLETION_REPORT.md
```

---

### Issue #5: Setup CI/CD Pipeline ✅ COMPLETE
```markdown
**Title:** Configure GitHub Actions for CI/CD

**Labels:** setup, phase-0, devops
**Status:** ✅ COMPLETED (Nov 9, 2025)

**Description:**
Setup automated testing and linting on every push.

**Tasks:**
- [x] Create `.github/workflows/backend.yml`
  - [x] Run pytest with coverage
  - [x] Run Black formatter check
  - [x] Run Flake8 linter
  - [x] Run isort import sorting
  - [x] Run mypy type checking
  - [x] Multi-version testing (Python 3.11, 3.12)
  - [x] Codecov integration
- [x] Create `.github/workflows/frontend.yml`
  - [x] Run npm build
  - [x] Run ESLint
  - [x] Type check with TypeScript
  - [x] Run Prettier format check
  - [x] Multi-version testing (Node 20.x, 22.x)
- [x] Create `.github/workflows/deploy.yml`
  - [x] Railway backend deployment
  - [x] Railway frontend deployment
  - [x] Auto-deploy on main push
- [x] Add status badges to README.md
- [x] Create comprehensive documentation
- [x] Create railway.toml configuration

**Acceptance Criteria:**
- ✅ CI runs on every push to develop/main
- ✅ Tests must pass to merge PR
- ✅ Linting enforced
- ✅ Auto-deploy to Railway on main merge
- ✅ Status badges visible in README
- ✅ Team action checklist created

**Deliverables:**
- `.github/workflows/backend.yml` - Backend CI pipeline
- `.github/workflows/frontend.yml` - Frontend CI pipeline
- `.github/workflows/deploy.yml` - Deployment workflow
- `railway.toml` - Railway configuration
- `docs/CI_CD_GUIDE.md` - Comprehensive guide
- `docs/CI_CD_ARCHITECTURE.md` - Architecture diagrams
- `.github/CI_CD_QUICKREF.md` - Quick reference
- `.github/CI_CD_ACTION_CHECKLIST.md` - Team checklist
- `.github/CI_CD_SETUP_COMPLETE.md` - Completion report

**References:**
- IMPLEMENTATION_PLAN_FOR_CODEX.md, Section 9.2
- See `.github/CI_CD_ACTION_CHECKLIST.md` for required team actions
```

---

### Issue #6: Design System & Mockups
```markdown
**Title:** Create design system and initial mockups in Figma

**Labels:** design, phase-0

**Description:**
Design key screens and components for the platform.

**Tasks:**
- [ ] Define color palette (primary, secondary, accent)
- [ ] Choose typography (fonts, sizes, weights)
- [ ] Create component library (buttons, inputs, cards)
- [ ] Design Home page
- [ ] Design Analyze page
- [ ] Design Results component
- [ ] Design mobile responsive layouts
- [ ] Export design tokens (colors, spacing)

**Acceptance Criteria:**
- Design system documented in Figma
- 5+ key screens designed
- Design tokens exported for developers

**References:**
- IMPLEMENTATION_PLAN_FOR_CODEX.md, Phase 0
```

---

## PHASE 1: MVP - Prosody Analyzer

### Week 1-2: Prosody Engine Core

---

### Issue #7: Implement Text Normalization Module
```markdown
**Title:** Implement `app/core/normalization.py` with Arabic text normalization

**Labels:** backend, phase-1, week-1-2, core-engine

**Description:**
Build text normalization functions for Arabic text processing.

**Tasks:**
- [ ] Implement `remove_diacritics()`
- [ ] Implement `normalize_hamza()`
- [ ] Implement `normalize_alef()`
- [ ] Implement `remove_tatweel()`
- [ ] Implement `normalize_arabic_text()` (main function)
- [ ] Implement `has_diacritics()`
- [ ] Write unit tests in `tests/core/test_normalization.py`
- [ ] Achieve 80%+ code coverage

**Acceptance Criteria:**
- All functions work correctly
- All unit tests pass
- Handles edge cases (empty text, non-Arabic)
- Code coverage ≥80%

**References:**
- PHASE_1_WEEK_1-2_SPEC.md, Task 1
```

---

### Issue #8: Implement Phonetic Analysis Module
```markdown
**Title:** Implement `app/core/phonetics.py` for phoneme extraction

**Labels:** backend, phase-1, week-1-2, core-engine

**Description:**
Convert Arabic text to phonetic representation for prosodic analysis.

**Tasks:**
- [ ] Create `Phoneme` dataclass
- [ ] Implement `extract_phonemes()` function
- [ ] Implement `phonemes_to_pattern()` function
- [ ] Implement `text_to_phonetic_pattern()` function
- [ ] Handle shadda (gemination)
- [ ] Handle long vowels (madd letters)
- [ ] Write unit tests in `tests/core/test_phonetics.py`

**Acceptance Criteria:**
- Correctly extracts phonemes from diacriticized text
- Handles text without diacritics (infers vowels)
- All tests pass
- Phonetic patterns match expected outputs

**References:**
- PHASE_1_WEEK_1-2_SPEC.md, Task 2
```

---

### Issue #9: Implement Taqti3 Algorithm
```markdown
**Title:** Implement `app/core/taqti3.py` for prosodic scansion

**Labels:** backend, phase-1, week-1-2, core-engine, critical

**Description:**
Implement the core taqti3 (تقطيع) algorithm to convert verses into tafa'il patterns.

**Tasks:**
- [ ] Define `BASIC_TAFAIL` dictionary (8 basic tafa'il)
- [ ] Implement `pattern_to_tafail()` function (greedy matching)
- [ ] Implement `perform_taqti3()` main function
- [ ] Write unit tests in `tests/core/test_taqti3.py`
- [ ] Test with known verses

**Acceptance Criteria:**
- Taqti3 correctly identifies tafa'il
- Works for common bahrs (Tawil, Kamil, Wafir, Ramal)
- All tests pass

**References:**
- PHASE_1_WEEK_1-2_SPEC.md, Task 3
- IMPLEMENTATION_PLAN_FOR_CODEX.md, Section 7.1
```

---

### Issue #10: Implement Bahr Detection
```markdown
**Title:** Implement `app/core/bahr_detector.py` for meter detection

**Labels:** backend, phase-1, week-1-2, core-engine, critical

**Description:**
Build bahr detector to identify which meter a verse follows.

**Tasks:**
- [ ] Create `BahrInfo` dataclass
- [ ] Define `BAHRS_DATA` with at least 4 bahrs (Tawil, Kamil, Wafir, Ramal)
- [ ] Implement `BahrDetector` class
- [ ] Implement `calculate_similarity()` method (fuzzy matching)
- [ ] Implement `detect_bahr()` method
- [ ] Implement `analyze_verse()` method (end-to-end)
- [ ] Write unit tests in `tests/core/test_bahr_detector.py`

**Acceptance Criteria:**
- Detects bahr with >70% confidence threshold
- Fuzzy matching allows for minor variations
- All tests pass

**References:**
- PHASE_1_WEEK_1-2_SPEC.md, Task 4
```

---

### Issue #11: Create Test Dataset
```markdown
**Title:** Compile test dataset of 50-100 verses across all bahrs

**Labels:** data, phase-1, week-1-2

**Description:**
Collect reference verses for testing accuracy.

**Tasks:**
- [ ] Find 10+ verses for each of 4 bahrs (Tawil, Kamil, Wafir, Ramal)
- [ ] Create `tests/fixtures/test_verses.json`
- [ ] Include metadata: poet, bahr, expected_tafail
- [ ] Verify each verse manually

**Acceptance Criteria:**
- At least 50 verses total
- All 4 bahrs covered (10+ verses each)
- JSON format matches specification
- Verses are from classical poetry (public domain)

**References:**
- PHASE_1_WEEK_1-2_SPEC.md, Task 5
```

---

### Issue #12: Accuracy Testing & Optimization
```markdown
**Title:** Implement accuracy tests and optimize engine to achieve 90%+

**Labels:** backend, phase-1, week-1-2, testing, critical

**Description:**
Test the prosody engine against reference dataset and optimize to meet 90% accuracy target.

**Tasks:**
- [ ] Implement `tests/core/test_accuracy.py`
- [ ] Run accuracy test: `test_overall_accuracy()`
- [ ] Run per-bahr accuracy test: `test_accuracy_by_bahr()`
- [ ] If accuracy <90%, debug and optimize:
  - [ ] Review phonetic analysis
  - [ ] Improve pattern matching
  - [ ] Adjust fuzzy matching threshold
  - [ ] Add more tafa'il variations
- [ ] Document accuracy results

**Acceptance Criteria:**
- Overall accuracy ≥90%
- Each bahr accuracy ≥80%
- Tests run successfully in CI

**References:**
- PHASE_1_WEEK_1-2_SPEC.md, Task 5-6
- IMPLEMENTATION_PLAN_FOR_CODEX.md, Section 8
```

---

### Week 3-4: API & Database

---

### Issue #13: Create Database Schema
```markdown
**Title:** Define SQLAlchemy models for core tables

**Labels:** backend, phase-1, week-3-4, database

**Description:**
Create database models for users, poems, verses, bahrs, and tafa'il.

**Tasks:**
- [ ] Implement `app/models/user.py`
- [ ] Implement `app/models/bahr.py`
- [ ] Implement `app/models/poem.py`
- [ ] Create `app/db/base.py` with all imports
- [ ] Create Alembic migration
- [ ] Run migration: `alembic upgrade head`
- [ ] Verify tables created in PostgreSQL

**Acceptance Criteria:**
- All models defined correctly
- Migration runs without errors
- Database schema matches specification

**References:**
- IMPLEMENTATION_PLAN_FOR_CODEX.md, Section 3
- PROJECT_STARTER_TEMPLATE.md, Section 4
```

---

### Issue #14: Seed Bahrs Data
```markdown
**Title:** Create seed script for bahrs table

**Labels:** backend, phase-1, week-3-4, database, data

**Description:**
Populate bahrs table with 16 classical Arabic meters.

**Tasks:**
- [ ] Create `scripts/seed_bahrs.py`
- [ ] Add data for all 16 bahrs:
  - [ ] الطويل, الكامل, الوافر, الرمل
  - [ ] البسيط, الخفيف, المتقارب, المتدارك
  - [ ] الهزج, الرجز, الرمل, السريع
  - [ ] المنسرح, المقتضب, المجتث, المضارع
- [ ] Include: name_ar, name_en, pattern, description, example_verse
- [ ] Run seed script
- [ ] Verify data in database

**Acceptance Criteria:**
- 16 bahrs in database
- All fields populated
- Script idempotent (can run multiple times)

**References:**
- IMPLEMENTATION_PLAN_FOR_CODEX.md, Section 3.1
```

---

### Issue #15: Implement Analyze API Endpoint
```markdown
**Title:** Create POST /api/v1/analyze endpoint

**Labels:** backend, phase-1, week-3-4, api, critical

**Description:**
Implement main analysis endpoint with caching.

**Tasks:**
- [ ] Create `app/schemas/analyze.py` (AnalyzeRequest, AnalyzeResponse)
- [ ] Create `app/api/v1/endpoints/analyze.py`
- [ ] Implement `analyze_verse()` endpoint
- [ ] Integrate prosody engine (normalization, taqti3, bahr detection)
- [ ] Add Redis caching (cache key: SHA256 hash of normalized text)
- [ ] Add error handling
- [ ] Write integration tests in `tests/api/v1/test_analyze.py`

**Acceptance Criteria:**
- Endpoint returns correct analysis
- Cache hit rate >50% in testing
- Response time <200ms (cached), <500ms (uncached)
- Swagger docs show endpoint correctly

**References:**
- IMPLEMENTATION_PLAN_FOR_CODEX.md, Section 4.2
- PROJECT_STARTER_TEMPLATE.md, Section 6
```

---

### Issue #16: Implement Bahrs API Endpoint
```markdown
**Title:** Create GET /api/v1/bahrs endpoint

**Labels:** backend, phase-1, week-3-4, api

**Description:**
Endpoint to list all available bahrs.

**Tasks:**
- [ ] Create `app/api/v1/endpoints/bahrs.py`
- [ ] Implement `list_bahrs()` endpoint
- [ ] Query bahrs from database
- [ ] Add caching (cache all bahrs, TTL: 1 day)
- [ ] Write tests

**Acceptance Criteria:**
- Returns all 16 bahrs
- Includes: id, name_ar, name_en, pattern, description
- Response cached

**References:**
- IMPLEMENTATION_PLAN_FOR_CODEX.md, Section 4.6
- PROJECT_STARTER_TEMPLATE.md, Section 6
```

---

### Issue #17: API Documentation
```markdown
**Title:** Complete API documentation with examples

**Labels:** backend, phase-1, week-3-4, documentation

**Description:**
Ensure comprehensive API documentation in Swagger.

**Tasks:**
- [ ] Add detailed descriptions to all endpoints
- [ ] Add example requests/responses in Pydantic schemas
- [ ] Add tags for endpoint grouping
- [ ] Test all examples in Swagger UI
- [ ] Write README for API usage

**Acceptance Criteria:**
- Swagger UI at `/docs` shows all endpoints
- All endpoints have descriptions
- Example requests work correctly
- README documents how to use API

**References:**
- IMPLEMENTATION_PLAN_FOR_CODEX.md, Section 4
```

---

### Week 5-6: Frontend

---

### Issue #18: Build Home Page
```markdown
**Title:** Create home page with hero section

**Labels:** frontend, phase-1, week-5-6, ui

**Description:**
Design and implement the landing page.

**Tasks:**
- [ ] Create `src/app/page.tsx`
- [ ] Design hero section with platform title
- [ ] Add tagline and description
- [ ] Add "Start Analysis" CTA button
- [ ] Make responsive (mobile, tablet, desktop)
- [ ] Test RTL layout

**Acceptance Criteria:**
- Page renders correctly with RTL
- Arabic fonts load
- Mobile responsive
- CTA links to `/analyze`

**References:**
- IMPLEMENTATION_PLAN_FOR_CODEX.md, Phase 1, Week 5-6
- PROJECT_STARTER_TEMPLATE.md, Section 9
```

---

### Issue #19: Build Analyze Page
```markdown
**Title:** Create analyze page with form and results

**Labels:** frontend, phase-1, week-5-6, ui, critical

**Description:**
Main analysis interface where users input verses and see results.

**Tasks:**
- [ ] Create `src/app/analyze/page.tsx`
- [ ] Create `src/components/AnalyzeForm.tsx`
  - [ ] Textarea for verse input
  - [ ] Submit button
  - [ ] Form validation (Zod schema)
- [ ] Create `src/components/AnalyzeResults.tsx`
  - [ ] Display taqti3
  - [ ] Display bahr name with confidence
  - [ ] Display quality score
  - [ ] Visualize pattern (optional)
- [ ] Integrate with API (`src/lib/api.ts`)
- [ ] Add loading states
- [ ] Add error handling

**Acceptance Criteria:**
- Form accepts Arabic text
- Calls `/api/v1/analyze` on submit
- Displays results correctly
- Shows loading spinner during analysis
- Handles errors gracefully

**References:**
- IMPLEMENTATION_PLAN_FOR_CODEX.md, Phase 1, Week 5-6
- PROJECT_STARTER_TEMPLATE.md, Section 9
```

---

### Issue #20: Implement API Client
```markdown
**Title:** Create API client with Axios and React Query

**Labels:** frontend, phase-1, week-5-6

**Description:**
Setup API client for backend communication.

**Tasks:**
- [ ] Create `src/lib/api.ts` with Axios instance
- [ ] Add request/response interceptors
- [ ] Implement `analyzeVerse()` function
- [ ] Implement `getBahrs()` function
- [ ] Create custom hooks with React Query:
  - [ ] `src/hooks/useAnalyze.ts`
  - [ ] `src/hooks/useBahrs.ts`
- [ ] Add error handling

**Acceptance Criteria:**
- API client makes successful requests
- Auth token added to requests (if present)
- React Query hooks work correctly
- Errors handled and displayed to user

**References:**
- PROJECT_STARTER_TEMPLATE.md, Section 9
```

---

### Issue #21: Mobile Responsive Design
```markdown
**Title:** Ensure all pages are mobile responsive

**Labels:** frontend, phase-1, week-5-6, ui

**Description:**
Test and fix responsive design for mobile devices.

**Tasks:**
- [ ] Test Home page on mobile (375px, 768px, 1024px)
- [ ] Test Analyze page on mobile
- [ ] Adjust Tailwind breakpoints if needed
- [ ] Test RTL layout on mobile
- [ ] Test Arabic fonts render correctly on mobile

**Acceptance Criteria:**
- All pages work on mobile (375px width)
- No horizontal scroll
- Text readable
- Buttons tappable (44px minimum)

**References:**
- IMPLEMENTATION_PLAN_FOR_CODEX.md, Phase 1, Week 5-6
```

---

### Week 7-8: Testing & Deployment

---

### Issue #22: Integration Testing
```markdown
**Title:** Write end-to-end integration tests

**Labels:** backend, testing, phase-1, week-7-8

**Description:**
Test complete user flows from API request to response.

**Tasks:**
- [ ] Test full analyze flow
- [ ] Test caching behavior
- [ ] Test error cases (invalid input, server error)
- [ ] Test database interactions
- [ ] Achieve 80%+ test coverage

**Acceptance Criteria:**
- All integration tests pass
- Coverage ≥80%
- Tests run in CI pipeline

**References:**
- IMPLEMENTATION_PLAN_FOR_CODEX.md, Section 8
```

---

### Issue #23: Load Testing
```markdown
**Title:** Perform load testing with 100 concurrent users

**Labels:** backend, testing, phase-1, week-7-8, performance

**Description:**
Test system performance under load.

**Tasks:**
- [ ] Setup load testing tool (Locust or k6)
- [ ] Create test scenarios (analyze endpoint)
- [ ] Run test with 100 concurrent users
- [ ] Measure response times (p50, p95, p99)
- [ ] Identify bottlenecks
- [ ] Optimize slow queries/operations

**Acceptance Criteria:**
- p95 response time <500ms
- System handles 100 concurrent users
- No errors under load

**References:**
- IMPLEMENTATION_PLAN_FOR_CODEX.md, Phase 1, Week 7-8
```

---

### Issue #24: Deploy to Staging
```markdown
**Title:** Deploy application to staging environment

**Labels:** devops, phase-1, week-7-8, deployment

**Description:**
Deploy backend and frontend to staging server.

**Tasks:**
- [ ] Choose hosting (Railway, Render, or DigitalOcean)
- [ ] Deploy backend
  - [ ] Connect to managed PostgreSQL
  - [ ] Connect to managed Redis
  - [ ] Set environment variables
- [ ] Deploy frontend
  - [ ] Set `NEXT_PUBLIC_API_URL`
- [ ] Run database migrations on staging
- [ ] Seed bahrs data on staging
- [ ] Test all endpoints on staging
- [ ] Document staging URLs

**Acceptance Criteria:**
- Staging environment accessible
- All API endpoints work
- Frontend connects to backend
- Database populated

**References:**
- IMPLEMENTATION_PLAN_FOR_CODEX.md, Section 9.2
```

---

### Issue #25: Beta Testing & Bug Fixes
```markdown
**Title:** Recruit 10 beta testers and fix critical bugs

**Labels:** testing, phase-1, week-7-8, user-research

**Description:**
Gather feedback from real users and iterate.

**Tasks:**
- [ ] Recruit 10 beta testers (students, poets, teachers)
- [ ] Create feedback form (Google Forms or Typeform)
- [ ] Send staging URL to testers
- [ ] Collect feedback (usability, accuracy, bugs)
- [ ] Prioritize bugs (P0, P1, P2)
- [ ] Fix P0 and P1 bugs
- [ ] Document feedback for future iterations

**Acceptance Criteria:**
- 10+ testers provide feedback
- Critical bugs fixed
- Feedback documented

**References:**
- IMPLEMENTATION_PLAN_FOR_CODEX.md, Phase 1, Week 7-8
```

---

## Quick Reference: Labels

### By Area
- `backend` - Backend/API work
- `frontend` - Frontend/UI work
- `devops` - Infrastructure/deployment
- `database` - Database schema/migrations
- `testing` - Tests
- `documentation` - Docs
- `design` - UI/UX design

### By Priority
- `critical` - Must be done for phase completion
- `high` - Important but not blocking
- `medium` - Nice to have
- `low` - Future enhancement

### By Phase
- `phase-0` - Pre-development
- `phase-1` - MVP
- `phase-2` - AI Poet
- `phase-3` - Competition Arena

### By Type
- `setup` - Initial setup
- `feature` - New feature
- `bug` - Bug fix
- `enhancement` - Improvement
- `research` - Research task

---

## Project Board Columns

1. **📋 Backlog** - Not started, prioritized
2. **🚀 In Progress** - Currently being worked on
3. **👀 Review** - Code review needed
4. **✅ Done** - Completed and merged

---

## Sprint Planning Template

### Sprint 1 (Week 1-2): Prosody Engine Core
**Goal:** Build and test core taqti3 algorithm

**Issues:** #7, #8, #9, #10, #11, #12

**Success Criteria:**
- Prosody engine achieves 90%+ accuracy
- All unit tests pass
- Code coverage ≥80%

---

### Sprint 2 (Week 3-4): API & Database
**Goal:** Expose analysis functionality via REST API

**Issues:** #13, #14, #15, #16, #17

**Success Criteria:**
- `/analyze` endpoint works correctly
- API documented in Swagger
- Response time <500ms

---

### Sprint 3 (Week 5-6): Frontend
**Goal:** Build user interface for analysis

**Issues:** #18, #19, #20, #21

**Success Criteria:**
- Users can analyze verses via web interface
- Mobile responsive
- API integration works

---

### Sprint 4 (Week 7-8): Testing & Deployment
**Goal:** Launch staging environment

**Issues:** #22, #23, #24, #25

**Success Criteria:**
- Staging environment live
- 10+ beta testers provide feedback
- Critical bugs fixed

---

## Progress Tracking

### Phase 1 Progress
- [ ] Week 1-2: Prosody Engine (6 issues)
- [ ] Week 3-4: API & Database (5 issues)
- [ ] Week 5-6: Frontend (4 issues)
- [ ] Week 7-8: Testing & Deployment (4 issues)

**Total:** 19 issues for Phase 1 MVP

---

## Notes for GitHub Setup

1. **Create labels** in GitHub repo settings
2. **Create milestones** for each phase
3. **Copy issues** using the templates above
4. **Create project board** (Kanban view)
5. **Assign issues** to team members or yourself
6. **Link issues to PRs** using keywords like "Closes #7"

---

## Example GitHub Issue Commands

```bash
# Close issue from commit
git commit -m "Implement text normalization module. Closes #7"

# Reference issue
git commit -m "Add tests for phonetics module (ref #8)"

# Multiple issues
git commit -m "Complete prosody engine. Closes #7, #8, #9"
```

---

## Ready to Start! 🚀

Your project tracker is complete. Next steps:
1. Create GitHub repository
2. Add these issues
3. Start with Sprint 1 (Week 1-2)
4. Update progress as you go

Good luck building BAHR! 🎭
