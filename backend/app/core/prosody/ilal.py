"""
'Ilal (علل) - End-of-verse variations.

'Ilal are prosodic changes that apply ONLY to the final taf'ila of a verse.
Unlike zihafat (which can apply to any non-final position), 'ilal are
position-specific and often mandatory or very common in certain meters.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Callable, List, Optional, Set

from .tafila import Tafila


class IlahType(Enum):
    """
    Types of 'Ilal (end-of-verse variations).

    Major 'Ilal:
    - HADHF: Remove last sabab (حذف)
    - QAT: Make last letter sakin + remove preceding letter (قطع)
    - QASR: Make last letter sakin (قصر)
    - BATR: Remove last sabab + make sakin (بتر)
    - KASHF: Remove last sakin (كشف)
    - HADHDHAH: Remove half of last watad (حذذ)
    """

    HADHF = "حذف"  # Remove last sabab
    QAT = "قطع"  # Make last sakin + remove preceding
    QASR = "قصر"  # Make last letter sakin
    BATR = "بتر"  # Remove last sabab + make sakin
    KASHF = "كشف"  # Remove last sakin
    HADHDHAH = "حذذ"  # Remove half of last watad


@dataclass
class Ilah:
    """
    Represents an end-of-verse variation (علة).

    'Ilal apply ONLY to the final taf'ila in a verse or hemistich.

    Attributes:
        type: Type of 'ilah (e.g., IlahType.HADHF)
        name_ar: Arabic name (e.g., "حذف")
        name_en: English transliteration (e.g., "hadhf")
        description: What the 'ilah does
        transformation: Function to apply the transformation
        result_pattern: Expected resulting phonetic pattern
        allowed_meters: Set of meter IDs where this 'ilah is allowed
        frequency: How common this 'ilah is
        is_mandatory: Whether this 'ilah is required (not optional)
    """

    type: IlahType
    name_ar: str
    name_en: str
    description: str
    transformation: Callable[[str], str]
    letter_transformation: Optional[Callable] = None  # Letter-level transformation (new architecture)
    result_pattern: Optional[str] = None
    allowed_meters: Optional[Set[int]] = None
    frequency: str = "common"  # common, rare, very_rare
    is_mandatory: bool = False

    def __str__(self) -> str:
        """String representation (Arabic name)."""
        return self.name_ar

    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return f"Ilah({self.name_ar}, {self.name_en})"

    def apply(self, tafila: Tafila) -> Tafila:
        """
        Apply this 'ilah to a taf'ila.

        Args:
            tafila: Base taf'ila to transform

        Returns:
            New Tafila with transformation applied

        Raises:
            ValueError: If transformation fails
        """
        try:
            # Try letter-level transformation first (if available)
            if self.letter_transformation is not None and hasattr(tafila, 'letter_structure') and tafila.letter_structure is not None:
                result_structure = self.letter_transformation(tafila.letter_structure)
                new_phonetic = result_structure.phonetic_pattern

                # Create new taf'ila name indicating the 'ilah
                new_name = f"{tafila.name} ({self.name_ar})"

                return Tafila(
                    name=new_name,
                    phonetic=new_phonetic,
                    structure=f"{tafila.structure} + {self.name_ar}",
                    syllable_count=tafila.syllable_count,
                    letter_structure=result_structure,  # Preserve letter structure
                )
            else:
                # Fall back to pattern-based transformation (backward compatibility)
                new_phonetic = self.transformation(tafila.phonetic)

                # Create new taf'ila name indicating the 'ilah
                new_name = f"{tafila.name} ({self.name_ar})"

                return Tafila(
                    name=new_name,
                    phonetic=new_phonetic,
                    structure=f"{tafila.structure} + {self.name_ar}",
                    syllable_count=tafila.syllable_count,  # May change
                )
        except Exception as e:
            raise ValueError(f"Failed to apply {self.name_ar} to {tafila.name}: {e}")

    def can_apply_to_meter(self, meter_id: int) -> bool:
        """Check if this 'ilah can be applied to a specific meter."""
        if self.allowed_meters is None:
            return True  # No restrictions
        return meter_id in self.allowed_meters

    def to_dict(self) -> dict:
        """Convert to dictionary representation."""
        return {
            "type": self.type.value,
            "name_ar": self.name_ar,
            "name_en": self.name_en,
            "description": self.description,
            "frequency": self.frequency,
            "is_mandatory": self.is_mandatory,
        }


# ============================================================================
# Transformation Functions for 'Ilal
# ============================================================================


def hadhf_transform_letters(tafila_structure):
    """
    حَذْف (Ḥadhf) - Remove last sabab khafīf (letter-level implementation).

    Classical Definition:
    "الحَذْف هو إسقاط السبب الخفيف من آخر التفعيلة"
    Translation: "Ḥadhf is removal of the light sabab from the end of the tafʿīlah"

    A sabab khafīf = mutaḥarrik + sākin (e.g., فَعْ)
    This transformation removes the last 2 letters if they form this pattern.

    Args:
        tafila_structure: TafilaLetterStructure with letter-level representation

    Returns:
        New TafilaLetterStructure with last sabab removed
    """
    from .letter_structure import TafilaLetterStructure

    if len(tafila_structure.letters) < 2:
        return tafila_structure

    # Remove last 2 letters (assuming they form a sabab khafīf)
    new_letters = tafila_structure.letters[:-2]

    return TafilaLetterStructure(
        name=f"{tafila_structure.name} (modified)",
        letters=new_letters,
        structure_type=tafila_structure.structure_type
    )


def qat_transform_letters(tafila_structure):
    """
    قَطْع (Qaṭʿ) - Remove sākin of watad majmūʿ and make preceding sākin (letter-level implementation).

    Classical Definition:
    "القَطْع هو حذف ساكن الوتد المجموع وتسكين ما قبله"
    Translation: "Qaṭʿ is removal of the sākin of watad majmūʿ and making the preceding letter sākin"

    Args:
        tafila_structure: TafilaLetterStructure with letter-level representation

    Returns:
        New TafilaLetterStructure with qaṭʿ applied
    """
    from .letter_structure import TafilaLetterStructure, HarakaType, VowelQuality

    if len(tafila_structure.letters) < 2:
        return tafila_structure

    # Remove last letter
    new_letters = tafila_structure.letters[:-1].copy()

    # Make the new last letter sākin
    if len(new_letters) > 0:
        last_letter = new_letters[-1]
        new_letters[-1] = type(last_letter)(
            consonant=last_letter.consonant,
            haraka_type=HarakaType.SAKIN,
            vowel_quality=VowelQuality.SUKUN,
            has_shadda=last_letter.has_shadda,
            prosody_role=last_letter.prosody_role,
            position_in_tafila=last_letter.position_in_tafila
        )

    return TafilaLetterStructure(
        name=f"{tafila_structure.name} (modified)",
        letters=new_letters,
        structure_type=tafila_structure.structure_type
    )


def qasr_transform_letters(tafila_structure):
    """
    قَصْر (Qaṣr) - Make last mutaḥarrik letter sākin (letter-level implementation).

    Classical Definition:
    "القَصْر هو تسكين المتحرك الأخير"
    Translation: "Qaṣr is making the last mutaḥarrik letter sākin"

    Args:
        tafila_structure: TafilaLetterStructure with letter-level representation

    Returns:
        New TafilaLetterStructure with last mutaḥarrik made sākin
    """
    from .letter_structure import TafilaLetterStructure, HarakaType, VowelQuality

    if len(tafila_structure.letters) == 0:
        return tafila_structure

    # Find last mutaharrik
    last_mutaharrik_pos = None
    for i in range(len(tafila_structure.letters) - 1, -1, -1):
        if tafila_structure.letters[i].is_mutaharrik():
            last_mutaharrik_pos = i
            break

    if last_mutaharrik_pos is None:
        return tafila_structure

    # Make it sākin
    return tafila_structure.change_haraka_at_position(
        last_mutaharrik_pos,
        HarakaType.SAKIN,
        VowelQuality.SUKUN
    )


def kashf_transform_letters(tafila_structure):
    """
    كَشْف (Kashf) - Remove last sākin letter (letter-level implementation).

    Classical Definition:
    "الكَشْف هو حذف الساكن الأخير"
    Translation: "Kashf is removal of the last sākin letter"

    Args:
        tafila_structure: TafilaLetterStructure with letter-level representation

    Returns:
        New TafilaLetterStructure with last sākin removed
    """
    from .letter_structure import TafilaLetterStructure

    # Find last sakin/madd
    last_sakin_pos = None
    for i in range(len(tafila_structure.letters) - 1, -1, -1):
        letter = tafila_structure.letters[i]
        if letter.is_sakin() or letter.is_madd():
            last_sakin_pos = i
            break

    if last_sakin_pos is None:
        return tafila_structure

    # Remove it
    return tafila_structure.remove_letter_at_position(last_sakin_pos)


def batr_transform_letters(tafila_structure):
    """
    بَتْر (Batr) - Combined: ḤADHF + QAṢR (letter-level implementation).

    Classical Definition:
    "البَتْر هو حذف السبب الخفيف وتسكين ما قبله"
    Translation: "Batr is removal of light sabab and making the preceding sākin"

    Args:
        tafila_structure: TafilaLetterStructure with letter-level representation

    Returns:
        New TafilaLetterStructure with both transformations applied
    """
    # Apply ḤADHF first (remove last sabab)
    result = hadhf_transform_letters(tafila_structure)

    # Then apply QAṢR (make last mutaharrik sakin)
    result = qasr_transform_letters(result)

    return result


def hadhdhah_transform_letters(tafila_structure):
    """
    حَذَذ (Ḥadhdhah) - Remove half of last watad (letter-level implementation).

    Classical Definition:
    "الحَذَذ هو حذف نصف الوتد الأخير"
    Translation: "Ḥadhdhah is removal of half the last watad"

    Very rare transformation. Removes last letter.

    Args:
        tafila_structure: TafilaLetterStructure with letter-level representation

    Returns:
        New TafilaLetterStructure with last letter removed
    """
    from .letter_structure import TafilaLetterStructure

    if len(tafila_structure.letters) == 0:
        return tafila_structure

    # Remove last letter
    new_letters = tafila_structure.letters[:-1]

    return TafilaLetterStructure(
        name=f"{tafila_structure.name} (modified)",
        letters=new_letters,
        structure_type=tafila_structure.structure_type
    )


def hadhf_transform(pattern: str) -> str:
    """
    حذف - Remove last sabab (last two characters).

    Example: /o//o/o → /o//o (remove "o/o")
    """
    if len(pattern) >= 2:
        return pattern[:-2]
    return pattern


def qat_transform(pattern: str) -> str:
    """
    قطع - Make last letter sakin + remove preceding letter.

    Example: /o//o → /o//oo
    Logic: Remove second-to-last char, change last to 'o'
    """
    if len(pattern) >= 2:
        return pattern[:-2] + "oo"
    return pattern


def qasr_transform(pattern: str) -> str:
    """
    قصر - Make last letter sakin (remove final consonant).

    Example: /o//o → /o//
    """
    if len(pattern) >= 1 and pattern[-1] == "o":
        return pattern[:-1]
    return pattern


def batr_transform(pattern: str) -> str:
    """
    بتر - Remove last sabab + make sakin (combination).

    Example: /o//o/o → /o//
    """
    result = hadhf_transform(pattern)
    result = qasr_transform(result)
    return result


def kashf_transform(pattern: str) -> str:
    """
    كشف - Remove last sakin.

    Example: /o//o → /o///
    """
    # Find and remove last 'o'
    last_o = pattern.rfind("o")
    if last_o != -1:
        return pattern[:last_o] + pattern[last_o + 1 :]
    return pattern


def hadhdhah_transform(pattern: str) -> str:
    """
    حذذ - Remove half of last watad (rare).

    Example: //o/o/o → //o/o
    """
    if len(pattern) >= 2:
        return pattern[:-1]
    return pattern


# ============================================================================
# Predefined 'Ilal
# ============================================================================

# حذف - Very common 'ilah (used in many meters)
HADHF = Ilah(
    type=IlahType.HADHF,
    name_ar="حذف",
    name_en="hadhf",
    description="Remove last sabab (last two letters)",
    transformation=hadhf_transform,
    letter_transformation=hadhf_transform_letters,
    allowed_meters={1, 4, 6, 7, 9, 11, 12, 13, 15, 16},  # الرمل, الخفيف, المتقارب, etc.
    frequency="very_common",
)

# قطع - Less common
QAT = Ilah(
    type=IlahType.QAT,
    name_ar="قطع",
    name_en="qat'",
    description="Make last letter sakin + remove preceding",
    transformation=qat_transform,
    letter_transformation=qat_transform_letters,
    allowed_meters={2, 3, 4, 6, 11, 14},  # الكامل, البسيط, الوافر
    frequency="rare",
)

# قصر - Common in several meters
QASR = Ilah(
    type=IlahType.QASR,
    name_ar="قصر",
    name_en="qasr",
    description="Make last letter sakin (remove final consonant)",
    transformation=qasr_transform,
    letter_transformation=qasr_transform_letters,
    allowed_meters={1, 5, 7, 8, 9, 16},  # الطويل, الرجز, السريع, المديد
    frequency="common",
)

# بتر - Rare
BATR = Ilah(
    type=IlahType.BATR,
    name_ar="بتر",
    name_en="batr",
    description="Remove last sabab + make sakin",
    transformation=batr_transform,
    letter_transformation=batr_transform_letters,
    allowed_meters={5, 7},  # الرجز, الخفيف
    frequency="rare",
)

# كشف - Rare
KASHF = Ilah(
    type=IlahType.KASHF,
    name_ar="كشف",
    name_en="kashf",
    description="Remove last sakin",
    transformation=kashf_transform,
    letter_transformation=kashf_transform_letters,
    allowed_meters={8, 10, 12},  # السريع, المنسرح
    frequency="rare",
)

# حذذ - Very rare
HADHDHAH = Ilah(
    type=IlahType.HADHDHAH,
    name_ar="حذذ",
    name_en="hadhdhah",
    description="Remove half of last watad",
    transformation=hadhdhah_transform,
    letter_transformation=hadhdhah_transform_letters,
    allowed_meters={},  # Very specialized usage
    frequency="very_rare",
)


# Registry of all predefined 'ilal
ILAL_REGISTRY = {
    IlahType.HADHF: HADHF,
    IlahType.QAT: QAT,
    IlahType.QASR: QASR,
    IlahType.BATR: BATR,
    IlahType.KASHF: KASHF,
    IlahType.HADHDHAH: HADHDHAH,
}


def get_ilah(ilah_type: IlahType) -> Optional[Ilah]:
    """Get an 'ilah by its type."""
    return ILAL_REGISTRY.get(ilah_type)


def get_ilal_for_meter(meter_id: int) -> List[Ilah]:
    """
    Get all allowed 'ilal for a specific meter.

    Args:
        meter_id: Meter ID (1-16)

    Returns:
        List of Ilah objects allowed for this meter
    """
    return [
        ilah for ilah in ILAL_REGISTRY.values() if ilah.can_apply_to_meter(meter_id)
    ]


def apply_ilah(tafila: Tafila, ilah: Ilah) -> Tafila:
    """
    Apply an 'ilah to a taf'ila (final position only).

    Args:
        tafila: Base taf'ila (should be final one in verse)
        ilah: 'Ilah to apply

    Returns:
        New Tafila with transformation applied
    """
    return ilah.apply(tafila)


def list_all_ilal() -> List[Ilah]:
    """Get list of all predefined 'ilal."""
    return list(ILAL_REGISTRY.values())
