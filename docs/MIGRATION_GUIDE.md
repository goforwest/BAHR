# 🔄 BAHR Repository Migration Guide

**For Developers & Contributors**  
**Migration Date:** November 10, 2025  
**Status:** Ready for Implementation

---

## 📋 What Changed?

The BAHR repository has been restructured for improved organization and maintainability. This guide helps you adapt your local development environment and workflows to the new structure.

---

## 🚨 Breaking Changes Summary

### 1. **Alembic (Database Migrations)**

**Before:**
```bash
# From repository root
alembic upgrade head
alembic revision --autogenerate -m "description"
```

**After:**
```bash
# From backend directory
cd backend
alembic -c database/migrations/alembic.ini upgrade head
alembic -c database/migrations/alembic.ini revision --autogenerate -m "description"
```

**Why:** Migrations moved from `/alembic/` → `/backend/database/migrations/`

---

### 2. **Docker Compose**

**Before:**
```bash
docker-compose up
docker-compose down
```

**After:**
```bash
docker-compose -f infrastructure/docker/docker-compose.yml up
docker-compose -f infrastructure/docker/docker-compose.yml down
```

**Why:** docker-compose.yml moved to `/infrastructure/docker/`

**Pro Tip:** Create an alias in your shell:
```bash
# Add to ~/.zshrc or ~/.bashrc
alias dc='docker-compose -f infrastructure/docker/docker-compose.yml'

# Then use:
dc up
dc down
```

---

### 3. **Python Imports in Tests**

**Before:**
```python
# backend/tests/test_example.py
from backend.app.main import app
```

**After:**
```python
# backend/tests/test_example.py
from app.main import app
```

**Why:** Tests always run from `/backend` directory, so `backend.` prefix is unnecessary

---

### 4. **Pytest Configuration**

**Before:**
```bash
# From repository root
pytest                    # Used root pytest.ini
```

**After:**
```bash
# For backend tests
cd backend
pytest                    # Uses backend/pytest.ini

# For dataset tests
pytest dataset/tests/     # Uses dataset/pytest.ini
```

**Why:** Root `pytest.ini` removed to avoid conflicts; each domain has specific config

---

### 5. **Documentation Locations**

**Before:**
- Implementation guides: `/implementation-guides/`
- Architecture docs: `/docs/ARCHITECTURE_DECISIONS.md`, `/docs/technical/ARCHITECTURE_OVERVIEW.md`

**After:**
- Feature guides: `/docs/features/`
- Architecture docs: `/docs/architecture/`

**Why:** Consolidated documentation into unified `/docs/` structure

---

## 🔧 Migration Steps for Your Local Environment

### Step 1: Backup Your Current Work

```bash
# Commit or stash any uncommitted changes
git status
git stash save "WIP: Pre-migration backup"

# Or commit your work
git add .
git commit -m "WIP: Before repository restructure"
```

### Step 2: Pull Latest Changes

```bash
git checkout main
git pull origin main
```

### Step 3: Clean Up Old Artifacts

```bash
# Remove old Python cache
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete

# Remove old virtual environments (optional - will recreate)
rm -rf .venv venv

# Remove database artifacts (will regenerate)
rm -f dummy.db .coverage
```

### Step 4: Recreate Virtual Environment

```bash
# Create new virtual environment
python3.11 -m venv .venv

# Activate
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate      # Windows

# Install backend dependencies
cd backend
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements/development.txt  # If exists

# Return to root
cd ..
```

### Step 5: Verify Database Migrations

```bash
cd backend

# Check migration status
alembic -c database/migrations/alembic.ini current

# Apply migrations if needed
alembic -c database/migrations/alembic.ini upgrade head

cd ..
```

### Step 6: Verify Docker Setup

```bash
# Build images with new structure
docker-compose -f infrastructure/docker/docker-compose.yml build

# Start services
docker-compose -f infrastructure/docker/docker-compose.yml up -d

# Verify services are running
docker-compose -f infrastructure/docker/docker-compose.yml ps

# Check logs
docker-compose -f infrastructure/docker/docker-compose.yml logs backend

# Stop services
docker-compose -f infrastructure/docker/docker-compose.yml down
```

### Step 7: Run Tests

```bash
# Backend tests
cd backend
pytest -v

# Dataset tests
cd ..
pytest dataset/tests/ -v
```

### Step 8: Update Your Bookmarks/Aliases

**Update shell aliases (optional but recommended):**

```bash
# Add to ~/.zshrc or ~/.bashrc

# Docker Compose shortcut
alias dc='docker-compose -f infrastructure/docker/docker-compose.yml'

# Backend shortcuts
alias backend='cd ~/path/to/BAHR/backend'
alias run-backend='cd ~/path/to/BAHR/backend && uvicorn app.main:app --reload'
alias test-backend='cd ~/path/to/BAHR/backend && pytest -v'

# Alembic shortcuts
alias alembic-migrate='cd ~/path/to/BAHR/backend && alembic -c database/migrations/alembic.ini'

# Frontend shortcuts
alias frontend='cd ~/path/to/BAHR/frontend'
alias run-frontend='cd ~/path/to/BAHR/frontend && npm run dev'
```

Then reload your shell:
```bash
source ~/.zshrc  # or source ~/.bashrc
```

---

## 📂 New File Locations Reference

### Quick Lookup Table

| Old Path | New Path | Notes |
|----------|----------|-------|
| `/alembic/` | `/backend/database/migrations/` | Includes alembic.ini |
| `/alembic.ini` | `/backend/database/migrations/alembic.ini` | Config moved with migrations |
| `/pytest.ini` | **REMOVED** | Use `backend/pytest.ini` or `dataset/pytest.ini` |
| `/docker-compose.yml` | `/infrastructure/docker/docker-compose.yml` | Updated paths inside |
| `/railway.toml` | `/infrastructure/railway/railway.toml` | Infra consolidation |
| `/backend/Dockerfile.dev` | `/infrastructure/docker/backend/Dockerfile.dev` | Docker configs centralized |
| `/backend/Dockerfile.railway` | `/infrastructure/docker/backend/Dockerfile.prod` | Renamed for clarity |
| `/backend/railway.json` | `/infrastructure/railway/backend.json` | Railway configs centralized |
| `/frontend/railway.json` | `/infrastructure/railway/frontend.json` | Railway configs centralized |
| `/implementation-guides/` | `/docs/features/` | Documentation consolidated |
| `/docs/ARCHITECTURE_DECISIONS.md` | `/docs/architecture/DECISIONS.md` | Reorganized |
| `/scripts/seed_database.py` | `/backend/scripts/seed_database.py` | Backend-specific |

---

## 🐛 Common Issues & Solutions

### Issue 1: "alembic: command not found"

**Problem:** Alembic not in PATH or virtual environment not activated

**Solution:**
```bash
# Activate virtual environment
source .venv/bin/activate

# Verify alembic is installed
which alembic
pip list | grep alembic

# If not installed
pip install alembic
```

---

### Issue 2: "alembic.ini not found"

**Problem:** Running alembic from wrong directory or without config flag

**Solution:**
```bash
# Always run from backend directory WITH config flag
cd backend
alembic -c database/migrations/alembic.ini upgrade head
```

---

### Issue 3: "ModuleNotFoundError: No module named 'backend'"

**Problem:** Test imports still using old `from backend.app.*` pattern

**Solution:**
```python
# WRONG (old):
from backend.app.main import app

# CORRECT (new):
from app.main import app
```

**Run from backend directory:**
```bash
cd backend
pytest
```

---

### Issue 4: "docker-compose.yml not found"

**Problem:** Running docker-compose from root without specifying path

**Solution:**
```bash
# Use full path
docker-compose -f infrastructure/docker/docker-compose.yml up

# Or create alias (recommended)
alias dc='docker-compose -f infrastructure/docker/docker-compose.yml'
dc up
```

---

### Issue 5: "Database connection failed after migration"

**Problem:** Environment variables or connection strings outdated

**Solution:**
```bash
# Check .env file exists and is correct
cp .env.example .env

# Edit .env with correct values
# Verify DATABASE_URL points to correct location

# Restart Docker services
docker-compose -f infrastructure/docker/docker-compose.yml down
docker-compose -f infrastructure/docker/docker-compose.yml up -d
```

---

### Issue 6: "Import paths broken in my branch"

**Problem:** Your feature branch has old structure

**Solution:**
```bash
# Save your work
git stash save "WIP: Feature work"

# Update main branch
git checkout main
git pull origin main

# Rebase your branch onto new main
git checkout your-feature-branch
git rebase main

# Fix any import conflicts
# Update any alembic/docker-compose commands in your code

# Continue your work
git stash pop
```

---

## 🧪 Verification Checklist

After migration, verify everything works:

- [ ] Virtual environment activated: `which python` shows `.venv/bin/python`
- [ ] Backend dependencies installed: `pip list | grep fastapi`
- [ ] Database migrations work: `cd backend && alembic -c database/migrations/alembic.ini current`
- [ ] Backend tests pass: `cd backend && pytest`
- [ ] Docker services start: `docker-compose -f infrastructure/docker/docker-compose.yml up -d`
- [ ] API health check: `curl http://localhost:8000/health`
- [ ] Frontend builds: `cd frontend && npm run build`
- [ ] Documentation links work: Check [docs/QUICK_REFERENCE.md](docs/QUICK_REFERENCE.md)

---

## 📚 Updated Documentation

**Must-read documents after migration:**

1. **[REPOSITORY_STRUCTURE.md](REPOSITORY_STRUCTURE.md)** - Visual tree of new structure
2. **[docs/QUICK_REFERENCE.md](docs/QUICK_REFERENCE.md)** - Updated navigation guide
3. **[docs/onboarding/GETTING_STARTED.md](docs/onboarding/GETTING_STARTED.md)** - Updated setup guide
4. **[docs/architecture/OVERVIEW.md](docs/architecture/OVERVIEW.md)** - System architecture

---

## 🔄 CI/CD Changes

**GitHub Actions workflows have been updated:**

- Path filters updated to include new infrastructure paths
- Test commands updated to use correct pytest.ini locations
- Docker build commands reference new paths

**No action required** - workflows automatically use new structure.

---

## 💡 Best Practices Going Forward

### 1. **Always Specify Config Paths**
```bash
# Alembic
alembic -c database/migrations/alembic.ini <command>

# Docker Compose
docker-compose -f infrastructure/docker/docker-compose.yml <command>
```

### 2. **Run Tests from Correct Directory**
```bash
# Backend tests - FROM backend/
cd backend
pytest

# Dataset tests - FROM root
pytest dataset/tests/
```

### 3. **Use Relative Imports in App Code**
```python
# In backend/app/api/v1/endpoints/analyze.py
from app.core.bahr_detector import BahrDetector  # ✅ GOOD
# NOT: from backend.app.core.bahr_detector import BahrDetector  # ❌ BAD
```

### 4. **Document Infrastructure Changes**
When adding new Docker services or deployment configs:
- Add to `/infrastructure/docker/docker-compose.yml`
- Document in `/infrastructure/README.md`
- Update deployment docs in `/docs/deployment/`

### 5. **Keep Documentation in Sync**
When moving/renaming files:
- Update references in `/docs/QUICK_REFERENCE.md`
- Update code examples in feature guides
- Run link checker to verify no broken links

---

## 🆘 Getting Help

**If you encounter issues:**

1. Check this migration guide for common issues
2. Review [docs/guides/TROUBLESHOOTING.md](docs/guides/TROUBLESHOOTING.md)
3. Search existing GitHub issues for similar problems
4. Create a new issue with label `migration-support`
5. Ask in team Slack/Discord channel

**Include in your issue:**
- What you were trying to do
- Exact commands you ran
- Error messages (full stack trace)
- Your environment (OS, Python version, etc.)

---

## 📊 Migration Validation

**Run this comprehensive test to verify everything works:**

```bash
#!/bin/bash
# save as: scripts/verify-migration.sh

set -e

echo "🔍 Verifying BAHR repository migration..."

# 1. Check Python environment
echo "✓ Checking Python environment..."
source .venv/bin/activate
python --version

# 2. Test backend imports
echo "✓ Testing backend imports..."
cd backend
python -c "from app.main import app; print('✓ Imports working')"

# 3. Test alembic
echo "✓ Testing Alembic..."
alembic -c database/migrations/alembic.ini current

# 4. Run backend tests
echo "✓ Running backend tests..."
pytest -v --maxfail=1

cd ..

# 5. Test Docker
echo "✓ Testing Docker Compose..."
docker-compose -f infrastructure/docker/docker-compose.yml config > /dev/null

# 6. Test dataset
echo "✓ Running dataset tests..."
pytest dataset/tests/ -v --maxfail=1

echo "✅ All verifications passed!"
```

**Run it:**
```bash
chmod +x scripts/verify-migration.sh
./scripts/verify-migration.sh
```

---

## 📝 Summary of Key Commands

### Before Migration
```bash
# Alembic
alembic upgrade head

# Docker
docker-compose up

# Tests
pytest  # from root
```

### After Migration
```bash
# Alembic
cd backend && alembic -c database/migrations/alembic.ini upgrade head

# Docker
docker-compose -f infrastructure/docker/docker-compose.yml up

# Tests
cd backend && pytest        # backend tests
pytest dataset/tests/       # dataset tests (from root)
```

---

**Questions?** Open an issue with label `migration-support`

**Version:** 1.0  
**Last Updated:** November 10, 2025  
**Related:** [REPOSITORY_RESTRUCTURING_PLAN.md](REPOSITORY_RESTRUCTURING_PLAN.md), [REPOSITORY_STRUCTURE.md](REPOSITORY_STRUCTURE.md)
