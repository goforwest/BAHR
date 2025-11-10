# ✅ Week 0 Critical Checklist
## Pre-Development Setup - Must Complete Before Coding

---

**Status:** 🔴 **CRITICAL - MUST COMPLETE BEFORE WEEK 1**
**Duration:** 3-5 days
**Goal:** Fix all reviewer issues and prepare infrastructure
**Team:** Solo founder or lead developer

---

## 🎯 Overview

This Week 0 phase addresses all 10 critical issues identified in the technical review. Completing these tasks ensures a smooth development process with no security vulnerabilities or architectural ambiguities.

**Why Week 0 is Critical:**
- ❌ **Without it:** Security vulnerabilities, deployment failures, wasted development time
- ✅ **With it:** Production-ready foundation, clear technical decisions, zero blockers

---

## 📋 Task Checklist (10 Critical Items)

### Issue #1: Secrets Management ⚠️ SECURITY CRITICAL

**Problem:** `.env` files in production are insecure

**Solution:** Setup Railway secrets management

- [ ] **1.1** Install Railway CLI
  ```bash
  npm install -g @railway/cli
  railway login
  ```

- [ ] **1.2** Create Railway project
  ```bash
  railway init
  # Select: "Create new project"
  # Name: "bahr-backend"
  ```

- [ ] **1.3** Generate production secrets
  ```bash
  chmod +x scripts/generate_secrets.sh
  ./scripts/generate_secrets.sh > secrets.txt
  # ⚠️ NEVER commit secrets.txt!
  ```

- [ ] **1.4** Add secrets to Railway
  ```bash
  # Copy values from secrets.txt and run:
  railway variables set DATABASE_PASSWORD=<strong-password>
  railway variables set REDIS_PASSWORD=<strong-password>
  railway variables set JWT_SECRET_KEY=<64-char-hex>
  railway variables set JWT_REFRESH_SECRET_KEY=<64-char-hex>
  railway variables set ENCRYPTION_KEY=<64-char-hex>

  # Add non-secret config
  railway variables set APP_ENV=production
  railway variables set LOG_LEVEL=INFO
  railway variables set CORS_ORIGINS=https://bahr.app,https://www.bahr.app
  ```

- [ ] **1.5** Delete secrets.txt securely
  ```bash
  rm secrets.txt
  # Verify it's deleted
  ls secrets.txt  # Should return "No such file"
  ```

- [ ] **1.6** Verify `.env` in `.gitignore`
  ```bash
  grep "^\.env$" .gitignore
  # Should output: .env
  ```

- [ ] **1.7** Check Git history for leaked secrets
  ```bash
  git log -S "password" --all
  git log -S "SECRET_KEY" --all
  # Should return empty or only template files
  ```

**Documentation:** [docs/technical/SECRETS_MANAGEMENT.md](./docs/technical/SECRETS_MANAGEMENT.md)

**Estimated Time:** 1-2 hours

---

### Issue #2: Database Indexes 🗄️ PERFORMANCE CRITICAL

**Problem:** No explicit CREATE INDEX statements

**Solution:** Create Alembic migration with all indexes

- [ ] **2.1** Review index strategy
  ```bash
  # Read the complete index documentation
  cat docs/technical/DATABASE_INDEXES.md
  ```

- [ ] **2.2** Create Alembic migration
  ```bash
  cd backend
  alembic revision -m "add_core_indexes"
  # This creates: alembic/versions/002_add_core_indexes.py
  ```

- [ ] **2.3** Copy index creation SQL from docs
  ```bash
  # Open: alembic/versions/002_add_core_indexes.py
  # Copy content from: docs/technical/DATABASE_INDEXES.md (Section 4)
  # Paste into upgrade() function
  ```

- [ ] **2.4** Test migration locally
  ```bash
  # Start local PostgreSQL (Docker Compose)
  docker-compose up -d postgres

  # Run migration
  alembic upgrade head

  # Verify indexes created
  psql $DATABASE_URL -c "\di"
  # Should show all indexes from DATABASE_INDEXES.md
  ```

- [ ] **2.5** Test index performance
  ```bash
  # Run benchmark queries
  psql $DATABASE_URL < scripts/test_indexes.sql
  # Verify all queries use expected indexes (EXPLAIN ANALYZE output)
  ```

**Documentation:** [docs/technical/DATABASE_INDEXES.md](./docs/technical/DATABASE_INDEXES.md)

**Estimated Time:** 2-3 hours

---

### Issue #3: API Gateway Decision 🌐 ARCHITECTURE CLARIFIED

**Problem:** Ambiguity between Kong and native FastAPI

**Solution:** Document decision to use native FastAPI

- [ ] **3.1** Read ADR-001
  ```bash
  # Review decision rationale
  cat docs/ARCHITECTURE_DECISIONS.md | grep -A 50 "ADR-001"
  ```

- [ ] **3.2** Update implementation notes
  ```bash
  # Add comment to app/main.py
  # """
  # API Gateway Strategy: Native FastAPI Middleware (ADR-001)
  # - Phase 1-3: Use FastAPI middleware for auth, rate limiting, CORS
  # - Phase 4+: Consider Kong if traffic exceeds 100k req/sec
  # """
  ```

- [ ] **3.3** Remove Kong references from Docker Compose
  ```bash
  # Ensure docker-compose.yml does NOT have Kong service
  grep -i kong docker-compose.yml
  # Should return empty
  ```

**Documentation:** [docs/ARCHITECTURE_DECISIONS.md#adr-001](./docs/ARCHITECTURE_DECISIONS.md#adr-001)

**Estimated Time:** 30 minutes

---

### Issue #4: Elasticsearch Timing 🔍 ARCHITECTURE CLARIFIED

**Problem:** Unclear when to integrate Elasticsearch

**Solution:** Document threshold (50k verses)

- [ ] **4.1** Read ADR-002
  ```bash
  cat docs/ARCHITECTURE_DECISIONS.md | grep -A 50 "ADR-002"
  ```

- [ ] **4.2** Update DEFERRED_FEATURES.md
  ```bash
  # Add to docs/planning/DEFERRED_FEATURES.md:
  # - Elasticsearch (defer to Phase 4 or 50k verses threshold)
  # - Use PostgreSQL full-text search for MVP (<50k verses)
  ```

- [ ] **4.3** Add PostgreSQL FTS index to migration
  ```sql
  -- Add to alembic migration (when verses table is created):
  CREATE INDEX idx_verses_fulltext
  ON verses
  USING gin(to_tsvector('arabic', text));
  ```

**Documentation:** [docs/ARCHITECTURE_DECISIONS.md#adr-002](./docs/ARCHITECTURE_DECISIONS.md#adr-002)

**Estimated Time:** 30 minutes

---

### Issue #5: CORS Policy 🔒 SECURITY CRITICAL

**Problem:** No CORS origins specified

**Solution:** Add explicit CORS configuration

- [ ] **5.1** Read ADR-003
  ```bash
  cat docs/ARCHITECTURE_DECISIONS.md | grep -A 50 "ADR-003"
  ```

- [ ] **5.2** Update SECURITY.md
  ```bash
  # Add CORS section to docs/technical/SECURITY.md:
  # ### CORS Policy
  # Development: http://localhost:3000, http://localhost:8000
  # Staging: https://staging.bahr.app
  # Production: https://bahr.app, https://www.bahr.app, https://api.bahr.app
  ```

- [ ] **5.3** Update app/config.py
  ```python
  # Add to Settings class:
  cors_origins: list[str] = [
      "http://localhost:3000",  # Dev
      "http://localhost:8000",
  ]
  ```

- [ ] **5.4** Add CORS middleware implementation
  ```bash
  # Create: backend/app/middleware/cors.py
  # Copy implementation from ADR-003
  ```

**Documentation:** [docs/ARCHITECTURE_DECISIONS.md#adr-003](./docs/ARCHITECTURE_DECISIONS.md#adr-003)

**Estimated Time:** 1 hour

---

### Issue #6: Backup Strategy 💾 OPERATIONS CRITICAL

**Problem:** No automated backup documentation

**Solution:** Enable Railway backups and document restore procedure

- [ ] **6.1** Read ADR-004
  ```bash
  cat docs/ARCHITECTURE_DECISIONS.md | grep -A 50 "ADR-004"
  ```

- [ ] **6.2** Enable Railway automated backups
  ```bash
  # Via Railway dashboard:
  # 1. Go to PostgreSQL service → Settings → Backups
  # 2. Enable automated backups
  # 3. Set retention: 30 days (production), 7 days (staging)
  ```

- [ ] **6.3** Create manual backup script
  ```bash
  # Copy from ADR-004 to scripts/backup_db.sh
  chmod +x scripts/backup_db.sh
  ```

- [ ] **6.4** Test backup restore (staging)
  ```bash
  # Create test backup
  ./scripts/backup_db.sh

  # Restore to local database
  psql $DATABASE_URL < bahr_backup_*.sql
  # Verify data integrity
  ```

- [ ] **6.5** Setup S3 bucket for DR backups (optional but recommended)
  ```bash
  # Create S3 bucket: bahr-db-backups
  aws s3 mb s3://bahr-db-backups
  # Enable versioning
  aws s3api put-bucket-versioning \
    --bucket bahr-db-backups \
    --versioning-configuration Status=Enabled
  ```

**Documentation:** [docs/ARCHITECTURE_DECISIONS.md#adr-004](./docs/ARCHITECTURE_DECISIONS.md#adr-004)

**Estimated Time:** 2 hours

---

### Issue #7: Batch Analysis API 🚀 FEATURE ADDITION

**Problem:** Users need to analyze multiple verses efficiently

**Solution:** Add batch endpoint specification

- [ ] **7.1** Update API_SPECIFICATION.yaml
  ```yaml
  # Add to docs/technical/API_SPECIFICATION.yaml:
  /api/v1/analyze/batch:
    post:
      summary: Analyze multiple verses in one request
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                verses:
                  type: array
                  items:
                    type: string
                  maxItems: 10  # Free tier limit
  ```

- [ ] **7.2** Add to implementation plan
  ```bash
  # Update docs/phases/PHASE_1_MVP.md
  # Add to Week 3-4 tasks:
  # - Implement POST /api/v1/analyze/batch endpoint
  ```

- [ ] **7.3** Create Pydantic schema
  ```python
  # Add to app/schemas/analyze.py:
  class BatchAnalyzeRequest(BaseModel):
      verses: list[str] = Field(..., max_items=10)
      options: Optional[AnalyzeOptions] = None

  class BatchAnalyzeResponse(BaseModel):
      success: bool
      data: dict
      meta: dict
  ```

**Documentation:** [IMPLEMENTATION_PLAN_REVISED_FINAL.md#7-batch-analysis-api](./IMPLEMENTATION_PLAN_REVISED_FINAL.md#7-batch-analysis-api)

**Estimated Time:** 1 hour (planning only, implementation in Week 3)

---

### Issue #8: Pagination Spec 📄 API STANDARDIZATION

**Problem:** No consistent pagination pattern

**Solution:** Define cursor-based pagination standard

- [ ] **8.1** Create pagination schema
  ```python
  # Add to app/schemas/pagination.py:
  from pydantic import BaseModel, Generic, TypeVar

  T = TypeVar('T')

  class PaginationMeta(BaseModel):
      next_cursor: Optional[str] = None
      has_more: bool
      limit: int

  class PaginatedResponse(BaseModel, Generic[T]):
      items: list[T]
      pagination: PaginationMeta
  ```

- [ ] **8.2** Update API_CONVENTIONS.md
  ```markdown
  # Add section: Pagination Standard
  All list endpoints must use cursor-based pagination:
  - Query params: ?limit=20&cursor=abc123
  - Response format: { items: [...], pagination: { next_cursor, has_more, limit } }
  ```

- [ ] **8.3** Add to implementation plan
  ```bash
  # Note: Will implement pagination in Week 4 when building list endpoints
  ```

**Documentation:** [IMPLEMENTATION_PLAN_REVISED_FINAL.md#8-pagination-specification](./IMPLEMENTATION_PLAN_REVISED_FINAL.md#8-pagination-specification)

**Estimated Time:** 1 hour (planning only)

---

### Issue #9: Circuit Breaker 🔄 RELIABILITY FEATURE

**Problem:** No retry logic for database failures

**Solution:** Add circuit breaker pattern with Tenacity

- [ ] **9.1** Add tenacity dependency
  ```bash
  # Add to backend/requirements.txt:
  tenacity==8.2.3
  ```

- [ ] **9.2** Create circuit breaker utility
  ```python
  # Create: backend/app/core/circuit_breaker.py
  # Copy implementation from IMPLEMENTATION_PLAN_REVISED_FINAL.md
  ```

- [ ] **9.3** Add to implementation plan
  ```bash
  # Note: Will integrate circuit breaker in Week 5 when building repositories
  ```

**Documentation:** [IMPLEMENTATION_PLAN_REVISED_FINAL.md#9-circuit-breaker-pattern](./IMPLEMENTATION_PLAN_REVISED_FINAL.md#9-circuit-breaker-pattern)

**Estimated Time:** 30 minutes (planning only, implementation in Week 5)

---

### Issue #10: Security Tests 🛡️ SECURITY CRITICAL

**Problem:** No automated security testing

**Solution:** Create security test suite

- [ ] **10.1** Create security test directory
  ```bash
  mkdir -p backend/tests/security
  touch backend/tests/security/__init__.py
  ```

- [ ] **10.2** Create test templates
  ```bash
  # Create files (content from IMPLEMENTATION_PLAN_REVISED_FINAL.md):
  touch backend/tests/security/test_sql_injection.py
  touch backend/tests/security/test_xss.py
  touch backend/tests/security/test_auth.py
  touch backend/tests/security/test_access_control.py
  ```

- [ ] **10.3** Add to CI/CD pipeline
  ```yaml
  # Update .github/workflows/backend.yml:
  - name: Run security tests
    run: pytest backend/tests/security/ -v
  ```

- [ ] **10.4** Add to implementation plan
  ```bash
  # Note: Will write security tests in Week 7
  ```

**Documentation:** [IMPLEMENTATION_PLAN_REVISED_FINAL.md#10-security-testing-suite](./IMPLEMENTATION_PLAN_REVISED_FINAL.md#10-security-testing-suite)

**Estimated Time:** 1 hour (setup only, tests written in Week 7)

---

## ✅ Verification Checklist

After completing all tasks, verify:

### Secrets Management
- [ ] Railway project created and linked
- [ ] All production secrets in Railway (not .env)
- [ ] `.env` in `.gitignore`
- [ ] No secrets in Git history

### Database
- [ ] Alembic migration `002_add_core_indexes.py` created
- [ ] Migration tested locally
- [ ] All indexes verified with `\di` command
- [ ] Index performance tested with EXPLAIN ANALYZE

### Architecture
- [ ] API Gateway decision documented (native FastAPI)
- [ ] Elasticsearch threshold documented (50k verses)
- [ ] No ambiguous architecture references in code

### Security
- [ ] CORS policy specified in SECURITY.md
- [ ] CORS middleware implementation ready
- [ ] Security test structure created

### Operations
- [ ] Railway backups enabled (30-day retention)
- [ ] Backup script created and tested
- [ ] Restore procedure documented

### API Design
- [ ] Batch endpoint specification added
- [ ] Pagination schema created
- [ ] API_CONVENTIONS.md updated

### Code Quality
- [ ] Circuit breaker utility created
- [ ] Tenacity added to requirements.txt
- [ ] Security test directory structure ready

---

## 📊 Progress Tracking

**Total Tasks:** 45 tasks across 10 critical issues

**Estimated Time:**
- Critical (must do): 8-10 hours
- Planning (for later phases): 3-4 hours
- **Total Week 0 effort:** 11-14 hours (2-3 days)

**Progress:**
- [ ] Issue #1: Secrets Management (5 tasks, ~2h)
- [ ] Issue #2: Database Indexes (5 tasks, ~3h)
- [ ] Issue #3: API Gateway (3 tasks, ~30m)
- [ ] Issue #4: Elasticsearch Timing (3 tasks, ~30m)
- [ ] Issue #5: CORS Policy (4 tasks, ~1h)
- [ ] Issue #6: Backup Strategy (5 tasks, ~2h)
- [ ] Issue #7: Batch API (3 tasks, ~1h)
- [ ] Issue #8: Pagination (3 tasks, ~1h)
- [ ] Issue #9: Circuit Breaker (3 tasks, ~30m)
- [ ] Issue #10: Security Tests (4 tasks, ~1h)

---

## 🚨 Blockers & Escalation

**If you encounter issues:**

1. **Railway signup fails:**
   - Alternative: Use Render or DigitalOcean
   - Update SECRETS_MANAGEMENT.md with new platform

2. **Cannot generate strong secrets:**
   - Install OpenSSL: `brew install openssl` (macOS)
   - Alternative: Use Python: `python3 -c "import secrets; print(secrets.token_hex(32))"`

3. **Alembic migration fails:**
   - Check PostgreSQL version (must be 13+)
   - Verify database connection: `psql $DATABASE_URL`

4. **Git history has secrets:**
   - Use BFG Repo-Cleaner: `bfg --replace-text passwords.txt`
   - Force push: `git push --force`
   - ⚠️ Rotate all exposed secrets immediately

---

## ✅ Completion Criteria

**Week 0 is complete when:**

1. ✅ All 10 critical issues resolved
2. ✅ Railway project configured with secrets
3. ✅ Database index migration created and tested
4. ✅ All architecture decisions documented (ADR-001 through ADR-004)
5. ✅ Security configurations in place (CORS, backups)
6. ✅ Team can start Week 1 development with zero blockers

**Sign-off:**
- [ ] Lead Developer approval
- [ ] Security review passed
- [ ] Architecture review passed

---

## 🚀 Next Step: Week 1

Once Week 0 is complete:

1. **Read:** [PHASE_1_WEEK_1-2_SPEC.md](./PHASE_1_WEEK_1-2_SPEC.md)
2. **Start:** Implement `backend/app/core/normalization.py`
3. **Track:** Update [PROJECT_TRACKER.md](./PROJECT_TRACKER.md) daily

**Good luck! 🎯**

---

**Document Owner:** Lead Developer
**Last Updated:** November 9, 2025
**Next Review:** After Week 0 completion (before Week 1 starts)
