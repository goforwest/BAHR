# =============================================================================
# BAHR Backend - MINIMAL Single-Stage Dockerfile
# Emergency fix for Railway cache issue
# Target: <2GB (no multi-stage complexity)
# =============================================================================

FROM python:3.11-slim-bullseye

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install minimal runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    gcc \
    libpq-dev && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Copy and install Python dependencies with MAXIMUM cleanup
COPY requirements/minimal-production.txt ./requirements/
RUN pip install --no-cache-dir -r requirements/minimal-production.txt && \
    find /usr/local -type d -name "tests" -exec rm -rf {} + 2>/dev/null || true && \
    find /usr/local -type d -name "test" -exec rm -rf {} + 2>/dev/null || true && \
    find /usr/local -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true && \
    find /usr/local -type f -name "*.pyc" -o -name "*.pyo" -delete && \
    find /usr/local -type f -name "*.c" -o -name "*.h" -o -name "*.cpp" -delete && \
    find /usr/local -name "*.so" -exec strip --strip-unneeded {} + 2>/dev/null || true && \
    rm -rf /usr/local/lib/python3.11/site-packages/pip* \
           /usr/local/lib/python3.11/site-packages/setuptools* \
           /usr/local/lib/python3.11/site-packages/wheel* \
           /usr/local/lib/python3.11/site-packages/*/tests \
           /usr/local/lib/python3.11/site-packages/*/*/tests \
           /usr/local/lib/python3.11/site-packages/*/test \
           /usr/local/share \
           /root/.cache && \
    apt-get purge -y gcc libpq-dev && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Copy application code
COPY app/ ./app/
COPY database/ ./database/
COPY alembic.ini ./
COPY alembic/ ./alembic/

# Create non-root user
RUN useradd -m -u 1000 -s /bin/sh appuser && \
    chown -R appuser:appuser /app

USER appuser

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl --fail http://localhost:8000/health || exit 1

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
