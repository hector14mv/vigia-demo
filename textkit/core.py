import re


def slugify(text: str) -> str:
    """Lowercase `text` and join its words with hyphens: "Hello, World!" -> "hello-world"."""
    words = re.findall(r"[a-z0-9]+", text.lower())
    return "-".join(words)


def word_count(text: str) -> int:
    """How many words `text` has, splitting on whitespace."""
    return len(text.split())


def truncate(text: str, width: int) -> str:
    """Shorten `text` to at most `width` characters on a word boundary, ending with "…".

    Text that already fits is returned unchanged. A first word longer than the room
    available is hard-cut. The ellipsis counts toward `width`.
    """
    if width < 1:
        raise ValueError("width must be at least 1")
    if len(text) <= width:
        return text
    budget = width - 1  # room left for the text once the ellipsis is counted
    if text[budget].isspace():
        head = text[:budget]  # the cut falls right after a whole word
    else:
        head = re.sub(r"\s*\S*$", "", text[:budget])  # drop the partial word
    head = head.rstrip()
    if not head:
        return text[:budget] + "…"  # the first word is too long: hard-cut it
    # Strip trailing punctuation, but keep a whole leading token such as "---" rather
    # than falling back to the partial word that follows it.
    return (head.rstrip(",.;:-").rstrip() or head) + "…"
