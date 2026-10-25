"""textkit — a tiny text utility library that vigia's agents work on in the demo."""

from .accents import strip_accents
from .core import slugify, truncate, word_count
from .money import format_eur
from .reading import reading_time
from .titlecase import title_case

__all__ = [
    "slugify",
    "word_count",
    "truncate",
    "format_eur",
    "strip_accents",
    "reading_time",
    "title_case",
]
