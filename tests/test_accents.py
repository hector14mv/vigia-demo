import unicodedata

from textkit.accents import strip_accents


def test_strips_vowel_accents():
    assert strip_accents("áéíóú") == "aeiou"


def test_strips_tilde_from_n():
    assert strip_accents("ñ") == "n"


def test_strips_diaeresis():
    assert strip_accents("ü") == "u"


def test_preserves_case():
    assert strip_accents("Ángel ÑU") == "Angel NU"


def test_text_without_diacritics_is_unchanged():
    assert strip_accents("Hello, World! 123") == "Hello, World! 123"


def test_empty_string():
    assert strip_accents("") == ""


def test_result_has_no_combining_marks():
    result = strip_accents("canción")
    assert result == "cancion"
    assert len(result) == len("cancion")
    assert not any(unicodedata.combining(ch) for ch in result)


def test_decomposed_input_is_stripped_too():
    assert strip_accents("n" + "̃") == "n"
    assert strip_accents(unicodedata.normalize("NFD", "Canción de cumpleaños")) == "Cancion de cumpleanos"


def test_precomposed_and_decomposed_give_the_same_result():
    text = "Ángel Ñandú, canción"
    assert strip_accents(text) == strip_accents(unicodedata.normalize("NFD", text))


def test_characters_without_a_decomposition_are_left_alone():
    # Pinned on purpose: these are not transliterated, and they are not dropped either.
    assert strip_accents("ß") == "ß"
    assert strip_accents("ø") == "ø"
    assert strip_accents("đ") == "đ"
    assert strip_accents("straße") == "straße"
