# =============================================================================
# BAHR - Railway Optimized Production Dockerfile
# Target: < 3.5 GB final image (Railway limit: 4 GB)
# Optimizations: CPU-only PyTorch, aggressive cleanup, multi-stage build
# =============================================================================

# =============================================================================
# Stage 1: Builder - Install dependencies only
# =============================================================================
FROM python:3.11-slim-bookworm AS builder

# Prevent Python from writing pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install ONLY build dependencies needed for Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy ONLY requirements files (not entire project)
COPY requirements/base.txt requirements/production.txt ./requirements/
COPY requirements.txt ./

# Install Python dependencies to /install directory
RUN set -ex && \
    pip install --upgrade pip setuptools wheel && \
    # Install all requirements to /usr/local first (default location)
    pip install -r requirements/production.txt && \
    # Verify packages are installed and importable
    python -c "import uvicorn, fastapi, torch; print(f'✓ Installed: uvicorn, fastapi, torch {torch.__version__}')" && \
    # NOW upgrade PyTorch to CPU-only version (replaces CUDA with CPU)
    pip install --upgrade --extra-index-url https://download.pytorch.org/whl/cpu torch==2.9.0+cpu && \
    python -c "import torch; print(f'✓ PyTorch upgraded to: {torch.__version__}')" && \
    # Remove pip cache
    rm -rf /root/.cache/pip && \
    # Remove test files and documentation from packages (saves ~800 MB)
    find /usr/local/lib/python3.11/site-packages -type d -name "tests" -exec rm -rf {} + 2>/dev/null || true && \
    find /usr/local/lib/python3.11/site-packages -type d -name "test" -exec rm -rf {} + 2>/dev/null || true && \
    find /usr/local/lib/python3.11/site-packages -type d -name "docs" -exec rm -rf {} + 2>/dev/null || true && \
    find /usr/local/lib/python3.11/site-packages -name "*.md" -delete 2>/dev/null || true && \
    find /usr/local/lib/python3.11/site-packages -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true && \
    find /usr/local/lib/python3.11/site-packages -type f -name "*.pyc" -delete && \
    find /usr/local/lib/python3.11/site-packages -type f -name "*.pyo" -delete && \
    # Remove large unused model files from transformers (saves ~300 MB)
    find /usr/local/lib/python3.11/site-packages -path "*/transformers/models/*" -name "*.ckpt" -delete 2>/dev/null || true && \
    find /usr/local/lib/python3.11/site-packages -path "*/transformers/models/*" -name "*.bin" -size +10M -delete 2>/dev/null || true && \
    # Remove unnecessary torch files
    find /usr/local/lib/python3.11/site-packages -path "*/torch/test" -exec rm -rf {} + 2>/dev/null || true && \
    find /usr/local/lib/python3.11/site-packages -path "*/torch/include" -exec rm -rf {} + 2>/dev/null || true && \
    echo "=== Final package directory ===" && \
    du -sh /usr/local/lib/python3.11/site-packages

# =============================================================================
# Stage 2: Runtime - Minimal production image
# =============================================================================
FROM python:3.11-slim-bookworm AS production

LABEL maintainer="BAHR Production Team"
LABEL description="BAHR Backend API - Railway Optimized"
LABEL version="2.0.0"

# Production environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    ENVIRONMENT=production \
    PATH=/usr/local/bin:$PATH

# Install ONLY runtime dependencies (no build tools)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean \
    && apt-get autoclean

WORKDIR /app

# Copy installed Python packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
# Copy binaries (for uvicorn executable, etc.)
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy ONLY application code (no tests, docs, scripts, etc.)
COPY app ./app
COPY alembic ./alembic
COPY alembic.ini ./

# Create non-root user and verify installation
RUN useradd -m -u 1000 -s /bin/sh appuser && \
    chown -R appuser:appuser /app && \
    chmod -R 755 /app && \
    # Clean up any cache
    find /app -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true && \
    # Verify uvicorn is installed and importable (fail build if not)
    python -c "import uvicorn, fastapi, torch; print('✓ All critical packages available in production image')"

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl --fail http://localhost:8000/health || exit 1

# Production startup with optimized worker count
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4", "--log-level", "info"]

# =============================================================================
# BUILD INSTRUCTIONS FOR RAILWAY
# =============================================================================
# 1. Ensure .dockerignore excludes .venv/, node_modules/, frontend/
# 2. Build: docker build -t bahr-backend:railway .
# 3. Test: docker run -p 8000:8000 bahr-backend:railway
# 4. Expected size: 1.0-1.5 GB (well under 4 GB Railway limit)
# =============================================================================
# trigger rebuild
