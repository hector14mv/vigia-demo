from textkit.core import word_count


def reading_time(text: str, wpm: int = 200) -> int:
    """Whole minutes `text` takes to read at `wpm` words per minute, rounded up.

    Text with at least one word takes at least 1 minute; text with no words takes 0.
    Uses integer arithmetic only, so the result is exact for any input size.
    """
    if wpm < 1:
        raise ValueError("wpm must be at least 1")
    return -(-word_count(text) // wpm)  # ceiling division without floats
