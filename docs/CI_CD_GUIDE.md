# CI/CD Pipeline Documentation

## Overview

BAHR uses GitHub Actions for Continuous Integration and Continuous Deployment (CI/CD), with automatic deployments to Railway on successful builds.

## Workflows

### 1. Backend CI (`backend.yml`)

**Triggers:**
- Push to `main` or `develop` branches (backend changes)
- Pull requests to `main` or `develop` (backend changes)

**Jobs:**

#### Test Matrix
- Runs on Python 3.11 and 3.12
- Ubuntu latest

**Steps:**
1. **Checkout code** - Clone repository
2. **Setup Python** - Configure Python environment with pip caching
3. **Install dependencies** - Install backend requirements
4. **Lint with flake8** - Check for syntax errors and code quality
5. **Format check with black** - Ensure consistent code formatting
6. **Import sorting with isort** - Verify import organization
7. **Type check with mypy** - Static type checking
8. **Run pytest** - Execute test suite with coverage
9. **Upload coverage** - Send coverage report to Codecov

**Quality Gates:**
- ✅ No syntax errors (flake8 E9, F63, F7, F82)
- ✅ Code formatted with black
- ✅ Imports sorted with isort
- ✅ All tests passing
- ✅ Type hints validated (warnings only)

---

### 2. Frontend CI (`frontend.yml`)

**Triggers:**
- Push to `main` or `develop` branches (frontend changes)
- Pull requests to `main` or `develop` (frontend changes)

**Jobs:**

#### Build and Test Matrix
- Runs on Node.js 20.x and 22.x
- Ubuntu latest

**Steps:**
1. **Checkout code** - Clone repository
2. **Setup Node.js** - Configure Node with npm caching
3. **Install dependencies** - Run `npm ci`
4. **Lint with ESLint** - Check TypeScript/React code
5. **Type check** - Run `tsc --noEmit`
6. **Build Next.js** - Full production build
7. **Run tests** - Execute Jest tests (if configured)

#### Code Quality Job
1. **Prettier check** - Verify code formatting

**Quality Gates:**
- ✅ ESLint passes (no errors)
- ✅ TypeScript compilation succeeds
- ✅ Production build completes
- ✅ Code formatted with Prettier
- ✅ All tests passing

---

### 3. Deploy Workflow (`deploy.yml`)

**Triggers:**
- Push to `main` branch
- Manual trigger via workflow_dispatch

**Jobs:**

#### Deploy Backend
- Triggers Railway backend deployment
- Runs in production environment

#### Deploy Frontend
- Triggers Railway frontend deployment
- Runs in production environment

#### Deployment Summary
- Reports overall deployment status

**Note:** Railway automatically deploys when changes are pushed to main. This workflow provides visibility and manual trigger capability.

---

## Railway Configuration

### Backend Service

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

**Environment Variables Required:**
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `JWT_SECRET_KEY` - Secret for JWT tokens
- `ENVIRONMENT` - Set to `production`

**Healthcheck:**
- Path: `/health`
- Timeout: 300s

### Frontend Service

**Build Command:**
```bash
npm install && npm run build
```

**Start Command:**
```bash
npm start
```

**Environment Variables Required:**
- `NEXT_PUBLIC_API_URL` - Backend API URL
- `NODE_ENV` - Set to `production`

**Healthcheck:**
- Path: `/`
- Timeout: 300s

---

## Status Badges

Add these badges to your README to show CI/CD status:

```markdown
[![Backend CI](https://github.com/goforwest/BAHR/actions/workflows/backend.yml/badge.svg)](https://github.com/goforwest/BAHR/actions/workflows/backend.yml)
[![Frontend CI](https://github.com/goforwest/BAHR/actions/workflows/frontend.yml/badge.svg)](https://github.com/goforwest/BAHR/actions/workflows/frontend.yml)
[![Deploy](https://github.com/goforwest/BAHR/actions/workflows/deploy.yml/badge.svg)](https://github.com/goforwest/BAHR/actions/workflows/deploy.yml)
```

---

## Development Workflow

### Branch Strategy

1. **main** - Production branch (auto-deploys to Railway)
2. **develop** - Development branch (runs CI, no deploy)
3. **feature/** - Feature branches (CI on PR)

### Recommended Flow

1. Create feature branch from `develop`
2. Make changes and commit
3. Push to GitHub - triggers CI checks
4. Create PR to `develop` - runs full CI suite
5. Merge to `develop` after approval
6. Create PR from `develop` to `main`
7. Merge to `main` - triggers CI + deployment

---

## Local Development

### Backend Testing

```bash
cd backend

# Run linting
flake8 app
black --check app
isort --check-only app
mypy app

# Run tests with coverage
pytest tests/ -v --cov=app --cov-report=term-missing
```

### Frontend Testing

```bash
cd frontend

# Run linting
npm run lint

# Type check
npx tsc --noEmit

# Format check
npx prettier --check "src/**/*.{ts,tsx,js,jsx,json,css,md}"

# Build
npm run build
```

---

## Troubleshooting

### Backend CI Failures

**Flake8 errors:**
- Fix syntax errors immediately
- Adjust line length if needed (max 127 chars)
- Address undefined names

**Black formatting:**
```bash
black app  # Auto-format
```

**Import sorting:**
```bash
isort app  # Auto-sort imports
```

**Test failures:**
- Check test logs in GitHub Actions
- Run tests locally first
- Verify database setup in tests

### Frontend CI Failures

**ESLint errors:**
```bash
npm run lint -- --fix  # Auto-fix where possible
```

**TypeScript errors:**
- Fix type errors in IDE
- Run `npx tsc --noEmit` locally

**Build failures:**
- Check build logs
- Verify environment variables
- Test build locally

**Prettier formatting:**
```bash
npx prettier --write "src/**/*.{ts,tsx,js,jsx,json,css,md}"
```

---

## Performance Optimization

### Caching Strategy

Both workflows use caching to speed up builds:

**Backend:**
- pip dependencies cached by `setup-python@v5`
- Cache key based on `requirements.txt`

**Frontend:**
- npm dependencies cached by `setup-node@v4`
- Cache key based on `package-lock.json`

### Matrix Strategy

- Backend tests on Python 3.11 and 3.12
- Frontend tests on Node 20.x and 22.x
- Ensures compatibility across versions

---

## Security

### Secrets Management

Store sensitive values in GitHub Secrets:

1. Go to repository **Settings** → **Secrets and variables** → **Actions**
2. Add secrets:
   - `NEXT_PUBLIC_API_URL`
   - Railway tokens (if using Railway CLI)
   - Codecov token (optional)

### Environment Protection

The `deploy.yml` workflow uses GitHub environment protection:
- Requires manual approval (optional)
- Environment-specific secrets
- Deployment logs and history

---

## Monitoring

### GitHub Actions Dashboard

View workflow runs at:
```
https://github.com/goforwest/BAHR/actions
```

### Railway Dashboard

Monitor deployments at:
```
https://railway.app/dashboard
```

### Coverage Reports

View coverage at:
```
https://codecov.io/gh/goforwest/BAHR
```

---

## Next Steps

- [ ] Set up Codecov account and add token
- [ ] Configure Railway environment variables
- [ ] Link Railway services to GitHub repository
- [ ] Set up branch protection rules
- [ ] Configure PR required checks
- [ ] Add deployment notifications (Slack/Discord)
- [ ] Set up performance monitoring
- [ ] Configure error tracking (Sentry)

---

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Railway Documentation](https://docs.railway.app/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Next.js Deployment](https://nextjs.org/docs/deployment)
