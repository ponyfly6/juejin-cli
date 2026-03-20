from __future__ import annotations

from pathlib import Path

API_HOST = "https://api.juejin.cn"
WEB_HOST = "https://juejin.cn"
AID = 2608
DEFAULT_LIMIT = 20
DEFAULT_CATEGORY = "backend"
DEFAULT_FEED_SORT = 200
DEFAULT_SEARCH_TYPE = 0

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/136.0.0.0 Safari/537.36"
)

CONFIG_DIR = Path.home() / ".juejin-cli"
INDEX_CACHE_FILE = CONFIG_DIR / "index_cache.json"
SEARCH_CURSOR_CACHE_FILE = CONFIG_DIR / "search_cursor_cache.json"
SEARCH_CURSOR_PREFIX = "local-search:"

SEARCH_SORTS = {
    "all": 0,
    "newest": 1,
    "hottest": 2,
}
