from fastapi import FastAPI, Request, Header
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.exceptions import RequestValidationError
from typing import Optional
import time

from .middleware.response_envelope import RequestIDMiddleware
from .middleware.util_request_id import HEADER_NAME as REQUEST_ID_HEADER
from .response_envelope import success, failure
from .exceptions import BahrException
from .config import settings
from .metrics.analysis_metrics import record_latency

try:
    from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
except Exception:
    CONTENT_TYPE_LATEST = "text/plain; version=0.0.4; charset=utf-8"
    def generate_latest():  # type: ignore
        return b""


app = FastAPI(title=settings.project_name, version=settings.version)

# Register middleware early to ensure request id propagation
app.add_middleware(RequestIDMiddleware)


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


# --------- Example Analyze Endpoint (Stub) ---------
from pydantic import BaseModel, Field
from .nlp.normalizer import basic_normalize
from .prosody.segmenter import segment
from .prosody.engine import build_pattern, detect_meter


class AnalysisOptions(BaseModel):
    remove_diacritics: bool = True
    analysis_mode: str = Field(default="accurate", pattern="^(fast|accurate|detailed)$")
    return_alternatives: bool = True
    include_suggestions: bool = True


class AnalysisRequest(BaseModel):
    text: str = Field(min_length=5, max_length=2000)
    options: Optional[AnalysisOptions] = None


@app.post("/api/v1/analyze")
async def analyze(
    request: Request,
    payload: AnalysisRequest,
    accept_language: Optional[str] = Header(default=None, alias="Accept-Language"),
):
    start = time.perf_counter()
    # Minimal validation example: ensure contains some Arabic letters
    if not any("\u0600" <= ch <= "\u06FF" for ch in payload.text):
        lang = "en" if (accept_language or "").lower().startswith("en") else "ar"
        elapsed = time.perf_counter() - start
        env = failure(
            code="ERR_INPUT_001",
            severity="warning",
            can_retry=False,
            request_id=getattr(request.state, "request_id", None),
            lang=lang,
            meta_extra={"processing_time_ms": int(elapsed * 1000), "cached": False},
        )
        headers = {REQUEST_ID_HEADER: request.state.request_id, "Content-Language": lang}
        return JSONResponse(env, status_code=422, headers=headers)

    # Normalization (MVP)
    normalized = basic_normalize(payload.text, remove_diacritics=payload.options.remove_diacritics if payload.options else True)
    syllables = segment(normalized)
    prosody_pattern = build_pattern(syllables)
    meter_name, meter_conf, alternatives = detect_meter(prosody_pattern.pattern)

    result = {
        "analysis_id": "00000000-0000-0000-0000-000000000000",
        "input_text": payload.text,
        "normalized_text": normalized,
        "prosodic_analysis": {
            "taqti3": prosody_pattern.taqti3,
            "pattern": prosody_pattern.pattern,
            "syllable_count": prosody_pattern.syllable_count,
            "stress_pattern": prosody_pattern.stress_pattern,
        },
        "meter_detection": {
            "detected_meter": meter_name,
            "confidence": meter_conf,
            "alternatives": alternatives,
        },
        "quality_score": round(min(1.0, (meter_conf * 0.7) + (prosody_pattern.syllable_count / 100)), 2),
        "suggestions": [
            "التقطيع دقيق ومتسق",
        ],
        "created_at": "2025-01-01T00:00:00Z",
    }

    elapsed = time.perf_counter() - start
    record_latency(elapsed)
    env = success(
        data=result,
        request_id=getattr(request.state, "request_id", None),
        meta_extra={"cached": False, "processing_time_ms": int(elapsed * 1000)},
    )
    lang = "en" if (accept_language or "").lower().startswith("en") else "ar"
    headers = {REQUEST_ID_HEADER: request.state.request_id, "Content-Language": lang}
    return JSONResponse(env, headers=headers)


@app.get("/")
async def root():
    return {"message": "BAHR API - see /docs"}
