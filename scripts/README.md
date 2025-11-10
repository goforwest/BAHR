# BAHR Scripts

Utility scripts for development, testing, and CI/CD operations.

---

## CI/CD Scripts

### `test-ci-local.sh`

**Purpose:** Run all CI checks locally before pushing to GitHub

**Usage:**
```bash
# Test only changed files (staged for commit)
./scripts/test-ci-local.sh

# Test everything (backend + frontend)
./scripts/test-ci-local.sh --all
```

**What it checks:**

**Backend:**
- ✅ Flake8 syntax and style
- ✅ Black code formatting
- ✅ isort import sorting
- ✅ mypy type checking
- ✅ pytest test suite + coverage

**Frontend:**
- ✅ ESLint code quality
- ✅ TypeScript type checking
- ✅ Prettier formatting
- ✅ Next.js production build
- ✅ Jest tests (if configured)

**Exit codes:**
- `0` - All checks passed, safe to push
- `1` - Some checks failed, fix before pushing

**Example output:**
```
════════════════════════════════════════════════════════════
   🧪 BAHR CI/CD Local Test Runner
════════════════════════════════════════════════════════════

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🐍 BACKEND CHECKS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣  Running flake8 (syntax & style)...
✅ Flake8 critical errors: PASSED
✅ Flake8 warnings: PASSED

2️⃣  Running black (code formatting)...
✅ Black formatting: PASSED

3️⃣  Running isort (import sorting)...
✅ isort: PASSED

4️⃣  Running mypy (type checking)...
✅ mypy: PASSED

5️⃣  Running pytest (test suite)...
✅ pytest: PASSED

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚛️  FRONTEND CHECKS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣  Running ESLint...
✅ ESLint: PASSED

2️⃣  Running TypeScript compiler...
✅ TypeScript: PASSED

3️⃣  Running Prettier (format check)...
✅ Prettier: PASSED

4️⃣  Running Next.js build...
✅ Next.js build: PASSED

5️⃣  Running tests...
✅ Tests: PASSED

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ✅ ALL CHECKS PASSED

  Your code is ready to push!
  CI pipeline will likely succeed.
```

**Why use this:**
- 🚀 Catch errors before pushing
- ⏱️ Faster feedback than waiting for CI
- 💰 Saves GitHub Actions minutes
- ✅ Ensures CI will pass

**Tips:**
```bash
# Add as pre-commit hook
echo "./scripts/test-ci-local.sh" > .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit

# Run in watch mode during development
watch -n 30 ./scripts/test-ci-local.sh

# Quick format fixes
cd backend && black app && isort app && cd ..
cd frontend && npm run lint -- --fix && npx prettier --write . && cd ..
```

---

## Dataset Scripts

Located in `dataset/scripts/` - see `dataset/scripts/README.md`

---

## Other Utility Scripts

### `verify_setup.sh`

**Purpose:** Verify development environment setup

**Usage:**
```bash
./verify_setup.sh
```

Checks:
- Python version and dependencies
- Node.js and npm
- Git configuration
- Required tools installed

---

## Adding New Scripts

**Guidelines:**

1. **Naming:** Use kebab-case (`my-script.sh`)
2. **Shebang:** Always start with `#!/bin/bash`
3. **Error handling:** Use `set -e` to exit on errors
4. **Documentation:** Add description to this README
5. **Permissions:** Make executable with `chmod +x`
6. **Location:**
   - General scripts: `scripts/`
   - Dataset scripts: `dataset/scripts/`
   - Backend scripts: `backend/scripts/`
   - Frontend scripts: `frontend/scripts/`

**Template:**
```bash
#!/bin/bash
# Script Name: my-script.sh
# Description: What this script does
# Usage: ./scripts/my-script.sh [options]

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Your script logic here

echo -e "${GREEN}✅ Done!${NC}"
```

---

## Contributing

When adding scripts:
1. Test thoroughly
2. Update this README
3. Add error handling
4. Include usage examples
5. Document exit codes

---

## CI/CD Integration

These scripts can be used in:
- Git hooks (pre-commit, pre-push)
- GitHub Actions workflows
- Local development
- CI/CD pipelines

Example pre-commit hook:
```bash
#!/bin/bash
# .git/hooks/pre-commit

./scripts/test-ci-local.sh || {
    echo "❌ Pre-commit checks failed"
    echo "Fix errors or use 'git commit --no-verify' to skip"
    exit 1
}
```

---

## Troubleshooting

**Script not executable:**
```bash
chmod +x scripts/test-ci-local.sh
```

**Command not found:**
```bash
# Run from project root
cd /Users/hamoudi/Desktop/Personal/BAHR
./scripts/test-ci-local.sh
```

**Backend checks fail:**
```bash
cd backend
pip install -r requirements.txt -r requirements/development.txt
```

**Frontend checks fail:**
```bash
cd frontend
npm ci
```

---

## Related Documentation

- [CI/CD Quick Reference](../.github/CI_CD_QUICKREF.md)
- [CI/CD Guide](../docs/CI_CD_GUIDE.md)
- [CI/CD Architecture](../docs/CI_CD_ARCHITECTURE.md)
- [Development Guide](../docs/START_HERE_DEVELOPER.md)
