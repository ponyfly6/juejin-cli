# Command Map

Prefer `uv run juejin ...` inside this repo. Add `--json` unless the user explicitly wants terminal tables.

## Intent Routing

- List categories:
  - `uv run juejin categories --json`
- Browse a category feed:
  - `uv run juejin feed --category backend --limit 5 --json`
- Browse the homepage recommendations:
  - `uv run juejin recommended --limit 5 --json`
- Browse article hot rankings:
  - `uv run juejin hot --category all --type hot --limit 10 --json`
  - `uv run juejin hot --category backend --type collect --limit 10 --json`
- Browse non-article boards:
  - `uv run juejin hot-columns --limit 10 --json`
  - `uv run juejin hot-collections --limit 10 --json`
  - `uv run juejin hot-authors --category ai --period weekly --limit 10 --json`
- Search articles:
  - `uv run juejin search "agent" --limit 5 --json`
  - `uv run juejin search "agent" --sort newest --limit 5 --json`
- Browse a user's posts:
  - `uv run juejin user-posts 4371313961738616 --limit 5 --json`
- Read an article:
  - `uv run juejin read 1`
  - `uv run juejin read 7540497727161417766 --json`
- Export markdown:
  - `uv run juejin export-md 1 -o article.md`

## Output Notes

- `feed`, `recommended`, `search`, and `user-posts` return `cursor`, `has_more`, and `items`.
- `hot`, `hot-columns`, `hot-collections`, and `hot-authors` return fixed rank lists.
- Article list items usually include:
  - `article_id`
  - `title`
  - `author`
  - `category`
  - `views`
  - `diggs`
  - `comments`
  - `url`
- `hot-authors` also returns:
  - `category`
  - `period`
  - `rank_period`
  - ranked author `items`

## Short Index Cache

- `read 1` and `export-md 1` only work after these commands:
  - `feed`
  - `recommended`
  - `hot`
  - `search`
  - `user-posts`
- Do not expect short-index reading after:
  - `hot-columns`
  - `hot-collections`
  - `hot-authors`
