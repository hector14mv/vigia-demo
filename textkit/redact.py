import re

# local@label.label.tld: the trailing dot of a sentence is never part of the domain.
_EMAIL = re.compile(r"[\w.%+-]+@(?:[^\W_](?:[\w-]*[^\W_])?\.)+[^\W\d_]{2,}")

# A phone-shaped run of digits: an optional "+" country code, an optional "(area)"
# group, then digit groups joined by one kind of separator (space, dash or dot) so
# that runs such as "2026-10-23 12:30" are not glued into one number. It may not
# start inside a word or after "#" (ids).
_PHONE = re.compile(
    r"(?<![\w#+])"
    r"(?:\+[0-9]{1,3}[ .-]?)?"
    r"(?:\([0-9]{1,4}\)[ .-]?)?"
    r"[0-9]+(?:(?P<sep>[ .-])[0-9]+(?:(?P=sep)[0-9]+)*)?"
    r"(?!\w)"
)

_MIN_PHONE_DIGITS = 9


def _mask_phone(match: re.Match[str]) -> str:
    digits = sum(ch.isdigit() for ch in match.group())
    return "[phone]" if digits >= _MIN_PHONE_DIGITS else match.group()


def redact(text: str) -> str:
    """Replace every email address with "[email]" and every phone number with "[phone]".

    A phone number is a run of at least 9 digits, optionally with a "+" country code
    and spaces, dashes, dots or parentheses. Shorter numbers (years, prices, "#1234"
    ids) and text with nothing to redact are returned unchanged.
    """
    text = _EMAIL.sub("[email]", text)
    return _PHONE.sub(_mask_phone, text)
