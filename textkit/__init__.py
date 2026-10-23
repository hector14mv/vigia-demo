"""textkit — a tiny text utility library that vigia's agents work on in the demo."""

from .core import slugify, truncate, word_count
from .redact import redact

__all__ = ["redact", "slugify", "truncate", "word_count"]
