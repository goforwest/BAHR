"""Custom exception hierarchy for BAHR.

Simplified MVP version aligned with documented taxonomy. Each exception
stores an error code and optional context. Global handlers will turn these
into standardized response envelopes.
"""

from __future__ import annotations

from typing import Any, Dict, Optional


class BahrException(Exception):
    def __init__(
        self,
        code: str,
        message: str,
        *,
        severity: str = "error",
        can_retry: bool = False,
        context: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.code = code
        self.message = message
        self.severity = severity
        self.can_retry = can_retry
        self.context = context or {}


class InputError(BahrException):
    def __init__(
        self, code: str = "ERR_INPUT_001", message: str = "Invalid input", **kw: Any
    ):
        super().__init__(code, message, severity="error", can_retry=False, **kw)


class AnalysisError(BahrException):
    def __init__(
        self,
        code: str = "ERR_ANALYSIS_001",
        message: str = "Analysis failed",
        **kw: Any,
    ):
        super().__init__(code, message, severity="error", **kw)


class RateLimitError(BahrException):
    def __init__(
        self,
        code: str = "ERR_RATE_001",
        message: str = "Rate limit exceeded",
        **kw: Any,
    ):
        super().__init__(code, message, severity="warning", can_retry=True, **kw)


class AuthError(BahrException):
    def __init__(
        self, code: str = "ERR_AUTH_001", message: str = "Unauthorized", **kw: Any
    ):
        super().__init__(code, message, severity="error", can_retry=False, **kw)


class UnknownError(BahrException):
    def __init__(
        self,
        code: str = "ERR_UNKNOWN_001",
        message: str = "Unexpected error",
        **kw: Any,
    ):
        super().__init__(code, message, severity="critical", **kw)


__all__ = [
    "BahrException",
    "InputError",
    "AnalysisError",
    "RateLimitError",
    "AuthError",
    "UnknownError",
]
