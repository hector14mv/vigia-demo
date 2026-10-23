import re

# local@label.label.tld: the trailing dot of a sentence is never part of the domain.
# The local part is either quoted ("first last") or a run of address characters
# in which an apostrophe may sit between two of them (o'connor). Delimiters common
# in logs (= / ` { | }) and a leading or trailing apostrophe are left out, so
# "user=ana@x.com" and "'ana@x.com'" keep their surrounding text.
_EMAIL = re.compile(
    r"""(?:"(?:[^"\\\r\n]|\\.)*"|[\w.!#$%&*+?^~-]+(?:'[\w.!#$%&*+?^~-]+)*)"""
    r"@(?:[^\W_](?:[\w-]*[^\W_])?\.)+[^\W\d_]{2,}"
)

_DAY = r"(?:0?[1-9]|[12][0-9]|3[01])"
_MONTH = r"(?:0?[1-9]|1[0-2])"
_YEAR = r"(?:19|20)[0-9]{2}"

# A phone-shaped run of digits: an optional "+" country code, an optional "(area)"
# group, then digit groups joined by single spaces, dashes or dots, in any mix. It
# may not start inside a word or after "#" (ids). Dates (2026-10-23, 23.10.2026)
# and runs of years (2025 2026 2027) are matched first and kept as they are, so
# they are never glued to each other or to a phone number that follows them.
_PHONE = re.compile(
    r"(?<![\w#+])(?:"
    rf"(?P<date>(?:{_YEAR}(?P<dsep>[.-]){_MONTH}(?P=dsep){_DAY}"
    rf"|{_DAY}(?P<esep>[.-]){_DAY}(?P=esep)[0-9]{{4}})(?!\w))"
    rf"|(?P<years>{_YEAR}(?:[ .-]{_YEAR})+(?!\w))"
    r"|(?P<phone>"
    r"(?:\+[0-9]{1,3}[ .-]?)?"
    r"(?:\([0-9]{1,4}\)[ .-]?)?"
    r"[0-9]+(?:[ .-][0-9]+)*"
    r"(?!\w))"
    r")"
)

_MIN_PHONE_DIGITS = 9

# The integer part of a price: plain (1234567) or grouped in thousands (1 234 567).
_PRICE_INTEGER = re.compile(r"[0-9]+|[0-9]{1,3}(?: [0-9]{3})+")


def _mask_phone(match: re.Match[str]) -> str:
    phone = match.group("phone")
    if phone is None:
        return match.group()
    # A ".dd" after a price-shaped integer is the decimal part of a price
    # (1234567.89), not a digit group: only the integer part can be a phone number.
    head, dot, tail = phone.rpartition(".")
    decimals = ""
    if dot and len(tail) <= 2 and _PRICE_INTEGER.fullmatch(head):
        phone, decimals = head, dot + tail
    digits = sum(ch.isdigit() for ch in phone)
    return "[phone]" + decimals if digits >= _MIN_PHONE_DIGITS else match.group()


def redact(text: str) -> str:
    """Replace every email address with "[email]" and every phone number with "[phone]".

    A phone number is a run of at least 9 digits, optionally with a "+" country code
    and spaces, dashes, dots or parentheses. Shorter numbers (years, prices, "#1234"
    ids), dates, runs of years, the decimal part of a price and text with nothing to
    redact are returned unchanged.
    """
    text = _EMAIL.sub("[email]", text)
    return _PHONE.sub(_mask_phone, text)
