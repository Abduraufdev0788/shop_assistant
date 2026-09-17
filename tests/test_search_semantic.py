"""Ticket #8 — FR-10, AC-4: cosine ranking."""
import numpy as np

from shop_assistant.search import cosine_top_k


def test_cosine_top_k_orders_by_similarity():
    m = np.array([[1, 0], [0, 1], [0.9, 0.1]], dtype=np.float32)
    assert cosine_top_k(np.array([1, 0], dtype=np.float32), m, 2) == [0, 2]


def test_cosine_top_k_ignores_magnitude():
    m = np.array([[10, 0], [0, 1]], dtype=np.float32)
    assert cosine_top_k(np.array([0, 5], dtype=np.float32), m, 1) == [1]


def test_cosine_top_k_empty_matrix():
    assert cosine_top_k(np.array([1, 0], dtype=np.float32), np.zeros((0, 2), np.float32), 5) == []
