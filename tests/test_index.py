"""Ticket #6 — FR-5 (pure part). embed()/reindex() hit Voyage: integration protocol in Notion."""
from shop_assistant.index import product_text
from tests.conftest import xfail_stub


@xfail_stub
def test_product_text_joins_name_body_keywords(products):
    t = product_text(products[1])
    assert t.startswith("Krossovka Nike Air ")
    assert "Razmer 40 41 42 43" in t
    assert t.endswith("krossovka krossovki sneakers nike")


@xfail_stub
def test_product_text_without_keywords(products):
    import dataclasses
    p = dataclasses.replace(products[0], keywords=())
    assert product_text(p) == "Dvoyka Yangi model Dvoyka Razmer M L XL 2XL 3XL"
