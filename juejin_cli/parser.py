from __future__ import annotations

import re
from html import unescape
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from markdownify import markdownify as html_to_markdown

ARTICLE_URL_RE = re.compile(r"/post/(\d+)")


def parse_article_reference(raw: str) -> str:
    value = raw.strip()
    if not value:
        raise ValueError("Empty article reference")
    if value.isdigit():
        return value
    match = ARTICLE_URL_RE.search(value)
    if match:
        return match.group(1)
    parsed = urlparse(value)
    if parsed.scheme or parsed.netloc:
        raise ValueError(f"Unsupported Juejin article URL: {value}")
    raise ValueError(f"Unsupported article reference: {value}")


def normalize_feed_items(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    items = payload.get("data")
    if not isinstance(items, list):
        return []
    rows: List[Dict[str, Any]] = []
    for entry in items:
        article = entry.get("article_info") or {}
        author = entry.get("author_user_info") or {}
        category = entry.get("category") or {}
        tags = entry.get("tags") or []
        article_id = str(entry.get("article_id") or article.get("article_id") or "").strip()
        if not article_id:
            continue
        rows.append(
            {
                "article_id": article_id,
                "title": str(article.get("title") or "").strip(),
                "author": str(author.get("user_name") or "").strip(),
                "category": str(category.get("category_url") or category.get("category_name") or "").strip(),
                "brief": str(article.get("brief_content") or "").strip(),
                "views": int(article.get("view_count") or 0),
                "diggs": int(article.get("digg_count") or 0),
                "comments": int(article.get("comment_count") or 0),
                "read_time": str(article.get("read_time") or "").strip(),
                "tags": [str(tag.get("tag_name") or "").strip() for tag in tags if isinstance(tag, dict)],
                "url": f"https://juejin.cn/post/{article_id}",
            }
        )
    return rows


def normalize_search_items(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    items = payload.get("data")
    if not isinstance(items, list):
        return []
    rows: List[Dict[str, Any]] = []
    for entry in items:
        if entry.get("result_type") != 2:
            continue
        model = entry.get("result_model") or {}
        article = model.get("article_info") or {}
        author = model.get("author_user_info") or {}
        category = model.get("category") or {}
        tags = model.get("tags") or []
        article_id = str(model.get("article_id") or article.get("article_id") or "").strip()
        if not article_id:
            continue
        rows.append(
            {
                "article_id": article_id,
                "title": _strip_highlight(entry.get("title_highlight") or article.get("title") or ""),
                "author": str(author.get("user_name") or "").strip(),
                "category": str(category.get("category_url") or category.get("category_name") or "").strip(),
                "brief": str(article.get("brief_content") or "").strip(),
                "views": int(article.get("view_count") or 0),
                "diggs": int(article.get("digg_count") or 0),
                "comments": int(article.get("comment_count") or 0),
                "read_time": str(article.get("read_time") or "").strip(),
                "tags": [str(tag.get("tag_name") or "").strip() for tag in tags if isinstance(tag, dict)],
                "url": f"https://juejin.cn/post/{article_id}",
            }
        )
    return rows


def parse_article_html(html: str, article_id: str) -> Dict[str, Any]:
    soup = BeautifulSoup(html, "html.parser")

    title = ""
    title_node = soup.select_one("h1.article-title")
    if title_node:
        title = title_node.get_text(" ", strip=True)
    if not title:
        page_title = soup.title.get_text(" ", strip=True) if soup.title else ""
        title = page_title.split(" - 掘金", 1)[0].strip()

    author = ""
    author_node = soup.select_one(".author-info-block .author-name, .author-info-block .name")
    if author_node:
        author = author_node.get_text(" ", strip=True)

    published_at = ""
    time_node = soup.select_one(".meta-box time")
    if time_node:
        published_at = time_node.get_text(" ", strip=True)

    views = ""
    view_node = soup.select_one(".meta-box .views-count")
    if view_node:
        views = view_node.get_text(" ", strip=True)

    read_time = ""
    read_time_node = soup.select_one(".meta-box .read-time")
    if read_time_node:
        read_time = re.sub(r"\s+", " ", read_time_node.get_text(" ", strip=True))

    article_root = soup.select_one("#article-root .article-viewer")
    if article_root is None:
        raise ValueError(f"Failed to locate article body for {article_id}")

    for node in article_root.select("style, script"):
        node.decompose()

    body_html = "".join(str(node) for node in article_root.contents).strip()
    markdown = html_to_markdown(body_html, heading_style="ATX", strip=["style"])
    markdown = _clean_markdown(markdown)

    description = ""
    desc_meta = soup.find("meta", attrs={"name": "description"})
    if desc_meta and desc_meta.get("content"):
        description = str(desc_meta["content"]).strip()

    canonical = ""
    canonical_link = soup.find("link", attrs={"rel": "canonical"})
    if canonical_link and canonical_link.get("href"):
        canonical = str(canonical_link["href"]).strip()
    if not canonical:
        canonical = f"https://juejin.cn/post/{article_id}"

    return {
        "article_id": article_id,
        "title": title,
        "author": author,
        "published_at": published_at,
        "views": views,
        "read_time": read_time,
        "description": description,
        "url": canonical,
        "html": body_html,
        "markdown": markdown,
    }


def _strip_highlight(value: str) -> str:
    text = re.sub(r"</?em>", "", value)
    return unescape(text).strip()


def _clean_markdown(value: str) -> str:
    text = value.replace("\r\n", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()
