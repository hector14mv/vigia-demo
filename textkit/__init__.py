"""textkit — a tiny text utility library that vigia's agents work on in the demo."""

from .core import slugify, truncate, word_count
from .money import format_eur

__all__ = ["slugify", "truncate", "word_count", "format_eur"]
