import dataclasses

import pytest

from shop_assistant.models import FaqEntry, Post, Product


def test_product_is_frozen_and_comparable(products):
    a, b = products[0], dataclasses.replace(products[0])
    assert a == b and hash(a) == hash(b)
    with pytest.raises(dataclasses.FrozenInstanceError):
        a.price = 1


def test_product_has_every_sdd_field():
    names = {f.name for f in dataclasses.fields(Product)}
    assert names >= {"id", "date", "link", "name", "category", "price", "subscriber_price",
                     "sizes", "colors", "keywords", "season", "body", "stale"}


def test_post_and_faq_defaults():
    p = Post(id=1, date="2026-09-10T14:02:00", link="https://t.me/status_dokon/1", caption="x")
    assert p.has_media is True
    f = FaqEntry(ts="2026-09-16T10:00:00", question="dastavka?", answer="35 ming")
    assert f.post_ids == ()
