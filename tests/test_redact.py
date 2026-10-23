import pytest

import textkit
from textkit import redact


def test_redact_is_exported_from_the_package():
    assert textkit.redact is redact
    assert "redact" in textkit.__all__


def test_redact_masks_a_simple_email():
    assert redact("write to ana@example.com") == "write to [email]"


def test_redact_masks_email_with_dots_plus_and_subdomains():
    assert redact("cc first.last+tag@mail.example.co.uk now") == "cc [email] now"


def test_redact_keeps_sentence_punctuation_after_an_email():
    assert redact("mail ana@example.com.") == "mail [email]."
    assert redact("<ana@example.com>, bob@example.org") == "<[email]>, [email]"


@pytest.mark.parametrize(
    "phone",
    [
        "+34 612 345 678",
        "612-345-678",
        "(555) 123-4567",
        "612345678",
        "+34612345678",
        "555.123.4567",
        "+1 (555) 123-4567",
        "+1-555-123-4567",
    ],
)
def test_redact_masks_phone_numbers(phone):
    assert redact(f"call {phone} today") == "call [phone] today"


def test_redact_keeps_sentence_punctuation_after_a_phone():
    assert redact("call 612 345 678.") == "call [phone]."
    assert redact("call 612-345-678, please") == "call [phone], please"


def test_redact_leaves_numbers_with_fewer_than_nine_digits():
    assert redact("call 612 345 67") == "call 612 345 67"
    assert redact("code 12345678") == "code 12345678"


def test_redact_never_masks_years_prices_or_ids():
    text = "In 2026 it cost 19.99, ticket #1234"
    assert redact(text) == text


def test_redact_does_not_glue_a_date_and_time_into_a_phone():
    text = "2026-10-23 12:30:45 job done"
    assert redact(text) == text


def test_redact_masks_a_phone_that_follows_a_date():
    assert redact("2026-10-23 612 345 678 called") == "2026-10-23 [phone] called"


def test_redact_does_not_glue_thousands_separators_into_a_phone():
    text = "revenue 1,234,567,890 EUR"
    assert redact(text) == text


def test_redact_does_not_mask_a_long_hash_prefixed_id():
    text = "order #612345678 shipped"
    assert redact(text) == text


@pytest.mark.parametrize(
    "text",
    ["", "plain text, nothing personal.", "  spaces\tand\nnewlines  ", "a @ b, x@y, 3.14"],
)
def test_redact_returns_text_without_personal_data_unchanged(text):
    assert redact(text) == text


def test_redact_masks_emails_and_phones_together():
    assert (
        redact("call +34 612 345 678 or mail ana@example.com")
        == "call [phone] or mail [email]"
    )
