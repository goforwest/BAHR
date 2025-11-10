"""Arabic text normalization utilities for prosody analysis.

IMPLEMENTATION SCOPE (Week 1-2 MVP):
This is a simplified 4-stage normalization pipeline for initial development.
The full 8-stage pipeline documented in feature-arabic-text-normalization.md
will be implemented in Week 3-4.

Current stages:
1. Strip diacritics (if enabled)
2. Character mapping (Alif variants, ta marbuta)
3. Punctuation removal
4. Whitespace normalization

TODO (Week 3-4): Implement full 8-stage pipeline
- Stage 1: Unicode normalization (NFD → NFC)
- Stage 2: Tatweel removal
- Stage 5: Hamza normalization
- Stage 6: Yaa forms normalization
- Stage 7: Non-Arabic character filtering (with Arabic % validation)
- See: docs/implementation-guides/feature-arabic-text-normalization.md

"""
import re

DIACRITICS_PATTERN = re.compile(r"[\u0610-\u061A\u064B-\u065F\u0670\u06D6-\u06ED]")

ALIF_VARIANTS = {
    "أ": "ا",
    "إ": "ا",
    "آ": "ا",
}

CHAR_MAP = {
    **ALIF_VARIANTS,
    "ة": "ه",  # treat ta marbuta as ha for stable patterning
}

PUNCT_CHARS = "،؛؟!?()[]{}\"'«»…:؛.,-"
PUNCT_PATTERN = re.compile("[" + re.escape(PUNCT_CHARS) + "]")


class ArabicNormalizer:
    """
    Simplified Arabic text normalizer (MVP version).
    
    This is a 4-stage pipeline for Week 1-2 development.
    Full 8-stage pipeline to be implemented in Week 3-4.
    """
    
    def __init__(self, remove_diacritics: bool = True) -> None:
        self.remove_diacritics = remove_diacritics

    def normalize(self, text: str) -> str:
        """
        Normalize Arabic text through 4-stage pipeline (MVP).
        
        Args:
            text: Input Arabic text
            
        Returns:
            Normalized text string
            
        TODO (Week 3): Return NormalizationResult dataclass with:
            - original
            - normalized
            - stages dict (intermediate results)
            - is_valid (Arabic % >= 70%)
            - arabic_percentage
        """
        t = text
        
        # Stage 1: Strip diacritics (if enabled)
        if self.remove_diacritics:
            t = self._strip_diacritics(t)
        
        # Stage 2: Character mapping (unify chars)
        for old, new in CHAR_MAP.items():
            t = t.replace(old, new)
        
        # Stage 3: Punctuation removal
        t = PUNCT_PATTERN.sub(" ", t)
        
        # Stage 4: Whitespace normalization
        t = re.sub(r"\s+", " ", t).strip()
        
        # TODO (Week 3): Add Arabic percentage validation
        # if arabic_percentage < 0.7:
        #     raise ValidationError("ERR_INPUT_001")
        
        return t

    def _strip_diacritics(self, text: str) -> str:
        """Remove Arabic diacritics (tashkeel)"""
        return DIACRITICS_PATTERN.sub("", text)


def basic_normalize(text: str, remove_diacritics: bool = True) -> str:
    """
    Convenience function for basic normalization.
    
    Args:
        text: Input Arabic text
        remove_diacritics: Whether to remove diacritics
        
    Returns:
        Normalized text string
    """
    return ArabicNormalizer(remove_diacritics=remove_diacritics).normalize(text)

