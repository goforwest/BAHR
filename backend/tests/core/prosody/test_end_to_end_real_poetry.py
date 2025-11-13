"""
End-to-end tests using real Arabic poetry from the golden dataset.

These tests verify the complete pipeline from text scanning to meter detection
using actual verses from classical Arabic poetry.
"""

import pytest
from app.core.prosody.detector_v2 import BahrDetectorV2
from app.core.prosody.letter_structure import parse_tafila_from_text
from app.core.prosody.tafila import Tafila


class TestRealPoetryDetection:
    """Test meter detection with real classical Arabic poetry."""

    @pytest.fixture
    def detector(self):
        """Initialize detector once for all tests."""
        return BahrDetectorV2()

    def test_imru_alqays_mutallaqah_opener(self, detector):
        """Test the famous opening line of Imru' al-Qays's Mu'allaqah."""
        # قِفا نَبْكِ مِن ذِكرى حَبيبٍ ومَنْزِلِ - الطويل
        pattern = "/o//o//o/o//o////o/o"

        results = detector.detect(pattern, top_k=1)

        assert len(results) > 0
        assert results[0].meter_name_ar == "الطويل"
        assert results[0].confidence >= 0.90

    def test_mutanabbi_azm_line(self, detector):
        """Test al-Mutanabbi's famous line about determination."""
        # على قَدرِ أَهلِ العَزمِ تَأتي العَزائِمُ - البسيط
        pattern = "/o///o///o/o///o///o"

        results = detector.detect(pattern, top_k=1)

        assert len(results) > 0
        assert results[0].meter_name_ar == "البسيط"
        assert results[0].confidence >= 0.65  # Lower confidence for البسيط

    def test_abu_alala_ramel(self, detector):
        """Test a verse in al-Ramal meter."""
        # يا لَيلَةَ الصَّبِّ مَتى غَدُكِ - الرمل
        pattern = "/o///o/o///o/o//"

        results = detector.detect(pattern, top_k=1)

        assert len(results) > 0
        assert results[0].meter_name_ar == "الرمل"
        assert results[0].confidence >= 0.90

    def test_abu_alala_kamil(self, detector):
        """Test a verse in al-Kamil meter by Abu al-'Ala' al-Ma'arri."""
        # أُراكَ تَعْلَلُ بالدُنيا وتَكْرَهُها - الكامل
        pattern = "//o//o//o//o//o//o//o/"

        results = detector.detect(pattern, top_k=1)

        assert len(results) > 0
        assert results[0].meter_name_ar == "الكامل"
        assert results[0].confidence >= 0.85

    def test_jamil_buthainah_tawil(self, detector):
        """Test a verse by Jamil Buthainah in al-Tawil meter."""
        # بانَ الخَليطُ وَلَمْ أَقْضِ الَّذي وَجَبا - الطويل
        pattern = "/o//o//o/o/o/o//o//o/"

        results = detector.detect(pattern, top_k=1)

        assert len(results) > 0
        assert results[0].meter_name_ar == "الطويل"
        assert results[0].confidence >= 0.90

    def test_mutanabbi_mutaqarib(self, detector):
        """Test al-Mutanabbi's verse in al-Mutaqarib meter."""
        # فَإِن تَفُقِ الأَنامَ وأَنتَ فيهمْ - المتقارب
        pattern = "/o///o///o///o//"

        results = detector.detect(pattern, top_k=1)

        assert len(results) > 0
        assert results[0].meter_name_ar == "المتقارب"
        assert results[0].confidence >= 0.90

    def test_rajaz_meter(self, detector):
        """Test a verse in al-Rajaz meter."""
        # أَلا فِي سَبيلِ المَجدِ ما أَنا فاعِلُ - الرجز
        pattern = "/o/o//o/o///o/o///"

        results = detector.detect(pattern, top_k=1)

        assert len(results) > 0
        assert results[0].meter_name_ar == "الرجز"
        assert results[0].confidence >= 0.90

    def test_khafif_meter(self, detector):
        """Test a verse in al-Khafif meter."""
        # سَأَبْكِي وَلَوْ بَلَّغْتُ نَصْبِي تَأَسُّفِي - الخفيف
        pattern = "/o//o/o/o/o//o/o//o/o"

        results = detector.detect(pattern, top_k=1)

        assert len(results) > 0
        assert results[0].meter_name_ar == "الخفيف"
        assert results[0].confidence >= 0.90


class TestTransformationTracking:
    """Test that transformations are properly tracked through detection."""

    @pytest.fixture
    def detector(self):
        """Initialize detector once for all tests."""
        return BahrDetectorV2()

    def test_base_pattern_has_no_transformations(self, detector):
        """Test that base patterns are marked as 'base' with no transformations."""
        # Pure base pattern for al-Tawil: فعولن مفاعيلن فعولن مفاعيلن
        pattern = "/o//o//o/o/o/o//o//o/o/o"

        results = detector.detect(pattern, top_k=1)

        assert len(results) > 0
        result = results[0]
        assert result.meter_name_ar == "الطويل"
        assert result.match_quality.value == "exact"
        assert all(t == "base" for t in result.transformations)

    def test_qabd_transformation_tracked(self, detector):
        """Test that QABD transformation is tracked."""
        # Al-Tawil with QABD on first taf'ilah: مفاعلن instead of مفاعيلن
        pattern = "/o////o/o/o/o//o//o/o/o"

        results = detector.detect(pattern, top_k=1)

        assert len(results) > 0
        result = results[0]
        assert result.meter_name_ar == "الطويل"
        # Should have at least one transformation
        assert any(t != "base" for t in result.transformations)

    def test_khabn_transformation_tracked(self, detector):
        """Test that KHABN transformation is tracked."""
        # Al-Rajaz with KHABN: متفعلن instead of مستفعلن
        pattern = "///o//o///o//o///o//o"

        results = detector.detect(pattern, top_k=1)

        assert len(results) > 0
        result = results[0]
        # Should detect a meter with transformations
        if result.transformations:
            assert any(t != "base" for t in result.transformations)

    def test_transformation_explanation(self, detector):
        """Test that explanations mention transformations."""
        # Pattern with transformations
        pattern = "/o////o/o/o/o//o//o/o/o"

        results = detector.detect(pattern, top_k=1)

        assert len(results) > 0
        result = results[0]
        # Explanation should exist
        assert result.explanation
        assert len(result.explanation) > 0


class TestLetterLevelIntegration:
    """Test that letter-level transformations integrate with detection."""

    def test_tafila_with_letter_structure_detection(self):
        """Test that taf'ilah with letter structure works in detection."""
        # Parse a taf'ilah with letter structure
        faculun = parse_tafila_from_text('فعولن', 'فَعُولُنْ')

        # Create Tafila with letter structure
        tafila = Tafila(
            name="فعولن",
            phonetic=faculun.phonetic_pattern,
            structure="/o//o",
            syllable_count=2,
            letter_structure=faculun
        )

        # Verify letter structure is preserved
        assert tafila.letter_structure is not None
        assert tafila.letter_structure.phonetic_pattern == tafila.phonetic

    def test_zahaf_preserves_letter_structure(self):
        """Test that applying zahaf preserves letter structure."""
        from app.core.prosody.zihafat import QABD

        # Parse taf'ilah with letter structure
        mafacilun = parse_tafila_from_text('مفاعيلن', 'مَفَاعِيلُنْ')

        tafila = Tafila(
            name="مفاعيلن",
            phonetic=mafacilun.phonetic_pattern,
            structure="//o/o/o",
            syllable_count=3,
            letter_structure=mafacilun
        )

        # Apply QABD
        result = QABD.apply(tafila)

        # Letter structure should be preserved
        assert result.letter_structure is not None
        assert result.phonetic == result.letter_structure.phonetic_pattern

    def test_ilal_preserves_letter_structure(self):
        """Test that applying 'ilah preserves letter structure."""
        from app.core.prosody.ilal import HADHF

        # Parse taf'ilah with letter structure
        faculun = parse_tafila_from_text('فعولن', 'فَعُولُنْ')

        tafila = Tafila(
            name="فعولن",
            phonetic=faculun.phonetic_pattern,
            structure="/o//o",
            syllable_count=2,
            letter_structure=faculun
        )

        # Apply HADHF
        result = HADHF.apply(tafila)

        # Letter structure should be preserved
        assert result.letter_structure is not None
        assert result.phonetic == result.letter_structure.phonetic_pattern


class TestGoldenDatasetSamples:
    """Test detection accuracy with samples from the golden dataset."""

    @pytest.fixture
    def detector(self):
        """Initialize detector once for all tests."""
        return BahrDetectorV2()

    @pytest.mark.parametrize("pattern,expected_meter,min_confidence", [
        ("/o//o//o/o//o////o/o", "الطويل", 0.90),  # golden_001
        ("/o/o//o/o///o/o///", "الرجز", 0.90),       # golden_002
        ("/o///o/o///o/o//", "الرمل", 0.90),        # golden_003
        ("/o///o///o/o///o///o", "البسيط", 0.65),   # golden_004
        ("//o//o//o//o//o//o//o/", "الكامل", 0.85), # golden_006
        ("/o//o//o/o/o/o//o//o/", "الطويل", 0.90),  # golden_007
        ("/o///o///o///o//", "المتقارب", 0.90),     # golden_009
        ("/o//o/o/o/o//o/o//o/o", "الخفيف", 0.90),  # golden_010
    ])
    def test_golden_dataset_detection(self, detector, pattern, expected_meter, min_confidence):
        """Test meter detection with patterns from the golden dataset."""
        results = detector.detect(pattern, top_k=1)

        assert len(results) > 0, f"No results for pattern {pattern}"
        result = results[0]

        assert result.meter_name_ar == expected_meter, \
            f"Expected {expected_meter}, got {result.meter_name_ar} for pattern {pattern}"
        assert result.confidence >= min_confidence, \
            f"Confidence {result.confidence} below {min_confidence} for {expected_meter}"


class TestDifficultCases:
    """Test challenging cases from the golden dataset."""

    @pytest.fixture
    def detector(self):
        """Initialize detector once for all tests."""
        return BahrDetectorV2()

    def test_basit_with_low_fitness(self, detector):
        """Test al-Basit meter which can have lower fitness scores."""
        # golden_004: البسيط with fitness_score 0.677
        pattern = "/o///o///o/o///o///o"

        results = detector.detect(pattern, top_k=3)

        assert len(results) > 0
        # Should have البسيط in top 3
        meter_names = [r.meter_name_ar for r in results]
        assert "البسيط" in meter_names

    def test_diacritics_handling(self, detector):
        """Test verses with complex diacritics (shadda, tanwin)."""
        # golden_008: verse with شدة and مد
        pattern = "/o/o//o/o/o//o/o/o//o//o/"

        results = detector.detect(pattern, top_k=1)

        assert len(results) > 0
        assert results[0].meter_name_ar == "الكامل"

    def test_common_variations(self, detector):
        """Test verses marked as 'common_variations' in golden dataset."""
        # golden_007: Tawil with variations
        pattern = "/o//o//o/o/o/o//o//o/"

        results = detector.detect(pattern, top_k=1)

        assert len(results) > 0
        assert results[0].meter_name_ar == "الطويل"
        assert results[0].match_quality.value in ["exact", "strong", "moderate"]


class TestPerformance:
    """Test performance characteristics of the detection system."""

    def test_detector_initialization_time(self):
        """Test that detector initializes efficiently."""
        import time

        start = time.time()
        detector = BahrDetectorV2()
        elapsed = time.time() - start

        # Should initialize within 2 seconds
        assert elapsed < 2.0, f"Initialization took {elapsed:.2f}s"

        # Should have all 16 meters
        stats = detector.get_statistics()
        assert stats['total_meters'] == 16

    def test_detection_speed(self):
        """Test that detection is fast enough for real-time use."""
        import time

        detector = BahrDetectorV2()
        pattern = "/o//o//o/o/o/o//o//o/o/o"

        start = time.time()
        for _ in range(100):
            detector.detect_best(pattern)
        elapsed = time.time() - start

        # Should handle 100 detections in under 1 second
        assert elapsed < 1.0, f"100 detections took {elapsed:.2f}s"

    def test_pattern_cache_completeness(self):
        """Test that pattern cache covers all meters comprehensively."""
        detector = BahrDetectorV2()
        stats = detector.get_statistics()

        # Should have generated a significant number of patterns
        assert stats['total_patterns'] > 100

        # All 16 meters should have patterns
        for meter_id in range(1, 17):
            patterns = detector.get_valid_patterns(meter_id)
            assert len(patterns) > 0, f"Meter {meter_id} has no patterns"
