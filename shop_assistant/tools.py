"""@beta_tool wrappers with compact text output. SDD §3.6, FR-11, NFR-2. Ticket #9."""
from shop_assistant.models import Product


def format_product(p: Product) -> str:
    """One line: `name · price · sizes · date · link · [eskirgan]` (last tag only when stale)."""
    raise NotImplementedError("ticket #9")


def find_products_tool(category: str | None = None, min_price: int | None = None,
                       max_price: int | None = None, size: str | None = None,
                       color: str | None = None, keywords: list[str] | None = None) -> str:
    """search.find_products → one line per product, or 'no results'."""
    raise NotImplementedError("ticket #9")


def semantic_search_tool(text: str, max_price: int | None = None) -> str:
    raise NotImplementedError("ticket #9")


def latest_posts_tool(n: int = 5) -> str:
    raise NotImplementedError("ticket #9")


def search_faq_tool(text: str) -> str:
    raise NotImplementedError("ticket #9")


def ask_owner(question: str, post_ids: list[int]) -> str:
    """bot.escalate via run_coroutine_threadsafe; returns 'forwarded'."""
    raise NotImplementedError("ticket #9")


TOOLS: list = []   # filled with @beta_tool-decorated callables in ticket #9
