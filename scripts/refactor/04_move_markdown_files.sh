#!/bin/bash
set -e

echo "Moving Markdown files from root to docs/ and archive/..."

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO_ROOT"

# Create target directories
mkdir -p archive/phases
mkdir -p archive/sessions
mkdir -p archive/announcements
mkdir -p docs/deployment
mkdir -p docs/api
mkdir -p docs/specifications
mkdir -p docs/research
mkdir -p docs/internal
mkdir -p docs/checklists
mkdir -p docs/planning
mkdir -p docs/technical
mkdir -p docs/reports
mkdir -p docs/troubleshooting

echo "  Moving Phase files..."
for file in PHASE_*.md; do
    if [[ -f "$file" ]]; then
        git mv "$file" "archive/phases/$file"
        echo "    ✓ $file → archive/phases/"
    fi
done

echo "  Moving Session summaries..."
for file in SESSION_SUMMARY*.md; do
    if [[ -f "$file" ]]; then
        git mv "$file" "archive/sessions/$file"
        echo "    ✓ $file → archive/sessions/"
    fi
done

echo "  Moving deployment docs..."
[[ -f "RAILWAY_DEPLOYMENT_GUIDE.md" ]] && git mv "RAILWAY_DEPLOYMENT_GUIDE.md" "docs/deployment/" && echo "    ✓ RAILWAY_DEPLOYMENT_GUIDE.md"
[[ -f "QUICK_REFERENCE_RAILWAY.md" ]] && git mv "QUICK_REFERENCE_RAILWAY.md" "docs/deployment/" && echo "    ✓ QUICK_REFERENCE_RAILWAY.md"

echo "  Moving API docs..."
[[ -f "API_V2_USER_GUIDE.md" ]] && git mv "API_V2_USER_GUIDE.md" "docs/api/" && echo "    ✓ API_V2_USER_GUIDE.md"
[[ -f "API_V2_100_PERCENT_ACCURACY_GUIDE.md" ]] && git mv "API_V2_100_PERCENT_ACCURACY_GUIDE.md" "docs/api/" && echo "    ✓ API_V2_100_PERCENT_ACCURACY_GUIDE.md"

echo "  Moving specifications..."
[[ -f "PATTERN_NORMALIZATION_SPEC.md" ]] && git mv "PATTERN_NORMALIZATION_SPEC.md" "docs/specifications/" && echo "    ✓ PATTERN_NORMALIZATION_SPEC.md"
[[ -f "UI_MULTI_CANDIDATE_SPEC.md" ]] && git mv "UI_MULTI_CANDIDATE_SPEC.md" "docs/specifications/" && echo "    ✓ UI_MULTI_CANDIDATE_SPEC.md"

echo "  Moving research docs..."
[[ -f "ARABIC_PROSODY_ML_DATASET_BLUEPRINT.md" ]] && git mv "ARABIC_PROSODY_ML_DATASET_BLUEPRINT.md" "docs/research/" && echo "    ✓ ARABIC_PROSODY_ML_DATASET_BLUEPRINT.md"
[[ -f "HUGGINGFACE_DATASET_CARD.md" ]] && git mv "HUGGINGFACE_DATASET_CARD.md" "docs/research/" && echo "    ✓ HUGGINGFACE_DATASET_CARD.md"
[[ -f "DATASET_EXPANSION_PROMPT.md" ]] && git mv "DATASET_EXPANSION_PROMPT.md" "docs/research/" && echo "    ✓ DATASET_EXPANSION_PROMPT.md"
[[ -f "METER_DETECTION_INVESTIGATION.md" ]] && git mv "METER_DETECTION_INVESTIGATION.md" "docs/research/" && echo "    ✓ METER_DETECTION_INVESTIGATION.md"
[[ -f "mutadarik_sourcing_report.md" ]] && git mv "mutadarik_sourcing_report.md" "docs/research/" && echo "    ✓ mutadarik_sourcing_report.md"
[[ -f "mutadarik_summary_table.md" ]] && git mv "mutadarik_summary_table.md" "docs/research/" && echo "    ✓ mutadarik_summary_table.md"

echo "  Moving internal docs..."
[[ -f "AI_PROMPT_CORPUS_SOURCING.md" ]] && git mv "AI_PROMPT_CORPUS_SOURCING.md" "docs/internal/" && echo "    ✓ AI_PROMPT_CORPUS_SOURCING.md"
[[ -f "AI_PROMPT_QUICK_VERSION.md" ]] && git mv "AI_PROMPT_QUICK_VERSION.md" "docs/internal/" && echo "    ✓ AI_PROMPT_QUICK_VERSION.md"
[[ -f "PROMPT_FOR_AI.md" ]] && git mv "PROMPT_FOR_AI.md" "docs/internal/" && echo "    ✓ PROMPT_FOR_AI.md"

echo "  Moving checklists..."
[[ -f "TESTING_CHECKLIST.md" ]] && git mv "TESTING_CHECKLIST.md" "docs/checklists/" && echo "    ✓ TESTING_CHECKLIST.md"

echo "  Moving planning docs..."
[[ -f "README_ROADMAP.md" ]] && git mv "README_ROADMAP.md" "docs/planning/" && echo "    ✓ README_ROADMAP.md"
[[ -f "ROADMAP_TO_100_PERCENT_ACCURACY.md" ]] && git mv "ROADMAP_TO_100_PERCENT_ACCURACY.md" "docs/planning/" && echo "    ✓ ROADMAP_TO_100_PERCENT_ACCURACY.md"

echo "  Moving technical docs..."
[[ -f "DETECTOR_V2_SUMMARY.md" ]] && git mv "DETECTOR_V2_SUMMARY.md" "docs/technical/" && echo "    ✓ DETECTOR_V2_SUMMARY.md"
[[ -f "HYBRID_DETECTOR_ANALYSIS.md" ]] && git mv "HYBRID_DETECTOR_ANALYSIS.md" "docs/technical/" && echo "    ✓ HYBRID_DETECTOR_ANALYSIS.md"
[[ -f "IMPLEMENTATION_SUMMARY.md" ]] && git mv "IMPLEMENTATION_SUMMARY.md" "docs/technical/" && echo "    ✓ IMPLEMENTATION_SUMMARY.md"
[[ -f "ML_INTEGRATION_COMPLETE.md" ]] && git mv "ML_INTEGRATION_COMPLETE.md" "docs/technical/" && echo "    ✓ ML_INTEGRATION_COMPLETE.md"
[[ -f "ML_PIPELINE_IMPLEMENTATION_SUMMARY.md" ]] && git mv "ML_PIPELINE_IMPLEMENTATION_SUMMARY.md" "docs/technical/" && echo "    ✓ ML_PIPELINE_IMPLEMENTATION_SUMMARY.md"

echo "  Moving reports..."
[[ -f "DATA_AUGMENTATION_SUCCESS_REPORT.md" ]] && git mv "DATA_AUGMENTATION_SUCCESS_REPORT.md" "docs/reports/" && echo "    ✓ DATA_AUGMENTATION_SUCCESS_REPORT.md"
[[ -f "OPTION_A_SUCCESS_REPORT.md" ]] && git mv "OPTION_A_SUCCESS_REPORT.md" "docs/reports/" && echo "    ✓ OPTION_A_SUCCESS_REPORT.md"
[[ -f "CORPUS_COMPLETE_SUMMARY.md" ]] && git mv "CORPUS_COMPLETE_SUMMARY.md" "docs/reports/" && echo "    ✓ CORPUS_COMPLETE_SUMMARY.md"
[[ -f "DATASET_COLLECTION_COMPLETE.md" ]] && git mv "DATASET_COLLECTION_COMPLETE.md" "docs/reports/" && echo "    ✓ DATASET_COLLECTION_COMPLETE.md"
[[ -f "GOLDEN_SET_COVERAGE_ANALYSIS.md" ]] && git mv "GOLDEN_SET_COVERAGE_ANALYSIS.md" "docs/reports/" && echo "    ✓ GOLDEN_SET_COVERAGE_ANALYSIS.md"
[[ -f "GOLDEN_SET_EXPANSION_SUMMARY.md" ]] && git mv "GOLDEN_SET_EXPANSION_SUMMARY.md" "docs/reports/" && echo "    ✓ GOLDEN_SET_EXPANSION_SUMMARY.md"
[[ -f "CRITICAL_FINDINGS.md" ]] && git mv "CRITICAL_FINDINGS.md" "docs/reports/" && echo "    ✓ CRITICAL_FINDINGS.md"
[[ -f "PATH_TO_100_PERCENT.md" ]] && git mv "PATH_TO_100_PERCENT.md" "docs/reports/" && echo "    ✓ PATH_TO_100_PERCENT.md"
[[ -f "PHONETIC_CONVERSION_BUG_FIX_ATTEMPT.md" ]] && git mv "PHONETIC_CONVERSION_BUG_FIX_ATTEMPT.md" "docs/reports/" && echo "    ✓ PHONETIC_CONVERSION_BUG_FIX_ATTEMPT.md"

echo "  Moving troubleshooting docs..."
[[ -f "DOCKER_OPTIMIZATION_ISSUE.md" ]] && git mv "DOCKER_OPTIMIZATION_ISSUE.md" "docs/troubleshooting/" && echo "    ✓ DOCKER_OPTIMIZATION_ISSUE.md"

echo "  Moving archive docs..."
[[ -f "ANNOUNCEMENT.md" ]] && git mv "ANNOUNCEMENT.md" "archive/announcements/" && echo "    ✓ ANNOUNCEMENT.md"
[[ -f "PULL_REQUEST.md" ]] && git mv "PULL_REQUEST.md" "archive/" && echo "    ✓ PULL_REQUEST.md"

echo ""
echo "✓ Markdown files organized"
echo "  Note: Refactor-related docs (REFACTOR_*.md, CRITICAL_FIXES*.md) kept in root"
