import re

# local@label.label.tld: the trailing dot of a sentence is never part of the domain.
# The local part is a run of RFC 5322 dot-atom characters. Apostrophes and backticks
# may only sit between two other characters (o'connor), so an address quoted as
# 'ana@x.com' or `ana@x.com` keeps its quotes. Quoted local parts ("first last")
# are out of scope and left as they are.
_LOCAL_CHARS = r"[\w.!#$%&*+/=?^{|}~-]"
_EMAIL = re.compile(
    rf"{_LOCAL_CHARS}+(?:['`]{_LOCAL_CHARS}+)*"
    r"@(?:[^\W_](?:[\w-]*[^\W_])?\.)+[^\W\d_]{2,}"
)

_DAY = r"(?:0?[1-9]|[12][0-9]|3[01])"
_MONTH = r"(?:0?[1-9]|1[0-2])"
_YEAR = r"(?:19|20)[0-9]{2}"

# Digit groups joined by single spaces, dashes or dots. The lookahead makes every run
# maximal, so a phone shape is never cut out of a longer run (12 345 6789 stays whole).
_RUN = r"[0-9]+(?:[ .-][0-9]+)*(?![0-9]|[ .-][0-9])"

# A candidate is a whole run, optionally after "+country code" or "(area code) ".
# Dates (2026-10-23, 23.10.2026) and runs of years (2025 2026 2027) are matched first
# and kept as they are, so a phone number that follows them is still found.
_CANDIDATE = re.compile(
    r"(?<![0-9])(?:"
    rf"(?P<date>(?:{_YEAR}(?P<dsep>[.-]){_MONTH}(?P=dsep){_DAY}"
    rf"|{_DAY}(?P<esep>[.-]){_DAY}(?P=esep)[0-9]{{4}})(?!\w))"
    rf"|(?P<years>{_YEAR}(?:[ .-]{_YEAR})+(?!\w))"
    rf"|(?P<phone>\+{_RUN}|\([0-9]{{3}}\)[ .-]{_RUN}|{_RUN})"
    r")"
)

# The only phone shapes in scope.
_INTERNATIONAL = re.compile(r"\+[0-9]{1,3}((?:[ .-][0-9]{2,4})+)")
_THREE_BY_THREE = re.compile(r"[0-9]{3}[ .-][0-9]{3}[ .-][0-9]{3}")
_NORTH_AMERICAN = re.compile(r"(?:\([0-9]{3}\)[ .-]|[0-9]{3}[ .-])?[0-9]{3}[ .-][0-9]{4}")

_FORBIDDEN_NEIGHBOURS = "#-/"


def _is_phone(candidate: str) -> bool:
    international = _INTERNATIONAL.fullmatch(candidate)
    if international:
        return 8 <= sum(ch.isdigit() for ch in international.group(1)) <= 12
    return bool(
        _THREE_BY_THREE.fullmatch(candidate) or _NORTH_AMERICAN.fullmatch(candidate)
    )


def _forbidden_neighbour(ch: str) -> bool:
    return ch.isalnum() or ch == "_" or ch in _FORBIDDEN_NEIGHBOURS


def _mask_phone(match: re.Match[str]) -> str:
    phone = match.group("phone")
    if phone is None or not _is_phone(phone):
        return match.group()
    text, start, end = match.string, match.start(), match.end()
    if start > 0 and _forbidden_neighbour(text[start - 1]):
        return phone
    if end < len(text):
        after = text[end : end + 2]
        if _forbidden_neighbour(after[0]):
            return phone
        # 612 345 678,90 is a decimal number, not a phone followed by a comma.
        if after[0] in ".," and after[1:].isdigit():
            return phone
    return "[phone]"


def redact(text: str) -> str:
    """Replace every email address with "[email]" and every phone number with "[phone]".

    A phone number is one of three shapes: international (+34 612 345 678), three
    groups of three digits (612 345 678) or North American ((555) 123-4567, 123-4567),
    standing on its own: not next to a letter, digit, "#", "-" or "/", and not
    followed by a decimal part. Any other run of digits (years, prices, "#1234" ids,
    dates) and text with nothing to redact are returned unchanged.
    """
    text = _EMAIL.sub("[email]", text)
    return _CANDIDATE.sub(_mask_phone, text)
