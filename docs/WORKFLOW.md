# How to work a ticket

Every ticket on the Notion board follows the same loop. Read this once; each ticket repeats only the parts that differ.

## The idea
A senior writes the **tests** for a ticket on a branch and assigns it to you. Your job is to make those tests pass — not to change them. `main` only ever contains finished, tested work, so the test suite on `main` is always green.

## 0. One-time setup
```bash
git clone git@github.com:bhgroupai/shop_assistant.git && cd shop_assistant
uv venv && uv pip install -r requirements.txt
cp .env.example .env            # fill only the keys your ticket lists; ask Sanjarbek for values
# Models run on the Codeschool GPU server (Ollama). In the office: OLLAMA_URL=http://192.168.0.218:11434.
# From home: `ssh -N -L 11434:localhost:11434 codeschool` in a second terminal, keep OLLAMA_URL=http://localhost:11434.
uv run pytest -q                # expect: all passed
```
Never commit `.env`, `data/`, `session/` (already gitignored).

## 1. Pick up
- Board → "Do Next" view → filter by your Owner. Take the lowest `Order` that is `To Do` and whose "Needs" tickets are `Done`. Set `Status = In Progress`.
- The branch already exists: `git fetch && git switch t<Order>-<name>` (e.g. `t7-find-products`). It contains the ticket's tests and nothing else.
- Run them: `uv run pytest tests/<file the ticket names> -q` → **red**, every failure is `NotImplementedError("ticket #N")`. That is your starting point. If you see any other error, stop and tell Sanjarbek.
- Tickets without tests (#3, #11, #15) — create the branch yourself with the same naming.

## 2. Build
- The functions already exist as stubs that `raise NotImplementedError("ticket #N")`. Replace the body; keep the signature and docstring (other tickets call them).
- **Do not edit anything under `tests/`.** CI rejects the PR if you do. If a test looks wrong, write in the ticket's Notion comments what you think is wrong and why — Sanjarbek changes it.
- Never return a plausible default (`[]`, `0`, `""`) just to turn a test green.
- Commit small and often on your branch; `git pull --rebase origin main` daily so you stay close to `main`.
- Docs: `docs/shop_assistant_SDD.md` (§3 = per-module contract) and `docs/shop_assistant_SRS.md` (FR-x / NFR-x / AC-x). The ticket says which sections.

## 3. Using your agent (Claude Code / Cursor / etc.)
Paste the ticket's "Prompt for your agent" block. Rules for the agent, always:
- Work only in the files the ticket lists.
- Never modify `tests/`.
- Do not add dependencies not in `requirements.txt` without asking.
- Run `uv run pytest -q` before saying it is done.
Read the diff yourself before committing — you are responsible for it, not the agent.

## 4. Done means
1. `uv run pytest -q` → **0 failed** (your ticket's tests pass, everything on `main` still passes).
2. The ticket's CLI / manual protocol steps (if any) were run and the output pasted into the PR.
3. PR from your branch to `main`, titled `#<Order> <ticket name>`, using the PR template. CI must be green. Sanjarbek reviews and merges.
4. After merge: Notion `Status = Done`, tick the acceptance boxes, delete the branch.

## 5. Stuck?
15 minutes without progress → write in the ticket's Notion comments what you tried, ping Sanjarbek. Do not widen the ticket's scope to work around it.

## Later
Once the team is comfortable with this loop, tickets will switch to: senior writes 2–3 acceptance tests, **you** add the unit tests for edge cases in your PR. Start thinking about "what would I test here?" now.
