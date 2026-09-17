"""Real captions from @status_dokon (SDD §2.1) as fixtures. Never 'foo'."""
import pytest

from shop_assistant.models import Post, Product

FOOTER = "\n\n📍Manzil: Samarqand, Siyob bozori\n📞 +998 90 123 45 67\n@status_dokon\n🚚 Dastavka bor"

CAPTION_DVOYKA = (
    "🍂Kuz mavsumi uchun🍂\n🔥Yangi model Dvoyka🔥\nRazmer:M.L.XL.2XL.3XL\nNarx:980.000ming" + FOOTER
)
CAPTION_KROSSOVKA = (
    "👟Krossovka Nike Air👟\nRazmer: 40 41 42 43\nNarx: 350.000\n"
    "Telegram obunachilariga narx: 320.000" + FOOTER
)
CAPTION_KURTKA = "🧥Qishki kurtka\nRang: qora, kok\nRazmer: L XL\nNarx: 1.200.000" + FOOTER

@pytest.fixture
def posts() -> list[Post]:
    return [
        Post(id=1234, date="2026-09-10T14:02:00", link="https://t.me/status_dokon/1234",
             caption=CAPTION_DVOYKA),
        Post(id=1300, date="2026-09-12T10:00:00", link="https://t.me/status_dokon/1300",
             caption=CAPTION_KROSSOVKA),
        Post(id=1301, date="2026-09-13T09:00:00", link="https://t.me/status_dokon/1301",
             caption=CAPTION_DVOYKA),      # repost of 1234 — FR-3 keeps this one
        Post(id=1302, date="2026-09-13T09:05:00", link="https://t.me/status_dokon/1302",
             caption=""),                  # FR-2 skipped
    ]


@pytest.fixture
def products() -> list[Product]:
    return [
        Product(id=1234, date="2026-09-10", link="https://t.me/status_dokon/1234",
                name="Dvoyka", category="kiyim", price=980000, subscriber_price=None,
                sizes=("M", "L", "XL", "2XL", "3XL"), colors=(),
                keywords=("dvoyka", "dvoyka", "kostyum dvoyka", "two-piece set", "sport kostyum"),
                season="kuz", body="Yangi model Dvoyka Razmer M L XL 2XL 3XL"),
        Product(id=1300, date="2026-09-12", link="https://t.me/status_dokon/1300",
                name="Krossovka Nike Air", category="poyabzal", price=350000, subscriber_price=320000,
                sizes=("40", "41", "42", "43"), colors=(),
                keywords=("krossovka", "krossovki", "sneakers", "nike"),
                body="Krossovka Nike Air Razmer 40 41 42 43"),
        Product(id=900, date="2026-06-01", link="https://t.me/status_dokon/900",
                name="Qishki kurtka", category="kiyim", price=1200000, subscriber_price=None,
                sizes=("L", "XL"), colors=("qora", "kok"),
                keywords=("kurtka", "kurtka", "jacket", "qishki kurtka"),
                season="qish", body="Qishki kurtka Rang qora kok Razmer L XL"),   # > 60 days → stale
    ]
