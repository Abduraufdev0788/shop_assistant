"""Ticket #12 — AC-2, AC-3, AC-4 scoring is pure."""
from eval.run_eval import contains_invented_numbers, score


def test_score_counts_ac2_ac3_ac4():
    results = [
        {"expected": {"posts": [1300]}, "posts": [1300], "escalated": False, "invented": False, "semantic_only": True},
        {"expected": {"posts": [1234]}, "posts": [900], "escalated": False, "invented": True, "semantic_only": False},
        {"expected": {"escalate": True}, "posts": [], "escalated": True, "invented": False, "semantic_only": False},
    ]
    s = score(results)
    assert s == {"ac2": 2, "ac3": 1, "ac4": 1, "total": 3}


def test_score_empty():
    assert score([]) == {"ac2": 0, "ac3": 0, "ac4": 0, "total": 0}


def test_contains_invented_numbers(products):
    assert not contains_invented_numbers("Krossovka Nike Air, 350000 so'm, razmer 42", [products[1]])
    assert contains_invented_numbers("Krossovka Nike Air, 300000 so'm", [products[1]])
    assert contains_invented_numbers("razmer 45 bor", [products[1]])
