from textkit import slugify, word_count


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
