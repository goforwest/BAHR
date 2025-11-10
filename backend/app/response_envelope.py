"""Unified response envelope helpers.
Refer to docs/technical/API_CONVENTIONS.md for contract details.

Enhancements (2025-11-08):
 - Added optional localization support (ar/en) for error messages.
 - Added 'details' support for validation-style errors.
 - Added ability to propagate performance meta (processing_time_ms, cached) on failures.
 - Centralized error message lookup by code for consistent translations.
"""
from typing import Any, Optional, Dict, List, Tuple
import time
import uuid

# Supported languages
SUPPORTED_LANGS = {"ar", "en"}

# Basic bilingual message catalog (expand as needed)
# code -> (arabic_message, english_message)
ERROR_MESSAGES: Dict[str, Tuple[str, str]] = {
    # Input / validation
    "ERR_INPUT_001": (
        "النص يجب أن يحتوي على أحرف عربية",
        "Input must contain Arabic characters",
    ),
    "ERR_INPUT_002": (
        "النص أقصر من الحد الأدنى",
        "Text is shorter than the minimum length",
    ),
    "ERR_INPUT_003": (
        "النص أطول من الحد المسموح",
        "Text exceeds the maximum allowed length",
    ),
    # Analysis
    "ERR_ANALYSIS_001": (
        "تعذر إتمام التحليل",
        "Unable to complete analysis",
    ),
    # Rate / auth examples
    "ERR_RATE_001": ("تم تجاوز الحد الزمني للطلبات", "Rate limit exceeded"),
    "ERR_AUTH_001": ("غير مصرح بالدخول", "Unauthorized"),
    # Generic
    "ERR_UNKNOWN_001": ("خطأ غير متوقع", "Unexpected error"),
}

API_VERSION = "1.0.0"
ANALYSIS_ENGINE_VERSION = "1.0.0"  # bump when algorithm changes

def now_ts() -> int:
    return int(time.time())

def generate_request_id() -> str:
    return uuid.uuid4().hex[:12]

def success(
    data: Any,
    request_id: Optional[str] = None,
    meta_extra: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    meta = {
        "request_id": request_id or generate_request_id(),
        "timestamp": now_ts(),
        "version": API_VERSION,
        "analysis_engine_version": ANALYSIS_ENGINE_VERSION,
    }
    if meta_extra:
        meta.update(meta_extra)
    return {
        "success": True,
        "data": data,
        "error": None,
        "meta": meta,
    }

def failure(
    code: str,
    message: Optional[str] = None,
    *,
    severity: str = "error",
    can_retry: bool = False,
    request_id: Optional[str] = None,
    lang: str = "ar",
    details: Optional[List[Dict[str, Any]]] = None,
    retry_after: Optional[int] = None,
    meta_extra: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Create a failure envelope.

    Args:
        code: Error code.
        message: Optional explicit message override.
        severity: info | warning | error | critical
        can_retry: Whether client may retry as-is.
        lang: Preferred language ('ar' or 'en'). Defaults to Arabic.
        details: Optional list of validation detail dicts.
        retry_after: Optional seconds to wait (rate limiting / backoff).
        meta_extra: Optional meta extensions (processing_time_ms, cached ...)
    """
    lang_final = lang if lang in SUPPORTED_LANGS else "ar"
    resolved_message = message
    if not resolved_message:
        if code in ERROR_MESSAGES:
            resolved_message = (
                ERROR_MESSAGES[code][0]
                if lang_final == "ar"
                else ERROR_MESSAGES[code][1]
            )
        else:
            resolved_message = (
                "حدث خطأ" if lang_final == "ar" else "An error occurred"
            )

    meta = {
        "request_id": request_id or generate_request_id(),
        "timestamp": now_ts(),
        "version": API_VERSION,
        "analysis_engine_version": ANALYSIS_ENGINE_VERSION,
    }
    if meta_extra:
        meta.update(meta_extra)

    error_obj: Dict[str, Any] = {
        "code": code,
        "message": resolved_message,
        "severity": severity,
        "can_retry": can_retry,
    }
    if details:
        error_obj["details"] = details
    if retry_after is not None:
        error_obj["retry_after"] = retry_after

    return {
        "success": False,
        "data": None,
        "error": error_obj,
        "meta": meta,
    }

__all__ = [
    "success",
    "failure",
    "ERROR_MESSAGES",
    "SUPPORTED_LANGS",
]
