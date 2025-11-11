# 🗺️ BAHR Repository Structure

**Quick Visual Reference Guide**  
**Version:** 2.0 (Post-Restructure)  
**Last Updated:** November 10, 2025

---

## 📁 Complete Repository Tree

```
BAHR/
├── 📄 README.md                      # Main project overview
├── 📄 LICENSE                        # MIT License
├── 📄 CONTRIBUTING.md                # Contribution guidelines
├── 📄 CHANGELOG.md                   # Project changelog
├── 📄 REPOSITORY_STRUCTURE.md        # This file
├── 📄 .gitignore                     # Git ignore rules
├── 📄 .python-version                # Python version specification
├── 📄 .env.example                   # Environment variables template
│
├── 🔧 .github/                       # GitHub configuration
│   ├── workflows/                    # CI/CD pipelines
│   │   ├── backend.yml               # Backend testing & validation
│   │   ├── frontend.yml              # Frontend building & testing
│   │   ├── deploy.yml                # Production deployment
│   │   ├── test-golden-set.yml       # Dataset validation
│   │   └── docs-validation.yml       # Documentation link checking
│   ├── ISSUE_TEMPLATE/               # Issue templates (if exists)
│   └── PULL_REQUEST_TEMPLATE.md      # PR template (if exists)
│
├── 🐍 backend/                       # Backend Application
│   ├── 📄 README.md                  # Backend-specific documentation
│   ├── 📄 requirements.txt           # Python dependencies
│   ├── 📄 pytest.ini                 # Backend test configuration
│   ├── 📄 pyproject.toml             # Python project metadata
│   ├── 📄 runtime.txt                # Python runtime version
│   ├── 📄 Procfile                   # Railway start command
│   ├── 📄 .env.example               # Backend env template
│   ├── 📄 .dockerignore              # Docker ignore rules
│   │
│   ├── 📦 app/                       # Main application package
│   │   ├── __init__.py
│   │   ├── main.py                   # FastAPI application entry
│   │   ├── config.py                 # Configuration management
│   │   ├── exceptions.py             # Custom exception classes
│   │   ├── response_envelope.py      # API response wrapper
│   │   │
│   │   ├── api/                      # API layer (REST endpoints)
│   │   │   ├── __init__.py
│   │   │   └── v1/                   # API version 1
│   │   │       ├── __init__.py
│   │   │       ├── router.py         # Main API router
│   │   │       └── endpoints/        # Endpoint modules
│   │   │           ├── __init__.py
│   │   │           ├── analyze.py    # Poetry analysis endpoint
│   │   │           ├── auth.py       # Authentication endpoints
│   │   │           ├── health.py     # Health check endpoint
│   │   │           └── bahrs.py      # Meter reference endpoints
│   │   │
│   │   ├── core/                     # Business logic (Prosody Engine)
│   │   │   ├── __init__.py
│   │   │   ├── bahr_detector.py      # Meter detection algorithm
│   │   │   ├── normalization.py      # Arabic text normalization
│   │   │   ├── phonetics.py          # Phonetic processing
│   │   │   ├── taqti3.py             # Syllable segmentation (تقطيع)
│   │   │   └── quality.py            # Quality assessment
│   │   │
│   │   ├── database/                 # Database layer
│   │   │   ├── __init__.py
│   │   │   ├── session.py            # SQLAlchemy session management
│   │   │   ├── redis.py              # Redis connection & caching
│   │   │   │
│   │   │   └── migrations/           # Alembic database migrations
│   │   │       ├── alembic.ini       # Alembic configuration
│   │   │       ├── env.py            # Migration environment
│   │   │       ├── script.py.mako    # Migration template
│   │   │       └── versions/         # Migration version files
│   │   │           └── *.py
│   │   │
│   │   ├── models/                   # SQLAlchemy ORM models
│   │   │   ├── __init__.py
│   │   │   ├── base.py               # Base model class
│   │   │   ├── bahr.py               # Bahr (meter) model
│   │   │   ├── user.py               # User model
│   │   │   └── analysis.py           # Analysis result model
│   │   │
│   │   ├── schemas/                  # Pydantic validation schemas
│   │   │   ├── __init__.py
│   │   │   ├── analyze.py            # Analysis request/response
│   │   │   ├── auth.py               # Authentication schemas
│   │   │   └── bahr.py               # Bahr schemas
│   │   │
│   │   ├── middleware/               # Request/response middleware
│   │   │   ├── __init__.py
│   │   │   ├── response_envelope.py  # Response envelope wrapper
│   │   │   ├── util_request_id.py    # Request ID tracking
│   │   │   └── rate_limiting.py      # Rate limiting (if exists)
│   │   │
│   │   ├── metrics/                  # Observability & metrics
│   │   │   ├── __init__.py
│   │   │   └── analysis_metrics.py   # Prometheus metrics
│   │   │
│   │   ├── nlp/                      # NLP utilities
│   │   │   ├── __init__.py
│   │   │   └── normalizer.py         # Arabic text normalizer
│   │   │
│   │   └── prosody/                  # Prosody analysis engine
│   │       ├── __init__.py
│   │       ├── engine.py             # Prosody pattern engine
│   │       └── segmenter.py          # Syllable segmenter
│   │
│   ├── tests/                        # Backend test suite
│   │   ├── __init__.py
│   │   ├── conftest.py               # Pytest configuration & fixtures
│   │   │
│   │   ├── api/                      # API endpoint tests
│   │   │   └── v1/
│   │   │       └── test_analyze.py
│   │   │
│   │   ├── core/                     # Core logic tests
│   │   │   ├── test_bahr_detector.py
│   │   │   ├── test_normalization.py
│   │   │   ├── test_phonetics.py
│   │   │   ├── test_taqti3.py
│   │   │   └── test_accuracy.py
│   │   │
│   │   └── unit/                     # Unit tests
│   │       ├── test_engine.py
│   │       ├── test_normalizer.py
│   │       ├── test_segmenter.py
│   │       └── test_envelope.py
│   │
│   ├── scripts/                      # Backend-specific scripts
│   │   ├── seed_bahrs.py             # Seed meter database
│   │   └── seed_database.py          # Database initialization
│   │
│   └── requirements/                 # Dependency specifications
│       ├── base.txt                  # Production dependencies
│       ├── development.txt           # Development dependencies
│       └── production.txt            # Production-only dependencies
│
├── ⚛️  frontend/                     # Frontend Application
│   ├── 📄 README.md                  # Frontend documentation (English)
│   ├── 📄 README_AR.md               # Frontend documentation (Arabic)
│   ├── 📄 package.json               # npm dependencies & scripts
│   ├── 📄 tsconfig.json              # TypeScript configuration
│   ├── 📄 next.config.ts             # Next.js configuration
│   ├── 📄 components.json            # shadcn/ui configuration
│   ├── 📄 eslint.config.mjs          # ESLint configuration
│   ├── 📄 postcss.config.mjs         # PostCSS configuration
│   ├── 📄 nixpacks.toml              # Railway Nixpacks config
│   ├── 📄 next-env.d.ts              # Next.js TypeScript types
│   │
│   ├── src/                          # Source code
│   │   ├── app/                      # Next.js App Router
│   │   │   ├── layout.tsx            # Root layout
│   │   │   ├── page.tsx              # Home page
│   │   │   ├── globals.css           # Global styles
│   │   │   └── analyze/              # Analysis feature
│   │   │       └── page.tsx
│   │   │
│   │   └── lib/                      # Utilities & helpers
│   │       ├── api.ts                # API client
│   │       └── utils.ts              # Utility functions
│   │
│   ├── components/                   # React components
│   │   └── ui/                       # shadcn/ui components
│   │
│   └── public/                       # Static assets
│       └── fonts/                    # Custom fonts
│
├── 📊 dataset/                       # Dataset & Evaluation
│   ├── 📄 README.md                  # Dataset documentation
│   ├── 📄 pytest.ini                 # Dataset test configuration
│   ├── 📄 analyze_golden_set.py      # Golden set analyzer
│   │
│   ├── evaluation/                   # Evaluation data
│   │   ├── 📄 README.md              # Evaluation guide
│   │   ├── 📄 golden_set.json        # Annotated test verses
│   │   └── 📄 schema.json            # JSON schema
│   │
│   ├── scripts/                      # Data processing scripts
│   │   └── (various processing tools)
│   │
│   └── tests/                        # Dataset validation tests
│       ├── test_golden_set_loader.py
│       └── test_schema_validation.py
│
├── 📖 docs/                          # Unified Documentation Hub
│   ├── 📄 README.md                  # Documentation index
│   ├── 📄 QUICK_REFERENCE.md         # Fast navigation guide
│   │
│   ├── architecture/                 # System Architecture
│   │   ├── 📄 README.md              # Architecture index
│   │   ├── 📄 OVERVIEW.md            # High-level system design
│   │   ├── 📄 DECISIONS.md           # Architecture Decision Records
│   │   ├── 📄 COMPONENT_DIAGRAMS.md  # Visual diagrams
│   │   └── 📄 DATA_FLOW.md           # Data flow documentation
│   │
│   ├── features/                     # Feature Implementation Guides
│   │   ├── 📄 README.md              # Features index
│   │   ├── 📄 analysis-api.md
│   │   ├── 📄 arabic-text-normalization.md
│   │   ├── 📄 authentication-jwt.md
│   │   ├── 📄 caching-redis.md
│   │   ├── 📄 database-orm.md
│   │   ├── 📄 dataset-management.md
│   │   ├── 📄 deployment-cicd.md
│   │   ├── 📄 error-handling.md
│   │   ├── 📄 frontend-nextjs.md
│   │   ├── 📄 meter-detection.md
│   │   ├── 📄 monitoring-observability.md
│   │   ├── 📄 rate-limiting.md
│   │   ├── 📄 response-envelope.md
│   │   └── 📄 syllable-segmentation.md
│   │
│   ├── technical/                    # Technical Specifications
│   │   ├── 📄 BACKEND_API.md         # API documentation
│   │   ├── 📄 DATABASE_SCHEMA.md     # Database design
│   │   ├── 📄 FRONTEND_GUIDE.md      # Frontend architecture
│   │   ├── 📄 PROSODY_ENGINE.md      # Prosody algorithm
│   │   ├── 📄 SECURITY.md            # Security guidelines
│   │   ├── 📄 PERFORMANCE_TARGETS.md # Performance metrics
│   │   └── 📄 METRICS_REFERENCE.md   # Observability metrics
│   │
│   ├── deployment/                   # Deployment Guides
│   │   ├── 📄 RAILWAY_QUICK_START.md
│   │   ├── 📄 RAILWAY_DOCKER_GUIDE.md
│   │   └── 📄 ENVIRONMENT_SETUP.md
│   │
│   ├── devops/                       # DevOps Documentation
│   │   ├── 📄 CI_CD_COMPLETE_GUIDE.md
│   │   ├── 📄 DOCKER_SETUP.md
│   │   └── 📄 MONITORING_SETUP.md
│   │
│   ├── guides/                       # How-To Guides
│   │   ├── 📄 ANALYZE_ENDPOINT_QUICKSTART.md
│   │   ├── 📄 TESTING_GUIDE.md
│   │   └── 📄 TROUBLESHOOTING.md
│   │
│   ├── onboarding/                   # New Developer Onboarding
│   │   ├── 📄 GETTING_STARTED.md
│   │   └── 📄 DEVELOPMENT_SETUP.md
│   │
│   ├── planning/                     # Project Planning
│   │   ├── 📄 IMPLEMENTATION_ROADMAP.md
│   │   ├── 📄 PROJECT_TIMELINE.md
│   │   └── 📄 MILESTONES.md
│   │
│   ├── project-management/           # Project Management
│   │   ├── 📄 PROGRESS_LOG_CURRENT.md
│   │   ├── 📄 GITHUB_ISSUES_TEMPLATE.md
│   │   └── 📄 WORKFLOW_GUIDE.md
│   │
│   ├── research/                     # Research & References
│   │   ├── 📄 ARABIC_NLP_RESEARCH.md
│   │   └── 📄 PROSODY_REFERENCES.md
│   │
│   ├── checklists/                   # Implementation Checklists
│   │   ├── 📄 PRE_WEEK_1_FINAL.md
│   │   ├── 📄 WEEK_1_CRITICAL.md
│   │   └── 📄 DEPLOYMENT_CHECKLIST.md
│   │
│   ├── testing/                      # Testing Documentation
│   │   ├── 📄 TESTING_STRATEGY.md
│   │   └── 📄 TEST_DATA_GUIDE.md
│   │
│   ├── vision/                       # Vision & Strategy
│   │   ├── 📄 MASTER_PLAN.md
│   │   └── 📄 PRODUCT_VISION.md
│   │
│   ├── workflows/                    # Development Workflows
│   │   └── 📄 DEVELOPMENT_WORKFLOW.md
│   │
│   └── templates/                    # Document Templates
│       ├── 📄 ADR_TEMPLATE.md
│       └── 📄 FEATURE_TEMPLATE.md
│
├── 🏗️ infrastructure/                # Infrastructure as Code
│   ├── 📄 README.md                  # Infrastructure guide
│   │
│   ├── docker/                       # Docker configurations
│   │   ├── 📄 docker-compose.yml     # Multi-service orchestration
│   │   │
│   │   ├── backend/                  # Backend Docker configs
│   │   │   ├── Dockerfile.dev        # Development image
│   │   │   └── Dockerfile.prod       # Production image
│   │   │
│   │   └── frontend/                 # Frontend Docker configs (if needed)
│   │
│   ├── railway/                      # Railway deployment configs
│   │   ├── 📄 railway.toml           # Monorepo configuration
│   │   ├── 📄 backend.json           # Backend service config
│   │   └── 📄 frontend.json          # Frontend service config
│   │
│   └── nginx/                        # Nginx configs (if needed)
│
├── 🔧 scripts/                       # Repository-Wide Scripts
│   ├── 📄 README.md                  # Scripts inventory
│   │
│   ├── setup/                        # Setup & initialization scripts
│   │   ├── verify_setup.sh
│   │   ├── setup-branch-protection.sh
│   │   └── fix-workflow-dispatch.sh
│   │
│   ├── health/                       # Health check scripts
│   │   ├── health_check.sh
│   │   └── verify_deployment.sh
│   │
│   ├── testing/                      # Testing automation scripts
│   │   ├── test-ci-local.sh
│   │   ├── test_analyze_endpoint.sh
│   │   ├── test_redis_caching.py
│   │   └── verify_redis_caching.sh
│   │
│   └── deployment/                   # Deployment automation
│       └── (deployment scripts)
│
└── 📦 archive/                       # Historical Documentation
    ├── 📄 README.md                  # Archive guide
    ├── blockers/
    ├── checklists/
    ├── dataset/
    ├── deployment/
    ├── implementation/
    ├── integration/
    ├── milestones/
    ├── plans/
    ├── progress/
    └── reviews/
```

---

## 🎯 Quick Navigation Guide

### I want to...

#### **Develop Backend Features**
→ Start in `/backend/app/` - organized by layer (api, core, database, models, schemas)

#### **Develop Frontend Features**
→ Start in `/frontend/src/app/` - Next.js App Router structure

#### **Run Tests**
→ Backend: `cd backend && pytest`  
→ Dataset: `pytest dataset/tests/`

#### **Run Database Migrations**
→ `cd backend && alembic -c database/migrations/alembic.ini upgrade head`

#### **Start Local Development**
→ `docker-compose -f infrastructure/docker/docker-compose.yml up`

#### **Deploy to Production**
→ See `/docs/deployment/RAILWAY_QUICK_START.md`

#### **Understand Architecture**
→ Start with `/docs/architecture/OVERVIEW.md`

#### **Onboard New Developers**
→ `/docs/onboarding/GETTING_STARTED.md`

#### **Find Feature Implementation**
→ `/docs/features/` - all feature guides in one place

#### **Troubleshoot Issues**
→ `/docs/guides/TROUBLESHOOTING.md`

---

## 📏 Directory Purpose Legend

| Symbol | Type | Purpose |
|--------|------|---------|
| 🐍 | Backend | FastAPI Python application |
| ⚛️ | Frontend | Next.js React application |
| 📊 | Dataset | Data & evaluation resources |
| 📖 | Docs | Documentation hub |
| 🏗️ | Infrastructure | Deployment & orchestration |
| 🔧 | Scripts | Automation utilities |
| 📦 | Archive | Historical records |
| 🔐 | Config | Configuration files |

---

## 🔍 Key Changes from Previous Structure

### What Moved

| Old Location | New Location | Reason |
|-------------|--------------|--------|
| `/alembic/` | `/backend/database/migrations/` | Migrations belong with backend |
| `/alembic.ini` | `/backend/database/migrations/alembic.ini` | Config with migrations |
| `/pytest.ini` (root) | **Removed** (use domain-specific configs) | Avoid duplication |
| `/docker-compose.yml` | `/infrastructure/docker/docker-compose.yml` | Centralize infra |
| `/railway.toml` | `/infrastructure/railway/railway.toml` | Centralize infra |
| `/implementation-guides/` | `/docs/features/` | Consolidate documentation |
| `/scripts/seed_database.py` | `/backend/scripts/` | Backend-specific script |

### What Stayed

- `/backend/` - Backend application (internal reorganization only)
- `/frontend/` - Frontend application (no changes)
- `/dataset/` - Dataset evaluation (no changes)
- `/docs/` - Documentation (internal reorganization)
- `/.github/workflows/` - CI/CD pipelines (updated paths only)
- Root config files - `.gitignore`, `LICENSE`, `README.md`, etc.

---

## 📦 Package Structure Patterns

### Backend Python Package
```
app/
├── __init__.py           # Package initialization
├── main.py               # Application entry point
├── config.py             # Configuration management
├── {domain}/             # Domain-specific modules
│   ├── __init__.py
│   └── *.py
```

### Frontend TypeScript Package
```
src/
├── app/                  # Next.js App Router
│   ├── layout.tsx        # Root layout
│   ├── page.tsx          # Pages
│   └── {feature}/        # Feature-based routing
└── lib/                  # Shared utilities
```

### Documentation Structure
```
docs/{category}/
├── README.md             # Category index
└── *.md                  # Category documents
```

---

## 🛠️ Development Workflows

### Backend Development
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows
pip install -r requirements.txt
pytest
uvicorn app.main:app --reload
```

### Frontend Development
```bash
cd frontend
npm install
npm run dev
```

### Full Stack Development
```bash
docker-compose -f infrastructure/docker/docker-compose.yml up
```

### Database Migrations
```bash
cd backend

# Create migration
alembic -c database/migrations/alembic.ini revision --autogenerate -m "description"

# Apply migrations
alembic -c database/migrations/alembic.ini upgrade head

# Rollback
alembic -c database/migrations/alembic.ini downgrade -1
```

---

## 📝 Notes

- **Alembic:** Always run from `/backend` directory using `-c database/migrations/alembic.ini`
- **Docker Compose:** Always use `-f infrastructure/docker/docker-compose.yml`
- **Pytest:** Each domain (backend, dataset) has its own `pytest.ini`
- **Environment Variables:** Use `.env.example` as template, create local `.env`

---

**Version:** 2.0  
**Last Updated:** November 10, 2025  
**See Also:** [REPOSITORY_RESTRUCTURING_PLAN.md](REPOSITORY_RESTRUCTURING_PLAN.md)
