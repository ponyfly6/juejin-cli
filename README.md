# juejin-cli

A terminal-first CLI for Juejin.

Current `v0.1` scope:

- list article categories
- browse category feeds
- search articles
- read an article by URL, article ID, or short index
- export article content as Markdown

## Install

```bash
uv sync
uv run juejin --help
```

## Usage

```bash
# Categories
juejin categories

# Feed
juejin feed --category backend --limit 5
juejin feed --category ai --json

# Search
juejin search "python" --limit 5
juejin search "python" --sort newest --yaml
juejin search "python" --limit 3

# Read by article ID, full URL, or short index from the latest list output
juejin read 7540497727161417766
juejin read https://juejin.cn/post/7540497727161417766
juejin read 1

# Export as Markdown
juejin export-md 7540497727161417766 -o article.md
```

Pagination:

- `feed` and `search` print a `next cursor` when more results are available
- reuse it with `--cursor <value>` to continue
- `read 1` and `export-md 1` resolve against the latest `feed` or `search` result list
