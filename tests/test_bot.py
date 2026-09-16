"""Tickets #13, #14 — pure parts. Telegram round-trip is the AC-5 protocol in Notion."""
from shop_assistant.bot import format_escalation, log_turn, parse_esc_header, should_handle
from tests.conftest import xfail_stub


@xfail_stub
def test_should_handle_private_non_owner_only():
    assert should_handle(True, 111, owner_id=999)
    assert not should_handle(False, 111, owner_id=999)    # group — C-5
    assert not should_handle(True, 999, owner_id=999)     # owner


@xfail_stub
def test_escalation_header_roundtrip():
    msg = format_escalation(4242, "krossovka 42 bormi?", ["https://t.me/status_dokon/1300"])
    assert msg.startswith("#esc 4242\n")
    assert parse_esc_header(msg) == 4242


@xfail_stub
def test_parse_esc_header_not_an_escalation():
    assert parse_esc_header("salom") is None
    assert parse_esc_header("") is None


@xfail_stub
def test_log_turn_record_shape(tmp_path, monkeypatch):
    from shop_assistant import config
    monkeypatch.setattr(config, "LOG_PATH", tmp_path / "log.jsonl")
    rec = log_turn(4242, "krossovka 42", [{"name": "find_products", "input": {"size": "42"}, "n_results": 1}],
                   "Ha, bor: https://t.me/status_dokon/1300", False, 1200, 0.004)
    assert set(rec) >= {"ts", "chat_id", "question", "tools", "answer", "escalated", "ms", "usd"}
    assert (tmp_path / "log.jsonl").read_text().count("\n") == 1
