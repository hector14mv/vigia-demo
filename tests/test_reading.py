import pytest

from textkit.reading import reading_time


@pytest.mark.parametrize("text", ["", "   \n\t "])
def test_reading_time_no_words_is_zero(text):
    assert reading_time(text) == 0


def test_reading_time_a_single_word_takes_one_minute():
    assert reading_time("hola") == 1


@pytest.mark.parametrize(
    "words, minutes",
    [(1, 1), (199, 1), (200, 1), (201, 2), (400, 2), (401, 3)],
)
def test_reading_time_rounds_up_at_default_wpm(words, minutes):
    assert reading_time("w " * words) == minutes


def test_reading_time_honours_wpm():
    text = "w " * 300
    assert reading_time(text, wpm=100) == 3
    assert reading_time(text, wpm=300) == 1


def test_reading_time_returns_an_int():
    assert isinstance(reading_time("hola"), int)
    assert isinstance(reading_time(""), int)
    assert isinstance(reading_time("w " * 201), int)


def test_reading_time_splits_words_on_tabs_and_newlines():
    assert reading_time("a\tb\nc", wpm=1) == 3


@pytest.mark.parametrize("wpm", [0, -1])
def test_reading_time_rejects_wpm_below_one(wpm):
    with pytest.raises(ValueError):
        reading_time("hola", wpm=wpm)


def test_reading_time_is_exact_for_large_inputs():
    assert reading_time("w " * 1_000_001, wpm=1) == 1_000_001
