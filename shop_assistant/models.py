"""Value types shared by every stage. SDD §2. Ticket #2 (gating)."""
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Post:
    """One raw channel post, as written by fetch.py (SDD §2.1)."""
    id: int
    date: str            # ISO datetime
    link: str
    caption: str
    has_media: bool = True


@dataclass(frozen=True)
class Product:
    """One structured record per post, as written by extract.py (SDD §2.2)."""
    id: int
    date: str            # ISO date
    link: str
    name: str
    category: str
    price: int | None
    subscriber_price: int | None
    sizes: tuple[str, ...] = ()
    colors: tuple[str, ...] = ()
    keywords: tuple[str, ...] = ()     # already normalised (SDD §4.2)
    season: str | None = None
    body: str = ""
    stale: bool = False                # set by search.py (FR-16)


@dataclass(frozen=True)
class FaqEntry:
    """One owner answer, appended by bot.py (SDD §2.4, FR-22 — R2)."""
    ts: str
    question: str
    answer: str
    post_ids: tuple[int, ...] = field(default_factory=tuple)
