import textkit
from textkit import (
    format_eur,
    reading_time,
    slugify,
    strip_accents,
    title_case,
    truncate,
    word_count,
)

SEVEN = [
    "slugify",
    "word_count",
    "truncate",
    "format_eur",
    "strip_accents",
    "reading_time",
    "title_case",
]


def test_all_lists_exactly_the_seven_functions():
    assert sorted(textkit.__all__) == sorted(SEVEN)
    assert len(textkit.__all__) == len(SEVEN)


def test_package_exports_are_the_module_functions():
    from textkit.accents import strip_accents as m_strip
    from textkit.core import slugify as m_slugify
    from textkit.money import format_eur as m_eur
    from textkit.reading import reading_time as m_reading
    from textkit.titlecase import title_case as m_title

    assert strip_accents is m_strip
    assert slugify is m_slugify
    assert format_eur is m_eur
    assert reading_time is m_reading
    assert title_case is m_title


def test_every_exported_name_is_callable():
    for name in SEVEN:
        assert callable(getattr(textkit, name))
    assert callable(truncate) and callable(word_count)
