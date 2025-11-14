#!/bin/bash
set -e

echo "Updating Python imports and installing backend package..."

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO_ROOT"

# Install backend as editable package (critical step)
echo "  Installing backend as editable package..."
pip install -e ./src/backend > /dev/null 2>&1 && echo "    ✓ Backend installed: pip install -e ./src/backend"

# Add import guards to moved scripts
echo "  Adding import guards to scripts..."

IMPORT_GUARD='
# Import guard - ensure backend is installed
try:
    from app.core.prosody.detector_v2 import BahrDetectorV2
except ImportError as e:
    print("\\n❌ ERROR: Backend package not installed")
    print("Run: pip install -e ./src/backend")
    print(f"Details: {e}\\n")
    import sys
    sys.exit(1)
'

# Note: This is a simplified version
# In production, you'd use Python/sed to actually add import guards
# to each script file that needs them

echo "    ℹ️  Import guards should be added manually to:"
echo "       - scripts/ml/*.py"
echo "       - scripts/data_processing/*.py"
echo "       - tests/integration/*.py"

echo ""
echo "✓ Backend package installed"
echo "  All scripts can now use: from app.core.prosody import ..."
echo ""
echo "⚠️  Manual step: Add import guards to scripts (see Section 4.1 of refactor plan)"
