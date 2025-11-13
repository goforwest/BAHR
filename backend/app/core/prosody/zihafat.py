"""
Zihafat (زحافات) - Prosodic variations.

Zihafat are systematic transformations allowed in Arabic poetry meters.
They modify base tafa'il according to strict classical prosody rules.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Callable, List, Optional, Set

from .tafila import Tafila


class ZahafType(Enum):
    """
    Types of Zihafat (prosodic variations).

    Single Zihafat (مفرد):
    - KHABN: Remove 2nd sakin (خبن)
    - TAYY: Remove 4th sakin (طي)
    - QABD: Remove 5th sakin (قبض)
    - KAFF: Remove 7th sakin (كف)
    - WAQS: Remove 2nd mutaharrik (وقص)
    - ASB: Remove 5th mutaharrik (عصب)
    - AQL: Remove 5th sakin - variant (عقل)
    - IDMAR: Make 2nd letter sakin (إضمار)

    Double Zihafat (مزدوج):
    - KHABL: Khabn + Tayy (خبل)
    - KHAZL: Idmar + Tayy (خزل)
    - SHAKL: Khabn + Kaff (شكل)
    """

    # Single Zihafat
    KHABN = "خبن"  # Remove 2nd sakin
    TAYY = "طي"  # Remove 4th sakin
    QABD = "قبض"  # Remove 5th sakin
    KAFF = "كف"  # Remove 7th sakin
    WAQS = "وقص"  # Remove 2nd mutaharrik
    ASB = "عصب"  # Remove 5th mutaharrik
    AQL = "عقل"  # Remove 5th sakin (variant)
    IDMAR = "إضمار"  # Make 2nd letter sakin

    # Double Zihafat
    KHABL = "خبل"  # Khabn + Tayy
    KHAZL = "خزل"  # Idmar + Tayy
    SHAKL = "شكل"  # Khabn + Kaff


@dataclass
class Zahaf:
    """
    Represents a prosodic variation (زحاف).

    Attributes:
        type: Type of zahaf (e.g., ZahafType.KHABN)
        name_ar: Arabic name (e.g., "خبن")
        name_en: English transliteration (e.g., "khabn")
        description: What the zahaf does
        transformation: Function to apply the transformation
        result_pattern: Expected resulting phonetic pattern
        is_double: Whether this is a double zahaf (مزدوج)
        allowed_meters: Set of meter IDs where this zahaf is allowed
        allowed_positions: Set of positions where allowed (1-indexed)
        frequency: How common this zahaf is (common, rare, very_rare)
    """

    type: ZahafType
    name_ar: str
    name_en: str
    description: str
    transformation: Callable[[str], str]
    result_pattern: Optional[str] = None
    is_double: bool = False
    allowed_meters: Optional[Set[int]] = None
    allowed_positions: Optional[Set[int]] = None
    frequency: str = "common"  # common, rare, very_rare

    def __str__(self) -> str:
        """String representation (Arabic name)."""
        return self.name_ar

    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return f"Zahaf({self.name_ar}, {self.name_en})"

    def apply(self, tafila: Tafila) -> Tafila:
        """
        Apply this zahaf to a taf'ila.

        Args:
            tafila: Base taf'ila to transform

        Returns:
            New Tafila with transformation applied

        Raises:
            ValueError: If transformation fails
        """
        try:
            new_phonetic = self.transformation(tafila.phonetic)

            # Create new taf'ila name indicating the zahaf
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
        """Check if this zahaf can be applied to a specific meter."""
        if self.allowed_meters is None:
            return True  # No restrictions
        return meter_id in self.allowed_meters

    def can_apply_to_position(self, position: int) -> bool:
        """Check if this zahaf can be applied at a specific position."""
        if self.allowed_positions is None:
            return True  # No restrictions
        return position in self.allowed_positions

    def to_dict(self) -> dict:
        """Convert to dictionary representation."""
        return {
            "type": self.type.value,
            "name_ar": self.name_ar,
            "name_en": self.name_en,
            "description": self.description,
            "is_double": self.is_double,
            "frequency": self.frequency,
        }


# ============================================================================
# Transformation Functions
# ============================================================================


def remove_at_index(pattern: str, index: int) -> str:
    """Remove character at specific index."""
    if 0 <= index < len(pattern):
        return pattern[:index] + pattern[index + 1 :]
    return pattern


def khabn_transform(pattern: str) -> str:
    """خبن - Remove 2nd sakin (index 1 in 0-indexed)."""
    # Special case: فاعلن (/o//o) → فعِلن (///o) in letter-based notation
    # This matches classical prosody texts (especially for المتدارك)
    if pattern == "/o//o":
        return "///o"

    # General case: Find and remove 2nd sakin (o)
    sakin_count = 0
    for i, char in enumerate(pattern):
        if char == "o":
            sakin_count += 1
            if sakin_count == 2:
                return remove_at_index(pattern, i)
    return pattern


def tayy_transform(pattern: str) -> str:
    """طي - Remove 4th sakin."""
    sakin_count = 0
    for i, char in enumerate(pattern):
        if char == "o":
            sakin_count += 1
            if sakin_count == 4:
                return remove_at_index(pattern, i)
    return pattern


def qabd_transform(pattern: str) -> str:
    """
    قبض - Remove 5th sakin (DEPRECATED - use qabd_transform_letters).

    This function is kept for backwards compatibility but is fundamentally
    flawed as it operates on pattern strings instead of letter structures.

    For correct implementation, use qabd_transform_letters() with TafilaLetterStructure.
    """
    # For patterns like /o//o → /o//
    sakin_count = 0
    for i, char in enumerate(pattern):
        if char == "o":
            sakin_count += 1
            if sakin_count == 5:
                return remove_at_index(pattern, i)
    # If less than 5 sakins, remove last one
    last_o = pattern.rfind("o")
    if last_o != -1:
        return remove_at_index(pattern, last_o)
    return pattern


def qabd_transform_letters(tafila_structure):
    """
    قَبْض (Qabḍ) - Remove 2nd sākin/madd letter (letter-level implementation).

    Classical Definition:
    "القَبْض هو حذف الخامس الساكن"
    Translation: "Qabḍ is the removal of the 5th sākin"

    Classical Interpretation:
    In the 7-letter notation (م ف ا ع ي ل ن), position 5 (ي) is the 2nd sākin/madd.
    Therefore, QABD = "Remove the 2nd sākin/madd letter"

    Example:
        Input:  مَفَاعِيلُنْ (mafāʿīlun) = م(/) ف(/) ا(o) ع(/) ي(o) ل(/) ن(o)
                Classical positions: 1   2   3   4   5   6   7
                Sākin/madd positions: 3 (1st), 5 (2nd), 7 (3rd)

        Remove: Position 5 (ي) = 2nd sākin/madd
        Result: مَفَاعِلُنْ (mafāʿilun) = م(/) ف(/) ا(o) ع(/) ل(/) ن(o)
                Pattern: //o/o/o → //o//o ✓

    Note on Phoneme Representation:
        Our phoneme extraction combines consonant+long_vowel (e.g., فَا → فaa).
        This is linguistically correct but collapses the 7-letter structure to 5 phonemes.
        When counting sakins for transformations, we count these combined phonemes as single units.

    Args:
        tafila_structure: TafilaLetterStructure with letter-level representation

    Returns:
        New TafilaLetterStructure with 2nd sākin/madd removed

    Raises:
        ValueError: If tafʿīlah has fewer than 2 sākin/madd letters
    """
    from .letter_structure import TafilaLetterStructure

    # Get 2nd sākin/madd letter (includes both explicit sukūn and long vowels)
    sakin_result = tafila_structure.get_nth_sakin(2, include_madd=True)

    if sakin_result is None:
        # Fewer than 2 sakins/madds - qabd cannot apply
        # Return unchanged (not an error - just means this tafʿīlah doesn't support qabd)
        return tafila_structure

    position, letter = sakin_result

    # Remove this letter
    new_tafila = tafila_structure.remove_letter_at_position(position)

    # Note: We don't modify the name here as that's handled by the Zahaf.apply() method

    return new_tafila


def khabn_transform_letters(tafila_structure):
    """
    خَبْن (Khabn) - Remove 1st sākin/madd letter (letter-level implementation).

    Classical Definition:
    "الخَبْن هو حذف الساكن الثاني"
    Translation: "Khabn is the removal of the 2nd sākin"

    Classical Interpretation:
    In the 7-letter notation, this refers to the sākin at position 2,
    which is typically the 1st sākin in the sequence of sākin letters.
    Therefore, KHABN = "Remove the 1st sākin/madd letter"

    Example (from verification document):
        Input:  مُسْتَفْعِلُنْ (mustafʿilun) = م(/) س(o) ت(/) ف(o) ع(/) ل(/) ن(o)
                Sākin positions: س (1st), ف (2nd), ن (3rd)

        Remove: س (1st sākin, at letter position 2 in classical notation)
        Result: مُتَفْعِلُنْ (mutafʿilun) = م(/) ت(/) ف(o) ع(/) ل(/) ن(o)
                Pattern: /o/o//o → //o//o ✓

    Note on "2nd sākin" terminology:
        The classical Arabic "الساكن الثاني" literally means "the second sākin"
        but refers to the sākin at the 2nd position in the letter sequence,
        not the 2nd in the sequence of sākins. In most tafāʿīl, the first
        letter is mutaḥarrik, so position 2 contains the 1st sākin.

    Args:
        tafila_structure: TafilaLetterStructure with letter-level representation

    Returns:
        New TafilaLetterStructure with 1st sākin/madd removed

    Raises:
        ValueError: If tafʿīlah has no sākin/madd letters
    """
    from .letter_structure import TafilaLetterStructure

    # Get 1st sākin/madd letter (includes both explicit sukūn and long vowels)
    sakin_result = tafila_structure.get_nth_sakin(1, include_madd=True)

    if sakin_result is None:
        # No sakins/madds - khabn cannot apply
        # Return unchanged (not an error - just means this tafʿīlah doesn't support khabn)
        return tafila_structure

    position, letter = sakin_result

    # Remove this letter
    new_tafila = tafila_structure.remove_letter_at_position(position)

    # Note: We don't modify the name here as that's handled by the Zahaf.apply() method

    return new_tafila


def idmar_transform_letters(tafila_structure):
    """
    إِضْمَار (Iḍmār) - Make 2nd mutaḥarrik letter sākin (letter-level implementation).

    Classical Definition:
    "الإضمار هو تسكين الحرف الثاني المتحرك"
    Translation: "Iḍmār is making the 2nd mutaḥarrik letter sākin"

    Classical Interpretation:
    Unlike QABD and KHABN which REMOVE letters, IḌMĀR CHANGES a letter's ḥaraka.
    It takes a mutaḥarrik letter and adds sukūn to it, making it sākin.

    Example (from verification document):
        Input:  مُتَفَاعِلُنْ (mutafāʿilun) = م(/) ت(/) ف(/) ا(o) ع(/) ل(/) ن(o)
                Mutaḥarrik positions: م (1st), ت (2nd), ف (3rd), ع (4th), ل (5th)

        Change: ت (2nd mutaharrik) → add sukūn
        Result: مُتْفَاعِلُنْ (mutfāʿilun) = م(/) ت(o) ف(/) ا(o) ع(/) ل(/) ن(o)
                Pattern: ///o//o → /o/o//o ✓

    Note: This transformation is very common in الكامل meter.

    Args:
        tafila_structure: TafilaLetterStructure with letter-level representation

    Returns:
        New TafilaLetterStructure with 2nd mutaḥarrik made sākin

    Raises:
        ValueError: If tafʿīlah has fewer than 2 mutaḥarrik letters
    """
    from .letter_structure import TafilaLetterStructure, HarakaType, VowelQuality

    # Get 2nd mutaḥarrik letter
    mutaharrik_result = tafila_structure.get_nth_mutaharrik(2)

    if mutaharrik_result is None:
        # Fewer than 2 mutaharriks - idmar cannot apply
        # Return unchanged (not an error - just means this tafʿīlah doesn't support idmar)
        return tafila_structure

    position, letter = mutaharrik_result

    # Change this letter from mutaharrik to sakin
    new_tafila = tafila_structure.change_haraka_at_position(
        position,
        HarakaType.SAKIN,
        VowelQuality.SUKUN
    )

    # Note: We don't modify the name here as that's handled by the Zahaf.apply() method

    return new_tafila


def kaff_transform(pattern: str) -> str:
    """كف - Remove 7th sakin."""
    sakin_count = 0
    for i, char in enumerate(pattern):
        if char == "o":
            sakin_count += 1
            if sakin_count == 7:
                return remove_at_index(pattern, i)
    return pattern


def waqs_transform(pattern: str) -> str:
    """وقص - Remove 2nd mutaharrik (/)."""
    haraka_count = 0
    for i, char in enumerate(pattern):
        if char == "/":
            haraka_count += 1
            if haraka_count == 2:
                return remove_at_index(pattern, i)
    return pattern


def asb_transform(pattern: str) -> str:
    """عصب - Remove 5th mutaharrik."""
    haraka_count = 0
    for i, char in enumerate(pattern):
        if char == "/":
            haraka_count += 1
            if haraka_count == 5:
                return remove_at_index(pattern, i)
    return pattern


def idmar_transform(pattern: str) -> str:
    """إضمار - Make 2nd letter sakin (change 2nd / to o)."""
    # ///o//o → //o//o (2nd / becomes o)
    slash_count = 0
    for i, char in enumerate(pattern):
        if char == "/":
            slash_count += 1
            if slash_count == 2:
                return pattern[:i] + "o" + pattern[i + 1 :]
    return pattern


def khabl_transform(pattern: str) -> str:
    """خبل - Khabn + Tayy (double)."""
    result = khabn_transform(pattern)
    result = tayy_transform(result)
    return result


def khazl_transform(pattern: str) -> str:
    """خزل - Idmar + Tayy (double)."""
    result = idmar_transform(pattern)
    result = tayy_transform(result)
    return result


def shakl_transform(pattern: str) -> str:
    """شكل - Khabn + Kaff (double)."""
    result = khabn_transform(pattern)
    result = kaff_transform(result)
    return result


# ============================================================================
# Predefined Zihafat
# ============================================================================

# خبن - Most common zahaf across many meters
KHABN = Zahaf(
    type=ZahafType.KHABN,
    name_ar="خبن",
    name_en="khabn",
    description="Remove 2nd sakin letter",
    transformation=khabn_transform,
    is_double=False,
    allowed_meters={3, 5, 6, 7, 8, 9, 10, 11, 13, 16},  # البسيط, الرجز, الخفيف, etc.
    frequency="common",
)

# طي - Common in several meters
TAYY = Zahaf(
    type=ZahafType.TAYY,
    name_ar="طي",
    name_en="tayy",
    description="Remove 4th sakin letter",
    transformation=tayy_transform,
    is_double=False,
    allowed_meters={3, 5, 7, 8, 10, 12},  # البسيط, الرجز, الخفيف, السريع
    frequency="common",
)

# قبض - Common in الطويل, الهزج, المتقارب
QABD = Zahaf(
    type=ZahafType.QABD,
    name_ar="قبض",
    name_en="qabd",
    description="Remove 5th sakin letter (often last)",
    transformation=qabd_transform,
    is_double=False,
    allowed_meters={1, 6, 9, 12, 15},  # الطويل, الهزج, المتقارب
    frequency="common",
)

# كف - Less common
KAFF = Zahaf(
    type=ZahafType.KAFF,
    name_ar="كف",
    name_en="kaff",
    description="Remove 7th sakin letter",
    transformation=kaff_transform,
    is_double=False,
    allowed_meters={1, 4, 6, 9},  # الطويل, الرمل, الهزج, المديد
    frequency="rare",
)

# وقص - Rare
WAQS = Zahaf(
    type=ZahafType.WAQS,
    name_ar="وقص",
    name_en="waqs",
    description="Remove 2nd mutaharrik letter",
    transformation=waqs_transform,
    is_double=False,
    allowed_meters={2},  # الكامل
    frequency="rare",
)

# عصب - Used in الوافر
ASB = Zahaf(
    type=ZahafType.ASB,
    name_ar="عصب",
    name_en="'asb",
    description="Remove 5th mutaharrik letter",
    transformation=asb_transform,
    is_double=False,
    allowed_meters={4},  # الوافر
    frequency="common",
)

# إضمار - Very common in الكامل
IDMAR = Zahaf(
    type=ZahafType.IDMAR,
    name_ar="إضمار",
    name_en="idmar",
    description="Make 2nd letter sakin",
    transformation=idmar_transform,
    is_double=False,
    allowed_meters={2},  # الكامل
    frequency="very_common",
)

# خبل - Double zahaf (Khabn + Tayy)
KHABL = Zahaf(
    type=ZahafType.KHABL,
    name_ar="خبل",
    name_en="khabl",
    description="Khabn + Tayy (double)",
    transformation=khabl_transform,
    is_double=True,
    allowed_meters={3, 5, 7},  # البسيط, الرجز, الخفيف
    frequency="rare",
)

# خزل - Double zahaf (Idmar + Tayy)
KHAZL = Zahaf(
    type=ZahafType.KHAZL,
    name_ar="خزل",
    name_en="khazl",
    description="Idmar + Tayy (double)",
    transformation=khazl_transform,
    is_double=True,
    allowed_meters={2},  # الكامل
    frequency="very_rare",
)

# شكل - Double zahaf (Khabn + Kaff)
SHAKL = Zahaf(
    type=ZahafType.SHAKL,
    name_ar="شكل",
    name_en="shakl",
    description="Khabn + Kaff (double)",
    transformation=shakl_transform,
    is_double=True,
    allowed_meters={4, 6},  # الرمل, المديد
    frequency="very_rare",
)


# Registry of all predefined zihafat
ZIHAFAT_REGISTRY = {
    ZahafType.KHABN: KHABN,
    ZahafType.TAYY: TAYY,
    ZahafType.QABD: QABD,
    ZahafType.KAFF: KAFF,
    ZahafType.WAQS: WAQS,
    ZahafType.ASB: ASB,
    ZahafType.IDMAR: IDMAR,
    ZahafType.KHABL: KHABL,
    ZahafType.KHAZL: KHAZL,
    ZahafType.SHAKL: SHAKL,
}


def get_zahaf(zahaf_type: ZahafType) -> Optional[Zahaf]:
    """Get a zahaf by its type."""
    return ZIHAFAT_REGISTRY.get(zahaf_type)


def get_zihafat_for_meter(meter_id: int) -> List[Zahaf]:
    """
    Get all allowed zihafat for a specific meter.

    Args:
        meter_id: Meter ID (1-16)

    Returns:
        List of Zahaf objects allowed for this meter
    """
    return [
        zahaf
        for zahaf in ZIHAFAT_REGISTRY.values()
        if zahaf.can_apply_to_meter(meter_id)
    ]


def apply_zahaf(tafila: Tafila, zahaf: Zahaf) -> Tafila:
    """
    Apply a zahaf to a taf'ila.

    Args:
        tafila: Base taf'ila
        zahaf: Zahaf to apply

    Returns:
        New Tafila with transformation applied
    """
    return zahaf.apply(tafila)


def list_all_zihafat() -> List[Zahaf]:
    """Get list of all predefined zihafat."""
    return list(ZIHAFAT_REGISTRY.values())
