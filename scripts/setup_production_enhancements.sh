#!/bin/bash
# Quick setup script for BAHR production enhancements

set -e  # Exit on error

echo "🚀 BAHR Production Enhancements Setup"
echo "======================================"
echo ""

# Check if virtual environment is activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "⚠️  Warning: No virtual environment detected"
    echo "   Recommended: source .venv/bin/activate"
    echo ""
    read -p "Continue without virtual environment? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Install CAMeL Tools
echo "📦 Installing CAMeL Tools..."
pip install camel-tools || {
    echo "❌ Failed to install camel-tools"
    echo "   Try: conda install -c conda-forge camel-tools"
    exit 1
}

echo ""
echo "✅ CAMeL Tools installed"

# Verify installation
echo ""
echo "🔍 Verifying CAMeL Tools..."
python -c "from camel_tools.disambig.mle import MLEDisambiguator; print('✅ Import successful')" || {
    echo "❌ CAMeL Tools import failed"
    exit 1
}

# Generate production test set
echo ""
echo "📊 Generating production-distribution test set..."
python scripts/data_processing/create_production_test_set.py || {
    echo "❌ Test set generation failed"
    exit 1
}

echo ""
echo "======================================"
echo "✅ Setup Complete!"
echo ""
echo "Next steps:"
echo "1. Run tests: pytest tests/evaluation/test_production_distribution.py -v"
echo "2. Verify hamza wasl: pytest tests/core/test_hamza_wasl_elision.py -v"
echo "3. Check accuracy targets (≥75% undiacritized, ≥97.5% diacritized)"
echo ""
echo "See docs/PRODUCTION_ENHANCEMENTS.md for full documentation"
