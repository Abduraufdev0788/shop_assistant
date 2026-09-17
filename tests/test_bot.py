"""Ticket #13 — C-5, FR-25 (pure parts). Telegram behaviour is the protocol in Notion."""
from shop_assistant.bot import log_turn, should_handle


def test_should_handle_private_non_owner_only():
    assert should_handle(True, 111, owner_id=999)
    assert not should_handle(False, 111, owner_id=999)    # group — C-5
    assert not should_handle(True, 999, owner_id=999)     # owner


def test_log_turn_record_shape(tmp_path, monkeypatch):
    from shop_assistant import config
    monkeypatch.setattr(config, "LOG_PATH", tmp_path / "log.jsonl")
    rec = log_turn(4242, "krossovka 42", [{"name": "find_products", "input": {"size": "42"}, "n_results": 1}],
                   "Ha, bor: https://t.me/status_dokon/1300", False, 1200, 0.004)
    assert set(rec) >= {"ts", "chat_id", "question", "tools", "answer", "escalated", "ms", "usd"}
    assert (tmp_path / "log.jsonl").read_text().count("\n") == 1
