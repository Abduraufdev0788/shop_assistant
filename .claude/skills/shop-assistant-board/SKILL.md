---
name: shop-assistant-board
description: Use when working in the shop_assistant repo and the user asks "what's next", "what should I do now", "show the board", "mark ticket X done", "what's left for MVP", or wants to add/re-order tickets. Holds the Notion board ids, schema, ready-made queries and the planning decisions behind the Shop Assistant sprint board so a later session does not undo them.
---

# Shop Assistant — sprint board

The backlog for `shop_assistant/` lives in Notion. Follow `Order` top to bottom and you are always unblocked.

## Ids (verify with `notion-fetch` if a call fails)

| Thing | Value |
|---|---|
| Project page | `3ddb8d1c-364a-814b-9002-fc1e5ee85282` — https://app.notion.com/p/3ddb8d1c364a814b9002fc1e5ee85282 |
| SRS sub-page | `3ddb8d1c-364a-81da-95c0-eeefb6ae7e72` (digest; source of truth is `shop_assistant/docs/shop_assistant_SRS.md`) |
| SDD sub-page | `3ddb8d1c-364a-8109-ba7a-c5c77e23104d` (digest; source is `shop_assistant/docs/shop_assistant_SDD.md`) |
| Board database | `96fa75417b274b1395abe219e3bd5c3b` — https://app.notion.com/p/96fa75417b274b1395abe219e3bd5c3b |
| Data source | `collection://c386dd00-19e7-4a53-9944-9b692e9a89da` — what queries take |
| Views | Do Next `view://3ddb8d1c-364a-81f9-aee7-000c5bc40eba` · By Sprint `…81a3-9199-000ce26b364f` · MVP Board `…81b4-80ba-000ce4079ce2` · By Epic `…811e-a087-000c79c5549a` |

## Schema

`Name` title · `Order` number (dependency sequence, primary sort) · `Sprint` S1/S2/S3/R2 backlog · `Release` MVP/R2 · `Status` To Do/In Progress/Done · `Epic` E1 Setup/E2 Ingest/E3 Search/E4 Agent/E5 Bot/E6 Eval & Deploy · `Est (days)` · `Req` FR/NFR/AC ids · `Blocks` plain words · `Description` one line · `Owner` Sanjar/Abdurauf/Artur · `Track` A Search/B Ingest/C Agent/Bot.

Ticket body (junior-ready, since 2026-09-16): `## Scope` (Goal, Needs, Files you touch) · `## Steps` (numbered, each with a command + expected output, code patterns inlined — juniors have no access to `telegram_digest`) · `## Acceptance criteria` · `## Prompt for your agent` (paste-ready) · `## Notes / Watch out`. Shared rules live in `docs/WORKFLOW.md` in the repo. New tickets must follow this body.

## Queries (`notion-query-data-sources`, SQL mode, table = the data source url)

What's next:
```sql
SELECT "Order", "Name", "Epic", "Est (days)", "Req" FROM "collection://c386dd00-19e7-4a53-9944-9b692e9a89da"
WHERE "Release" = 'MVP' AND "Status" != 'Done' ORDER BY "Order" LIMIT 3
```
What's next for one person: add `AND "Owner" = 'Artur'`.
MVP progress:
```sql
SELECT "Status", COUNT(*) n, SUM("Est (days)") days FROM "collection://c386dd00-19e7-4a53-9944-9b692e9a89da"
WHERE "Release" = 'MVP' GROUP BY "Status"
```
Mark done: `notion-update-page` with `command: update_properties`, `properties: {"Status": "Done"}` on the ticket page id (get it from `SELECT url, "Name" … WHERE "Order" = N`).

Insert a ticket between 7 and 8: create with `Order` 7.5 — never renumber the rest.

## Decisions behind the plan (do not undo silently)

- **Order 2 is the gating ticket** — Product schema + `textnorm` are frozen first because extract, index, search and eval fixtures all depend on them; changing later means re-extracting every post.
- **Order 3 (Voyage spike) sits before any code that uses embeddings** — it is the only external dependency, and its cross-script sanity check (кроссовки ≈ krossovka) validates design decision D-3. If it fails, revisit SDD before ticket 5.
- **Filters first, semantic fallback** (SDD D-1) — tickets 7 then 8, in that order; the misses from 7 become the semantic-only eval questions in 11.
- **Eval questions (11) are written before agent.py (10) is finished** — otherwise they get biased toward what already passes.
- **R2 = FR-22 FAQ store, FR-26 /stats + /reindex, cron ingestion** — the user agreed on 2026-09-16 to defer them; MVP must still pass AC-1…AC-6 without them.
- **Three juniors since 2026-09-16, each with an AI agent** — `Owner` + `Track` columns added. Tracks run in parallel because every module already exists as a stub with SDD signatures and strict-xfail tests (commit `fad4eb4`):
  - A Search — Sanjar: 2 → 7 → 8 → 9
  - B Ingest — Abdurauf: 3 → 4 → 5 → 6
  - C Agent/Bot — Artur: 10 → 11 → 12 → 13 → 14 → 15 (10 starts against stubs; 12 needs 7/8 + data)
  Cross-track handoffs written into the tickets: #13 needs `agent.last_run` from #10; #9 adds a one-line `escalate_sync` stub to bot.py for #14.
- **Ticket 1 is Done** (scaffolding commit). Stubs raise `NotImplementedError("ticket #N")`; tests are `xfail(strict)` — a ticket is done when its markers are removed and the suite is green.

## When a ticket is finished

1. Set `Status = Done` in Notion.
2. If the work changed a requirement or design decision, update the repo doc (SRS/SDD change log) first, then the Notion digest page.
3. Run the "What's next" query and tell the user the next ticket's name, estimate and its *Notes / Watch out* section.
