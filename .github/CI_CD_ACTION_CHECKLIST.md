# CI/CD Setup - Team Action Checklist

**Status:** 🟡 AWAITING TEAM ACTION  
**Deadline:** Week 2  
**Owner:** DevOps / Team Lead  

---

## ✅ Completed (by Copilot)

- [x] Created `.github/workflows/backend.yml` - Backend CI pipeline
- [x] Created `.github/workflows/frontend.yml` - Frontend CI pipeline  
- [x] Created `.github/workflows/deploy.yml` - Deployment workflow
- [x] Created `railway.toml` - Railway configuration
- [x] Added status badges to `README.md`
- [x] Created comprehensive documentation
- [x] Created quick reference guide
- [x] Created architecture diagrams

---

## 🔴 ACTION REQUIRED: GitHub Repository Settings

### 1. Branch Protection (HIGH PRIORITY)

**Path:** Settings → Branches → Add rule

**Rule for `main` branch:**
```yaml
Branch name pattern: main

☑️ Require a pull request before merging
   ☑️ Require approvals: 1
   ☑️ Dismiss stale pull request approvals when new commits are pushed
   
☑️ Require status checks to pass before merging
   ☑️ Require branches to be up to date before merging
   Status checks to require:
      ☑️ Backend CI (test matrix: Python 3.11, 3.12)
      ☑️ Frontend CI (build-and-test matrix: Node 20.x, 22.x)
      ☑️ Frontend CI (code-quality)
      
☑️ Require conversation resolution before merging

☑️ Do not allow bypassing the above settings
```

**Estimated Time:** 5 minutes

---

### 2. GitHub Secrets Configuration

**Path:** Settings → Secrets and variables → Actions

#### Required Secrets

| Secret Name | Description | Priority | Example |
|-------------|-------------|----------|---------|
| `CODECOV_TOKEN` | Codecov upload token | MEDIUM | Get from codecov.io |
| `NEXT_PUBLIC_API_URL` | Backend API URL for builds | HIGH | https://api.bahr.railway.app |

#### Optional Secrets

| Secret Name | Description | Use Case |
|-------------|-------------|----------|
| `SLACK_WEBHOOK` | Slack notifications | CI/CD alerts |
| `DISCORD_WEBHOOK` | Discord notifications | CI/CD alerts |
| `SENTRY_DSN` | Error tracking | Production monitoring |

**Command to add secrets:**
```bash
# Using GitHub CLI
gh secret set NEXT_PUBLIC_API_URL --body "https://your-backend.railway.app"
gh secret set CODECOV_TOKEN --body "your-token-here"
```

**Estimated Time:** 10 minutes

---

## 🔴 ACTION REQUIRED: Codecov Setup

### Step 1: Create Codecov Account

1. Visit https://codecov.io/
2. Sign up with GitHub account
3. Authorize Codecov app
4. Add BAHR repository

**Estimated Time:** 5 minutes

### Step 2: Get Upload Token

1. Go to repository settings in Codecov
2. Copy upload token
3. Add to GitHub Secrets as `CODECOV_TOKEN`

**Estimated Time:** 2 minutes

### Step 3: Configure Coverage Settings (Optional)

Create `.codecov.yml`:
```yaml
coverage:
  status:
    project:
      default:
        target: 70%
        threshold: 5%
    patch:
      default:
        target: 80%
        
comment:
  layout: "reach, diff, flags, files"
  behavior: default
```

**Estimated Time:** 5 minutes  
**Total:** ~12 minutes

---

## 🔴 ACTION REQUIRED: Railway Deployment Setup

### Step 1: Create Railway Account

1. Visit https://railway.app/
2. Sign up with GitHub account
3. Authorize Railway app

**Estimated Time:** 3 minutes

### Step 2: Create Backend Service

1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose `BAHR` repository
4. Configure:
   - **Root Directory:** `backend`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

**Estimated Time:** 5 minutes

### Step 3: Add Backend Environment Variables

In Railway backend service settings:

```bash
DATABASE_URL=postgresql://user:pass@host:5432/bahr
REDIS_URL=redis://host:6379/0
JWT_SECRET_KEY=your-secret-key-min-32-chars
ENVIRONMENT=production
CORS_ORIGINS=https://your-frontend.railway.app
ALLOWED_HOSTS=your-backend.railway.app
```

**Generate JWT Secret:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Estimated Time:** 10 minutes

### Step 4: Create PostgreSQL Database

1. In Railway project, click "New"
2. Select "Database" → "PostgreSQL"
3. Link to backend service
4. Copy `DATABASE_URL` to backend env vars

**Estimated Time:** 3 minutes

### Step 5: Create Redis Instance

1. In Railway project, click "New"
2. Select "Database" → "Redis"
3. Link to backend service
4. Copy `REDIS_URL` to backend env vars

**Estimated Time:** 3 minutes

### Step 6: Create Frontend Service

1. Click "New Service"
2. Select "Deploy from GitHub repo"
3. Choose `BAHR` repository
4. Configure:
   - **Root Directory:** `frontend`
   - **Build Command:** `npm install && npm run build`
   - **Start Command:** `npm start`

**Estimated Time:** 5 minutes

### Step 7: Add Frontend Environment Variables

In Railway frontend service settings:

```bash
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
NODE_ENV=production
```

**Estimated Time:** 2 minutes

### Step 8: Configure Custom Domains (Optional)

1. Go to service settings
2. Click "Generate Domain" or add custom domain
3. Suggested:
   - Backend: `api.bahr.app` or `bahr-api.railway.app`
   - Frontend: `bahr.app` or `bahr.railway.app`

**Estimated Time:** 5 minutes

**Total Railway Setup:** ~36 minutes

---

## 🟡 OPTIONAL: Additional Enhancements

### 1. Pre-commit Hooks (Developer Experience)

Create `.git/hooks/pre-commit`:
```bash
#!/bin/bash
echo "🔍 Running pre-commit checks..."

# Backend
if git diff --cached --name-only | grep -q "^backend/"; then
    cd backend
    black --check app || { echo "❌ Run 'black app'"; exit 1; }
    isort --check app || { echo "❌ Run 'isort app'"; exit 1; }
    flake8 app || exit 1
    cd ..
fi

# Frontend
if git diff --cached --name-only | grep -q "^frontend/"; then
    cd frontend
    npm run lint || exit 1
    npx tsc --noEmit || exit 1
    cd ..
fi

echo "✅ Pre-commit checks passed!"
```

Make executable:
```bash
chmod +x .git/hooks/pre-commit
```

**Estimated Time:** 5 minutes

---

### 2. Slack/Discord Notifications

Add to workflow files:

```yaml
- name: Notify Slack
  if: always()
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

**Estimated Time:** 10 minutes

---

### 3. Dependabot Configuration

Create `.github/dependabot.yml`:
```yaml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/backend"
    schedule:
      interval: "weekly"
      
  - package-ecosystem: "npm"
    directory: "/frontend"
    schedule:
      interval: "weekly"
      
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

**Estimated Time:** 3 minutes

---

### 4. Issue Templates

Create `.github/ISSUE_TEMPLATE/bug_report.md`:
```yaml
---
name: Bug Report
about: Report a bug
title: '[BUG] '
labels: bug
---

**Description:**
<!-- Clear description of the bug -->

**Steps to Reproduce:**
1. 
2. 
3. 

**Expected Behavior:**
<!-- What should happen -->

**Actual Behavior:**
<!-- What actually happens -->

**Environment:**
- Browser/OS:
- Version:

**Screenshots:**
<!-- If applicable -->
```

**Estimated Time:** 10 minutes

---

## 📋 Verification Checklist

After completing the setup, verify:

### Backend CI
```bash
# Make a trivial change
echo "# Test" >> backend/app/main.py

# Commit and push to develop
git add backend/app/main.py
git commit -m "test: trigger backend CI"
git push origin develop

# Watch workflow
gh run watch

# Expected: ✅ All checks pass
```

### Frontend CI
```bash
# Make a trivial change
echo "// Test" >> frontend/src/app/page.tsx

# Commit and push to develop
git add frontend/src/app/page.tsx
git commit -m "test: trigger frontend CI"
git push origin develop

# Watch workflow
gh run watch

# Expected: ✅ All checks pass
```

### Deployment
```bash
# After merging to main
git checkout main
git merge develop
git push origin main

# Watch deployment
gh run list --workflow=deploy.yml

# Expected: ✅ Deployment succeeds
# Check Railway dashboard for live services
```

### Branch Protection
```bash
# Try to push directly to main (should fail)
git checkout main
echo "test" >> README.md
git add README.md
git commit -m "test: direct push"
git push origin main

# Expected: ❌ Push rejected (branch protected)
```

---

## 📊 Success Metrics

After 1 week of use:

| Metric | Target | How to Measure |
|--------|--------|----------------|
| CI Pass Rate | > 90% | GitHub Actions insights |
| Avg CI Duration | < 5 min | Workflow run times |
| Deploy Frequency | > 5/week | Railway deploy count |
| Failed Deploys | < 10% | Railway dashboard |
| Coverage Trend | Increasing | Codecov graphs |

---

## 🆘 Troubleshooting

### CI Not Triggering

**Check:**
1. Workflow file syntax (YAML validation)
2. File paths in `on.push.paths`
3. Branch names match
4. GitHub Actions enabled in repo settings

**Fix:**
```bash
# Validate YAML
yamllint .github/workflows/*.yml

# Check GitHub Actions status
gh api repos/{owner}/{repo}/actions/permissions
```

### Deployment Failing

**Check:**
1. Railway environment variables set
2. Build logs in Railway dashboard
3. Health check endpoints working
4. Database/Redis connections

**Fix:**
1. Review Railway logs
2. Test locally with production env vars
3. Check service health endpoints
4. Verify Railway service linking

### Badge Not Updating

**Check:**
1. Badge URL matches repository
2. Workflow name matches badge
3. GitHub Actions public visibility

**Fix:**
```markdown
<!-- Correct format -->
[![Backend CI](https://github.com/USERNAME/REPO/actions/workflows/backend.yml/badge.svg)](https://github.com/USERNAME/REPO/actions/workflows/backend.yml)
```

---

## 📞 Support Resources

- **GitHub Actions:** https://docs.github.com/en/actions
- **Railway Docs:** https://docs.railway.app/
- **Codecov Docs:** https://docs.codecov.com/
- **Project Docs:** `docs/CI_CD_GUIDE.md`
- **Quick Ref:** `.github/CI_CD_QUICKREF.md`

---

## ✅ Sign-off

When all steps are complete:

- [ ] GitHub branch protection configured
- [ ] GitHub secrets added
- [ ] Codecov account created and linked
- [ ] Railway backend service deployed
- [ ] Railway frontend service deployed
- [ ] PostgreSQL database provisioned
- [ ] Redis instance provisioned
- [ ] Environment variables configured
- [ ] Custom domains configured (optional)
- [ ] All verification tests passed
- [ ] Team trained on CI/CD workflow

**Completed by:** _______________  
**Date:** _______________  
**Verified by:** _______________  

---

**Status:** 🔴 AWAITING ACTION → 🟢 READY FOR PRODUCTION
