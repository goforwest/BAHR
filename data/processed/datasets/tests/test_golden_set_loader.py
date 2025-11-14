"""
Unit tests for Golden Set data loading and filtering.

Tests the GoldenSetLoader class and related functionality.
"""

import pytest
import json
from pathlib import Path
import sys

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from golden_set_usage_examples import GoldenSetLoader


# ============================================================================
# Test Data Loading
# ============================================================================

@pytest.mark.unit
class TestGoldenSetLoader:
    """Test GoldenSetLoader class."""
    
    def test_loader_initialization(self, golden_set_path):
        """Test that loader initializes correctly."""
        loader = GoldenSetLoader(str(golden_set_path))
        assert loader is not None
        assert loader.verses is not None
        assert len(loader.verses) > 0
    
    def test_loads_correct_number_of_verses(self, golden_set_path):
        """Test that all 20 verses are loaded."""
        loader = GoldenSetLoader(str(golden_set_path))
        assert len(loader.verses) == 20
    
    def test_all_verses_have_required_fields(self, golden_set_path):
        """Test that all verses have required fields."""
        loader = GoldenSetLoader(str(golden_set_path))
        required_fields = [
            'verse_id', 'text', 'normalized_text', 'meter',
            'era', 'confidence', 'notes', 'taqti3',
            'expected_tafail', 'syllable_pattern', 'syllable_count',
            'edge_case_type', 'difficulty_level', 'validation', 'metadata'
        ]
        
        for verse in loader.verses:
            for field in required_fields:
                assert field in verse, f"Missing field '{field}' in {verse['verse_id']}"


# ============================================================================
# Test Query Methods
# ============================================================================

@pytest.mark.unit
class TestQueryMethods:
    """Test GoldenSetLoader query methods."""
    
    def test_get_by_id_success(self, golden_set_path):
        """Test retrieving verse by ID."""
        loader = GoldenSetLoader(str(golden_set_path))
        verse = loader.get_by_id('golden_001')
        assert verse is not None
        assert verse['verse_id'] == 'golden_001'
    
    def test_get_by_id_not_found(self, golden_set_path):
        """Test that missing ID raises KeyError."""
        loader = GoldenSetLoader(str(golden_set_path))
        with pytest.raises(KeyError):
            loader.get_by_id('golden_999')
    
    def test_get_by_meter(self, golden_set_path):
        """Test filtering by meter."""
        loader = GoldenSetLoader(str(golden_set_path))
        tawil = loader.get_by_meter('الطويل')
        assert len(tawil) == 4
        assert all(v['meter'] == 'الطويل' for v in tawil)
    
    def test_get_by_difficulty(self, golden_set_path):
        """Test filtering by difficulty level."""
        loader = GoldenSetLoader(str(golden_set_path))
        easy = loader.get_by_difficulty('easy')
        assert len(easy) == 8
        assert all(v['difficulty_level'] == 'easy' for v in easy)
    
    def test_get_by_edge_case(self, golden_set_path):
        """Test filtering by edge case type."""
        loader = GoldenSetLoader(str(golden_set_path))
        perfect = loader.get_by_edge_case('perfect_match')
        assert len(perfect) == 13
        assert all(v['edge_case_type'] == 'perfect_match' for v in perfect)
    
    def test_get_high_confidence_default(self, golden_set_path):
        """Test high confidence filter with default threshold."""
        loader = GoldenSetLoader(str(golden_set_path))
        high_conf = loader.get_high_confidence()
        assert all(v['confidence'] >= 0.95 for v in high_conf)
    
    def test_get_high_confidence_custom_threshold(self, golden_set_path):
        """Test high confidence filter with custom threshold."""
        loader = GoldenSetLoader(str(golden_set_path))
        high_conf = loader.get_high_confidence(threshold=0.90)
        assert all(v['confidence'] >= 0.90 for v in high_conf)
        assert len(high_conf) >= len(loader.get_high_confidence(threshold=0.95))


# ============================================================================
# Test Statistics
# ============================================================================

@pytest.mark.unit
class TestStatistics:
    """Test statistics generation."""
    
    def test_get_statistics_structure(self, golden_set_path):
        """Test that statistics have correct structure."""
        loader = GoldenSetLoader(str(golden_set_path))
        stats = loader.get_statistics()
        
        assert 'total_verses' in stats
        assert 'meter_distribution' in stats
        assert 'difficulty_distribution' in stats
        assert 'edge_case_distribution' in stats
        assert 'average_confidence' in stats
        assert 'average_syllable_count' in stats
        assert 'unique_poets' in stats
    
    def test_total_verses_count(self, golden_set_path):
        """Test total verses count."""
        loader = GoldenSetLoader(str(golden_set_path))
        stats = loader.get_statistics()
        assert stats['total_verses'] == 20
    
    def test_meter_distribution(self, golden_set_path, covered_meters):
        """Test meter distribution."""
        loader = GoldenSetLoader(str(golden_set_path))
        stats = loader.get_statistics()
        
        # All meters should be from covered list
        for meter in stats['meter_distribution'].keys():
            assert meter in covered_meters
        
        # Total count should equal total verses
        total_count = sum(stats['meter_distribution'].values())
        assert total_count == 20
    
    def test_difficulty_distribution(self, golden_set_path):
        """Test difficulty distribution."""
        loader = GoldenSetLoader(str(golden_set_path))
        stats = loader.get_statistics()
        
        assert 'easy' in stats['difficulty_distribution']
        assert 'medium' in stats['difficulty_distribution']
        assert stats['difficulty_distribution']['easy'] == 8
        assert stats['difficulty_distribution']['medium'] == 12
    
    def test_average_confidence(self, golden_set_path):
        """Test average confidence calculation."""
        loader = GoldenSetLoader(str(golden_set_path))
        stats = loader.get_statistics()
        
        assert 0.0 <= stats['average_confidence'] <= 1.0
        assert abs(stats['average_confidence'] - 0.924) < 0.01  # Should be ~0.924
    
    def test_average_syllable_count(self, golden_set_path):
        """Test average syllable count."""
        loader = GoldenSetLoader(str(golden_set_path))
        stats = loader.get_statistics()
        
        assert stats['average_syllable_count'] > 0
        assert abs(stats['average_syllable_count'] - 15.2) < 0.5  # Should be ~15.2


# ============================================================================
# Test Data Integrity
# ============================================================================

@pytest.mark.unit
class TestDataIntegrity:
    """Test data integrity and consistency."""
    
    def test_all_verse_ids_unique(self, golden_set_verses):
        """Test that all verse IDs are unique."""
        verse_ids = [v['verse_id'] for v in golden_set_verses]
        assert len(verse_ids) == len(set(verse_ids))
    
    def test_verse_ids_follow_pattern(self, golden_set_verses, assert_valid_verse_id):
        """Test that verse IDs follow golden_NNN pattern."""
        for verse in golden_set_verses:
            assert_valid_verse_id(verse['verse_id'])
    
    def test_confidence_in_valid_range(self, golden_set_verses):
        """Test that all confidence values are between 0 and 1."""
        for verse in golden_set_verses:
            assert 0.0 <= verse['confidence'] <= 1.0
    
    def test_syllable_count_matches_pattern(self, golden_set_verses):
        """Test that syllable count matches syllable pattern."""
        for verse in golden_set_verses:
            pattern = verse['syllable_pattern']
            # Count - and u in pattern
            syllables = pattern.count('-') + pattern.count('u')
            assert syllables == verse['syllable_count'], \
                f"Mismatch in {verse['verse_id']}: count={verse['syllable_count']}, pattern has {syllables}"
    
    def test_tafail_count_reasonable(self, golden_set_verses):
        """Test that taf'ilah count is reasonable (2-8)."""
        for verse in golden_set_verses:
            tafail_count = len(verse['expected_tafail'])
            assert 2 <= tafail_count <= 8, \
                f"{verse['verse_id']} has {tafail_count} taf'ilah (expected 2-8)"
    
    def test_syllable_pattern_format(self, golden_set_verses, assert_valid_syllable_pattern):
        """Test that syllable patterns use correct symbols."""
        for verse in golden_set_verses:
            assert_valid_syllable_pattern(verse['syllable_pattern'])
    
    def test_meters_are_valid(self, golden_set_verses, covered_meters):
        """Test that all meters are from covered list."""
        for verse in golden_set_verses:
            assert verse['meter'] in covered_meters, \
                f"Unexpected meter: {verse['meter']}"
    
    def test_difficulty_levels_are_valid(self, golden_set_verses):
        """Test that difficulty levels are valid."""
        valid_levels = ['easy', 'medium', 'hard']
        for verse in golden_set_verses:
            assert verse['difficulty_level'] in valid_levels
    
    def test_edge_case_types_are_valid(self, golden_set_verses):
        """Test that edge case types are valid."""
        valid_types = ['perfect_match', 'common_variations', 'rare_variations', 
                       'diacritics_test', 'ambiguous']
        for verse in golden_set_verses:
            assert verse['edge_case_type'] in valid_types
    
    def test_validation_has_required_fields(self, golden_set_verses):
        """Test that validation object has required fields."""
        required_fields = ['verified_by', 'verified_date', 'reference_sources']
        for verse in golden_set_verses:
            for field in required_fields:
                assert field in verse['validation'], \
                    f"Missing validation.{field} in {verse['verse_id']}"
    
    def test_metadata_has_required_fields(self, golden_set_verses):
        """Test that metadata object has required fields."""
        required_fields = ['created_at', 'updated_at', 'version']
        for verse in golden_set_verses:
            for field in required_fields:
                assert field in verse['metadata'], \
                    f"Missing metadata.{field} in {verse['verse_id']}"


# ============================================================================
# Test Specific Verses
# ============================================================================

@pytest.mark.unit
class TestSpecificVerses:
    """Test specific known verses."""
    
    def test_golden_001_imru_alqais(self, golden_set_path):
        """Test the famous first verse of Imru' al-Qais."""
        loader = GoldenSetLoader(str(golden_set_path))
        verse = loader.get_by_id('golden_001')
        
        assert verse['poet'] == 'امرؤ القيس'
        assert verse['meter'] == 'الطويل'
        assert verse['source'] == 'المعلقة'
        assert verse['confidence'] >= 0.95
        assert verse['difficulty_level'] == 'easy'
        assert verse['edge_case_type'] == 'perfect_match'
    
    def test_all_tawil_verses_have_correct_meter(self, tawil_verses):
        """Test that all الطويل verses are correctly labeled."""
        assert len(tawil_verses) == 4
        for verse in tawil_verses:
            assert verse['meter'] == 'الطويل'
            # الطويل typically has 16 syllables
            assert 14 <= verse['syllable_count'] <= 18
