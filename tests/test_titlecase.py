import pytest

from textkit.titlecase import title_case


def test_leading_joining_word_is_capitalised_inner_ones_are_not():
    assert title_case("la casa de la pradera") == "La Casa de la Pradera"


def test_english_joining_words():
    assert title_case("the lord of the rings") == "The Lord of the Rings"


def test_other_words_are_normalised_whatever_the_input_case():
    assert title_case("HELLO wORLD") == "Hello World"


def test_joining_word_is_recognised_regardless_of_case():
    assert title_case("casa DE campo") == "Casa de Campo"


@pytest.mark.parametrize("word", ["de", "del", "la", "y", "of", "and", "the"])
def test_each_joining_word_stays_lowercase_when_not_first(word):
    assert title_case(f"casa {word} campo") == f"Casa {word} Campo"


def test_word_merely_starting_with_a_joining_word_is_unaffected():
    assert title_case("delta y lavanda") == "Delta y Lavanda"
    assert title_case("land of theory") == "Land of Theory"


def test_empty_string_returns_empty_string():
    assert title_case("") == ""


def test_whitespace_only_returns_empty_string():
    assert title_case("   ") == ""


def test_whitespace_runs_collapse_to_single_spaces():
    assert title_case("a  b") == "A B"
    assert title_case("  la\tcasa \n de  campo ") == "La Casa de Campo"


def test_single_joining_word_is_capitalised():
    assert title_case("de") == "De"


def test_punctuation_stays_attached_and_blocks_joining_match():
    # The joining check is on the whole token, so "de," is not a joining word.
    assert title_case("casa, de campo") == "Casa, de Campo"
    assert title_case("casa de, campo") == "Casa De, Campo"
