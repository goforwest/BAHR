"""
Analyze endpoint for prosodic analysis of Arabic poetry.
"""

import logging
from fastapi import APIRouter, HTTPException, status
from app.schemas.analyze import AnalyzeRequest, AnalyzeResponse, BahrInfo
from app.core.normalization import normalize_arabic_text
from app.core.taqti3 import perform_taqti3
from app.core.bahr_detector import BahrDetector
from app.db.redis import cache_get, cache_set, generate_cache_key

logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize bahr detector (singleton)
bahr_detector = BahrDetector()


@router.post(
    "/",
    response_model=AnalyzeResponse,
    status_code=status.HTTP_200_OK,
    summary="Analyze Arabic verse",
    description="Perform prosodic analysis on Arabic poetry verse, including taqti3 (scansion) and bahr (meter) detection.",
    responses={
        200: {
            "description": "Successful analysis",
            "content": {
                "application/json": {
                    "example": {
                        "text": "إذا غامَرتَ في شَرَفٍ مَرومِ",
                        "taqti3": "فعولن مفاعيلن فعولن مفاعيلن",
                        "bahr": {
                            "name_ar": "الطويل",
                            "name_en": "at-Tawil",
                            "confidence": 0.95
                        },
                        "errors": [],
                        "suggestions": ["التقطيع دقيق ومتسق"],
                        "score": 95.0
                    }
                }
            }
        },
        400: {"description": "Invalid input"},
        500: {"description": "Server error"}
    }
)
async def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    """
    Analyze Arabic verse for prosodic structure and meter.
    
    This endpoint performs the following steps:
    1. Normalizes the input text
    2. Checks Redis cache for previous analysis
    3. If cache miss: performs taqti3 (scansion) and detects bahr (meter)
    4. Calculates quality score
    5. Caches the result (TTL: 24 hours)
    6. Returns analysis response
    
    Args:
        request: Analysis request with text and options
        
    Returns:
        AnalyzeResponse with taqti3, bahr detection, and quality score
        
    Raises:
        HTTPException: 400 for invalid input, 500 for server errors
    """
    try:
        # Edge case: Very long text (beyond validation but still problematic)
        if len(request.text) > 5000:
            logger.warning(f"Text length {len(request.text)} exceeds recommended limit")
        
        # Step a: Normalize text
        logger.info(f"Analyzing verse: {request.text[:50]}...")
        
        try:
            normalized_text = normalize_arabic_text(
                request.text,
                remove_tashkeel=False,  # Keep diacritics for accurate analysis
                normalize_hamzas=True,
                normalize_alefs=True
            )
        except Exception as e:
            logger.error(f"Text normalization failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to normalize text: {str(e)}"
            )
        
        # Edge case: Empty text after normalization
        if not normalized_text or not normalized_text.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Text is empty after normalization"
            )
        
        # Step b: Check Redis cache (with graceful degradation)
        cache_key = generate_cache_key(normalized_text)
        cached_result = None
        
        try:
            cached_result = await cache_get(cache_key)
            if cached_result:
                logger.info(f"Cache hit for key: {cache_key}")
                return AnalyzeResponse(**cached_result)
        except Exception as e:
            # Cache failure should not break the request
            logger.warning(f"Cache read failed (continuing without cache): {e}")
        
        logger.info(f"Cache miss for key: {cache_key}, performing analysis")
        
        # Step c: Perform taqti3 (scansion)
        try:
            taqti3_result = perform_taqti3(normalized_text, normalize=False)
            
            # Edge case: Empty taqti3 result
            if not taqti3_result or not taqti3_result.strip():
                logger.warning("Taqti3 returned empty result")
                taqti3_result = "غير محدد"  # "Not determined"
                
        except ValueError as e:
            logger.error(f"Taqti3 validation error: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid verse structure: {str(e)}"
            )
        except Exception as e:
            logger.error(f"Taqti3 processing failed: {e}", exc_info=True)
            # Provide graceful fallback
            taqti3_result = "خطأ في التحليل"  # "Analysis error"
        
        # Step d: Detect bahr (meter) with error handling
        bahr_info = None
        confidence = 0.0
        
        if request.detect_bahr:
            try:
                detected_bahr = bahr_detector.analyze_verse(normalized_text)
                if detected_bahr:
                    bahr_info = BahrInfo(
                        name_ar=detected_bahr.name_ar,
                        name_en=detected_bahr.name_en,
                        confidence=detected_bahr.confidence
                    )
                    confidence = detected_bahr.confidence
                    logger.info(f"Detected bahr: {bahr_info.name_ar} (confidence: {confidence:.2f})")
                else:
                    logger.info("No bahr detected with sufficient confidence")
            except Exception as e:
                logger.error(f"Bahr detection failed: {e}", exc_info=True)
                # Continue without bahr detection - don't fail the whole request
        
        # Step e: Calculate score (confidence * 100)
        score = round(confidence * 100, 2) if confidence > 0 else 0.0
        
        # Edge case: Ensure score is within valid range
        score = max(0.0, min(100.0, score))
        
        # Generate suggestions
        suggestions = []
        if confidence >= 0.9:
            suggestions.append("التقطيع دقيق ومتسق")
        elif confidence >= 0.7:
            suggestions.append("التقطيع جيد مع بعض الاختلافات البسيطة")
        elif confidence > 0:
            suggestions.append("قد يحتاج البيت إلى مراجعة للتقطيع")
        
        if not bahr_info and request.detect_bahr:
            suggestions.append("لم يتم التعرف على البحر بثقة كافية")
        
        # Step f: Build response
        response = AnalyzeResponse(
            text=request.text,
            taqti3=taqti3_result,
            bahr=bahr_info,
            errors=[],
            suggestions=suggestions if request.suggest_corrections else [],
            score=score
        )
        
        # Step g: Cache result (TTL: 24 hours = 86400 seconds) with error handling
        try:
            response_dict = response.model_dump()
            await cache_set(cache_key, response_dict, ttl=86400)
            logger.info(f"Cached analysis result with key: {cache_key}")
        except Exception as e:
            # Cache failure should not break the response
            logger.warning(f"Failed to cache result: {e}")
        
        # Step h: Return response
        return response
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except ValueError as e:
        # Handle validation errors
        logger.error(f"Validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        # Handle unexpected server errors
        logger.error(f"Unexpected error during analysis: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during analysis. Please try again."
        )
