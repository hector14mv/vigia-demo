import unicodedata


def strip_accents(text: str) -> str:
    """Remove diacritics from `text`: "Canción" -> "Cancion", "ñ" -> "n".

    Works on decomposed and precomposed input alike. Characters whose diacritic is not
    a combining mark ("ß", "ø", "đ") have no decomposition and are left as they are.
    """
    decomposed = unicodedata.normalize("NFD", text)
    kept = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
    # Recompose so characters NFD split apart without a combining mark (e.g. Hangul) come back whole.
    return unicodedata.normalize("NFC", kept)
