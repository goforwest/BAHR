"""
Schema validation tests for Golden Set.

Tests that all verses comply with the JSON Schema specification.
"""

import pytest
from jsonschema import validate, ValidationError, Draft7Validator


# ============================================================================
# Test Schema Structure
# ============================================================================

@pytest.mark.schema
class TestSchemaStructure:
    """Test the JSON schema itself."""
    
    def test_schema_is_valid_json(self, golden_set_schema):
        """Test that schema is valid JSON."""
        assert golden_set_schema is not None
        assert isinstance(golden_set_schema, dict)
    
    def test_schema_has_required_properties(self, golden_set_schema):
        """Test that schema defines required properties."""
        assert '$schema' in golden_set_schema
        assert 'type' in golden_set_schema
        assert 'properties' in golden_set_schema
        assert 'required' in golden_set_schema
    
    def test_schema_defines_all_fields(self, golden_set_schema):
        """Test that schema defines all 17 fields."""
        properties = golden_set_schema['properties']
        expected_fields = [
            'verse_id', 'text', 'normalized_text', 'meter', 'poet', 'source',
            'era', 'confidence', 'notes', 'taqti3', 'expected_tafail',
            'syllable_pattern', 'syllable_count', 'edge_case_type',
            'difficulty_level', 'validation', 'metadata'
        ]
        
        for field in expected_fields:
            assert field in properties, f"Schema missing property: {field}"
    
    def test_schema_required_fields(self, golden_set_schema):
        """Test that schema specifies required fields correctly."""
        required = golden_set_schema['required']
        
        # These fields should be required
        mandatory_fields = [
            'verse_id', 'text', 'normalized_text', 'meter',
            'era', 'confidence', 'notes', 'taqti3', 'expected_tafail',
            'syllable_pattern', 'syllable_count', 'edge_case_type',
            'difficulty_level', 'validation', 'metadata'
        ]
        
        for field in mandatory_fields:
            assert field in required, f"Field '{field}' should be required"


# ============================================================================
# Test Individual Verse Validation
# ============================================================================

@pytest.mark.schema
class TestVerseValidation:
    """Test that all verses validate against schema."""
    
    def test_all_verses_validate(self, golden_set_verses, golden_set_schema):
        """Test that all 20 verses pass schema validation."""
        validator = Draft7Validator(golden_set_schema)
        
        for verse in golden_set_verses:
            errors = list(validator.iter_errors(verse))
            assert len(errors) == 0, \
                f"Validation errors in {verse['verse_id']}: {errors}"
    
    def test_sample_verse_validates(self, sample_verse, golden_set_schema):
        """Test that sample verse validates."""
        validate(instance=sample_verse, schema=golden_set_schema)
        # No exception means validation passed
    
    def test_verse_with_missing_required_field_fails(self, sample_verse, golden_set_schema):
        """Test that verse missing required field fails validation."""
        invalid_verse = sample_verse.copy()
        del invalid_verse['verse_id']
        
        with pytest.raises(ValidationError):
            validate(instance=invalid_verse, schema=golden_set_schema)
    
    def test_verse_with_invalid_confidence_fails(self, sample_verse, golden_set_schema):
        """Test that verse with out-of-range confidence fails."""
        invalid_verse = sample_verse.copy()
        invalid_verse['confidence'] = 1.5  # Invalid (>1.0)
        
        with pytest.raises(ValidationError):
            validate(instance=invalid_verse, schema=golden_set_schema)
    
    def test_verse_with_invalid_meter_fails(self, sample_verse, golden_set_schema):
        """Test that verse with invalid meter name fails."""
        invalid_verse = sample_verse.copy()
        invalid_verse['meter'] = "بحر غير موجود"  # Not in enum
        
        with pytest.raises(ValidationError):
            validate(instance=invalid_verse, schema=golden_set_schema)
    
    def test_verse_with_invalid_difficulty_fails(self, sample_verse, golden_set_schema):
        """Test that verse with invalid difficulty fails."""
        invalid_verse = sample_verse.copy()
        invalid_verse['difficulty_level'] = "super_hard"  # Not in enum
        
        with pytest.raises(ValidationError):
            validate(instance=invalid_verse, schema=golden_set_schema)


# ============================================================================
# Test Field Type Validation
# ============================================================================

@pytest.mark.schema
class TestFieldTypes:
    """Test that field types match schema."""
    
    def test_verse_id_is_string(self, golden_set_verses):
        """Test that verse_id is always a string."""
        for verse in golden_set_verses:
            assert isinstance(verse['verse_id'], str)
    
    def test_text_is_string(self, golden_set_verses):
        """Test that text is always a string."""
        for verse in golden_set_verses:
            assert isinstance(verse['text'], str)
            assert len(verse['text']) >= 10
    
    def test_confidence_is_float(self, golden_set_verses):
        """Test that confidence is a number."""
        for verse in golden_set_verses:
            assert isinstance(verse['confidence'], (int, float))
            assert 0.0 <= verse['confidence'] <= 1.0
    
    def test_expected_tafail_is_array(self, golden_set_verses):
        """Test that expected_tafail is an array."""
        for verse in golden_set_verses:
            assert isinstance(verse['expected_tafail'], list)
            assert len(verse['expected_tafail']) >= 2
            assert all(isinstance(t, str) for t in verse['expected_tafail'])
    
    def test_syllable_count_is_integer(self, golden_set_verses):
        """Test that syllable_count is an integer."""
        for verse in golden_set_verses:
            assert isinstance(verse['syllable_count'], int)
            assert 6 <= verse['syllable_count'] <= 32
    
    def test_validation_is_object(self, golden_set_verses):
        """Test that validation is an object."""
        for verse in golden_set_verses:
            assert isinstance(verse['validation'], dict)
            assert 'verified_by' in verse['validation']
            assert 'verified_date' in verse['validation']
            assert 'reference_sources' in verse['validation']
    
    def test_metadata_is_object(self, golden_set_verses):
        """Test that metadata is an object."""
        for verse in golden_set_verses:
            assert isinstance(verse['metadata'], dict)
            assert 'created_at' in verse['metadata']
            assert 'updated_at' in verse['metadata']
            assert 'version' in verse['metadata']


# ============================================================================
# Test Pattern Validation
# ============================================================================

@pytest.mark.schema
class TestPatternValidation:
    """Test regex pattern validation."""
    
    def test_verse_id_pattern(self, golden_set_verses):
        """Test that verse_id matches pattern."""
        import re
        pattern = r'^(golden|train|test|dev)_\d{3,}$'
        
        for verse in golden_set_verses:
            assert re.match(pattern, verse['verse_id']), \
                f"Invalid verse_id format: {verse['verse_id']}"
    
    def test_syllable_pattern_format(self, golden_set_verses):
        """Test that syllable_pattern uses valid characters."""
        import re
        pattern = r'^[\-u \|]+$'
        
        for verse in golden_set_verses:
            assert re.match(pattern, verse['syllable_pattern']), \
                f"Invalid syllable_pattern in {verse['verse_id']}: {verse['syllable_pattern']}"
    
    def test_metadata_version_pattern(self, golden_set_verses):
        """Test that version follows X.Y pattern."""
        import re
        pattern = r'^\d+\.\d+$'
        
        for verse in golden_set_verses:
            version = verse['metadata']['version']
            assert re.match(pattern, version), \
                f"Invalid version format in {verse['verse_id']}: {version}"


# ============================================================================
# Test Enum Validation
# ============================================================================

@pytest.mark.schema
class TestEnumValidation:
    """Test enum field validation."""
    
    def test_era_is_valid(self, golden_set_verses):
        """Test that era is from valid enum."""
        valid_eras = ['classical', 'modern', 'contemporary', 'unknown']
        
        for verse in golden_set_verses:
            assert verse['era'] in valid_eras, \
                f"Invalid era in {verse['verse_id']}: {verse['era']}"
    
    def test_difficulty_level_is_valid(self, golden_set_verses):
        """Test that difficulty_level is from valid enum."""
        valid_levels = ['easy', 'medium', 'hard']
        
        for verse in golden_set_verses:
            assert verse['difficulty_level'] in valid_levels, \
                f"Invalid difficulty in {verse['verse_id']}: {verse['difficulty_level']}"
    
    def test_edge_case_type_is_valid(self, golden_set_verses):
        """Test that edge_case_type is from valid enum."""
        valid_types = ['perfect_match', 'common_variations', 'rare_variations',
                       'diacritics_test', 'ambiguous']
        
        for verse in golden_set_verses:
            assert verse['edge_case_type'] in valid_types, \
                f"Invalid edge_case_type in {verse['verse_id']}: {verse['edge_case_type']}"
    
    def test_meter_is_valid(self, golden_set_verses, meter_names):
        """Test that meter is from valid list of 16 classical meters."""
        for verse in golden_set_verses:
            assert verse['meter'] in meter_names, \
                f"Invalid meter in {verse['verse_id']}: {verse['meter']}"


# ============================================================================
# Test Nested Object Validation
# ============================================================================

@pytest.mark.schema
class TestNestedObjects:
    """Test validation of nested objects."""
    
    def test_validation_object_structure(self, golden_set_verses):
        """Test validation object has required structure."""
        for verse in golden_set_verses:
            val = verse['validation']
            
            assert 'verified_by' in val
            assert 'verified_date' in val
            assert 'reference_sources' in val
            
            assert isinstance(val['verified_by'], str)
            assert isinstance(val['verified_date'], str)
            assert isinstance(val['reference_sources'], list)
            assert len(val['reference_sources']) >= 1
    
    def test_metadata_object_structure(self, golden_set_verses):
        """Test metadata object has required structure."""
        for verse in golden_set_verses:
            meta = verse['metadata']
            
            assert 'created_at' in meta
            assert 'updated_at' in meta
            assert 'version' in meta
            
            assert isinstance(meta['created_at'], str)
            assert isinstance(meta['updated_at'], str)
            assert isinstance(meta['version'], str)
    
    def test_reference_sources_are_strings(self, golden_set_verses):
        """Test that reference sources are all strings."""
        for verse in golden_set_verses:
            sources = verse['validation']['reference_sources']
            for source in sources:
                assert isinstance(source, str)
                assert len(source) > 0


# ============================================================================
# Test Constraint Validation
# ============================================================================

@pytest.mark.schema
class TestConstraints:
    """Test min/max constraints."""
    
    def test_text_min_length(self, golden_set_verses):
        """Test that text meets minimum length."""
        for verse in golden_set_verses:
            assert len(verse['text']) >= 10, \
                f"Text too short in {verse['verse_id']}"
    
    def test_syllable_count_in_range(self, golden_set_verses):
        """Test that syllable count is in valid range."""
        for verse in golden_set_verses:
            count = verse['syllable_count']
            assert 6 <= count <= 32, \
                f"Syllable count out of range in {verse['verse_id']}: {count}"
    
    def test_tafail_count_in_range(self, golden_set_verses):
        """Test that taf'ilah count is in valid range."""
        for verse in golden_set_verses:
            count = len(verse['expected_tafail'])
            assert 2 <= count <= 8, \
                f"Taf'ilah count out of range in {verse['verse_id']}: {count}"
    
    def test_confidence_in_range(self, golden_set_verses):
        """Test that confidence is 0.0-1.0."""
        for verse in golden_set_verses:
            conf = verse['confidence']
            assert 0.0 <= conf <= 1.0, \
                f"Confidence out of range in {verse['verse_id']}: {conf}"
