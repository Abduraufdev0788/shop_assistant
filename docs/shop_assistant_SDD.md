# Software Design Description — Shop Assistant

Version 0.2 · 2026-09-16 · Status: draft · Implements: shop_assistant_SRS.md v0.3

## 1. Overview

Six stages, one Python module each, every module runnable on its own (NFR-7). Data flows left to right through files on disk; the bot process only reads them.

```
 offline (ingest, run by admin)                       online (bot service)
 ─────────────────────────────                        ────────────────────
 @status_dokon                                        customer ⇄ Telegram bot
      │ fetch.py (Telethon, user account)                        │
      ▼                                                          ▼ bot.py
 data/posts.jsonl        raw captions                      agent.py  (Claude, Tool Runner)
      │ extract.py (Claude)                                     │ tools.py
      ▼                                                         ├─ find_products ─┐
 data/products.jsonl     structured records ◀───────────────────┤                 │ search.py
      │ index.py (Voyage)                                       ├─ semantic_search┘
      ▼                                                         ├─ latest_posts
 data/embeddings.npy + data/embeddings_ids.json ◀───────────────┤
                                                                ├─ search_faq ──▶ data/faq.jsonl
                                                                └─ ask_owner ───▶ owner (same bot) ──reply──▶ customer
```

### 1.1 Technology
| Concern | Choice | Why |
|---|---|---|
| Language | Python 3.11+ | same as the rest of the repo |
| Telegram, channel history | Telethon **user account** | bots cannot read channel history; session pattern reused from `telegram_digest/tgclient.py` |
| Telegram, customers + owner | Telethon **bot account** (BotFather token) | customers must not talk to a personal account; bot can message the owner; pattern from `telegram_digest/approval.py` |
| LLM | Anthropic SDK, `client.beta.messages.tool_runner` | same agent loop as `telegram_digest/agent.py` and `course/09_tool_runner.py` |
| Embeddings | Voyage `voyage-multilingual-2` (or current multilingual model), via `voyageai` SDK | C-2 |
| Vector store | `numpy` array + cosine similarity | ≤ a few thousand posts; a DB adds nothing to learn yet |
| Storage | JSONL files under `data/` | greppable, diffable, restart-safe (FR-6) |
| Secrets | `.env` via `python-dotenv` | NFR-6 |
| Deploy | rsync + user-level systemd, copy of `telegram_digest/deploy.sh` | NFR-5, C-3 |

## 2. Data Model

All files live in `shop_assistant/data/` (gitignored). One JSON object per line.

### 2.1 `posts.jsonl` — raw, written by fetch.py
```json
{"id": 1234, "date": "2026-09-10T14:02:00", "link": "https://t.me/status_dokon/1234",
 "caption": "🍂Kuz mavsumi uchun🍂\n🔥Yangi model Dvoyka🔥\nRazmer:M.L.XL.2XL.3XL\nNarx:980.000ming\n...",
 "has_media": true}
```

### 2.2 `products.jsonl` — one record per post, written by extract.py
```json
{"id": 1234, "date": "2026-09-10", "link": "https://t.me/status_dokon/1234",
 "name": "Dvoyka", "category": "kiyim",
 "price": 980000, "subscriber_price": null,
 "sizes": ["M","L","XL","2XL","3XL"], "colors": [],
 "keywords": ["dvoyka","двойка","костюм двойка","two-piece set","sport kostyum"],
 "season": "kuz", "body": "Yangi model Dvoyka Razmer M L XL 2XL 3XL"}
```
- `category` ∈ fixed list: `kiyim`, `poyabzal`, `aksessuar`, `boshqa` (extend when the channel shows more).
- `body` = caption with footer (FR-3a) and emoji stripped; this is the text that gets embedded.
- `keywords` are produced by Claude in four scripts/languages (FR-4) and stored already **normalised** (§4.2).

### 2.3 `embeddings.npy` + `embeddings_ids.json`
`float32[N, D]` matrix, row *i* belongs to post `ids[i]`. Both rewritten together by index.py.

### 2.4 `faq.jsonl` — owner answers, appended by bot.py (FR-22)
```json
{"ts": "...", "question": "dastavka Samarqandga qancha?", "answer": "35 ming, 2 kun", "post_ids": [1234]}
```
FAQ entries are embedded too (separate `faq_embeddings.npy`), so `search_faq` is semantic.

### 2.5 `state.json`
`{"last_post_id": 1234, "last_index_at": "..."}` — drives incremental ingestion (FR-7) and `/stats` (FR-26).

### 2.6 `log.jsonl` — one line per customer turn (FR-25)
`{"ts", "chat_id", "question", "tools": [{"name", "input", "n_results"}], "answer", "escalated": bool, "ms", "usd"}`

## 3. Components

### 3.1 `fetch.py` — FR-1, FR-2, FR-3, FR-7
- `fetch(channel, min_id, limit=500) -> list[Post]` via `tg.iter_messages(channel, min_id=min_id, limit=limit)`.
- Skip empty captions. Dedup on `normalise(caption)` keeping the newest id.
- Append to `posts.jsonl`, update `state.last_post_id`.
- CLI: `python -m shop_assistant.fetch [--full]`.

### 3.2 `extract.py` — FR-3a, FR-3b, FR-4
- `strip_footer(caption) -> body`: drop lines matching phone / `@handle` / `📍` / delivery boilerplate; strip emoji.
- `extract(body) -> Product` — one Claude call with a JSON schema (tool-use with a single `record_product` tool, forced) so the output is always valid. Prompt gives the fixed category list, price notation examples (`980.000ming` → 980000), and asks for keywords in uz-Latin, uz-Cyrillic, ru, en.
- Batches of 10 posts per call to keep NFR-3.
- CLI: `python -m shop_assistant.extract` processes posts not yet in `products.jsonl`.

### 3.3 `index.py` — FR-5, FR-6
- `embed(texts: list[str]) -> np.ndarray` — Voyage, `input_type="document"`, batches of 128.
- Embeds `name + " " + body + " " + " ".join(keywords)` per product; rewrites `embeddings.npy` / `embeddings_ids.json` for all products (cheap at this size; simpler than patching rows).
- Same for `faq.jsonl` → `faq_embeddings.npy`.
- CLI: `python -m shop_assistant.index`.

### 3.4 `textnorm.py` — FR-9
- `normalise(s) -> str`: lowercase → Cyrillic→Latin transliteration table (uz + ru letters) → `oʻ o' o` / `gʻ g' g` / `ў o` / `ғ g` / `ҳ h` / `қ q` folded → collapse whitespace.
- Used on keywords at extract time and on customer filter values at search time, so `krossovka`, `кроссовка`, `Krossovka` all match.

### 3.5 `search.py` — FR-8, FR-10, FR-11, FR-12
```python
def find_products(category=None, min_price=None, max_price=None, size=None, color=None, keywords=None, limit=5) -> list[Product]
def semantic_search(text, max_price=None, limit=5) -> list[Product]     # Voyage query embedding, cosine, then price filter
def latest_posts(n=5) -> list[Product]
def search_faq(text, limit=3) -> list[FaqEntry]
```
- Filters are ANDed; `keywords` matches if **any** normalised customer keyword is a substring of any normalised product keyword or of `normalise(name)`.
- Every returned product carries `link`, `date`, and `stale: bool` (`date` older than `config.STALE_DAYS = 60`, FR-16).
- Loads `products.jsonl` + `.npy` once at import; `reload()` for the admin re-index command.
- CLI: `python -m shop_assistant.search "krosovka 42"` prints both filter and semantic results (FR-24).

### 3.6 `tools.py` — the agent's interface
Thin `@beta_tool` wrappers around §3.5 that return compact text (one line per product: `name · price · sizes · date · link · [eskirgan]`), plus:
- `ask_owner(question: str, post_ids: list[int]) -> str` — calls `bot.escalate(...)` through `run_coroutine_threadsafe` (same thread-bridge as `tgclient.run`). Returns `"forwarded"`.

### 3.7 `agent.py` — FR-13…FR-18, FR-20
- `run_agent(chat_id, text) -> str`, blocking, run in a worker thread.
- Per-customer history: `dict[chat_id, list[message]]`, last 10 turns, in memory only (FR-17, NFR-4).
- System prompt (rules, kept short):
  1. Answer in the customer's language and script.
  2. First `find_products`; if empty and the question has a descriptive part, `semantic_search`. For delivery/payment/other shop questions, `search_faq`.
  3. Never state price, size or availability not in tool output. Never guess stock.
  4. Escalate with `ask_owner` when: stock/availability asked, nothing relevant found, or question is outside the catalog.
  5. Max 5 products per reply; if more, ask the customer to narrow down. Always include links. Mark stale posts with the "may be sold out" note.
- `max_iterations=8`, `max_tokens=1024`, model `claude-sonnet-5` (NFR-1/NFR-2; Opus only if eval demands it).

### 3.8 `bot.py` — FR-19, FR-21, FR-22, FR-26, C-5
- One Telethon bot client. Handlers:
  - `NewMessage(incoming, is_private, sender != owner)` → `asyncio.to_thread(run_agent, chat_id, text)` → reply. Groups are ignored (C-5).
  - `escalate(customer_id, question, post_ids)` → message to `TG_OWNER_ID`: `"#esc <customer_id>\n<question>\n<links>"`. Tells the customer "Egasi tez orada javob beradi".
  - `NewMessage` from owner **that is a reply** to an `#esc` message → parse `customer_id` from the quoted text → forward owner's text to the customer → append to `faq.jsonl` → `index.reindex_faq()`.
  - `/stats` from owner only → counts from `state.json` and today's `log.jsonl`.
- Logs every turn to `log.jsonl` (FR-25).

### 3.9 `config.py`
`CHANNEL = "status_dokon"`, `STALE_DAYS = 60`, `MAX_RESULTS = 5`, `CATEGORIES = [...]`, `FETCH_LIMIT = 500`, model names, paths. Secrets from env: `TG_API_ID`, `TG_API_HASH`, `TG_BOT_TOKEN`, `TG_OWNER_ID`, `ANTHROPIC_API_KEY`, `VOYAGE_API_KEY`.

### 3.10 `main.py`
Loads `.env`, starts the bot, runs forever. Ingestion is **not** in the service: admin runs `fetch → extract → index` by hand or cron (FR-23), then sends `/reindex` to the bot (calls `search.reload()`).

## 4. Key Design Decisions

| # | Decision | Alternative rejected | Reason |
|---|---|---|---|
| D-1 | Filters first, embeddings as fallback | embeddings only | numbers (size 42, ≤ 200k) embed badly; also the teaching point of the project |
| D-2 | Structured extraction with forced tool-use JSON | regex on captions | template drifts; Claude handles "980.000ming", "Telegram obunachilariga narx", missing lines |
| D-3 | Normalise scripts at index *and* query time | fuzzy matching at query time | one cheap deterministic function, testable in isolation |
| D-4 | Rewrite the whole embedding matrix on index | patch rows | N is small; correctness over cleverness |
| D-5 | Owner replies via Telegram "reply to" the escalation message | inline buttons / commands | zero UI to build; the quoted `#esc <id>` header carries the routing |
| D-6 | Conversation history in memory only | persist per customer | NFR-4 privacy; restart loses only the current chat context |
| D-7 | Ingestion outside the bot process | live `on_channel_post` handler | keeps the service simple; live updates are a v2 item |

## 5. Module Layout

```
shop_assistant/                   # repo root; run everything from here
  docs/shop_assistant_SRS.md, shop_assistant_SDD.md
  shop_assistant/                 # the package: `python -m shop_assistant.fetch`
    config.py  models.py  textnorm.py  fetch.py  extract.py  index.py  search.py
    tools.py   agent.py   bot.py      main.py
  eval/questions.jsonl        # 20 questions, expected: {"posts":[ids]} or {"escalate":true}
  eval/run_eval.py            # runs agent offline (ask_owner stubbed), prints AC-2..AC-4
  tests/                      # one file per module; stubs are xfail(strict) until their ticket lands
  pytest.ini                  # xfail_strict = true
  data/  session/             # gitignored
  requirements.txt  .env.example  deploy.sh  shop-assistant.service
```

## 6. Traceability

| Requirement | Component |
|---|---|
| FR-1, 2, 3, 7 | fetch.py |
| FR-3a, 3b, 4 | extract.py |
| FR-5, 6 | index.py |
| FR-8, 9, 10, 11, 12 | search.py, textnorm.py |
| FR-13–18, 20 | agent.py (system prompt + history) |
| FR-19, 21, 22 | bot.py `escalate` + owner-reply handler, tools.ask_owner |
| FR-23, 24 | CLIs of fetch/extract/index/search |
| FR-25, 26 | bot.py logging, `/stats` |
| NFR-1, 2 | Sonnet, max_iterations=8, compact tool output |
| NFR-3 | extract batching (10/call), Voyage batching (128) |
| NFR-4 | in-memory history, log stores question text only |
| NFR-5 | systemd `Restart=always` |
| NFR-6 | `.env`, `data/` and `session/` gitignored |
| NFR-7 | one module per stage, each with `__main__` |
| AC-1–4 | eval/ |
| AC-5 | manual test with owner account |
| AC-6 | restart service, confirm `search.py` loads from disk without network |

## 7. Risks
- Voyage rate limits on first full index → batch + retry with backoff.
- Category list too narrow → `boshqa` bucket; review after first extract run.
- Customer sends a photo/voice only → agent gets `<media>`; reply asking for text (v1), photo search is out of scope.
- Owner forgets to *reply* to the `#esc` message → bot answers the owner with a hint.

## 8. Change Log
| Version | Date | Change |
|---|---|---|
| 0.1 | 2026-09-16 | Initial design against SRS v0.3 |
| 0.2 | 2026-09-16 | §5: code lives in a `shop_assistant/` package (so `python -m shop_assistant.x` works from repo root); `models.py` holds Post/Product/FaqEntry; scaffolding + strict-xfail tests for tickets 1–15 |
