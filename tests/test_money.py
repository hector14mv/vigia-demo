import pytest

import textkit
from textkit import format_eur

NBSP = " "


@pytest.mark.parametrize(
    "cents, expected",
    [
        (0, "0,00"),
        (5, "0,05"),
        (100, "1,00"),
        (99, "0,99"),
        (1234567, "12.345,67"),
        (100000, "1.000,00"),
        (99999, "999,99"),
        (100000000, "1.000.000,00"),
    ],
)
def test_format_eur_formats_positive_amounts(cents, expected):
    assert format_eur(cents) == expected + NBSP + "€"


@pytest.mark.parametrize(
    "cents, expected",
    [
        (-1250, "-12,50"),
        (-5, "-0,05"),
        (-100, "-1,00"),
        (-1234567, "-12.345,67"),
    ],
)
def test_format_eur_keeps_the_sign_in_front_of_negative_amounts(cents, expected):
    assert format_eur(cents) == expected + NBSP + "€"


def test_format_eur_uses_a_no_break_space_before_the_euro_sign():
    result = format_eur(1234567)
    assert result.endswith(" €")
    assert " " not in result


def test_format_eur_is_exact_beyond_float_precision():
    # 2**53 + 1 cannot be represented as a float; integer arithmetic keeps the last cent.
    assert format_eur(2**53 + 1) == "90.071.992.547.409,93" + NBSP + "€"


@pytest.mark.parametrize("value", [12.5, 1234567.0, "1234567", None, True, False])
def test_format_eur_rejects_anything_that_is_not_an_int(value):
    with pytest.raises(TypeError):
        format_eur(value)


def test_format_eur_is_exported_from_the_package():
    assert textkit.format_eur is format_eur
    assert "format_eur" in textkit.__all__
