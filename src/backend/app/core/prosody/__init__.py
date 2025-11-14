"""
Prosody module for BAHR v2.0 - Rule-based meter detection.

This module implements classical Arabic prosody rules (Zihafat and 'Ilal)
for accurate meter detection across all 16 classical Arabic meters.

Key components:
- Tafila: Prosodic feet (تفعيلة)
- Zahaf: Prosodic variations (زحاف)
- Ilah: End-of-verse variations (علة)
- Meter: Complete meter definition with rules (بحر)
"""

from .ilal import Ilah, IlahType, apply_ilah
from .meters import METERS_REGISTRY, Meter, MeterTier, load_meters
from .tafila import Tafila, TafilaStructure
from .zihafat import Zahaf, ZahafType, apply_zahaf

__all__ = [
    # Tafila
    "Tafila",
    "TafilaStructure",
    # Zahaf
    "Zahaf",
    "ZahafType",
    "apply_zahaf",
    # Ilah
    "Ilah",
    "IlahType",
    "apply_ilah",
    # Meter
    "Meter",
    "MeterTier",
    "load_meters",
    "METERS_REGISTRY",
]

__version__ = "2.0.0"
__author__ = "BAHR Development Team"
