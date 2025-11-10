# 🔧 دليل تكامل مكتبات معالجة اللغة العربية
## NLP Libraries Integration & Compatibility Guide

---

## 📋 نظرة عامة

دليل تفصيلي لتكامل مكتبات NLP العربية مع حل مشاكل التوافق والأداء والترخيص.

**تم التحديث:** November 8, 2025  
**الأهمية:** حرجة - يجب قراءته قبل بدء التطوير

---

## 📦 مصفوفة التبعيات (Dependencies Matrix)

### المكتبات الأساسية للـ MVP:

```yaml
camel-tools==1.5.2:
  purpose: "Core Arabic NLP - normalization, morphology, tokenization"
  size: "~150MB"
  runtime_memory: "500MB (typical), 1GB (with morphology DB)"
  license: "MIT ✅"
  conflicts: "None known"
  python_version: ">=3.8, <3.12"
  installation_time: "2-3 minutes"
  priority: "CRITICAL - Core dependency"
  
  critical_notes: |
    - Requires download of morphology database on first use (~100MB)
    - Database caching significantly improves performance
    - Works well on ARM64 (M1/M2 Macs)

pyarabic==0.6.15:
  purpose: "Lightweight utilities - character checks, normalization"
  size: "~2MB"
  runtime_memory: "Minimal (<10MB)"
  license: "GPL v3 ⚠️"
  conflicts: "None"
  python_version: ">=3.6"
  installation_time: "<30 seconds"
  priority: "HIGH - Utility functions"
  
  critical_notes: |
    - GPL license may affect commercial use
    - Consider BSD alternative: python-arabic-reshaper
    - Pure Python - very fast for basic operations

transformers==4.35.0:
  purpose: "AraBERT models for future AI features (Phase 2+)"
  size: "~4GB (with AraBERT model)"
  runtime_memory: "2GB GPU / 8GB CPU minimum"
  license: "Apache 2.0 ✅"
  conflicts: "Requires specific torch version"
  python_version: ">=3.8"
  installation_time: "5-10 minutes + model download"
  priority: "LOW - Phase 2 only"
  
  critical_notes: |
    - DO NOT install for MVP - unnecessary overhead
    - Plan for model caching strategy before Phase 2
    - Consider quantized models for CPU inference

torch==2.1.0:
  purpose: "Required for transformers (AraBERT)"
  size: "~800MB"
  runtime_memory: "Varies by model"
  license: "BSD ✅"
  conflicts: "Platform-specific builds"
  python_version: ">=3.8"
  installation_time: "3-5 minutes"
  priority: "LOW - Phase 2 only"
  
  critical_notes: |
    - CPU-only version for MVP if needed
    - GPU support requires CUDA setup
    - M1/M2 Macs use MPS backend
```

### مكتبات مُستبعدة (مع الأسباب):

```yaml
farasa==0.0.14:
  reason_excluded: "REDUNDANT with camel-tools"
  details: |
    - CAMeL Tools provides better segmentation accuracy
    - Adds 200MB+ unnecessary dependency
    - Potential version conflicts with camel-tools
    - Maintenance burden (last update 2019)
  
  when_to_use: "Only if you specifically need NER (Named Entity Recognition)"
  alternative: "Use camel-tools for all segmentation/tokenization"

arabic-reshaper + python-bidi:
  reason_excluded: "Not needed - handled by frontend"
  details: |
    - RTL rendering is frontend responsibility
    - Backend should store/process text as-is
    - Adds complexity without benefit
  
  when_to_use: "Only for PDF/image generation with Arabic text"
```

---

## 🔧 Installation Strategy

### Step 1: Virtual Environment Setup

```bash
# Using Poetry (RECOMMENDED for production)
cd backend
poetry init --name bahr-backend --python "^3.11"
poetry add camel-tools==1.5.2
poetry add pyarabic==0.6.15
poetry add fastapi[all]==0.104.1
poetry add sqlalchemy==2.0.23
poetry add alembic==1.12.1

# Using pip + requirements.txt (Alternative)
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements/base.txt
```

### Step 2: Platform-Specific Installation

#### macOS Intel (x86_64):
```bash
# Standard installation
pip install camel-tools==1.5.2
```

#### macOS Apple Silicon (M1/M2/M3):
```bash
# Install with ARM64 native support
arch -arm64 pip install camel-tools==1.5.2

# If issues occur, use Rosetta (slower but more compatible)
arch -x86_64 pip install camel-tools==1.5.2

# Verify installation
python -c "from camel_tools.utils.normalize import normalize_unicode; print('✅ CAMeL Tools working')"
```

#### Docker (Production):
```dockerfile
# Dockerfile for multi-platform support
FROM --platform=linux/amd64 python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements/base.txt .
RUN pip install --no-cache-dir -r base.txt

# Download CAMeL Tools databases (do once in build)
RUN python -c "from camel_tools.morphology.database import MorphologyDB; MorphologyDB.builtin_db()"
```

### Step 3: Verify Installation

```python
# scripts/verify_nlp_setup.py
"""Verify all NLP libraries are correctly installed"""

def verify_camel_tools():
    try:
        from camel_tools.utils.normalize import normalize_unicode
        from camel_tools.morphology.database import MorphologyDB
        
        # Test normalization
        text = "أَلَا في سَبيلِ المَجدِ"
        normalized = normalize_unicode(text)
        
        # Test morphology DB (this triggers download if needed)
        db = MorphologyDB.builtin_db()
        
        print("✅ CAMeL Tools: OK")
        return True
    except Exception as e:
        print(f"❌ CAMeL Tools: FAILED - {e}")
        return False

def verify_pyarabic():
    try:
        import pyarabic.araby as araby
        
        # Test basic function
        text = "السلام عليكم"
        is_arabic = araby.is_arabicstring(text)
        
        print("✅ PyArabic: OK")
        return True
    except Exception as e:
        print(f"❌ PyArabic: FAILED - {e}")
        return False

def check_memory_usage():
    import psutil
    import os
    
    process = psutil.Process(os.getpid())
    memory_mb = process.memory_info().rss / 1024 / 1024
    
    print(f"📊 Current memory usage: {memory_mb:.1f} MB")
    
    if memory_mb > 2000:
        print("⚠️  Warning: High memory usage detected")
    
    return memory_mb

if __name__ == "__main__":
    print("🔍 Verifying NLP Setup...\n")
    
    camel_ok = verify_camel_tools()
    pyarabic_ok = verify_pyarabic()
    memory = check_memory_usage()
    
    if camel_ok and pyarabic_ok:
        print("\n✅ All NLP libraries verified successfully!")
    else:
        print("\n❌ Some libraries failed verification. Check errors above.")
```

---

## ⚠️ Known Issues & Solutions

### Issue 1: CAMeL Tools Database Download Failures

**Symptom:**
```
RuntimeError: Failed to download morphology database
ConnectionError: [Errno 60] Operation timed out
```

**Solutions:**
```bash
# Solution 1: Manual download
cd ~/.camel_tools
wget https://github.com/CAMeL-Lab/camel_morph/releases/download/v1.0/calima-msa-s31.tar.bz2
tar -xjf calima-msa-s31.tar.bz2

# Solution 2: Use local copy
from camel_tools.morphology.database import MorphologyDB
db = MorphologyDB('/path/to/local/db', 'calima-msa-s31')

# Solution 3: Pre-download in Docker build
RUN python -c "from camel_tools.morphology.database import MorphologyDB; MorphologyDB.builtin_db()"
```

### Issue 2: PyArabic GPL License Conflict

**Problem:** GPL v3 is copyleft - may affect your project license

**Solutions:**
```python
# Option 1: Keep PyArabic for development, reimplement critical functions
# app/core/utils/arabic_utils.py
def is_arabic_char(char: str) -> bool:
    """Reimplemented to avoid GPL dependency in production"""
    return '\u0600' <= char <= '\u06FF'

def remove_diacritics(text: str) -> str:
    """Reimplemented basic diacritic removal"""
    diacritics = 'َُِّْ'  # Common diacritics
    return ''.join(c for c in text if c not in diacritics)

# Option 2: Use arabic-reshaper (BSD license)
# pip install arabic-reshaper  # BSD license
```

### Issue 3: Memory Leaks with MorphologyDB

**Symptom:** Memory grows over time when analyzing many texts

**Solution:**
```python
# app/core/nlp/analyzer_pool.py
from camel_tools.morphology.database import MorphologyDB
from camel_tools.morphology.analyzer import Analyzer

class AnalyzerPool:
    """Shared analyzer instance to prevent memory leaks"""
    
    _db = None
    _analyzer = None
    
    @classmethod
    def get_analyzer(cls):
        if cls._analyzer is None:
            cls._db = MorphologyDB.builtin_db()
            cls._analyzer = Analyzer(cls._db)
        return cls._analyzer
    
    @classmethod
    def cleanup(cls):
        """Call on application shutdown"""
        cls._analyzer = None
        cls._db = None

# Use in FastAPI lifespan
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    AnalyzerPool.get_analyzer()  # Warm up
    yield
    # Shutdown
    AnalyzerPool.cleanup()
```

---

## 📊 Performance Benchmarks

### Initialization Times (First Run):

```
CAMeL Tools Database Download: 30-60 seconds (one-time)
CAMeL Tools Import: 2-3 seconds
PyArabic Import: <0.1 seconds
MorphologyDB Load: 1-2 seconds
Analyzer Creation: 0.5-1 second
```

### Runtime Performance (per text):

```
Text Normalization (CAMeL): 1-5ms per 100 words
Character Checks (PyArabic): <1ms per 100 words
Morphological Analysis: 10-50ms per word
Tokenization: 2-10ms per sentence
```

### Memory Footprint:

```
Base Python Process: ~50MB
+ CAMeL Tools Import: +100MB
+ MorphologyDB Loaded: +400MB
+ Active Analysis: +50-100MB per concurrent request
---
Total MVP Expected: 600-800MB backend process
```

---

## 🔄 Dependency Update Strategy

### Version Pinning:

```toml
# pyproject.toml (Poetry)
[tool.poetry.dependencies]
python = "^3.11"
camel-tools = "1.5.2"  # Pin exact version
pyarabic = "^0.6.15"   # Allow patch updates
fastapi = "^0.104.1"   # Allow minor updates

[tool.poetry.dev-dependencies]
pytest = "^7.4.0"
black = "^23.10.0"
```

```txt
# requirements/base.txt (pip)
camel-tools==1.5.2
pyarabic>=0.6.15,<0.7.0
fastapi>=0.104.1,<0.105.0
```

### Update Schedule:

```yaml
Weekly:
  - Check for security updates: pip-audit
  - Review dependency alerts: GitHub Dependabot

Monthly:
  - Test patch version updates in staging
  - Update dev dependencies

Quarterly:
  - Evaluate minor version upgrades
  - Plan migration for breaking changes

Yearly:
  - Major version review
  - Consider alternative libraries
```

---

## 🧪 Testing NLP Integration

```python
# tests/test_nlp_integration.py
import pytest
from app.core.nlp.normalizer import ArabicNormalizer

class TestCAMeLIntegration:
    def test_normalize_unicode(self):
        normalizer = ArabicNormalizer()
        text = "أَلَا في سَبيلِ المَجدِ"
        result = normalizer.normalize(text)
        
        assert result is not None
        assert len(result) > 0
        assert "ا" in result  # Normalized alef
    
    def test_handling_edge_cases(self):
        normalizer = ArabicNormalizer()
        
        # Empty string
        assert normalizer.normalize("") == ""
        
        # Non-Arabic text
        result = normalizer.normalize("Hello World")
        assert result == "Hello World"
        
        # Mixed text
        result = normalizer.normalize("مرحبا Hello")
        assert "مرحبا" in result

@pytest.mark.performance
class TestPerformance:
    def test_normalization_speed(self, benchmark):
        normalizer = ArabicNormalizer()
        text = "هذا نص طويل " * 100  # 200 words
        
        result = benchmark(normalizer.normalize, text)
        
        # Should complete in < 50ms
        assert benchmark.stats['mean'] < 0.05
```

---

## 📝 Troubleshooting Checklist

```markdown
Problem: Import errors after installation
□ Check Python version: python --version (should be 3.11+)
□ Verify virtual environment is activated
□ Clear pip cache: pip cache purge
□ Reinstall: pip install --force-reinstall camel-tools

Problem: Slow performance
□ Check if MorphologyDB is being reloaded (use singleton)
□ Verify caching is enabled
□ Monitor memory usage: top / htop
□ Profile with: python -m cProfile script.py

Problem: Unicode errors
□ Ensure files are UTF-8: file -I filename.py
□ Set environment: export LANG=en_US.UTF-8
□ Check database encoding: SHOW SERVER_ENCODING;

Problem: Docker build failures
□ Use --platform=linux/amd64 for consistency
□ Increase Docker memory limit (>4GB)
□ Check network connectivity for downloads
□ Use multi-stage builds to reduce image size
```

---

## 🎯 Best Practices Summary

✅ **DO:**
- Pin camel-tools to exact version (1.5.2)
- Use singleton pattern for MorphologyDB
- Implement caching for repeated analyses
- Test on target deployment platform
- Monitor memory usage in production

❌ **DON'T:**
- Install farasa unless absolutely needed
- Load MorphologyDB per request
- Use GPL libraries without license review
- Upgrade dependencies without testing
- Ignore platform-specific builds

---

## 📚 Additional Resources

- [CAMeL Tools Documentation](https://camel-tools.readthedocs.io/)
- [PyArabic GitHub](https://github.com/linuxscout/pyarabic)
- [Arabic NLP Resources](https://github.com/topics/arabic-nlp)
- [Hugging Face Arabic Models](https://huggingface.co/models?language=ar)

---

**Last Updated:** November 8, 2025  
**Next Review:** Week 4 (after initial integration testing)
