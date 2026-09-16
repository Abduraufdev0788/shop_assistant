"""Run the agent offline over eval/questions.jsonl and print AC-2..AC-4. Ticket #12.

Each line of questions.jsonl: {"q": "...", "expected": {"posts": [ids]} | {"escalate": true}}
"""


def load_questions(path) -> list[dict]:
    raise NotImplementedError("ticket #12")


def contains_invented_numbers(answer: str, products: list) -> bool:
    """True when the reply states a price or size not present in the referenced records (AC-3, FR-15)."""
    raise NotImplementedError("ticket #12")


def score(results: list[dict]) -> dict:
    """results: [{"expected": ..., "posts": [ids], "escalated": bool, "invented": bool, "semantic_only": bool}]
    → {"ac2": n_correct, "ac3": n_invented, "ac4": n_semantic_only, "total": n}."""
    raise NotImplementedError("ticket #12")


def main() -> None:
    raise NotImplementedError("ticket #12")


if __name__ == "__main__":
    main()
