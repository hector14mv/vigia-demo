def format_eur(cents: int) -> str:
    """Format an integer amount of euro cents as Spanish invoice text: 1234567 -> "12.345,67 €".

    Thousands are grouped with dots, the decimal separator is a comma, and the space
    before "€" is a no-break space (U+00A0). Only integer arithmetic is used, so no
    amount is ever rounded through a float. Anything that is not an `int` (including
    `bool`, which is an `int` subclass) raises `TypeError`.
    """
    if isinstance(cents, bool) or not isinstance(cents, int):
        raise TypeError(f"cents must be an int, not {type(cents).__name__}")
    sign = "-" if cents < 0 else ""
    # Split the magnitude, not the signed value: divmod floors, so divmod(-5, 100) is (-1, 95).
    euros, rest = divmod(abs(cents), 100)
    grouped = f"{euros:,}".replace(",", ".")
    return f"{sign}{grouped},{rest:02d} €"
