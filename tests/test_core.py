import pytest

from textkit import slugify, truncate, word_count


def test_slugify_joins_words_with_hyphens():
    assert slugify("Hello, World!") == "hello-world"


def test_slugify_keeps_digits():
    assert slugify("Top 10 tips") == "top-10-tips"


def test_word_count_counts_words():
    assert word_count("one two  three") == 3


def test_word_count_empty_string_is_zero():
    assert word_count("") == 0


def test_word_count_whitespace_only_is_zero():
    assert word_count("   \n\t ") == 0


def test_word_count_splits_on_tabs_and_newlines():
    assert word_count("a\tb\nc") == 3


def test_truncate_returns_text_that_fits_unchanged():
    assert truncate("hello world", 20) == "hello world"
    assert truncate("hello world", 11) == "hello world"


def test_truncate_cuts_on_a_word_boundary_within_width():
    result = truncate("hello brave new world", 12)
    assert result == "hello brave…"
    assert len(result) <= 12


def test_truncate_drops_the_partial_word():
    assert truncate("hello brave new world", 14) == "hello brave…"


def test_truncate_hard_cuts_a_single_long_word():
    assert truncate("supercalifragilistic", 6) == "super…"


def test_truncate_hard_cuts_when_the_first_word_does_not_fit():
    assert truncate("supercalifragilistic word", 6) == "super…"


def test_truncate_leaves_no_trailing_space_or_punctuation_before_the_ellipsis():
    assert truncate("hello, brave new world", 8) == "hello…"
    assert truncate("hello brave  new world", 13) == "hello brave…"


def test_truncate_does_not_restore_the_partial_word_when_punctuation_empties_the_prefix():
    result = truncate("--- hello world", 6)
    assert result == "---…"
    assert len(result) <= 6
    assert truncate("... hello world", 6) == "...…"


def test_truncate_width_one_is_just_the_ellipsis():
    assert truncate("hello world", 1) == "…"


@pytest.mark.parametrize("width", [0, -1])
def test_truncate_rejects_width_below_one(width):
    with pytest.raises(ValueError):
        truncate("hello", width)


def test_slugify_empty_input_is_empty():
    assert slugify("") == ""


def test_slugify_text_without_letters_or_digits_is_empty():
    assert slugify("!!! ??? ...") == ""


def test_slugify_ignores_surrounding_whitespace():
    assert slugify("  Hello  ") == "hello"
