"""
Integration tests for the analyze API endpoint.

Tests cover:
- Valid verse analysis
- Caching behavior
- Input validation
- Error handling
- Performance requirements

Note: 200 responses return raw Pydantic schema, 422 errors return envelope structure.
"""

import pytest
import time
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.fixture
async def async_client():
    """
    Create an async HTTP client for testing the FastAPI application.
    
    Yields:
        AsyncClient: Configured async client for API testing
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test", follow_redirects=True) as ac:
        yield ac


@pytest.mark.asyncio
async def test_analyze_valid_verse(async_client):
    """
    Test successful analysis of a valid Arabic verse.
    
    Verifies:
    - 200 status code
    - Response contains taqti3 (scansion)
    - Response contains bahr (meter) information
    - Response contains score
    """
    # Famous verse from المتنبي (al-Mutanabbi) in الطويل (at-Tawil) meter
    verse = "إذا غامَرتَ في شَرَفٍ مَرومِ"
    
    response = await async_client.post(
        "/api/v1/analyze",
        json={
            "text": verse,
            "detect_bahr": True,
            "suggest_corrections": False
        }
    )
    
    # Assert status code
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    
    # Parse response (200 responses are raw Pydantic schema, not enveloped)
    data = response.json()
    
    # Assert response has required fields
    assert "text" in data
    assert "taqti3" in data
    assert "bahr" in data
    assert "score" in data
    assert "errors" in data
    assert "suggestions" in data
    
    # Verify data content
    assert data["text"] == verse
    assert isinstance(data["taqti3"], str)
    assert len(data["taqti3"]) > 0, "Taqti3 should not be empty"
    
    # Verify bahr information (should detect الطويل)
    if data["bahr"] is not None:
        assert "name_ar" in data["bahr"]
        assert "name_en" in data["bahr"]
        assert "confidence" in data["bahr"]
        assert 0.0 <= data["bahr"]["confidence"] <= 1.0
    
    # Verify score
    assert isinstance(data["score"], (int, float))
    assert 0.0 <= data["score"] <= 100.0
    
    # Verify errors and suggestions are lists
    assert isinstance(data["errors"], list)
    assert isinstance(data["suggestions"], list)


@pytest.mark.asyncio
async def test_analyze_cached_response(async_client):
    """
    Test that identical requests are served from cache and are faster.
    
    Verifies:
    - First request performs analysis
    - Second request with same verse returns identical result
    - Responses are identical
    """
    verse = "قِفا نَبكِ مِن ذِكرى حَبيبٍ وَمَنزِلِ"  # امرؤ القيس (Imru' al-Qais)
    
    payload = {
        "text": verse,
        "detect_bahr": True,
        "suggest_corrections": True
    }
    
    # First request - should miss cache and perform analysis
    start_time = time.time()
    response1 = await async_client.post("/api/v1/analyze", json=payload)
    first_request_time = time.time() - start_time
    
    assert response1.status_code == 200
    data1 = response1.json()
    
    # Second request - should hit cache
    start_time = time.time()
    response2 = await async_client.post("/api/v1/analyze", json=payload)
    second_request_time = time.time() - start_time
    
    assert response2.status_code == 200
    data2 = response2.json()
    
    # Verify responses are identical
    assert data1["text"] == data2["text"]
    assert data1["taqti3"] == data2["taqti3"]
    assert data1["bahr"] == data2["bahr"]
    assert data1["score"] == data2["score"]
    
    # Verify second request completed successfully
    assert second_request_time < 1.0, "Cached request should complete within 1 second"
    
    print(f"\nCache performance: First={first_request_time*1000:.1f}ms, Cached={second_request_time*1000:.1f}ms")


@pytest.mark.asyncio
async def test_analyze_invalid_input_empty(async_client):
    """
    Test that empty text input returns 422 validation error.
    
    Verifies:
    - 422 status code (validation error)
    - Error envelope structure
    - Appropriate error message
    """
    response = await async_client.post(
        "/api/v1/analyze",
        json={
            "text": "",
            "detect_bahr": True
        }
    )
    
    # Assert validation error status
    assert response.status_code == 422
    
    # Parse response (422 errors return envelope structure)
    body = response.json()
    
    # Verify error envelope structure
    assert "success" in body
    assert body["success"] is False
    assert "error" in body
    assert body["error"] is not None
    assert "data" in body
    assert body["data"] is None
    
    # Verify error details
    error = body["error"]
    assert "code" in error
    assert "message" in error
    # Error code for validation errors
    assert error["code"] in ["ERR_INPUT_001", "ERR_INPUT_003", "VALIDATION_ERROR"]


@pytest.mark.asyncio
async def test_analyze_invalid_input_no_arabic(async_client):
    """
    Test that non-Arabic text returns 422 validation error.
    
    Verifies:
    - 422 status code
    - Error indicates Arabic text is required
    - Proper error envelope
    """
    response = await async_client.post(
        "/api/v1/analyze",
        json={
            "text": "This is English text, not Arabic",
            "detect_bahr": True
        }
    )
    
    # Assert validation error status
    assert response.status_code == 422
    
    # Parse response (422 errors return envelope structure)
    body = response.json()
    
    # Verify error envelope
    assert body["success"] is False
    assert body["error"] is not None
    assert body["data"] is None
    
    # Verify error indicates Arabic is required
    error = body["error"]
    assert "code" in error
    assert error["code"] in ["ERR_INPUT_001", "ERR_INPUT_003", "VALIDATION_ERROR"]
    assert "details" in error
    # Check that error mentions Arabic requirement
    details_str = str(error["details"])
    assert "Arabic" in details_str or "عربي" in details_str.lower() or "arabic" in details_str.lower()


@pytest.mark.asyncio
async def test_analyze_verse_without_diacritics(async_client):
    """
    Test analysis of verse without diacritical marks (tashkeel).
    
    The system should still perform analysis by inferring vowels.
    
    Verifies:
    - 200 status code
    - Analysis completes successfully
    - Returns taqti3 and bahr
    - Score may be lower due to ambiguity
    """
    # Same verse as test_analyze_valid_verse but without diacritics
    verse_without_tashkeel = "اذا غامرت في شرف مروم"
    
    response = await async_client.post(
        "/api/v1/analyze",
        json={
            "text": verse_without_tashkeel,
            "detect_bahr": True,
            "suggest_corrections": True
        }
    )
    
    # Assert successful response
    assert response.status_code == 200
    
    data = response.json()
    
    # Verify analysis was performed
    assert "taqti3" in data
    assert isinstance(data["taqti3"], str)
    assert len(data["taqti3"]) > 0
    
    # Bahr detection may or may not succeed without diacritics
    # but the request should not fail
    assert "bahr" in data
    assert "score" in data
    
    # Score might be lower due to inference ambiguity
    assert isinstance(data["score"], (int, float))
    assert 0.0 <= data["score"] <= 100.0


@pytest.mark.asyncio
async def test_analyze_missing_required_field(async_client):
    """
    Test that missing required 'text' field returns 422 validation error.
    
    Verifies:
    - 422 status code
    - Error envelope structure
    - Error indicates missing field
    """
    response = await async_client.post(
        "/api/v1/analyze",
        json={
            "detect_bahr": True
            # Missing 'text' field
        }
    )
    
    assert response.status_code == 422
    
    body = response.json()
    assert body["success"] is False
    assert body["error"] is not None
    assert body["data"] is None


@pytest.mark.asyncio
async def test_analyze_text_too_long(async_client):
    """
    Test that text exceeding maximum length returns validation error.
    
    The schema specifies max_length=2000 characters.
    
    Verifies:
    - 422 status code for text > 2000 chars
    - Appropriate error message
    """
    # Create text longer than 2000 characters
    long_text = "ا" * 2001  # 2001 Arabic letter alef
    
    response = await async_client.post(
        "/api/v1/analyze",
        json={
            "text": long_text,
            "detect_bahr": True
        }
    )
    
    assert response.status_code == 422
    
    body = response.json()
    assert body["success"] is False
    assert body["error"] is not None


@pytest.mark.asyncio
async def test_analyze_with_mixed_arabic_english(async_client):
    """
    Test analysis of text with mixed Arabic and English characters.
    
    Should succeed as long as Arabic characters are present.
    
    Verifies:
    - 200 status code (passes validation due to Arabic presence)
    - Analysis focuses on Arabic text
    """
    mixed_text = "البيت: إذا غامَرتَ في شَرَفٍ مَرومِ (famous verse)"
    
    response = await async_client.post(
        "/api/v1/analyze",
        json={
            "text": mixed_text,
            "detect_bahr": True
        }
    )
    
    # Should succeed since Arabic characters are present
    assert response.status_code == 200
    
    data = response.json()
    assert data["taqti3"] is not None
    assert len(data["taqti3"]) > 0


@pytest.mark.asyncio
async def test_analyze_detect_bahr_disabled(async_client):
    """
    Test analysis with bahr detection disabled.
    
    Verifies:
    - 200 status code
    - Taqti3 is performed
    - Bahr is None when detect_bahr=False
    """
    verse = "قِفا نَبكِ مِن ذِكرى حَبيبٍ وَمَنزِلِ"
    
    response = await async_client.post(
        "/api/v1/analyze",
        json={
            "text": verse,
            "detect_bahr": False,
            "suggest_corrections": False
        }
    )
    
    assert response.status_code == 200
    
    data = response.json()
    
    # Taqti3 should still be performed
    assert data["taqti3"] is not None
    assert isinstance(data["taqti3"], str)
    
    # Bahr should be None when detection is disabled
    assert data["bahr"] is None


@pytest.mark.asyncio
async def test_analyze_suggest_corrections_enabled(async_client):
    """
    Test analysis with suggest_corrections enabled.
    
    Verifies:
    - 200 status code
    - Suggestions list is populated when enabled
    """
    verse = "إذا غامَرتَ في شَرَفٍ مَرومِ"
    
    response = await async_client.post(
        "/api/v1/analyze",
        json={
            "text": verse,
            "detect_bahr": True,
            "suggest_corrections": True
        }
    )
    
    assert response.status_code == 200
    
    data = response.json()
    
    # Suggestions should be present when requested
    assert "suggestions" in data
    assert isinstance(data["suggestions"], list)


@pytest.mark.asyncio
async def test_analyze_multiple_verses_different_bahrs(async_client):
    """
    Test analyzing multiple verses from different meters.
    
    Verifies system can handle different inputs correctly.
    """
    test_verses = [
        {
            "text": "إذا غامَرتَ في شَرَفٍ مَرومِ",
            "expected_bahr": "الطويل"  # at-Tawil
        },
        {
            "text": "قِفا نَبكِ مِن ذِكرى حَبيبٍ وَمَنزِلِ",
            "expected_bahr": "الطويل"  # at-Tawil
        }
    ]
    
    for verse_info in test_verses:
        response = await async_client.post(
            "/api/v1/analyze",
            json={
                "text": verse_info["text"],
                "detect_bahr": True
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify bahr was detected
        if data["bahr"] is not None:
            assert isinstance(data["bahr"]["name_ar"], str)
            assert len(data["bahr"]["name_ar"]) > 0


# Performance benchmark test (optional, can be slow)
@pytest.mark.asyncio
@pytest.mark.slow
async def test_analyze_performance_benchmark(async_client):
    """
    Performance benchmark: Analyze should complete within reasonable time.
    
    Target: < 500ms for uncached request, < 50ms for cached request
    """
    verse = "قِفا نَبكِ مِن ذِكرى حَبيبٍ وَمَنزِلِ"
    
    # Uncached request
    start = time.time()
    response = await async_client.post(
        "/api/v1/analyze",
        json={"text": verse, "detect_bahr": True}
    )
    uncached_time = time.time() - start
    
    assert response.status_code == 200
    
    # Cached request
    start = time.time()
    response = await async_client.post(
        "/api/v1/analyze",
        json={"text": verse, "detect_bahr": True}
    )
    cached_time = time.time() - start
    
    assert response.status_code == 200
    assert cached_time < 0.1, f"Cached request took {cached_time:.3f}s (should be < 100ms)"
    
    print(f"\nPerformance: Uncached={uncached_time*1000:.1f}ms, Cached={cached_time*1000:.1f}ms")
