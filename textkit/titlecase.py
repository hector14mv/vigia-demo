JOINING_WORDS = frozenset({"de", "del", "la", "y", "of", "and", "the"})


def title_case(text: str) -> str:
    """Capitalise each word of `text`, keeping the joining words lowercase unless first.

    Words are the whitespace-separated tokens of `text` and are rejoined with single
    spaces. Each word is normalised to an uppercase first character and lowercase rest;
    a word in `JOINING_WORDS` (matched case-insensitively, on the whole token) stays
    lowercase unless it is the first word. Punctuation stays attached to its word, so
    "de," is not a joining word and comes out as "De,".
    """
    words = []
    for index, word in enumerate(text.split()):
        lowered = word.lower()
        if index > 0 and lowered in JOINING_WORDS:
            words.append(lowered)
        else:
            words.append(lowered[:1].upper() + lowered[1:])
    return " ".join(words)
