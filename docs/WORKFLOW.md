# How to work a ticket

Every ticket on the Notion board follows the same loop. Read this once; each ticket repeats only the parts that differ.

## 0. One-time setup
```bash
git clone <repo-url> shop_assistant && cd shop_assistant
uv venv && uv pip install -r requirements.txt
cp .env.example .env            # fill only the keys your ticket lists; ask Sanjar for values
uv run pytest -q                # expect: N passed, M xfailed, 0 failed
```
Never commit `.env`, `data/`, `session/` (already gitignored).

## 1. Pick up
- Board → "Do Next" view → your Owner. Take the lowest `Order` that is `To Do` and whose "Needs" tickets are `Done`.
- Set `Status = In Progress`.
- `git switch -c t<Order>-<short-name>` from `main` (e.g. `t7-find-products`).

## 2. Build
- The functions already exist as stubs that `raise NotImplementedError("ticket #N")`. Replace the body; keep the signature and docstring (other tickets call them).
- The tests already exist and are marked `@xfail_stub`. **Do not edit the assertions.** Remove the `@xfail_stub` line from the tests your ticket names and make them pass. If you believe a test is wrong, say so in the PR — do not change it silently.
- Never return a plausible default (`[]`, `0`, `""`) to make a test green.
- Docs: `docs/shop_assistant_SDD.md` (design, §3 = per-module contract) and `docs/shop_assistant_SRS.md` (requirements FR-x / NFR-x / AC-x). The ticket tells you which sections.

## 3. Using your agent (Claude Code / Cursor / etc.)
Paste the ticket's "Prompt for your agent" block. Rules for the agent, always:
- Work only in the files the ticket lists.
- Do not edit `tests/` except removing `@xfail_stub` markers.
- Do not add dependencies not in `requirements.txt` without asking.
- Run `uv run pytest -q` before saying it is done.
Read the diff yourself before committing — you are responsible for it, not the agent.

## 4. Done means
1. `uv run pytest -q` → `0 failed`, and the ticket's tests are no longer xfailed.
2. The ticket's CLI / manual protocol steps (if any) were run and the output pasted into the PR.
3. PR to `main` titled `#<Order> <ticket name>`, body = what you did + test output. Sanjar reviews.
4. After merge: Notion `Status = Done`, tick the acceptance boxes.

## 5. Stuck?
15 minutes without progress → write in the ticket's Notion comments what you tried, ping Sanjar. Do not widen the ticket's scope to work around it.
