---
name: juejin-cli
description: Use the local `juejin` CLI to browse current Juejin categories, feeds, hot boards, search results, user posts, and article content. Use when an agent should query Juejin through the installed CLI instead of scraping the website manually.
---

# Juejin CLI

Use this skill when the task is about reading or querying Juejin content with the local CLI.

## Preconditions

- Prefer `uv run juejin ...` when working inside the `juejin-cli` repo.
- If the CLI is installed globally, `juejin ...` is fine.
- Verify availability with `uv run juejin --help` or `juejin --help`.
- If neither works, tell the user the local CLI is unavailable.

## Workflow

1. Prefer `--json` for agent-readable output.
2. Start from the list commands:
   - `categories`
   - `feed`
   - `recommended`
   - `hot`
   - `hot-columns`
   - `hot-collections`
   - `hot-authors`
   - `search`
   - `user-posts`
3. Use `read` and `export-md` only for articles.
4. `read 1` and `export-md 1` work only after an article list command has populated the short index cache.
5. Do not invent write features. The CLI currently has no login, draft, or publish support.

For command routing and examples, read [references/commands.md](references/commands.md).

## Guardrails

- Treat Juejin results as live data. Re-run commands instead of relying on memory.
- `hot-columns`, `hot-collections`, and `hot-authors` are ranking views only; they do not feed `read 1`.
- When the user asks to inspect a specific article from a list, prefer the returned `article_id` or the saved short index.
