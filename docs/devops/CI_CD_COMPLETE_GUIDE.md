# CI/CD Complete Guide
## BAHR Platform - Continuous Integration & Deployment

**Category:** DevOps  
**Status:** ✅ Complete  
**Version:** 2.1  
**Last Updated:** 2025-11-10  
**Audience:** DevOps Engineers, Developers  
**Purpose:** Comprehensive CI/CD setup and deployment guide  
**Consolidates:** CI_CD_GUIDE.md + CI_CD_ARCHITECTURE.md + CI_CD_QUICKREF.md  
**Related Docs:** [Railway Deployment](../deployment/RAILWAY_COMPLETE_GUIDE.md), [Architecture](../technical/ARCHITECTURE_OVERVIEW.md)

---

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Workflows](#workflows)
4. [Quick Reference](#quick-reference)
5. [Railway Configuration](#railway-configuration)
6. [Development Workflow](#development-workflow)
7. [Troubleshooting](#troubleshooting)
8. [Monitoring](#monitoring)

---

<a name="overview"></a>
## 1. Overview

BAHR uses **GitHub Actions** for Continuous Integration and Continuous Deployment (CI/CD), with automatic deployments to **Railway** on successful builds.

### Key Features
- ✅ Automated testing on every push and PR
- ✅ Multi-version testing (Python 3.11/3.12, Node 20.x/22.x)
- ✅ Code quality gates (linting, formatting, type-checking)
- ✅ Automatic deployment to Railway on main branch
- ✅ Dependency caching for faster builds (5-10x speedup)
- ✅ Coverage reporting to Codecov

### Pipeline Flow
```
Developer Push → GitHub Actions CI → Quality Gates → Deploy to Railway → Production
```

---

<a name="architecture"></a>
## 2. Architecture

### 2.1 High-Level Architecture Diagram

```mermaid
graph TB
    subgraph "Development"
        A[Developer] -->|git push| B[GitHub Repository]
        A -->|Create PR| B
    end

    subgraph "GitHub Actions - Backend CI"
        B -->|backend/** changes| C[Backend Workflow]
        C --> D[Setup Python 3.11/3.12]
        D --> E[Install Dependencies]
        E --> F[Flake8 Lint]
        F --> G[Black Format Check]
        G --> H[isort Import Check]
        H --> I[mypy Type Check]
        I --> J[pytest + Coverage]
        J --> K[Upload to Codecov]
    end

    subgraph "GitHub Actions - Frontend CI"
        B -->|frontend/** changes| L[Frontend Workflow]
        L --> M[Setup Node 20.x/22.x]
        M --> N[Install Dependencies]
        N --> O[ESLint]
        O --> P[TypeScript Check]
        P --> Q[Prettier Check]
        Q --> R[Next.js Build]
        R --> S[Run Tests]
    end

    subgraph "GitHub Actions - Deploy"
        B -->|push to main| T[Deploy Workflow]
        T --> U{All CI Passed?}
        U -->|Yes| V[Deploy Backend]
        U -->|Yes| W[Deploy Frontend]
        U -->|No| X[❌ Block Deploy]
    end

    subgraph "Railway Platform"
        V --> Y[Backend Service]
        W --> Z[Frontend Service]
        Y --> AA[PostgreSQL]
        Y --> AB[Redis]
        Z --> AC[CDN/Edge]
    end

    subgraph "Production"
        AA --> AD[🚀 Live Backend API]
        AC --> AE[🌐 Live Frontend App]
    end

    K -.->|Coverage Report| AF[Codecov Dashboard]
    J -.->|Test Results| AG[GitHub Checks]
    S -.->|Build Status| AG

    style C fill:#e1f5e1
    style L fill:#e1f5e1
    style T fill:#fff3cd
    style AD fill:#d4edda
    style AE fill:#d4edda
    style X fill:#f8d7da
```

### 2.2 Decision Flow

```mermaid
flowchart TD
    A[Code Changed] --> B{Which Files?}
    
    B -->|backend/**| C[Run Backend CI]
    B -->|frontend/**| D[Run Frontend CI]
    B -->|Both| E[Run Both CIs]
    
    C --> F{All Checks Pass?}
    D --> F
    E --> F
    
    F -->|Yes ✅| G{Branch = main?}
    F -->|No ❌| H[❌ Block Merge]
    
    G -->|Yes| I[Trigger Deployment]
    G -->|No| J[✅ Ready to Merge]
    
    I --> K[Deploy Backend]
    I --> L[Deploy Frontend]
    
    K --> M{Health Check?}
    L --> M
    M -->|Pass ✅| N[🚀 Production Live]
    M -->|Fail ❌| O[🔴 Rollback]
```

### 2.3 Caching Strategy

```mermaid
graph TD
    A[Workflow Starts] --> B{Cache Exists?}
    
    subgraph Backend
        B -->|Yes| C[Restore pip cache]
        B -->|No| D[Download all packages]
        C --> E[Install only new deps]
        D --> F[Install all deps]
        E --> G[Save cache]
        F --> G
    end
    
    subgraph Frontend
        B -->|Yes| H[Restore npm cache]
        B -->|No| I[Download all packages]
        H --> J[Install only new deps]
        I --> K[Install all deps]
        J --> L[Save cache]
        K --> L
    end
    
    G --> M[Run Tests]
    L --> M
    
    style C fill:#d4edda
    style H fill:#d4edda
    style D fill:#f8d7da
    style I fill:#f8d7da
```

**Cache Keys:**
- Backend: Hash of `requirements.txt`
- Frontend: Hash of `package-lock.json`

**Performance Impact:**
- ✅ With cache: ~30 seconds install
- ❌ Without cache: ~3-5 minutes install
- 🚀 **5-10x faster** with cache hits

---

<a name="workflows"></a>
## 3. Workflows

### 3.1 Backend CI (`backend.yml`)

**Location:** `.github/workflows/backend.yml`

**Triggers:**
- Push to `main` or `develop` branches (backend changes)
- Pull requests to `main` or `develop` (backend changes)

**Test Matrix:**
- Python versions: 3.11, 3.12
- OS: Ubuntu latest
- **Parallel execution** for faster results

**Pipeline Steps:**
```
┌─────────────────────────────────────────┐
│  Backend CI (Python 3.11, 3.12)        │
├─────────────────────────────────────────┤
│  1. Checkout code                       │
│  2. Setup Python with pip caching       │
│  3. Install dependencies                │
│  4. Flake8: Syntax & style check       │
│  5. Black: Format validation           │
│  6. isort: Import organization         │
│  7. mypy: Static type checking         │
│  8. pytest: Run test suite             │
│  9. Coverage: Generate report          │
│  10. Upload: Send to Codecov           │
└─────────────────────────────────────────┘
```

**Quality Gates:**
- ✅ No syntax errors (flake8 E9, F63, F7, F82)
- ✅ Code formatted with black
- ✅ Imports sorted with isort
- ✅ All tests passing
- ✅ Type hints validated (warnings only)

**Duration:** ~3-5 minutes

---

### 3.2 Frontend CI (`frontend.yml`)

**Location:** `.github/workflows/frontend.yml`

**Triggers:**
- Push to `main` or `develop` branches (frontend changes)
- Pull requests to `main` or `develop` (frontend changes)

**Test Matrix:**
- Node.js versions: 20.x, 22.x
- OS: Ubuntu latest
- **Parallel execution** for faster results

**Pipeline Steps:**
```
┌─────────────────────────────────────────┐
│  Frontend CI (Node 20.x, 22.x)         │
├─────────────────────────────────────────┤
│  1. Checkout code                       │
│  2. Setup Node.js with npm caching      │
│  3. Install dependencies (npm ci)       │
│  4. ESLint: Code quality check         │
│  5. TypeScript: Type validation        │
│  6. Prettier: Format check             │
│  7. Next.js: Production build          │
│  8. Jest: Run test suite               │
└─────────────────────────────────────────┘
```

**Quality Gates:**
- ✅ ESLint passes (no errors)
- ✅ TypeScript compilation succeeds
- ✅ Production build completes
- ✅ Code formatted with Prettier
- ✅ All tests passing

**Duration:** ~4-6 minutes

---

### 3.3 Deploy Workflow (`deploy.yml`)

**Location:** `.github/workflows/deploy.yml`

**Triggers:**
- Push to `main` branch (automatic)
- Manual trigger via `workflow_dispatch`

**Pipeline Steps:**
```
┌─────────────────────────────────────────┐
│  Deploy (main branch only)             │
├─────────────────────────────────────────┤
│  1. Check all CI passed                │
│  2. Deploy backend to Railway          │
│  3. Deploy frontend to Railway         │
│  4. Health check endpoints             │
│  5. Report deployment status           │
└─────────────────────────────────────────┘
```

**Jobs:**

#### Deploy Backend
- Triggers Railway backend deployment
- Runs in production environment
- Includes health check verification

#### Deploy Frontend
- Triggers Railway frontend deployment
- Runs in production environment
- Includes health check verification

#### Deployment Summary
- Reports overall deployment status
- Sends notifications (if configured)

**Duration:** ~2-4 minutes

**Note:** Railway automatically deploys when changes are pushed to main. This workflow provides visibility and manual trigger capability.

---

<a name="quick-reference"></a>
## 4. Quick Reference

### 4.1 Pre-Commit Checklist

**Automated Local Testing:**
```bash
# From project root - runs all CI checks locally
./scripts/test-ci-local.sh

# Test everything (even if no changes)
./scripts/test-ci-local.sh --all
```

This script mirrors GitHub Actions checks:
- Backend: flake8, black, isort, mypy, pytest
- Frontend: ESLint, TypeScript, Prettier, build

### 4.2 Backend Development Commands

```bash
# Navigate to backend
cd backend

# Format code (auto-fix)
black app
isort app

# Lint (check only)
flake8 app

# Type check
mypy app --ignore-missing-imports

# Run tests with coverage
pytest tests/ -v --cov=app

# Coverage report (HTML)
pytest tests/ --cov=app --cov-report=html
open htmlcov/index.html
```

### 4.3 Frontend Development Commands

```bash
# Navigate to frontend
cd frontend

# Format code (auto-fix)
npx prettier --write "src/**/*.{ts,tsx}"

# Lint (auto-fix where possible)
npm run lint -- --fix

# Type check
npx tsc --noEmit

# Build
npm run build

# Clean build
rm -rf .next node_modules
npm install
npm run build
```

### 4.4 GitHub Actions Commands

```bash
# View workflow runs
gh run list

# Watch latest run in real-time
gh run watch

# View specific workflow run
gh run view <run-id>

# Trigger manual deploy
gh workflow run deploy.yml

# View deployment status
gh run list --workflow=deploy.yml
```

### 4.5 Railway Commands

```bash
# View backend logs
railway logs --service=backend

# View frontend logs
railway logs --service=frontend

# View service status
railway status

# Redeploy service
railway up
```

### 4.6 Status Badges

Add to README.md:
```markdown
[![Backend CI](https://github.com/goforwest/BAHR/actions/workflows/backend.yml/badge.svg)](https://github.com/goforwest/BAHR/actions/workflows/backend.yml)
[![Frontend CI](https://github.com/goforwest/BAHR/actions/workflows/frontend.yml/badge.svg)](https://github.com/goforwest/BAHR/actions/workflows/frontend.yml)
[![Deploy](https://github.com/goforwest/BAHR/actions/workflows/deploy.yml/badge.svg)](https://github.com/goforwest/BAHR/actions/workflows/deploy.yml)
```

---

<a name="railway-configuration"></a>
## 5. Railway Configuration

### 5.1 Backend Service

**Build Settings:**
```yaml
Build Command: pip install -r requirements.txt
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

**Environment Variables:**
```env
# Required
DATABASE_URL=postgresql://user:pass@host:5432/bahr
REDIS_URL=redis://host:6379
JWT_SECRET_KEY=your-secret-key-here
ENVIRONMENT=production

# Optional
CORS_ORIGINS=https://your-frontend.railway.app
LOG_LEVEL=info
```

**Healthcheck:**
- Path: `/health`
- Timeout: 300s
- Expected: HTTP 200

### 5.2 Frontend Service

**Build Settings:**
```yaml
Build Command: npm install && npm run build
Start Command: npm start
```

**Environment Variables:**
```env
# Required
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
NODE_ENV=production

# Optional
NEXT_PUBLIC_APP_VERSION=1.0.0
```

**Healthcheck:**
- Path: `/`
- Timeout: 300s
- Expected: HTTP 200

### 5.3 Database Services

**PostgreSQL:**
- Managed by Railway
- Automatic backups
- `$DATABASE_URL` auto-injected

**Redis:**
- Managed by Railway
- Persistence enabled
- `$REDIS_URL` auto-injected

---

<a name="development-workflow"></a>
## 6. Development Workflow

### 6.1 Branch Strategy

```mermaid
graph LR
    A[Local Dev] -->|git push| B[feature/* branch]
    B -->|PR + CI| C[develop branch]
    C -->|Stabilize| D[PR to main]
    D -->|CI + Review| E[main branch]
    E -->|Auto-deploy| F[Railway Production]
    
    style A fill:#e3f2fd
    style B fill:#fff9c4
    style C fill:#fff9c4
    style E fill:#ffecb3
    style F fill:#c8e6c9
```

**Branch Types:**
1. **main** - Production branch (auto-deploys to Railway)
2. **develop** - Development branch (runs CI, no deploy)
3. **feature/***, **fix/***, **refactor/** - Feature branches (CI on PR)

### 6.2 Recommended Git Flow

```bash
# 1. Create feature branch from develop
git checkout develop
git pull origin develop
git checkout -b feature/analysis-caching

# 2. Make changes and commit
git add .
git commit -m "feat: add Redis caching for analysis results"

# 3. Push to GitHub - triggers CI checks
git push origin feature/analysis-caching

# 4. Create PR to develop
# - GitHub Actions runs full CI suite
# - Request code review

# 5. After approval, merge to develop
# - CI runs again
# - No deployment (develop branch)

# 6. When ready for production
git checkout develop
git pull origin develop
git checkout -b release/v1.1.0

# 7. Create PR from release branch to main
# - Final review and testing

# 8. Merge to main
# - CI runs
# - Automatic deployment to Railway
# - Production goes live
```

### 6.3 Branch Protection Rules

**Recommended Settings for `main` branch:**
```yaml
Branch Protection Rules:
  ☑️ Require a pull request before merging
     ☑️ Require approvals: 1+
     ☑️ Dismiss stale pull request approvals when new commits are pushed
     
  ☑️ Require status checks to pass before merging
     ☑️ Require branches to be up to date before merging
     Status checks to require:
        ☑️ Backend CI (test matrix: Python 3.11, 3.12)
        ☑️ Frontend CI (build-and-test matrix: Node 20.x, 22.x)
        ☑️ Frontend CI (code-quality)
        
  ☑️ Require conversation resolution before merging
  
  ☑️ Do not allow bypassing the above settings
  
  ☑️ Restrict who can push to matching branches
     - Add: Project maintainers only
```

---

<a name="troubleshooting"></a>
## 7. Troubleshooting

### 7.1 Backend CI Failures

#### Flake8 Errors
```bash
# View errors
flake8 app

# Common fixes:
# - Fix syntax errors immediately
# - Adjust line length if needed (max 127 chars)
# - Address undefined names
# - Remove unused imports
```

#### Black Formatting
```bash
# Auto-format all code
black app

# Check without modifying
black --check app
```

#### Import Sorting
```bash
# Auto-sort imports
isort app

# Check without modifying
isort --check-only app
```

#### Type Checking
```bash
# Run mypy
mypy app --ignore-missing-imports

# Common fixes:
# - Add type hints to function signatures
# - Import types from typing module
# - Use type: ignore comments sparingly
```

#### Test Failures
```bash
# Run tests with verbose output
pytest tests/ -v

# Run specific test
pytest tests/test_analyzer.py::test_meter_detection -v

# Run with coverage
pytest tests/ --cov=app --cov-report=term-missing

# Debug failing test
pytest tests/test_analyzer.py -v -s  # -s shows print statements
```

### 7.2 Frontend CI Failures

#### ESLint Errors
```bash
# View errors
npm run lint

# Auto-fix where possible
npm run lint -- --fix

# Common errors:
# - Unused variables
# - Missing dependencies in useEffect
# - Console statements in production code
```

#### TypeScript Errors
```bash
# Type check
npx tsc --noEmit

# Common fixes:
# - Add type annotations
# - Import types correctly
# - Fix type mismatches
# - Use type assertions carefully
```

#### Build Failures
```bash
# Clean build
rm -rf .next node_modules
npm install
npm run build

# Check build logs for:
# - Missing environment variables
# - Import errors
# - API route issues
```

#### Prettier Formatting
```bash
# Auto-format all code
npx prettier --write "src/**/*.{ts,tsx,js,jsx,json,css,md}"

# Check without modifying
npx prettier --check "src/**/*.{ts,tsx}"
```

### 7.3 "CI Failed But Works Locally"

**1. Check Python/Node version:**
```bash
# Backend
python --version  # Should be 3.11 or 3.12

# Frontend
node --version    # Should be 20.x or 22.x
```

**2. Clear caches:**
```bash
# Backend
pip cache purge
rm -rf __pycache__ .pytest_cache .coverage

# Frontend
npm cache clean --force
rm -rf .next node_modules package-lock.json
```

**3. Match CI environment:**
```bash
# Backend - install exactly what CI installs
pip install -r requirements.txt -r requirements/development.txt

# Frontend - use ci command like GitHub Actions
npm ci  # Not npm install
```

### 7.4 Deployment Failures

**1. Check Railway logs:**
```bash
railway logs --service=backend
railway logs --service=frontend
```

**2. Verify environment variables:**
- Go to Railway dashboard
- Check all required env vars are set
- Verify no typos in variable names

**3. Health check failures:**
```bash
# Test health endpoint locally
curl http://localhost:8000/health  # Backend
curl http://localhost:3000/        # Frontend
```

**4. Build errors:**
- Review build logs in Railway dashboard
- Check for missing dependencies
- Verify start command is correct

**5. Database connection issues:**
```bash
# Verify DATABASE_URL format
echo $DATABASE_URL
# Should be: postgresql://user:pass@host:5432/dbname

# Test connection
psql $DATABASE_URL -c "SELECT 1;"
```

---

<a name="monitoring"></a>
## 8. Monitoring & Performance

### 8.1 CI/CD Performance Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Backend CI Duration | < 5 min | ~3-4 min ✅ |
| Frontend CI Duration | < 6 min | ~4-5 min ✅ |
| Deploy Duration | < 5 min | ~2-3 min ✅ |
| Cache Hit Rate | > 80% | ~90% ✅ |
| Test Coverage (Backend) | > 70% | TBD 📊 |
| Test Coverage (Frontend) | > 70% | TBD 📊 |

### 8.2 Quality Gates Summary

| Check | Status | Blocking |
|-------|--------|----------|
| Syntax Errors (flake8) | ✅ Active | Yes |
| Format Issues (black/prettier) | ✅ Active | Yes |
| Import Sorting (isort) | ✅ Active | Yes |
| Type Errors (mypy/tsc) | ✅ Active | Yes (warnings only) |
| Failing Tests | ✅ Active | Yes |
| Build Failures | ✅ Active | Yes |
| Low Coverage | ⚠️ Warning | No |

### 8.3 Monitoring Dashboards

**GitHub Actions:**
```
https://github.com/goforwest/BAHR/actions
```

**Railway Dashboard:**
```
https://railway.app/dashboard
```

**Codecov (Coverage Reports):**
```
https://codecov.io/gh/goforwest/BAHR
```

### 8.4 Alerts & Notifications

**GitHub Actions Notifications:**
- Email on workflow failure (default)
- Slack/Discord webhooks (optional - see Railway integrations)

**Railway Deployment Notifications:**
- Deploy status in Railway dashboard
- Optional: Integrate with Slack/Discord

---

## 9. Best Practices

### ✅ DO:
- Run pre-commit checks before pushing (`./scripts/test-ci-local.sh`)
- Write tests for new features (target >70% coverage)
- Keep commits small and focused (atomic commits)
- Update documentation with code changes
- Use feature branches for development
- Review CI logs when builds fail
- Fix CI failures immediately (don't merge broken code)
- Use semantic commit messages (feat:, fix:, docs:, refactor:)

### ❌ DON'T:
- Push directly to `main` (always use PRs)
- Skip tests or linting
- Commit broken code
- Merge failing PRs
- Ignore CI failures ("works on my machine")
- Disable quality gates to force merges
- Commit sensitive data (.env files, secrets)
- Use `git push --force` on shared branches

---

## 10. Git Hooks (Optional)

### Pre-Commit Hook

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash

echo "🔍 Running pre-commit checks..."

# Backend checks
if git diff --cached --name-only | grep -q "^backend/"; then
    echo "→ Checking backend..."
    cd backend || exit 1
    
    echo "  • Running black..."
    black --check app || exit 1
    
    echo "  • Running isort..."
    isort --check-only app || exit 1
    
    echo "  • Running flake8..."
    flake8 app || exit 1
    
    echo "  • Running tests..."
    pytest tests/ -v || exit 1
    
    cd ..
fi

# Frontend checks  
if git diff --cached --name-only | grep -q "^frontend/"; then
    echo "→ Checking frontend..."
    cd frontend || exit 1
    
    echo "  • Running lint..."
    npm run lint || exit 1
    
    echo "  • Running type check..."
    npx tsc --noEmit || exit 1
    
    cd ..
fi

echo "✅ All pre-commit checks passed!"
```

Make executable:
```bash
chmod +x .git/hooks/pre-commit
```

---

## 11. Next Steps & Resources

### Immediate Actions
- [ ] Configure Railway environment variables
- [ ] Link Railway services to GitHub repository
- [ ] Set up branch protection rules on GitHub
- [ ] Add status badges to README.md
- [ ] Configure Codecov token (optional)

### Future Enhancements
- [ ] Add deployment notifications (Slack/Discord)
- [ ] Set up performance monitoring (Railway metrics)
- [ ] Configure error tracking (Sentry)
- [ ] Add E2E tests to CI pipeline
- [ ] Implement canary deployments
- [ ] Add security scanning (Snyk/Dependabot)

### Documentation Resources
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Railway Documentation](https://docs.railway.app/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Next.js Deployment](https://nextjs.org/docs/deployment)
- [BAHR Technical Docs](../docs/README.md)

---

## Changelog

### Version 2.0 (November 9, 2025)
- ✅ Consolidated `CI_CD_GUIDE.md`, `CI_CD_ARCHITECTURE.md`, `CI_CD_QUICKREF.md`
- ✅ Added comprehensive troubleshooting section
- ✅ Enhanced architecture diagrams with Mermaid
- ✅ Added quick reference commands throughout
- ✅ Included performance metrics and monitoring
- ✅ Added best practices and git hooks examples
- ✅ Unified structure for better navigation

### Version 1.0 (November 9, 2025)
- Initial CI/CD pipeline setup
- Backend and frontend workflows
- Railway deployment integration

---

**Maintained By:** BAHR Platform Team  
**Questions?** Check [troubleshooting](#troubleshooting) or create a GitHub issue  
**Related:** [docs/technical/DEPLOYMENT_GUIDE.md](../docs/technical/DEPLOYMENT_GUIDE.md)
