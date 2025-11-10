# 🔧 Troubleshooting Guide
## Common Issues and Solutions for BAHR Development

**Last Updated:** November 9, 2025  
**Target Audience:** Developers setting up or running BAHR  
**Related:** `PHASE_0_SETUP.md`, `DEPLOYMENT_GUIDE.md`

---

## 📋 Quick Reference

| Issue | Quick Fix | Details |
|-------|-----------|---------|
| CAMeL Tools fails on M1/M2 | Try Rosetta 2 or Docker | [Section 1.1](#11-camel-tools-installation-fails) |
| Redis connection refused | Check Docker container | [Section 2.1](#21-redis-connection-error) |
| PostgreSQL auth failed | Verify credentials | [Section 2.2](#22-postgresql-authentication-failed) |
| Port already in use | Kill process or change port | [Section 3.1](#31-port-already-in-use) |
| Module import errors | Check virtual env | [Section 4.1](#41-python-import-errors) |

---

## 1. NLP Library Issues

### 1.1. CAMeL Tools Installation Fails

**Symptom:**
```bash
$ pip install camel-tools==1.5.2
ERROR: Failed building wheel for camel-tools
```

**Cause:** Architecture mismatch on Apple Silicon (M1/M2/M3 Macs)

**Solution 1: Try ARM64 Native (First)**
```bash
# Check your architecture
uname -m  # Should show "arm64"

# Create fresh virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Try ARM64 installation
arch -arm64 pip install camel-tools==1.5.2

# Test
python -c "from camel_tools.utils.normalize import normalize_unicode; print('✅ Success')"
```

**Solution 2: Use Rosetta 2 (If Solution 1 Fails)**
```bash
# Install Rosetta 2 (if not already)
softwareupdate --install-rosetta --agree-to-license

# Reinstall with x86_64 emulation
arch -x86_64 pip install camel-tools==1.5.2

# Test again
python -c "from camel_tools.morphology.database import MorphologyDB; print('✅ Works via Rosetta')"
```

**Solution 3: Docker with Platform Flag (Guaranteed)**
```bash
# Run in Docker with explicit platform
docker run --platform linux/amd64 \
  -v $(pwd):/app \
  python:3.11 \
  bash -c "pip install camel-tools==1.5.2 && python -c 'import camel_tools; print(camel_tools.__version__)'"
```

**Solution 4: Fallback to PyArabic Only**
```bash
# Disable CAMeL Tools in configuration
echo "NLP_ENABLE_MORPHOLOGY=false" >> .env

# Use PyArabic-only implementation
pip install pyarabic==0.6.15
```

**Reference:** `docs/phases/PHASE_0_SETUP.md` Section 4.5

---

### 1.2. PyArabic Import Errors

**Symptom:**
```python
ImportError: No module named 'pyarabic'
```

**Solution:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Install PyArabic
pip install pyarabic==0.6.15

# Verify
python -c "import pyarabic; print(pyarabic.__version__)"
```

---

### 1.3. Unicode Encoding Errors

**Symptom:**
```python
UnicodeDecodeError: 'ascii' codec can't decode byte 0xd8
```

**Solution:**
```bash
# Set environment variables for UTF-8
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
export PYTHONIOENCODING=utf-8

# Add to .bashrc or .zshrc for permanence
echo 'export PYTHONIOENCODING=utf-8' >> ~/.zshrc
```

---

## 2. Database & Cache Issues

### 2.1. Redis Connection Error

**Symptom:**
```python
redis.exceptions.ConnectionError: Error 61 connecting to localhost:6379. Connection refused.
```

**Diagnosis:**
```bash
# Check if Redis is running
docker ps | grep redis

# Check if port is listening
lsof -i :6379
```

**Solution 1: Start Redis via Docker**
```bash
# Start Redis container
docker run -d \
  --name bahr_redis \
  -p 6379:6379 \
  redis:7-alpine

# Verify
redis-cli ping  # Should return "PONG"
```

**Solution 2: Start via Docker Compose**
```bash
# Start only Redis
docker-compose up -d redis

# Check logs
docker-compose logs redis
```

**Solution 3: Local Redis Installation**
```bash
# Install via Homebrew (macOS)
brew install redis

# Start Redis service
brew services start redis

# Test connection
redis-cli ping
```

---

### 2.2. PostgreSQL Authentication Failed

**Symptom:**
```
psycopg2.OperationalError: FATAL:  password authentication failed for user "bahr"
```

**Solution 1: Check Credentials**
```bash
# Verify credentials in .env
cat .env | grep DATABASE_URL

# Should match docker-compose.yml
# DATABASE_URL=postgresql://bahr:bahr_dev_password@localhost:5432/bahr_dev
```

**Solution 2: Reset PostgreSQL Container**
```bash
# Stop and remove container
docker-compose down postgres
docker volume rm bahr_postgres_data

# Restart with fresh data
docker-compose up -d postgres

# Wait for health check
docker-compose ps postgres
```

**Solution 3: Manual Connection Test**
```bash
# Test connection directly
psql -h localhost -p 5432 -U bahr -d bahr_dev

# If successful, issue is in connection string format
```

---

### 2.3. Database Migration Errors

**Symptom:**
```bash
$ alembic upgrade head
ERROR: relation "users" already exists
```

**Solution:**
```bash
# Check current migration state
alembic current

# If mismatched, stamp the database
alembic stamp head

# Or reset migrations completely
docker-compose down postgres
docker volume rm bahr_postgres_data
docker-compose up -d postgres
alembic upgrade head
```

---

## 3. Server & Port Issues

### 3.1. Port Already in Use

**Symptom:**
```
OSError: [Errno 48] Address already in use
```

**Diagnosis:**
```bash
# Find process using port 8000
lsof -i :8000

# Example output:
# COMMAND   PID   USER
# Python  12345   user
```

**Solution 1: Kill Existing Process**
```bash
# Kill by PID
kill -9 12345

# Or kill by port
lsof -ti:8000 | xargs kill -9
```

**Solution 2: Use Different Port**
```bash
# Run on port 8001 instead
uvicorn app.main:app --host 0.0.0.0 --port 8001

# Or set in environment
export PORT=8001
```

---

### 3.2. Docker Container Fails to Start

**Symptom:**
```bash
$ docker-compose up
ERROR: for bahr_api  Container "xxxx" is unhealthy
```

**Diagnosis:**
```bash
# Check container logs
docker-compose logs api

# Check health status
docker inspect bahr_api | grep -A 10 Health
```

**Solution:**
```bash
# Rebuild container
docker-compose build api

# Start with fresh state
docker-compose down
docker-compose up -d

# View logs in real-time
docker-compose logs -f api
```

---

## 4. Python Environment Issues

### 4.1. Python Import Errors

**Symptom:**
```python
ModuleNotFoundError: No module named 'fastapi'
```

**Solution:**
```bash
# Verify virtual environment is activated
which python  # Should show path in venv/

# If not activated
source venv/bin/activate  # Unix/macOS
# or
.\venv\Scripts\activate   # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

---

### 4.2. pip SSL Certificate Errors

**Symptom:**
```bash
$ pip install fastapi
SSL: CERTIFICATE_VERIFY_FAILED
```

**Solution:**
```bash
# Option 1: Update certificates (macOS)
/Applications/Python\ 3.11/Install\ Certificates.command

# Option 2: Use pip with trusted host (temporary)
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org fastapi

# Option 3: Update pip
python -m pip install --upgrade pip
```

---

### 4.3. Version Conflicts

**Symptom:**
```bash
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed.
```

**Solution:**
```bash
# Create clean virtual environment
deactivate
rm -rf venv
python3.11 -m venv venv
source venv/bin/activate

# Install from scratch
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 5. Frontend Issues (Next.js)

### 5.1. npm Install Fails

**Symptom:**
```bash
$ npm install
npm ERR! code ERESOLVE
```

**Solution:**
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and lockfile
rm -rf node_modules package-lock.json

# Reinstall
npm install

# Or use legacy peer deps
npm install --legacy-peer-deps
```

---

### 5.2. RTL CSS Issues

**Symptom:**
Arabic text displays left-to-right instead of right-to-left.

**Solution:**
```javascript
// Add to _app.tsx or layout
<html dir="rtl" lang="ar">
  <body className="font-arabic">
    {children}
  </body>
</html>

// Ensure Tailwind RTL plugin is installed
npm install tailwindcss-rtl
```

---

## 6. Development Workflow Issues

### 6.1. Hot Reload Not Working

**Symptom:**
Code changes don't trigger automatic reload.

**Solution:**
```bash
# Ensure --reload flag is set
uvicorn app.main:app --reload

# For Docker, ensure volume is mounted
# Check docker-compose.yml:
volumes:
  - ./backend/app:/app/app:ro
```

---

### 6.2. Tests Failing in CI but Pass Locally

**Symptom:**
```bash
$ pytest
✅ All tests pass (local)

# In GitHub Actions:
❌ FAILED tests/test_analysis.py
```

**Solution:**
```bash
# Check for environment-specific issues
# 1. Verify Python version matches CI
python --version

# 2. Run tests in clean environment
docker run --rm -v $(pwd):/app python:3.11 bash -c "cd /app && pip install -r requirements.txt && pytest"

# 3. Check for timing issues
pytest --log-cli-level=DEBUG

# 4. Ensure test database is isolated
export DATABASE_URL=postgresql://test:test@localhost/test_db
```

---

## 7. Performance Issues

### 7.1. Slow Analysis Response

**Symptom:**
Analysis endpoint takes > 2 seconds to respond.

**Diagnosis:**
```python
# Add timing logs
import time

start = time.perf_counter()
# ... analysis code ...
elapsed = time.perf_counter() - start
print(f"Analysis took {elapsed:.3f}s")
```

**Solution:**
```python
# 1. Enable caching
CACHE_TTL_ANALYSIS=3600

# 2. Use fast analysis mode
{"text": "...", "options": {"analysis_mode": "fast"}}

# 3. Check database query performance
EXPLAIN ANALYZE SELECT * FROM analyses WHERE ...;

# 4. Monitor with Prometheus metrics
http://localhost:9090/graph?g0.expr=verse_analysis_latency_seconds
```

---

### 7.2. High Memory Usage

**Symptom:**
```bash
$ docker stats
CONTAINER    MEM USAGE
bahr_api     2.5GiB / 4GiB
```

**Solution:**
```bash
# 1. Check for memory leaks
# Install memory profiler
pip install memory-profiler

# Profile endpoint
@profile
def analyze_verse(text: str):
    ...

# 2. Limit CAMeL Tools database cache
export CAMEL_TOOLS_CACHE_SIZE=100

# 3. Set Docker memory limits
docker run -m 512m bahr_api
```

---

## 8. Security Issues

### 8.1. JWT Token Invalid

**Symptom:**
```json
{
  "error": {
    "code": "ERR_AUTH_002",
    "message": "Invalid token"
  }
}
```

**Solution:**
```bash
# 1. Check SECRET_KEY hasn't changed
cat .env | grep SECRET_KEY

# 2. Verify token hasn't expired
# Decode JWT at https://jwt.io

# 3. Check token format
curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:8000/api/v1/auth/me
```

---

### 8.2. CORS Errors in Browser

**Symptom:**
```
Access to fetch at 'http://localhost:8000' from origin 'http://localhost:3000' has been blocked by CORS policy
```

**Solution:**
```python
# Add to main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 9. Monitoring & Logging Issues

### 9.1. Prometheus Metrics Not Showing

**Symptom:**
Grafana dashboard shows "No Data"

**Solution:**
```bash
# 1. Check Prometheus is scraping
curl http://localhost:9090/api/v1/targets

# 2. Verify metrics endpoint works
curl http://localhost:8000/metrics

# 3. Check Prometheus config
docker exec bahr_prometheus cat /etc/prometheus/prometheus.yml

# 4. Restart Prometheus
docker-compose restart prometheus
```

---

### 9.2. Logs Not Structured

**Symptom:**
Logs are unreadable or missing fields

**Solution:**
```python
# Use structured logging
import logging
import json

class JSONFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps({
            'timestamp': self.formatTime(record),
            'level': record.levelname,
            'message': record.getMessage(),
            'module': record.module,
            'request_id': getattr(record, 'request_id', None)
        })

handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)
```

---

## 10. Common Configuration Mistakes

### 10.1. Missing Environment Variables

**Symptom:**
```
RuntimeError: Missing required environment variable: SECRET_KEY
```

**Solution:**
```bash
# Copy example file
cp .env.example .env

# Verify all required vars are set
grep "required=True" backend/app/config.py

# Check current env
env | grep BAHR
```

---

### 10.2. Wrong Python Version

**Symptom:**
```bash
SyntaxError: invalid syntax (match statement)
```

**Solution:**
```bash
# Check version
python --version  # Must be 3.11+

# Use specific version
python3.11 -m venv venv
source venv/bin/activate
```

---

## 📞 Getting Help

If you've tried these solutions and still have issues:

1. **Check Documentation:**
   - `docs/phases/PHASE_0_SETUP.md` - Setup guide
   - `docs/technical/DEPLOYMENT_GUIDE.md` - Deployment
   - `docs/workflows/DEVELOPMENT_WORKFLOW.md` - Dev workflow

2. **Search Issues:**
   - GitHub Issues: `https://github.com/your-org/BAHR/issues`
   - Stack Overflow: Tag `[bahr] [arabic-nlp]`

3. **Ask for Help:**
   - Create detailed issue with:
     - OS and version
     - Python version
     - Full error message
     - Steps to reproduce
     - What you've tried

4. **Common Resources:**
   - FastAPI Docs: https://fastapi.tiangolo.com
   - CAMeL Tools: https://github.com/CAMeL-Lab/camel_tools
   - Docker Docs: https://docs.docker.com

---

## 🔍 Debug Checklist

Before asking for help, verify:

- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip list`)
- [ ] Environment variables set (`.env` file)
- [ ] Docker containers running (`docker ps`)
- [ ] Ports not in use (`lsof -i :8000`)
- [ ] Database accessible (`psql` or `pgcli`)
- [ ] Redis accessible (`redis-cli ping`)
- [ ] Python version correct (`python --version`)
- [ ] Git branch up to date (`git pull`)
- [ ] Logs checked (`docker-compose logs`)

---

**Last Updated:** November 9, 2025  
**Contributors:** Core team  
**Feedback:** Create issue or PR with additional troubleshooting tips
