"""FastAPI middleware for injecting request_id and normalizing envelopes.
Attach early in stack. The actual endpoint handlers should use helpers in response_envelope.py.
"""
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from .util_request_id import ensure_request_id

class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        ensure_request_id(request)
        response = await call_next(request)
        # Propagate X-Request-ID in response headers
        response.headers.setdefault("X-Request-ID", request.state.request_id)
        return response
