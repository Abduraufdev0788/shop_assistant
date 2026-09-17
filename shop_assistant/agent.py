"""Tool Runner agent (Anthropic SDK → Ollama) + per-customer history. SDD §3.7, FR-13…18/20. Ticket #10."""

SYSTEM_PROMPT = ""   # written in ticket #10 (SDD §3.7 rules 1–5)


class History:
    """Per-customer message history, last config.HISTORY_TURNS turns, in memory only (FR-17, NFR-4)."""

    def __init__(self, max_turns: int = 10) -> None:
        self.max_turns = max_turns
        self._chats: dict[int, list[dict]] = {}

    def get(self, chat_id: int) -> list[dict]:
        raise NotImplementedError("ticket #10")

    def append(self, chat_id: int, role: str, content) -> None:
        """Append and trim so at most max_turns user/assistant pairs remain."""
        raise NotImplementedError("ticket #10")

    def clear(self, chat_id: int) -> None:
        raise NotImplementedError("ticket #10")


def run_agent(chat_id: int, text: str, history: History | None = None) -> str:
    """Blocking. tool_runner with TOOLS, max_iterations=8, max_tokens=1024. Returns final reply text."""
    raise NotImplementedError("ticket #10")


if __name__ == "__main__":
    import sys
    print(run_agent(0, " ".join(sys.argv[1:])))
