"""Utility for managing request IDs."""

import uuid

from fastapi import Request

HEADER_NAME = "X-Request-ID"


def ensure_request_id(request: Request) -> None:
    rid = request.headers.get(HEADER_NAME)
    if not rid:
        rid = uuid.uuid4().hex[:12]
    request.state.request_id = rid
