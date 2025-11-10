from fastapi import FastAPI, Request, Header
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import time

from .middleware.response_envelope import RequestIDMiddleware
from .middleware.util_request_id import HEADER_NAME as REQUEST_ID_HEADER
from .response_envelope import success, failure
from .exceptions import BahrException
from .config import settings
from .metrics.analysis_metrics import record_latency
from .api.v1.router import api_router
from .db.redis import get_redis, close_redis

try:
    from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
except Exception:
    CONTENT_TYPE_LATEST = "text/plain; version=0.0.4; charset=utf-8"
    def generate_latest():  # type: ignore
        return b""


app = FastAPI(title=settings.project_name, version=settings.version)

# Include API v1 router
app.include_router(api_router, prefix="/api/v1")

# CORS middleware (ADR-003: Explicit CORS configuration)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register middleware early to ensure request id propagation
app.add_middleware(RequestIDMiddleware)


# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Initialize Redis connection on startup."""
    try:
        await get_redis()
        print("✓ Redis connection initialized")
    except Exception as e:
        print(f"✗ Redis connection failed: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    """Close Redis connection on shutdown."""
    await close_redis()
    print("✓ Redis connection closed")


@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": time.time(), "version": app.version}


@app.get("/health/detailed")
async def health_detailed():
    # Minimal stub; extend with real checks (DB/Redis) later
    return {
        "status": "healthy",
        "checks": {
            "database": {"status": "unknown", "message": "not wired"},
            "redis": {"status": "unknown", "message": "not wired"},
            "system": {"cpu_percent": 0, "memory_percent": 0},
        },
    }


@app.get("/metrics")
async def metrics():
    content = generate_latest()
    return PlainTextResponse(content, media_type=CONTENT_TYPE_LATEST)


# ------------- Global exception handlers to enforce envelope -------------
@app.exception_handler(RequestValidationError)
async def handle_validation_error(request: Request, exc: RequestValidationError):
    lang = request.headers.get("Accept-Language", "ar")
    env = failure(
        code="ERR_INPUT_003",  # generic invalid format
        request_id=getattr(request.state, "request_id", None),
        lang="en" if (lang or "").lower().startswith("en") else "ar",
        severity="warning",
        can_retry=False,
        details=[{"field": e.get("loc"), "issue": e.get("msg")} for e in exc.errors()],
    )
    headers = {REQUEST_ID_HEADER: getattr(request.state, "request_id", "")}
    headers["Content-Language"] = "en" if (lang or "").lower().startswith("en") else "ar"
    return JSONResponse(env, status_code=422, headers=headers)


@app.exception_handler(BahrException)
async def handle_bahr_exception(request: Request, exc: BahrException):
    lang = request.headers.get("Accept-Language", "ar")
    env = failure(
        code=exc.code,
        message=exc.message,
        severity=exc.severity,
        can_retry=exc.can_retry,
        request_id=getattr(request.state, "request_id", None),
        lang="en" if (lang or "").lower().startswith("en") else "ar",
        details=[exc.context] if exc.context else None,
    )
    headers = {REQUEST_ID_HEADER: getattr(request.state, "request_id", "")}
    headers["Content-Language"] = "en" if (lang or "").lower().startswith("en") else "ar"
    # Default 400; callers can adjust by raising HTTPException alternatively
    return JSONResponse(env, status_code=400, headers=headers)


@app.exception_handler(Exception)
async def handle_unknown_exception(request: Request, exc: Exception):
    lang = request.headers.get("Accept-Language", "ar")
    env = failure(
        code="ERR_UNKNOWN_001",
        request_id=getattr(request.state, "request_id", None),
        lang="en" if (lang or "").lower().startswith("en") else "ar",
        severity="error",
        can_retry=True,
        details=[{"exception": str(exc)}],
    )
    headers = {REQUEST_ID_HEADER: getattr(request.state, "request_id", "")}
    headers["Content-Language"] = "en" if (lang or "").lower().startswith("en") else "ar"
    return JSONResponse(env, status_code=500, headers=headers)


# --------- Example Analyze Endpoint (Stub) - DISABLED ---------
# NOTE: The actual /api/v1/analyze endpoint with Redis caching is in
# backend/app/api/v1/endpoints/analyze.py and is included via api_router
# This stub endpoint has been commented out to avoid conflicts
#
# from pydantic import BaseModel, Field
# from .nlp.normalizer import basic_normalize
# from .prosody.segmenter import segment
# from .prosody.engine import build_pattern, detect_meter
#
# class AnalysisOptions(BaseModel):
#     remove_diacritics: bool = True
#     analysis_mode: str = Field(default="accurate", pattern="^(fast|accurate|detailed)$")
#     return_alternatives: bool = True
#     include_suggestions: bool = True
#
# class AnalysisRequest(BaseModel):
#     text: str = Field(min_length=5, max_length=2000)
#     options: Optional[AnalysisOptions] = None
#
# @app.post("/api/v1/analyze")
# async def analyze(...):
#     ... (endpoint implementation removed - see endpoints/analyze.py instead)
# --------- End of disabled stub ---------


@app.get("/")
async def root():
    return {"message": "BAHR API - see /docs"}
