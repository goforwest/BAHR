"""
Letter-level prosodic representation.

This module provides the foundation for classical Arabic prosody analysis
at the letter level (حرف), as defined by Al-Khalīl ibn Aḥmad.

Classical Arabic prosody operates on individual letters (حروف) with their
vocalizations (حركات), not on abstract phonetic patterns. This module
provides the data structures to represent and manipulate prosodic units
at the correct level of abstraction.

References:
    - Phase 1 Verification Report: docs/phase1/PHASE1_FINAL_REPORT.md
    - Classical Ziḥāfāt Definitions: docs/phase1/zihafat_ilal_verification.yaml
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Tuple


class HarakaType(Enum):
    """
    Types of ḥaraka (vocalization) on Arabic letters.

    Classical prosody distinguishes three fundamental types:
    - MUTAHARRIK: Letter with short vowel (متحرك) - "moving"
    - SAKIN: Letter with sukūn (ساكن) - "still"
    - MADD: Long vowel letter (حرف مد) - vowel extension

    These categories determine how prosodic transformations apply.

    Examples:
        >>> # فَ = letter ف with fatḥa (mutaḥarrik)
        >>> HarakaType.MUTAHARRIK

        >>> # نْ = letter ن with sukūn (sākin)
        >>> HarakaType.SAKIN

        >>> # ا after fatḥa (madd letter extending to long vowel)
        >>> HarakaType.MADD
    """
    MUTAHARRIK = "mutaharrik"  # Short vowel (fatḥa, ḍamma, kasra)
    SAKIN = "sakin"            # Sukūn (no vowel)
    MADD = "madd"              # Long vowel (alef, wāw, yāʾ after compatible vowel)


class VowelQuality(Enum):
    """
    Quality of vowel (which specific vowel, if any).

    This distinguishes between the three short vowels, three long vowels,
    and the absence of vowel (sukūn).

    Values:
        FATHA: Fatḥa (َ) - 'a' sound
        DAMMA: Ḍamma (ُ) - 'u' sound
        KASRA: Kasra (ِ) - 'i' sound
        SUKUN: Sukūn (no vowel)
        AA: Long alef - 'ā' sound
        UU: Long wāw - 'ū' sound
        II: Long yāʾ - 'ī' sound
    """
    FATHA = "a"      # Fatḥa (َ)
    DAMMA = "u"      # Ḍamma (ُ)
    KASRA = "i"      # Kasra (ِ)
    SUKUN = ""       # Sukūn (no vowel)
    AA = "aa"        # Long alef
    UU = "uu"        # Long wāw
    II = "ii"        # Long yāʾ


class ProsodyRole(Enum):
    """
    Role of letter in prosodic structure.

    Used to identify sabab (سبب) and watad (وتد) boundaries.
    This is important for understanding which transformations can apply.

    Classical prosodic units:
        - Sabab Khafīf (السبب الخفيف): Light sabab = mutaḥarrik + sākin
        - Sabab Thaqīl (السبب الثقيل): Heavy sabab = mutaḥarrik + mutaḥarrik
        - Watad Majmūʿ (الوتد المجموع): Joined watad = mut. + mut. + sākin
        - Watad Mafrūq (الوتد المفروق): Separated watad = mut. + madd + mut.
    """
    SABAB_KHAFIF_START = "sabab_khafif_start"    # Start of light sabab
    SABAB_KHAFIF_END = "sabab_khafif_end"        # End of light sabab
    SABAB_THAQIL_START = "sabab_thaqil_start"    # Start of heavy sabab
    SABAB_THAQIL_END = "sabab_thaqil_end"        # End of heavy sabab
    WATAD_MAJMU_START = "watad_majmu_start"      # Start of majmūʿ watad
    WATAD_MAJMU_MID = "watad_majmu_mid"          # Middle of majmūʿ watad
    WATAD_MAJMU_END = "watad_majmu_end"          # End of majmūʿ watad
    WATAD_MAFRUQ_START = "watad_mafruq_start"    # Start of mafrūq watad
    WATAD_MAFRUQ_MID = "watad_mafruq_mid"        # Middle (madd letter)
    WATAD_MAFRUQ_END = "watad_mafruq_end"        # End of mafrūq watad
    UNKNOWN = "unknown"


@dataclass
class LetterUnit:
    """
    Represents a single Arabic letter in prosodic analysis.

    This is the atomic unit for classical prosody transformations.
    Each letter has a consonant and a vocalization (ḥaraka).

    Attributes:
        consonant: The Arabic consonant character (ح ر ف)
        haraka_type: Type of vocalization (mutaḥarrik, sākin, madd)
        vowel_quality: Which vowel (if any)
        has_shadda: Whether letter has gemination (shadda/tashdīd)
        prosody_role: Role in sabab/watad structure
        position_in_tafila: 1-indexed position (1 = first letter)

    Examples:
        >>> # ف with fatḥa (فَ)
        >>> LetterUnit('ف', HarakaType.MUTAHARRIK, VowelQuality.FATHA)
        LetterUnit(consonant='ف', haraka_type=HarakaType.MUTAHARRIK, vowel_quality=VowelQuality.FATHA)

        >>> # ن with sukūn (نْ)
        >>> LetterUnit('ن', HarakaType.SAKIN, VowelQuality.SUKUN)
        LetterUnit(consonant='ن', haraka_type=HarakaType.SAKIN, vowel_quality=VowelQuality.SUKUN)

        >>> # Long alef (ا after fatḥa)
        >>> LetterUnit('ا', HarakaType.MADD, VowelQuality.AA)
        LetterUnit(consonant='ا', haraka_type=HarakaType.MADD, vowel_quality=VowelQuality.AA)
    """
    consonant: str
    haraka_type: HarakaType
    vowel_quality: VowelQuality
    has_shadda: bool = False
    prosody_role: ProsodyRole = ProsodyRole.UNKNOWN
    position_in_tafila: int = 0

    def is_mutaharrik(self) -> bool:
        """
        Check if letter is mutaḥarrik (has short vowel).

        Returns:
            True if letter has short vowel (fatḥa, ḍamma, or kasra)

        Example:
            >>> letter = LetterUnit('ف', HarakaType.MUTAHARRIK, VowelQuality.FATHA)
            >>> letter.is_mutaharrik()
            True
        """
        return self.haraka_type == HarakaType.MUTAHARRIK

    def is_sakin(self) -> bool:
        """
        Check if letter is sākin (has sukūn).

        Returns:
            True if letter has sukūn (no vowel)

        Example:
            >>> letter = LetterUnit('ن', HarakaType.SAKIN, VowelQuality.SUKUN)
            >>> letter.is_sakin()
            True
        """
        return self.haraka_type == HarakaType.SAKIN

    def is_madd(self) -> bool:
        """
        Check if letter is madd (long vowel).

        Returns:
            True if letter is a long vowel (aa, uu, ii)

        Example:
            >>> letter = LetterUnit('ا', HarakaType.MADD, VowelQuality.AA)
            >>> letter.is_madd()
            True
        """
        return self.haraka_type == HarakaType.MADD

    def to_phonetic_symbol(self) -> str:
        """
        Convert to phonetic symbol for pattern representation.

        Classical prosody notation:
        - '/' = mutaḥarrik (moving/light)
        - 'o' = sākin or madd (still/heavy)

        Returns:
            '/' for mutaḥarrik, 'o' for sākin/madd

        Example:
            >>> letter = LetterUnit('ف', HarakaType.MUTAHARRIK, VowelQuality.FATHA)
            >>> letter.to_phonetic_symbol()
            '/'
            >>> letter = LetterUnit('ن', HarakaType.SAKIN, VowelQuality.SUKUN)
            >>> letter.to_phonetic_symbol()
            'o'
        """
        if self.is_mutaharrik():
            return '/'
        elif self.is_sakin() or self.is_madd():
            return 'o'
        else:
            return '?'  # Should never happen

    def __str__(self) -> str:
        """
        String representation showing consonant and ḥaraka.

        Returns:
            Arabic letter with diacritic mark

        Example:
            >>> letter = LetterUnit('ف', HarakaType.MUTAHARRIK, VowelQuality.FATHA)
            >>> str(letter)
            'فَ'
        """
        if self.is_mutaharrik():
            vowel_mark = {
                'a': '\u064e',  # Fatḥa َ
                'u': '\u064f',  # Ḍamma ُ
                'i': '\u0650',  # Kasra ِ
            }.get(self.vowel_quality.value, '')
            shadda_mark = '\u0651' if self.has_shadda else ''
            return f"{self.consonant}{shadda_mark}{vowel_mark}"
        elif self.is_sakin():
            shadda_mark = '\u0651' if self.has_shadda else ''
            return f"{self.consonant}{shadda_mark}\u0652"  # Sukūn ْ
        else:  # madd
            return self.consonant


@dataclass
class TafilaLetterStructure:
    """
    Letter-level representation of a tafʿīlah.

    This allows classical prosody transformations to operate at the
    correct level of abstraction (letters with ḥarakāt, not phonetic patterns).

    Classical prosody transformations (ziḥāfāt and ʿilal) are defined in terms
    of letter operations:
        - "Remove the 5th sākin letter" (القَبْض)
        - "Make the 2nd mutaḥarrik letter sākin" (الإِضْمَار)
        - "Remove the last sabab" (الحَذْف)

    This class enables these operations to be performed correctly.

    Attributes:
        name: Arabic name of tafʿīlah (e.g., "فعولن")
        letters: List of LetterUnit objects (the core representation)
        phonetic_pattern: Derived /o pattern (computed from letters)
        structure_type: Prosodic structure description

    Examples:
        >>> # فَعُولُنْ = fa-ʿū-lun
        >>> faculun = TafilaLetterStructure(
        ...     name="فعولن",
        ...     letters=[
        ...         LetterUnit('ف', HarakaType.MUTAHARRIK, VowelQuality.FATHA),
        ...         LetterUnit('ع', HarakaType.MUTAHARRIK, VowelQuality.DAMMA),
        ...         LetterUnit('و', HarakaType.MADD, VowelQuality.UU),
        ...         LetterUnit('ل', HarakaType.MUTAHARRIK, VowelQuality.DAMMA),
        ...         LetterUnit('ن', HarakaType.SAKIN, VowelQuality.SUKUN),
        ...     ]
        ... )
        >>> faculun.phonetic_pattern
        '//o//o'
        >>> len(faculun.letters)
        5
    """
    name: str
    letters: List[LetterUnit]
    phonetic_pattern: str = field(init=False)
    structure_type: str = ""

    def __post_init__(self):
        """Compute phonetic pattern from letters and validate."""
        self.phonetic_pattern = self.compute_phonetic_pattern()
        self._assign_prosody_roles()

        # Validate
        if not self.name:
            raise ValueError("Tafʿīlah name cannot be empty")
        if not self.letters:
            raise ValueError("Tafʿīlah must have at least one letter")

    def compute_phonetic_pattern(self) -> str:
        """
        Derive phonetic pattern from letter sequence.

        This is the key connection between letter-level representation
        and the existing pattern-based detection system.

        Returns:
            Pattern string like "/o//o" derived from letter ḥarakāt

        Example:
            >>> # فَعُولُنْ = / (mut.) + / (mut.) + o (madd) + / (mut.) + o (sakin)
            >>> letters = [...]
            >>> structure = TafilaLetterStructure("فعولن", letters)
            >>> structure.compute_phonetic_pattern()
            '//o//o'
        """
        return ''.join(letter.to_phonetic_symbol() for letter in self.letters)

    def _assign_prosody_roles(self):
        """
        Assign prosodic roles (sabab, watad boundaries) to letters.

        This analyzes the letter sequence and identifies the classical
        sabab/watad structure based on ḥaraka patterns.

        Note: This is a placeholder for future enhancement. Currently,
        prosodic roles are left as UNKNOWN. Full implementation would
        require parsing the structure definition or using heuristics.
        """
        # TODO: Implement sabab/watad boundary detection
        # This would require:
        # 1. Pattern matching on haraka sequences
        # 2. Understanding of tafʿīlah structure (sabab+watad, etc.)
        # 3. Rules for identifying boundaries
        # For now, leave as UNKNOWN
        pass

    def get_mutaharrik_letters(self) -> List[Tuple[int, LetterUnit]]:
        """
        Get all mutaḥarrik letters with their positions.

        This is used by transformations that operate on mutaḥarrik letters,
        such as iḍmār (making a mutaḥarrik letter sākin).

        Returns:
            List of (position, LetterUnit) tuples for all mutaḥarrik letters

        Example:
            >>> # فَعُولُنْ has 3 mutaharriks: ف(0), ع(1), ل(3)
            >>> structure.get_mutaharrik_letters()
            [(0, LetterUnit('ف', ...)), (1, LetterUnit('ع', ...)), (3, LetterUnit('ل', ...))]
        """
        return [
            (i, letter) for i, letter in enumerate(self.letters)
            if letter.is_mutaharrik()
        ]

    def get_sakin_letters(self) -> List[Tuple[int, LetterUnit]]:
        """
        Get all sākin letters with their positions.

        This is used by transformations that operate on sākin letters,
        such as qabd (removing a sākin letter) and khabn (removing a sākin).

        Note: In classical prosody, madd letters are often counted as sākin
        for the purposes of transformations. This function returns only
        explicit sukūn letters. Use get_sakin_and_madd_letters() for both.

        Returns:
            List of (position, LetterUnit) tuples for all sākin letters

        Example:
            >>> # فَعُولُنْ has 1 sakin: ن(4)
            >>> structure.get_sakin_letters()
            [(4, LetterUnit('ن', HarakaType.SAKIN, ...))]
        """
        return [
            (i, letter) for i, letter in enumerate(self.letters)
            if letter.is_sakin()
        ]

    def get_sakin_and_madd_letters(self) -> List[Tuple[int, LetterUnit]]:
        """
        Get all sākin and madd letters with their positions.

        In classical prosody, both explicit sukūn and madd (long vowel) letters
        are often treated as "sākin" for transformation purposes, because both
        represent a "heavy" or "still" position in the prosodic pattern.

        Returns:
            List of (position, LetterUnit) tuples for sākin and madd letters

        Example:
            >>> # فَعُولُنْ has 2 sakin/madd: و(2, madd), ن(4, sakin)
            >>> structure.get_sakin_and_madd_letters()
            [(2, LetterUnit('و', HarakaType.MADD, ...)), (4, LetterUnit('ن', ...))]
        """
        return [
            (i, letter) for i, letter in enumerate(self.letters)
            if letter.is_sakin() or letter.is_madd()
        ]

    def get_nth_sakin(self, n: int, include_madd: bool = True) -> Optional[Tuple[int, LetterUnit]]:
        """
        Get the nth sākin letter (1-indexed).

        This is the core operation for transformations like:
        - QABD: Remove 5th sākin
        - KHABN: Remove 2nd sākin
        - ṬAYY: Remove 4th sākin
        - KAFF: Remove 7th sākin

        Args:
            n: Which sākin to get (1 = first sākin, 2 = second, etc.)
            include_madd: Whether to count madd letters as sākin (default: True)
                         This matches classical prosody where madd = "heavy" position

        Returns:
            (position, LetterUnit) tuple or None if not enough sakins

        Example:
            >>> # فَعُولُنْ: 1st sakin = و(madd), 2nd sakin = ن
            >>> structure.get_nth_sakin(1)
            (2, LetterUnit('و', HarakaType.MADD, ...))
            >>> structure.get_nth_sakin(2)
            (4, LetterUnit('ن', HarakaType.SAKIN, ...))
            >>> structure.get_nth_sakin(3)
            None
        """
        if include_madd:
            sakin_letters = self.get_sakin_and_madd_letters()
        else:
            sakin_letters = self.get_sakin_letters()

        if 0 < n <= len(sakin_letters):
            return sakin_letters[n - 1]
        return None

    def get_nth_mutaharrik(self, n: int) -> Optional[Tuple[int, LetterUnit]]:
        """
        Get the nth mutaḥarrik letter (1-indexed).

        This is the core operation for transformations like:
        - IḌMĀR: Make 2nd mutaḥarrik sākin
        - WAQṢ: Remove 2nd mutaḥarrik
        - ʿAṢB: Remove 5th mutaḥarrik

        Args:
            n: Which mutaḥarrik to get (1 = first, 2 = second, etc.)

        Returns:
            (position, LetterUnit) tuple or None if not enough mutaharriks

        Example:
            >>> # فَعُولُنْ: 1st mut. = ف, 2nd mut. = ع, 3rd mut. = ل
            >>> structure.get_nth_mutaharrik(1)
            (0, LetterUnit('ف', HarakaType.MUTAHARRIK, ...))
            >>> structure.get_nth_mutaharrik(2)
            (1, LetterUnit('ع', HarakaType.MUTAHARRIK, ...))
            >>> structure.get_nth_mutaharrik(4)
            None
        """
        mutaharrik_letters = self.get_mutaharrik_letters()
        if 0 < n <= len(mutaharrik_letters):
            return mutaharrik_letters[n - 1]
        return None

    def remove_letter_at_position(self, position: int) -> 'TafilaLetterStructure':
        """
        Create new tafʿīlah with letter at position removed.

        This is used by ziḥāfāt transformations that remove letters:
        - QABD, KHABN, ṬAYY, KAFF (remove sākin letters)
        - WAQṢ, ʿAṢB (remove mutaḥarrik letters)

        Args:
            position: 0-indexed position to remove

        Returns:
            New TafilaLetterStructure with letter removed

        Raises:
            ValueError: If position is out of bounds

        Example:
            >>> # فَعُولُنْ → remove position 2 (و) → فَعُلُنْ
            >>> structure.remove_letter_at_position(2)
            TafilaLetterStructure('فعولن (modified)', pattern='///o')
        """
        if not (0 <= position < len(self.letters)):
            raise ValueError(
                f"Invalid position {position} for tafʿīlah with {len(self.letters)} letters"
            )

        new_letters = self.letters[:position] + self.letters[position + 1:]
        return TafilaLetterStructure(
            name=f"{self.name} (modified)",
            letters=new_letters,
            structure_type=self.structure_type
        )

    def change_haraka_at_position(
        self,
        position: int,
        new_haraka_type: HarakaType,
        new_vowel_quality: VowelQuality
    ) -> 'TafilaLetterStructure':
        """
        Create new tafʿīlah with ḥaraka changed at position.

        This is used by transformations that modify vocalization:
        - IḌMĀR: Make mutaḥarrik → sākin
        - QAṢR: Long vowel → short vowel (ʿillah)

        Args:
            position: 0-indexed position to modify
            new_haraka_type: New ḥaraka type (MUTAHARRIK, SAKIN, or MADD)
            new_vowel_quality: New vowel quality

        Returns:
            New TafilaLetterStructure with modified letter

        Raises:
            ValueError: If position is out of bounds

        Example:
            >>> # فَعُولُنْ → make position 1 (ع) sakin → فَعْوُلُنْ
            >>> structure.change_haraka_at_position(
            ...     1, HarakaType.SAKIN, VowelQuality.SUKUN
            ... )
            TafilaLetterStructure('فعولن (modified)', pattern='/o/o//o')
        """
        if not (0 <= position < len(self.letters)):
            raise ValueError(
                f"Invalid position {position} for tafʿīlah with {len(self.letters)} letters"
            )

        new_letters = self.letters.copy()
        old_letter = self.letters[position]
        new_letters[position] = LetterUnit(
            consonant=old_letter.consonant,
            haraka_type=new_haraka_type,
            vowel_quality=new_vowel_quality,
            has_shadda=old_letter.has_shadda,
            prosody_role=old_letter.prosody_role,
            position_in_tafila=old_letter.position_in_tafila
        )

        return TafilaLetterStructure(
            name=f"{self.name} (modified)",
            letters=new_letters,
            structure_type=self.structure_type
        )

    def to_dict(self) -> dict:
        """
        Convert to dictionary representation.

        Returns:
            Dictionary with letter structure data

        Example:
            >>> structure.to_dict()
            {
                'name': 'فعولن',
                'letters': [
                    {'consonant': 'ف', 'haraka_type': 'mutaharrik', ...},
                    ...
                ],
                'phonetic_pattern': '//o//o',
                'structure_type': 'sabab+watad'
            }
        """
        return {
            'name': self.name,
            'letters': [
                {
                    'consonant': letter.consonant,
                    'haraka_type': letter.haraka_type.value,
                    'vowel_quality': letter.vowel_quality.value,
                    'has_shadda': letter.has_shadda,
                    'prosody_role': letter.prosody_role.value
                }
                for letter in self.letters
            ],
            'phonetic_pattern': self.phonetic_pattern,
            'structure_type': self.structure_type
        }

    def __str__(self) -> str:
        """
        String representation showing Arabic letters with ḥarakāt.

        Returns:
            Vocalized Arabic text

        Example:
            >>> str(structure)
            'فَعُولُنْ'
        """
        return ''.join(str(letter) for letter in self.letters)

    def __repr__(self) -> str:
        """
        Developer representation.

        Returns:
            String showing name and pattern

        Example:
            >>> repr(structure)
            "TafilaLetterStructure('فعولن', pattern='//o//o')"
        """
        return f"TafilaLetterStructure('{self.name}', pattern='{self.phonetic_pattern}')"


def parse_tafila_from_text(tafila_name: str, text: str) -> TafilaLetterStructure:
    """
    Parse a tafʿīlah from vocalized Arabic text.

    This converts vocalized text (with tashkeel/diacritics) into letter-level
    structure using the existing phoneme extraction system.

    The function bridges between the existing phonetics module and the new
    letter-level representation system.

    Args:
        tafila_name: Name of tafʿīlah (e.g., "فعولن")
        text: Vocalized Arabic text (e.g., "فَعُولُنْ")

    Returns:
        TafilaLetterStructure with letters parsed from text

    Raises:
        ValueError: If text cannot be parsed

    Examples:
        >>> parse_tafila_from_text("فعولن", "فَعُولُنْ")
        TafilaLetterStructure('فعولن', pattern='//o//o')

        >>> # مَفَاعِيلُنْ
        >>> parse_tafila_from_text("مفاعيلن", "مَفَاعِيلُنْ")
        TafilaLetterStructure('مفاعيلن', pattern='//o/o/o')

        >>> # فَاعِلُنْ
        >>> parse_tafila_from_text("فاعلن", "فَاعِلُنْ")
        TafilaLetterStructure('فاعلن', pattern='/o//o')
    """
    from app.core.phonetics import extract_phonemes, Phoneme

    # Extract phonemes using existing phonetics module
    phonemes = extract_phonemes(text, has_tashkeel=True)

    if not phonemes:
        raise ValueError(f"Could not extract phonemes from text: {text}")

    # Convert phonemes to letter units
    letters = []

    for i, phoneme in enumerate(phonemes):
        # Determine haraka type and vowel quality
        if phoneme.is_long_vowel():
            # Long vowel (madd letter)
            haraka_type = HarakaType.MADD
            # Map long vowel to VowelQuality
            vowel_map = {
                'aa': VowelQuality.AA,
                'uu': VowelQuality.UU,
                'ii': VowelQuality.II,
            }
            vowel_quality = vowel_map.get(phoneme.vowel, VowelQuality.AA)

        elif phoneme.is_sukun():
            # Sākin (sukūn)
            haraka_type = HarakaType.SAKIN
            vowel_quality = VowelQuality.SUKUN

        else:
            # Mutaḥarrik (short vowel)
            haraka_type = HarakaType.MUTAHARRIK
            # Map short vowel to VowelQuality
            vowel_map = {
                'a': VowelQuality.FATHA,
                'u': VowelQuality.DAMMA,
                'i': VowelQuality.KASRA,
            }
            vowel_quality = vowel_map.get(phoneme.vowel, VowelQuality.FATHA)

        # Create letter unit
        letter = LetterUnit(
            consonant=phoneme.consonant,
            haraka_type=haraka_type,
            vowel_quality=vowel_quality,
            has_shadda=phoneme.has_shadda,
            position_in_tafila=i + 1  # 1-indexed
        )
        letters.append(letter)

    # Create and return letter structure
    return TafilaLetterStructure(
        name=tafila_name,
        letters=letters
    )


def parse_tafila_from_pattern_template(
    tafila_name: str,
    pattern: str,
    template: str
) -> TafilaLetterStructure:
    """
    Parse tafʿīlah from pattern and letter template.

    This is used to create letter structures for base tafāʿīl where
    we know the classical letter structure but don't have vocalized text.

    Template format:
        - C = consonant letter position (generic)
        - v = short vowel (mutaḥarrik)
        - vv = long vowel (madd)
        - c = sukūn (sākin)

    Args:
        tafila_name: Name (e.g., "فعولن")
        pattern: Phonetic pattern (e.g., "//o//o")
        template: Letter template (e.g., "CvCvvCvC" for فَعُولُنْ)

    Returns:
        TafilaLetterStructure

    Raises:
        NotImplementedError: Not yet implemented (future enhancement)

    Examples:
        >>> # Future: Create structure from template
        >>> parse_tafila_from_pattern_template(
        ...     "فعولن", "//o//o", "CvCvvCvC"
        ... )
        TafilaLetterStructure('فعولن', pattern='//o//o')

    Note:
        This function is not implemented in Phase 2. It is reserved for
        future enhancement if needed. Currently, we use parse_tafila_from_text()
        with vocalized Arabic text, which is more straightforward and reliable.
    """
    # TODO: Implement template parsing if needed
    # This would be used for programmatic generation of tafāʿīl
    # Currently not needed since we have vocalized text for all base tafāʿīl
    raise NotImplementedError(
        "Template parsing not yet implemented. "
        "Use parse_tafila_from_text() with vocalized Arabic text instead."
    )
