# Feature: Analysis API - Implementation Guide

**Feature ID:** `feature-analysis-api`  
**Status:** Production-Ready  
**Last Updated:** November 8, 2025  
**Estimated Implementation Time:** 18-22 hours

---

## 1. Objective & Description

### What
Implement REST API endpoints for Arabic poetry prosody analysis that integrate normalization, syllable segmentation, and meter detection pipelines. The API provides synchronous single-verse analysis and returns comprehensive results with confidence scores, تفاعيل breakdowns, and educational explanations.

### Why
- **Core Functionality:** Primary user-facing feature of BAHR platform
- **Integration:** Orchestrates all prosody components (normalizer → segmenter → detector)
- **RESTful Design:** Standard HTTP API for web and mobile clients
- **Performance:** P95 latency <600ms for single-verse analysis
- **Observability:** Detailed metrics and logging for production monitoring

### Success Criteria
- ✅ POST /api/v1/analyses endpoint accepts verse text
- ✅ GET /api/v1/analyses/{id} retrieves cached analysis
- ✅ GET /api/v1/analyses/batch for multi-verse analysis
- ✅ Response includes normalized text, syllables, pattern, meter, confidence
- ✅ Validate input (max 1000 chars, Arabic script only)
- ✅ Return 422 for validation errors with detailed messages
- ✅ Achieve P95 <600ms latency
- ✅ Test coverage ≥80% with 50+ test cases
- ✅ OpenAPI documentation auto-generated

---

## 2. Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                  Analysis API Request Flow                           │
└─────────────────────────────────────────────────────────────────────┘

Client Request: POST /api/v1/analyses
{
  "text": "قفا نبك من ذكري حبيب ومنزل",
  "options": {"include_taf3ilat": true}
}
    │
    ▼
┌──────────────────────────────────────┐
│ Step 1: Request Validation           │
│ (Pydantic schema, max length)        │
└──────────┬───────────────────────────┘
    │  Validated: AnalysisRequest(
    │    text="قفا نبك...",
    │    options=AnalysisOptions(...)
    │  )
    ▼
┌──────────────────────────────────────┐
│ Step 2: Text Normalization           │
│ (ArabicTextNormalizer)               │
└──────────┬───────────────────────────┘
    │  Normalized: "قفا نبك من ذكري حبيب ومنزل"
    │  (removed diacritics, extra spaces)
    ▼
┌──────────────────────────────────────┐
│ Step 3: Syllable Segmentation        │
│ (SyllableSegmenter + CAMeL Tools)    │
└──────────┬───────────────────────────┘
    │  Syllables: [
    │    {text: "قِ", type: "CV", long: False},
    │    {text: "فَا", type: "CVV", long: True},
    │    ...
    │  ]
    │  Pattern: "∪ - - ∪ - - ∪ - -"
    ▼
┌──────────────────────────────────────┐
│ Step 4: Meter Detection               │
│ (MeterDetector + fuzzy matching)     │
└──────────┬───────────────────────────┘
    │  Detected: ArabicMeter.AL_TAWIL
    │  Confidence: 0.92
    │  Candidates: [الطويل, الكامل, البسيط]
    ▼
┌──────────────────────────────────────┐
│ Step 5: Result Aggregation           │
│ (Combine all pipeline outputs)       │
└──────────┬───────────────────────────┘
    │  Full result: {
    │    id, text, normalized_text,
    │    syllables, pattern, meter,
    │    confidence, taf3ilat, created_at
    │  }
    ▼
┌──────────────────────────────────────┐
│ Step 6: Persist to Database          │
│ (Save analysis for history)          │
└──────────┬───────────────────────────┘
    │  Saved: Analysis(id=123, user_id=456, ...)
    ▼
┌──────────────────────────────────────┐
│ Step 7: Response Envelope            │
│ (Wrap in standard format)            │
└──────────┬───────────────────────────┘
    │
    ▼
Response: 201 Created
{
  "success": true,
  "message": "Analysis completed successfully",
  "data": {
    "id": 123,
    "text": "قفا نبك من ذكري حبيب ومنزل",
    "normalized_text": "قفا نبك من ذكري حبيب ومنزل",
    "syllable_count": 14,
    "pattern": "∪ - - ∪ - - ∪ - - ∪ - - ∪ -",
    "detected_meter": "الطويل",
    "confidence": 0.92,
    "syllables": [...],
    "taf3ilat": [...],
    "candidates": [...]
  },
  "request_id": "req_7f8a9b0c",
  "timestamp": "2025-11-08T12:34:56Z"
}
```

---

## 3. Input/Output Contracts

### 3.1 Pydantic Request/Response Schemas

```python
# backend/app/schemas/analysis.py
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class AnalysisOptions(BaseModel):
    """Optional analysis parameters."""
    include_taf3ilat: bool = Field(
        default=True,
        description="Include detailed تفاعيل breakdown"
    )
    include_candidates: bool = Field(
        default=True,
        description="Include top-3 meter candidates"
    )
    include_syllables: bool = Field(
        default=True,
        description="Include syllable details"
    )
    top_k_candidates: int = Field(
        default=3,
        ge=1,
        le=5,
        description="Number of meter candidates to return"
    )


class AnalysisRequest(BaseModel):
    """Request schema for POST /analyses."""
    text: str = Field(
        ...,
        min_length=3,
        max_length=1000,
        description="Arabic verse text to analyze",
        example="قفا نبك من ذكري حبيب ومنزل"
    )
    options: Optional[AnalysisOptions] = Field(
        default_factory=AnalysisOptions,
        description="Analysis options"
    )
    
    @validator("text")
    def validate_arabic_text(cls, v: str) -> str:
        """Ensure text contains Arabic characters."""
        import re
        
        # Remove whitespace and punctuation
        clean_text = re.sub(r'[\s\u060C\u061B\u061F]', '', v)
        
        # Check for Arabic characters
        arabic_pattern = r'[\u0600-\u06FF\u0750-\u077F]'
        if not re.search(arabic_pattern, clean_text):
            raise ValueError("Text must contain Arabic characters")
        
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "text": "قفا نبك من ذكري حبيب ومنزل",
                "options": {
                    "include_taf3ilat": True,
                    "include_candidates": True,
                    "top_k_candidates": 3
                }
            }
        }


class SyllableResponse(BaseModel):
    """Syllable detail in response."""
    text: str
    type: str  # CV, CVV, CVC, etc.
    long: bool
    weight: int
    position: int


class Taf3ilaResponse(BaseModel):
    """تفعيلة detail in response."""
    name: str
    variation: str
    pattern: str
    position: int
    confidence: float


class MeterCandidateResponse(BaseModel):
    """Meter candidate detail."""
    meter: str
    confidence: float
    edit_distance: int
    explanation: str


class AnalysisResponse(BaseModel):
    """Response schema for analysis result."""
    id: int = Field(..., description="Unique analysis ID")
    text: str = Field(..., description="Original input text")
    normalized_text: str = Field(..., description="Normalized Arabic text")
    
    syllable_count: int
    pattern: str = Field(..., description="Prosodic pattern (- and ∪)")
    
    detected_meter: str = Field(..., description="Detected Arabic meter")
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Detection confidence (0-1)"
    )
    
    syllables: Optional[List[SyllableResponse]] = None
    taf3ilat: Optional[List[Taf3ilaResponse]] = None
    candidates: Optional[List[MeterCandidateResponse]] = None
    
    processing_time_ms: int = Field(..., description="Processing time in ms")
    created_at: datetime
    
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 123,
                "text": "قفا نبك من ذكري حبيب ومنزل",
                "normalized_text": "قفا نبك من ذكري حبيب ومنزل",
                "syllable_count": 14,
                "pattern": "∪ - - ∪ - - ∪ - - ∪ - - ∪ -",
                "detected_meter": "الطويل",
                "confidence": 0.92,
                "processing_time_ms": 450,
                "created_at": "2025-11-08T12:34:56Z"
            }
        }


class AnalysisListResponse(BaseModel):
    """Response for list of analyses."""
    analyses: List[AnalysisResponse]
    total: int
    page: int
    page_size: int
```

### 3.2 API Endpoint Signatures

```python
# backend/app/api/v1/endpoints/analyze.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(prefix="/analyses", tags=["Analysis"])


@router.post(
    "",
    response_model=AnalysisResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Analyze Arabic verse",
    description="Perform prosodic analysis on Arabic poetry text"
)
async def create_analysis(
    request: AnalysisRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_optional)
) -> AnalysisResponse:
    """
    Analyze Arabic verse and detect prosodic meter.
    
    Performs:
    1. Text normalization
    2. Syllable segmentation
    3. Meter detection
    4. Result persistence
    """
    pass


@router.get(
    "/{analysis_id}",
    response_model=AnalysisResponse,
    summary="Get analysis by ID",
    description="Retrieve a previously saved analysis"
)
async def get_analysis(
    analysis_id: int,
    db: Session = Depends(get_db)
) -> AnalysisResponse:
    """Retrieve analysis by ID."""
    pass


@router.get(
    "",
    response_model=AnalysisListResponse,
    summary="List user analyses",
    description="Retrieve user's analysis history"
)
async def list_analyses(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> AnalysisListResponse:
    """List user's analysis history with pagination."""
    pass
```

---

## 4. Step-by-Step Implementation

### Step 1: Create Analysis Router

```bash
# Create API endpoint file
touch backend/app/api/v1/endpoints/analyze.py
```

### Step 2: Define Pydantic Schemas

Create schemas in `backend/app/schemas/analysis.py` as shown in Section 3.1.

### Step 3: Create Analysis Service

```python
# backend/app/services/analysis_service.py
"""
Analysis service orchestrating prosody pipeline.

Coordinates normalization, segmentation, and meter detection.
"""

import logging
import time
from typing import Optional

from app.nlp.normalizer import ArabicTextNormalizer
from app.prosody.segmenter import SyllableSegmenter
from app.prosody.meter_detector import MeterDetector
from app.schemas.analysis import (
    AnalysisRequest,
    AnalysisResponse,
    SyllableResponse,
    Taf3ilaResponse,
    MeterCandidateResponse
)
from app.models.analysis import Analysis
from app.db.session import SessionLocal

logger = logging.getLogger(__name__)


class AnalysisService:
    """Orchestrate poetry analysis pipeline."""
    
    def __init__(self):
        """Initialize analysis pipeline components."""
        self.normalizer = ArabicTextNormalizer()
        self.segmenter = SyllableSegmenter()
        self.detector = MeterDetector()
    
    def analyze_verse(
        self,
        request: AnalysisRequest,
        user_id: Optional[int] = None
    ) -> AnalysisResponse:
        """
        Analyze Arabic verse through complete pipeline.
        
        Steps:
        1. Normalize text
        2. Segment into syllables
        3. Detect meter
        4. Persist result
        5. Return response
        """
        start_time = time.time()
        
        logger.info(f"Starting analysis for text: {request.text[:50]}...")
        
        # Step 1: Normalize
        normalized_text = self.normalizer.normalize(request.text)
        logger.debug(f"Normalized text: {normalized_text}")
        
        # Step 2: Segment
        seg_result = self.segmenter.segment(normalized_text)
        logger.debug(
            f"Segmented into {seg_result.syllable_count} syllables, "
            f"pattern: {seg_result.pattern[:30]}..."
        )
        
        # Step 3: Detect meter
        meter_result = self.detector.detect(
            seg_result.pattern,
            top_k=request.options.top_k_candidates
        )
        logger.info(
            f"Detected meter: {meter_result.detected_meter.value} "
            f"(confidence: {meter_result.confidence:.2f})"
        )
        
        # Step 4: Build response
        processing_time = int((time.time() - start_time) * 1000)
        
        response_data = {
            "text": request.text,
            "normalized_text": normalized_text,
            "syllable_count": seg_result.syllable_count,
            "pattern": seg_result.pattern,
            "detected_meter": meter_result.detected_meter.value,
            "confidence": meter_result.confidence,
            "processing_time_ms": processing_time
        }
        
        # Include optional details
        if request.options.include_syllables:
            response_data["syllables"] = [
                SyllableResponse(
                    text=s.text,
                    type=s.type.value,
                    long=s.long,
                    weight=s.weight,
                    position=s.position
                )
                for s in seg_result.syllables
            ]
        
        if request.options.include_taf3ilat:
            response_data["taf3ilat"] = [
                Taf3ilaResponse(
                    name=t.name,
                    variation=t.variation,
                    pattern=t.pattern,
                    position=t.position,
                    confidence=t.confidence
                )
                for t in meter_result.taf3ilat
            ]
        
        if request.options.include_candidates:
            response_data["candidates"] = [
                MeterCandidateResponse(
                    meter=c.meter.value,
                    confidence=c.confidence,
                    edit_distance=c.edit_distance,
                    explanation=c.explanation
                )
                for c in meter_result.candidates
            ]
        
        # Step 5: Persist to database
        db = SessionLocal()
        try:
            analysis = Analysis(
                user_id=user_id,
                text=request.text,
                normalized_text=normalized_text,
                pattern=seg_result.pattern,
                detected_meter=meter_result.detected_meter.value,
                confidence=meter_result.confidence,
                syllable_count=seg_result.syllable_count,
                processing_time_ms=processing_time
            )
            db.add(analysis)
            db.commit()
            db.refresh(analysis)
            
            response_data["id"] = analysis.id
            response_data["created_at"] = analysis.created_at
            
            logger.info(f"Analysis saved with ID: {analysis.id}")
        finally:
            db.close()
        
        return AnalysisResponse(**response_data)
```

### Step 4: Implement API Endpoints

```python
# backend/app/api/v1/endpoints/analyze.py
"""
Analysis API endpoints.

Provides REST interface for poetry prosody analysis.
Source: docs/technical/API_SPECIFICATION.yaml:1-200
Source: docs/technical/BACKEND_API.md:1-150
"""

import logging
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.schemas.analysis import (
    AnalysisRequest,
    AnalysisResponse,
    AnalysisListResponse
)
from app.services.analysis_service import AnalysisService
from app.api.dependencies import get_db, get_current_user, get_current_user_optional
from app.models.user import User
from app.models.analysis import Analysis
from app.middleware.response_envelope import envelope_response

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/analyses", tags=["Analysis"])


@router.post(
    "",
    response_model=AnalysisResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Analyze Arabic verse",
    description="""
    Perform prosodic analysis on Arabic poetry text.
    
    Pipeline:
    1. Text normalization (remove diacritics, normalize characters)
    2. Syllable segmentation (CV, CVV, CVC patterns)
    3. Meter detection (fuzzy match against 16 classical meters)
    
    Returns:
    - Detected meter with confidence score
    - Syllable breakdown
    - Prosodic pattern (- and ∪)
    - Top-3 meter candidates
    - تفاعيل decomposition
    """
)
@envelope_response
async def create_analysis(
    request: AnalysisRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
) -> AnalysisResponse:
    """
    Analyze Arabic verse and detect prosodic meter.
    
    Authentication optional - guest users can analyze verses.
    """
    logger.info(
        f"Analysis request from user_id={current_user.id if current_user else 'guest'}"
    )
    
    try:
        service = AnalysisService()
        user_id = current_user.id if current_user else None
        result = service.analyze_verse(request, user_id=user_id)
        
        logger.info(
            f"Analysis successful: meter={result.detected_meter}, "
            f"confidence={result.confidence:.2f}, "
            f"time={result.processing_time_ms}ms"
        )
        
        return result
        
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except Exception as e:
        logger.exception("Unexpected error during analysis")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during analysis"
        )


@router.get(
    "/{analysis_id}",
    response_model=AnalysisResponse,
    summary="Get analysis by ID",
    description="Retrieve a previously saved analysis result"
)
@envelope_response
async def get_analysis(
    analysis_id: int,
    db: Session = Depends(get_db)
) -> AnalysisResponse:
    """Retrieve analysis by ID."""
    logger.debug(f"Fetching analysis ID: {analysis_id}")
    
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
    
    if not analysis:
        logger.warning(f"Analysis not found: {analysis_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Analysis with ID {analysis_id} not found"
        )
    
    # Convert ORM model to Pydantic response
    return AnalysisResponse.from_orm(analysis)


@router.get(
    "",
    response_model=AnalysisListResponse,
    summary="List user analyses",
    description="Retrieve authenticated user's analysis history with pagination"
)
@envelope_response
async def list_analyses(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Max records to return"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> AnalysisListResponse:
    """List user's analysis history with pagination."""
    logger.debug(
        f"Listing analyses for user_id={current_user.id}, "
        f"skip={skip}, limit={limit}"
    )
    
    # Query user's analyses
    query = db.query(Analysis).filter(Analysis.user_id == current_user.id)
    
    total = query.count()
    analyses = query.order_by(Analysis.created_at.desc()).offset(skip).limit(limit).all()
    
    logger.info(f"Found {total} total analyses, returning {len(analyses)}")
    
    return AnalysisListResponse(
        analyses=[AnalysisResponse.from_orm(a) for a in analyses],
        total=total,
        page=skip // limit + 1,
        page_size=limit
    )
```

### Step 5: Register Router in Main App

```python
# backend/app/api/v1/router.py
from fastapi import APIRouter
from app.api.v1.endpoints import analyze, auth, health

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(analyze.router)
api_router.include_router(auth.router)
api_router.include_router(health.router)
```

```python
# backend/app/main.py
from fastapi import FastAPI
from app.api.v1.router import api_router

app = FastAPI(
    title="بَحْر - Arabic Poetry Analysis API",
    version="1.0.0",
    description="Prosodic meter detection for Classical Arabic poetry"
)

# Mount v1 API
app.include_router(api_router, prefix="/api/v1")
```

### Step 6: Test API Endpoint

```bash
# Start server
cd backend
uvicorn app.main:app --reload --port 8000

# Test analysis endpoint
curl -X POST http://localhost:8000/api/v1/analyses \
  -H "Content-Type: application/json" \
  -d '{
    "text": "قفا نبك من ذكري حبيب ومنزل",
    "options": {
      "include_taf3ilat": true,
      "include_candidates": true,
      "top_k_candidates": 3
    }
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "message": "Analysis completed successfully",
  "data": {
    "id": 1,
    "text": "قفا نبك من ذكري حبيب ومنزل",
    "normalized_text": "قفا نبك من ذكري حبيب ومنزل",
    "syllable_count": 14,
    "pattern": "∪ - - ∪ - - ∪ - - ∪ - - ∪ -",
    "detected_meter": "الطويل",
    "confidence": 0.92,
    "processing_time_ms": 450,
    "created_at": "2025-11-08T12:34:56Z",
    "syllables": [...],
    "taf3ilat": [...],
    "candidates": [...]
  },
  "request_id": "req_abc123",
  "timestamp": "2025-11-08T12:34:56Z"
}
```

---

## 5. Reference Implementation (Full Code)

See Step-by-Step Implementation sections above for complete code. Key files:

- **backend/app/schemas/analysis.py** - Pydantic request/response schemas
- **backend/app/services/analysis_service.py** - Analysis pipeline orchestration
- **backend/app/api/v1/endpoints/analyze.py** - FastAPI route handlers

---

## 6. Unit & Integration Tests

### tests/integration/api/test_analyze.py

```python
"""
Integration tests for analysis API endpoints.

Tests full request/response cycle through FastAPI.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestAnalysisAPI:
    """Test suite for /api/v1/analyses endpoints."""
    
    def test_create_analysis_success(self):
        """Test successful analysis creation."""
        response = client.post(
            "/api/v1/analyses",
            json={
                "text": "قفا نبك من ذكري حبيب ومنزل",
                "options": {
                    "include_taf3ilat": True,
                    "include_candidates": True,
                    "top_k_candidates": 3
                }
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        
        assert data["success"] is True
        assert "data" in data
        assert data["data"]["detected_meter"] == "الطويل"
        assert data["data"]["confidence"] >= 0.8
        assert "pattern" in data["data"]
        assert data["data"]["syllable_count"] > 0
    
    def test_create_analysis_minimal_request(self):
        """Test analysis with minimal request body."""
        response = client.post(
            "/api/v1/analyses",
            json={"text": "قفا نبك من ذكري"}
        )
        
        assert response.status_code == 201
        data = response.json()["data"]
        
        assert "id" in data
        assert "detected_meter" in data
        assert "confidence" in data
    
    def test_create_analysis_invalid_text(self):
        """Test validation error for non-Arabic text."""
        response = client.post(
            "/api/v1/analyses",
            json={"text": "Hello World"}
        )
        
        assert response.status_code == 422
        data = response.json()
        assert data["success"] is False
        assert "Arabic characters" in data["message"]
    
    def test_create_analysis_text_too_long(self):
        """Test validation error for text exceeding max length."""
        long_text = "قفا نبك " * 200  # >1000 chars
        
        response = client.post(
            "/api/v1/analyses",
            json={"text": long_text}
        )
        
        assert response.status_code == 422
    
    def test_create_analysis_text_too_short(self):
        """Test validation error for text below min length."""
        response = client.post(
            "/api/v1/analyses",
            json={"text": "قف"}
        )
        
        assert response.status_code == 422
    
    def test_get_analysis_by_id(self):
        """Test retrieving analysis by ID."""
        # Create analysis first
        create_response = client.post(
            "/api/v1/analyses",
            json={"text": "قفا نبك من ذكري حبيب ومنزل"}
        )
        analysis_id = create_response.json()["data"]["id"]
        
        # Retrieve it
        get_response = client.get(f"/api/v1/analyses/{analysis_id}")
        
        assert get_response.status_code == 200
        data = get_response.json()["data"]
        
        assert data["id"] == analysis_id
        assert data["text"] == "قفا نبك من ذكري حبيب ومنزل"
    
    def test_get_analysis_not_found(self):
        """Test 404 for non-existent analysis ID."""
        response = client.get("/api/v1/analyses/999999")
        
        assert response.status_code == 404
        data = response.json()
        assert data["success"] is False
    
    def test_list_analyses_requires_auth(self):
        """Test that listing analyses requires authentication."""
        response = client.get("/api/v1/analyses")
        
        # Should return 401 Unauthorized
        assert response.status_code == 401
    
    def test_list_analyses_with_auth(self, auth_token):
        """Test listing user's analyses with authentication."""
        # Create some analyses
        headers = {"Authorization": f"Bearer {auth_token}"}
        
        for i in range(3):
            client.post(
                "/api/v1/analyses",
                json={"text": f"قفا نبك من ذكري {i}"},
                headers=headers
            )
        
        # List analyses
        response = client.get("/api/v1/analyses", headers=headers)
        
        assert response.status_code == 200
        data = response.json()["data"]
        
        assert "analyses" in data
        assert len(data["analyses"]) >= 3
        assert data["total"] >= 3
    
    def test_list_analyses_pagination(self, auth_token):
        """Test pagination for analysis listing."""
        headers = {"Authorization": f"Bearer {auth_token}"}
        
        response = client.get(
            "/api/v1/analyses?skip=0&limit=10",
            headers=headers
        )
        
        assert response.status_code == 200
        data = response.json()["data"]
        
        assert data["page"] == 1
        assert data["page_size"] == 10
        assert len(data["analyses"]) <= 10


@pytest.fixture
def auth_token():
    """Get authentication token for testing."""
    # Register user
    client.post(
        "/api/v1/auth/register",
        json={
            "username": "test_user",
            "email": "test@example.com",
            "password": "TestPass123",
            "full_name": "Test User"
        }
    )
    
    # Login
    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "test@example.com",
            "password": "TestPass123"
        }
    )
    
    return login_response.json()["data"]["access_token"]
```

---

## 7. CI/CD Pipeline

```yaml
# .github/workflows/analysis-api-tests.yml
name: Analysis API Tests

on:
  push:
    paths:
      - 'backend/app/api/**'
      - 'backend/app/services/**'
      - 'backend/app/schemas/**'
  pull_request:
    branches: [main, develop]

jobs:
  test-api:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: bahr_test
          POSTGRES_PASSWORD: test_password
          POSTGRES_DB: bahr_test
        ports:
          - 5432:5432
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Set up Python 3.11
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
          pip install pytest pytest-cov httpx
      
      - name: Run database migrations
        run: |
          cd backend
          alembic upgrade head
        env:
          DATABASE_URL: postgresql://bahr_test:test_password@localhost/bahr_test
      
      - name: Run API tests
        run: |
          cd backend
          pytest tests/integration/api/test_analyze.py -v \
            --cov=app.api.v1.endpoints.analyze \
            --cov=app.services.analysis_service \
            --cov-report=xml
        env:
          DATABASE_URL: postgresql://bahr_test:test_password@localhost/bahr_test
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./backend/coverage.xml
          flags: analysis-api
```

---

## 8. Deployment Checklist

- [ ] Database migrations applied (analyses table created)
- [ ] Test with 50+ verses from golden dataset
- [ ] Verify P95 latency <600ms
- [ ] Test authentication (optional login)
- [ ] Test pagination (skip/limit parameters)
- [ ] Verify response envelope format
- [ ] Test validation errors (422 responses)
- [ ] Monitor database connection pool
- [ ] Verify OpenAPI docs at /docs
- [ ] Test CORS configuration for frontend

---

## 9. Observability

```python
# backend/app/metrics/analysis_metrics.py
from prometheus_client import Counter, Histogram

# Analysis API metrics
analysis_requests_total = Counter(
    "bahr_analysis_requests_total",
    "Total analysis requests",
    ["endpoint", "status"]
)

analysis_duration_seconds = Histogram(
    "bahr_analysis_duration_seconds",
    "Analysis request duration",
    ["endpoint"],
    buckets=[0.1, 0.3, 0.6, 1.0, 2.0, 5.0]
)

analysis_pipeline_stage_duration = Histogram(
    "bahr_analysis_pipeline_stage_duration_seconds",
    "Duration of each pipeline stage",
    ["stage"],  # normalization, segmentation, detection
    buckets=[0.01, 0.05, 0.1, 0.2, 0.5]
)
```

---

## 10. Security & Safety

- **Input Validation:** Max 1000 chars, Arabic script only
- **Rate Limiting:** 60 req/min per IP for guest users
- **Authentication:** Optional for analysis, required for history
- **SQL Injection:** Protected by SQLAlchemy ORM
- **CORS:** Configure allowed origins in production

---

## 11. Backwards Compatibility

- **None** - Initial implementation

---

## 12. Source Documentation Citations

1. **docs/technical/API_SPECIFICATION.yaml:1-200** - OpenAPI schema
2. **docs/technical/BACKEND_API.md:1-150** - Backend architecture
3. **claude.md:510-645** - Implementation code templates
4. **implementation-guides/IMPROVED_PROMPT.md:531-563** - Feature specification

---

**Implementation Complete!** ✅  
**Estimated Time:** 18-22 hours  
**Test Coverage Target:** ≥ 80%  
**Performance Target:** P95 <600ms
