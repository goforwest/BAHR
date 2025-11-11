#!/usr/bin/env bash
set -euo pipefail

OWNER="goforwest"
REPO="BAHR"
BRANCH="main"
TMP=$(mktemp)

echo "🔧 Fetching workflow list…"
workflow_names=$(gh api repos/$OWNER/$REPO/actions/workflows --jq '.workflows[].name')

echo "📋 Workflows detected:"
echo "$workflow_names"
echo ""

# Convert workflow names → JSON array
contexts=$(echo "$workflow_names" | jq -R . | jq -s .)

echo "🔧 Applying LEGACY branch protection API"

json_payload=$(jq -n \
  --argjson contexts "$contexts" \
  '
  {
    required_status_checks: {
      strict: true,
      contexts: $contexts
    },
    enforce_admins: true,
    required_pull_request_reviews: {
      dismiss_stale_reviews: true,
      required_approving_review_count: 1
    },
    restrictions: null
  }
')

echo "📤 Sending branch protection rule…"

echo "$json_payload" | gh api \
  --method PUT \
  -H "Accept: application/vnd.github+json" \
  -H "Content-Type: application/json" \
  "repos/goforwest/BAHR/branches/main/protection" \
  --input -

echo ""
echo "🎉 SUCCESS!"
echo "✅ Legacy branch protection is now active."
echo "✅ This repo does NOT support Ruleset API — using correct API instead."
