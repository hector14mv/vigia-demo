import unicodedata


def strip_accents(text: str) -> str:
    """Remove diacritics from `text`: "Canción" -> "Cancion", "ñ" -> "n".

    Works on decomposed and precomposed input alike. Characters whose diacritic is not
    a combining mark ("ß", "ø", "đ") have no decomposition and are left as they are.
    """
    out = []
    for ch in text:
        decomposed = unicodedata.normalize("NFD", ch)
        if any(unicodedata.combining(part) for part in decomposed):
            out.append("".join(part for part in decomposed if not unicodedata.combining(part)))
        else:
            # No diacritic to remove: keep the original, since NFD may swap in an equivalent
            # character (KELVIN SIGN -> "K", OHM SIGN -> GREEK CAPITAL OMEGA) or split it (Hangul).
            out.append(ch)
    return "".join(out)
