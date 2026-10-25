# vigia-demo

A tiny Python library (`textkit`) that [vigia](https://github.com/hector14mv/vigia) builds on its own.

Every pull request here was opened by an AI builder from a GitHub issue, reviewed on its exact
commit by a model from a different AI lab, and merged by `vigia watch`, a Python script that does
not call any model. Read the issues, then the pull requests: the handoff, the review and the merge
comment on each one are the whole story.

## Functions

Import from the module, or straight from `textkit`.

| Function | What it does | Import |
| --- | --- | --- |
| `slugify` | Lowercases text and joins its words with hyphens. | `from textkit.core import slugify` |
| `word_count` | How many words the text has, splitting on whitespace. | `from textkit.core import word_count` |
| `truncate` | Shortens text to at most `width` characters on a word boundary, ending with "…". | `from textkit.core import truncate` |
| `format_eur` | Formats an integer amount of euro cents as Spanish invoice text. | `from textkit.money import format_eur` |
| `strip_accents` | Removes diacritics from text. | `from textkit.accents import strip_accents` |
| `reading_time` | Whole minutes the text takes to read at `wpm` words per minute, rounded up. | `from textkit.reading import reading_time` |
| `title_case` | Capitalises each word, keeping the joining words lowercase unless first. | `from textkit.titlecase import title_case` |

All seven functions import straight from `textkit`: `from textkit import slugify, word_count, truncate, format_eur, strip_accents, reading_time, title_case`.
Each one also imports from its own module, as the table shows.

```bash
python -m pytest
```
