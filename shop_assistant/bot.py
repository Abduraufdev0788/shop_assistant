"""Telethon bot: customer handler, escalation, owner relay, logging. SDD §3.8. Tickets #13, #14."""

ESC_PREFIX = "#esc"


def log_turn(chat_id: int, question: str, tools: list[dict], answer: str,
             escalated: bool, ms: int, usd: float) -> dict:
    """Build + append one log.jsonl line (SDD §2.6, FR-25). Returns the record."""
    raise NotImplementedError("ticket #13")


def should_handle(is_private: bool, sender_id: int, owner_id: int) -> bool:
    """Customers only: private chat and not the owner (C-5)."""
    raise NotImplementedError("ticket #13")


async def handle_customer(event) -> None:
    """to_thread(run_agent) → reply; log the turn."""
    raise NotImplementedError("ticket #13")


def format_escalation(customer_id: int, question: str, links: list[str]) -> str:
    """'#esc <customer_id>\\n<question>\\n<links>' — header is the routing key (D-5)."""
    raise NotImplementedError("ticket #14")


def parse_esc_header(text: str) -> int | None:
    """customer_id from a quoted '#esc <id>' message; None when the owner did not reply to one."""
    raise NotImplementedError("ticket #14")


async def escalate(customer_id: int, question: str, post_ids: list[int]) -> None:
    """Message the owner; tell the customer 'Egasi tez orada javob beradi' (FR-19)."""
    raise NotImplementedError("ticket #14")


async def handle_owner_reply(event) -> None:
    """Owner reply-to '#esc' → forward text to the customer (FR-21); hint if not a reply."""
    raise NotImplementedError("ticket #14")


def run() -> None:
    """Start the bot client and register handlers."""
    raise NotImplementedError("ticket #15")
