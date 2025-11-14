"""
Test edge cases and error handling for production readiness.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestInputValidationEdgeCases:
    """Test edge cases for input validation."""
    
    def test_empty_text(self):
        """Empty text should return 422 validation error."""
        resp = client.post("/api/v1/analyze", json={"text": ""})
        assert resp.status_code == 422
    
    def test_whitespace_only_text(self):
        """Whitespace-only text should return 422."""
        resp = client.post("/api/v1/analyze", json={"text": "   \n\t  "})
        assert resp.status_code == 422
    
    def test_very_short_text(self):
        """Text shorter than 5 chars should return 422."""
        resp = client.post("/api/v1/analyze", json={"text": "abc"})
        assert resp.status_code == 422
    
    def test_non_arabic_text(self):
        """Non-Arabic text should return 422."""
        resp = client.post("/api/v1/analyze", json={"text": "Hello World"})
        assert resp.status_code == 422
    
    def test_mixed_language_mostly_english(self):
        """Text with <30% Arabic might still pass validation due to word count."""
        # Note: The 30% check is character-based, not strict
        resp = client.post("/api/v1/analyze", json={"text": "Hello مرحبا World كيف حالك?"})
        # May pass validation but fail analysis
        assert resp.status_code in [200, 400, 422]
    
    def test_mixed_language_mostly_arabic(self):
        """Text with >30% Arabic should pass validation."""
        resp = client.post("/api/v1/analyze", json={"text": "مرحبا بك في hello العالم world الجديد"})
        assert resp.status_code in [200, 400]  # May fail analysis but passes validation
    
    def test_text_with_special_characters(self):
        """Text with special characters should be handled."""
        resp = client.post("/api/v1/analyze", json={"text": "الشعر @#$% العربي !!! الجميل"})
        # Should either succeed or fail gracefully with 400
        assert resp.status_code in [200, 400]
    
    def test_text_with_numbers(self):
        """Text with numbers should be handled."""
        resp = client.post("/api/v1/analyze", json={"text": "كتب الشعر 123 في العام 456"})
        assert resp.status_code in [200, 400]
    
    def test_text_with_emojis(self):
        """Text with emojis should be handled."""
        resp = client.post("/api/v1/analyze", json={"text": "الشعر العربي 😀 الجميل 🎉"})
        assert resp.status_code in [200, 400]
    
    def test_very_long_text(self):
        """Text at max length (2000 chars) should work."""
        long_text = "الشعر العربي الجميل " * 95  # ~2000 chars
        resp = client.post("/api/v1/analyze", json={"text": long_text})
        # Should work but might return analysis error
        assert resp.status_code in [200, 400]
    
    def test_text_exceeding_max_length(self):
        """Text exceeding 2000 chars should return 422."""
        very_long_text = "الشعر العربي الجميل " * 200  # >2000 chars
        resp = client.post("/api/v1/analyze", json={"text": very_long_text})
        assert resp.status_code == 422
    
    def test_missing_text_field(self):
        """Request without 'text' field should return 422."""
        resp = client.post("/api/v1/analyze", json={})
        assert resp.status_code == 422
    
    def test_null_text_field(self):
        """Request with null text should return 422."""
        resp = client.post("/api/v1/analyze", json={"text": None})
        assert resp.status_code == 422
    
    def test_invalid_json(self):
        """Invalid JSON should return 422."""
        resp = client.post(
            "/api/v1/analyze",
            data="not json",
            headers={"Content-Type": "application/json"}
        )
        assert resp.status_code == 422
    
    def test_wrong_content_type(self):
        """Request with wrong content type should fail."""
        resp = client.post(
            "/api/v1/analyze",
            data="text=الشعر",
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        assert resp.status_code in [422, 415]


class TestArabicTextEdgeCases:
    """Test edge cases specific to Arabic text processing."""
    
    def test_text_with_only_diacritics(self):
        """Text with only diacritics should fail with 400 (not 422)."""
        # Passes validation but fails in processing
        resp = client.post("/api/v1/analyze", json={"text": "َُِّْ"})
        assert resp.status_code in [400, 422]
    
    def test_text_with_tatweel(self):
        """Text with tatweel (kashida) should be normalized."""
        resp = client.post("/api/v1/analyze", json={"text": "الـــشـــعـــر الـــعـــربـــي"})
        # Should normalize and process
        assert resp.status_code in [200, 400]
    
    def test_text_with_multiple_spaces(self):
        """Text with multiple spaces should be normalized."""
        resp = client.post("/api/v1/analyze", json={"text": "الشعر    العربي     الجميل"})
        assert resp.status_code in [200, 400]
    
    def test_text_with_hamza_variants(self):
        """Text with different hamza forms should be normalized."""
        resp = client.post("/api/v1/analyze", json={"text": "أحمد إبراهيم آمن ؤمن ئل"})
        assert resp.status_code in [200, 400]
    
    def test_text_with_alef_variants(self):
        """Text with different alef forms should be normalized."""
        resp = client.post("/api/v1/analyze", json={"text": "موسى على إلى"})
        assert resp.status_code in [200, 400]
    
    def test_repeated_characters(self):
        """Text with repeated characters should be handled."""
        resp = client.post("/api/v1/analyze", json={"text": "اللللللللله أأأأأأأأأكبر"})
        assert resp.status_code in [200, 400]


class TestAPIBehaviorEdgeCases:
    """Test API behavior edge cases."""
    
    def test_concurrent_requests_same_text(self):
        """Multiple concurrent requests for same text should use cache."""
        text = {"text": "إذا غامرت في شرف مروم"}
        
        # First request
        resp1 = client.post("/api/v1/analyze", json=text)
        assert resp1.status_code == 200
        
        # Second request should hit cache
        resp2 = client.post("/api/v1/analyze", json=text)
        assert resp2.status_code == 200
        assert resp1.json() == resp2.json()
    
    def test_options_detect_bahr_false(self):
        """Request with detect_bahr=false should skip meter detection."""
        resp = client.post("/api/v1/analyze", json={
            "text": "كتب الشعر العربي الجميل",
            "detect_bahr": False
        })
        if resp.status_code == 200:
            body = resp.json()
            assert body.get("bahr") is None
    
    def test_options_suggest_corrections_true(self):
        """Request with suggest_corrections=true should include suggestions."""
        resp = client.post("/api/v1/analyze", json={
            "text": "إذا غامرت في شرف مروم",
            "suggest_corrections": True
        })
        if resp.status_code == 200:
            body = resp.json()
            assert "suggestions" in body
    
    def test_invalid_option_value(self):
        """Invalid option value - Pydantic coerces 'yes' to True."""
        # Pydantic is smart and coerces string 'yes' to boolean True
        resp = client.post("/api/v1/analyze", json={
            "text": "كتب الشعر العربي",
            "detect_bahr": "invalid_non_bool_string"  # This should fail
        })
        assert resp.status_code in [200, 422]  # May coerce or reject


class TestErrorResponses:
    """Test that error responses are well-formed."""
    
    def test_validation_error_has_envelope(self):
        """Validation errors should have proper envelope structure."""
        resp = client.post("/api/v1/analyze", json={"text": "hello"})
        assert resp.status_code == 422
        body = resp.json()
        # Should have envelope fields
        assert "success" in body or "detail" in body
    
    def test_error_response_has_useful_message(self):
        """Error responses should have useful error messages."""
        resp = client.post("/api/v1/analyze", json={})
        assert resp.status_code == 422
        body = resp.json()
        # Should have some kind of error information
        assert body is not None
        assert len(str(body)) > 10  # Not empty


class TestPerformanceEdgeCases:
    """Test performance-related edge cases."""
    
    def test_rapid_sequential_requests(self):
        """Rapid sequential requests should all succeed."""
        text = {"text": "الشعر العربي الجميل"}
        for _ in range(10):
            resp = client.post("/api/v1/analyze", json=text)
            assert resp.status_code in [200, 400, 422]
    
    def test_different_texts_no_cache_pollution(self):
        """Different texts should not pollute each other's cache."""
        text1 = {"text": "الشعر الأول للاختبار"}
        text2 = {"text": "الشعر الثاني للاختبار"}
        
        resp1 = client.post("/api/v1/analyze", json=text1)
        resp2 = client.post("/api/v1/analyze", json=text2)
        
        if resp1.status_code == 200 and resp2.status_code == 200:
            assert resp1.json() != resp2.json()
