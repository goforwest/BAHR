"""
Pytest configuration and shared fixtures for Golden Set tests.
"""

import json
import pytest
from pathlib import Path
from typing import List, Dict, Any


# ============================================================================
# Path Configuration
# ============================================================================

@pytest.fixture(scope="session")
def dataset_root() -> Path:
    """Root directory of the dataset."""
    return Path(__file__).parent.parent


@pytest.fixture(scope="session")
def evaluation_dir(dataset_root) -> Path:
    """Evaluation directory containing golden set."""
    return dataset_root / "evaluation"


@pytest.fixture(scope="session")
def scripts_dir(dataset_root) -> Path:
    """Scripts directory."""
    return dataset_root / "scripts"


# ============================================================================
# Golden Set Data Fixtures
# ============================================================================

@pytest.fixture(scope="session")
def golden_set_path(evaluation_dir) -> Path:
    """Path to golden set JSONL file."""
    return evaluation_dir / "golden_set_v0_20_complete.jsonl"


@pytest.fixture(scope="session")
def schema_path(evaluation_dir) -> Path:
    """Path to JSON schema file."""
    return evaluation_dir / "golden_set_schema.json"


@pytest.fixture(scope="session")
def metadata_path(evaluation_dir) -> Path:
    """Path to metadata JSON file."""
    return evaluation_dir / "golden_set_metadata.json"


@pytest.fixture(scope="session")
def golden_set_verses(golden_set_path) -> List[Dict[str, Any]]:
    """Load all verses from golden set."""
    verses = []
    with open(golden_set_path, 'r', encoding='utf-8') as f:
        for line in f:
            verses.append(json.loads(line))
    return verses


@pytest.fixture(scope="session")
def golden_set_schema(schema_path) -> Dict[str, Any]:
    """Load JSON schema."""
    with open(schema_path, 'r', encoding='utf-8') as f:
        return json.load(f)


@pytest.fixture(scope="session")
def golden_set_metadata(metadata_path) -> Dict[str, Any]:
    """Load metadata."""
    with open(metadata_path, 'r', encoding='utf-8') as f:
        return json.load(f)


# ============================================================================
# Sample Data Fixtures
# ============================================================================

@pytest.fixture
def sample_verse() -> Dict[str, Any]:
    """Sample verse for testing."""
    return {
        "verse_id": "golden_001",
        "text": "قِفا نَبْكِ مِن ذِكرى حَبيبٍ ومَنْزِلِ",
        "normalized_text": "قفا نبك من ذكري حبيب ومنزل",
        "meter": "الطويل",
        "poet": "امرؤ القيس",
        "source": "المعلقة",
        "era": "classical",
        "confidence": 0.98,
        "notes": "بيت افتتاحي قياسي واضح التفعيلات",
        "taqti3": "فَعُولُنْ مَفَاعِيلُنْ فَعُولُنْ مَفَاعِيلُنْ",
        "expected_tafail": ["فعولن", "مفاعيلن", "فعولن", "مفاعيلن"],
        "syllable_pattern": "- u - - | - u u - | - u - - | - u u -",
        "syllable_count": 16,
        "edge_case_type": "perfect_match",
        "difficulty_level": "easy",
        "validation": {
            "verified_by": "manual_expert_review",
            "verified_date": "2025-11-09",
            "reference_sources": [
                "كتاب العروض للخليل",
                "الكافي في العروض والقوافي"
            ]
        },
        "metadata": {
            "created_at": "2025-11-09",
            "updated_at": "2025-11-09",
            "version": "0.20"
        }
    }


@pytest.fixture
def tawil_verses(golden_set_verses) -> List[Dict[str, Any]]:
    """All verses in الطويل meter."""
    return [v for v in golden_set_verses if v['meter'] == 'الطويل']


@pytest.fixture
def easy_verses(golden_set_verses) -> List[Dict[str, Any]]:
    """All easy difficulty verses."""
    return [v for v in golden_set_verses if v['difficulty_level'] == 'easy']


@pytest.fixture
def high_confidence_verses(golden_set_verses) -> List[Dict[str, Any]]:
    """All high confidence verses (≥0.95)."""
    return [v for v in golden_set_verses if v['confidence'] >= 0.95]


# ============================================================================
# Meter Reference Data
# ============================================================================

@pytest.fixture(scope="session")
def meter_names() -> List[str]:
    """List of all 16 classical Arabic meters."""
    return [
        "الطويل", "المديد", "البسيط", "الوافر",
        "الكامل", "الهزج", "الرجز", "الرمل",
        "السريع", "المنسرح", "الخفيف", "المضارع",
        "المقتضب", "المجتث", "المتقارب", "المتدارك"
    ]


@pytest.fixture(scope="session")
def covered_meters() -> List[str]:
    """Meters covered in golden set v0.20."""
    return [
        "الطويل", "البسيط", "الكامل", "الرجز",
        "الرمل", "المتقارب", "الخفيف", "الهزج"
    ]


# ============================================================================
# Test Markers
# ============================================================================

def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers", "unit: Unit tests (fast)"
    )
    config.addinivalue_line(
        "markers", "integration: Integration tests (slower)"
    )
    config.addinivalue_line(
        "markers", "schema: Schema validation tests"
    )
    config.addinivalue_line(
        "markers", "quality: Data quality tests"
    )


# ============================================================================
# Test Helpers
# ============================================================================

@pytest.fixture
def assert_valid_verse_id():
    """Helper to validate verse ID format."""
    def _assert(verse_id: str):
        import re
        pattern = r'^(golden|train|test|dev)_\d{3,}$'
        assert re.match(pattern, verse_id), f"Invalid verse_id format: {verse_id}"
    return _assert


@pytest.fixture
def assert_valid_syllable_pattern():
    """Helper to validate syllable pattern format."""
    def _assert(pattern: str):
        import re
        # Pattern should only contain -, u, space, and |
        pattern_regex = r'^[\-u \|]+$'
        assert re.match(pattern_regex, pattern), f"Invalid syllable pattern: {pattern}"
    return _assert
