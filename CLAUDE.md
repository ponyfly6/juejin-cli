# Claude Code Notes

Use the local `juejin` CLI instead of scraping Juejin directly when the task is about browsing, searching, or reading Juejin content.

## Preferred Invocation

- From this repo root, run `uv run juejin ...`
- Prefer `--json` for machine-readable output
- Use list commands before article reads:
  - `categories`
  - `feed`
  - `recommended`
  - `hot`
  - `hot-columns`
  - `hot-collections`
  - `hot-authors`
  - `search`
  - `user-posts`

## Article Reading

- `read` and `export-md` only work for articles
- `read 1` and `export-md 1` only work after an article list command has populated the short index cache
- `hot-columns`, `hot-collections`, and `hot-authors` do not populate that cache

## Boundaries

- Current CLI scope is read-only
- Do not assume login, draft, or publish support exists

For examples, see [skills/juejin-cli/references/commands.md](skills/juejin-cli/references/commands.md).
