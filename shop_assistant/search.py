"""Filter search, semantic fallback, latest, faq. SDD §3.5, FR-8/10/11/12/16/24. Tickets #7, #8."""
from shop_assistant.models import FaqEntry, Product


def is_stale(date: str, today: str, stale_days: int) -> bool:
    """True when `date` (ISO) is more than stale_days before `today` (FR-16)."""
    raise NotImplementedError("ticket #7")


def keyword_match(customer_keywords: list[str], product: Product) -> bool:
    """Any normalised customer keyword is a substring of any product keyword or of normalise(name)."""
    raise NotImplementedError("ticket #7")


def find_products(category: str | None = None, min_price: int | None = None,
                  max_price: int | None = None, size: str | None = None,
                  color: str | None = None, keywords: list[str] | None = None,
                  limit: int = 5, products: list[Product] | None = None) -> list[Product]:
    """ANDed filters over products.jsonl; newest first; each result carries `stale` (FR-8, FR-16)."""
    raise NotImplementedError("ticket #7")


def latest_posts(n: int = 5, products: list[Product] | None = None) -> list[Product]:
    """Most recent n products by date (FR-12)."""
    raise NotImplementedError("ticket #7")


def semantic_search(text: str, max_price: int | None = None, limit: int = 5) -> list[Product]:
    """Ollama query embedding (index.embed), cosine over the matrix, then price filter, top-k (FR-10)."""
    raise NotImplementedError("ticket #8")


def cosine_top_k(query, matrix, k: int) -> list[int]:
    """Indices of the k rows of `matrix` most similar to `query` (pure numpy)."""
    raise NotImplementedError("ticket #8")


def search_faq(text: str, limit: int = 3) -> list[FaqEntry]:
    """Semantic search over faq entries. Stub returns [] until R2 (ticket #16)."""
    raise NotImplementedError("ticket #8")


def reload() -> None:
    """Re-read products.jsonl + .npy from disk (admin /reindex)."""
    raise NotImplementedError("ticket #7")


if __name__ == "__main__":
    import sys
    q = " ".join(sys.argv[1:])
    print(find_products(keywords=q.split()))
    print(semantic_search(q))
