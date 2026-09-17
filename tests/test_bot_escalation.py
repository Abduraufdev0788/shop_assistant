"""Ticket #14 — FR-19/21, D-5 (pure parts). Round-trip is the AC-5 protocol in Notion."""
from shop_assistant.bot import format_escalation, parse_esc_header


def test_escalation_header_roundtrip():
    msg = format_escalation(4242, "krossovka 42 bormi?", ["https://t.me/status_dokon/1300"])
    assert msg.startswith("#esc 4242\n")
    assert parse_esc_header(msg) == 4242


def test_parse_esc_header_not_an_escalation():
    assert parse_esc_header("salom") is None
    assert parse_esc_header("") is None
