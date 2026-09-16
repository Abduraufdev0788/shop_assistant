"""Ticket #5 — FR-3a, FR-3b (pure parts). extract() needs Claude: integration protocol in Notion."""
import pytest

from shop_assistant.extract import parse_price, strip_footer
from tests.conftest import CAPTION_DVOYKA, CAPTION_KROSSOVKA, xfail_stub


@xfail_stub
def test_strip_footer_removes_contact_lines_and_emoji():
    body = strip_footer(CAPTION_DVOYKA)
    assert "998" not in body and "@status_dokon" not in body and "Manzil" not in body
    assert "🍂" not in body and "🔥" not in body
    assert "Dvoyka" in body and "980.000" in body


@xfail_stub
def test_strip_footer_keeps_subscriber_price_line():
    body = strip_footer(CAPTION_KROSSOVKA)
    assert "obunachilariga" in body


@xfail_stub
def test_strip_footer_empty():
    assert strip_footer("") == ""


@xfail_stub
@pytest.mark.parametrize("raw,expected", [
    ("980.000ming", 980000),
    ("Narx:980.000ming", 980000),
    ("350.000", 350000),
    ("1.200.000", 1200000),
    ("980 000 so'm", 980000),
    ("980k", 980000),
    ("narxi so'rang", None),
    ("", None),
])
def test_parse_price_shop_notation(raw, expected):
    assert parse_price(raw) == expected
