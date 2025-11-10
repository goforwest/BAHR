# CI/CD Quick Reference

## Pre-Commit Checklist

### Automated Local Testing

**Run all CI checks locally before pushing:**
```bash
# From project root
./scripts/test-ci-local.sh

# Test everything (even if no changes)
./scripts/test-ci-local.sh --all
```

This script runs the same checks as GitHub Actions:
- Backend: flake8, black, isort, mypy, pytest
- Frontend: ESLint, TypeScript, Prettier, build

### Backend Changes
```bash
# Navigate to backend
cd backend

# Run all checks
black app                                    # Format code
isort app                                    # Sort imports  
flake8 app                                   # Lint
mypy app --ignore-missing-imports            # Type check
pytest tests/ -v --cov=app                   # Test with coverage
```

### Frontend Changes
```bash
# Navigate to frontend
cd frontend

# Run all checks
npx prettier --write "src/**/*.{ts,tsx}"     # Format
npm run lint -- --fix                        # Lint & fix
npx tsc --noEmit                            # Type check
npm run build                                # Build
```

---

## Common Commands

### Check CI Status
```bash
# View workflow runs
gh run list

# Watch latest run
gh run watch

# View specific workflow
gh run view <run-id>
```

### Manual Deployment
```bash
# Trigger deploy workflow
gh workflow run deploy.yml

# View deployment status
gh run list --workflow=deploy.yml
```

### Fix Common Issues

**Backend:**
```bash
# Auto-fix formatting
black app && isort app

# Run tests locally
pytest tests/ -v

# Check coverage
pytest tests/ --cov=app --cov-report=html
open htmlcov/index.html
```

**Frontend:**
```bash
# Auto-fix everything
npx prettier --write . && npm run lint -- --fix

# Clean build
rm -rf .next node_modules
npm install
npm run build
```

---

## GitHub Actions Status

| Workflow | Badge | Purpose |
|----------|-------|---------|
| Backend CI | ![Backend CI](https://github.com/goforwest/BAHR/actions/workflows/backend.yml/badge.svg) | Tests, lint, type-check |
| Frontend CI | ![Frontend CI](https://github.com/goforwest/BAHR/actions/workflows/frontend.yml/badge.svg) | Build, lint, type-check |
| Deploy | ![Deploy](https://github.com/goforwest/BAHR/actions/workflows/deploy.yml/badge.svg) | Production deployment |

---

## Railway Deployment

### Backend
- **Auto-deploy:** Push to `main` branch
- **Manual deploy:** Railway dashboard
- **Logs:** `railway logs --service=backend`

### Frontend  
- **Auto-deploy:** Push to `main` branch
- **Manual deploy:** Railway dashboard
- **Logs:** `railway logs --service=frontend`

---

## Troubleshooting

### "CI failed but works locally"

1. **Check Python/Node version:**
   ```bash
   # Backend
   python --version  # Should be 3.11 or 3.12
   
   # Frontend
   node --version    # Should be 20.x or 22.x
   ```

2. **Clear caches:**
   ```bash
   # Backend
   pip cache purge
   rm -rf __pycache__ .pytest_cache
   
   # Frontend
   npm cache clean --force
   rm -rf .next node_modules
   ```

3. **Check dependencies:**
   ```bash
   # Backend
   pip install -r requirements.txt -r requirements/development.txt
   
   # Frontend
   npm ci  # Use ci instead of install
   ```

### "Deploy failed"

1. Check Railway logs
2. Verify environment variables are set
3. Check health endpoint returns 200
4. Review build logs for errors

---

## Best Practices

✅ **DO:**
- Run pre-commit checks before pushing
- Write tests for new features
- Keep commits small and focused
- Update documentation with code changes
- Use feature branches for development

❌ **DON'T:**
- Push directly to `main` (use PRs)
- Skip tests or linting
- Commit broken code
- Merge failing PRs
- Ignore CI failures

---

## Git Hooks (Optional)

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash

echo "Running pre-commit checks..."

# Backend checks
if git diff --cached --name-only | grep -q "^backend/"; then
    echo "→ Checking backend..."
    cd backend
    black --check app || exit 1
    isort --check-only app || exit 1
    flake8 app || exit 1
    pytest tests/ -v || exit 1
    cd ..
fi

# Frontend checks  
if git diff --cached --name-only | grep -q "^frontend/"; then
    echo "→ Checking frontend..."
    cd frontend
    npm run lint || exit 1
    npx tsc --noEmit || exit 1
    cd ..
fi

echo "✅ All checks passed!"
```

Make executable:
```bash
chmod +x .git/hooks/pre-commit
```

---

## Environment Variables Reference

### Backend (Railway)
```env
DATABASE_URL=postgresql://user:pass@host:5432/bahr
REDIS_URL=redis://host:6379
JWT_SECRET_KEY=your-secret-key-here
ENVIRONMENT=production
CORS_ORIGINS=https://your-frontend.railway.app
```

### Frontend (Railway)
```env
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
NODE_ENV=production
```

---

## Contact & Support

- **CI/CD Issues:** Check GitHub Actions logs
- **Deployment Issues:** Check Railway dashboard
- **Code Issues:** Create an issue on GitHub

For detailed documentation, see [CI_CD_GUIDE.md](./CI_CD_GUIDE.md)
