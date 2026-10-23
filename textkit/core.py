import re


def slugify(text: str) -> str:
    """Lowercase `text` and join its words with hyphens: "Hello, World!" -> "hello-world"."""
    words = re.findall(r"[a-z0-9]+", text.lower())
    return "-".join(words)


def word_count(text: str) -> int:
    """How many words `text` has, splitting on whitespace."""
    return len(text.split())
