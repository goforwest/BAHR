"""
Rhyme analysis (قافية - Qafiyah) for Arabic poetry.

This module provides functionality to:
1. Extract rhyme patterns from verses
2. Identify the rhyme letter (حرف الروي - harf al-rawi)
3. Classify rhyme types (مطلقة، مقيدة، etc.)
4. Validate rhyme consistency across multiple verses
5. Detect common rhyme errors

Classical Arabic rhyme structure:
- الروي (al-rawi): The main rhyme letter
- الوصل (al-wasl): The connection after al-rawi
- الخروج (al-khuruj): The exit after al-wasl
- الردف (al-radif): The supporting letter before al-rawi
- التأسيس (al-ta'sis): The foundation before al-radif
"""

from typing import List, Optional, Dict, Tuple
from dataclasses import dataclass
from enum import Enum
from app.core.normalization import normalize_arabic_text, has_diacritics
from app.core.phonetics import extract_phonemes, Phoneme


class RhymeType(Enum):
    """Types of Arabic rhyme (أنواع القافية)."""
    MUTLAQAH = "مطلقة"  # Unrestricted (ends with vowel)
    MUQAYYADAH = "مقيدة"  # Restricted (ends with sukun)
    MUJARRADAH = "مجردة"  # Simple (no wasl or khuruj)
    MURAKKABAH = "مركبة"  # Complex (has wasl or khuruj)
    MUTAWATIR = "متواتر"  # With radif (supporting letter)
    MUTADARIK = "متدارك"  # With ta'sis (foundation)


class RhymeError(Enum):
    """Common rhyme errors in Arabic poetry."""
    IQWA = "إقواء"  # Changing rawi vowel
    SINA = "سناد"  # Changing rawi letter
    IKFA = "إكفاء"  # Changing rawi type (restricted/unrestricted)
    ITAA = "إطاء"  # Changing wasl after rawi
    INCONSISTENT_RADIF = "عدم اتساق الردف"  # Inconsistent radif


@dataclass
class QafiyahComponents:
    """
    Components of a qafiyah (rhyme structure).
    
    According to classical Arabic prosody, a complete qafiyah consists of:
    - ta'sis (تأسيس): Foundation letter before radif (optional)
    - radif (ردف): Supporting letter before rawi (optional)
    - rawi (روي): Main rhyme letter (required)
    - wasl (وصل): Connection after rawi (optional)
    - khuruj (خروج): Exit after wasl (optional)
    
    Example for "النجومِ" (an-nujumi):
    - rawi: م (meem)
    - wasl: ي (kasra vowel as yaa)
    - radif: و (waw before rawi)
    """
    rawi: str  # Main rhyme letter (حرف الروي)
    rawi_vowel: str  # Vowel of rawi (i, u, a, or '' for sukun)
    wasl: Optional[str] = None  # Connection after rawi (الوصل)
    khuruj: Optional[str] = None  # Exit vowel after wasl (الخروج)
    radif: Optional[str] = None  # Supporting letter before rawi (الردف)
    tasis: Optional[str] = None  # Foundation before radif (التأسيس)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary representation."""
        return {
            "rawi": self.rawi,
            "rawi_vowel": self.rawi_vowel,
            "wasl": self.wasl,
            "khuruj": self.khuruj,
            "radif": self.radif,
            "tasis": self.tasis,
        }
    
    def __str__(self) -> str:
        """String representation of qafiyah."""
        parts = []
        if self.tasis:
            parts.append(f"تأسيس:{self.tasis}")
        if self.radif:
            parts.append(f"ردف:{self.radif}")
        parts.append(f"روي:{self.rawi}")
        if self.wasl:
            parts.append(f"وصل:{self.wasl}")
        if self.khuruj:
            parts.append(f"خروج:{self.khuruj}")
        return " + ".join(parts)


@dataclass
class RhymePattern:
    """
    Complete rhyme pattern extracted from a verse.
    
    Attributes:
        verse_ending: Last 5-7 phonemes of the verse
        qafiyah: Identified qafiyah components
        rhyme_types: List of applicable rhyme type classifications
        rhyme_string: String representation of rhyme for comparison
    """
    verse_ending: List[Phoneme]
    qafiyah: QafiyahComponents
    rhyme_types: List[RhymeType]
    rhyme_string: str  # For easy comparison (e.g., "م-i-و")
    
    def to_dict(self) -> Dict:
        """Convert to dictionary representation."""
        return {
            "verse_ending": [str(p) for p in self.verse_ending],
            "qafiyah": self.qafiyah.to_dict(),
            "rhyme_types": [rt.value for rt in self.rhyme_types],
            "rhyme_string": self.rhyme_string,
        }


@dataclass
class RhymeAnalysisResult:
    """
    Result of rhyme consistency analysis across multiple verses.
    
    Attributes:
        is_consistent: Whether rhyme is consistent across all verses
        common_rawi: The common rhyme letter (if consistent)
        common_rawi_vowel: The common rawi vowel (if consistent)
        rhyme_patterns: List of rhyme patterns for each verse
        errors: List of detected rhyme errors with descriptions
        consistency_score: Score from 0.0 to 1.0 indicating rhyme quality
    """
    is_consistent: bool
    common_rawi: Optional[str]
    common_rawi_vowel: Optional[str]
    rhyme_patterns: List[RhymePattern]
    errors: List[Tuple[RhymeError, str, str]]  # (error_type, error_ar, error_en)
    consistency_score: float  # 0.0 to 1.0
    
    def to_dict(self) -> Dict:
        """Convert to dictionary representation."""
        return {
            "is_consistent": self.is_consistent,
            "common_rawi": self.common_rawi,
            "common_rawi_vowel": self.common_rawi_vowel,
            "rhyme_patterns": [rp.to_dict() for rp in self.rhyme_patterns],
            "errors": [
                {
                    "type": err[0].value,
                    "message_ar": err[1],
                    "message_en": err[2]
                }
                for err in self.errors
            ],
            "consistency_score": self.consistency_score,
        }


class RhymeAnalyzer:
    """Analyzer for Arabic poetry rhyme patterns."""
    
    # Letters that can be rawi (exclude weak letters in some contexts)
    VALID_RAWI_LETTERS = set("بتثجحخدذرزسشصضطظعغفقكلمنهويء")
    
    # Long vowel letters (ألف، واو، ياء مد)
    LONG_VOWEL_LETTERS = {"ا", "و", "ي"}
    
    # Letters that typically appear as radif
    RADIF_LETTERS = {"ا", "و", "ي", "ن"}
    
    def __init__(self):
        """Initialize rhyme analyzer."""
        pass
    
    def extract_qafiyah(self, verse: str) -> RhymePattern:
        """
        Extract qafiyah (rhyme pattern) from a verse.
        
        Process:
        1. Normalize and convert to phonemes
        2. Extract last 5-7 phonemes (verse ending)
        3. Identify rawi (last consonant with vowel, excluding weak positions)
        4. Identify wasl and khuruj (if present after rawi)
        5. Identify radif (if present before rawi)
        6. Identify ta'sis (if present before radif)
        7. Classify rhyme type
        
        Args:
            verse: Arabic poetry verse
            
        Returns:
            RhymePattern object with complete analysis
            
        Example:
            >>> analyzer = RhymeAnalyzer()
            >>> pattern = analyzer.extract_qafiyah("على قدر أهل العزم تأتي العزائم")
            >>> pattern.qafiyah.rawi
            'م'
        """
        # Normalize text
        normalized = normalize_arabic_text(verse)
        
        # Check if text has diacritics
        has_tashkeel = has_diacritics(verse)
        
        # Convert to phonemes
        phonemes = extract_phonemes(normalized, has_tashkeel=has_tashkeel)
        
        if len(phonemes) < 2:
            raise ValueError("Verse too short for rhyme analysis")
        
        # Extract last 5-7 phonemes for analysis
        ending_length = min(7, len(phonemes))
        verse_ending = phonemes[-ending_length:]
        
        # Identify rawi (main rhyme letter)
        rawi, rawi_vowel, rawi_index = self._find_rawi(verse_ending)
        
        # Identify wasl and khuruj (after rawi)
        wasl, khuruj = self._find_wasl_and_khuruj(verse_ending, rawi_index)
        
        # Identify radif (before rawi)
        radif = self._find_radif(verse_ending, rawi_index)
        
        # Identify tasis (before radif)
        tasis = self._find_tasis(verse_ending, rawi_index, radif)
        
        # Create qafiyah components
        qafiyah = QafiyahComponents(
            rawi=rawi,
            rawi_vowel=rawi_vowel,
            wasl=wasl,
            khuruj=khuruj,
            radif=radif,
            tasis=tasis
        )
        
        # Classify rhyme types
        rhyme_types = self._classify_rhyme_type(qafiyah)
        
        # Create rhyme string for comparison
        rhyme_string = self._create_rhyme_string(qafiyah)
        
        return RhymePattern(
            verse_ending=verse_ending,
            qafiyah=qafiyah,
            rhyme_types=rhyme_types,
            rhyme_string=rhyme_string
        )
    
    def _find_rawi(self, phonemes: List[Phoneme]) -> Tuple[str, str, int]:
        """
        Find the rawi (main rhyme letter) in verse ending.
        
        The rawi is typically the last consonant following classical rules:
        1. The last non-weak consonant (excluding و، ي، ا in certain positions)
        2. Can have a vowel (مطلقة) or sukun (مقيدة)
        3. Special handling for weak letters that are part of the root
        
        Returns:
            Tuple of (rawi_letter, rawi_vowel, index_in_phonemes)
        """
        # Strategy: Find the last "strong" consonant
        # A strong consonant is one that's likely part of the word root, not a grammatical suffix
        
        # Check the last phoneme first
        last_idx = len(phonemes) - 1
        last_phoneme = phonemes[last_idx]
        
        # If last phoneme is a strong consonant (not weak letter), use it
        if last_phoneme.consonant in self.VALID_RAWI_LETTERS:
            vowel = last_phoneme.vowel if not last_phoneme.is_sukun() else ''
            # Normalize long vowels
            if vowel in ['aa', 'uu', 'ii']:
                vowel = vowel[0]
            return (last_phoneme.consonant, vowel, last_idx)
        
        # If last is a weak letter, check previous consonant
        # This handles cases like "العزائم" where final م is the rawi, not the يم
        if last_idx > 0:
            prev_phoneme = phonemes[last_idx - 1]
            if prev_phoneme.consonant in self.VALID_RAWI_LETTERS:
                vowel = prev_phoneme.vowel if not prev_phoneme.is_sukun() else ''
                if vowel in ['aa', 'uu', 'ii']:
                    vowel = vowel[0]
                return (prev_phoneme.consonant, vowel, last_idx - 1)
        
        # Fallback: Search backwards for first valid rawi letter
        for i in range(len(phonemes) - 1, -1, -1):
            phoneme = phonemes[i]
            
            if phoneme.consonant in self.VALID_RAWI_LETTERS:
                vowel = phoneme.vowel if not phoneme.is_sukun() else ''
                if vowel in ['aa', 'uu', 'ii']:
                    vowel = vowel[0]
                return (phoneme.consonant, vowel, i)
        
        # Last resort: use the final phoneme regardless
        vowel = last_phoneme.vowel if not last_phoneme.is_sukun() else ''
        if vowel in ['aa', 'uu', 'ii']:
            vowel = vowel[0]
        return (last_phoneme.consonant, vowel, last_idx)
    
    def _find_wasl_and_khuruj(
        self, 
        phonemes: List[Phoneme], 
        rawi_index: int
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Find wasl (connection) and khuruj (exit) after rawi.
        
        - Wasl: A long vowel (ا، و، ي) after rawi
        - Khuruj: A vowel after wasl
        
        Returns:
            Tuple of (wasl, khuruj) or (None, None)
        """
        wasl = None
        khuruj = None
        
        # Check if there's a phoneme after rawi
        if rawi_index < len(phonemes) - 1:
            next_phoneme = phonemes[rawi_index + 1]
            
            # Check for wasl (long vowel letter)
            if next_phoneme.consonant in self.LONG_VOWEL_LETTERS:
                wasl = next_phoneme.consonant
                
                # Check for khuruj (vowel on wasl)
                if not next_phoneme.is_sukun():
                    khuruj = next_phoneme.vowel
        
        return (wasl, khuruj)
    
    def _find_radif(
        self, 
        phonemes: List[Phoneme], 
        rawi_index: int
    ) -> Optional[str]:
        """
        Find radif (supporting letter) before rawi.
        
        Radif is typically:
        - A long vowel (ا، و، ي) immediately before rawi
        - A noon (ن) before rawi in some cases
        
        Returns:
            Radif letter or None
        """
        if rawi_index > 0:
            prev_phoneme = phonemes[rawi_index - 1]
            
            # Check for radif (long vowel or noon)
            if prev_phoneme.consonant in self.RADIF_LETTERS:
                # Additional check: radif should have a long vowel
                if prev_phoneme.is_long_vowel() or prev_phoneme.consonant == 'ن':
                    return prev_phoneme.consonant
        
        return None
    
    def _find_tasis(
        self, 
        phonemes: List[Phoneme], 
        rawi_index: int,
        radif: Optional[str]
    ) -> Optional[str]:
        """
        Find ta'sis (foundation) before radif.
        
        Ta'sis appears when:
        - There's a radif present
        - There's an alif (ا) with a specific distance before radif
        
        Returns:
            Ta'sis letter or None
        """
        if not radif:
            return None
        
        # Ta'sis requires radif, so find radif index
        radif_index = rawi_index - 1
        
        # Check 2-3 positions before radif for alif
        if radif_index >= 2:
            for i in range(radif_index - 3, radif_index):
                if i >= 0 and phonemes[i].consonant == 'ا':
                    return 'ا'
        
        return None
    
    def _classify_rhyme_type(self, qafiyah: QafiyahComponents) -> List[RhymeType]:
        """
        Classify rhyme type based on qafiyah components.
        
        Types:
        - مطلقة (mutlaqah): Ends with vowel
        - مقيدة (muqayyadah): Ends with sukun
        - مجردة (mujarradah): No wasl or khuruj
        - مركبة (murakkabah): Has wasl or khuruj
        - متواتر (mutawatir): Has radif
        - متدارك (mutadarik): Has tasis
        
        Returns:
            List of applicable RhymeType enums
        """
        types = []
        
        # Check if mutlaqah or muqayyadah
        if qafiyah.rawi_vowel and qafiyah.rawi_vowel != '':
            types.append(RhymeType.MUTLAQAH)
        else:
            types.append(RhymeType.MUQAYYADAH)
        
        # Check if mujarradah or murakkabah
        if qafiyah.wasl or qafiyah.khuruj:
            types.append(RhymeType.MURAKKABAH)
        else:
            types.append(RhymeType.MUJARRADAH)
        
        # Check for radif
        if qafiyah.radif:
            types.append(RhymeType.MUTAWATIR)
        
        # Check for tasis
        if qafiyah.tasis:
            types.append(RhymeType.MUTADARIK)
        
        return types
    
    def _create_rhyme_string(self, qafiyah: QafiyahComponents) -> str:
        """
        Create a string representation of rhyme for comparison.
        
        Format: "[radif]-rawi-vowel[-wasl]"
        Example: "و-م-i" for وم with kasra
        
        Returns:
            Rhyme string for pattern matching
        """
        parts = []
        
        if qafiyah.radif:
            parts.append(qafiyah.radif)
        
        parts.append(qafiyah.rawi)
        parts.append(qafiyah.rawi_vowel if qafiyah.rawi_vowel else 'sukun')
        
        if qafiyah.wasl:
            parts.append(qafiyah.wasl)
        
        return "-".join(parts)
    
    def analyze_rhyme_consistency(
        self, 
        verses: List[str]
    ) -> RhymeAnalysisResult:
        """
        Analyze rhyme consistency across multiple verses.
        
        Checks for:
        1. إقواء (iqwa): Changing rawi vowel
        2. سناد (sina): Changing rawi letter
        3. إكفاء (ikfa): Changing rhyme type
        4. إطاء (itaa): Changing wasl
        5. Radif consistency
        
        Args:
            verses: List of Arabic poetry verses
            
        Returns:
            RhymeAnalysisResult with consistency analysis
            
        Example:
            >>> analyzer = RhymeAnalyzer()
            >>> verses = ["بيت أول", "بيت ثاني", "بيت ثالث"]
            >>> result = analyzer.analyze_rhyme_consistency(verses)
            >>> result.is_consistent
            True
        """
        if len(verses) < 2:
            raise ValueError("Need at least 2 verses for rhyme consistency analysis")
        
        # Extract rhyme patterns for all verses
        rhyme_patterns = []
        for verse in verses:
            try:
                pattern = self.extract_qafiyah(verse)
                rhyme_patterns.append(pattern)
            except Exception as e:
                # Skip verses that fail analysis
                continue
        
        if len(rhyme_patterns) < 2:
            raise ValueError("Could not extract rhyme patterns from verses")
        
        # Analyze consistency
        errors = []
        
        # Get reference pattern (first verse)
        ref_pattern = rhyme_patterns[0]
        ref_qafiyah = ref_pattern.qafiyah
        
        # Check each verse against reference
        for i, pattern in enumerate(rhyme_patterns[1:], start=1):
            qafiyah = pattern.qafiyah
            
            # Check for سناد (sina): Different rawi letter
            if qafiyah.rawi != ref_qafiyah.rawi:
                errors.append((
                    RhymeError.SINA,
                    f"البيت {i+1}: تغيير حرف الروي من '{ref_qafiyah.rawi}' إلى '{qafiyah.rawi}'",
                    f"Verse {i+1}: Rhyme letter changed from '{ref_qafiyah.rawi}' to '{qafiyah.rawi}'"
                ))
            
            # Check for إقواء (iqwa): Different rawi vowel
            elif qafiyah.rawi_vowel != ref_qafiyah.rawi_vowel:
                errors.append((
                    RhymeError.IQWA,
                    f"البيت {i+1}: تغيير حركة الروي من '{ref_qafiyah.rawi_vowel}' إلى '{qafiyah.rawi_vowel}'",
                    f"Verse {i+1}: Rawi vowel changed from '{ref_qafiyah.rawi_vowel}' to '{qafiyah.rawi_vowel}'"
                ))
            
            # Check for إكفاء (ikfa): Different rhyme type
            if (RhymeType.MUTLAQAH in ref_pattern.rhyme_types) != (RhymeType.MUTLAQAH in pattern.rhyme_types):
                errors.append((
                    RhymeError.IKFA,
                    f"البيت {i+1}: تغيير نوع القافية (مطلقة/مقيدة)",
                    f"Verse {i+1}: Rhyme type changed (unrestricted/restricted)"
                ))
            
            # Check for إطاء (itaa): Different wasl
            if qafiyah.wasl != ref_qafiyah.wasl:
                errors.append((
                    RhymeError.ITAA,
                    f"البيت {i+1}: تغيير الوصل",
                    f"Verse {i+1}: Wasl changed"
                ))
            
            # Check for inconsistent radif
            if qafiyah.radif != ref_qafiyah.radif:
                errors.append((
                    RhymeError.INCONSISTENT_RADIF,
                    f"البيت {i+1}: عدم اتساق الردف",
                    f"Verse {i+1}: Inconsistent radif"
                ))
        
        # Calculate consistency score
        total_checks = len(rhyme_patterns) - 1
        errors_count = len(errors)
        consistency_score = max(0.0, (total_checks - errors_count) / total_checks)
        
        # Determine if consistent (no errors)
        is_consistent = len(errors) == 0
        
        # Extract common rawi if consistent
        common_rawi = ref_qafiyah.rawi if is_consistent else None
        common_rawi_vowel = ref_qafiyah.rawi_vowel if is_consistent else None
        
        return RhymeAnalysisResult(
            is_consistent=is_consistent,
            common_rawi=common_rawi,
            common_rawi_vowel=common_rawi_vowel,
            rhyme_patterns=rhyme_patterns,
            errors=errors,
            consistency_score=consistency_score
        )


def analyze_verse_rhyme(verse: str) -> Tuple[RhymePattern, str, str]:
    """
    Convenience function to analyze rhyme of a single verse.
    
    Args:
        verse: Arabic poetry verse
        
    Returns:
        Tuple of (RhymePattern, rhyme_description_ar, rhyme_description_en)
        
    Example:
        >>> pattern, desc_ar, desc_en = analyze_verse_rhyme("على قدر أهل العزم تأتي العزائم")
        >>> desc_ar
        'القافية: روي:م + ردف:ئ (مطلقة)'
    """
    analyzer = RhymeAnalyzer()
    pattern = analyzer.extract_qafiyah(verse)
    
    # Generate descriptions
    desc_ar = f"القافية: {pattern.qafiyah}"
    desc_en = f"Qafiyah: rawi={pattern.qafiyah.rawi}"
    
    if pattern.qafiyah.radif:
        desc_en += f", radif={pattern.qafiyah.radif}"
    
    # Add type
    types_ar = ", ".join([rt.value for rt in pattern.rhyme_types])
    desc_ar += f" ({types_ar})"
    
    return (pattern, desc_ar, desc_en)


def analyze_poem_rhyme(verses: List[str]) -> Tuple[RhymeAnalysisResult, str, str]:
    """
    Convenience function to analyze rhyme consistency of a poem.
    
    Args:
        verses: List of Arabic poetry verses
        
    Returns:
        Tuple of (RhymeAnalysisResult, summary_ar, summary_en)
        
    Example:
        >>> result, summary_ar, summary_en = analyze_poem_rhyme(verses)
        >>> summary_ar
        'القافية متسقة - الروي: م'
    """
    analyzer = RhymeAnalyzer()
    result = analyzer.analyze_rhyme_consistency(verses)
    
    # Generate summary
    if result.is_consistent:
        summary_ar = f"القافية متسقة - الروي: {result.common_rawi}"
        summary_en = f"Consistent rhyme - rawi: {result.common_rawi}"
    else:
        summary_ar = f"القافية غير متسقة - {len(result.errors)} أخطاء"
        summary_en = f"Inconsistent rhyme - {len(result.errors)} errors"
    
    return (result, summary_ar, summary_en)
