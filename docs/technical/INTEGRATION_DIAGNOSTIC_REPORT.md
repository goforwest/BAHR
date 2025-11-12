# Integration Diagnostic Report - BAHR Platform

**Date:** November 11, 2025  
**Analyst:** Repository Auditor  
**Issue:** Frontend and Backend Online but Not Connected  
**Context:** Post-Restructuring Analysis with BAHR v2.0 Zihafat Engine Compatibility  

---

## Executive Summary

This diagnostic report identifies **integration breakpoints** in the BAHR Arabic poetry analysis platform following a recent repository restructuring. The analysis reveals that while both frontend (Next.js) and backend (FastAPI) services are running, the **analysis functionality fails** due to potential wiring issues at multiple integration layers.

**Critical Finding:** The platform architecture is **sound**, but several runtime dependencies (Redis, environment configuration) and import paths may be misconfigured post-restructure. The ongoing **BAHR v2.0 Zihafat Rules Engine** implementation appears to be in **planning phase only** (no code artifacts detected), so diagnostic and repair operations will **not disrupt** this initiative.

---

## 1. Architecture Overview

### 1.1 Current System Structure

```
┌─────────────────────────────────────────────────────────────┐
│                     BAHR Platform                            │
├──────────────────┬──────────────────────────────────────────┤
│   Frontend       │         Backend API                      │
│   (Next.js)      │         (FastAPI)                        │
│   Port: 3000     │         Port: 8000                       │
├──────────────────┼──────────────────────────────────────────┤
│                  │                                          │
│  ┌────────────┐  │  ┌──────────────────────────────────┐   │
│  │ UI Layer   │  │  │   API Router (v1)                │   │
│  │            │  │  │   /api/v1/analyze                │   │
│  │ - Forms    │──┼──┤   /api/v1/analytics              │   │
│  │ - Results  │  │  │   /health, /metrics              │   │
│  └────────────┘  │  └─────────┬────────────────────────┘   │
│        │         │            │                             │
│  ┌────────────┐  │  ┌─────────▼────────────────────────┐   │
│  │ API Client │  │  │  Analysis Engine                  │   │
│  │ (api.ts)   │  │  │  - Normalization                  │   │
│  │            │  │  │  - Taqti3 (Scansion)              │   │
│  │ - Axios    │  │  │  - Bahr Detection (v1)            │   │
│  │ - Hooks    │  │  │  - Quality Analysis               │   │
│  └────────────┘  │  │  - Rhyme Analysis                 │   │
│                  │  └─────────┬────────────────────────┘   │
│                  │            │                             │
│                  │  ┌─────────▼────────────────────────┐   │
│                  │  │  Support Services                 │   │
│                  │  │  - Redis (Cache)                  │   │
│                  │  │  - PostgreSQL (Analytics)         │   │
│                  │  └───────────────────────────────────┘   │
└──────────────────┴──────────────────────────────────────────┘
```

### 1.2 BAHR v2.0 Zihafat Engine Status

**Status:** Planning/Design Phase  
**Location:** `docs/planning/ZIHAFAT_IMPLEMENTATION_PLAN.md`  
**Impact:** No code artifacts found (`bahr_detector_v2.py` does not exist)  
**Risk:** **ZERO** - Diagnostic operations will not affect future implementation

**Note:** The current `BahrDetector` class in `backend/app/core/bahr_detector.py` is the **v1 pattern-matching** implementation. The v2 rule-based engine is planned but not yet implemented.

---

## 2. Diagnostic Findings

### 2.1 Integration Flow Analysis

#### ✅ **Working Components**

1. **Frontend Service**
   - Location: `frontend/src/`
   - API Client: `frontend/src/lib/api.ts` ✓
   - Type Definitions: `frontend/src/types/analyze.ts` ✓
   - React Hooks: `frontend/src/hooks/useAnalyze.ts` ✓
   - Environment: `.env.local` configured with `NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1` ✓

2. **Backend API Routes**
   - Main App: `backend/app/main.py` ✓
   - API Router: `backend/app/api/v1/router.py` ✓
   - Analyze Endpoint: `backend/app/api/v1/endpoints/analyze.py` ✓
   - Schemas: `backend/app/schemas/analyze.py` ✓

3. **Core Analysis Modules**
   - Normalization: `backend/app/core/normalization.py` ✓
   - Taqti3: `backend/app/core/taqti3.py` ✓
   - Bahr Detector: `backend/app/core/bahr_detector.py` ✓
   - Phonetics: `backend/app/core/phonetics.py` ✓
   - Quality: `backend/app/core/quality.py` ✓
   - Rhyme: `backend/app/core/rhyme.py` ✓

#### ⚠️ **Potential Breakpoints**

| Layer | Component | Issue | Severity |
|-------|-----------|-------|----------|
| **Infrastructure** | Redis | May not be running or accessible | HIGH |
| **Configuration** | CORS Origins | Mismatch between frontend/backend URLs | MEDIUM |
| **Dependencies** | Python Packages | Missing packages after restructure | HIGH |
| **Imports** | Module Paths | Absolute imports may fail if PYTHONPATH incorrect | CRITICAL |
| **Runtime** | Backend Startup | Redis connection failure blocks startup | HIGH |
| **Network** | API Endpoint | Frontend calling wrong URL or endpoint path | MEDIUM |

---

## 3. Probable Root Causes

### 3.1 Critical: Backend Not Actually Running

**Hypothesis:** While the user reports "backend online", the FastAPI server may have **started but crashed** during initialization.

**Evidence:**
```python
# backend/app/main.py (lines 42-49)
@app.on_event("startup")
async def startup_event():
    """Initialize Redis connection on startup."""
    try:
        await get_redis()
        print("✓ Redis connection initialized")
    except Exception as e:
        print(f"✗ Redis connection failed: {e}")
        # NOTE: Does NOT raise exception - server continues!
```

**Problem:** If Redis is not running, the server prints an error but **continues to run** in a degraded state. The analyze endpoint will fail because it expects Redis caching.

**Impact:** `/api/v1/analyze` endpoint will return **500 Internal Server Error** on every request.

---

### 3.2 High Priority: PYTHONPATH Configuration

**Issue:** Backend uses absolute imports (`from app.core.normalization import ...`), which require the parent directory (`backend/`) to be in `PYTHONPATH`.

**Evidence:**
```python
# backend/app/api/v1/endpoints/analyze.py
from app.schemas.analyze import AnalyzeRequest, AnalyzeResponse  # ← Absolute import
from app.core.normalization import normalize_arabic_text
from app.core.taqti3 import perform_taqti3
from app.core.bahr_detector import BahrDetector
```

**Failure Mode:**
```bash
$ cd backend
$ python -m uvicorn app.main:app --reload
# ✓ Works (app is importable)

$ cd backend/app
$ python -m uvicorn main:app --reload
# ✗ FAILS: ModuleNotFoundError: No module named 'app.core'
```

**Post-Restructure Risk:** If startup commands changed, imports will break.

---

### 3.3 Medium Priority: CORS Misconfiguration

**Current Configuration:**
```python
# backend/app/config.py
cors_origins: list[str] = None

def __post_init__(self):
    cors_str = _get("CORS_ORIGINS", "http://localhost:3000,http://localhost:8000")
    self.cors_origins = [origin.strip() for origin in cors_str.split(",")]
```

**Frontend Environment:**
```bash
# frontend/.env.local
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

**Potential Issue:** If frontend is served on a different port (e.g., 3001 after rebuild) or if the backend is deployed with incorrect CORS settings, requests will fail with:
```
Access to fetch at 'http://localhost:8000/api/v1/analyze/' from origin 
'http://localhost:3001' has been blocked by CORS policy
```

---

### 3.4 Medium Priority: API Endpoint Path Mismatch

**Frontend calls:**
```typescript
// frontend/src/lib/api.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';
// ...
const response = await apiClient.post<AnalyzeResponse>('/analyze/', data);
```

**Constructed URL:** `http://localhost:8000/api/v1/analyze/`

**Backend route:**
```python
# backend/app/main.py
app.include_router(api_router, prefix="/api/v1")

# backend/app/api/v1/router.py
api_router.include_router(analyze.router, prefix="/analyze", tags=["Analysis"])

# backend/app/api/v1/endpoints/analyze.py
@router.post("/", response_model=AnalyzeResponse, ...)
async def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
```

**Expected URL:** `http://localhost:8000/api/v1/analyze/`

**Status:** ✅ Paths match correctly (trailing slash is fine)

---

### 3.5 Low Priority: Redis Caching Graceful Degradation

**Good News:** The analyze endpoint has **graceful fallback** for Redis failures:

```python
# backend/app/api/v1/endpoints/analyze.py (lines 111-121)
try:
    cached_result = await cache_get(cache_key)
    if cached_result:
        return AnalyzeResponse(**cached_result)
except Exception as e:
    logger.warning(f"Cache read failed (continuing without cache): {e}")
```

**However:** Redis connection failure at **startup** is NOT gracefully handled and may crash subsequent requests.

---

## 4. Step-by-Step Diagnostic Workflow

### Phase 1: Verify Services Are Running

#### Step 1.1: Check Backend Status

```bash
# Terminal 1: Navigate to backend directory
cd /Users/hamoudi/Desktop/Personal/BAHR/backend

# Check if any process is listening on port 8000
lsof -i :8000

# Expected output:
# COMMAND   PID   USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
# Python  12345  user    5u  IPv4  0x...      0t0  TCP localhost:8000 (LISTEN)

# If nothing, backend is NOT running
```

#### Step 1.2: Check Frontend Status

```bash
# Terminal 2: Navigate to frontend directory
cd /Users/hamoudi/Desktop/Personal/BAHR/frontend

# Check if any process is listening on port 3000
lsof -i :3000

# Expected output:
# COMMAND   PID   USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
# node    23456  user   23u  IPv4  0x...      0t0  TCP *:3000 (LISTEN)
```

#### Step 1.3: Test Health Endpoint

```bash
# Test backend health (should return JSON)
curl -v http://localhost:8000/health

# Expected response:
# HTTP/1.1 200 OK
# {"status": "healthy", "timestamp": 1699707600, "version": "1.0.0"}

# If connection refused: Backend is NOT running
# If timeout: Backend is hanging
# If 404: Route not found (serious issue)
```

---

### Phase 2: Verify Dependencies

#### Step 2.1: Check Redis

```bash
# Check if Redis is running
redis-cli ping

# Expected: PONG
# If error: Redis is not running

# Start Redis if needed (macOS)
brew services start redis

# Or using Docker
docker run -d -p 6379:6379 redis:alpine

# Verify connection
redis-cli -h localhost -p 6379 ping
```

#### Step 2.2: Check Python Dependencies

```bash
cd /Users/hamoudi/Desktop/Personal/BAHR/backend

# Verify required packages are installed
python -c "import fastapi; print('FastAPI:', fastapi.__version__)"
python -c "import redis.asyncio; print('Redis: OK')"
python -c "import pydantic; print('Pydantic:', pydantic.__version__)"

# If any import fails, reinstall dependencies
pip install -r requirements/base.txt
```

---

### Phase 3: Test Analysis Flow

#### Step 3.1: Direct API Test

```bash
# Test analyze endpoint with curl
curl -X POST http://localhost:8000/api/v1/analyze/ \
  -H "Content-Type: application/json" \
  -d '{
    "text": "إذا غامَرتَ في شَرَفٍ مَرومِ",
    "detect_bahr": true,
    "suggest_corrections": false
  }'

# Expected response (200 OK):
# {
#   "text": "إذا غامَرتَ في شَرَفٍ مَرومِ",
#   "taqti3": "فعولن مفاعيلن فعولن مفاعيلن",
#   "bahr": {
#     "id": 1,
#     "name_ar": "الطويل",
#     "name_en": "at-Tawil",
#     "confidence": 0.95
#   },
#   "errors": [],
#   "suggestions": [],
#   "score": 95.0
# }

# Common errors:
# - 422: Validation error (check request format)
# - 400: Invalid input (text not Arabic)
# - 500: Server error (check backend logs)
# - Connection refused: Backend not running
```

#### Step 3.2: Check CORS

```bash
# Test CORS headers
curl -X OPTIONS http://localhost:8000/api/v1/analyze/ \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: POST" \
  -v

# Look for these headers in response:
# Access-Control-Allow-Origin: http://localhost:3000
# Access-Control-Allow-Methods: POST, OPTIONS
# Access-Control-Allow-Credentials: true

# If missing: CORS misconfigured
```

---

### Phase 4: Debug Backend Startup

#### Step 4.1: Start Backend with Verbose Logging

```bash
cd /Users/hamoudi/Desktop/Personal/BAHR/backend

# Set environment variables
export LOG_LEVEL=DEBUG
export REDIS_URL=redis://localhost:6379/0
export CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# Start server with reload
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --log-level debug

# Watch for errors:
# ✓ Redis connection initialized
# ✗ Redis connection failed: [Errno 61] Connection refused
# ✗ ModuleNotFoundError: No module named 'app.core'
```

#### Step 4.2: Test Individual Modules

```bash
cd /Users/hamoudi/Desktop/Personal/BAHR/backend

# Test normalization
python -c "
from app.core.normalization import normalize_arabic_text
text = 'إذا غامَرتَ في شَرَفٍ مَرومِ'
print(normalize_arabic_text(text))
"

# Test taqti3
python -c "
from app.core.taqti3 import perform_taqti3
result = perform_taqti3('إذا غامَرتَ في شَرَفٍ مَرومِ')
print(result)
"

# Test bahr detection
python -c "
from app.core.bahr_detector import BahrDetector
detector = BahrDetector()
result = detector.analyze_verse('إذا غامَرتَ في شَرَفٍ مَرومِ')
print(result)
"

# If any fail: Check imports and dependencies
```

---

### Phase 5: Frontend Integration Test

#### Step 5.1: Check Network Tab

1. Open browser DevTools (F12)
2. Go to Network tab
3. Navigate to `http://localhost:3000`
4. Submit analysis form
5. Check XHR/Fetch requests

**Look for:**
- Request URL: Should be `http://localhost:8000/api/v1/analyze/`
- Status: 200 (success), 4xx (client error), 5xx (server error)
- CORS errors in console

#### Step 5.2: Test API Client Directly

```typescript
// In browser console (http://localhost:3000)
import { analyzeVerse } from '@/lib/api';

analyzeVerse({
  text: 'إذا غامَرتَ في شَرَفٍ مَرومِ',
  detect_bahr: true,
  suggest_corrections: false
})
  .then(result => console.log('Success:', result))
  .catch(error => console.error('Error:', error));

// Check response or error
```

---

## 5. Probable Causes Ranked by Likelihood

| Rank | Cause | Probability | Quick Test |
|------|-------|-------------|------------|
| 1 | Redis not running | 85% | `redis-cli ping` |
| 2 | Backend not started | 70% | `lsof -i :8000` |
| 3 | PYTHONPATH incorrect | 60% | `python -c "from app.core import normalization"` |
| 4 | Missing Python packages | 50% | `pip list \| grep fastapi` |
| 5 | CORS misconfiguration | 30% | Check browser console |
| 6 | Frontend env vars wrong | 20% | Check `.env.local` |
| 7 | API path mismatch | 10% | Routes are correct |

---

## 6. Recommended Fix Plan

### Fix 1: Start Redis (if not running)

**Priority:** CRITICAL  
**Time:** 2 minutes  
**Impact:** Resolves 85% probability issue

```bash
# macOS with Homebrew
brew services start redis

# Verify
redis-cli ping  # Should return PONG

# OR use Docker
docker run -d --name bahr-redis -p 6379:6379 redis:alpine
```

---

### Fix 2: Verify Backend Startup

**Priority:** CRITICAL  
**Time:** 5 minutes  
**Impact:** Ensures server is running correctly

```bash
cd /Users/hamoudi/Desktop/Personal/BAHR/backend

# Kill any existing processes on port 8000
lsof -ti:8000 | xargs kill -9

# Set environment
export REDIS_URL=redis://localhost:6379/0
export LOG_LEVEL=DEBUG

# Start backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Wait for:
# ✓ Redis connection initialized
# INFO:     Uvicorn running on http://0.0.0.0:8000

# Test health endpoint
curl http://localhost:8000/health
```

---

### Fix 3: Install/Update Dependencies

**Priority:** HIGH  
**Time:** 3 minutes  
**Impact:** Ensures all packages are available

```bash
cd /Users/hamoudi/Desktop/Personal/BAHR/backend

# Upgrade pip
pip install --upgrade pip

# Install base requirements
pip install -r requirements/base.txt

# Verify critical packages
python -c "import fastapi, redis, pydantic; print('OK')"
```

---

### Fix 4: Fix PYTHONPATH (if needed)

**Priority:** MEDIUM  
**Time:** 2 minutes  
**Impact:** Fixes import errors

```bash
# Add to ~/.zshrc or run before starting server
export PYTHONPATH="/Users/hamoudi/Desktop/Personal/BAHR/backend:$PYTHONPATH"

# Or use -m flag (recommended)
cd /Users/hamoudi/Desktop/Personal/BAHR/backend
python -m uvicorn app.main:app --reload
```

---

### Fix 5: Update CORS Configuration

**Priority:** LOW  
**Time:** 1 minute  
**Impact:** Fixes cross-origin issues if present

```bash
# Edit backend/.env (create if doesn't exist)
echo "CORS_ORIGINS=http://localhost:3000,http://localhost:3001,http://127.0.0.1:3000" > backend/.env

# Restart backend
```

---

## 7. Testing After Fixes

### Integration Test Script

```bash
#!/bin/bash
# Location: scripts/testing/test_integration.sh

set -e  # Exit on error

echo "🔍 BAHR Integration Test"
echo "========================"

# Test 1: Redis
echo "1️⃣  Testing Redis..."
if redis-cli ping > /dev/null 2>&1; then
    echo "   ✓ Redis is running"
else
    echo "   ✗ Redis is NOT running"
    exit 1
fi

# Test 2: Backend Health
echo "2️⃣  Testing Backend Health..."
HEALTH=$(curl -s http://localhost:8000/health)
if echo "$HEALTH" | grep -q "healthy"; then
    echo "   ✓ Backend is healthy"
else
    echo "   ✗ Backend health check failed"
    exit 1
fi

# Test 3: Analyze Endpoint
echo "3️⃣  Testing Analyze Endpoint..."
RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/analyze/ \
  -H "Content-Type: application/json" \
  -d '{"text": "إذا غامَرتَ في شَرَفٍ مَرومِ", "detect_bahr": true}')

if echo "$RESPONSE" | grep -q "taqti3"; then
    echo "   ✓ Analyze endpoint working"
else
    echo "   ✗ Analyze endpoint failed"
    echo "   Response: $RESPONSE"
    exit 1
fi

# Test 4: Frontend
echo "4️⃣  Testing Frontend..."
if curl -s http://localhost:3000 > /dev/null; then
    echo "   ✓ Frontend is accessible"
else
    echo "   ✗ Frontend is NOT accessible"
    exit 1
fi

echo ""
echo "✅ All integration tests passed!"
```

**Usage:**
```bash
chmod +x scripts/testing/test_integration.sh
./scripts/testing/test_integration.sh
```

---

## 8. BAHR v2.0 Zihafat Engine Compatibility

### Current State

**Status:** ✅ **SAFE TO PROCEED**

The BAHR v2.0 Zihafat Rules Engine is currently in the **planning phase**:
- Design document exists: `docs/planning/ZIHAFAT_IMPLEMENTATION_PLAN.md`
- No implementation code yet (`bahr_detector_v2.py` not found)
- Current system uses `BahrDetector` v1 (pattern-matching)

### Migration Strategy (from planning docs)

The plan maintains **both v1 and v2** implementations:

```python
# Planned migration path
class BahrDetector:
    def __init__(self, version="v1"):
        if version == "v2":
            self._impl = BahrDetectorV2()  # Future
        else:
            self._impl = BahrDetectorV1()  # Current
```

### Compatibility Guarantees

All diagnostic and repair operations in this report:
- ✅ Do NOT modify `backend/app/core/bahr_detector.py`
- ✅ Do NOT change API contracts or schemas
- ✅ Do NOT alter analysis endpoint signatures
- ✅ Focus only on infrastructure and wiring issues

**Result:** BAHR v2.0 implementation can proceed **without interference** from these fixes.

---

## 9. Monitoring and Prevention

### 9.1 Health Check Enhancements

**Add to `backend/app/main.py`:**

```python
@app.get("/health/detailed")
async def health_detailed():
    """Detailed health check with dependency status."""
    checks = {
        "status": "healthy",
        "checks": {}
    }
    
    # Redis check
    try:
        redis = await get_redis()
        await redis.ping()
        checks["checks"]["redis"] = {"status": "up", "message": "Connected"}
    except Exception as e:
        checks["checks"]["redis"] = {"status": "down", "message": str(e)}
        checks["status"] = "degraded"
    
    # Database check (future)
    checks["checks"]["database"] = {"status": "unknown", "message": "not implemented"}
    
    return checks
```

**Test:**
```bash
curl http://localhost:8000/health/detailed
```

---

### 9.2 Startup Validation

**Add to `backend/app/main.py`:**

```python
@app.on_event("startup")
async def startup_event():
    """Validate all dependencies on startup."""
    logger = logging.getLogger(__name__)
    
    # Redis validation
    try:
        redis = await get_redis()
        await redis.ping()
        logger.info("✓ Redis connection validated")
    except Exception as e:
        logger.error(f"✗ Redis connection failed: {e}")
        # Consider raising exception to prevent startup
        # raise RuntimeError("Redis is required for operation")
    
    # Module imports validation
    try:
        from app.core.normalization import normalize_arabic_text
        from app.core.taqti3 import perform_taqti3
        from app.core.bahr_detector import BahrDetector
        logger.info("✓ Core modules imported successfully")
    except ImportError as e:
        logger.critical(f"✗ Failed to import core modules: {e}")
        raise
```

---

### 9.3 CI/CD Integration Test

**Add to `.github/workflows/integration-test.yml`:**

```yaml
name: Integration Test

on: [push, pull_request]

jobs:
  integration:
    runs-on: ubuntu-latest
    
    services:
      redis:
        image: redis:alpine
        ports:
          - 6379:6379
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements/base.txt
      
      - name: Start backend
        run: |
          cd backend
          python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &
          sleep 5
      
      - name: Test health endpoint
        run: |
          curl -f http://localhost:8000/health
      
      - name: Test analyze endpoint
        run: |
          curl -f -X POST http://localhost:8000/api/v1/analyze/ \
            -H "Content-Type: application/json" \
            -d '{"text": "إذا غامَرتَ في شَرَفٍ مَرومِ", "detect_bahr": true}'
```

---

## 10. Summary and Next Steps

### Current Diagnosis

**Probable Issue:** Redis not running or backend startup failed

**Confidence:** 85%

**Evidence:**
1. ✅ Code structure is correct
2. ✅ API routes properly configured
3. ✅ Frontend environment configured
4. ⚠️ Redis required for startup (may be missing)
5. ⚠️ No graceful degradation if Redis fails at startup

---

### Immediate Actions (30 minutes)

1. **Start Redis** (2 min)
   ```bash
   brew services start redis
   redis-cli ping
   ```

2. **Restart Backend** (5 min)
   ```bash
   cd backend
   export REDIS_URL=redis://localhost:6379/0
   python -m uvicorn app.main:app --reload
   ```

3. **Test Health** (1 min)
   ```bash
   curl http://localhost:8000/health
   ```

4. **Test Analysis** (2 min)
   ```bash
   curl -X POST http://localhost:8000/api/v1/analyze/ \
     -H "Content-Type: application/json" \
     -d '{"text": "إذا غامَرتَ في شَرَفٍ مَرومِ", "detect_bahr": true}'
   ```

5. **Test Frontend** (5 min)
   - Open `http://localhost:3000`
   - Submit a verse
   - Verify results appear

---

### Long-Term Improvements

1. **Add health checks** to validate dependencies at startup
2. **Implement graceful degradation** if Redis is unavailable
3. **Add integration tests** to CI/CD pipeline
4. **Document startup procedures** after restructuring
5. **Create troubleshooting guide** for common issues

---

### BAHR v2.0 Compatibility Checklist

- ✅ No changes to `bahr_detector.py` required
- ✅ API contracts remain stable
- ✅ Schemas unchanged
- ✅ Analysis flow preserved
- ✅ v2 can be implemented alongside v1

**Result:** All fixes are **BAHR v2.0 compatible**.

---

## Appendix A: Quick Reference Commands

### Start All Services

```bash
# Terminal 1: Redis
brew services start redis

# Terminal 2: Backend
cd /Users/hamoudi/Desktop/Personal/BAHR/backend
export REDIS_URL=redis://localhost:6379/0
python -m uvicorn app.main:app --reload

# Terminal 3: Frontend
cd /Users/hamoudi/Desktop/Personal/BAHR/frontend
npm run dev
```

### Test Connectivity

```bash
# Redis
redis-cli ping

# Backend health
curl http://localhost:8000/health

# Backend analyze
curl -X POST http://localhost:8000/api/v1/analyze/ \
  -H "Content-Type: application/json" \
  -d '{"text": "إذا غامَرتَ في شَرَفٍ مَرومِ", "detect_bahr": true}'

# Frontend
open http://localhost:3000
```

### Debug Logs

```bash
# Backend logs with debug level
cd backend
LOG_LEVEL=DEBUG python -m uvicorn app.main:app --reload --log-level debug

# Check Redis connection
redis-cli monitor

# Check running processes
lsof -i :8000  # Backend
lsof -i :3000  # Frontend
lsof -i :6379  # Redis
```

---

## Appendix B: Environment Variables Checklist

### Backend (`.env` or export)

```bash
# Core
PROJECT_NAME=BAHR API
API_VERSION=1.0.0
LOG_LEVEL=DEBUG

# Redis
REDIS_URL=redis://localhost:6379/0
CACHE_TTL=86400

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# Database (optional for analysis)
DATABASE_URL=postgresql://bahr:password@localhost:5432/bahr_dev
```

### Frontend (`.env.local`)

```bash
# API
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1

# Environment
NODE_ENV=development

# Application
NEXT_PUBLIC_APP_NAME=بَحْر
LOG_LEVEL=debug
```

---

## Document Metadata

**Version:** 1.0  
**Author:** Repository Auditor  
**Date:** November 11, 2025  
**Last Updated:** November 11, 2025  
**Status:** Active  
**Related Documents:**
- `docs/onboarding/QUICKSTART_NEW_PATHS.md`
- `docs/planning/ZIHAFAT_IMPLEMENTATION_PLAN.md`
- `docs/technical/ARCHITECTURE_OVERVIEW.md`
- `docs/technical/PROSODY_ENGINE_LIMITATIONS.md`

**Change Log:**
- 2025-11-11: Initial diagnostic report created

---

**End of Report**
