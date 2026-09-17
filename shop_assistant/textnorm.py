"""Script/case/diacritic folding. SDD §3.4, FR-9. Ticket #2."""

CYRILLIC_TO_LATIN = {
    "а": "a",
    "б": "b",
    "в": "v",
    "г": "g",
    "д": "d",
    "е": "e",
    "ё": "yo",
    "ж": "j",
    "з": "z",
    "и": "i",
    "й": "y",
    "к": "k",
    "л": "l",
    "м": "m",
    "н": "n",
    "о": "o",
    "п": "p",
    "р": "r",
    "с": "s",
    "т": "t",
    "у": "u",
    "ф": "f",
    "х": "x",
    "ц": "ts",
    "ч": "ch",
    "ш": "sh",
    "щ": "sh",
    "ъ": "",
    "ы": "y",
    "ь": "",
    "э": "e",
    "ю": "yu",
    "я": "ya",
    "ў": "o",
    "ғ": "g",
    "ҳ": "h",
    "қ": "q",
}

_TRANS_TABLE = str.maketrans(CYRILLIC_TO_LATIN)
_APOSTROPHES = ("ʻ", "'", "ʼ", "’", "‘", "`", "´")


def normalise(s: str) -> str:
    """lowercase → Cyrillic→Latin (uz + ru) → fold oʻ/o'/ў→o, gʻ/g'/ғ→g, ҳ→h, қ→q → collapse whitespace.

    `krossovka`, `кроссовка`, `Krossovka` must all map to the same string.
    """
    s = s.lower().translate(_TRANS_TABLE)
    for apo in _APOSTROPHES:
        s = s.replace("o" + apo, "o").replace("g" + apo, "g")
    return " ".join(s.split())
