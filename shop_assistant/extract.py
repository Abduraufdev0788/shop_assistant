"""Footer strip + Claude structured extraction. SDD §3.2, FR-3a/3b/4. Ticket #5."""
from shop_assistant.models import Post, Product


def strip_footer(caption: str) -> str:
    """Drop lines with phone / @handle / 📍 / delivery boilerplate; strip emoji; collapse blank lines (FR-3a)."""
    raise NotImplementedError("ticket #5")


def parse_price(s: str) -> int | None:
    """Shop notation → so'm: '980.000ming' → 980000, '1.200.000' → 1200000, 'narxi so'rang' → None (FR-3b)."""
    raise NotImplementedError("ticket #5")


def extract(post: Post) -> Product:
    """One forced tool-use call (`record_product`) → Product. Keywords in uz-Latin/uz-Cyrillic/ru/en, normalised (FR-4)."""
    raise NotImplementedError("ticket #5")


def extract_batch(posts: list[Post]) -> list[Product]:
    """Batches of config.EXTRACT_BATCH per call (NFR-3)."""
    raise NotImplementedError("ticket #5")


def main() -> None:
    """CLI: process posts not yet in products.jsonl."""
    raise NotImplementedError("ticket #5")


if __name__ == "__main__":
    main()
