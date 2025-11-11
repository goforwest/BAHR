# ⚠️ External Dependencies Report - BAHR Restructuring

**Migration Impact Assessment**  
**Date:** November 10, 2025  
**Status:** Pre-Migration Analysis

---

## 📋 Executive Summary

This document identifies all systems, configurations, and processes **outside this repository** that require updates after the BAHR repository restructuring. Use this as a checklist during and after migration.

---

## 🎯 Critical External Dependencies

### 1. Railway Deployment Configuration

**Impact:** 🔴 **CRITICAL**  
**Owner:** DevOps Team / Repository Owner  
**Action Required:** YES - Update Railway project settings

#### Backend Service

**Railway Dashboard Settings to Verify/Update:**

```yaml
Service: bahr-backend

Settings to Check:
  Root Directory: /backend  # ← Should already be set, verify
  
  Build Settings:
    Builder: Nixpacks (auto-detected)
    Build Command: (auto-detected from requirements.txt)
    
  Deploy Settings:
    Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    
  Environment Variables:
    DATABASE_URL: [VERIFY - should be unchanged]
    REDIS_URL: [VERIFY - should be unchanged]
    SECRET_KEY: [VERIFY - should be unchanged]
    # ... all other env vars unchanged
```

**Files Moved (Railway Auto-Detection):**
- `backend/railway.json` → `infrastructure/railway/backend.json`
- `backend/Dockerfile.railway` → `infrastructure/docker/backend/Dockerfile.prod`

**Verification Steps:**
1. Log into Railway dashboard
2. Navigate to `bahr-backend` service
3. Check "Settings" → "Service Settings" → Root Directory = `/backend`
4. Verify "Deploy" settings reference correct start command
5. After migration, trigger manual deployment
6. Monitor deployment logs for errors
7. Test deployed API: `curl https://your-backend-url.railway.app/health`

---

#### Frontend Service

**Railway Dashboard Settings to Verify/Update:**

```yaml
Service: bahr-frontend

Settings to Check:
  Root Directory: /frontend  # ← Should already be set, verify
  
  Build Settings:
    Builder: Nixpacks (auto-detected)
    Build Command: npm run build
    
  Deploy Settings:
    Start Command: npm start
    
  Environment Variables:
    NEXT_PUBLIC_API_URL: [VERIFY - should be unchanged]
    # ... all other env vars unchanged
```

**Files Moved (Railway Auto-Detection):**
- `frontend/railway.json` → `infrastructure/railway/frontend.json`

**Verification Steps:**
1. Log into Railway dashboard
2. Navigate to `bahr-frontend` service
3. Check "Settings" → "Service Settings" → Root Directory = `/frontend`
4. After migration, trigger manual deployment
5. Monitor deployment logs
6. Test deployed frontend: `https://your-frontend-url.railway.app`

---

**Railway Monorepo Configuration (if used):**

If using `railway.toml` for monorepo setup:

```toml
# infrastructure/railway/railway.toml
# Verify paths after move from root

[build]
builder = "nixpacks"

[deploy]
restartPolicyType = "on_failure"
restartPolicyMaxRetries = 10

# Backend service
[[services]]
name = "backend"
rootDirectory = "backend"
startCommand = "uvicorn app.main:app --host 0.0.0.0 --port $PORT"

# Frontend service  
[[services]]
name = "frontend"
rootDirectory = "frontend"
startCommand = "npm start"
```

**Action Required:**
- [ ] Verify Railway reads `infrastructure/railway/railway.toml` (or update Railway to reference it)
- [ ] OR migrate to per-service `railway.json` files in respective service directories

---

### 2. GitHub Actions Secrets & Variables

**Impact:** 🟡 **MEDIUM**  
**Owner:** Repository Administrator  
**Action Required:** VERIFY (likely no changes needed)

**Secrets/Variables to Verify Still Work:**

```yaml
Repository Secrets (GitHub Settings → Secrets and variables → Actions):
  - RAILWAY_TOKEN (if used for deployments)
  - Any API keys for external services
  - Docker registry credentials (if used)
  
Repository Variables:
  - BACKEND_URL (if used in workflows)
  - FRONTEND_URL (if used in workflows)
```

**Action Required:**
- [ ] Navigate to: `https://github.com/goforwest/BAHR/settings/secrets/actions`
- [ ] Verify all secrets are still present and valid
- [ ] No changes needed (secrets are repository-level, not path-dependent)
- [ ] After migration, verify workflow runs still have access to secrets

---

### 3. External Documentation & Links

**Impact:** 🟡 **MEDIUM**  
**Owner:** Documentation Team / Content Authors  
**Action Required:** YES - Update external references

#### Broken Links After Migration

**GitHub URLs that will return 404:**

```
# Direct file links (will break)
https://github.com/goforwest/BAHR/blob/main/alembic/env.py
  → Now: https://github.com/goforwest/BAHR/blob/main/backend/database/migrations/env.py

https://github.com/goforwest/BAHR/blob/main/alembic.ini
  → Now: https://github.com/goforwest/BAHR/blob/main/backend/database/migrations/alembic.ini

https://github.com/goforwest/BAHR/blob/main/pytest.ini
  → Now: REMOVED (use backend/pytest.ini or dataset/pytest.ini)

https://github.com/goforwest/BAHR/blob/main/docker-compose.yml
  → Now: https://github.com/goforwest/BAHR/blob/main/infrastructure/docker/docker-compose.yml

https://github.com/goforwest/BAHR/tree/main/implementation-guides
  → Now: https://github.com/goforwest/BAHR/tree/main/docs/features
```

#### Places to Update

**Internal GitHub:**
- [ ] Repository wiki (if exists)
- [ ] Pinned issues (if any reference old paths)
- [ ] Issue templates (`.github/ISSUE_TEMPLATE/`)
- [ ] PR templates (`.github/PULL_REQUEST_TEMPLATE.md`)
- [ ] GitHub Discussions (if any reference old structure)

**External Sites:**
- [ ] Personal blog posts about the project
- [ ] Medium articles or dev.to posts
- [ ] LinkedIn posts with code snippets
- [ ] Stack Overflow answers referencing the repo
- [ ] External wikis (Notion, Confluence, etc.)
- [ ] Team knowledge bases
- [ ] Documentation hosted elsewhere (ReadTheDocs, GitBook, etc.)

**Action Required:**
1. Search for external references: `site:yoursite.com "github.com/goforwest/BAHR"`
2. Update all external documentation referencing old paths
3. Consider adding GitHub redirects (not possible for blob URLs)
4. Update bookmarks in team browsers

---

### 4. Developer Workstations

**Impact:** 🟢 **LOW-MEDIUM**  
**Owner:** Individual Developers  
**Action Required:** YES - Each developer follows migration guide

**What Developers Need to Update:**

#### IDE Configurations

**VS Code:**
```json
// .vscode/settings.json (if exists in repo - will be updated)
// Individual developer settings.json may need updates:

{
  // Python path (may need update if referencing old structure)
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  
  // Test discovery (should auto-detect new pytest.ini locations)
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": ["-v"],
  
  // Alembic may need custom task updates (see below)
}
```

**PyCharm/IntelliJ:**
- Python interpreter: Should auto-detect, but verify points to correct `.venv`
- Test configuration: Verify pytest working directory is `backend/` for backend tests
- Run configurations: Update any custom run configs referencing old paths

---

#### Custom Scripts & Aliases

**Shell Aliases (personal `~/.zshrc` or `~/.bashrc`):**

```bash
# OLD (will break):
alias bahr-migrate='cd ~/Projects/BAHR && alembic upgrade head'
alias bahr-test='cd ~/Projects/BAHR && pytest'
alias bahr-up='cd ~/Projects/BAHR && docker-compose up'

# NEW (updated):
alias bahr-migrate='cd ~/Projects/BAHR/backend && alembic -c database/migrations/alembic.ini upgrade head'
alias bahr-test='cd ~/Projects/BAHR/backend && pytest'
alias bahr-up='cd ~/Projects/BAHR && docker-compose -f infrastructure/docker/docker-compose.yml up'
```

**Action Required:**
- [ ] Each developer reviews their personal shell aliases
- [ ] Update any aliases referencing old paths
- [ ] Provide template aliases in migration guide (already done)

---

#### Pre-commit Hooks (if configured locally)

**Git hooks in `.git/hooks/` (local, not in repo):**

If developers have local pre-commit hooks that run tests or migrations:

```bash
# .git/hooks/pre-commit (example)
#!/bin/bash

# OLD:
pytest || exit 1

# NEW:
cd backend && pytest || exit 1
```

**Action Required:**
- [ ] Notify team to review local git hooks
- [ ] Update any hooks referencing old structure

---

### 5. Continuous Integration Runners

**Impact:** 🟡 **MEDIUM**  
**Owner:** DevOps Team  
**Action Required:** VERIFY (workflows updated in repo)

**GitHub Actions (Already Handled in Migration):**
- ✅ Workflow files updated in repository
- ✅ Path filters updated
- ✅ Working directories updated
- ✅ Test commands updated

**Self-Hosted Runners (if any):**
- [ ] Verify runner environments have correct dependencies
- [ ] Clear old caches after migration
- [ ] Verify runner workspace cleanup works with new structure

**Third-Party CI (if used):**
- [ ] **Travis CI:** Update `.travis.yml` if exists
- [ ] **CircleCI:** Update `.circleci/config.yml` if exists
- [ ] **Jenkins:** Update Jenkinsfile if exists
- [ ] **GitLab CI:** Update `.gitlab-ci.yml` if exists

**Action Required:**
1. Identify any CI systems beyond GitHub Actions
2. Update their configuration files (similar to GitHub Actions changes)
3. Test on feature branch before merging

---

### 6. External Monitoring & APM Services

**Impact:** 🟢 **LOW**  
**Owner:** DevOps Team  
**Action Required:** VERIFY (likely minimal changes)

#### Sentry (if configured)

**What to Check:**
- Source maps still upload correctly (frontend)
- Stack traces still resolve correctly
- Release tagging still works

**Action Required:**
- [ ] Monitor Sentry after deployment for any path-related issues
- [ ] Verify error grouping still works correctly
- [ ] Check source maps if frontend errors appear

---

#### Prometheus/Grafana (if configured)

**What to Check:**
- Metrics scraping endpoints unchanged (`/metrics`)
- Dashboard queries still work
- Alert rules still trigger correctly

**Action Required:**
- [ ] Verify `/metrics` endpoint still accessible
- [ ] Check dashboards for missing data after deployment
- [ ] Test alert rules fire correctly

---

#### DataDog / New Relic (if configured)

**What to Check:**
- APM traces still work
- Log aggregation patterns still match
- Service maps show correct topology

**Action Required:**
- [ ] Review APM dashboard after deployment
- [ ] Verify log parsing patterns still work
- [ ] Check service topology visualization

---

### 7. Dependency Scanning & Security Tools

**Impact:** 🟢 **LOW**  
**Owner:** Security Team / DevOps  
**Action Required:** VERIFY

#### Dependabot

**Configuration:** `.github/dependabot.yml` (if exists)

```yaml
# May need to update if it references specific paths
version: 2
updates:
  # Backend dependencies
  - package-ecosystem: "pip"
    directory: "/backend"  # ← Verify this is correct
    schedule:
      interval: "weekly"
      
  # Frontend dependencies
  - package-ecosystem: "npm"
    directory: "/frontend"  # ← Should be unchanged
    schedule:
      interval: "weekly"
```

**Action Required:**
- [ ] Review `.github/dependabot.yml` (if exists)
- [ ] Verify Dependabot PRs still create successfully after migration
- [ ] Check that dependency updates still work

---

#### Snyk / GitHub Security Scanning

**What to Check:**
- Dependency scans still find `requirements.txt` and `package.json`
- Security advisories still appear correctly
- Auto-fix PRs still work

**Action Required:**
- [ ] Monitor security alerts after migration
- [ ] Verify Snyk (if used) still scans correctly
- [ ] Check GitHub security tab for any issues

---

### 8. Code Quality Services

**Impact:** 🟢 **LOW**  
**Owner:** Development Team  
**Action Required:** VERIFY

#### CodeClimate (if configured)

**Configuration:** `.codeclimate.yml` (if exists)

```yaml
# May have path exclusions that need updating
exclude_patterns:
  - "backend/database/migrations/"  # ← Update from "alembic/"
  - "backend/tests/"
  - "frontend/node_modules/"
```

**Action Required:**
- [ ] Update `.codeclimate.yml` if it exists
- [ ] Re-run code quality scan after migration
- [ ] Verify quality metrics still accurate

---

#### SonarQube (if configured)

**Configuration:** `sonar-project.properties` (if exists)

```properties
# May need path updates
sonar.sources=backend/app,frontend/src
sonar.exclusions=**/tests/**,**/migrations/**,**/node_modules/**
```

**Action Required:**
- [ ] Update `sonar-project.properties` if it exists
- [ ] Re-run SonarQube analysis
- [ ] Verify code coverage reports still accurate

---

### 9. Docker Registry / Image Storage

**Impact:** 🟢 **LOW**  
**Owner:** DevOps Team  
**Action Required:** VERIFY

**Docker Hub / GitHub Container Registry (if used):**

- Image build contexts may change (now in `infrastructure/docker/backend/`)
- Image tags should remain unchanged
- Automated builds should still work

**Action Required:**
- [ ] Verify automated Docker builds still trigger
- [ ] Check image sizes haven't changed significantly
- [ ] Test pulling and running images

---

### 10. Team Communication & Knowledge Bases

**Impact:** 🟢 **LOW**  
**Owner:** Project Manager / Team Lead  
**Action Required:** YES - Notify team

**Slack/Discord/Teams:**
- [ ] Announce migration in team channels
- [ ] Share migration guide
- [ ] Pin important migration messages
- [ ] Update channel descriptions if they reference old structure

**Notion/Confluence/Wiki:**
- [ ] Update team wiki pages referencing repository structure
- [ ] Update onboarding documentation
- [ ] Update runbooks referencing old paths
- [ ] Archive old documentation clearly marked as "outdated"

**Email/Newsletters:**
- [ ] Send migration announcement to all contributors
- [ ] Include link to migration guide
- [ ] Provide support contact for questions

---

## 📊 Summary Checklist

### Pre-Migration
- [ ] Backup Railway deployment settings
- [ ] Document current environment variables
- [ ] Export CI/CD configurations
- [ ] List all external documentation
- [ ] Notify all team members

### During Migration
- [ ] Monitor Railway deployments
- [ ] Watch CI/CD pipeline runs
- [ ] Check for external link breakage
- [ ] Verify secrets/variables still accessible

### Post-Migration (Week 1)
- [ ] Railway backend deploys successfully
- [ ] Railway frontend deploys successfully
- [ ] All CI/CD workflows pass
- [ ] No broken external links reported
- [ ] Team confirms local environments working
- [ ] Monitoring dashboards show normal metrics
- [ ] Security scans still functioning
- [ ] No production incidents related to restructure

### Post-Migration (Week 2-4)
- [ ] All external documentation updated
- [ ] Team fully adapted to new structure
- [ ] No ongoing migration-related issues
- [ ] Metrics show improved or unchanged performance
- [ ] Knowledge base fully updated

---

## 🚨 Rollback Procedures

**If critical issues arise:**

### Railway Rollback
1. Log into Railway dashboard
2. Navigate to affected service (backend/frontend)
3. Go to "Deployments" tab
4. Find last successful pre-migration deployment
5. Click "Redeploy"
6. Monitor until stable

### GitHub Rollback
```bash
# Revert to pre-migration state
git checkout main
git revert <migration-commit-hash>
git push origin main

# OR hard reset (destructive)
git reset --hard <pre-migration-tag>
git push origin main --force-with-lease
```

### Notify Team
- Post in all team channels
- Explain rollback reason
- Provide updated timeline
- Assign investigation to determine root cause

---

## 📞 Support Contacts

**For Railway Issues:**
- Railway Dashboard: https://railway.app/
- Railway Support: support@railway.app
- Railway Discord: https://discord.gg/railway

**For GitHub Issues:**
- GitHub Support: https://support.github.com/
- Repository Owner: [Your Contact]

**For Team Issues:**
- Project Manager: [Contact]
- DevOps Lead: [Contact]
- Technical Lead: [Contact]

---

## 📝 Migration Timeline

| Phase | Duration | External Dependencies Affected |
|-------|----------|-------------------------------|
| **Planning** | Complete | None |
| **Migration Execution** | 4-8 hours | None (repository only) |
| **Deployment** | 1-2 hours | Railway (backend & frontend) |
| **Verification** | 24 hours | All monitoring systems |
| **Documentation Update** | 1 week | External docs, wikis, blogs |
| **Team Adaptation** | 2-4 weeks | Developer workstations |
| **Full Stability** | 4 weeks | All systems normalized |

---

## 🎯 Success Criteria

**Migration is considered successful when:**

- [ ] Railway backend deploys and passes health checks
- [ ] Railway frontend deploys and loads correctly
- [ ] All GitHub Actions workflows pass
- [ ] No increase in error rates or response times
- [ ] 100% of team members can develop locally
- [ ] All external documentation updated
- [ ] Zero production incidents related to migration
- [ ] Monitoring shows stable or improved metrics
- [ ] All security scans still functioning
- [ ] Dependency updates still automated

---

**Document Version:** 1.0  
**Last Updated:** November 10, 2025  
**Related Documents:**
- [REPOSITORY_RESTRUCTURING_PLAN.md](../REPOSITORY_RESTRUCTURING_PLAN.md)
- [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)
- [REPOSITORY_STRUCTURE.md](../REPOSITORY_STRUCTURE.md)
