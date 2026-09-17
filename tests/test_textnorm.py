"""Ticket #2 — FR-9. Remove xfail_stub when normalise() is implemented."""
import pytest

from shop_assistant.textnorm import normalise


@pytest.mark.parametrize("a,b", [
    ("Krossovka", "krossovka"),          # case
    ("кроссовка", "krossovka"),          # ru Cyrillic → Latin
    ("Кроссовка", "krossovka"),
    ("oʻzbek", "ozbek"),                 # oʻ
    ("o'zbek", "ozbek"),                 # o'
    ("ўзбек", "ozbek"),                  # ў
    ("gʻisht", "gisht"),
    ("ғишт", "gisht"),
    ("ҳамма", "hamma"),
    ("қора", "qora"),
    ("Dvoyka", "dvoyka"),
    ("двойка", "dvoyka"),
    ("куртка", "kurtka"),                # from CAPTION_KURTKA
    ("қишки", "qishki"),                # from CAPTION_KURTKA
    ("самарқанд", "samarqand"),          # from FOOTER
    ("янги", "yangi"),                  # from CAPTION_DVOYKA
    ("нарх", "narx"),                   # from CAPTION_DVOYKA
])
def test_scripts_fold_to_one_form(a, b):
    assert normalise(a) == normalise(b) == b


def test_whitespace_collapsed():
    assert normalise("  qishki   kurtka \n") == "qishki kurtka"


def test_empty_string():
    assert normalise("") == ""


def test_digits_and_punctuation_kept():
    assert normalise("Razmer: 42") == "razmer: 42"
