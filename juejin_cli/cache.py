from __future__ import annotations

import json
from pathlib import Path
from secrets import token_urlsafe
from typing import Any, Dict, List, Optional

from .constants import CONFIG_DIR, INDEX_CACHE_FILE, SEARCH_CURSOR_CACHE_FILE, SEARCH_CURSOR_PREFIX


def ensure_config_dir() -> Path:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    return CONFIG_DIR


def _read_json(path: Path, *, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return default


def _write_json(path: Path, data: Any) -> None:
    ensure_config_dir()
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def save_index(items: List[Dict[str, Any]]) -> None:
    normalized = []
    for item in items:
        article_id = str(item.get("article_id", "")).strip()
        if not article_id:
            continue
        normalized.append(
            {
                "article_id": article_id,
                "title": str(item.get("title", "")).strip(),
                "url": str(item.get("url", "")).strip(),
            }
        )
    _write_json(INDEX_CACHE_FILE, normalized)


def load_index() -> List[Dict[str, Any]]:
    data = _read_json(INDEX_CACHE_FILE, default=[])
    if not isinstance(data, list):
        return []
    return [item for item in data if isinstance(item, dict)]


def get_index_item(index: int) -> Optional[Dict[str, Any]]:
    if index <= 0:
        return None
    data = load_index()
    if index > len(data):
        return None
    return data[index - 1]


def is_local_search_cursor(cursor: str) -> bool:
    return cursor.startswith(SEARCH_CURSOR_PREFIX)


def save_search_cursor(state: Dict[str, Any]) -> str:
    token = f"{SEARCH_CURSOR_PREFIX}{token_urlsafe(12)}"
    data = _read_json(SEARCH_CURSOR_CACHE_FILE, default={})
    if not isinstance(data, dict):
        data = {}
    data[token] = state
    _write_json(SEARCH_CURSOR_CACHE_FILE, data)
    return token


def load_search_cursor(cursor: str) -> Optional[Dict[str, Any]]:
    data = _read_json(SEARCH_CURSOR_CACHE_FILE, default={})
    if not isinstance(data, dict):
        return None
    state = data.get(cursor)
    return state if isinstance(state, dict) else None
