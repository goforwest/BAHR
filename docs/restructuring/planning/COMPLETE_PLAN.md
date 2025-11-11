# 🏗️ BAHR Repository Restructuring Plan

**Project:** BAHR - Arabic Poetry Analysis Platform  
**Date:** November 10, 2025  
**Status:** Design Phase - Ready for Review & Implementation  
**Author:** Senior Software Architect

---

## 📋 Executive Summary

This document provides a comprehensive, step-by-step plan to restructure the BAHR repository for improved organization, maintainability, and scalability. The restructuring addresses:

1. **Root directory clutter** - Multiple config files, migrations, and testing tools scattered at root level
2. **Documentation synchronization** - Ensuring all docs reflect the new structure
3. **Functional integrity** - Guaranteeing all systems work post-migration
4. **External dependencies** - Identifying required updates in CI/CD, deployment, and external systems

---

## 🔍 Part 1: Current State Audit

### Root-Level Files Inventory

#### **Backend-Related (Misplaced)**
```
alembic/                    → Database migrations (should be in backend/)
alembic.ini                 → Alembic config (should be in backend/)
pytest.ini                  → Root pytest config (conflicts with backend/pytest.ini)
migration.sql               → Legacy migration script (should be archived or removed)
```

#### **Infrastructure & Deployment**
```
docker-compose.yml          → Multi-service orchestration (stays at root)
railway.toml                → Railway deployment config (stays at root)
.env                        → Environment variables (stays at root, gitignored)
.env.example                → Environment template (stays at root)
.python-version             → Python version specification (stays at root)
```

#### **Project Management**
```
README.md                   → Main project readme (stays at root)
CONTRIBUTING.md             → Contribution guidelines (stays at root)
LICENSE                     → License file (stays at root)
.gitignore                  → Git ignore rules (stays at root)
```

#### **Development Environment**
```
.venv/                      → Virtual environment (gitignored, stays at root)
venv/                       → Duplicate venv (should be removed)
.pytest_cache/              → Pytest cache (gitignored)
.coverage                   → Coverage data (gitignored)
dummy.db                    → Test database (should be removed/gitignored)
```

### Categorization Analysis

| Category | Current Location | Issues | Proposed Action |
|----------|-----------------|--------|-----------------|
| **Backend Migrations** | `alembic/`, `alembic.ini` | At root, should be with backend code | Move to `backend/database/migrations/` |
| **Test Configs** | `pytest.ini` (root), `backend/pytest.ini` | Duplicate configs cause confusion | Consolidate in `backend/` |
| **Documentation** | `docs/`, `implementation-guides/` | Two separate doc locations | Merge into unified `docs/` |
| **Scripts** | `scripts/` | Mixed backend/dataset scripts | Separate by domain |
| **Archive** | `archive/` | Historical docs mixed with active | Keep but reorganize |
| **Dataset** | `dataset/` | Proper domain separation | Keep structure, add docs |

---

## 🎯 Part 2: Proposed Repository Structure

### Complete New Layout

```
BAHR/
├── .github/
│   └── workflows/                    # CI/CD pipelines
│       ├── backend.yml
│       ├── frontend.yml
│       ├── deploy.yml
│       └── test-golden-set.yml
│
├── backend/                          # Backend application
│   ├── app/                          # Main application code
│   │   ├── __init__.py
│   │   ├── main.py                   # FastAPI entry point
│   │   ├── config.py                 # Configuration management
│   │   ├── exceptions.py             # Custom exceptions
│   │   ├── response_envelope.py      # Response formatting
│   │   │
│   │   ├── api/                      # API layer
│   │   │   └── v1/
│   │   │       ├── router.py
│   │   │       └── endpoints/
│   │   │           ├── analyze.py
│   │   │           ├── auth.py
│   │   │           └── health.py
│   │   │
│   │   ├── core/                     # Business logic
│   │   │   ├── bahr_detector.py      # Meter detection
│   │   │   ├── normalization.py      # Text normalization
│   │   │   ├── phonetics.py          # Phonetic processing
│   │   │   └── taqti3.py             # Syllable segmentation
│   │   │
│   │   ├── database/                 # Database layer (NEW)
│   │   │   ├── __init__.py
│   │   │   ├── session.py            # DB session management
│   │   │   ├── redis.py              # Redis connection
│   │   │   │
│   │   │   └── migrations/           # ← MOVED FROM ROOT
│   │   │       ├── alembic.ini       # ← FROM ROOT
│   │   │       ├── env.py
│   │   │       ├── script.py.mako
│   │   │       └── versions/
│   │   │           └── *.py
│   │   │
│   │   ├── models/                   # SQLAlchemy models
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── bahr.py
│   │   │   └── user.py
│   │   │
│   │   ├── schemas/                  # Pydantic schemas
│   │   │   ├── analyze.py
│   │   │   ├── auth.py
│   │   │   └── bahr.py
│   │   │
│   │   ├── middleware/               # Request middleware
│   │   │   ├── response_envelope.py
│   │   │   └── util_request_id.py
│   │   │
│   │   ├── metrics/                  # Observability
│   │   │   └── analysis_metrics.py
│   │   │
│   │   ├── nlp/                      # NLP utilities
│   │   │   └── normalizer.py
│   │   │
│   │   └── prosody/                  # Prosody engine
│   │       ├── engine.py
│   │       └── segmenter.py
│   │
│   ├── tests/                        # Backend tests
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── api/
│   │   │   └── v1/
│   │   │       └── test_analyze.py
│   │   ├── core/
│   │   │   ├── test_bahr_detector.py
│   │   │   ├── test_normalization.py
│   │   │   └── test_taqti3.py
│   │   └── unit/
│   │       ├── test_engine.py
│   │       ├── test_normalizer.py
│   │       └── test_segmenter.py
│   │
│   ├── scripts/                      # Backend-specific scripts
│   │   ├── seed_bahrs.py
│   │   └── seed_database.py          # ← FROM ROOT /scripts
│   │
│   ├── requirements/                 # Python dependencies
│   │   ├── base.txt
│   │   ├── development.txt
│   │   └── production.txt
│   │
│   ├── .dockerignore
│   ├── .env.example
│   ├── Dockerfile.dev
│   ├── Dockerfile.railway
│   ├── Procfile
│   ├── pytest.ini                    # Backend test config
│   ├── pyproject.toml                # Python project metadata (NEW)
│   ├── railway.json
│   ├── nixpacks.toml
│   ├── runtime.txt
│   ├── requirements.txt              # Main requirements
│   └── README.md                     # Backend-specific readme
│
├── frontend/                         # Frontend application
│   ├── src/
│   │   ├── app/                      # Next.js App Router
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx
│   │   │   └── analyze/
│   │   │       └── page.tsx
│   │   │
│   │   └── lib/                      # Utilities
│   │       ├── api.ts
│   │       └── utils.ts
│   │
│   ├── components/                   # React components
│   │   └── ui/
│   │
│   ├── public/                       # Static assets
│   │   └── fonts/
│   │
│   ├── .env.local.example
│   ├── components.json
│   ├── eslint.config.mjs
│   ├── next-env.d.ts
│   ├── next.config.ts
│   ├── nixpacks.toml
│   ├── package.json
│   ├── postcss.config.mjs
│   ├── railway.json
│   ├── tsconfig.json
│   ├── README.md                     # Frontend-specific readme
│   └── README_AR.md                  # Arabic readme
│
├── dataset/                          # Dataset & evaluation
│   ├── evaluation/
│   │   ├── golden_set.json
│   │   ├── schema.json
│   │   └── README.md
│   │
│   ├── scripts/                      # Dataset processing scripts
│   │   └── (processing tools)
│   │
│   ├── tests/                        # Dataset tests
│   │   ├── test_golden_set_loader.py
│   │   └── test_schema_validation.py
│   │
│   ├── analyze_golden_set.py
│   ├── pytest.ini                    # Dataset-specific test config
│   └── README.md
│
├── docs/                             # Unified documentation
│   ├── README.md                     # Documentation index
│   ├── QUICK_REFERENCE.md            # Fast navigation guide
│   │
│   ├── architecture/                 # Architecture documentation (NEW)
│   │   ├── OVERVIEW.md               # System architecture
│   │   ├── DECISIONS.md              # ADRs
│   │   ├── COMPONENT_DIAGRAMS.md     # Visual diagrams
│   │   └── DATA_FLOW.md              # Data flow documentation
│   │
│   ├── features/                     # Feature implementation guides (NEW)
│   │   │                             # ← MOVED FROM /implementation-guides
│   │   ├── analysis-api.md
│   │   ├── arabic-text-normalization.md
│   │   ├── authentication-jwt.md
│   │   ├── caching-redis.md
│   │   ├── database-orm.md
│   │   ├── dataset-management.md
│   │   ├── deployment-cicd.md
│   │   ├── error-handling.md
│   │   ├── frontend-nextjs.md
│   │   ├── meter-detection.md
│   │   ├── monitoring-observability.md
│   │   ├── rate-limiting.md
│   │   ├── response-envelope.md
│   │   ├── syllable-segmentation.md
│   │   └── README.md
│   │
│   ├── technical/                    # Technical specifications
│   │   ├── ARCHITECTURE_OVERVIEW.md  # Consolidated architecture
│   │   ├── BACKEND_API.md            # API documentation
│   │   ├── DATABASE_SCHEMA.md        # Database design
│   │   ├── FRONTEND_GUIDE.md         # Frontend architecture
│   │   ├── PROSODY_ENGINE.md         # Prosody algorithm
│   │   ├── SECURITY.md               # Security guidelines
│   │   ├── PERFORMANCE_TARGETS.md    # Performance metrics
│   │   └── METRICS_REFERENCE.md      # Observability metrics
│   │
│   ├── deployment/                   # Deployment guides
│   │   ├── RAILWAY_QUICK_START.md
│   │   ├── RAILWAY_DOCKER_GUIDE.md
│   │   └── ENVIRONMENT_SETUP.md
│   │
│   ├── devops/                       # DevOps documentation
│   │   ├── CI_CD_COMPLETE_GUIDE.md
│   │   ├── DOCKER_SETUP.md
│   │   └── MONITORING_SETUP.md
│   │
│   ├── guides/                       # How-to guides
│   │   ├── ANALYZE_ENDPOINT_QUICKSTART.md
│   │   ├── TESTING_GUIDE.md
│   │   └── TROUBLESHOOTING.md
│   │
│   ├── onboarding/                   # New developer guides
│   │   ├── GETTING_STARTED.md
│   │   └── DEVELOPMENT_SETUP.md
│   │
│   ├── planning/                     # Project planning
│   │   ├── IMPLEMENTATION_ROADMAP.md
│   │   ├── PROJECT_TIMELINE.md
│   │   └── MILESTONES.md
│   │
│   ├── project-management/           # PM documentation
│   │   ├── PROGRESS_LOG_CURRENT.md
│   │   ├── GITHUB_ISSUES_TEMPLATE.md
│   │   └── WORKFLOW_GUIDE.md
│   │
│   ├── research/                     # Research & references
│   │   ├── ARABIC_NLP_RESEARCH.md
│   │   └── PROSODY_REFERENCES.md
│   │
│   ├── checklists/                   # Implementation checklists
│   │   ├── PRE_WEEK_1_FINAL.md
│   │   ├── WEEK_1_CRITICAL.md
│   │   └── DEPLOYMENT_CHECKLIST.md
│   │
│   ├── testing/                      # Testing documentation
│   │   ├── TESTING_STRATEGY.md
│   │   └── TEST_DATA_GUIDE.md
│   │
│   ├── vision/                       # Vision & strategy
│   │   ├── MASTER_PLAN.md
│   │   └── PRODUCT_VISION.md
│   │
│   ├── workflows/                    # Development workflows
│   │   └── DEVELOPMENT_WORKFLOW.md
│   │
│   └── templates/                    # Document templates
│       ├── ADR_TEMPLATE.md
│       └── FEATURE_TEMPLATE.md
│
├── infrastructure/                   # Infrastructure as Code (NEW)
│   ├── docker/
│   │   ├── backend/
│   │   │   ├── Dockerfile.dev        # ← MOVED FROM backend/
│   │   │   └── Dockerfile.prod       # ← MOVED FROM backend/Dockerfile.railway
│   │   │
│   │   ├── frontend/
│   │   │   └── (if needed)
│   │   │
│   │   └── docker-compose.yml        # ← MOVED FROM ROOT
│   │
│   ├── railway/
│   │   ├── railway.toml              # ← MOVED FROM ROOT
│   │   ├── backend.json              # ← MOVED FROM backend/railway.json
│   │   └── frontend.json             # ← MOVED FROM frontend/railway.json
│   │
│   └── nginx/
│       └── (if needed for reverse proxy)
│
├── scripts/                          # Repository-wide scripts
│   ├── setup/
│   │   ├── verify_setup.sh           # ← FROM ROOT
│   │   └── setup-branch-protection.sh
│   │
│   ├── health/
│   │   ├── health_check.sh
│   │   └── verify_deployment.sh
│   │
│   ├── testing/
│   │   ├── test-ci-local.sh
│   │   ├── test_analyze_endpoint.sh
│   │   ├── test_redis_caching.py     # ← MOVED if backend-agnostic
│   │   └── verify_redis_caching.sh
│   │
│   ├── deployment/
│   │   └── (deployment automation)
│   │
│   ├── fix-workflow-dispatch.sh
│   └── README.md
│
├── archive/                          # Historical documentation
│   ├── blockers/
│   ├── checklists/
│   ├── dataset/
│   ├── deployment/
│   ├── implementation/
│   ├── integration/
│   ├── milestones/
│   ├── plans/
│   ├── progress/
│   ├── reviews/
│   └── README.md
│
├── .gitignore
├── .python-version
├── .env.example                      # Root env template
├── CONTRIBUTING.md
├── LICENSE
├── README.md                         # Main project readme
├── REPOSITORY_STRUCTURE.md           # This document (NEW)
└── CHANGELOG.md                      # Migration changelog (NEW)
```

---

## 📦 Part 3: File Migration Mapping

### Priority 1: Critical Backend Restructuring

| Source | Destination | Justification |
|--------|-------------|---------------|
| `/alembic/` | `/backend/database/migrations/` | Database migrations belong with backend code; improves cohesion |
| `/alembic.ini` | `/backend/database/migrations/alembic.ini` | Config should be with migrations; reduces root clutter |
| `/pytest.ini` (root) | **REMOVE** (keep `backend/pytest.ini` and `dataset/pytest.ini`) | Two pytest.ini files exist; backend & dataset have domain-specific configs |
| `/migration.sql` | **ARCHIVE or REMOVE** | Legacy migration; replaced by Alembic |

### Priority 2: Infrastructure Consolidation

| Source | Destination | Justification |
|--------|-------------|---------------|
| `/docker-compose.yml` | `/infrastructure/docker/docker-compose.yml` | Centralize all infra config; cleaner separation |
| `/railway.toml` | `/infrastructure/railway/railway.toml` | Group deployment configs by platform |
| `/backend/Dockerfile.dev` | `/infrastructure/docker/backend/Dockerfile.dev` | Separate infra from app code |
| `/backend/Dockerfile.railway` | `/infrastructure/docker/backend/Dockerfile.prod` | Rename for clarity; separate from app code |
| `/backend/railway.json` | `/infrastructure/railway/backend.json` | Consolidate Railway configs |
| `/frontend/railway.json` | `/infrastructure/railway/frontend.json` | Consolidate Railway configs |

### Priority 3: Documentation Consolidation

| Source | Destination | Justification |
|--------|-------------|---------------|
| `/implementation-guides/*.md` | `/docs/features/*.md` | Consolidate feature docs; single source of truth |
| `/docs/technical/ARCHITECTURE_OVERVIEW.md` | `/docs/architecture/OVERVIEW.md` | Better categorization; dedicated architecture folder |
| `/docs/ARCHITECTURE_DECISIONS.md` | `/docs/architecture/DECISIONS.md` | Co-locate with architecture docs |

### Priority 4: Scripts Organization

| Source | Destination | Justification |
|--------|-------------|---------------|
| `/scripts/seed_database.py` | `/backend/scripts/seed_database.py` | Backend-specific script |
| `/scripts/test_redis_caching.py` | `/scripts/testing/test_redis_caching.py` OR `/backend/scripts/` | Decide based on scope (testing vs backend-specific) |
| Other scripts in `/scripts/` | Categorize into `/scripts/{setup,health,testing,deployment}/` | Logical grouping by function |

### Priority 5: Cleanup & Optimization

| Item | Action | Justification |
|------|--------|---------------|
| `/venv/` | **DELETE** | Duplicate of `.venv/`; both gitignored |
| `/dummy.db` | **DELETE** | Test artifact; should be in `.gitignore` |
| `/.coverage` | Already gitignored | Keep in `.gitignore` |
| `/.pytest_cache/` | Already gitignored | Keep in `.gitignore` |

---

## 🔧 Part 4: Code & Configuration Changes Required

### 4.1 Alembic Migration Path Updates

**File:** `/backend/database/migrations/alembic.ini`

```ini
[alembic]
# OLD:
# script_location = %(here)s/alembic

# NEW:
script_location = %(here)s
```

**File:** `/backend/database/migrations/env.py`

```python
# UPDATE import paths - no longer need complex sys.path manipulation
# NEW simplified version:

from pathlib import Path
import sys

# Add backend root to path
backend_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(backend_root))

from app.models import Base
```

**Run migration commands from:**
```bash
# OLD:
cd /path/to/BAHR
alembic upgrade head

# NEW:
cd /path/to/BAHR/backend
alembic -c database/migrations/alembic.ini upgrade head
```

### 4.2 Backend Test Configuration

**File:** `/backend/pytest.ini`

Update `testpaths` if test structure changes:

```ini
[pytest]
testpaths = tests

# Coverage source paths remain:
[coverage:run]
source = app
omit = 
    */tests/*
    */database/migrations/*  # ← UPDATED PATH
```

### 4.3 Docker & Docker Compose Updates

**File:** `/infrastructure/docker/docker-compose.yml`

```yaml
# Update volume and build context paths:

services:
  backend:
    build:
      context: ../../backend  # ← UPDATED (was ./backend)
      dockerfile: ../../infrastructure/docker/backend/Dockerfile.dev  # ← NEW PATH
    volumes:
      - ../../backend:/app  # ← UPDATED

  # ... similar updates for frontend if needed
```

**File:** `/infrastructure/docker/backend/Dockerfile.prod`

```dockerfile
# No internal path changes needed - all relative to backend/
# But CI/CD must reference new location
```

### 4.4 Railway Deployment Configs

**File:** `/infrastructure/railway/railway.toml`

```toml
# Ensure build paths reference correct directories

[build]
builder = "nixpacks"
buildCommand = "pip install -r backend/requirements.txt"  # ← IF root-relative

[deploy]
startCommand = "cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT"
```

**OR** use separate Railway services with local paths in respective configs.

### 4.5 Import Path Updates (Minimal Impact)

**Analysis:** Most Python imports use relative `from app.*` - these remain unchanged.

**Exceptions to verify:**
- `/backend/tests/test_envelope.py` - uses `from backend.app.main import app` (should change to `from app.main import app`)
- Any scripts in `/backend/scripts/` - ensure they can import `app.*` correctly

### 4.6 CI/CD Workflow Updates

**File:** `/.github/workflows/backend.yml`

```yaml
# Update paths:

on:
  push:
    paths:
      - 'backend/**'
      - '.github/workflows/backend.yml'
      # REMOVE: - 'pytest.ini'  (now in backend/)
      # ADD:
      - 'infrastructure/docker/backend/**'
      - 'infrastructure/railway/backend.json'
```

```yaml
steps:
  - name: Run tests
    working-directory: ./backend
    run: |
      pytest  # Uses backend/pytest.ini automatically
```

**File:** `/.github/workflows/deploy.yml`

```yaml
# Update Docker build commands if using docker-compose:

- name: Build images
  run: |
    docker-compose -f infrastructure/docker/docker-compose.yml build
```

**File:** `/.github/workflows/test-golden-set.yml`

```yaml
# Update dataset test paths (minimal changes):

- name: Run tests
  run: |
    pytest dataset/tests/ -c dataset/pytest.ini
```

---

## 📚 Part 5: Documentation Synchronization

### 5.1 Documentation Files Requiring Updates

| Document | Required Updates | Priority |
|----------|------------------|----------|
| `/README.md` | Update "Project Structure" section with new layout | **HIGH** |
| `/docs/README.md` | Update navigation links to reflect new paths | **HIGH** |
| `/docs/QUICK_REFERENCE.md` | Update all file path references | **HIGH** |
| `/docs/onboarding/GETTING_STARTED.md` | Update setup commands (alembic, docker-compose paths) | **HIGH** |
| `/docs/devops/CI_CD_COMPLETE_GUIDE.md` | Update workflow file references | **MEDIUM** |
| `/docs/deployment/RAILWAY_QUICK_START.md` | Update Railway config paths | **MEDIUM** |
| `/docs/deployment/RAILWAY_DOCKER_GUIDE.md` | Update Dockerfile references | **MEDIUM** |
| `/docs/technical/BACKEND_API.md` | Update code structure references | **LOW** |
| `/backend/README.md` | Create new backend-specific readme | **HIGH** |
| `/frontend/README.md` | Already exists, verify accuracy | **LOW** |

### 5.2 New Documentation to Create

| New Document | Purpose | Location |
|--------------|---------|----------|
| `REPOSITORY_STRUCTURE.md` | Visual tree + navigation guide for entire repo | `/` (root) |
| `MIGRATION_GUIDE.md` | How to adapt to new structure (for contributors) | `/docs/` |
| `backend/README.md` | Backend architecture, setup, and development guide | `/backend/` |
| `infrastructure/README.md` | Infrastructure setup and deployment guide | `/infrastructure/` |
| `scripts/README.md` | Script inventory and usage guide | `/scripts/` |
| `docs/architecture/README.md` | Architecture documentation index | `/docs/architecture/` |
| `docs/features/README.md` | Feature implementation index | `/docs/features/` |

### 5.3 Documentation Consolidation Plan

**Merge duplicates:**

1. **Implementation Guides → Features Documentation**
   - Move all `/implementation-guides/*.md` → `/docs/features/`
   - Update internal cross-references
   - Update `docs/QUICK_REFERENCE.md` links

2. **Architecture Documents**
   - Move `/docs/ARCHITECTURE_DECISIONS.md` → `/docs/architecture/DECISIONS.md`
   - Restructure `/docs/technical/ARCHITECTURE_OVERVIEW.md` → `/docs/architecture/OVERVIEW.md`
   - Create `/docs/architecture/README.md` as index

3. **Archive Cleanup**
   - Verify all `/archive/*` documents are historical
   - Add `/archive/README.md` explaining archive purpose
   - Consider moving truly obsolete docs to a separate branch

### 5.4 Automated Documentation Checks

**Add to CI/CD:**

```yaml
# .github/workflows/docs-validation.yml (NEW)

name: Documentation Validation

on:
  pull_request:
    paths:
      - 'docs/**'
      - '**.md'

jobs:
  validate-links:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Check Markdown links
        uses: gaurav-nelson/github-action-markdown-link-check@v1
        with:
          config-file: '.github/markdown-link-check-config.json'
```

---

## 🧪 Part 6: Validation & Testing Checklist

### 6.1 Pre-Migration Validation

- [ ] **Backup repository** - Create full backup before any changes
- [ ] **Document current state** - Take inventory of all running services
- [ ] **Tag current version** - Create git tag: `pre-restructure-backup`
- [ ] **Export environment configs** - Backup all `.env` files
- [ ] **Review open PRs** - Note any in-progress work that might conflict

### 6.2 Migration Execution Checklist

#### Phase 1: Backend Restructuring
- [ ] Create `/backend/database/` directory structure
- [ ] Move `alembic/` → `/backend/database/migrations/`
- [ ] Move `alembic.ini` → `/backend/database/migrations/alembic.ini`
- [ ] Update `alembic.ini` script_location path
- [ ] Update `/backend/database/migrations/env.py` import paths
- [ ] Delete root `/pytest.ini` (keep backend & dataset versions)
- [ ] Update backend test imports (remove `backend.app.*` → `app.*`)
- [ ] Run backend tests: `cd backend && pytest`
- [ ] Run Alembic migrations: `cd backend && alembic -c database/migrations/alembic.ini upgrade head`
- [ ] Verify database schema is correct

#### Phase 2: Infrastructure Consolidation
- [ ] Create `/infrastructure/` directory structure
- [ ] Move `docker-compose.yml` → `/infrastructure/docker/`
- [ ] Create `/infrastructure/docker/backend/` directory
- [ ] Move `backend/Dockerfile.dev` → `/infrastructure/docker/backend/`
- [ ] Move `backend/Dockerfile.railway` → `/infrastructure/docker/backend/Dockerfile.prod`
- [ ] Update `docker-compose.yml` paths (context, volumes, Dockerfiles)
- [ ] Create `/infrastructure/railway/` directory
- [ ] Move `railway.toml` → `/infrastructure/railway/`
- [ ] Move `backend/railway.json` → `/infrastructure/railway/backend.json`
- [ ] Move `frontend/railway.json` → `/infrastructure/railway/frontend.json`
- [ ] Test Docker builds: `docker-compose -f infrastructure/docker/docker-compose.yml build`
- [ ] Test Docker services: `docker-compose -f infrastructure/docker/docker-compose.yml up`

#### Phase 3: Documentation Consolidation
- [ ] Create `/docs/architecture/` directory
- [ ] Create `/docs/features/` directory
- [ ] Move `implementation-guides/*.md` → `/docs/features/`
- [ ] Move `/docs/ARCHITECTURE_DECISIONS.md` → `/docs/architecture/DECISIONS.md`
- [ ] Reorganize technical docs into `/docs/architecture/`
- [ ] Create new `README.md` files for each major docs folder
- [ ] Update all internal documentation links
- [ ] Update `/docs/QUICK_REFERENCE.md` paths

#### Phase 4: Scripts Organization
- [ ] Create `/scripts/{setup,health,testing,deployment}/` directories
- [ ] Move backend-specific scripts → `/backend/scripts/`
- [ ] Categorize root scripts into appropriate subdirectories
- [ ] Update script documentation
- [ ] Test critical scripts still work

#### Phase 5: Cleanup
- [ ] Delete `/venv/` directory
- [ ] Delete `/dummy.db`
- [ ] Delete `/migration.sql` (or archive)
- [ ] Update `.gitignore` if needed
- [ ] Remove any other identified obsolete files

### 6.3 Post-Migration Validation

#### Functional Testing
- [ ] **Backend API Tests**
  ```bash
  cd backend
  pytest -v
  pytest --cov=app tests/
  ```

- [ ] **Database Migrations**
  ```bash
  cd backend
  alembic -c database/migrations/alembic.ini current
  alembic -c database/migrations/alembic.ini upgrade head
  alembic -c database/migrations/alembic.ini downgrade -1
  alembic -c database/migrations/alembic.ini upgrade head
  ```

- [ ] **Frontend Build**
  ```bash
  cd frontend
  npm install
  npm run build
  npm run dev
  ```

- [ ] **Dataset Tests**
  ```bash
  pytest dataset/tests/ -v
  ```

- [ ] **Docker Compose**
  ```bash
  docker-compose -f infrastructure/docker/docker-compose.yml up -d
  docker-compose -f infrastructure/docker/docker-compose.yml ps
  docker-compose -f infrastructure/docker/docker-compose.yml logs backend
  curl http://localhost:8000/health
  docker-compose -f infrastructure/docker/docker-compose.yml down
  ```

#### CI/CD Validation
- [ ] Push changes to test branch
- [ ] Verify `.github/workflows/backend.yml` runs successfully
- [ ] Verify `.github/workflows/frontend.yml` runs successfully
- [ ] Verify `.github/workflows/test-golden-set.yml` runs successfully
- [ ] Verify `.github/workflows/deploy.yml` references correct paths
- [ ] Check all GitHub Actions pass

#### Documentation Validation
- [ ] All internal links resolve correctly
- [ ] Code examples reference correct paths
- [ ] Setup instructions work for new developers
- [ ] Navigation index is accurate
- [ ] Run markdown link checker

#### Integration Testing
- [ ] Start full stack locally: `docker-compose -f infrastructure/docker/docker-compose.yml up`
- [ ] Test API endpoint: `curl http://localhost:8000/api/v1/health`
- [ ] Test frontend: http://localhost:3000
- [ ] Test end-to-end analysis flow
- [ ] Verify Redis caching works
- [ ] Verify PostgreSQL connections work
- [ ] Check logs for errors

---

## ⚠️ Part 7: External Dependencies & Required Updates

### 7.1 Railway Deployment

**Impact:** HIGH  
**Files to Update Externally:**

1. **Railway Service Configuration** (in Railway Dashboard)
   - **Backend Service:**
     - Update "Root Directory" → `/backend` (if not already set)
     - Update "Build Command" → reference correct paths
     - Update "Start Command" → `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
     - Verify environment variables unchanged
   
   - **Frontend Service:**
     - Update "Root Directory" → `/frontend` (if not already set)
     - Verify build command unchanged
     - Verify start command unchanged

2. **Railway Configuration Files** (now in `/infrastructure/railway/`)
   - Update Railway project to reference:
     - `/infrastructure/railway/railway.toml` (if using monorepo config)
     - OR separate configs per service

3. **Action Required:**
   ```
   ⚠️  After migration, verify Railway deployments:
   - Check build logs for path errors
   - Verify services start successfully
   - Test deployed API endpoints
   - Monitor for 24 hours post-deployment
   ```

### 7.2 GitHub Actions Workflows

**Impact:** MEDIUM  
**Files Already in Repo:** `.github/workflows/*.yml`

**Changes Required:**

1. **`.github/workflows/backend.yml`**
   ```yaml
   # BEFORE:
   paths:
     - 'backend/**'
     - 'pytest.ini'
   
   # AFTER:
   paths:
     - 'backend/**'
     - 'infrastructure/docker/backend/**'
     - 'infrastructure/railway/backend.json'
   ```

2. **`.github/workflows/deploy.yml`**
   ```yaml
   # Add Docker build context updates if using docker-compose
   # Verify Railway deployments reference correct service configs
   ```

3. **`.github/workflows/frontend.yml`**
   ```yaml
   # Minimal changes - verify paths still correct
   ```

4. **`.github/workflows/test-golden-set.yml`**
   ```yaml
   # Update pytest command to reference dataset/pytest.ini
   ```

**Action Required:**
```
✅ These files are in the repository and will be updated during migration.
⚠️  Test all workflows on a feature branch before merging to main.
```

### 7.3 Docker Volume Mounts (Local Development)

**Impact:** MEDIUM  
**Affected Users:** Developers using Docker locally

**Old docker-compose.yml:**
```yaml
volumes:
  - ./backend:/app
  - postgres_data:/var/lib/postgresql/data
```

**New docker-compose.yml:**
```yaml
volumes:
  - ../../backend:/app  # ← Relative to infrastructure/docker/
  - postgres_data:/var/lib/postgresql/data
```

**Action Required:**
```
⚠️  Notify team:
- Update docker-compose command: 
  docker-compose -f infrastructure/docker/docker-compose.yml up
- Update local .env paths if referencing docker-compose location
- Clear old Docker volumes if needed:
  docker-compose down -v
```

### 7.4 Developer Tooling & IDE Configurations

**Impact:** LOW-MEDIUM  
**Affected Areas:**

1. **Python Import Resolution:**
   - IDEs (PyCharm, VS Code) may need to reconfigure Python interpreter paths
   - `PYTHONPATH` environment variables may need updating
   - Action: Update project `.vscode/settings.json` or equivalent

2. **Test Discovery:**
   - Test runners should automatically find `backend/pytest.ini`
   - VS Code Python extension: verify test discovery still works
   - Action: Test local dev environment after migration

3. **Linters & Formatters:**
   - Ensure `.flake8`, `.pylintrc`, `.black.toml` (if any) are in correct locations
   - Update paths in pre-commit hooks if used
   - Action: Verify code quality tools still function

### 7.5 External Documentation & Links

**Impact:** LOW  
**Affected Areas:**

1. **README.md External References:**
   - Any external sites linking to specific file paths in GitHub
   - Example: `https://github.com/goforwest/BAHR/blob/main/alembic/` → 404 after move
   - Action: Update external wikis, notion pages, or blog posts

2. **Issue Templates:**
   - GitHub issue templates may reference old paths
   - Action: Review `.github/ISSUE_TEMPLATE/` and update

3. **Pull Request Templates:**
   - PR templates may reference old structure
   - Action: Review `.github/PULL_REQUEST_TEMPLATE.md` if exists

### 7.6 Third-Party Integrations

**Impact:** LOW (currently)  
**Potential Areas:**

1. **Monitoring Services:**
   - If using external APM (DataDog, New Relic, Sentry)
   - Verify trace/log paths still make sense
   - Action: Check monitoring dashboards post-deployment

2. **Code Quality Services:**
   - CodeClimate, SonarQube configurations
   - Update exclusion/inclusion paths
   - Action: Re-run code quality scans

3. **Dependency Scanners:**
   - Dependabot, Snyk, Renovate
   - May need to update file paths for dependency tracking
   - Action: Verify automated PR creation still works

---

## 📋 Part 8: Migration Execution Plan

### 8.1 Migration Strategy

**Approach:** Incremental migration with validation gates

**Timeline:** 1-2 days for full migration

**Risk Level:** Medium (mitigated by testing & backups)

### 8.2 Step-by-Step Execution

#### Preparation (30 minutes)
1. Create git tag: `git tag -a pre-restructure-v1.0 -m "Pre-restructure backup"`
2. Create feature branch: `git checkout -b feature/repository-restructure`
3. Backup `.env` files
4. Document current running services
5. Notify team of upcoming changes

#### Phase 1: Backend Core (1-2 hours)
1. Create directory structure:
   ```bash
   mkdir -p backend/database/migrations
   ```

2. Move Alembic files:
   ```bash
   mv alembic/* backend/database/migrations/
   mv alembic.ini backend/database/migrations/
   rmdir alembic
   ```

3. Update `backend/database/migrations/alembic.ini`:
   - Change `script_location = %(here)s/alembic` → `script_location = %(here)s`

4. Update `backend/database/migrations/env.py`:
   - Simplify sys.path manipulation
   - Test imports work

5. Test migrations:
   ```bash
   cd backend
   alembic -c database/migrations/alembic.ini current
   alembic -c database/migrations/alembic.ini check
   ```

6. Run backend tests:
   ```bash
   cd backend
   pytest -v
   ```

7. **VALIDATION GATE:** All backend tests must pass before proceeding.

#### Phase 2: Infrastructure (1-2 hours)
1. Create infrastructure directories:
   ```bash
   mkdir -p infrastructure/docker/backend
   mkdir -p infrastructure/railway
   ```

2. Move Docker files:
   ```bash
   mv docker-compose.yml infrastructure/docker/
   mv backend/Dockerfile.dev infrastructure/docker/backend/
   cp backend/Dockerfile.railway infrastructure/docker/backend/Dockerfile.prod
   ```

3. Move Railway configs:
   ```bash
   mv railway.toml infrastructure/railway/
   mv backend/railway.json infrastructure/railway/backend.json
   mv frontend/railway.json infrastructure/railway/frontend.json
   ```

4. Update `infrastructure/docker/docker-compose.yml`:
   - Update all context and volume paths
   - Update Dockerfile references

5. Test Docker build:
   ```bash
   docker-compose -f infrastructure/docker/docker-compose.yml build
   docker-compose -f infrastructure/docker/docker-compose.yml up -d
   docker-compose -f infrastructure/docker/docker-compose.yml ps
   curl http://localhost:8000/health
   docker-compose -f infrastructure/docker/docker-compose.yml down
   ```

6. **VALIDATION GATE:** Docker services must start and respond correctly.

#### Phase 3: Documentation (2-3 hours)
1. Create documentation structure:
   ```bash
   mkdir -p docs/architecture
   mkdir -p docs/features
   ```

2. Move implementation guides:
   ```bash
   mv implementation-guides/* docs/features/
   rmdir implementation-guides
   ```

3. Reorganize architecture docs:
   ```bash
   mv docs/ARCHITECTURE_DECISIONS.md docs/architecture/DECISIONS.md
   # Optionally restructure ARCHITECTURE_OVERVIEW.md
   ```

4. Update all documentation:
   - Update `README.md` project structure section
   - Update `docs/QUICK_REFERENCE.md` all paths
   - Update `docs/onboarding/GETTING_STARTED.md` setup commands
   - Create new README files for major folders

5. Run link checker:
   ```bash
   # Use markdown-link-check or similar tool
   ```

6. **VALIDATION GATE:** All documentation links must resolve.

#### Phase 4: Scripts & Cleanup (30 minutes)
1. Organize scripts:
   ```bash
   mkdir -p scripts/{setup,health,testing,deployment}
   mv scripts/verify_setup.sh scripts/setup/
   mv scripts/health_check.sh scripts/health/
   # ... continue for all scripts
   ```

2. Move backend scripts:
   ```bash
   mv scripts/seed_database.py backend/scripts/
   ```

3. Cleanup:
   ```bash
   rm -rf venv/
   rm -f dummy.db
   # Archive or delete migration.sql
   ```

4. Update `.gitignore` if needed

#### Phase 5: CI/CD & Final Validation (1 hour)
1. Update workflow files:
   - Edit `.github/workflows/backend.yml`
   - Edit `.github/workflows/deploy.yml`
   - Edit `.github/workflows/test-golden-set.yml`

2. Create documentation validation workflow:
   - Add `.github/workflows/docs-validation.yml`

3. Commit all changes:
   ```bash
   git add .
   git commit -m "Restructure repository for improved organization

   - Move alembic to backend/database/migrations
   - Consolidate infrastructure configs
   - Merge implementation-guides into docs/features
   - Organize scripts by function
   - Update all documentation references
   
   BREAKING CHANGES:
   - Alembic commands now require: alembic -c database/migrations/alembic.ini
   - Docker Compose path: infrastructure/docker/docker-compose.yml
   - See MIGRATION_GUIDE.md for details"
   ```

4. Push to feature branch:
   ```bash
   git push origin feature/repository-restructure
   ```

5. **VALIDATION GATE:** All CI/CD workflows must pass on feature branch.

#### Phase 6: Deployment & Monitoring (variable)
1. Merge to main after approval
2. Monitor Railway deployments
3. Verify production services
4. Check error logs for 24 hours
5. Update external documentation

### 8.3 Rollback Plan

If issues arise:

1. **Immediate Rollback:**
   ```bash
   git checkout main
   git reset --hard pre-restructure-v1.0
   git push origin main --force-with-lease
   ```

2. **Partial Rollback:**
   - Revert specific commits
   - Fix issues incrementally

3. **Railway Rollback:**
   - Use Railway dashboard to rollback to previous deployment
   - Verify database migrations haven't broken schema

---

## 📊 Part 9: Success Metrics & Monitoring

### 9.1 Migration Success Criteria

- [ ] All backend tests pass (100% success rate)
- [ ] All frontend builds succeed
- [ ] All CI/CD pipelines pass
- [ ] Docker services start without errors
- [ ] Database migrations run correctly
- [ ] All documentation links resolve
- [ ] No 404 errors in production
- [ ] API response times unchanged (< 5% variance)
- [ ] Zero production incidents in first 48 hours

### 9.2 Post-Migration Monitoring

**Week 1:**
- Daily check of Railway deployment logs
- Monitor API error rates
- Track developer onboarding issues
- Collect team feedback on new structure

**Week 2-4:**
- Weekly review of CI/CD success rates
- Monitor documentation usage patterns
- Track time-to-setup for new developers
- Measure reduction in "where is X?" questions

### 9.3 Expected Benefits

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Root directory files | 20+ | ~10 | 50% reduction |
| Documentation locations | 2 | 1 | Consolidated |
| Time to find implementation guide | ~5 min | ~30 sec | 90% faster |
| New developer setup confusion | High | Low | Qualitative |
| CI/CD pipeline clarity | Medium | High | Qualitative |

---

## 🎯 Part 10: Justifications & Rationale

### 10.1 Why Restructure Now?

1. **Technical Debt Accumulation:** Root directory has grown cluttered with misplaced configs
2. **Developer Onboarding:** New developers struggle to understand repository organization
3. **Scalability:** Current structure doesn't scale as project grows (future microservices, dataset expansion)
4. **Best Practices Alignment:** Industry-standard project layouts improve collaboration and tool support
5. **Documentation Drift:** Multiple doc locations have diverged; consolidation is critical

### 10.2 Design Principles Applied

1. **Domain-Driven Structure:** Code organized by domain (backend, frontend, dataset, infrastructure)
2. **Separation of Concerns:** Infrastructure separate from application code
3. **Single Source of Truth:** One location for each type of documentation
4. **Discoverability:** Intuitive folder names and clear README files
5. **Tool Convention Over Configuration:** Follow pytest, Alembic, Docker conventions

### 10.3 Alternative Approaches Considered

| Approach | Pros | Cons | Decision |
|----------|------|------|----------|
| **Monorepo with workspaces** | Better tooling support (Nx, Turborepo) | Overkill for current size; complex migration | Rejected |
| **Keep current structure** | No migration risk | Continues to accumulate debt | Rejected |
| **Gradual migration** | Lower risk per change | Dragged out process; confusion | Rejected |
| **Full restructure (chosen)** | Clean slate; clear benefits | Higher upfront cost; coordination needed | **Accepted** |

### 10.4 Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Breaking production deployment | Medium | High | Test on staging; feature branch; rollback plan |
| Developer confusion | High | Medium | Clear communication; migration guide; pair programming |
| Documentation out of sync | Medium | Medium | Automated link checking; comprehensive update checklist |
| Lost git history | Low | Low | Files moved with `git mv` to preserve history |
| External integrations break | Low | Medium | Identify all integrations beforehand; monitor post-deploy |

---

## 📖 Part 11: Communication & Documentation Plan

### 11.1 Team Communication

**Before Migration:**
- [ ] Present this plan to team for review and feedback
- [ ] Schedule migration window (low-traffic period)
- [ ] Create Slack/Discord announcement
- [ ] Document current state for reference

**During Migration:**
- [ ] Post updates at each phase completion
- [ ] Be available for questions/issues
- [ ] Monitor CI/CD pipelines in real-time

**After Migration:**
- [ ] Announce completion with summary
- [ ] Share `MIGRATION_GUIDE.md` for adaptation
- [ ] Conduct retrospective (what went well/what didn't)
- [ ] Update onboarding docs

### 11.2 Documentation Deliverables

1. **This Document:** `REPOSITORY_RESTRUCTURING_PLAN.md`
2. **Migration Guide:** `docs/MIGRATION_GUIDE.md` - How to adapt workflows
3. **Repository Structure:** `REPOSITORY_STRUCTURE.md` - Visual tree reference
4. **Changelog:** `CHANGELOG.md` - Record of structural changes
5. **Updated README:** Main `README.md` with new structure section

---

## ✅ Part 12: Final Checklist

### Pre-Migration
- [ ] Review and approve this plan
- [ ] Create backup tag: `pre-restructure-v1.0`
- [ ] Create feature branch: `feature/repository-restructure`
- [ ] Notify team of migration schedule
- [ ] Backup all `.env` files
- [ ] Document current running services
- [ ] Prepare rollback procedure

### Migration Execution
- [ ] Execute Phase 1: Backend Core
- [ ] Execute Phase 2: Infrastructure
- [ ] Execute Phase 3: Documentation
- [ ] Execute Phase 4: Scripts & Cleanup
- [ ] Execute Phase 5: CI/CD Updates
- [ ] Execute Phase 6: Deployment

### Post-Migration
- [ ] Run full test suite
- [ ] Verify all CI/CD pipelines
- [ ] Test Docker Compose locally
- [ ] Deploy to staging/production
- [ ] Monitor for 24-48 hours
- [ ] Update external documentation
- [ ] Notify team of completion
- [ ] Conduct retrospective

### Documentation
- [ ] Update `README.md`
- [ ] Update `docs/QUICK_REFERENCE.md`
- [ ] Update `docs/onboarding/GETTING_STARTED.md`
- [ ] Create `MIGRATION_GUIDE.md`
- [ ] Create `REPOSITORY_STRUCTURE.md`
- [ ] Update `CHANGELOG.md`
- [ ] Run link checker on all docs

---

## 📞 Support & Questions

**For questions or issues during migration:**
- Open GitHub issue with label: `migration-support`
- Contact: [Your contact method]
- Reference this document: `REPOSITORY_RESTRUCTURING_PLAN.md`

---

## 📚 References

- [Structuring Python Projects](https://docs.python-guide.org/writing/structure/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/en/latest/)
- [Docker Compose Best Practices](https://docs.docker.com/compose/production/)
- [Railway Deployment Guide](https://docs.railway.app/)
- [Conventional Commits](https://www.conventionalcommits.org/)

---

**Document Version:** 1.0  
**Last Updated:** November 10, 2025  
**Next Review:** Post-migration retrospective
