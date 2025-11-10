# Feature: Deployment & CI/CD - Implementation Guide

**Feature ID:** `feature-deployment-cicd`  
**Status:** Production-Ready  
**Last Updated:** November 8, 2025  
**Estimated Implementation Time:** 12-16 hours

---

## 1. Objective & Description

### What
Implement complete CI/CD pipeline with Docker containerization, GitHub Actions workflows, automated testing, and deployment to Railway (backend) and Vercel (frontend).

### Why
- **Automation:** Deploy on every merge to main
- **Quality:** Run tests before deployment
- **Consistency:** Identical environments (dev/staging/prod)
- **Speed:** Fast iteration cycles
- **Reliability:** Rollback capabilities

### Success Criteria
- ✅ Multi-stage Dockerfile for backend (Python 3.11)
- ✅ Docker Compose for local development
- ✅ GitHub Actions workflow (test → build → deploy)
- ✅ Automated tests on pull requests
- ✅ Railway deployment for backend API
- ✅ Vercel deployment for Next.js frontend
- ✅ Environment variable management
- ✅ Health check endpoints

---

## 2. Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                CI/CD Pipeline Architecture                           │
└─────────────────────────────────────────────────────────────────────┘

Developer
    │
    │  git push
    ▼
┌──────────────────────────────────────┐
│ GitHub Repository                    │
│ - main branch                        │
│ - pull requests                      │
└──────────┬───────────────────────────┘
           │
           │  webhook trigger
           ▼
┌──────────────────────────────────────┐
│ GitHub Actions                       │
│ ┌─────────────────────────────────┐  │
│ │ 1. Checkout code                │  │
│ │ 2. Run linters (ruff, mypy)     │  │
│ │ 3. Run tests (pytest)           │  │
│ │ 4. Build Docker image           │  │
│ │ 5. Push to registry             │  │
│ └─────────────────────────────────┘  │
└──────────┬───────────────────────────┘
           │
           ├─────────────┬─────────────┐
           │             │             │
           ▼             ▼             ▼
    ┌──────────┐  ┌──────────┐  ┌──────────┐
    │ Railway  │  │ Vercel   │  │ Docker   │
    │ (Backend)│  │(Frontend)│  │ Registry │
    └──────────┘  └──────────┘  └──────────┘

Deployment Flow:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Pull Request → Run tests + linters
2. Merge to main → Build + Deploy to Railway/Vercel
3. Health check → Verify deployment
4. Rollback if health check fails

Environments:
- Development: docker-compose up (local)
- Staging: Railway preview deployments
- Production: Railway + Vercel (main branch)
```

---

## 3. Input/Output Contracts

### 3.1 Environment Variables

```bash
# backend/.env.example
# Database
DATABASE_URL=postgresql://bahr_user:password@localhost:5432/bahr_db

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API
API_VERSION=1.0.0
ALLOWED_ORIGINS=http://localhost:3000,https://bahr.example.com

# Rate Limiting
RATE_LIMIT_GUEST=100
RATE_LIMIT_AUTHENTICATED=1000

# Monitoring
PROMETHEUS_ENABLED=true
```

```bash
# frontend/.env.example
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_VERSION=1.0.0
```

---

## 4. Step-by-Step Implementation

### Step 1: Create Multi-Stage Dockerfile

```dockerfile
# backend/Dockerfile
"""
Multi-stage Dockerfile for Python FastAPI backend.

Source: docs/technical/DEPLOYMENT_GUIDE.md:1-120
"""

# Stage 1: Build dependencies
FROM python:3.11-slim as builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY . .

# Update PATH
ENV PATH=/root/.local/bin:$PATH

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Step 2: Create Docker Compose

```yaml
# docker-compose.yml
"""
Docker Compose for local development.

Source: docker-compose.yml:1-150
"""

version: '3.8'

services:
  # PostgreSQL Database
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: bahr_user
      POSTGRES_PASSWORD: bahr_password
      POSTGRES_DB: bahr_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U bahr_user -d bahr_db"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis Cache
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5

  # Backend API
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://bahr_user:bahr_password@postgres:5432/bahr_db
      REDIS_URL: redis://redis:6379/0
      SECRET_KEY: dev-secret-key-change-in-production
      ALLOWED_ORIGINS: http://localhost:3000
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      - ./backend:/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  # Frontend (Next.js)
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      NEXT_PUBLIC_API_URL: http://localhost:8000
    depends_on:
      - backend
    volumes:
      - ./frontend:/app
      - /app/node_modules
    command: npm run dev

volumes:
  postgres_data:
  redis_data:
```

### Step 3: Create GitHub Actions Workflow

```yaml
# .github/workflows/ci-cd.yml
"""
Main CI/CD workflow for BAHR project.

Runs on: Pull requests, pushes to main
"""

name: CI/CD Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  PYTHON_VERSION: '3.11'
  NODE_VERSION: '18'

jobs:
  # Job 1: Lint and Test Backend
  backend-test:
    name: Backend Tests
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_password
          POSTGRES_DB: test_db
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
      
      redis:
        image: redis:7
        ports:
          - 6379:6379
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          cache: 'pip'
      
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
          pip install pytest pytest-cov ruff mypy
      
      - name: Run linters
        run: |
          cd backend
          ruff check .
          mypy app --ignore-missing-imports
      
      - name: Run tests
        env:
          DATABASE_URL: postgresql://test_user:test_password@localhost:5432/test_db
          REDIS_URL: redis://localhost:6379/0
          SECRET_KEY: test-secret-key
        run: |
          cd backend
          pytest tests/ -v --cov=app --cov-report=xml --cov-report=term
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./backend/coverage.xml

  # Job 2: Test Frontend
  frontend-test:
    name: Frontend Tests
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
          cache-dependency-path: frontend/package-lock.json
      
      - name: Install dependencies
        run: |
          cd frontend
          npm ci
      
      - name: Run linter
        run: |
          cd frontend
          npm run lint
      
      - name: Run tests
        run: |
          cd frontend
          npm test
      
      - name: Build
        run: |
          cd frontend
          npm run build

  # Job 3: Build and Push Docker Image
  build-backend:
    name: Build Backend Docker Image
    runs-on: ubuntu-latest
    needs: [backend-test]
    if: github.ref == 'refs/heads/main'
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
      
      - name: Login to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      
      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: ./backend
          push: true
          tags: |
            ${{ secrets.DOCKER_USERNAME }}/bahr-backend:latest
            ${{ secrets.DOCKER_USERNAME }}/bahr-backend:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  # Job 4: Deploy to Railway
  deploy-backend:
    name: Deploy Backend to Railway
    runs-on: ubuntu-latest
    needs: [build-backend]
    if: github.ref == 'refs/heads/main'
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Install Railway CLI
        run: npm install -g @railway/cli
      
      - name: Deploy to Railway
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
        run: |
          cd backend
          railway up --service backend

  # Job 5: Deploy Frontend to Vercel
  deploy-frontend:
    name: Deploy Frontend to Vercel
    runs-on: ubuntu-latest
    needs: [frontend-test]
    if: github.ref == 'refs/heads/main'
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          working-directory: ./frontend
          vercel-args: '--prod'
```

### Step 4: Create Health Check Endpoint

```python
# backend/app/api/v1/routes/health.py
"""
Health check endpoints for monitoring.

Source: docs/technical/MONITORING_INTEGRATION.md:50-100
"""

from fastapi import APIRouter, status
from sqlalchemy import text
from app.db.base import SessionLocal
import redis
import os

router = APIRouter(tags=["health"])


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """
    Basic health check.
    
    Returns 200 if service is running.
    """
    return {
        "status": "healthy",
        "service": "bahr-api",
        "version": os.getenv("API_VERSION", "1.0.0")
    }


@router.get("/health/detailed", status_code=status.HTTP_200_OK)
async def detailed_health_check():
    """
    Detailed health check with dependency status.
    
    Checks:
    - Database connectivity
    - Redis connectivity
    """
    health = {
        "status": "healthy",
        "checks": {}
    }
    
    # Check database
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        health["checks"]["database"] = "healthy"
    except Exception as e:
        health["checks"]["database"] = f"unhealthy: {str(e)}"
        health["status"] = "degraded"
    
    # Check Redis
    try:
        redis_client = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"))
        redis_client.ping()
        health["checks"]["redis"] = "healthy"
    except Exception as e:
        health["checks"]["redis"] = f"unhealthy: {str(e)}"
        health["status"] = "degraded"
    
    return health
```

### Step 5: Railway Configuration

```toml
# backend/railway.toml
[build]
builder = "DOCKERFILE"
dockerfilePath = "Dockerfile"

[deploy]
startCommand = "uvicorn app.main:app --host 0.0.0.0 --port $PORT"
healthcheckPath = "/health"
healthcheckTimeout = 100
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 3

[env]
PORT = "8000"
```

### Step 6: Vercel Configuration

```json
// frontend/vercel.json
{
  "framework": "nextjs",
  "buildCommand": "npm run build",
  "devCommand": "npm run dev",
  "installCommand": "npm ci",
  "regions": ["iad1"],
  "env": {
    "NEXT_PUBLIC_API_URL": "@bahr-api-url"
  },
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Frame-Options",
          "value": "DENY"
        },
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        }
      ]
    }
  ]
}
```

### Step 7: Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.6
    hooks:
      - id: ruff
        args: [--fix]
      
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.1
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
```

---

## 5. Reference Implementation (Full Code)

See Step-by-Step Implementation sections above for complete code.

---

## 6. Unit & Integration Tests

```python
# tests/integration/test_health.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_endpoint():
    """Test basic health check."""
    response = client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


def test_detailed_health():
    """Test detailed health check."""
    response = client.get("/health/detailed")
    
    assert response.status_code == 200
    data = response.json()
    assert "checks" in data
    assert "database" in data["checks"]
    assert "redis" in data["checks"]
```

---

## 7. CI/CD Pipeline

See Step 3 above for complete GitHub Actions workflow.

---

## 8. Deployment Checklist

### Pre-Deployment
- [ ] Set all environment variables in Railway/Vercel
- [ ] Configure database connection (PostgreSQL 15)
- [ ] Configure Redis connection
- [ ] Set SECRET_KEY (generate with `openssl rand -hex 32`)
- [ ] Configure ALLOWED_ORIGINS
- [ ] Test health check endpoints locally

### Railway Deployment (Backend)
- [ ] Create Railway project
- [ ] Link GitHub repository
- [ ] Set environment variables
- [ ] Configure Dockerfile build
- [ ] Set up PostgreSQL plugin
- [ ] Set up Redis plugin
- [ ] Run Alembic migrations
- [ ] Verify /health endpoint

### Vercel Deployment (Frontend)
- [ ] Create Vercel project
- [ ] Link GitHub repository
- [ ] Set NEXT_PUBLIC_API_URL
- [ ] Configure production domain
- [ ] Test RTL rendering
- [ ] Verify API connectivity

### Post-Deployment
- [ ] Run smoke tests
- [ ] Monitor error rates
- [ ] Check performance metrics
- [ ] Verify SSL certificates
- [ ] Set up monitoring alerts
- [ ] Document deployment process

---

## 9. Observability

```yaml
# Monitoring Stack
- Railway Metrics: CPU, Memory, Request count
- Vercel Analytics: Page views, Web Vitals
- Prometheus: Custom metrics from /metrics endpoint
- Sentry: Error tracking (optional)

# Key Metrics
- Deployment frequency: Track via GitHub Actions
- Lead time: Commit to production time
- MTTR: Mean time to recovery
- Change failure rate: Failed deployments / total
```

---

## 10. Security & Safety

- **Secrets Management:** Use GitHub Secrets, never commit .env files
- **Image Scanning:** Scan Docker images for vulnerabilities
- **HTTPS Only:** Enforce HTTPS in production
- **Environment Isolation:** Separate dev/staging/prod databases
- **Rollback Strategy:** Keep last 3 Docker images

---

## 11. Backwards Compatibility

- **Database Migrations:** Always use Alembic, never manual changes
- **API Versioning:** Use /api/v1 prefix for breaking changes
- **Feature Flags:** Use environment variables for gradual rollout

---

## 12. Source Documentation Citations

1. **docs/technical/DEPLOYMENT_GUIDE.md:1-300** - Deployment procedures
2. **docker-compose.yml:1-150** - Local development setup
3. **backend/Dockerfile:1-50** - Container configuration
4. **implementation-guides/IMPROVED_PROMPT.md:788-810** - Feature specification

---

**Implementation Complete!** ✅  
**Estimated Time:** 12-16 hours  
**Deployment Targets:** Railway (backend) + Vercel (frontend)  
**CI/CD Platform:** GitHub Actions
