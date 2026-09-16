"""Script/case/diacritic folding. SDD §3.4, FR-9. Ticket #2."""


def normalise(s: str) -> str:
    """lowercase → Cyrillic→Latin (uz + ru) → fold oʻ/o'/ў→o, gʻ/g'/ғ→g, ҳ→h, қ→q → collapse whitespace.

    `krossovka`, `кроссовка`, `Krossovka` must all map to the same string.
    """
    raise NotImplementedError("ticket #2")
