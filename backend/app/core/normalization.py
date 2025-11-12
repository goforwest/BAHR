"""
Arabic text normalization for prosodic analysis.
"""

import re
import unicodedata
from typing import Optional

# Unicode ranges for Arabic
ARABIC_DIACRITICS = [
    "\u064b",  # Tanween Fath
    "\u064c",  # Tanween Damm
    "\u064d",  # Tanween Kasr
    "\u064e",  # Fatha
    "\u064f",  # Damma
    "\u0650",  # Kasra
    "\u0651",  # Shadda
    "\u0652",  # Sukun
    "\u0653",  # Maddah
    "\u0654",  # Hamza above
    "\u0655",  # Hamza below
    "\u0656",  # Subscript Alef
    "\u0657",  # Inverted Damma
    "\u0658",  # Mark Noon Ghunna
]


def remove_diacritics(text: str) -> str:
    """
    Remove all Arabic diacritical marks (tashkeel).

    Args:
        text: Arabic text with diacritics

    Returns:
        Text without diacritics

    Example:
        >>> remove_diacritics("مَرْحَبًا")
        "مرحبا"
    """
    for diacritic in ARABIC_DIACRITICS:
        text = text.replace(diacritic, "")
    return text


def normalize_hamza(text: str) -> str:
    """
    Normalize all hamza variants to base form.

    Converts: أ، إ، آ، ء، ؤ، ئ → ا or ء

    Args:
        text: Arabic text with hamza variants

    Returns:
        Text with normalized hamza

    Example:
        >>> normalize_hamza("أحمد")
        "احمد"
        >>> normalize_hamza("ؤمن")
        "ومن"
    """
    # Hamza on alef variants → alef
    text = text.replace("أ", "ا")
    text = text.replace("إ", "ا")
    text = text.replace("آ", "ا")

    # Hamza on waw → waw
    text = text.replace("ؤ", "و")

    # Hamza on ya → ya
    text = text.replace("ئ", "ي")

    return text


def normalize_alef(text: str) -> str:
    """
    Normalize alef variants.

    Converts: ى، أ، إ، آ → ا

    Args:
        text: Arabic text with alef variants

    Returns:
        Text with normalized alef

    Example:
        >>> normalize_alef("على")
        "علي"
        >>> normalize_alef("موسى")
        "موسي"
    """
    text = text.replace("ى", "ي")  # Alef maksura → ya
    text = text.replace("أ", "ا")
    text = text.replace("إ", "ا")
    text = text.replace("آ", "ا")

    return text


def remove_tatweel(text: str) -> str:
    """
    Remove Arabic tatweel (kashida) character.

    Args:
        text: Arabic text possibly containing tatweel

    Returns:
        Text without tatweel

    Example:
        >>> remove_tatweel("مـــرحبا")
        "مرحبا"
    """
    return text.replace("\u0640", "")


def normalize_whitespace(text: str) -> str:
    """
    Normalize whitespace to single spaces.

    Args:
        text: Text with irregular whitespace

    Returns:
        Text with normalized whitespace

    Example:
        >>> normalize_whitespace("  مرحبا   بك  ")
        "مرحبا بك"
    """
    # Replace multiple spaces/tabs/newlines with single space
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def normalize_arabic_text(
    text: str,
    remove_tashkeel: bool = False,
    normalize_hamzas: bool = True,
    normalize_alefs: bool = True,
) -> str:
    """
    Main normalization function for Arabic text.

    Args:
        text: Raw Arabic text
        remove_tashkeel: Whether to remove diacritics (default: False)
        normalize_hamzas: Normalize hamza variants (default: True)
        normalize_alefs: Normalize alef variants (default: True)

    Returns:
        Normalized Arabic text

    Raises:
        ValueError: If text is empty or contains no Arabic

    Example:
        >>> normalize_arabic_text("إِذَا غَامَرْتَ فِي شَرَفٍ مَرُومِ")
        "اِذَا غَامَرْتَ فِي شَرَفٍ مَرُومِ"
        >>> normalize_arabic_text("مَرْحَبًا", remove_tashkeel=True)
        "مرحبا"
    """
    # Edge case: None input
    if text is None:
        raise ValueError("Text cannot be None")

    # Edge case: Non-string input
    if not isinstance(text, str):
        raise ValueError(f"Text must be a string, got {type(text).__name__}")

    if not text or not text.strip():
        raise ValueError("Text cannot be empty")

    # Edge case: Text too short (less than 2 characters)
    if len(text.strip()) < 2:
        raise ValueError("Text must contain at least 2 characters")

    # Check if text contains Arabic
    if not any("\u0600" <= c <= "\u06ff" for c in text):
        raise ValueError("Text must contain Arabic characters")

    # Normalize whitespace
    text = normalize_whitespace(text)

    # Remove tatweel
    text = remove_tatweel(text)

    # Normalize hamza
    if normalize_hamzas:
        text = normalize_hamza(text)

    # Normalize alef
    if normalize_alefs:
        text = normalize_alef(text)

    # Remove diacritics if requested
    if remove_tashkeel:
        text = remove_diacritics(text)

    # Edge case: Check text is still non-empty after normalization
    if not text or not text.strip():
        raise ValueError("Text is empty after normalization")

    return text


def has_diacritics(text: str) -> bool:
    """
    Check if text contains any diacritical marks.

    Args:
        text: Arabic text

    Returns:
        True if text has diacritics, False otherwise

    Example:
        >>> has_diacritics("مَرْحَبًا")
        True
        >>> has_diacritics("مرحبا")
        False
    """
    return any(diacritic in text for diacritic in ARABIC_DIACRITICS)
