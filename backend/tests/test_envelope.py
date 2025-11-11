import os
import sys
from fastapi.testclient import TestClient

# Import from app module directly (works in both local and Docker/Railway contexts)
from app.main import app


client = TestClient(app)


def test_analyze_envelope_success_has_request_id_and_meta():
    resp = client.post("/api/v1/analyze", json={"text": "قفا نبك من ذكرى حبيب ومنزل"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["success"] is True
    assert body["error"] is None
    assert body["data"] is not None
    assert "meta" in body and isinstance(body["meta"], dict)
    assert "request_id" in body["meta"]
    # header echo
    assert resp.headers.get("X-Request-ID")


def test_request_id_propagation_from_header():
    rid = "fixedrid12345"
    resp = client.post(
        "/api/v1/analyze",
        headers={"X-Request-ID": rid},
        json={"text": "قفا نبك من ذكرى حبيب ومنزل"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["meta"]["request_id"] == rid
    assert resp.headers.get("X-Request-ID") == rid


def test_validation_422_for_non_arabic():
    resp = client.post("/api/v1/analyze", json={"text": "hello world"})
    assert resp.status_code == 422
    body = resp.json()
    assert body["success"] is False
    assert body["error"]["code"] == "ERR_INPUT_001"


def test_validation_error_envelope_on_missing_field():
    # Missing required 'text' should trigger RequestValidationError handled as envelope
    resp = client.post("/api/v1/analyze", json={})
    assert resp.status_code == 422
    body = resp.json()
    assert body["success"] is False
    assert body["error"]["code"] == "ERR_INPUT_003"  # invalid format
    assert "meta" in body and "request_id" in body["meta"]


def test_content_language_header_and_localization():
    # Arabic default
    resp_ar = client.post("/api/v1/analyze", json={"text": "hello"})
    assert resp_ar.status_code == 422
    assert resp_ar.headers.get("Content-Language") == "ar"
    # English requested
    resp_en = client.post(
        "/api/v1/analyze",
        headers={"Accept-Language": "en"},
        json={"text": "hello"},
    )
    assert resp_en.status_code == 422
    assert resp_en.headers.get("Content-Language") == "en"


def test_metrics_endpoint_available():
    r = client.get("/metrics")
    assert r.status_code == 200
    assert "text/plain" in r.headers.get("content-type", "")


def test_normalization_removes_diacritics_by_default():
    text = "قَفا نَبْكِ"
    resp = client.post("/api/v1/analyze", json={"text": text})
    assert resp.status_code == 200
    body = resp.json()
    norm = body["data"]["normalized_text"]
    assert "َ" not in norm and "ْ" not in norm


def test_normalization_keep_diacritics_when_flag_false():
    text = "قَفا نَبْكِ"
    resp = client.post("/api/v1/analyze", json={"text": text, "options": {"remove_diacritics": False}})
    assert resp.status_code == 200
    body = resp.json()
    norm = body["data"]["normalized_text"]
    # Diacritics should remain
    assert "َ" in norm or "ْ" in norm