"""
Tests for Tafila class and related functionality.
"""

import pytest
from app.core.prosody.tafila import (
    Tafila,
    TafilaStructure,
    TAFAIL_BASE,
    get_tafila,
    get_tafila_by_pattern,
    list_all_tafail
)


class TestTafila:
    """Test Tafila class."""

    def test_create_tafila(self):
        """Test creating a basic taf'ila."""
        tafila = Tafila(
            name="فعولن",
            phonetic="/o//o",
            structure="sabab+watad",
            syllable_count=3
        )

        assert tafila.name == "فعولن"
        assert tafila.phonetic == "/o//o"
        assert tafila.pattern_length == 5
        assert tafila.syllable_count == 3

    def test_tafila_string_representation(self):
        """Test string representations."""
        tafila = TAFAIL_BASE["فعولن"]

        assert str(tafila) == "فعولن"
        assert "Tafila" in repr(tafila)
        assert "/o//o" in repr(tafila)

    def test_tafila_equality(self):
        """Test taf'ila equality based on phonetic pattern."""
        tafila1 = Tafila("فعولن", "/o//o", "test", 3)
        tafila2 = Tafila("فعولن_2", "/o//o", "test", 3)
        tafila3 = Tafila("مفاعيلن", "//o/o/o", "test", 4)

        assert tafila1 == tafila2  # Same phonetic
        assert tafila1 != tafila3  # Different phonetic

    def test_tafila_harakat_count(self):
        """Test counting harakat."""
        tafila = TAFAIL_BASE["متفاعلن"]  # ///o//o
        assert tafila.harakat_count == 5  # 5 slashes

    def test_tafila_sukunat_count(self):
        """Test counting sukunat."""
        tafila = TAFAIL_BASE["متفاعلن"]  # ///o//o
        assert tafila.sukunat_count == 2  # 2 'o's

    def test_tafila_matches_pattern(self):
        """Test exact pattern matching."""
        tafila = TAFAIL_BASE["فعولن"]

        assert tafila.matches_pattern("/o//o")
        assert not tafila.matches_pattern("/o//")
        assert not tafila.matches_pattern("//o/o")

    def test_tafila_similarity(self):
        """Test pattern similarity calculation."""
        tafila = TAFAIL_BASE["فعولن"]  # /o//o

        assert tafila.similarity("/o//o") == 1.0  # Exact match
        assert tafila.similarity("/o//") > 0.5    # Close match
        assert tafila.similarity("ooooo") < 0.5   # Poor match
        assert tafila.similarity("") == 0.0       # Empty

    def test_tafila_to_dict(self):
        """Test conversion to dictionary."""
        tafila = TAFAIL_BASE["فعولن"]
        data = tafila.to_dict()

        assert data["name"] == "فعولن"
        assert data["phonetic"] == "/o//o"
        assert data["pattern_length"] == 5
        assert "harakat_count" in data
        assert "sukunat_count" in data

    def test_invalid_tafila_empty_name(self):
        """Test validation: empty name."""
        with pytest.raises(ValueError, match="name cannot be empty"):
            Tafila("", "/o//o", "test", 3)

    def test_invalid_tafila_empty_phonetic(self):
        """Test validation: empty phonetic."""
        with pytest.raises(ValueError, match="phonetic pattern cannot be empty"):
            Tafila("test", "", "test", 3)

    def test_invalid_tafila_zero_syllables(self):
        """Test validation: zero syllables."""
        with pytest.raises(ValueError, match="must have at least 1 syllable"):
            Tafila("test", "/o//o", "test", 0)

    def test_invalid_tafila_bad_phonetic(self):
        """Test validation: invalid phonetic characters."""
        with pytest.raises(ValueError, match="Invalid phonetic pattern"):
            Tafila("test", "/o#/o", "test", 3)


class TestTafailRegistry:
    """Test tafa'il registry functions."""

    def test_get_tafila(self):
        """Test getting taf'ila by name."""
        tafila = get_tafila("فعولن")
        assert tafila is not None
        assert tafila.name == "فعولن"
        assert tafila.phonetic == "/o//o"

    def test_get_tafila_not_found(self):
        """Test getting non-existent taf'ila."""
        tafila = get_tafila("غير موجود")
        assert tafila is None

    def test_get_tafila_by_pattern(self):
        """Test getting taf'ila by phonetic pattern."""
        tafila = get_tafila_by_pattern("/o//o")
        assert tafila is not None
        assert tafila.name in ["فعولن", "فاعلن"]  # Both have this pattern

    def test_get_tafila_by_pattern_not_found(self):
        """Test getting taf'ila by non-existent pattern."""
        tafila = get_tafila_by_pattern("xyz")
        assert tafila is None

    def test_list_all_tafail(self):
        """Test listing all base tafa'il."""
        all_tafail = list_all_tafail()

        assert len(all_tafail) == 9  # 9 base tafa'il defined
        assert all(isinstance(t, Tafila) for t in all_tafail)

    def test_tafail_base_registry(self):
        """Test TAFAIL_BASE registry."""
        assert "فعولن" in TAFAIL_BASE
        assert "مفاعيلن" in TAFAIL_BASE
        assert "متفاعلن" in TAFAIL_BASE
        assert "مستفعلن" in TAFAIL_BASE
        assert "فاعلاتن" in TAFAIL_BASE
        assert "مفاعلتن" in TAFAIL_BASE

        # Verify all have proper structure
        for name, tafila in TAFAIL_BASE.items():
            assert tafila.name == name
            assert len(tafila.phonetic) > 0
            assert tafila.syllable_count > 0
