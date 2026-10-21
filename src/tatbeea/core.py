"""Core normalization functions.

Every function takes a str and returns a new str; none of them mutate input
or depend on anything outside the standard library.
"""

import re

# Harakat (U+064B..U+0652), superscript alef (U+0670) and Quranic marks
# (U+0610..U+061A, U+06D6..U+06ED).
_TASHKEEL_RE = re.compile("[ؐ-ًؚ-ْٰۖ-ۭ]")

_TATWEEL = "ـ"

_ALEF_MAP = str.maketrans({
    "أ": "ا",  # أ
    "إ": "ا",  # إ
    "آ": "ا",  # آ
    "ٱ": "ا",  # ٱ
})

_YEH_MAP = str.maketrans({"ى": "ي"})  # ى -> ي

_TEH_MARBUTA_MAP = str.maketrans({"ة": "ه"})  # ة -> ه

_ARABIC_INDIC = "٠١٢٣٤٥٦٧٨٩"
_PERSIAN = "۰۱۲۳۴۵۶۷۸۹"
_LATIN = "0123456789"

_TO_LATIN_DIGITS = str.maketrans(_ARABIC_INDIC + _PERSIAN, _LATIN * 2)
_TO_ARABIC_DIGITS = str.maketrans(_LATIN, _ARABIC_INDIC)


def remove_tashkeel(text: str) -> str:
    """Remove harakat and Quranic annotation marks: "مُحَمَّد" -> "محمد"."""
    return _TASHKEEL_RE.sub("", text)


def remove_tatweel(text: str) -> str:
    """Remove the kashida/tatweel stretch character: "مـــرحبا" -> "مرحبا"."""
    return text.replace(_TATWEEL, "")


def normalize_alef(text: str) -> str:
    """Fold أ, إ, آ and ٱ into a bare ا."""
    return text.translate(_ALEF_MAP)


def normalize_yeh(text: str) -> str:
    """Fold alef maksura ى into ي."""
    return text.translate(_YEH_MAP)


def normalize_teh_marbuta(text: str) -> str:
    """Fold teh marbuta ة into ه."""
    return text.translate(_TEH_MARBUTA_MAP)


def normalize_digits(text: str) -> str:
    """Convert Arabic-Indic (٠-٩) and Persian (۰-۹) digits to 0-9."""
    return text.translate(_TO_LATIN_DIGITS)


def to_arabic_digits(text: str) -> str:
    """Convert 0-9 to Arabic-Indic digits (٠-٩)."""
    return text.translate(_TO_ARABIC_DIGITS)


def normalize(
    text: str,
    *,
    tashkeel: bool = True,
    tatweel: bool = True,
    alef: bool = True,
    yeh: bool = True,
    teh_marbuta: bool = False,
    digits: bool = True,
    collapse_spaces: bool = True,
) -> str:
    """Apply the common normalization steps used before search or matching.

    Teh marbuta folding is off by default because it changes meaning more
    often than the other steps (e.g. "مدرسة" vs "مدرسه" are both common,
    but "ة" and "ه" are distinct letters in formal writing).
    """
    if tashkeel:
        text = remove_tashkeel(text)
    if tatweel:
        text = remove_tatweel(text)
    if alef:
        text = normalize_alef(text)
    if yeh:
        text = normalize_yeh(text)
    if teh_marbuta:
        text = normalize_teh_marbuta(text)
    if digits:
        text = normalize_digits(text)
    if collapse_spaces:
        text = " ".join(text.split())
    return text
