# Shop Assistant

Telegram bot that answers customers' "do you have …?" questions about a shop whose catalog is the posts of a Telegram channel (@status_dokon). Filters first, embeddings as fallback, escalates to the owner when unsure. Built from scratch — no agent/RAG frameworks.

- Requirements: `docs/shop_assistant_SRS.md`
- Design: `docs/shop_assistant_SDD.md`
- Backlog: Notion board (ids in `.claude/skills/shop-assistant-board/`)

## Dev
```
uv venv && uv pip install -r requirements.txt
uv run pytest -q        # stubs are xfail(strict): implementing a ticket turns its tests XPASS → remove the marker
```
