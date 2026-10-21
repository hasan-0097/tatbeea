"""tatbeea: small, dependency-free Arabic text normalization."""

from .core import (
    normalize,
    normalize_alef,
    normalize_digits,
    normalize_teh_marbuta,
    normalize_yeh,
    remove_tashkeel,
    remove_tatweel,
    to_arabic_digits,
)

__all__ = [
    "normalize",
    "normalize_alef",
    "normalize_digits",
    "normalize_teh_marbuta",
    "normalize_yeh",
    "remove_tashkeel",
    "remove_tatweel",
    "to_arabic_digits",
]

__version__ = "0.1.0"
