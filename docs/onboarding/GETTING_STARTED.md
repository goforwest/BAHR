# BAHR Platform - Getting Started Guide
## Complete Setup & Onboarding for Developers

**Category:** Onboarding  
**Status:** 🎯 Active  
**Version:** 2.1  
**Last Updated:** 2025-11-10  
**Audience:** Developers, New Contributors  
**Consolidates:** QUICK_START_GUIDE.md + START_HERE.md + START_HERE_DEVELOPER.md  
**Related Docs:** [Phase 0 Setup](../phases/PHASE_0_SETUP.md), [Week 1 Checklist](../checklists/WEEK_1_CRITICAL.md)

---

## 📋 Table of Contents

1. [🚨 Critical Updates - Read First!](#-critical-updates---read-first)
2. [⚡ Express 5-Minute Setup](#-express-5-minute-setup) (Existing Repository)
3. [🏗️ Complete 30-Minute Setup](#️-complete-30-minute-setup) (New Project From Scratch)
4. [🆘 Troubleshooting](#-troubleshooting)
5. [📚 Next Steps](#-next-steps)

---

## 🚨 Critical Updates - Read First!

### Recent Changes (November 8-9, 2025)

**If you're starting Week 1, read this section carefully!**

#### 1️⃣ Timeline Extended to 14 Weeks ✅

**Before:** 12 weeks (too aggressive)
**After:** 14 weeks (realistic and sustainable)

```yaml
New Distribution:
  Week 1-2: Setup + Dataset preparation (was 1 week!)
  Week 3-5: Prosody Engine (was 1 week! 😱)
  Week 6: API Integration
  Week 7-8: Polish + Optimization
  Week 9-10: Testing
  Week 11-12: Beta
  Week 13: Production Launch
  Week 14: Buffer for emergencies
```

📖 **Reference:** [PROJECT_TIMELINE.md](docs/planning/PROJECT_TIMELINE.md)

---

#### 2️⃣ Day 1: Test CAMeL Tools on M1/M2! 🔴

**Problem:** CAMeL Tools may not work on ARM64
**Solution:** Test 3 approaches on Day 1

```bash
# Day 1 - First Hour!
# 1. Try ARM64 native
arch -arm64 pip install camel-tools==1.5.2

# 2. If fails, try Rosetta
arch -x86_64 pip install camel-tools==1.5.2

# 3. If fails, use Docker
# docker run --platform=linux/amd64 ...
```

**⏱️ Time:** 30-60 minutes (Day 1)
📖 **Reference:** [PHASE_0_SETUP.md](docs/phases/PHASE_0_SETUP.md) Section 4.5

---

#### 3️⃣ Week 2: Allocate Time for Data Annotation ⏰

**New:** 2-3 hours/day for manual annotation

```yaml
Week 2 Schedule:
  Day 2: 50 verses (3 hours)
  Day 3: 25 verses (2 hours)
  Day 4: 25 verses (2 hours)
  Total: 100 verses in 3 days

Annotation Rate:
  - ~10-15 minutes/verse
  - Includes: verification, taqti', documentation
```

**✅ Action:** Prepare verse sources (Al-Diwan) in advance

---

#### 4️⃣ Prevent Scope Creep: New File! 🛡️

**New File:** [docs/planning/DEFERRED_FEATURES.md](docs/planning/DEFERRED_FEATURES.md)

**Deferred Features (Don't Develop Now!):**
- ❌ Competition System (Phase 2)
- ❌ Social Features (Phase 2)
- ❌ AI Poet (Phase 2)
- ❌ Rhyme Analysis (Post-MVP)
- ❌ Rhetorical Analysis (Post-MVP)

**Golden Rule:**
> New idea? → Write it in `DEFERRED_FEATURES.md` → Don't develop it now!

---

#### 5️⃣ Quick Wins: 5.5 Hours Save 15-20 Hours! 🚀

**New File:** [docs/planning/QUICK_WINS.md](docs/planning/QUICK_WINS.md)

**8 High-Impact Tasks in Week 1-2:**

| Task | Time | ROI |
|------|------|-----|
| Golden Set (20 perfect verses) | 60 min | Immediate testing |
| Mock API Endpoint | 45 min | Frontend starts Week 2 |
| 100+ Normalization Tests | 90 min | Prevents bugs |
| Database Seeding Script | 45 min | Fast setup |
| Monitoring Dashboard | 30 min | Early detection |
| .env.example | 15 min | No config errors |
| Pre-commit Hooks | 20 min | Code quality |
| API Docs Stubs | 30 min | Clear contract |

**ROI:** 5.5 hours → Save 15-20 hours = **3x return!**

---

### 🔥 Red Flags - Avoid These Mistakes!

#### ❌ Don't:
1. **Don't start development without M1/M2 testing first** - Could cost you a week!
2. **Don't develop features outside MVP scope** - Use DEFERRED_FEATURES.md
3. **Don't skip Quick Wins** - They save time later
4. **Don't underestimate data annotation time** - 2-3 hours/day required
5. **Don't skip Monitoring setup** - Week 2 is critical!
6. **Don't forget to write tests first** - TDD saves debugging time

#### ✅ Do:
1. **Test M1/M2 compatibility Day 1** - 1 hour prevents disaster
2. **Execute Quick Wins in Week 1** - 5.5 hours smart investment
3. **Allocate daily time for annotation in Week 2** - Quality > Speed
4. **Use Mock API for parallel development** - Frontend doesn't wait till Week 5
5. **Review DEFERRED_FEATURES.md for every idea** - Stay focused
6. **Update docs/project-management/PROGRESS_LOG_CURRENT.md daily** - 5 min documentation prevents "Where was I?"

---

### 📂 New Files You Must Know

1. **[docs/planning/DEFERRED_FEATURES.md](docs/planning/DEFERRED_FEATURES.md)** ✨
   - **What:** List of deferred features
   - **Why:** Prevent scope creep
   - **When:** Before Week 1 + when new ideas arise

2. **[docs/planning/QUICK_WINS.md](docs/planning/QUICK_WINS.md)** ✨
   - **What:** 8 quick high-impact tasks
   - **Why:** Accelerate development
   - **When:** Start of Week 1

3. **[docs/technical/DEPLOYMENT_GUIDE.md](docs/technical/DEPLOYMENT_GUIDE.md)** (Updated)
   - **What:** Docker, migrations, hosting options
   - **Why:** Production-ready from Day 1
   - **When:** Week 1 (setup Docker Compose)

4. **[docs/technical/PERFORMANCE_TARGETS.md](docs/technical/PERFORMANCE_TARGETS.md)** (Updated)
   - **What:** Monitoring, alerting, metrics
   - **Why:** Detect problems early
   - **When:** Week 2 (setup Grafana)

---

### ✅ Pre-Week 1 Checklist

```yaml
☐ Read this file (Getting Started Guide)
☐ Reviewed PROJECT_TIMELINE.md (14 weeks)
☐ Understood DEFERRED_FEATURES.md (what NOT to do)
☐ Reviewed QUICK_WINS.md (what to do first)
☐ Understood M1/M2 testing requirements
☐ Read DEPLOYMENT_GUIDE.md (Docker Compose)
☐ Ready to allocate 2-3 hours/day in Week 2 for annotation
```

---

## ⚡ Express 5-Minute Setup

**Use this if:** You're cloning an existing BAHR repository

**Target Audience:** New developers joining the project
**Prerequisites:** Git installed, basic command-line knowledge
**Estimated Time:** 5-10 minutes

---

### System Requirements

**Required Software:**
- **Operating System:** macOS, Linux, or Windows (WSL2)
- **Python:** 3.11 or higher
- **Node.js:** 20.0 or higher (for frontend, Week 5+)
- **Git:** 2.30+
- **Docker:** 20.10+ (for PostgreSQL and Redis)

**Recommended Hardware:**
- **RAM:** 8GB minimum (16GB recommended)
- **Storage:** 5GB free space
- **Network:** Stable internet for package downloads

**For Apple Silicon (M1/M2/M3) Users:**
- Rosetta 2 installed (automatic on first native app run)
- Ensure Docker is running with Apple Silicon support

---

### Step 1: Clone Repository

```bash
# Clone the repository
git clone https://github.com/goforwest/BAHR.git
cd BAHR

# Verify you're in the right place
ls -la
# Should see: backend/, docs/, dataset/, etc.
```

---

### Step 2: Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create Python virtual environment
python3.11 -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# OR
.\venv\Scripts\activate   # Windows

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements/base.txt
pip install -r requirements/development.txt

# ⚠️ CRITICAL TEST: Verify CAMeL Tools (M1/M2 compatibility check)
python -c "from camel_tools.morphology.database import MorphologyDB; print('✅ CAMeL Tools OK')"

# If the above fails on M1/M2, try:
# arch -arm64 pip install camel-tools==1.5.2
# python -c "from camel_tools.morphology.database import MorphologyDB; print('✅ OK')"
```

**Expected Output:**
```
✅ CAMeL Tools OK
```

If you see an error, check [docs/technical/NLP_INTEGRATION_GUIDE.md](docs/technical/NLP_INTEGRATION_GUIDE.md) for troubleshooting.

---

### Step 3: Start Database Services (Docker)

```bash
# Navigate back to project root
cd ..

# Start all services using Docker Compose
docker-compose up -d

# Verify containers are running
docker ps
# Should show: bahr_postgres and bahr_redis both "Up"
```

**Expected Output:**
```
CONTAINER ID   IMAGE               STATUS         PORTS
abc123...      postgres:15-alpine  Up 5 seconds   0.0.0.0:5432->5432/tcp
def456...      redis:7-alpine      Up 3 seconds   0.0.0.0:6379->6379/tcp
```

---

### Step 4: Configure Environment Variables

```bash
cd backend

# Copy example environment file
cp .env.example .env

# Quick .env generator (optional):
cat > .env << 'EOF'
PROJECT_NAME=BAHR API
SECRET_KEY=dev-secret-key-$(openssl rand -hex 32)
DATABASE_URL=postgresql://bahr:bahr_password@localhost:5432/bahr_dev
REDIS_URL=redis://localhost:6379/0
LOG_LEVEL=DEBUG
RATE_LIMIT_REQUESTS=1000
RATE_LIMIT_PERIOD=3600
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
EOF
```

---

### Step 5: Initialize Database

```bash
# Run database migrations (creates tables)
alembic upgrade head

# Seed initial data (16 Arabic prosody meters + 8 tafa'il)
python scripts/seed_database.py

# Verify database is populated
docker exec bahr_postgres psql -U bahr -d bahr_dev -c "SELECT COUNT(*) FROM meters;"
# Should return: count: 16
```

**Expected Output:**
```
INFO  [alembic.runtime.migration] Running upgrade  -> a8bdbba834b3, Initial schema
✅ Database migrations complete

Seeding meters...
✅ Seeded 16 meters successfully
✅ Seeded 8 tafa'il successfully
```

---

### Step 6: Start Backend Server

```bash
# Start FastAPI development server with hot reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Server should start on http://localhost:8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

---

### Step 7: Verify Installation

Open a **new terminal** (keep server running) and test:

```bash
# Test health endpoint
curl http://localhost:8000/health
# Expected: {"status":"healthy","timestamp":1699999999.99,"version":"1.0.0"}

# Test analysis endpoint (basic)
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"text":"قفا نبك من ذكرى حبيب ومنزل"}'

# Expected: JSON response with meter detection ("الطويل")
```

**Access API Documentation:**
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

### ✅ Express Setup Success Checklist

After completing the setup, verify:

- [ ] Python virtual environment activated
- [ ] CAMeL Tools import successful (critical for M1/M2)
- [ ] PostgreSQL container running (port 5432)
- [ ] Redis container running (port 6379)
- [ ] Database migrations applied (16 meters + 8 tafa'il seeded)
- [ ] Backend server running (http://localhost:8000)
- [ ] Health endpoint returns `{"status":"healthy"}`
- [ ] Swagger UI accessible (http://localhost:8000/docs)
- [ ] Test analysis request succeeds

**All checked?** 🎉 **You're ready to start developing!**

---

## 🏗️ Complete 30-Minute Setup

**Use this if:** You're creating a new BAHR project from scratch

**Target Audience:** Solo developers, forks, or teaching environment
**Prerequisites:** Git, Docker, Python 3.11+, Node.js 20+
**Estimated Time:** 30 minutes

---

### Prerequisites

Before starting, ensure you have:
- **Git** installed
- **Docker** and **Docker Compose** installed
- **Node.js** 18+ and **npm** installed
- **Python** 3.11+ installed
- **Code editor** (VS Code recommended)
- **Terminal** access

**System Requirements:**
- macOS, Linux, or Windows with WSL2
- 8GB+ RAM
- 10GB+ free disk space

---

### Step 1: Create Project Structure (5 minutes)

#### 1.1 Create Project Directory

```bash
# Create main project directory
mkdir BAHR
cd BAHR

# Create backend and frontend directories
mkdir backend frontend

# Verify structure
ls -la
# Should show: backend/ frontend/
```

#### 1.2 Initialize Git Repository

```bash
# Initialize Git
git init

# Create .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
*.egg-info/
.pytest_cache/

# Node
node_modules/
.next/
out/
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# Environment
.env

# Database
*.db
*.sqlite

# OS
.DS_Store
Thumbs.db

# Docker
*.log
EOF

# Initial commit
git add .
git commit -m "Initial commit: Project structure"
```

---

### Step 2: Setup Backend (10 minutes)

#### 2.1 Create Backend Project Structure

```bash
cd backend

# Create directory structure
mkdir -p app/{core,api/v1/endpoints,models,schemas,db,nlp,prosody,services,utils}
mkdir -p tests/{nlp,prosody,api,fixtures}
mkdir -p alembic/versions
mkdir scripts

# Create __init__.py files
touch app/__init__.py
touch app/core/__init__.py
touch app/api/__init__.py
touch app/api/v1/__init__.py
touch app/api/v1/endpoints/__init__.py
touch app/models/__init__.py
touch app/schemas/__init__.py
touch app/db/__init__.py
touch app/nlp/__init__.py
touch app/prosody/__init__.py
touch app/services/__init__.py
touch app/utils/__init__.py
touch tests/__init__.py
touch tests/nlp/__init__.py
touch tests/prosody/__init__.py
touch tests/api/__init__.py

# Verify structure
tree -L 3 app/
```

#### 2.2 Create Requirements Files

```bash
# Create requirements structure
mkdir requirements

# Base requirements (production)
cat > requirements/base.txt << 'EOF'
# FastAPI
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6

# Database
sqlalchemy==2.0.23
alembic==1.12.1
psycopg2-binary==2.9.9

# Redis
redis==5.0.1

# Pydantic
pydantic==2.5.0
pydantic-settings==2.1.0

# Security
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
bcrypt==4.0.1

# Arabic NLP
camel-tools==1.5.2

# Monitoring
prometheus-client==0.19.0

# Utilities
python-dotenv==1.0.0
tenacity==8.2.3
EOF

# Development requirements
cat > requirements/development.txt << 'EOF'
-r base.txt

# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
httpx==0.25.2

# Code Quality
black==23.11.0
ruff==0.1.6
mypy==1.7.1
bandit==1.7.5

# Pre-commit
pre-commit==3.5.0
EOF

# Production requirements
cat > requirements/production.txt << 'EOF'
-r base.txt

# Production Server
gunicorn==21.2.0

# Error Tracking
sentry-sdk[fastapi]==1.38.0
EOF
```

#### 2.3 Create Python Virtual Environment

```bash
# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# .\venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements/base.txt
pip install -r requirements/development.txt

# Verify installation
python -c "import fastapi; print(f'FastAPI {fastapi.__version__} installed')"
```

#### 2.4 Create Basic FastAPI App

```bash
# Create main.py
cat > app/main.py << 'EOF'
"""BAHR Platform - FastAPI Application"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="BAHR - Arabic Poetry Platform",
    description="Arabic Poetry Analysis and Generation API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "مرحباً بك في منصة بَحْر", "status": "healthy"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
EOF

# Test server
uvicorn app.main:app --reload &
sleep 3
curl http://localhost:8000/
# Should return JSON with "مرحباً بك في منصة بَحْر"
pkill -f uvicorn
```

#### 2.5 Create Environment File

```bash
cat > .env.example << 'EOF'
# Environment
PROJECT_NAME=BAHR API
ENVIRONMENT=development
DEBUG=true

# Database
DATABASE_URL=postgresql://bahr:bahr_password@localhost:5432/bahr_dev

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=CHANGE_THIS_TO_RANDOM_SECRET_KEY_IN_PRODUCTION
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Rate Limiting
RATE_LIMIT_REQUESTS=1000
RATE_LIMIT_PERIOD=3600

# Feature Flags
ENABLE_AI_GENERATION=false
ENABLE_COMPETITIONS=false

# Logging
LOG_LEVEL=DEBUG
EOF

# Copy to .env
cp .env.example .env

# Generate random secret key
python3 -c "import secrets; print(f'SECRET_KEY={secrets.token_urlsafe(32)}')" >> .env
```

---

### Step 3: Setup Frontend (10 minutes)

#### 3.1 Create Next.js Project

```bash
cd ../frontend

# Create Next.js app
npx create-next-app@latest . --typescript --tailwind --app --no-src-dir --import-alias "@/*"

# Answer prompts:
# ✔ Would you like to use TypeScript? Yes
# ✔ Would you like to use ESLint? Yes
# ✔ Would you like to use Tailwind CSS? Yes
# ✔ Would you like to use `src/` directory? No
# ✔ Would you like to use App Router? Yes
# ✔ Would you like to customize the default import alias? Yes (@/*)
```

#### 3.2 Install Additional Dependencies

```bash
npm install @tanstack/react-query axios zustand react-hook-form zod @hookform/resolvers
npm install framer-motion recharts clsx tailwind-merge
npm install -D @types/node
```

#### 3.3 Configure Environment

```bash
cat > .env.local << 'EOF'
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
EOF

cat > .env.example << 'EOF'
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
EOF
```

---

### Step 4: Setup Docker (5 minutes)

#### 4.1 Create Docker Compose File

```bash
cd ..  # Back to project root

cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    container_name: bahr_postgres
    environment:
      POSTGRES_USER: bahr
      POSTGRES_PASSWORD: bahr_password
      POSTGRES_DB: bahr_dev
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U bahr"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: bahr_redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
  redis_data:
EOF
```

#### 4.2 Start Docker Services

```bash
# Start PostgreSQL and Redis
docker-compose up -d

# Verify services are running
docker-compose ps

# Expected output:
# NAME              STATUS    PORTS
# bahr_postgres     Up        0.0.0.0:5432->5432/tcp
# bahr_redis        Up        0.0.0.0:6379->6379/tcp

# Test PostgreSQL connection
docker exec bahr_postgres psql -U bahr -d bahr_dev -c "SELECT version();"

# Test Redis connection
docker exec bahr_redis redis-cli ping
# Should return: PONG
```

---

### Step 5: Verify Everything Works (5 minutes)

#### 5.1 Test Backend

```bash
cd backend

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# .\venv\Scripts\activate  # Windows

# Start FastAPI server
uvicorn app.main:app --reload

# In another terminal, test endpoints:
curl http://localhost:8000/
curl http://localhost:8000/health
curl http://localhost:8000/docs  # Open in browser for Swagger UI

# Stop server (Ctrl+C)
```

#### 5.2 Test Frontend

```bash
cd ../frontend

# Start Next.js dev server
npm run dev

# Open browser: http://localhost:3000
```

---

### ✅ Complete Setup Success!

Your BAHR development environment is fully set up. You should have:

✅ Backend FastAPI server running on http://localhost:8000
✅ Frontend Next.js app running on http://localhost:3000
✅ PostgreSQL database running on localhost:5432
✅ Redis cache running on localhost:6379
✅ API documentation at http://localhost:8000/docs

**Total setup time: ~30 minutes**

---

## 🆘 Troubleshooting

### Issue 1: CAMeL Tools Import Error (M1/M2 Macs)

**Symptom:**
```
ImportError: cannot import name 'MorphologyDB' from 'camel_tools.morphology.database'
```

**Solution:**
```bash
# Reinstall with ARM64 native support
pip uninstall camel-tools
arch -arm64 pip install camel-tools==1.5.2

# If still fails, use Rosetta (slower but more compatible)
arch -x86_64 pip install camel-tools==1.5.2
```

📖 **Reference:** [docs/technical/NLP_INTEGRATION_GUIDE.md](docs/technical/NLP_INTEGRATION_GUIDE.md) Section 3.2

---

### Issue 2: Database Connection Error

**Symptom:**
```
sqlalchemy.exc.OperationalError: could not connect to server
```

**Solution:**
```bash
# Verify PostgreSQL is running
docker ps | grep postgres

# If not running, start it
docker-compose up -d postgres

# Verify connection manually
docker exec bahr_postgres psql -U bahr -d bahr_dev -c "SELECT 1;"
```

---

### Issue 3: Redis Connection Error

**Symptom:**
```
redis.exceptions.ConnectionError: Error connecting to Redis
```

**Solution:**
```bash
# Verify Redis is running
docker ps | grep redis

# If not running, start it
docker-compose up -d redis

# Test connection
docker exec bahr_redis redis-cli PING
# Expected: PONG
```

---

### Issue 4: Port Already in Use

**Symptom:**
```
OSError: [Errno 48] Address already in use
```

**Solution:**
```bash
# Find process using port 8000
lsof -i :8000

# Kill process (replace PID)
kill -9 <PID>

# Or use different port
uvicorn app.main:app --reload --port 8001
```

---

### Issue 5: Alembic Migration Fails

**Symptom:**
```
alembic.util.exc.CommandError: Can't locate revision identified by 'head'
```

**Solution:**
```bash
# Reset Alembic (development only, destroys data)
alembic downgrade base
alembic upgrade head

# If that fails, recreate database
docker-compose down -v
docker-compose up -d
# Then repeat migrations
```

---

## 📚 Next Steps

Now that your environment is set up:

### 1. Understand the Architecture (20 min)

📖 Read: [docs/technical/ARCHITECTURE_OVERVIEW.md](docs/technical/ARCHITECTURE_OVERVIEW.md)

**Key Concepts:**
- Request flow (Client → FastAPI → Prosody Engine → Database)
- Interface contracts (ITextNormalizer, IMeterDetector, etc.)
- Caching strategy (Redis integration)
- Error handling (standardized envelopes)

---

### 2. Explore the Prosody Engine (30 min)

📖 Read: [docs/technical/PROSODY_ENGINE.md](docs/technical/PROSODY_ENGINE.md)

**Key Topics:**
- Arabic text normalization (removing diacritics, unifying characters)
- Syllable segmentation (CV patterns)
- Meter detection algorithm (pattern matching)
- Confidence calibration

---

### 3. Execute Quick Wins (Week 1-2)

📖 Read: [docs/planning/QUICK_WINS.md](docs/planning/QUICK_WINS.md)

**Recommended Order:**
1. Create Golden Set (20 perfect verses) - 60 min
2. Write 100+ Normalization Tests - 90 min
3. Create Mock API endpoint - 45 min
4. Database Seeding Script - 45 min
5. Setup .env.example - 15 min
6. Setup Pre-commit Hooks - 20 min

---

### 4. Review Current Week's Tasks

📖 Read: [docs/planning/PROJECT_TIMELINE.md](docs/planning/PROJECT_TIMELINE.md)

**Week 1 Priorities:**
- Day 1: M1/M2 compatibility testing (CRITICAL!)
- Day 2: Golden Set creation
- Day 3: Database migrations
- Day 4: Unit tests (prosody modules)
- Day 5: Weekly review

---

### 5. Run Tests

```bash
# Run unit tests
cd backend
source venv/bin/activate
pytest tests/

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_normalizer.py -v
```

---

### 6. Make Your First Contribution

**Good First Issues:**
- Add test cases for edge cases (empty input, very long text)
- Improve error messages (make them more user-friendly)
- Add logging to track performance bottlenecks
- Document a function or class that's missing docstrings

**Workflow:**
```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes
# ... edit files ...

# Run tests
pytest tests/

# Commit
git add .
git commit -m "feat: add XYZ feature"

# Push and create PR
git push origin feature/your-feature-name
# Then create Pull Request on GitHub
```

---

## 🎓 Learning Resources

### Arabic Prosody (علم العروض):
- **Classical Reference:** الكتاب الكافي في علم العروض والقوافي (online PDF)
- **Interactive Tutorial:** https://www.aldiwan.net/arood.htm
- **YouTube Series:** "تعلم العروض" (Search on YouTube)

### FastAPI:
- **Official Tutorial:** https://fastapi.tiangolo.com/tutorial/
- **Advanced Guide:** https://fastapi.tiangolo.com/advanced/
- **Async Python:** https://realpython.com/async-io-python/

### Arabic NLP:
- **CAMeL Tools Docs:** https://camel-tools.readthedocs.io/
- **Arabic NLP Papers:** https://arxiv.org/search/?query=arabic+nlp

---

## 📝 Quick Reference Commands

### Daily Development

```bash
# Start everything (from project root)
docker-compose up -d  # Start DB and Redis

# Terminal 1: Start backend
cd backend && source venv/bin/activate && uvicorn app.main:app --reload

# Terminal 2: Start frontend (Week 5+)
cd frontend && npm run dev
```

### Testing

```bash
# Backend tests
cd backend
source venv/bin/activate
pytest tests/ -v

# Frontend tests (when added)
cd frontend
npm test
```

### Database Management

```bash
# Access PostgreSQL
docker exec -it bahr_postgres psql -U bahr -d bahr_dev

# Reset database (⚠️ destroys all data)
docker-compose down -v
docker-compose up -d

# Run migrations (after Alembic setup)
cd backend
alembic upgrade head
```

### Stopping Services

```bash
# Stop all
docker-compose down

# Stop and remove volumes (⚠️ destroys data)
docker-compose down -v
```

---

## 🚀 Ready to Build!

**Congratulations!** You've successfully set up the BAHR development environment.

**Remember:**
- ✅ Test M1/M2 compatibility on Day 1 (CRITICAL!)
- ✅ Execute Quick Wins in Week 1-2
- ✅ Use DEFERRED_FEATURES.md to prevent scope creep
- ✅ Allocate 2-3 hours/day for data annotation in Week 2
- ✅ Update docs/project-management/PROGRESS_LOG_CURRENT.md daily (5 minutes)
- ✅ Ask questions early and often
- ✅ Write tests for everything you build
- ✅ Have fun building سوق عكاظ الرقمي! 🎭

**Welcome to the team!** 🎉

---

**Document Maintained By:** Documentation Team
**Version:** 2.0 (Consolidated from 3 guides)
**Last Updated:** November 9, 2025
**Next Review:** December 1, 2025
**Feedback:** Create issue with label `docs-improvement`

---

## 📋 Consolidation Notes

This guide consolidates three previous documents:

1. **QUICK_START_GUIDE.md** (945 lines) - Complete 30-minute setup
2. **docs/START_HERE.md** (305 lines) - Critical updates summary (Arabic)
3. **docs/START_HERE_DEVELOPER.md** (568 lines) - Express 5-minute setup

**Changes Made:**
- ✅ Merged critical updates into top section
- ✅ Organized into two clear paths: Express (5-min) vs Complete (30-min)
- ✅ Preserved all technical content
- ✅ Maintained all warnings and troubleshooting
- ✅ Added cross-references to relevant documentation
- ✅ Standardized formatting and structure

**Archived Files:**
- Original files preserved in Git history
- Symlinks created for backward compatibility (optional)

**Version:** 2.0
**Consolidation Date:** November 9, 2025

---

## 📜 Document History

| Version | Date | Changes | Reason |
|---------|------|---------|--------|
| 2.1 | 2025-11-10 | Relocated to /docs/onboarding/, updated metadata | Documentation reorganization |
| 2.0 | 2025-11-09 | Consolidated 3 guides into single document | Reduce duplication |
| 1.0 | 2024-12-01 | Initial QUICK_START_GUIDE.md | Project setup |

