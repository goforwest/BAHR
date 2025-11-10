"""
API v1 router aggregating all endpoints.
"""

from fastapi import APIRouter
from .endpoints import analyze

api_router = APIRouter()

# Include analyze endpoint
api_router.include_router(
    analyze.router,
    prefix="/analyze",
    tags=["Analysis"]
)
