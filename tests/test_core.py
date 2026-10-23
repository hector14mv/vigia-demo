from textkit import slugify, word_count


def test_slugify_joins_words_with_hyphens():
    assert slugify("Hello, World!") == "hello-world"


def test_slugify_keeps_digits():
    assert slugify("Top 10 tips") == "top-10-tips"


def test_word_count_counts_words():
    assert word_count("one two  three") == 3
