"""Tickets #7, #8 — FR-8, FR-10, FR-11, FR-12, FR-16."""
import numpy as np
import pytest

from shop_assistant.search import (cosine_top_k, find_products, is_stale, keyword_match,
                                   latest_posts)
from tests.conftest import xfail_stub

TODAY = "2026-09-16"


# ---- ticket #7: filters ----------------------------------------------------

@xfail_stub
@pytest.mark.parametrize("date,expected", [
    ("2026-09-10", False),
    ("2026-07-18", False),   # exactly 60 days
    ("2026-07-17", True),    # 61 days
    ("2026-06-01", True),
])
def test_is_stale_boundary(date, expected):
    assert is_stale(date, TODAY, 60) is expected


@xfail_stub
def test_keyword_match_is_script_insensitive(products):
    assert keyword_match(["Кроссовка"], products[1])
    assert keyword_match(["nike"], products[1])
    assert not keyword_match(["kurtka"], products[1])


@xfail_stub
def test_find_products_filters_are_anded(products):
    got = find_products(category="kiyim", max_price=1000000, products=products)
    assert [p.id for p in got] == [1234]
    assert find_products(category="kiyim", size="42", products=products) == []


@xfail_stub
def test_find_products_size_and_price_range(products):
    got = find_products(size="42", min_price=300000, max_price=400000, products=products)
    assert [p.id for p in got] == [1300]


@xfail_stub
def test_find_products_color(products):
    assert [p.id for p in find_products(color="qora", products=products)] == [900]


@xfail_stub
def test_find_products_marks_stale_and_keeps_link_date(products):
    got = find_products(keywords=["kurtka"], products=products)
    assert len(got) == 1 and got[0].stale is True
    assert got[0].link.startswith("https://t.me/status_dokon/") and got[0].date   # FR-11


@xfail_stub
def test_find_products_limit_and_newest_first(products):
    got = find_products(category="kiyim", limit=1, products=products)
    assert [p.id for p in got] == [1234]          # 2026-09-10 beats 2026-06-01


@xfail_stub
def test_find_products_no_filters_empty_catalog():
    assert find_products(products=[]) == []


@xfail_stub
def test_latest_posts(products):
    assert [p.id for p in latest_posts(2, products=products)] == [1300, 1234]


# ---- ticket #8: semantic ---------------------------------------------------

@xfail_stub
def test_cosine_top_k_orders_by_similarity():
    m = np.array([[1, 0], [0, 1], [0.9, 0.1]], dtype=np.float32)
    assert cosine_top_k(np.array([1, 0], dtype=np.float32), m, 2) == [0, 2]


@xfail_stub
def test_cosine_top_k_ignores_magnitude():
    m = np.array([[10, 0], [0, 1]], dtype=np.float32)
    assert cosine_top_k(np.array([0, 5], dtype=np.float32), m, 1) == [1]


@xfail_stub
def test_cosine_top_k_empty_matrix():
    assert cosine_top_k(np.array([1, 0], dtype=np.float32), np.zeros((0, 2), np.float32), 5) == []
