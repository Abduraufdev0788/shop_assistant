"""Ticket #4 — FR-2, FR-3 (pure part). fetch() itself is integration: see Notion protocol."""
from shop_assistant.fetch import dedup
from tests.conftest import xfail_stub


@xfail_stub
def test_dedup_drops_empty_and_keeps_newest_repost(posts):
    kept = dedup(posts)
    ids = {p.id for p in kept}
    assert 1302 not in ids            # FR-2 empty caption
    assert 1301 in ids and 1234 not in ids   # FR-3 same caption → newest id wins
    assert 1300 in ids


@xfail_stub
def test_dedup_empty_input():
    assert dedup([]) == []
