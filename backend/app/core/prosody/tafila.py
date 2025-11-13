"""
Tafila (تفعيلة) - Prosodic foot representation.

A taf'ila is the basic rhythmic unit in Arabic poetry prosody.
Each taf'ila has a specific phonetic pattern and prosodic structure.
"""

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, TYPE_CHECKING

# Use TYPE_CHECKING to avoid circular imports at runtime
if TYPE_CHECKING:
    from .letter_structure import TafilaLetterStructure


class TafilaStructure(Enum):
    """
    Prosodic structure types for tafa'il.

    Based on classical Arabic prosody:
    - SABAB: Two-letter unit (سبب)
    - WATAD: Three-letter unit (وتد)
    """

    SABAB_KHAFIF = "sabab_khafif"  # ب خ - Two letters: mut., sakin (e.g., "فَعْ")
    SABAB_THAQIL = "sabab_thaqil"  # ب ث - Two letters: mut., mut. (e.g., "فَعَ")
    WATAD_MAJMU = "watad_majmu"  # و م - Three letters: mut., mut., sakin (e.g., "فَعُولْ")
    WATAD_MAFRUQ = (
        "watad_mafruq"  # و ف - Three letters: mut., sakin, mut. (e.g., "فَاعِ")
    )
    FASILA = "fasila"  # فاصلة - Four or five letters
    COMPLEX = "complex"  # Mixed structure


@dataclass(frozen=True)
class Tafila:
    """
    Represents a prosodic foot (تفعيلة).

    Attributes:
        name: Arabic name (e.g., "فعولن")
        phonetic: Phonetic pattern using '/' (haraka) and 'o' (sakin)
        structure: Prosodic structure description
        syllable_count: Number of syllables
        components: List of prosodic components (sabab, watad)
        letter_structure: Letter-level representation (NEW in Phase 2)

    Examples:
        >>> fa_u_lun = Tafila("فعولن", "/o/o", "sabab+watad", 3)
        >>> print(fa_u_lun.name)
        فعولن
        >>> print(fa_u_lun.phonetic)
        /o/o
    """

    name: str  # Arabic name (e.g., "فعولن")
    phonetic: str  # Phonetic pattern (e.g., "/o/o")
    structure: str  # Description (e.g., "sabab+watad")
    syllable_count: int  # Number of syllables
    components: Optional[List[TafilaStructure]] = None  # Prosodic components

    # NEW: Letter-level representation for Phase 2 transformations
    letter_structure: Optional["TafilaLetterStructure"] = None

    def __post_init__(self):
        """Validate taf'ila data."""
        if not self.name:
            raise ValueError("Tafila name cannot be empty")
        if not self.phonetic:
            raise ValueError("Tafila phonetic pattern cannot be empty")
        if self.syllable_count < 1:
            raise ValueError("Tafila must have at least 1 syllable")

        # Validate phonetic pattern contains only '/' and 'o'
        if not all(c in "/o" for c in self.phonetic):
            raise ValueError(
                f"Invalid phonetic pattern: {self.phonetic}. Must contain only '/' and 'o'"
            )

    def __str__(self) -> str:
        """String representation (Arabic name)."""
        return self.name

    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return f"Tafila('{self.name}', '{self.phonetic}')"

    def __len__(self) -> int:
        """Length of phonetic pattern."""
        return len(self.phonetic)

    def __eq__(self, other) -> bool:
        """Equality based on phonetic pattern."""
        if not isinstance(other, Tafila):
            return False
        return self.phonetic == other.phonetic

    def __hash__(self) -> int:
        """Hash based on phonetic pattern."""
        return hash(self.phonetic)

    @property
    def pattern_length(self) -> int:
        """Length of the phonetic pattern."""
        return len(self.phonetic)

    @property
    def harakat_count(self) -> int:
        """Count of harakat (/) in pattern."""
        return self.phonetic.count("/")

    @property
    def sukunat_count(self) -> int:
        """Count of sukunat (o) in pattern."""
        return self.phonetic.count("o")

    def matches_pattern(self, pattern: str) -> bool:
        """
        Check if a phonetic pattern matches this taf'ila.

        Args:
            pattern: Phonetic pattern to check

        Returns:
            True if pattern matches exactly
        """
        return self.phonetic == pattern

    def similarity(self, pattern: str) -> float:
        """
        Calculate similarity to a phonetic pattern.

        Args:
            pattern: Phonetic pattern to compare

        Returns:
            Similarity score (0.0 to 1.0)
        """
        if not pattern:
            return 0.0

        max_len = max(len(self.phonetic), len(pattern))
        if max_len == 0:
            return 1.0

        matches = sum(
            1
            for i in range(min(len(self.phonetic), len(pattern)))
            if self.phonetic[i] == pattern[i]
        )

        return matches / max_len

    def to_dict(self) -> dict:
        """
        Convert to dictionary representation.

        Returns:
            Dictionary with taf'ila data
        """
        return {
            "name": self.name,
            "phonetic": self.phonetic,
            "structure": self.structure,
            "syllable_count": self.syllable_count,
            "pattern_length": self.pattern_length,
            "harakat_count": self.harakat_count,
            "sukunat_count": self.sukunat_count,
        }


# ============================================================================
# Helper function to create letter structures
# ============================================================================

def _create_letter_structure(name: str, vocalized_text: str):
    """
    Helper to create letter structure, imported dynamically to avoid circular imports.

    Args:
        name: Tafila name
        vocalized_text: Vocalized Arabic text

    Returns:
        TafilaLetterStructure or None if parsing fails
    """
    try:
        from .letter_structure import parse_tafila_from_text
        return parse_tafila_from_text(name, vocalized_text)
    except Exception:
        # If letter structure parsing fails, return None
        # This allows the system to work even if letter_structure module has issues
        return None


# ============================================================================
# Common Tafa'il - Base Forms (Most Frequent)
# ============================================================================

# These are the 8 most common base tafa'il across all 16 meters
TAFAIL_BASE = {
    # Used in: الطويل, المتقارب, الوافر, الهزج
    "فعولن": Tafila(
        name="فعولن",
        phonetic="/o/o",  # Updated: actual pattern from phoneme extraction
        structure="sabab+watad",
        syllable_count=3,
        components=[TafilaStructure.SABAB_KHAFIF, TafilaStructure.WATAD_MAJMU],
        letter_structure=_create_letter_structure("فعولن", "فَعُولُنْ"),
    ),
    # Used in: الطويل, الهزج, المضارع
    "مفاعيلن": Tafila(
        name="مفاعيلن",
        phonetic="//o/o/o",
        structure="sabab+sabab+watad",
        syllable_count=4,
        components=[
            TafilaStructure.SABAB_THAQIL,
            TafilaStructure.SABAB_KHAFIF,
            TafilaStructure.WATAD_MAJMU,
        ],
        letter_structure=_create_letter_structure("مفاعيلن", "مَفَاعِيلُنْ"),
    ),
    # Used in: المديد, البسيط, السريع, المتدارك
    "فاعلن": Tafila(
        name="فاعلن",
        phonetic="/o//o",
        structure="watad+sabab",
        syllable_count=3,
        components=[TafilaStructure.WATAD_MAFRUQ, TafilaStructure.SABAB_KHAFIF],
        letter_structure=_create_letter_structure("فاعلن", "فَاعِلُنْ"),
    ),
    # Used in: الكامل
    "متفاعلن": Tafila(
        name="متفاعلن",
        phonetic="///o//o",
        structure="sabab+sabab+watad",
        syllable_count=4,
        components=[
            TafilaStructure.SABAB_THAQIL,
            TafilaStructure.SABAB_THAQIL,
            TafilaStructure.WATAD_MAJMU,
        ],
        letter_structure=_create_letter_structure("متفاعلن", "مُتَفَاعِلُنْ"),
    ),
    # Used in: الرجز, البسيط, السريع, المنسرح, الخفيف, المجتث
    "مستفعلن": Tafila(
        name="مستفعلن",
        phonetic="/o/o//o",
        structure="sabab+sabab+watad",
        syllable_count=4,
        components=[
            TafilaStructure.SABAB_KHAFIF,
            TafilaStructure.SABAB_THAQIL,
            TafilaStructure.WATAD_MAJMU,
        ],
        letter_structure=_create_letter_structure("مستفعلن", "مُسْتَفْعِلُنْ"),
    ),
    # Used in: المنسرح, المقتضب
    "مفعولات": Tafila(
        name="مفعولات",
        phonetic="/o/o/o/",
        structure="watad_mafruq+sabab+sabab",
        syllable_count=4,
        components=[
            TafilaStructure.WATAD_MAFRUQ,
            TafilaStructure.SABAB_KHAFIF,
            TafilaStructure.SABAB_THAQIL,
        ],
        letter_structure=_create_letter_structure("مفعولات", "مَفْعُولَاتُ"),
    ),
    # Used in: الرمل, المديد, الخفيف, المجتث, المضارع
    "فاعلاتن": Tafila(
        name="فاعلاتن",
        phonetic="/o//o/o",
        structure="watad+sabab+sabab",
        syllable_count=4,
        components=[
            TafilaStructure.WATAD_MAFRUQ,
            TafilaStructure.SABAB_KHAFIF,
            TafilaStructure.SABAB_KHAFIF,
        ],
        letter_structure=_create_letter_structure("فاعلاتن", "فَاعِلَاتُنْ"),
    ),
    # Used in: الوافر
    "مفاعلتن": Tafila(
        name="مفاعلتن",
        phonetic="//o///o",
        structure="sabab+sabab+sabab+watad",
        syllable_count=4,
        components=[
            TafilaStructure.SABAB_THAQIL,
            TafilaStructure.SABAB_KHAFIF,
            TafilaStructure.SABAB_THAQIL,
            TafilaStructure.WATAD_MAJMU,
        ],
        letter_structure=_create_letter_structure("مفاعلتن", "مُفَاعَلَتُنْ"),
    ),
    # Used in: المنسرح (rare)
    "مفتعلن": Tafila(
        name="مفتعلن",
        phonetic="/o/o//o",
        structure="sabab+sabab+watad",
        syllable_count=4,
        components=[
            TafilaStructure.SABAB_KHAFIF,
            TafilaStructure.SABAB_THAQIL,
            TafilaStructure.WATAD_MAJMU,
        ],
        letter_structure=_create_letter_structure("مفتعلن", "مُفْتَعِلُنْ"),
    ),
    # ============================================================================
    # Commonly Used Modified Forms (from Zihafat/Ilal)
    # ============================================================================
    # فعلن - Modified form of فاعلن (with حذف - removing last sabab)
    # Used in final position in many meters
    "فعلن": Tafila(
        name="فعلن",
        phonetic="//o",
        structure="sabab+watad_modified",
        syllable_count=2,
        components=[TafilaStructure.SABAB_THAQIL, TafilaStructure.WATAD_MAJMU],
        letter_structure=_create_letter_structure("فعلن", "فَعُلُنْ"),
    ),
    # فعِلن - Alternative notation: Modified form of فاعلن (with خبن)
    # Letter-based notation used in classical prosody texts (especially المتدارك)
    # Represents: فَ (/) + عِ (/) + لُ (/) + نْ (o) = ///o
    "فعِلن": Tafila(
        name="فعِلن",
        phonetic="///o",
        structure="three_mutaharrik+sakin",
        syllable_count=4,
        components=[TafilaStructure.SABAB_THAQIL, TafilaStructure.SABAB_THAQIL],
        letter_structure=_create_letter_structure("فعِلن", "فَعِلُنْ"),
    ),
    # مفاعلن - Modified form of مفاعيلن (with قبض - removing 5th sakin)
    # Very common in الطويل final position
    "مفاعلن": Tafila(
        name="مفاعلن",
        phonetic="//o//o",
        structure="sabab+sabab+watad_modified",
        syllable_count=3,
        components=[
            TafilaStructure.SABAB_THAQIL,
            TafilaStructure.SABAB_THAQIL,
            TafilaStructure.WATAD_MAJMU,
        ],
        letter_structure=_create_letter_structure("مفاعلن", "مَفَاعِلُنْ"),
    ),
    # فاعلان - Modified form of فاعلاتن (with حذف)
    # Used in الرمل
    "فاعلان": Tafila(
        name="فاعلان",
        phonetic="/o//o",
        structure="watad+sabab_modified",
        syllable_count=3,
        components=[TafilaStructure.WATAD_MAFRUQ, TafilaStructure.SABAB_KHAFIF],
        letter_structure=_create_letter_structure("فاعلان", "فَاعِلَانْ"),
    ),
}


def get_tafila(name: str) -> Optional[Tafila]:
    """
    Get a taf'ila by its Arabic name.

    Args:
        name: Arabic name of taf'ila (e.g., "فعولن")

    Returns:
        Tafila object or None if not found
    """
    return TAFAIL_BASE.get(name)


def get_tafila_by_pattern(pattern: str) -> Optional[Tafila]:
    """
    Get a taf'ila by its phonetic pattern.

    Args:
        pattern: Phonetic pattern (e.g., "/o//o")

    Returns:
        Tafila object or None if not found
    """
    for tafila in TAFAIL_BASE.values():
        if tafila.phonetic == pattern:
            return tafila
    return None


def list_all_tafail() -> List[Tafila]:
    """
    Get list of all base tafa'il.

    Returns:
        List of all Tafila objects
    """
    return list(TAFAIL_BASE.values())
