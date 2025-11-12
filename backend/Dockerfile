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

# Install Python dependencies to /install prefix
RUN set -ex && \
    pip install --upgrade pip setuptools wheel && \
    # Create target directory explicitly
    mkdir -p /install && \
    # Install all requirements first (including torch with CUDA by default)
    pip install --target=/install --no-warn-script-location \
    -r requirements/production.txt && \
    # List what was installed for debugging
    echo "=== Installed packages in /install ===" && \
    ls -la /install/ | head -20 && \
    # Verify critical packages in builder stage
    /usr/local/bin/python -c "import sys; sys.path.insert(0, '/install'); import uvicorn, fastapi; print('✓ Builder: uvicorn and fastapi verified')" && \
    # NOW replace PyTorch CUDA with CPU-only version (keeps all deps)
    pip install --target=/install --no-warn-script-location --upgrade \
    --extra-index-url https://download.pytorch.org/whl/cpu \
    torch==2.9.0+cpu && \
    # Verify torch is CPU version
    /usr/local/bin/python -c "import sys; sys.path.insert(0, '/install'); import torch; print(f'✓ Builder: PyTorch {torch.__version__} installed')" && \
    # Remove pip cache and unnecessary files
    rm -rf /root/.cache/pip && \
    find /install -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true && \
    find /install -type f -name "*.pyc" -delete && \
    find /install -type f -name "*.pyo" -delete && \
    # Remove test files and documentation from packages (saves ~800 MB)
    find /install -type d -name "tests" -exec rm -rf {} + 2>/dev/null || true && \
    find /install -type d -name "test" -exec rm -rf {} + 2>/dev/null || true && \
    find /install -type d -name "docs" -exec rm -rf {} + 2>/dev/null || true && \
    find /install -name "*.md" -delete 2>/dev/null || true && \
    # Remove large unused model files from transformers (saves ~300 MB)
    find /install -path "*/transformers/models/*" -name "*.ckpt" -delete 2>/dev/null || true && \
    find /install -path "*/transformers/models/*" -name "*.bin" -size +10M -delete 2>/dev/null || true && \
    # Remove unnecessary torch files
    find /install -path "*/torch/test" -exec rm -rf {} + 2>/dev/null || true && \
    find /install -path "*/torch/include" -exec rm -rf {} + 2>/dev/null || true && \
    echo "=== Final /install directory ===" && \
    ls -la /install/ | head -20

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

# Copy installed Python packages from builder (--target installs to /install directly)
COPY --from=builder /install /usr/local/lib/python3.11/site-packages

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
