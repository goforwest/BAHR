# BAHR Implementation Guides

**Project:** بَحْر (BAHR) - AI-Powered Arabic Poetry Analysis Platform
**Purpose:** Production-ready, step-by-step implementation guides for LLM-based code generation
**Target Audience:** Development teams, AI coding assistants (Claude Code, GitHub Copilot, GPT-4)
**Documentation Status:** ✅ Complete (95% coverage, 42 technical docs)
**Last Updated:** November 8, 2025

---

## 📚 Guide Structure

This directory contains **14 feature-specific implementation guides** + **1 top-level application guide**, each providing:

1. **Objective & Architecture** – What to build and why
2. **Input/Output Contracts** – API schemas, data structures
3. **Implementation Steps** – Numbered, executable instructions
4. **Code Templates** – Copy-paste reference implementations
5. **Testing Strategy** – Unit, integration, E2E test plans
6. **Deployment Checklist** – CI/CD, rollout, monitoring
7. **Observability** – Metrics, logs, alerts
8. **Security & Safety** – Vulnerability mitigations
9. **Documentation References** – Line-by-line citations to source docs

---

## 🎯 Quick Start

### For Developers
1. **Start here:** Read [`app.md`](./app.md) for system-wide architecture
2. **Pick a feature:** Choose from the list below based on your sprint
3. **Follow the guide:** Execute steps in order, copy code templates
4. **Run tests:** Use provided test cases to verify implementation
5. **Deploy:** Follow CI/CD checklist for staging/production

### For AI Coding Assistants
Each guide is structured as a **reproducible prompt** that can be:
- Fed directly to Codex/Claude Code/GPT-4 for code generation
- Used as context for multi-turn coding sessions
- Referenced for debugging and code reviews

---

## 📖 Guide Index

### Core Application
- **[`app.md`](./app.md)** – End-to-end application architecture, deployment, operations

### Backend Features (Python/FastAPI)
1. **[`feature-authentication-jwt.md`](./feature-authentication-jwt.md)**
   JWT auth, password hashing (bcrypt), user registration/login

2. **[`feature-arabic-text-normalization.md`](./feature-arabic-text-normalization.md)**
   8-stage Arabic text preprocessing pipeline (CAMeL Tools integration)

3. **[`feature-syllable-segmentation.md`](./feature-syllable-segmentation.md)**
   Taqti' algorithm, phonetic transcription, syllable weight calculation

4. **[`feature-meter-detection.md`](./feature-meter-detection.md)**
   16 classical Arabic meters, fuzzy pattern matching, confidence calibration

5. **[`feature-analysis-api.md`](./feature-analysis-api.md)**
   REST endpoints for verse analysis (POST /analyze, batch processing)

6. **[`feature-caching-redis.md`](./feature-caching-redis.md)**
   Redis caching strategy, cache key design, TTL policies

7. **[`feature-rate-limiting.md`](./feature-rate-limiting.md)**
   Sliding window rate limiter, 100 req/hour enforcement

8. **[`feature-monitoring-observability.md`](./feature-monitoring-observability.md)**
   Prometheus metrics, Grafana dashboards, alerting rules

9. **[`feature-database-orm.md`](./feature-database-orm.md)**
   PostgreSQL schema, SQLAlchemy models, Alembic migrations

10. **[`feature-response-envelope.md`](./feature-response-envelope.md)**
    Standardized JSON response wrapper, error formatting

11. **[`feature-error-handling.md`](./feature-error-handling.md)**
    Error taxonomy (ERR_INPUT_*, ERR_AUTH_*), bilingual messages

### Frontend Features (Next.js/TypeScript)
12. **[`feature-frontend-nextjs.md`](./feature-frontend-nextjs.md)**
    RTL support, analysis form, prosody visualization, TanStack Query

### Data & DevOps
13. **[`feature-dataset-management.md`](./feature-dataset-management.md)**
    JSONL dataset format, validation scripts, labeling workflows

14. **[`feature-deployment-cicd.md`](./feature-deployment-cicd.md)**
    Docker Compose, GitHub Actions, Railway/Vercel deployment

---

## 🛠️ Technology Stack

### Backend
- **Language:** Python 3.11+
- **Framework:** FastAPI 0.104+
- **ORM:** SQLAlchemy 2.0+
- **Database:** PostgreSQL 15 (with pgvector)
- **Cache:** Redis 7
- **NLP:** CAMeL Tools 1.5.2, PyArabic
- **Testing:** pytest, pytest-cov (≥70% coverage)
- **Linting:** Black, Flake8, mypy

### Frontend
- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript 5+
- **UI:** Tailwind CSS + shadcn/ui
- **State:** Zustand / TanStack Query
- **Forms:** React Hook Form + Zod

### DevOps
- **Containers:** Docker + Docker Compose
- **CI/CD:** GitHub Actions
- **Hosting:** Railway (backend), Vercel (frontend)
- **Monitoring:** Prometheus + Grafana
- **Logging:** Structured JSON (request_id)

---

## 📐 Architecture Principles

All guides adhere to these principles (cited from `docs/technical/ARCHITECTURE_OVERVIEW.md`):

1. **Interface-Driven Design**
   Clear contracts: `ITextNormalizer`, `ISyllableSegmenter`, `IMeterMatcher`, etc.

2. **Response Envelope Pattern**
   ```json
   {
     "success": true,
     "data": {...},
     "meta": {"request_id": "...", "timestamp": "..."}
   }
   ```

3. **Error Taxonomy**
   Structured error codes: `ERR_INPUT_002`, `ERR_AUTH_001`, etc.

4. **Performance Targets**
   - P95 latency < 600ms
   - Meter accuracy ≥ 70%
   - Cache hit ratio > 40%

5. **Security-First**
   - bcrypt (rounds=12), JWT tokens, rate limiting, input validation

6. **Observable Systems**
   - Prometheus metrics, structured logs, distributed tracing

---

## 🔗 Source Documentation References

All guides map to authoritative source documentation:

| Topic | Source Document | Location |
|-------|-----------------|----------|
| Architecture | `docs/technical/ARCHITECTURE_OVERVIEW.md` | Lines 1-272 |
| Prosody Engine | `docs/technical/PROSODY_ENGINE.md` | 2570 lines |
| API Spec | `docs/technical/API_SPECIFICATION.yaml` | OpenAPI 3.0.3 |
| Database Schema | `docs/technical/DATABASE_SCHEMA.md` | 1779 lines |
| Security | `docs/technical/SECURITY.md` | Week 1 checklist |
| Deployment | `docs/technical/DEPLOYMENT_GUIDE.md` | Docker, Railway |
| Performance | `docs/technical/PERFORMANCE_TARGETS.md` | SLOs, metrics |
| Error Handling | `docs/technical/ERROR_HANDLING_STRATEGY.md` | Taxonomy |

---

## ✅ Prerequisites

Before using these guides, ensure:

### Development Environment
- [ ] Python 3.11+ installed
- [ ] Node.js 18+ and npm/pnpm installed
- [ ] Docker Desktop running (for local dev)
- [ ] Git configured
- [ ] IDE/editor with Python + TypeScript support

### Critical Day 1 Task (M1/M2 Macs)
- [ ] Test CAMeL Tools compatibility (see `docs/PHASE_0_SETUP.md:Section 4.5`)
  ```bash
  # Test native ARM64
  arch -arm64 pip install camel-tools==1.5.2
  python -c "from camel_tools import __version__; print(__version__)"
  ```
- [ ] Fallback to Docker if incompatible

### Knowledge Requirements
- Python async/await, type hints
- FastAPI basics (routers, dependencies, middleware)
- SQLAlchemy ORM
- PostgreSQL fundamentals
- Redis caching concepts
- React/Next.js (for frontend)
- Docker Compose
- Basic Arabic linguistics (understanding of تفاعيل / buhūr)

---

## 🧪 Testing Philosophy

All guides include **3-tier testing pyramid**:

| Layer | Coverage | Focus |
|-------|----------|-------|
| **Unit** (80%) | Individual functions | Normalizer, segmenter, matcher logic |
| **Integration** (15%) | API endpoints | Request/response contracts |
| **E2E** (5%) | Full user flows | Register → Login → Analyze |

**Coverage Targets:**
- Normalizer: ≥80%
- Prosody Engine: ≥75%
- API Endpoints: ≥70%
- **Overall: ≥70%**

---

## 🚀 Implementation Timeline

Guides are organized to support this **14-week development plan**:

```yaml
Week 1-2:   Backend infrastructure (Auth, DB, Docker)
Week 3-5:   Prosody engine (Normalizer, Segmenter, Matcher)
Week 6:     API integration
Week 7-8:   Frontend (Next.js)
Week 9-10:  Testing & optimization
Week 11-12: Beta deployment
Week 13:    Production launch
Week 14:    Buffer week
```

**Daily Workflow:**
1. Morning: Pick feature guide
2. Implement: Follow numbered steps
3. Test: Run provided test cases
4. Commit: Use conventional commits (`feat(prosody): add al-tawil meter`)
5. Update: Log progress in `docs/project-management/PROGRESS_LOG_CURRENT.md`

---

## 🎯 Success Criteria

Implementation is complete when:

### Functional Requirements
- [ ] User can register/login with JWT auth
- [ ] User can analyze Arabic verse (POST /api/v1/analyses)
- [ ] System detects meter with ≥70% accuracy (golden set)
- [ ] Results display meter, confidence, syllable pattern
- [ ] Rate limiting enforced (100 req/hour)

### Technical Requirements
- [ ] API P95 latency < 600ms
- [ ] Test coverage ≥70%
- [ ] Docker Compose runs all services
- [ ] Prometheus metrics exposed
- [ ] CI/CD pipeline passes

### Security Requirements
- [ ] Passwords hashed (bcrypt, cost=12)
- [ ] JWT tokens expire (access: 30min, refresh: 7d)
- [ ] Input validation prevents XSS/SQL injection
- [ ] HTTPS enforced in production

---

## 📞 Getting Help

### Documentation Lookup
```yaml
"How do I...?"
  - Normalize Arabic text → feature-arabic-text-normalization.md
  - Implement JWT auth → feature-authentication-jwt.md
  - Deploy to production → feature-deployment-cicd.md
  - Setup monitoring → feature-monitoring-observability.md
  - Define database schema → feature-database-orm.md
```

### Source Documentation
- **Quick Start:** `docs/START_HERE.md` (10-min read)
- **Architecture:** `docs/technical/ARCHITECTURE_OVERVIEW.md`
- **Timeline:** `docs/planning/PROJECT_TIMELINE.md`
- **Deferred Features:** `docs/planning/DEFERRED_FEATURES.md` (scope control)

### Common Issues
- **M1/M2 CAMeL Tools fails:** Use Docker with `--platform linux/amd64`
- **Accuracy < 70%:** Pivot to 10 most common meters (see `docs/planning/TECHNICAL_ASSUMPTIONS.md:180`)
- **Performance > 1s:** Enable aggressive caching (TTL 3600s)

---

## 🔄 Version Control

### Git Workflow
```bash
# Feature branch naming
git checkout -b feature/agent-b-prosody

# Conventional commits
git commit -m "feat(prosody): implement al-tawil meter detection"
git commit -m "fix(api): handle empty verse input correctly"
git commit -m "test(normalizer): add 100+ edge case tests"
```

**Types:** `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

### Branching Strategy
```
main (production)
└── develop (integration)
    ├── feature/authentication
    ├── feature/prosody-engine
    ├── feature/analysis-api
    └── feature/frontend
```

---

## 📊 Progress Tracking

Update `docs/project-management/PROGRESS_LOG_CURRENT.md` daily (5 minutes):

```markdown
## [Agent B] - 2025-11-10

### Completed:
- ✅ Implemented ArabicTextNormalizer (8 stages)
- ✅ Added 100+ edge case tests

### In Progress:
- 🟡 SyllableSegmenter (60% complete)

### Blockers:
- None

### Next:
- Implement Shadda expansion logic
- Test CAMeL Tools morphological analyzer
```

---

## ⚠️ Critical Warnings

### DO NOT:
- ❌ Skip documentation review – Always consult source docs first
- ❌ Implement deferred features – Check `DEFERRED_FEATURES.md`
- ❌ Skip M1/M2 testing – Test CAMeL Tools Day 1 Hour 1
- ❌ Hardcode credentials – Use `.env` variables
- ❌ Commit to main directly – Use feature branches
- ❌ Deploy without migrations – Run `alembic upgrade head`

### DO:
- ✅ Reference documentation line numbers (e.g., "Per PROSODY_ENGINE.md:540")
- ✅ Write tests before implementation (TDD)
- ✅ Use conventional commits
- ✅ Validate Arabic input (≥70% Arabic characters)
- ✅ Cache analysis results (24-hour TTL)
- ✅ Log with `request_id` for distributed tracing

---

## 📄 License & Contribution

These implementation guides are part of the BAHR project documentation. They are:
- **Reproducible:** Exact commands, package versions, expected outputs
- **Traceable:** Every design choice maps to source documentation
- **Executable:** Copy-paste code templates work out-of-the-box
- **Testable:** Comprehensive test plans included

**Maintenance:** Update guides when `CRITICAL_CHANGES.md` is modified.

---

## 🎓 Learning Path

**For new developers:**
1. Read `app.md` (30 min) – Understand overall system
2. Read `feature-authentication-jwt.md` (20 min) – Learn auth flow
3. Read `feature-analysis-api.md` (30 min) – Understand core API
4. Read `feature-arabic-text-normalization.md` (45 min) – Deep dive into NLP
5. Start coding! 🚀

**For AI assistants:**
- Use `app.md` as system context
- Feed feature guides as prompts for code generation
- Validate outputs against provided test cases
- Cross-reference with source documentation

---

**Last Updated:** November 8, 2025
**Status:** ✅ Production-ready
**Total Guides:** 15 (1 app + 14 features)
**Total Documentation:** 42 source files, 95% coverage

**Ready to build? Start with [`app.md`](./app.md)** 🚀
