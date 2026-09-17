"""Ticket #9 — compact tool output, NFR-2."""
import dataclasses

from shop_assistant.tools import format_product


def test_format_product_one_line_with_link(products):
    line = format_product(products[1])
    assert "\n" not in line
    assert "Krossovka Nike Air" in line and "350000" in line and "40" in line
    assert "https://t.me/status_dokon/1300" in line
    assert "eskirgan" not in line


def test_format_product_stale_tag(products):
    line = format_product(dataclasses.replace(products[2], stale=True))
    assert line.endswith("[eskirgan]")


def test_format_product_unknown_price(products):
    line = format_product(dataclasses.replace(products[0], price=None))
    assert "None" not in line
