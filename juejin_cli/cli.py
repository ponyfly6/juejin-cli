from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

import click

from .cache import (
    get_index_item,
    is_local_search_cursor,
    load_search_cursor,
    save_index,
    save_search_cursor,
)
from .client import JuejinCliError, JuejinClient
from .constants import DEFAULT_CATEGORY, DEFAULT_LIMIT, SEARCH_SORTS
from .output import (
    emit_structured,
    render_article,
    render_article_list,
    render_categories,
    render_pagination,
)
from .parser import normalize_feed_items, normalize_search_items, parse_article_html, parse_article_reference


def structured_output_options(func):
    func = click.option("--yaml", "as_yaml", is_flag=True, help="Emit YAML output")(func)
    func = click.option("--json", "as_json", is_flag=True, help="Emit JSON output")(func)
    return func


@click.group()
def cli() -> None:
    """Juejin terminal CLI."""


def _resolve_category(categories: List[Dict[str, Any]], raw: str) -> Dict[str, Any]:
    needle = raw.strip().lower()
    for item in categories:
        if str(item.get("category_id", "")).strip() == raw:
            return item
        if str(item.get("category_url", "")).strip().lower() == needle:
            return item
        if str(item.get("category_name", "")).strip().lower() == needle:
            return item
    raise click.ClickException(f"Unknown category: {raw}")


def _normalize_cursor(raw: str) -> str:
    return raw.strip() or "0"


def _resolve_article_id(reference: str) -> str:
    raw = reference.strip()
    if raw.isdigit() and len(raw) <= 4:
        cached = get_index_item(int(raw))
        if not cached:
            raise click.ClickException(f"No cached article at index {raw}")
        return str(cached["article_id"])
    try:
        return parse_article_reference(raw)
    except ValueError as exc:
        raise click.ClickException(str(exc)) from exc


def _paginate_search_items(
    query: str,
    sort_type: int,
    limit: int,
    items: List[Dict[str, Any]],
    server_cursor: str,
    has_more: bool,
) -> Dict[str, Any]:
    visible = items[:limit]
    buffered = items[limit:]
    next_cursor = ""
    if buffered or has_more:
        next_cursor = save_search_cursor(
            {
                "query": query,
                "sort_type": sort_type,
                "buffer": buffered,
                "server_cursor": server_cursor,
                "has_more": has_more,
            }
        )
    elif server_cursor:
        next_cursor = server_cursor

    return {
        "cursor": next_cursor,
        "has_more": bool(buffered or has_more or server_cursor),
        "items": visible,
    }


def _search_with_cursor(query: str, cursor: str, limit: int, sort_type: int) -> Dict[str, Any]:
    with JuejinClient() as client:
        if is_local_search_cursor(cursor):
            cached = load_search_cursor(cursor)
            if not cached:
                raise click.ClickException(f"Unknown or expired search cursor: {cursor}")
            if str(cached.get("query", "")) != query:
                raise click.ClickException("Local search cursor must be reused with the same query")
            if int(cached.get("sort_type", -1)) != sort_type:
                raise click.ClickException("Local search cursor must be reused with the same sort")

            items = list(cached.get("buffer") or [])
            server_cursor = str(cached.get("server_cursor") or "").strip()
            has_more = bool(cached.get("has_more", False))

            while len(items) < limit and server_cursor and has_more:
                payload = client.search_articles(
                    query=query,
                    cursor=server_cursor,
                    limit=limit,
                    sort_type=sort_type,
                )
                items.extend(normalize_search_items(payload))
                server_cursor = str(payload.get("cursor") or "").strip()
                has_more = bool(payload.get("has_more", False))

            return _paginate_search_items(
                query=query,
                sort_type=sort_type,
                limit=limit,
                items=items,
                server_cursor=server_cursor,
                has_more=has_more,
            )

        payload = client.search_articles(
            query=query,
            cursor=cursor,
            limit=limit,
            sort_type=sort_type,
        )
    items = normalize_search_items(payload)
    return _paginate_search_items(
        query=query,
        sort_type=sort_type,
        limit=limit,
        items=items,
        server_cursor=str(payload.get("cursor") or "").strip(),
        has_more=bool(payload.get("has_more", False)),
    )


def _load_article(reference: str) -> Dict[str, Any]:
    article_id = _resolve_article_id(reference)
    with JuejinClient() as client:
        html = client.fetch_article_html(article_id)
    try:
        return parse_article_html(html, article_id)
    except ValueError as exc:
        raise click.ClickException(str(exc)) from exc


@cli.command()
@structured_output_options
def categories(as_json: bool, as_yaml: bool) -> None:
    """List Juejin article categories."""
    with JuejinClient() as client:
        items = client.get_categories()
    if emit_structured(items, as_json=as_json, as_yaml=as_yaml):
        return
    render_categories(items)


@cli.command()
@click.option("--category", "category_ref", default=DEFAULT_CATEGORY, show_default=True)
@click.option("--cursor", default="0", show_default=True)
@click.option("--limit", default=DEFAULT_LIMIT, show_default=True, type=click.IntRange(min=1))
@structured_output_options
def feed(category_ref: str, cursor: str, limit: int, as_json: bool, as_yaml: bool) -> None:
    """Browse a category feed."""
    with JuejinClient() as client:
        categories = client.get_categories()
        category = _resolve_category(categories, category_ref)
        payload = client.get_feed(
            cate_id=str(category["category_id"]),
            cursor=_normalize_cursor(cursor),
            limit=limit,
        )

    items = normalize_feed_items(payload)
    save_index(items)
    result = {
        "category": category,
        "cursor": payload.get("cursor", ""),
        "has_more": bool(payload.get("has_more", False)),
        "items": items,
    }
    if emit_structured(result, as_json=as_json, as_yaml=as_yaml):
        return
    render_article_list(f"Juejin Feed: {category['category_name']}", items)
    render_pagination(str(result["cursor"]), bool(result["has_more"]))


@cli.command()
@click.argument("query")
@click.option("--cursor", default="0", show_default=True)
@click.option("--limit", default=DEFAULT_LIMIT, show_default=True, type=click.IntRange(min=1))
@click.option(
    "--sort",
    type=click.Choice(sorted(SEARCH_SORTS.keys())),
    default="all",
    show_default=True,
)
@structured_output_options
def search(query: str, cursor: str, limit: int, sort: str, as_json: bool, as_yaml: bool) -> None:
    """Search Juejin articles."""
    result = _search_with_cursor(
        query=query,
        cursor=_normalize_cursor(cursor),
        limit=limit,
        sort_type=SEARCH_SORTS[sort],
    )
    items = result["items"]
    save_index(items)
    result["query"] = query
    if emit_structured(result, as_json=as_json, as_yaml=as_yaml):
        return
    render_article_list(f"Juejin Search: {query}", items)
    render_pagination(str(result["cursor"]), bool(result["has_more"]))


@cli.command()
@click.argument("reference")
@structured_output_options
def read(reference: str, as_json: bool, as_yaml: bool) -> None:
    """Read an article by ID, URL, or short index."""
    article = _load_article(reference)
    if emit_structured(article, as_json=as_json, as_yaml=as_yaml):
        return
    render_article(article)


@cli.command("export-md")
@click.argument("reference")
@click.option("-o", "--output", type=click.Path(path_type=Path), required=False)
def export_md(reference: str, output: Optional[Path]) -> None:
    """Export an article as Markdown."""
    article = _load_article(reference)
    output_path = output or Path(f"{article['article_id']}.md")
    output_path.write_text(article["markdown"], encoding="utf-8")
    click.echo(str(output_path))


def main() -> None:
    try:
        cli()
    except JuejinCliError as exc:
        raise click.ClickException(str(exc)) from exc
