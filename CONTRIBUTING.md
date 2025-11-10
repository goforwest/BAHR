# Contributing to BAHR - بَحْر
## دليل المساهمة في مشروع بَحْر

Thank you for considering contributing to BAHR! This document provides guidelines for contributing to the Arabic Poetry Analysis Platform.

شكراً لاهتمامك بالمساهمة في مشروع بَحْر! هذا الملف يوضح إرشادات المساهمة في منصة تحليل الشعر العربي.

---

## 📋 Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [How to Contribute](#how-to-contribute)
4. [Development Workflow](#development-workflow)
5. [Coding Standards](#coding-standards)
6. [Testing Requirements](#testing-requirements)
7. [Documentation](#documentation)
8. [Arabic Text Guidelines](#arabic-text-guidelines)
9. [Pull Request Process](#pull-request-process)
10. [Community](#community)

---

## 🤝 Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors, regardless of:
- Experience level
- Nationality or language
- Gender identity and expression
- Sexual orientation
- Disability
- Personal appearance
- Age
- Religion

### Expected Behavior

- Be respectful and considerate
- Welcome newcomers and help them get started
- Accept constructive criticism gracefully
- Focus on what's best for the community and the project
- Show empathy towards other community members

### Unacceptable Behavior

- Harassment, trolling, or discriminatory comments
- Personal attacks or derogatory language
- Publishing others' private information
- Any conduct that would be inappropriate in a professional setting

---

## 🚀 Getting Started

### Prerequisites

Before contributing, ensure you have:

- **Python 3.11+** installed
- **Node.js 18+** (for frontend contributions)
- **PostgreSQL 15+** (or use Docker)
- **Redis 7+** (or use Docker)
- **Git** for version control
- **Docker** (optional, but recommended)

### Initial Setup

1. **Fork the repository** on GitHub

2. **Clone your fork:**
   ```bash
   git clone https://github.com/YOUR-USERNAME/bahr.git
   cd bahr
   ```

3. **Add upstream remote:**
   ```bash
   git remote add upstream https://github.com/ORIGINAL-OWNER/bahr.git
   ```

4. **Set up development environment:**
   ```bash
   # Using Docker (recommended)
   docker-compose up -d

   # Or manually
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt -r requirements-dev.txt
   ```

5. **Run tests to verify setup:**
   ```bash
   cd backend
   pytest
   ```

6. **Read the documentation:**
   - Start with [`docs/START_HERE.md`](docs/START_HERE.md)
   - Review [`docs/ARCHITECTURE_OVERVIEW.md`](docs/technical/ARCHITECTURE_OVERVIEW.md)
   - Check [`docs/DEVELOPMENT_WORKFLOW.md`](docs/workflows/DEVELOPMENT_WORKFLOW.md)

---

## 💡 How to Contribute

### Types of Contributions

We welcome various types of contributions:

#### 🐛 Bug Reports
- Use the GitHub Issues tab
- Search existing issues first to avoid duplicates
- Provide detailed reproduction steps
- Include environment information (OS, Python version, etc.)
- Use the bug report template

#### ✨ Feature Requests
- Discuss in GitHub Issues before implementing
- Align with project vision (see `docs/BAHR_AI_POET_MASTER_PLAN.md`)
- Check `docs/planning/DEFERRED_FEATURES.md` for scope
- Use the feature request template

#### 📝 Documentation Improvements
- Fix typos, clarify instructions
- Add examples or use cases
- Translate documentation (Arabic ↔ English)
- Improve code comments

#### 🧪 Test Contributions
- Add test cases for edge cases
- Improve test coverage
- Add Arabic poetry test data

#### 🎨 Design Contributions
- UI/UX improvements
- Accessibility enhancements
- RTL (right-to-left) layout fixes

#### 📊 Dataset Contributions
- High-quality labeled poetry data
- Verified prosody analysis
- Classical and modern Arabic poetry

---

## 🔄 Development Workflow

### 1. Create a Branch

Create a feature branch from `develop`:

```bash
# Update your local develop branch
git checkout develop
git pull upstream develop

# Create a feature branch
git checkout -b feature/your-feature-name

# Branch naming convention:
# feature/add-mutaqarib-meter
# fix/authentication-bug
# docs/update-api-specs
# refactor/prosody-engine
# test/add-edge-cases
```

### 2. Make Your Changes

- Write clean, readable code
- Follow coding standards (see below)
- Add tests for new functionality
- Update documentation as needed
- Ensure all tests pass locally

### 3. Commit Your Changes

We use **Conventional Commits** format:

```bash
# Format: <type>(<scope>): <description>

# Examples:
git commit -m "feat(prosody): add support for al-mutaqarib meter"
git commit -m "fix(api): handle empty verse input correctly"
git commit -m "docs(readme): update installation instructions"
git commit -m "test(analyzer): add unit tests for normalization"
git commit -m "refactor(engine): simplify pattern matching logic"
```

**Commit Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style/formatting (no functional changes)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks (dependencies, build config)
- `perf`: Performance improvements

**Commit Guidelines:**
- Use present tense ("add feature" not "added feature")
- Use imperative mood ("move cursor to..." not "moves cursor to...")
- Limit first line to 72 characters
- Add detailed description if needed (after blank line)
- Reference issues: "fix(api): handle null input (#123)"

### 4. Keep Your Branch Updated

```bash
# Fetch latest changes from upstream
git fetch upstream

# Rebase your branch on latest develop
git rebase upstream/develop

# Resolve conflicts if any
# Then continue rebase
git rebase --continue

# Force push to your fork (only on your feature branch!)
git push origin feature/your-feature-name --force
```

---

## 📏 Coding Standards

### Python Code Style

We follow **PEP 8** with additional project-specific conventions:

**Formatting:**
- Use **Black** formatter (line length: 88)
- Use **flake8** for linting
- Use **mypy** for type checking

```bash
# Format code
black .

# Lint code
flake8 .

# Type check
mypy .
```

**Code Structure:**
```python
"""
Module docstring explaining purpose.

This module provides Arabic text normalization for prosody analysis.
"""

from typing import List, Dict, Optional
import logging

# Constants (UPPER_CASE)
MAX_VERSE_LENGTH = 500
DEFAULT_CONFIDENCE = 0.70

# Configure module logger
logger = logging.getLogger(__name__)


class ArabicNormalizer:
    """
    Normalizes Arabic text for prosody analysis.

    Attributes:
        preserve_diacritics (bool): Whether to keep diacritics
        alef_variants (dict): Mapping of alef variant characters

    Example:
        >>> normalizer = ArabicNormalizer()
        >>> result = normalizer.normalize("أَلَا لَيْتَ...")
        >>> print(result['normalized'])
    """

    def __init__(self, preserve_diacritics: bool = True):
        """
        Initialize normalizer.

        Args:
            preserve_diacritics: Whether to keep diacritics in output
        """
        self.preserve_diacritics = preserve_diacritics

    def normalize(self, text: str) -> Dict[str, str]:
        """
        Normalize Arabic text.

        Args:
            text: Input Arabic text

        Returns:
            Dictionary with keys:
                - original: Original text
                - normalized: Normalized text
                - no_diacritics: Text without diacritics

        Raises:
            ValueError: If text is empty or too long
        """
        if not text or len(text) > MAX_VERSE_LENGTH:
            raise ValueError(f"Text must be 1-{MAX_VERSE_LENGTH} chars")

        # Implementation...
        logger.info("Normalized text successfully")
        return {"original": text, "normalized": normalized}
```

**Naming Conventions:**
- Classes: `PascalCase`
- Functions/methods: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Private methods: `_leading_underscore`
- Type hints: Always use for function signatures

### TypeScript/React Code Style

**Formatting:**
- Use **Prettier** formatter
- Use **ESLint** for linting

```typescript
/**
 * Component for displaying verse analysis results.
 */
import React, { useState } from 'react';
import { AnalysisResult } from '@/types';

interface AnalysisCardProps {
  /** Analysis result to display */
  result: AnalysisResult;
  /** Optional callback on re-analysis */
  onReanalyze?: () => void;
}

export const AnalysisCard: React.FC<AnalysisCardProps> = ({
  result,
  onReanalyze,
}) => {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <div className="analysis-card" dir="rtl">
      <h3>{result.bahr.name_ar}</h3>
      {/* Component content */}
    </div>
  );
};
```

**Naming Conventions:**
- Components: `PascalCase`
- Hooks: `useCamelCase`
- Props interfaces: `ComponentNameProps`
- CSS classes: `kebab-case`

---

## 🧪 Testing Requirements

### Test Coverage

- **Minimum coverage:** 70% for core modules
- **Target coverage:** 80%+ for production code
- All new features **must** include tests
- Bug fixes **should** include regression tests

### Test Structure

```
backend/tests/
├── unit/              # Unit tests (80%)
│   ├── test_normalizer.py
│   ├── test_segmenter.py
│   └── test_matcher.py
├── integration/       # Integration tests (15%)
│   ├── test_api.py
│   └── test_database.py
└── e2e/              # End-to-end tests (5%)
    └── test_user_flow.py
```

### Writing Tests

```python
# tests/unit/test_normalizer.py

import pytest
from app.nlp.normalizer import ArabicNormalizer


class TestArabicNormalizer:
    """Test suite for Arabic text normalization."""

    @pytest.fixture
    def normalizer(self):
        """Provide normalizer instance for tests."""
        return ArabicNormalizer()

    def test_alef_normalization(self, normalizer):
        """Test that alef variants normalize to standard alef."""
        # Arrange
        text = "أَحْمَد"  # Alef with hamza

        # Act
        result = normalizer.normalize(text)

        # Assert
        assert 'أ' not in result['normalized']
        assert 'ا' in result['normalized']

    def test_empty_input_raises_error(self, normalizer):
        """Test that empty input raises ValueError."""
        with pytest.raises(ValueError, match="Text must be"):
            normalizer.normalize("")

    @pytest.mark.parametrize("input_text,expected", [
        ("أَلَا", "الا"),
        ("إِسْلام", "اسلام"),
        ("مَكَّة", "مكة"),
    ])
    def test_normalization_cases(self, normalizer, input_text, expected):
        """Test various normalization cases."""
        result = normalizer.normalize(input_text)
        assert result['no_diacritics'] == expected
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/unit/test_normalizer.py

# Run specific test
pytest tests/unit/test_normalizer.py::TestArabicNormalizer::test_alef_normalization

# Run with verbose output
pytest -v

# Run only fast tests (exclude slow E2E)
pytest -m "not slow"
```

---

## 📚 Documentation

### Documentation Requirements

- **All public functions** must have docstrings
- **All classes** must have class-level docstrings
- **Complex algorithms** should have inline comments
- **API changes** must update `docs/technical/API_SPECIFICATION.yaml`
- **Architecture changes** must update relevant docs

### Docstring Format

Use **Google-style** docstrings:

```python
def analyze_verse(text: str, include_explanation: bool = False) -> Dict:
    """
    Analyze a verse for prosodic structure.

    This function performs multiple steps:
    1. Normalize Arabic text
    2. Perform taqti3 (scansion)
    3. Match to known bahrs

    Args:
        text: The Arabic verse to analyze
        include_explanation: Whether to include detailed explanation

    Returns:
        Dictionary containing:
            - bahr: Identified poetic meter
            - confidence: Confidence score (0-1)
            - pattern: Taqti3 pattern

    Raises:
        ValueError: If text is empty or too long

    Example:
        >>> result = analyze_verse("أَلَا لَيْتَ...")
        >>> print(result['bahr'])
        'الطويل'
    """
```

---

## 🌐 Arabic Text Guidelines

### Working with Arabic Text

**Character Encoding:**
- Always use **UTF-8** encoding
- Test with various Arabic scripts (MSA, dialects)
- Handle diacritics correctly

**RTL (Right-to-Left) Support:**
- Use `dir="rtl"` in HTML/JSX
- Test layouts in RTL mode
- Ensure proper text alignment

**Arabic-Specific Testing:**
- Test with diacritized and non-diacritized text
- Test with various hamza forms (أ إ ؤ ئ)
- Test with alef variants (ا آ إ أ)
- Test with tanween (ً ٌ ٍ)

**Example Test Data:**
```python
# Good test cases
CLASSICAL_VERSE = "قِفَا نَبْكِ مِنْ ذِكْرَى حَبِيبٍ وَمَنْزِلِ"
MODERN_VERSE = "أنا لا أريد سماء غير سماك"
DIALECTAL_VERSE = "يا بنت يا بنت الأكابر"

# Edge cases
MIXED_SCRIPT = "Hello مرحبا 123"
ZERO_WIDTH = "test\u200Btest"  # Zero-width space
RTL_OVERRIDE = "test\u202Etest"  # RTL override (security issue)
```

---

## 🔀 Pull Request Process

### Before Submitting

- [ ] All tests pass locally
- [ ] Code is formatted (Black/Prettier)
- [ ] Linters pass (flake8/ESLint)
- [ ] Type checks pass (mypy/tsc)
- [ ] Documentation is updated
- [ ] Commit messages follow convention
- [ ] Branch is rebased on latest `develop`
- [ ] No merge conflicts

### Creating a Pull Request

1. **Push your branch to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Open a Pull Request on GitHub:**
   - Base: `develop` (not `main`)
   - Compare: `your-fork:feature/your-feature-name`
   - Use the PR template
   - Fill out all sections

3. **PR Title Format:**
   ```
   feat(prosody): add support for al-mutaqarib meter
   fix(api): handle empty verse input correctly
   docs(readme): update installation instructions
   ```

4. **PR Description Must Include:**
   - **Summary:** What does this PR do?
   - **Motivation:** Why is this change needed?
   - **Changes:** List of changes made
   - **Testing:** How was this tested?
   - **Screenshots:** If UI changes (before/after)
   - **Related Issues:** Fixes #123, Closes #456
   - **Checklist:** Completed checklist items

### Review Process

1. **Automated Checks:**
   - CI/CD pipeline runs tests
   - Code coverage checked
   - Linters validate code style

2. **Code Review:**
   - At least **1 reviewer** required
   - Address all review comments
   - Request re-review after changes

3. **Approval:**
   - Reviewer approves PR
   - No merge conflicts
   - All checks pass

4. **Merging:**
   - **Squash and merge** (for feature branches)
   - **Rebase and merge** (for hotfixes)
   - Delete branch after merge

### After Merge

- Your changes are in `develop`
- Will be deployed to staging automatically
- Will be included in next release

---

## 🌍 Community

### Getting Help

- **GitHub Issues:** Bug reports, feature requests
- **GitHub Discussions:** Questions, ideas, general discussion
- **Documentation:** Start with `docs/START_HERE.md`

### Communication Channels

- **GitHub Issues:** Primary channel for technical discussions
- **Pull Requests:** Code review and implementation discussions
- **Commit Messages:** Document changes and rationale

### Recognition

Contributors are recognized in:
- `CONTRIBUTORS.md` file
- Release notes
- Project README

---

## 📜 License

By contributing to BAHR, you agree that your contributions will be licensed under the same license as the project.

---

## 🙏 Thank You!

Every contribution, no matter how small, helps make BAHR better for the Arabic poetry community. We appreciate your time and effort!

شكراً لمساهمتك في مشروع بَحْر! 🎭

---

**Questions?** Open a GitHub Discussion or Issue labeled "question".

**First time contributing?** Look for issues labeled `good-first-issue`.

**Ready to contribute?** Start with the [Getting Started](#getting-started) guide!
