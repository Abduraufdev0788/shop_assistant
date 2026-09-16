"""Embed products with Voyage, persist matrix. SDD §3.3, FR-5/6. Ticket #6."""
from shop_assistant.models import Product


def product_text(p: Product) -> str:
    """Text that gets embedded: name + ' ' + body + ' ' + ' '.join(keywords)."""
    raise NotImplementedError("ticket #6")


def embed(texts: list[str], input_type: str = "document"):
    """Voyage embeddings, batches of config.EMBED_BATCH → float32[N, D] ndarray."""
    raise NotImplementedError("ticket #6")


def reindex() -> int:
    """Rewrite embeddings.npy + embeddings_ids.json for all products (D-4). Returns N."""
    raise NotImplementedError("ticket #6")


def reindex_faq() -> int:
    """Same for faq.jsonl → faq_embeddings.npy (R2, ticket #16)."""
    raise NotImplementedError("ticket #16")


if __name__ == "__main__":
    print(reindex())
