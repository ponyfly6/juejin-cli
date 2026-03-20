from __future__ import annotations

import json
import sys
from typing import Any, Dict, Iterable, List

import yaml
from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table

console = Console()


def emit_structured(data: Any, *, as_json: bool, as_yaml: bool) -> bool:
    auto_yaml = not sys.stdout.isatty() and not as_json and not as_yaml
    if not (as_json or as_yaml or auto_yaml):
        return False

    payload = {"ok": True, "schema_version": "1", "data": data}
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return True

    print(yaml.safe_dump(payload, sort_keys=False, allow_unicode=True))
    return True


def render_categories(items: List[Dict[str, Any]]) -> None:
    table = Table(title="Juejin Categories")
    table.add_column("#", justify="right")
    table.add_column("slug")
    table.add_column("name")
    table.add_column("category_id")
    for idx, item in enumerate(items, start=1):
        table.add_row(
            str(idx),
            str(item.get("category_url", "")),
            str(item.get("category_name", "")),
            str(item.get("category_id", "")),
        )
    console.print(table)


def render_article_list(title: str, items: List[Dict[str, Any]]) -> None:
    table = Table(title=title)
    table.add_column("#", justify="right")
    table.add_column("title", overflow="fold")
    table.add_column("author")
    table.add_column("category")
    table.add_column("views", justify="right")
    table.add_column("diggs", justify="right")
    table.add_column("comments", justify="right")
    for idx, item in enumerate(items, start=1):
        table.add_row(
            str(idx),
            str(item.get("title", "")),
            str(item.get("author", "")),
            str(item.get("category", "")),
            str(item.get("views", "")),
            str(item.get("diggs", "")),
            str(item.get("comments", "")),
        )
    console.print(table)


def render_column_list(title: str, items: List[Dict[str, Any]]) -> None:
    table = Table(title=title)
    table.add_column("#", justify="right")
    table.add_column("title", overflow="fold")
    table.add_column("author")
    table.add_column("followers", justify="right")
    table.add_column("articles", justify="right")
    for idx, item in enumerate(items, start=1):
        table.add_row(
            str(idx),
            str(item.get("title", "")),
            str(item.get("author", "")),
            str(item.get("followers", "")),
            str(item.get("articles", "")),
        )
    console.print(table)


def render_collection_list(title: str, items: List[Dict[str, Any]]) -> None:
    table = Table(title=title)
    table.add_column("#", justify="right")
    table.add_column("title", overflow="fold")
    table.add_column("creator")
    table.add_column("followers", justify="right")
    table.add_column("articles", justify="right")
    for idx, item in enumerate(items, start=1):
        table.add_row(
            str(idx),
            str(item.get("title", "")),
            str(item.get("creator", "")),
            str(item.get("followers", "")),
            str(item.get("articles", "")),
        )
    console.print(table)


def render_author_rank_list(title: str, items: List[Dict[str, Any]]) -> None:
    table = Table(title=title)
    table.add_column("#", justify="right")
    table.add_column("author")
    table.add_column("title")
    table.add_column("company")
    table.add_column("followers", justify="right")
    table.add_column("diggs", justify="right")
    table.add_column("hot", justify="right")
    for item in items:
        table.add_row(
            str(item.get("rank", "")),
            str(item.get("user_name", "")),
            str(item.get("job_title", "")),
            str(item.get("company", "")),
            str(item.get("follower_count", "")),
            str(item.get("got_digg_count", "")),
            str(item.get("hot_value", "")),
        )
    console.print(table)


def render_pagination(cursor: str, has_more: bool) -> None:
    if not has_more:
        return
    if cursor:
        console.print(f"next cursor: {cursor}", style="dim")
    else:
        console.print("more results available", style="dim")


def render_article(article: Dict[str, Any]) -> None:
    console.rule(article.get("title", "Untitled"))
    meta_parts = [
        article.get("author", ""),
        article.get("published_at", ""),
        article.get("views", ""),
        article.get("read_time", ""),
        article.get("url", ""),
    ]
    meta = " | ".join(part for part in meta_parts if part)
    if meta:
        console.print(meta, style="dim")
        console.print()
    console.print(Markdown(article.get("markdown", "")))
