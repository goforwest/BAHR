# Feature: Error Handling Strategy - Implementation Guide

**Feature ID:** `feature-error-handling`  
**Status:** Production-Ready  
**Last Updated:** November 8, 2025  
**Estimated Implementation Time:** 8-10 hours

---

## 1. Objective & Description

### What
Implement comprehensive error handling strategy with custom exception classes, error code taxonomy (ERR_*), severity levels, retry logic, and structured logging.

### Why
- **Consistency:** Unified error handling across all components
- **Debuggability:** Structured errors with codes and context
- **User Experience:** Clear, actionable error messages
- **Monitoring:** Track error patterns and trends
- **Resilience:** Graceful degradation with retry logic

### Success Criteria
- ✅ Define 20+ error codes across 6 categories
- ✅ Create custom exception hierarchy
- ✅ Implement retry logic for transient failures
- ✅ Add structured logging with error context
- ✅ Map errors to HTTP status codes
- ✅ Test coverage ≥85% for error handling paths

---

## 2. Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                Error Handling Architecture                           │
└─────────────────────────────────────────────────────────────────────┘

Request → Handler
           │
           │  try:
           │    process()
           ▼
    ┌──────────────┐
    │ Business     │
    │ Logic        │
    └──────┬───────┘
           │
           │  except:
           ▼
    ┌──────────────────────────────────┐
    │ Custom Exception Raised          │
    │ - BAHRInputError                 │
    │ - BAHRAnalysisError              │
    │ - BAHRAuthenticationError        │
    │ - BAHRRateLimitError             │
    └──────┬───────────────────────────┘
           │
           ▼
    ┌──────────────────────────────────┐
    │ Exception Handler Middleware     │
    │ - Map to error code              │
    │ - Log with context               │
    │ - Create envelope response       │
    └──────┬───────────────────────────┘
           │
           ▼
    ┌──────────────────────────────────┐
    │ Response Envelope                │
    │ {                                │
    │   "success": false,              │
    │   "error": {                     │
    │     "code": "ERR_INPUT_001",     │
    │     "message": {...},            │
    │     "severity": "error"          │
    │   }                              │
    │ }                                │
    └──────────────────────────────────┘

Error Code Taxonomy:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ERR_INPUT_*      - Input validation errors (001-099)
ERR_AUTH_*       - Authentication/authorization (100-199)
ERR_ANALYSIS_*   - Analysis processing errors (200-299)
ERR_RATE_*       - Rate limiting errors (300-399)
ERR_DB_*         - Database errors (400-499)
ERR_CACHE_*      - Caching errors (500-599)
ERR_UNKNOWN_*    - Unknown/system errors (900-999)

Severity Levels:
- info: Informational (e.g., cache miss)
- warning: Non-critical (e.g., low confidence)
- error: Request failed (e.g., validation error)
- critical: System failure (e.g., DB connection lost)
```

---

## 3. Input/Output Contracts

### 3.1 Custom Exception Classes

```python
# backend/app/core/exceptions.py
"""
Custom exception hierarchy for BAHR system.

Source: docs/technical/ERROR_HANDLING_STRATEGY.md:1-150
"""

from typing import Optional, Dict, Any


class BAHRException(Exception):
    """
    Base exception for all BAHR errors.
    
    Attributes:
        code: Error code (e.g., ERR_INPUT_001)
        message: Human-readable error message
        severity: Error severity (info, warning, error, critical)
        context: Additional error context
    """
    
    def __init__(
        self,
        code: str,
        message: str,
        severity: str = "error",
        context: Optional[Dict[str, Any]] = None
    ):
        self.code = code
        self.message = message
        self.severity = severity
        self.context = context or {}
        super().__init__(message)
    
    def __repr__(self):
        return f"<{self.__class__.__name__}(code='{self.code}', message='{self.message}')>"


class BAHRInputError(BAHRException):
    """Input validation errors (ERR_INPUT_*)."""
    
    def __init__(self, code: str, message: str, context: Optional[Dict] = None):
        super().__init__(code, message, severity="error", context=context)


class BAHRAuthenticationError(BAHRException):
    """Authentication/authorization errors (ERR_AUTH_*)."""
    
    def __init__(self, code: str, message: str, context: Optional[Dict] = None):
        super().__init__(code, message, severity="error", context=context)


class BAHRAnalysisError(BAHRException):
    """Analysis processing errors (ERR_ANALYSIS_*)."""
    
    def __init__(self, code: str, message: str, context: Optional[Dict] = None):
        super().__init__(code, message, severity="warning", context=context)


class BAHRRateLimitError(BAHRException):
    """Rate limiting errors (ERR_RATE_*)."""
    
    def __init__(self, code: str, message: str, context: Optional[Dict] = None):
        super().__init__(code, message, severity="warning", context=context)


class BAHRDatabaseError(BAHRException):
    """Database errors (ERR_DB_*)."""
    
    def __init__(self, code: str, message: str, context: Optional[Dict] = None):
        super().__init__(code, message, severity="critical", context=context)


class BAHRCacheError(BAHRException):
    """Caching errors (ERR_CACHE_*)."""
    
    def __init__(self, code: str, message: str, context: Optional[Dict] = None):
        super().__init__(code, message, severity="info", context=context)
```

### 3.2 Error Code Catalog

```python
# backend/app/core/error_codes.py
"""
Complete error code catalog with HTTP status mappings.

Source: docs/technical/API_CONVENTIONS.md:145-210
"""

from typing import Dict, Tuple
from app.schemas.envelope import BilingualMessage


class ErrorCode:
    """Error code with metadata."""
    
    def __init__(self, code: str, http_status: int, message: BilingualMessage):
        self.code = code
        self.http_status = http_status
        self.message = message


# Error code registry
ERROR_CATALOG: Dict[str, ErrorCode] = {
    # Input validation errors (ERR_INPUT_*)
    "ERR_INPUT_001": ErrorCode(
        code="ERR_INPUT_001",
        http_status=400,
        message=BilingualMessage(
            en="Input text is required",
            ar="النص المدخل مطلوب"
        )
    ),
    "ERR_INPUT_002": ErrorCode(
        code="ERR_INPUT_002",
        http_status=400,
        message=BilingualMessage(
            en="Input text exceeds maximum length (1000 characters)",
            ar="النص المدخل يتجاوز الحد الأقصى (1000 حرف)"
        )
    ),
    "ERR_INPUT_003": ErrorCode(
        code="ERR_INPUT_003",
        http_status=422,
        message=BilingualMessage(
            en="Invalid input format",
            ar="صيغة الإدخال غير صالحة"
        )
    ),
    "ERR_INPUT_004": ErrorCode(
        code="ERR_INPUT_004",
        http_status=400,
        message=BilingualMessage(
            en="Input text contains insufficient Arabic content",
            ar="النص المدخل لا يحتوي على محتوى عربي كافٍ"
        )
    ),
    
    # Authentication errors (ERR_AUTH_*)
    "ERR_AUTH_100": ErrorCode(
        code="ERR_AUTH_100",
        http_status=401,
        message=BilingualMessage(
            en="Invalid credentials",
            ar="بيانات الاعتماد غير صحيحة"
        )
    ),
    "ERR_AUTH_101": ErrorCode(
        code="ERR_AUTH_101",
        http_status=401,
        message=BilingualMessage(
            en="Token expired",
            ar="انتهت صلاحية الرمز"
        )
    ),
    "ERR_AUTH_102": ErrorCode(
        code="ERR_AUTH_102",
        http_status=401,
        message=BilingualMessage(
            en="Invalid token",
            ar="رمز غير صالح"
        )
    ),
    "ERR_AUTH_103": ErrorCode(
        code="ERR_AUTH_103",
        http_status=403,
        message=BilingualMessage(
            en="Insufficient permissions",
            ar="صلاحيات غير كافية"
        )
    ),
    "ERR_AUTH_104": ErrorCode(
        code="ERR_AUTH_104",
        http_status=409,
        message=BilingualMessage(
            en="Username already exists",
            ar="اسم المستخدم موجود بالفعل"
        )
    ),
    
    # Analysis errors (ERR_ANALYSIS_*)
    "ERR_ANALYSIS_200": ErrorCode(
        code="ERR_ANALYSIS_200",
        http_status=500,
        message=BilingualMessage(
            en="Analysis processing failed",
            ar="فشل معالجة التحليل"
        )
    ),
    "ERR_ANALYSIS_201": ErrorCode(
        code="ERR_ANALYSIS_201",
        http_status=200,  # Not an error, but low confidence
        message=BilingualMessage(
            en="No meter detected with sufficient confidence",
            ar="لم يتم اكتشاف بحر شعري بثقة كافية"
        )
    ),
    "ERR_ANALYSIS_202": ErrorCode(
        code="ERR_ANALYSIS_202",
        http_status=408,
        message=BilingualMessage(
            en="Analysis timeout exceeded",
            ar="تم تجاوز مهلة التحليل"
        )
    ),
    
    # Rate limiting errors (ERR_RATE_*)
    "ERR_RATE_300": ErrorCode(
        code="ERR_RATE_300",
        http_status=429,
        message=BilingualMessage(
            en="Rate limit exceeded. Please try again later.",
            ar="تم تجاوز حد المعدل. يرجى المحاولة لاحقًا."
        )
    ),
    
    # Database errors (ERR_DB_*)
    "ERR_DB_400": ErrorCode(
        code="ERR_DB_400",
        http_status=500,
        message=BilingualMessage(
            en="Database connection failed",
            ar="فشل الاتصال بقاعدة البيانات"
        )
    ),
    "ERR_DB_401": ErrorCode(
        code="ERR_DB_401",
        http_status=404,
        message=BilingualMessage(
            en="Resource not found",
            ar="المورد غير موجود"
        )
    ),
    
    # Cache errors (ERR_CACHE_*)
    "ERR_CACHE_500": ErrorCode(
        code="ERR_CACHE_500",
        http_status=200,  # Fail gracefully
        message=BilingualMessage(
            en="Cache unavailable (proceeding without cache)",
            ar="ذاكرة التخزين المؤقت غير متاحة (المتابعة بدون ذاكرة تخزين مؤقت)"
        )
    ),
    
    # Unknown errors (ERR_UNKNOWN_*)
    "ERR_UNKNOWN_900": ErrorCode(
        code="ERR_UNKNOWN_900",
        http_status=500,
        message=BilingualMessage(
            en="Internal server error",
            ar="خطأ داخلي في الخادم"
        )
    ),
}


def get_error_info(code: str) -> ErrorCode:
    """Get error information by code."""
    return ERROR_CATALOG.get(
        code,
        ErrorCode(
            code="ERR_UNKNOWN_900",
            http_status=500,
            message=BilingualMessage(en="Unknown error", ar="خطأ غير معروف")
        )
    )
```

---

## 4. Step-by-Step Implementation

### Step 1: Create Exception Handler Middleware

```python
# backend/app/middleware/exception_handler.py
"""
Global exception handler middleware.

Source: docs/technical/ERROR_HANDLING_STRATEGY.md:80-150
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import logging
import traceback

from app.core.exceptions import BAHRException
from app.core.error_codes import get_error_info
from app.middleware.response_envelope import failure

logger = logging.getLogger(__name__)


class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    """
    Global exception handler for BAHR exceptions.
    
    Catches all exceptions and converts to envelope responses.
    """
    
    async def dispatch(self, request: Request, call_next):
        """Process request and handle exceptions."""
        try:
            response = await call_next(request)
            return response
            
        except BAHRException as e:
            # Handle BAHR custom exceptions
            logger.error(
                f"BAHR Exception: {e.code}",
                extra={
                    "error_code": e.code,
                    "severity": e.severity,
                    "context": e.context,
                    "request_id": getattr(request.state, "request_id", None),
                    "path": request.url.path,
                    "method": request.method
                }
            )
            
            # Get error info
            error_info = get_error_info(e.code)
            
            # Return formatted error response
            return failure(
                error_code=e.code,
                request_id=getattr(request.state, "request_id", "unknown"),
                details=e.context.get("details") if e.context else None,
                status_code=error_info.http_status
            )
            
        except Exception as e:
            # Handle unexpected exceptions
            logger.critical(
                f"Unhandled exception: {str(e)}",
                extra={
                    "exception_type": type(e).__name__,
                    "traceback": traceback.format_exc(),
                    "request_id": getattr(request.state, "request_id", None),
                    "path": request.url.path,
                    "method": request.method
                }
            )
            
            # Return generic error
            return failure(
                error_code="ERR_UNKNOWN_900",
                request_id=getattr(request.state, "request_id", "unknown"),
                details=[{"field": "exception", "issue": str(e)}],
                status_code=500
            )
```

### Step 2: Implement Retry Logic

```python
# backend/app/core/retry.py
"""
Retry logic for transient failures.

Source: docs/technical/ERROR_HANDLING_STRATEGY.md:120-180
"""

import time
import logging
from typing import Callable, TypeVar, Optional
from functools import wraps

from app.core.exceptions import BAHRException, BAHRDatabaseError, BAHRCacheError

logger = logging.getLogger(__name__)

T = TypeVar('T')


def retry_on_transient_error(
    max_attempts: int = 3,
    delay_seconds: float = 0.5,
    backoff_multiplier: float = 2.0,
    retryable_exceptions: tuple = (BAHRDatabaseError, BAHRCacheError)
):
    """
    Decorator to retry on transient errors.
    
    Args:
        max_attempts: Maximum retry attempts
        delay_seconds: Initial delay between retries
        backoff_multiplier: Exponential backoff multiplier
        retryable_exceptions: Exception types to retry
    
    Usage:
        @retry_on_transient_error(max_attempts=3)
        def fetch_from_db():
            ...
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            attempt = 0
            current_delay = delay_seconds
            
            while attempt < max_attempts:
                try:
                    return func(*args, **kwargs)
                    
                except retryable_exceptions as e:
                    attempt += 1
                    
                    if attempt >= max_attempts:
                        logger.error(
                            f"Max retry attempts ({max_attempts}) exceeded for {func.__name__}",
                            extra={"error_code": e.code if isinstance(e, BAHRException) else None}
                        )
                        raise
                    
                    logger.warning(
                        f"Transient error in {func.__name__}, retrying ({attempt}/{max_attempts})",
                        extra={
                            "error_code": e.code if isinstance(e, BAHRException) else None,
                            "delay_seconds": current_delay
                        }
                    )
                    
                    time.sleep(current_delay)
                    current_delay *= backoff_multiplier
                    
                except Exception:
                    # Don't retry non-transient errors
                    raise
            
            raise RuntimeError(f"Retry logic failed for {func.__name__}")
        
        return wrapper
    return decorator


# Example usage
@retry_on_transient_error(max_attempts=3, delay_seconds=0.5)
def fetch_analysis_from_db(analysis_id: str):
    """Fetch analysis with retry logic."""
    # Database query that may fail transiently
    pass
```

### Step 3: Structured Logging

```python
# backend/app/core/logging_config.py
"""
Structured logging configuration.

Source: docs/technical/ERROR_HANDLING_STRATEGY.md:200-250
"""

import logging
import json
from datetime import datetime
from typing import Dict, Any


class StructuredFormatter(logging.Formatter):
    """
    JSON structured logging formatter.
    
    Outputs logs in JSON format for easy parsing.
    """
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_data: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        # Add extra fields
        if hasattr(record, "error_code"):
            log_data["error_code"] = record.error_code
        if hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id
        if hasattr(record, "severity"):
            log_data["severity"] = record.severity
        if hasattr(record, "context"):
            log_data["context"] = record.context
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_data, ensure_ascii=False)


def configure_logging():
    """Configure application logging."""
    # Create formatter
    formatter = StructuredFormatter()
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(console_handler)
    
    # Suppress noisy loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
```

### Step 4: Example Usage in Routes

```python
# backend/app/api/v1/routes/analyses.py
"""Analysis routes with error handling."""

from fastapi import APIRouter, Request
from app.core.exceptions import BAHRInputError, BAHRAnalysisError
from app.schemas.analysis import AnalysisRequest

router = APIRouter(prefix="/api/v1/analyses")


@router.post("")
async def create_analysis(request: Request, body: AnalysisRequest):
    """
    Analyze verse with comprehensive error handling.
    """
    # Input validation
    if not body.text.strip():
        raise BAHRInputError(
            code="ERR_INPUT_001",
            message="Input text is required",
            context={"field": "text"}
        )
    
    if len(body.text) > 1000:
        raise BAHRInputError(
            code="ERR_INPUT_002",
            message="Input text exceeds maximum length",
            context={"field": "text", "max_length": 1000, "actual_length": len(body.text)}
        )
    
    # Check Arabic content
    arabic_chars = sum(1 for c in body.text if '\u0600' <= c <= '\u06FF')
    if arabic_chars < 5:
        raise BAHRInputError(
            code="ERR_INPUT_004",
            message="Insufficient Arabic content",
            context={"arabic_chars": arabic_chars, "min_required": 5}
        )
    
    # Process analysis (may raise BAHRAnalysisError)
    try:
        result = process_verse(body.text)
    except Exception as e:
        raise BAHRAnalysisError(
            code="ERR_ANALYSIS_200",
            message="Analysis processing failed",
            context={"original_error": str(e)}
        )
    
    return result
```

---

## 5. Reference Implementation (Full Code)

See Step-by-Step Implementation sections above for complete code.

---

## 6. Unit & Integration Tests

```python
# tests/unit/test_exceptions.py
import pytest
from app.core.exceptions import (
    BAHRException,
    BAHRInputError,
    BAHRAnalysisError
)


def test_bahr_exception_creation():
    """Test BAHR exception instantiation."""
    exc = BAHRException(
        code="ERR_TEST_001",
        message="Test error",
        severity="error",
        context={"field": "test"}
    )
    
    assert exc.code == "ERR_TEST_001"
    assert exc.message == "Test error"
    assert exc.severity == "error"
    assert exc.context["field"] == "test"


def test_input_error_defaults():
    """Test BAHRInputError defaults."""
    exc = BAHRInputError(
        code="ERR_INPUT_001",
        message="Input required"
    )
    
    assert exc.severity == "error"
    assert exc.context == {}


def test_retry_decorator():
    """Test retry logic decorator."""
    from app.core.retry import retry_on_transient_error
    from app.core.exceptions import BAHRDatabaseError
    
    attempt_count = 0
    
    @retry_on_transient_error(max_attempts=3, delay_seconds=0.1)
    def flaky_function():
        nonlocal attempt_count
        attempt_count += 1
        if attempt_count < 3:
            raise BAHRDatabaseError("ERR_DB_400", "Connection failed")
        return "success"
    
    result = flaky_function()
    
    assert result == "success"
    assert attempt_count == 3
```

```python
# tests/integration/test_error_handling.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_input_validation_error():
    """Test input validation returns proper error envelope."""
    response = client.post(
        "/api/v1/analyses",
        json={"text": ""}  # Empty text
    )
    
    assert response.status_code == 400
    data = response.json()
    
    assert data["success"] is False
    assert data["error"]["code"] == "ERR_INPUT_001"
    assert "مطلوب" in data["error"]["message"]["ar"]


def test_rate_limit_error():
    """Test rate limit error response."""
    # Make many requests to trigger rate limit
    for _ in range(150):
        client.post("/api/v1/analyses", json={"text": "test"})
    
    response = client.post("/api/v1/analyses", json={"text": "test"})
    
    assert response.status_code == 429
    data = response.json()
    assert data["error"]["code"] == "ERR_RATE_300"
```

---

## 7. CI/CD Pipeline

```yaml
# .github/workflows/error-handling-tests.yml
name: Error Handling Tests

on:
  push:
    paths:
      - 'backend/app/core/exceptions.py'
      - 'backend/app/core/error_codes.py'
      - 'backend/app/middleware/exception_handler.py'

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Run error handling tests
        run: |
          cd backend
          pytest tests/unit/test_exceptions.py \
            tests/integration/test_error_handling.py \
            -v --cov=app.core.exceptions \
            --cov=app.core.error_codes
```

---

## 8. Deployment Checklist

- [ ] Add ExceptionHandlerMiddleware to FastAPI app
- [ ] Configure structured logging
- [ ] Test all error codes with proper HTTP status
- [ ] Verify bilingual error messages
- [ ] Test retry logic for database/cache errors
- [ ] Add error metrics to Prometheus
- [ ] Create error dashboard in Grafana
- [ ] Document all error codes in API documentation
- [ ] Test error responses in all languages
- [ ] Configure error alerting thresholds

---

## 9. Observability

```python
# backend/app/metrics/error_metrics.py
from prometheus_client import Counter

error_total = Counter(
    "bahr_errors_total",
    "Total errors by code and severity",
    ["error_code", "severity", "http_status"]
)

retry_attempts_total = Counter(
    "bahr_retry_attempts_total",
    "Total retry attempts",
    ["function", "success"]
)
```

---

## 10. Security & Safety

- **Error Message Sanitization:** Never expose internal details
- **Stack Trace Filtering:** Only in development mode
- **Context Validation:** Sanitize error context before logging
- **Rate Limit Errors:** Don't expose rate limit internals

---

## 11. Backwards Compatibility

- **None** - Initial implementation
- **Future Changes:** Add error codes, never remove existing codes

---

## 12. Source Documentation Citations

1. **docs/technical/ERROR_HANDLING_STRATEGY.md:1-250** - Error handling specification
2. **docs/technical/API_CONVENTIONS.md:145-210** - Error code catalog
3. **implementation-guides/IMPROVED_PROMPT.md:716-738** - Feature specification

---

**Implementation Complete!** ✅  
**Estimated Time:** 8-10 hours  
**Test Coverage Target:** ≥ 85%  
**Error Categories:** 6 (Input, Auth, Analysis, Rate, DB, Cache)
