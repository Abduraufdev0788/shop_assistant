"""Ticket #10 — FR-17 history (pure part). run_agent needs Claude: eval/ covers it (AC-2..4)."""
from shop_assistant.agent import History
from tests.conftest import xfail_stub


@xfail_stub
def test_history_keeps_last_10_turns():
    h = History(max_turns=10)
    for i in range(12):
        h.append(7, "user", f"q{i}")
        h.append(7, "assistant", f"a{i}")
    msgs = h.get(7)
    assert len(msgs) == 20
    assert msgs[0] == {"role": "user", "content": "q2"}
    assert msgs[-1] == {"role": "assistant", "content": "a11"}


@xfail_stub
def test_history_is_per_customer():
    h = History()
    h.append(1, "user", "krossovka bormi")
    assert h.get(2) == []


@xfail_stub
def test_history_clear():
    h = History()
    h.append(1, "user", "x")
    h.clear(1)
    assert h.get(1) == []
