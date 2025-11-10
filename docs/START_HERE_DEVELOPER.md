# 🚀 Developer Quick Start Guide
## Get BAHR Running in 5 Minutes

---

**Last Updated:** November 8, 2025  
**Target Audience:** New developers joining the BAHR project  
**Prerequisites:** Basic command-line knowledge, Git installed  
**Estimated Time:** 5-10 minutes

---

## 📋 System Requirements

### Required Software:
- **Operating System:** macOS, Linux, or Windows (WSL2)
- **Python:** 3.11 or higher
- **Node.js:** 20.0 or higher (for frontend, Week 5+)
- **Git:** 2.30+
- **Docker:** 20.10+ (for PostgreSQL and Redis)

### Recommended Hardware:
- **RAM:** 8GB minimum (16GB recommended)
- **Storage:** 5GB free space
- **Network:** Stable internet for package downloads

### For Apple Silicon (M1/M2/M3) Users:
- Rosetta 2 installed (automatic on first native app run)
- Ensure Docker is running with Apple Silicon support

---

## ⚡ Quick Setup (Copy & Paste)

### Step 1: Clone Repository

```bash
# Clone the repository
git clone https://github.com/your-org/BAHR.git
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
pip install -r requirements.txt

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

If you see an error, check `docs/technical/NLP_INTEGRATION_GUIDE.md` for troubleshooting.

---

### Step 3: Start Database Services (Docker)

```bash
# Start PostgreSQL (Database)
docker run -d \
  --name bahr-postgres \
  -e POSTGRES_DB=bahr_dev \
  -e POSTGRES_USER=bahr \
  -e POSTGRES_PASSWORD=dev_password_123 \
  -p 5432:5432 \
  postgres:15-alpine

# Start Redis (Cache)
docker run -d \
  --name bahr-redis \
  -p 6379:6379 \
  redis:7-alpine

# Verify containers are running
docker ps
# Should show: bahr-postgres and bahr-redis both "Up"
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
# Copy example environment file
cp .env.example .env

# Edit .env with your settings (use nano, vim, or any editor)
nano .env

# Minimal configuration for local development:
# DATABASE_URL=postgresql://bahr:dev_password_123@localhost:5432/bahr_dev
# REDIS_URL=redis://localhost:6379/0
# SECRET_KEY=dev-secret-key-change-in-production
# LOG_LEVEL=DEBUG
```

**Quick .env generator (optional):**
```bash
cat > .env << 'EOF'
PROJECT_NAME=BAHR API
SECRET_KEY=dev-secret-key-$(openssl rand -hex 32)
DATABASE_URL=postgresql://bahr:dev_password_123@localhost:5432/bahr_dev
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

# Seed initial data (16 Arabic prosody meters)
python scripts/seed_meters.py

# Verify database is populated
psql postgresql://bahr:dev_password_123@localhost:5432/bahr_dev -c "SELECT COUNT(*) FROM meters;"
# Should return: count: 16
```

**Expected Output:**
```
INFO  [alembic.runtime.migration] Running upgrade  -> abc123, Initial schema
INFO  [alembic.runtime.migration] Running upgrade abc123 -> def456, Add meters table
✅ Database migrations complete

Seeding meters...
✅ Seeded 16 meters successfully
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

### Step 8 (Optional): Frontend Setup

**Note:** Frontend development starts in Week 5+. Skip this for now if you're focused on backend.

```bash
# Open new terminal
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Frontend should start on http://localhost:3000
```

---

## ✅ Success Checklist

After completing the setup, verify:

- [ ] Python virtual environment activated
- [ ] CAMeL Tools import successful (critical for M1/M2)
- [ ] PostgreSQL container running (port 5432)
- [ ] Redis container running (port 6379)
- [ ] Database migrations applied (16 meters seeded)
- [ ] Backend server running (http://localhost:8000)
- [ ] Health endpoint returns `{"status":"healthy"}`
- [ ] Swagger UI accessible (http://localhost:8000/docs)
- [ ] Test analysis request succeeds

**All checked?** 🎉 **You're ready to start developing!**

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

**Reference:** `docs/technical/NLP_INTEGRATION_GUIDE.md` Section 3.2

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
docker start bahr-postgres

# Verify connection manually
psql postgresql://bahr:dev_password_123@localhost:5432/bahr_dev -c "SELECT 1;"
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
docker start bahr-redis

# Test connection
redis-cli -h localhost -p 6379 PING
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
docker stop bahr-postgres
docker rm bahr-postgres
# Then repeat Step 3 and Step 5
```

---

## 📚 Next Steps

Now that your environment is set up:

### 1. **Understand the Architecture** (20 min)
Read: `docs/technical/ARCHITECTURE_OVERVIEW.md`

**Key Concepts:**
- Request flow (Client → FastAPI → Prosody Engine → Database)
- Interface contracts (ITextNormalizer, IMeterDetector, etc.)
- Caching strategy (Redis integration)
- Error handling (standardized envelopes)

---

### 2. **Explore the Prosody Engine** (30 min)
Read: `docs/technical/PROSODY_ENGINE.md`

**Key Topics:**
- Arabic text normalization (removing diacritics, unifying characters)
- Syllable segmentation (CV patterns)
- Meter detection algorithm (pattern matching)
- Confidence calibration

**Try modifying:**
```python
# backend/app/prosody/engine.py
# Add a new meter signature and test it
```

---

### 3. **Review Current Week's Tasks**
Read: `docs/planning/PROJECT_TIMELINE_DETAILED.md` (when created)

**For now:**
- Check Slack channel: `#bahr-dev`
- Review open GitHub issues
- Ask team lead for assignment

---

### 4. **Run Tests**

```bash
# Run unit tests
pytest tests/

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_normalizer.py -v
```

---

### 5. **Make Your First Contribution**

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

## 💬 Getting Help

### Internal Resources:
- **Slack Channels:**
  - `#bahr-dev` - General development questions
  - `#bahr-backend` - Backend-specific issues
  - `#bahr-nlp` - NLP and prosody questions

- **Documentation:**
  - `docs/technical/` - Technical specifications
  - `docs/planning/` - Project planning and timelines
  - `docs/workflows/` - Development workflows

- **Weekly Stand-ups:**
  - Monday 10 AM - Sprint planning
  - Friday 3 PM - Demo and retrospective

### External Resources:
- **Stack Overflow:** Tag questions with `fastapi`, `arabic-nlp`, or `poetry-analysis`
- **GitHub Issues:** Report bugs or request features
- **Email:** dev@bahr.app (for sensitive issues)

---

## 📝 Development Conventions

### Code Style:
```bash
# Format code with Black
black app/

# Lint with Ruff
ruff check app/

# Type check with mypy
mypy app/
```

### Commit Messages:
Follow [Conventional Commits](https://www.conventionalcommits.org/):
```
feat: add new meter detection algorithm
fix: resolve Unicode normalization bug
docs: update API specification
test: add integration tests for /analyze
refactor: simplify syllable segmentation logic
```

### Branch Naming:
```
feature/meter-confidence-calibration
bugfix/redis-connection-timeout
docs/update-deployment-guide
test/add-prosody-engine-tests
```

---

## 🎯 Your First Week Goals

### Day 1-2: Setup & Learning
- [ ] Complete this quick start guide
- [ ] Read Architecture Overview
- [ ] Understand Prosody Engine basics
- [ ] Run all tests successfully

### Day 3-4: First Contribution
- [ ] Pick a "good first issue" from GitHub
- [ ] Implement the change
- [ ] Write tests for your changes
- [ ] Create Pull Request

### Day 5: Integration
- [ ] Code review feedback addressed
- [ ] Merge your first PR 🎉
- [ ] Understand team workflow
- [ ] Plan next sprint tasks

---

## 🚀 You're Ready!

**Congratulations!** You've successfully set up the BAHR development environment.

**Remember:**
- ✅ Ask questions early and often (Slack #bahr-dev)
- ✅ Write tests for everything you build
- ✅ Document complex logic
- ✅ Keep PRs small and focused
- ✅ Have fun building سوق عكاظ الرقمي! 🎭

**Welcome to the team!** 🎉

---

**Document Maintained By:** DevOps Team  
**Last Tested:** November 8, 2025  
**Next Review:** December 1, 2025  
**Feedback:** Create issue with label `docs-improvement`
