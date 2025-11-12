"""
API v1 router aggregating all endpoints.
"""

from fastapi import APIRouter
from .endpoints import analyze, analyze_v2, analytics, feedback

api_router = APIRouter()

# Include analyze endpoint (original)
api_router.include_router(
    analyze.router,
    prefix="/analyze",
    tags=["Analysis"]
)

# Include analyze V2 endpoint (enhanced with explainability)
api_router.include_router(
    analyze_v2.router,
    prefix="/analyze-v2",
    tags=["Analysis V2 (Enhanced)"]
)

# Include analytics endpoint
api_router.include_router(
    analytics.router,
    prefix="/analytics",
    tags=["Analytics"]
)

# Include feedback endpoint
api_router.include_router(
    feedback.router,
    prefix="/feedback",
    tags=["Feedback"]
)
