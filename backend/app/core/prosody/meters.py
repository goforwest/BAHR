"""
Meters (البحور) - Complete meter definitions with rules.

This module defines all 16 classical Arabic meters with their:
- Base tafa'il patterns
- Allowed zihafat per position
- Allowed 'ilal for final positions
- Pattern generation and validation logic
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Set, Optional, Tuple
from .tafila import Tafila, TAFAIL_BASE
from .zihafat import Zahaf, KHABN, TAYY, QABD, KAFF, ASB, IDMAR, KHABL, WAQS
from .ilal import Ilah, HADHF, QAT, QASR, BATR, KASHF


class MeterTier(Enum):
    """
    Meter classification by frequency and implementation priority.
    """
    TIER_1 = 1  # Common meters (85% of poetry)
    TIER_2 = 2  # Medium frequency (10% of poetry)
    TIER_3 = 3  # Rare meters (5% of poetry)


@dataclass
class MeterRules:
    """
    Rules for a specific taf'ila position in a meter.

    Attributes:
        allowed_zihafat: List of zihafat allowed at this position
        allowed_ilal: List of 'ilal allowed (for final position only)
        is_final: Whether this is the final position
    """
    allowed_zihafat: List[Zahaf] = field(default_factory=list)
    allowed_ilal: List[Ilah] = field(default_factory=list)
    is_final: bool = False


@dataclass
class Meter:
    """
    Represents a complete Arabic poetry meter (بحر).

    Attributes:
        id: Meter ID (1-16)
        name_ar: Arabic name (e.g., "الطويل")
        name_en: English name (e.g., "al-Tawil")
        tier: Implementation tier (1, 2, or 3)
        frequency_rank: Popularity ranking (1 = most common)
        base_tafail: List of base tafa'il (canonical pattern)
        rules_by_position: Dictionary mapping position → MeterRules
        description: Description of the meter
        example_verse: Example verse in this meter
    """

    id: int
    name_ar: str
    name_en: str
    tier: MeterTier
    frequency_rank: int
    base_tafail: List[Tafila]
    rules_by_position: Dict[int, MeterRules]
    description: Optional[str] = None
    example_verse: Optional[str] = None

    # Cached generated patterns
    _valid_patterns: Optional[Set[str]] = field(default=None, init=False, repr=False)

    def __str__(self) -> str:
        """String representation (Arabic name)."""
        return self.name_ar

    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return f"Meter({self.id}, {self.name_ar}, {self.name_en})"

    @property
    def base_pattern(self) -> str:
        """Get the base phonetic pattern (all tafa'il concatenated)."""
        return "".join(tafila.phonetic for tafila in self.base_tafail)

    @property
    def tafail_count(self) -> int:
        """Number of tafa'il in this meter."""
        return len(self.base_tafail)

    def get_tafila_at_position(self, position: int) -> Optional[Tafila]:
        """
        Get the base taf'ila at a specific position (1-indexed).

        Args:
            position: Position (1 to tafail_count)

        Returns:
            Tafila at that position or None
        """
        if 1 <= position <= len(self.base_tafail):
            return self.base_tafail[position - 1]
        return None

    def get_rules_at_position(self, position: int) -> Optional[MeterRules]:
        """
        Get rules for a specific position (1-indexed).

        Args:
            position: Position (1 to tafail_count)

        Returns:
            MeterRules for that position or None
        """
        return self.rules_by_position.get(position)

    def get_allowed_zihafat(self, position: int) -> List[Zahaf]:
        """Get allowed zihafat for a position."""
        rules = self.get_rules_at_position(position)
        return rules.allowed_zihafat if rules else []

    def get_allowed_ilal(self, position: int) -> List[Ilah]:
        """Get allowed 'ilal for final position."""
        rules = self.get_rules_at_position(position)
        return rules.allowed_ilal if rules else []

    def is_final_position(self, position: int) -> bool:
        """Check if a position is the final one."""
        return position == len(self.base_tafail)

    def generate_valid_patterns(self) -> Set[str]:
        """
        Generate all valid phonetic patterns for this meter.

        This applies all possible combinations of allowed zihafat and 'ilal
        according to the meter's rules.

        Returns:
            Set of all valid phonetic patterns
        """
        if self._valid_patterns is not None:
            return self._valid_patterns

        patterns = set()

        # Start with base pattern
        patterns.add(self.base_pattern)

        # Generate variations by applying zihafat and 'ilal
        # This is a simplified version - full implementation would use
        # combinatorial generation
        # TODO: Implement full pattern generation in pattern_generator.py

        self._valid_patterns = patterns
        return patterns

    def validate_pattern(self, pattern: str) -> Tuple[bool, float, List[str]]:
        """
        Validate if a phonetic pattern belongs to this meter.

        Args:
            pattern: Phonetic pattern to validate

        Returns:
            Tuple of (is_valid, confidence, applied_transformations)
        """
        # Exact match check
        if pattern == self.base_pattern:
            return True, 1.0, []

        # TODO: Implement full validation logic
        # - Segment pattern into tafa'il
        # - Check if each segment matches allowed variations
        # - Track which zihafat/ilal were applied
        # - Calculate confidence based on match quality

        return False, 0.0, []

    def to_dict(self) -> dict:
        """Convert to dictionary representation."""
        return {
            "id": self.id,
            "name_ar": self.name_ar,
            "name_en": self.name_en,
            "tier": self.tier.value,
            "frequency_rank": self.frequency_rank,
            "base_pattern": self.base_pattern,
            "tafail_count": self.tafail_count,
            "base_tafail": [t.name for t in self.base_tafail],
            "description": self.description,
        }


# ============================================================================
# Meter Definitions - Tier 1 (Common Meters)
# ============================================================================

# 1. الطويل (al-Tawil) - "The Long"
AL_TAWIL = Meter(
    id=1,
    name_ar="الطويل",
    name_en="al-Tawil",
    tier=MeterTier.TIER_1,
    frequency_rank=1,
    base_tafail=[
        TAFAIL_BASE["فعولن"],
        TAFAIL_BASE["مفاعيلن"],
        TAFAIL_BASE["فعولن"],
        TAFAIL_BASE["مفاعيلن"],
    ],
    rules_by_position={
        1: MeterRules(allowed_zihafat=[QABD, KAFF]),
        2: MeterRules(allowed_zihafat=[QABD, KAFF]),
        3: MeterRules(allowed_zihafat=[QABD, KAFF]),
        4: MeterRules(allowed_zihafat=[QABD, KAFF], allowed_ilal=[QASR, HADHF], is_final=True),
    },
    description="أشهر البحور وأكثرها استخداماً في الشعر العربي",
    example_verse="قِفَا نَبْكِ مِنْ ذِكْرَى حَبِيبٍ وَمَنْزِلِ"
)

# 2. الكامل (al-Kamil) - "The Perfect"
AL_KAMIL = Meter(
    id=2,
    name_ar="الكامل",
    name_en="al-Kamil",
    tier=MeterTier.TIER_1,
    frequency_rank=2,
    base_tafail=[
        TAFAIL_BASE["متفاعلن"],
        TAFAIL_BASE["متفاعلن"],
        TAFAIL_BASE["متفاعلن"],
        TAFAIL_BASE["متفاعلن"],
    ],
    rules_by_position={
        1: MeterRules(allowed_zihafat=[IDMAR, WAQS]),
        2: MeterRules(allowed_zihafat=[IDMAR, WAQS]),
        3: MeterRules(allowed_zihafat=[IDMAR, WAQS]),
        4: MeterRules(allowed_zihafat=[IDMAR, WAQS], allowed_ilal=[HADHF, QAT], is_final=True),
    },
    description="ثاني أشهر البحور، متوازن وسهل الحفظ",
    example_verse="بَدَا لِيَ أَنَّ الدَّهْرَ عِنْدِي لَحْظَةٌ"
)

# 3. البسيط (al-Basit) - "The Simple"
AL_BASIT = Meter(
    id=3,
    name_ar="البسيط",
    name_en="al-Basit",
    tier=MeterTier.TIER_1,
    frequency_rank=3,
    base_tafail=[
        TAFAIL_BASE["مستفعلن"],
        TAFAIL_BASE["فاعلن"],
        TAFAIL_BASE["مستفعلن"],
        TAFAIL_BASE["فاعلن"],
    ],
    rules_by_position={
        1: MeterRules(allowed_zihafat=[KHABN, TAYY, KHABL]),
        2: MeterRules(allowed_zihafat=[KHABN]),
        3: MeterRules(allowed_zihafat=[KHABN, TAYY, KHABL]),
        4: MeterRules(allowed_zihafat=[KHABN], allowed_ilal=[QAT], is_final=True),
    },
    description="بحر واسع الانتشار، يصلح للفخر والحماسة"
)

# 4. الوافر (al-Wafir) - "The Abundant"
AL_WAFIR = Meter(
    id=4,
    name_ar="الوافر",
    name_en="al-Wafir",
    tier=MeterTier.TIER_1,
    frequency_rank=4,
    base_tafail=[
        TAFAIL_BASE["مفاعلتن"],
        TAFAIL_BASE["مفاعلتن"],
        TAFAIL_BASE["فعولن"],
    ],
    rules_by_position={
        1: MeterRules(allowed_zihafat=[ASB]),
        2: MeterRules(allowed_zihafat=[ASB]),
        3: MeterRules(allowed_zihafat=[QABD], allowed_ilal=[QAT], is_final=True),
    },
    description="بحر موسيقي جميل، كثير الاستعمال في العصر الحديث"
)

# 5. الرجز (al-Rajaz) - "The Trembling"
AL_RAJAZ = Meter(
    id=5,
    name_ar="الرجز",
    name_en="al-Rajaz",
    tier=MeterTier.TIER_1,
    frequency_rank=5,
    base_tafail=[
        TAFAIL_BASE["مستفعلن"],
        TAFAIL_BASE["مستفعلن"],
        TAFAIL_BASE["مستفعلن"],
    ],
    rules_by_position={
        1: MeterRules(allowed_zihafat=[KHABN, TAYY, KHABL]),
        2: MeterRules(allowed_zihafat=[KHABN, TAYY, KHABL]),
        3: MeterRules(allowed_zihafat=[KHABN, TAYY, KHABL], allowed_ilal=[QAT, QASR], is_final=True),
    },
    description="بحر سهل بسيط، استخدم كثيراً في الأرجوزات التعليمية"
)

# 6. الرمل (ar-Ramal) - "The Sand"
AR_RAMAL = Meter(
    id=6,
    name_ar="الرمل",
    name_en="ar-Ramal",
    tier=MeterTier.TIER_1,
    frequency_rank=6,
    base_tafail=[
        TAFAIL_BASE["فاعلاتن"],
        TAFAIL_BASE["فاعلاتن"],
        TAFAIL_BASE["فاعلاتن"],
    ],
    rules_by_position={
        1: MeterRules(allowed_zihafat=[KHABN, KAFF]),
        2: MeterRules(allowed_zihafat=[KHABN, KAFF]),
        3: MeterRules(allowed_zihafat=[KHABN, KAFF], allowed_ilal=[HADHF], is_final=True),
    },
    description="بحر سلس رقيق، مناسب للغزل والرثاء"
)

# 7. الخفيف (al-Khafif) - "The Light"
AL_KHAFIF = Meter(
    id=7,
    name_ar="الخفيف",
    name_en="al-Khafif",
    tier=MeterTier.TIER_1,
    frequency_rank=7,
    base_tafail=[
        TAFAIL_BASE["فاعلاتن"],
        TAFAIL_BASE["مستفعلن"],
        TAFAIL_BASE["فاعلاتن"],
    ],
    rules_by_position={
        1: MeterRules(allowed_zihafat=[KHABN]),
        2: MeterRules(allowed_zihafat=[KHABN, TAYY]),
        3: MeterRules(allowed_zihafat=[KHABN], allowed_ilal=[HADHF], is_final=True),
    },
    description="بحر خفيف الوزن، مناسب للموشحات"
)

# 8. المتقارب (al-Mutaqarib) - "The Convergent"
AL_MUTAQARIB = Meter(
    id=11,
    name_ar="المتقارب",
    name_en="al-Mutaqarib",
    tier=MeterTier.TIER_1,
    frequency_rank=11,
    base_tafail=[
        TAFAIL_BASE["فعولن"],
        TAFAIL_BASE["فعولن"],
        TAFAIL_BASE["فعولن"],
        TAFAIL_BASE["فعولن"],
    ],
    rules_by_position={
        1: MeterRules(allowed_zihafat=[QABD]),
        2: MeterRules(allowed_zihafat=[QABD]),
        3: MeterRules(allowed_zihafat=[QABD]),
        4: MeterRules(allowed_zihafat=[QABD], allowed_ilal=[HADHF, QAT], is_final=True),
    },
    description="بحر متقارب التفعيلات، سهل الحفظ"
)

# 9. الهزج (al-Hazaj) - "The Rhythmic"
# Note: Supporting the 3-tafila تام version (complete form)
# The 2-tafila مجزوء version (shortened) will still match with truncated patterns
AL_HAZAJ = Meter(
    id=12,
    name_ar="الهزج",
    name_en="al-Hazaj",
    tier=MeterTier.TIER_1,
    frequency_rank=12,
    base_tafail=[
        TAFAIL_BASE["مفاعيلن"],
        TAFAIL_BASE["مفاعيلن"],
        TAFAIL_BASE["فعولن"],  # 3rd tafila for تام version
    ],
    rules_by_position={
        1: MeterRules(allowed_zihafat=[QABD, KAFF]),
        2: MeterRules(allowed_zihafat=[QABD, KAFF]),
        3: MeterRules(allowed_zihafat=[QABD], allowed_ilal=[HADHF], is_final=True),
    },
    description="بحر خفيف رشيق، يصلح للغناء (تام ومجزوء)"
)

# ============================================================================
# Meter Definitions - Tier 2 (Medium Frequency Meters)
# ============================================================================

# 10. السريع (as-Sari') - "The Fast"
AS_SARI = Meter(
    id=8,
    name_ar="السريع",
    name_en="as-Sari'",
    tier=MeterTier.TIER_2,
    frequency_rank=8,
    base_tafail=[
        TAFAIL_BASE["مستفعلن"],
        TAFAIL_BASE["مستفعلن"],
        TAFAIL_BASE["فاعلن"],
    ],
    rules_by_position={
        1: MeterRules(allowed_zihafat=[KHABN, TAYY, KHABL]),
        2: MeterRules(allowed_zihafat=[KHABN, TAYY, KHABL]),
        3: MeterRules(allowed_zihafat=[KHABN], allowed_ilal=[KASHF, QASR], is_final=True),
    },
    description="بحر سريع الإيقاع، مناسب للحماسة والحكمة",
    example_verse="يا دَهْرُ وَيْحَكَ ما أَبْقَيْتَ مِنْ أَحَدِ"
)

# 10b. السريع (مفعولات variant) - "The Fast (maf'ulat ending)"
AS_SARI_MAFOOLAT = Meter(
    id=20,
    name_ar="السريع (مفعولات)",
    name_en="as-Sari' (maf'ulat)",
    tier=MeterTier.TIER_2,
    frequency_rank=20,
    base_tafail=[
        TAFAIL_BASE["مستفعلن"],
        TAFAIL_BASE["مستفعلن"],
        TAFAIL_BASE["مفعولات"],
    ],
    rules_by_position={
        1: MeterRules(allowed_zihafat=[KHABN, TAYY, KHABL]),
        2: MeterRules(allowed_zihafat=[KHABN, TAYY, KHABL]),
        3: MeterRules(allowed_zihafat=[KHABN], allowed_ilal=[HADHF], is_final=True),
    },
    description="نسخة السريع المنتهية بمفعولات بدلاً من فاعلن",
    example_verse="لا تَعذُليهِ فَإِنَّ العَذلَ يولَعُهُ"
)

# 11. المديد (al-Madid) - "The Extended"
AL_MADID = Meter(
    id=9,
    name_ar="المديد",
    name_en="al-Madid",
    tier=MeterTier.TIER_2,
    frequency_rank=9,
    base_tafail=[
        TAFAIL_BASE["فاعلاتن"],
        TAFAIL_BASE["فاعلن"],
        TAFAIL_BASE["فاعلاتن"],
    ],
    rules_by_position={
        1: MeterRules(allowed_zihafat=[KHABN, KAFF]),
        2: MeterRules(allowed_zihafat=[KHABN]),
        3: MeterRules(allowed_zihafat=[KHABN], allowed_ilal=[HADHF, QASR], is_final=True),
    },
    description="بحر رقيق عذب، مناسب للغزل والوصف"
)


# ============================================================================
# Meter Definitions - Tier 3 (Rare Meters)
# ============================================================================

# 12. المنسرح (al-Munsarih) - "The Flowing"
AL_MUNSARIH = Meter(
    id=10,
    name_ar="المنسرح",
    name_en="al-Munsarih",
    tier=MeterTier.TIER_3,
    frequency_rank=10,
    base_tafail=[
        TAFAIL_BASE["مستفعلن"],
        TAFAIL_BASE["مفعولات"],
        TAFAIL_BASE["مفتعلن"],
    ],
    rules_by_position={
        1: MeterRules(allowed_zihafat=[KHABN, TAYY]),
        2: MeterRules(allowed_zihafat=[TAYY]),
        3: MeterRules(allowed_zihafat=[], allowed_ilal=[KASHF], is_final=True),
    },
    description="بحر منساح السياق، قليل الاستعمال"
)

# 13. المجتث (al-Mujtathth) - "The Uprooted"
AL_MUJTATHTH = Meter(
    id=13,
    name_ar="المجتث",
    name_en="al-Mujtathth",
    tier=MeterTier.TIER_3,
    frequency_rank=13,
    base_tafail=[
        TAFAIL_BASE["مستفعلن"],
        TAFAIL_BASE["فاعلاتن"],
    ],
    rules_by_position={
        1: MeterRules(allowed_zihafat=[KHABN]),
        2: MeterRules(allowed_zihafat=[KHABN], allowed_ilal=[HADHF], is_final=True),
    },
    description='بحر نادر، "مجتث" من البسيط'
)

# 14. المقتضب (al-Muqtadab) - "The Condensed"
AL_MUQTADAB = Meter(
    id=14,
    name_ar="المقتضب",
    name_en="al-Muqtadab",
    tier=MeterTier.TIER_3,
    frequency_rank=14,
    base_tafail=[
        TAFAIL_BASE["مفعولات"],
        TAFAIL_BASE["مستفعلن"],
    ],
    rules_by_position={
        1: MeterRules(allowed_zihafat=[TAYY]),
        2: MeterRules(allowed_zihafat=[KHABN], allowed_ilal=[QAT], is_final=True),
    },
    description="بحر قليل الاستخدام، مقتضب من المنسرح"
)

# 15. المضارع (al-Mudari') - "The Resembling"
AL_MUDARI = Meter(
    id=15,
    name_ar="المضارع",
    name_en="al-Mudari'",
    tier=MeterTier.TIER_3,
    frequency_rank=15,
    base_tafail=[
        TAFAIL_BASE["مفاعيلن"],
        TAFAIL_BASE["فاعلاتن"],
    ],
    rules_by_position={
        1: MeterRules(allowed_zihafat=[QABD]),
        2: MeterRules(allowed_zihafat=[KHABN], allowed_ilal=[HADHF], is_final=True),
    },
    description="بحر نادر الاستعمال، يضارع الهزج في الإيقاع"
)

# 16. المتدارك (al-Mutadarik) - "The Overtaking"
AL_MUTADARIK = Meter(
    id=16,
    name_ar="المتدارك",
    name_en="al-Mutadarik",
    tier=MeterTier.TIER_3,
    frequency_rank=16,
    base_tafail=[
        TAFAIL_BASE["فاعلن"],
        TAFAIL_BASE["فاعلن"],
        TAFAIL_BASE["فاعلن"],
        TAFAIL_BASE["فاعلن"],
    ],
    rules_by_position={
        1: MeterRules(allowed_zihafat=[KHABN]),
        2: MeterRules(allowed_zihafat=[KHABN]),
        3: MeterRules(allowed_zihafat=[KHABN]),
        4: MeterRules(allowed_zihafat=[KHABN], allowed_ilal=[HADHF, QASR], is_final=True),
    },
    description='البحر السادس عشر، "استدركه الأخفش على الخليل"'
)

# ============================================================================
# مجزوء (Majzū') Variants - Shortened Meter Forms
# ============================================================================
# These are standard shortened forms of meters with fewer tafāʿīl than the
# complete (تام) forms. They are widely used in classical and modern poetry.

# 17. مجزوء الكامل (Majzū' al-Kamil) - "Shortened Perfect"
MAJZU_AL_KAMIL = Meter(
    id=17,
    name_ar="الكامل (مجزوء)",
    name_en="al-Kamil (majzū')",
    tier=MeterTier.TIER_1,  # Very common variant
    frequency_rank=17,
    base_tafail=[
        TAFAIL_BASE["متفاعلن"],
        TAFAIL_BASE["متفاعلن"],
    ],
    rules_by_position={
        1: MeterRules(allowed_zihafat=[IDMAR]),
        2: MeterRules(allowed_zihafat=[IDMAR], allowed_ilal=[HADHF, QAT], is_final=True),
    },
    description="النسخة المجزوءة من بحر الكامل (تفعيلتان بدلاً من أربع)"
)

# 18. مجزوء الهزج (Majzū' al-Hazaj) - "Shortened Trilling"
MAJZU_AL_HAZAJ = Meter(
    id=18,
    name_ar="الهزج (مجزوء)",
    name_en="al-Hazaj (majzū')",
    tier=MeterTier.TIER_1,  # Common variant
    frequency_rank=18,
    base_tafail=[
        TAFAIL_BASE["مفاعيلن"],
        TAFAIL_BASE["مفاعيلن"],
    ],
    rules_by_position={
        1: MeterRules(allowed_zihafat=[QABD, KAFF]),
        2: MeterRules(allowed_zihafat=[QABD, KAFF], allowed_ilal=[HADHF], is_final=True),
    },
    description="النسخة المجزوءة من بحر الهزج (تفعيلتان بدلاً من ثلاث)"
)

# 19. الكامل (3 تفاعيل) - Medium length variant
AL_KAMIL_3 = Meter(
    id=19,
    name_ar="الكامل (3 تفاعيل)",
    name_en="al-Kamil (3 tafail)",
    tier=MeterTier.TIER_1,
    frequency_rank=19,
    base_tafail=[
        TAFAIL_BASE["متفاعلن"],
        TAFAIL_BASE["متفاعلن"],
        TAFAIL_BASE["متفاعلن"],
    ],
    rules_by_position={
        1: MeterRules(allowed_zihafat=[IDMAR, WAQS]),
        2: MeterRules(allowed_zihafat=[IDMAR, WAQS]),
        3: MeterRules(allowed_zihafat=[IDMAR, WAQS], allowed_ilal=[HADHF, QAT], is_final=True),
    },
    description="نسخة الكامل بثلاث تفاعيل (متوسطة)"
)


# ============================================================================
# Meters Registry - All Classical Arabic Meters (16 Base + مجزوء Variants)
# ============================================================================

METERS_REGISTRY: Dict[int, Meter] = {
    # Tier 1: Common Meters (9)
    1: AL_TAWIL,
    2: AL_KAMIL,
    3: AL_BASIT,
    4: AL_WAFIR,
    5: AL_RAJAZ,
    6: AR_RAMAL,
    7: AL_KHAFIF,
    11: AL_MUTAQARIB,
    12: AL_HAZAJ,

    # Tier 2: Medium Frequency (2)
    8: AS_SARI,
    9: AL_MADID,

    # Tier 3: Rare Meters (5)
    10: AL_MUNSARIH,
    13: AL_MUJTATHTH,
    14: AL_MUQTADAB,
    15: AL_MUDARI,
    16: AL_MUTADARIK,

    # مجزوء (Majzū') Variants - Shortened Forms
    17: MAJZU_AL_KAMIL,
    18: MAJZU_AL_HAZAJ,
    19: AL_KAMIL_3,
    20: AS_SARI_MAFOOLAT,
}


def get_meter(meter_id: int) -> Optional[Meter]:
    """
    Get a meter by its ID.

    Args:
        meter_id: Meter ID (1-16)

    Returns:
        Meter object or None if not found
    """
    return METERS_REGISTRY.get(meter_id)


def get_meter_by_name(name_ar: str) -> Optional[Meter]:
    """
    Get a meter by its Arabic name.

    Args:
        name_ar: Arabic name (e.g., "الطويل")

    Returns:
        Meter object or None if not found
    """
    for meter in METERS_REGISTRY.values():
        if meter.name_ar == name_ar:
            return meter
    return None


def list_all_meters() -> List[Meter]:
    """Get list of all defined meters."""
    return list(METERS_REGISTRY.values())


def list_meters_by_tier(tier: MeterTier) -> List[Meter]:
    """Get list of meters in a specific tier."""
    return [m for m in METERS_REGISTRY.values() if m.tier == tier]


def load_meters() -> Dict[int, Meter]:
    """
    Load all meters into memory.

    This function can be extended to load from database or config file.

    Returns:
        Dictionary mapping meter ID to Meter object
    """
    return METERS_REGISTRY.copy()
