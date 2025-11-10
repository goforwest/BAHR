#!/usr/bin/env bash
set -euo pipefail

echo "🔧 Fixing workflow_dispatch formatting…"

for wf in .github/workflows/*.yml; do
  if grep -q "^  workflow_dispatch:$" "$wf"; then
    echo "➡️ Fixing: $wf"
    sed -i '' 's/^  workflow_dispatch:$/  workflow_dispatch: {}/' "$wf"
  fi
done

echo "✅ Done. Now commit & push:"
echo "   git add .github/workflows"
echo "   git commit -m 'Fix workflow_dispatch formatting'"
echo "   git push"
