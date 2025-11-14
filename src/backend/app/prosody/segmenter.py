"""Phonetic segmentation for Arabic prosody (simplified).
Segments into rough syllable units based on consonant/vowel heuristics.
"""

from dataclasses import dataclass
from typing import List

VOWELS = set("اويى")  # treat alif, waw, ya as long potential vowels
CONSONANTS = set("بتثجحخدذرزسشصضطظعغفقكلمنهه")


@dataclass
class Syllable:
    text: str
    kind: str  # CV, CVV, CVC, other
    long: bool


def classify_syllable(s: str) -> Syllable:
    # simplistic classification
    if len(s) == 2 and s[0] in CONSONANTS and s[1] in VOWELS:
        return Syllable(text=s, kind="CV", long=False)
    if len(s) == 2 and s[0] in CONSONANTS and s[1] in VOWELS:
        return Syllable(text=s, kind="CV", long=False)
    if len(s) == 3 and s[0] in CONSONANTS and s[1] in VOWELS and s[2] in VOWELS:
        return Syllable(text=s, kind="CVV", long=True)
    if len(s) == 3 and s[0] in CONSONANTS and s[1] in VOWELS and s[2] in CONSONANTS:
        return Syllable(text=s, kind="CVC", long=True)
    return Syllable(text=s, kind="other", long=len(s) > 2)


def segment(text: str) -> List[Syllable]:
    syllables: List[Syllable] = []
    buf = ""
    for ch in text:
        if ch == " ":
            if buf:
                syllables.append(classify_syllable(buf))
                buf = ""
            continue
        buf += ch
        # naive boundary rules
        if len(buf) >= 3:
            syllables.append(classify_syllable(buf))
            buf = ""
    if buf:
        syllables.append(classify_syllable(buf))
    return syllables
