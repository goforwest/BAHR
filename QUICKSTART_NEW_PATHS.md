# 🚀 Quick Start - Updated Commands After Restructuring

**Updated:** November 10, 2025  
**Applies to:** Repository after restructuring (commits d2a37bc → 8fcdce9)

---

## ⚡ Essential Command Updates

### Docker Compose (Changed)

**OLD:**
```bash
docker-compose up -d
docker-compose down
docker-compose ps
```

**NEW:**
```bash
docker-compose -f infrastructure/docker/docker-compose.yml up -d
docker-compose -f infrastructure/docker/docker-compose.yml down
docker-compose -f infrastructure/docker/docker-compose.yml ps
```

**Tip:** Create an alias to save typing:
```bash
# Add to ~/.zshrc or ~/.bashrc
alias dc='docker-compose -f infrastructure/docker/docker-compose.yml'

# Then use:
dc up -d
dc down
dc ps
```

---

### Alembic Migrations (Changed)

**OLD:**
```bash
alembic upgrade head
alembic current
alembic revision --autogenerate -m "description"
```

**NEW:**
```bash
cd backend
alembic -c database/migrations/alembic.ini upgrade head
alembic -c database/migrations/alembic.ini current
alembic -c database/migrations/alembic.ini revision --autogenerate -m "description"
```

**Tip:** Create a shell function:
```bash
# Add to ~/.zshrc or ~/.bashrc
bahr-alembic() {
    (cd ~/Desktop/Personal/BAHR/backend && alembic -c database/migrations/alembic.ini "$@")
}

# Then use from anywhere:
bahr-alembic upgrade head
bahr-alembic current
```

---

### Backend Testing (Changed)

**OLD:**
```bash
pytest tests/
pytest tests/core/test_bahr_detector.py -v
```

**NEW:**
```bash
cd backend
pytest tests/
pytest tests/core/test_bahr_detector.py -v
pytest tests/ --cov=app --cov-report=term-missing
```

**Note:** Must run from `backend/` directory due to `pythonpath = .` in pytest.ini

---

### Database Seeding (Changed)

**OLD:**
```bash
python scripts/seed_database.py
```

**NEW:**
```bash
cd backend
python scripts/seed_database.py
```

---

### Backend Server (Unchanged)

**Still works the same:**
```bash
cd backend
source venv/bin/activate  # or your virtual environment
uvicorn app.main:app --reload
```

---

### Frontend (Unchanged)

**Still works the same:**
```bash
cd frontend
npm run dev
```

---

## 📁 New Directory Structure Reference

```
BAHR/
├── backend/
│   ├── database/
│   │   └── migrations/        # ← Alembic moved here
│   │       ├── alembic.ini   # ← Alembic config moved here
│   │       └── versions/
│   ├── scripts/              # ← seed_database.py moved here
│   └── pytest.ini            # ← Updated with pythonpath
│
├── infrastructure/            # ← NEW
│   ├── docker/
│   │   └── docker-compose.yml  # ← Moved here
│   └── railway/
│
├── docs/
│   └── features/             # ← implementation-guides moved here
│
└── scripts/
    ├── setup/                # ← Organized
    ├── health/
    └── testing/
```

---

## 🔧 Complete Daily Development Workflow

### 1. Start Development Environment

```bash
# From project root
cd ~/Desktop/Personal/BAHR

# Start databases
docker-compose -f infrastructure/docker/docker-compose.yml up -d

# Verify services running
docker ps | grep bahr
```

### 2. Update Database Schema (if needed)

```bash
cd backend

# Check current migration status
alembic -c database/migrations/alembic.ini current

# Apply migrations
alembic -c database/migrations/alembic.ini upgrade head

# Or create new migration
alembic -c database/migrations/alembic.ini revision --autogenerate -m "Add new field"
```

### 3. Start Backend Server

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

### 4. Start Frontend (in separate terminal)

```bash
cd ~/Desktop/Personal/BAHR/frontend
npm run dev
```

### 5. Run Tests

```bash
# Backend tests
cd ~/Desktop/Personal/BAHR/backend
pytest tests/ -v

# Dataset tests
cd ~/Desktop/Personal/BAHR/dataset
pytest tests/ -v
```

---

## 🛠️ Recommended Shell Aliases

Add these to your `~/.zshrc` or `~/.bashrc`:

```bash
# BAHR Project Aliases
export BAHR_ROOT="$HOME/Desktop/Personal/BAHR"

# Docker Compose shortcut
alias bahr-dc='docker-compose -f $BAHR_ROOT/infrastructure/docker/docker-compose.yml'

# Alembic shortcut
bahr-alembic() {
    (cd "$BAHR_ROOT/backend" && alembic -c database/migrations/alembic.ini "$@")
}

# Quick navigation
alias bahr='cd $BAHR_ROOT'
alias bahr-backend='cd $BAHR_ROOT/backend'
alias bahr-frontend='cd $BAHR_ROOT/frontend'

# Quick start
bahr-start() {
    echo "Starting BAHR services..."
    bahr-dc up -d
    echo "✓ Databases started"
}

bahr-stop() {
    echo "Stopping BAHR services..."
    bahr-dc down
    echo "✓ Services stopped"
}

# Quick testing
bahr-test() {
    echo "Running backend tests..."
    (cd "$BAHR_ROOT/backend" && pytest tests/ -v)
}
```

**After adding aliases:**
```bash
source ~/.zshrc  # or source ~/.bashrc

# Then use:
bahr-start           # Start databases
bahr-stop            # Stop databases
bahr-alembic current # Check migrations
bahr-test            # Run tests
bahr-backend         # Jump to backend directory
```

---

## 📋 Troubleshooting Updated Paths

### Issue: "alembic: command not found" when using new path

**Solution:**
```bash
# Activate virtual environment first
cd backend
source venv/bin/activate
alembic -c database/migrations/alembic.ini --version
```

### Issue: "ModuleNotFoundError: No module named 'app'" in tests

**Solution:**
```bash
# Must run pytest from backend/ directory
cd backend
pytest tests/
```

### Issue: "docker-compose.yml not found"

**Solution:**
```bash
# Use full path to new location
docker-compose -f infrastructure/docker/docker-compose.yml up -d
```

### Issue: Old git hooks or scripts failing

**Solution:**
```bash
# Update any custom scripts with new paths
# Check .git/hooks/ for outdated paths
grep -r "docker-compose.yml" .git/hooks/
grep -r "alembic upgrade" .git/hooks/
```

---

## 🔄 Migration Checklist for Your Local Environment

- [ ] Update shell aliases (add to ~/.zshrc)
- [ ] Source updated shell config: `source ~/.zshrc`
- [ ] Test Docker Compose: `bahr-dc ps` (or use alias)
- [ ] Test Alembic: `bahr-alembic current` (or cd backend && alembic -c database/migrations/alembic.ini current)
- [ ] Test backend tests: `cd backend && pytest tests/ --collect-only`
- [ ] Update any custom scripts referencing old paths
- [ ] Update IDE run configurations (if using PyCharm/VSCode)
- [ ] Clear old .pyc files: `find . -type d -name __pycache__ -exec rm -rf {} +`

---

## 📚 Reference Documentation

- **Full Setup Guide:** `docs/onboarding/GETTING_STARTED.md`
- **Validation Report:** `docs/RESTRUCTURING_VALIDATION_REPORT.md`
- **Execution Summary:** `docs/RESTRUCTURING_EXECUTION_SUMMARY.md`
- **Feature Guides:** `docs/features/` (was `implementation-guides/`)

---

## ✅ Quick Validation

Test that everything works:

```bash
# 1. Databases
docker-compose -f infrastructure/docker/docker-compose.yml up -d
docker ps | grep bahr  # Should show postgres and redis

# 2. Alembic
cd backend
alembic -c database/migrations/alembic.ini current  # Should show current revision

# 3. Tests
pytest tests/ --collect-only  # Should discover 20+ tests

# 4. Backend imports
python -c "from app.main import app; print('✓ OK')"  # Should print ✓ OK

# 5. Stop services
cd ..
docker-compose -f infrastructure/docker/docker-compose.yml down
```

---

**Last Updated:** November 10, 2025  
**Questions?** See `docs/RESTRUCTURING_COMPLETE.md` for full migration details
