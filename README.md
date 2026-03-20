# juejin-cli

A terminal-first CLI for Juejin.

Current scope:

- list article categories
- browse category feeds
- browse article hot rankings
- browse hot ranked columns
- browse hot ranked collection sets
- browse hot ranked authors
- browse the recommended home feed
- search articles
- list a user's posts
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

# Recommended
juejin recommended --limit 5

# Hot rankings
juejin hot --limit 10
juejin hot --category backend --limit 5
juejin hot --type collect --category all --json
juejin hot-columns --limit 10
juejin hot-collections --limit 10
juejin hot-authors --category ai --period weekly --limit 5
juejin hot-authors --category backend --period monthly --json

# Search
juejin search "python" --limit 5
juejin search "python" --sort newest --yaml
juejin search "python" --limit 3

# User posts
juejin user-posts 4371313961738616
juejin user-posts https://juejin.cn/user/4371313961738616/posts --sort popular

# Read by article ID, full URL, or short index from the latest list output
juejin read 7540497727161417766
juejin read https://juejin.cn/post/7540497727161417766
juejin read 1

# Export as Markdown
juejin export-md 7540497727161417766 -o article.md
```

Pagination:

- `feed`, `recommended`, `search`, and `user-posts` print a `next cursor` when more results are available
- reuse it with `--cursor <value>` to continue
- `hot`, `hot-columns`, `hot-collections`, and `hot-authors` return fixed rank lists and do not use cursor pagination
- `read 1` and `export-md 1` resolve against the latest article list output from `feed`, `hot`, `recommended`, `search`, or `user-posts`

Hot author categories:

- `backend`
- `frontend`
- `client`
- `ai`
- `tools`
- `career`
- `reading`
