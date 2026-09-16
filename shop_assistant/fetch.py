"""Dump channel posts to posts.jsonl. SDD §3.1, FR-1/2/3/7/23. Ticket #4."""
from shop_assistant.models import Post


def dedup(posts: list[Post]) -> list[Post]:
    """Drop empty captions (FR-2); among posts with equal normalise(caption) keep the newest id (FR-3)."""
    raise NotImplementedError("ticket #4")


def fetch(channel: str, min_id: int = 0, limit: int = 500) -> list[Post]:
    """Telethon user account, iter_messages(channel, min_id, limit) → Post list, already dedup'ed."""
    raise NotImplementedError("ticket #4")


def main(full: bool = False) -> None:
    """CLI: append new posts to posts.jsonl and update state.last_post_id (FR-7)."""
    raise NotImplementedError("ticket #4")


if __name__ == "__main__":
    import sys
    main(full="--full" in sys.argv)
