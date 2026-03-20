from __future__ import annotations

from pathlib import Path

API_HOST = "https://api.juejin.cn"
WEB_HOST = "https://juejin.cn"
AID = 2608
DEFAULT_LIMIT = 20
DEFAULT_CATEGORY = "backend"
DEFAULT_FEED_SORT = 200
DEFAULT_SEARCH_TYPE = 0
DEFAULT_USER_POSTS_LIMIT = 10
HOT_ALL_CATEGORY_ID = "1"
HOT_RANK_SORT_DESC = 2

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

USER_POST_SORTS = {
    "newest": "newest",
    "popular": "popular",
}

HOT_RANK_TYPES = {
    "hot": "hot",
    "collect": "collect",
}

HOT_AUTHOR_PERIODS = {
    "weekly": 1,
    "monthly": 2,
}

HOT_AUTHOR_CATEGORIES = {
    "backend": {
        "id": "6809637769959178254",
        "name": "后端",
    },
    "frontend": {
        "id": "6809637767543259144",
        "name": "前端",
    },
    "client": {
        "id": "6809635626879549454",
        "name": "客户端",
    },
    "ai": {
        "id": "6809637773935378440",
        "name": "人工智能",
    },
    "tools": {
        "id": "6809637771511070734",
        "name": "开发工具",
    },
    "career": {
        "id": "6809637776263217160",
        "name": "代码人生",
    },
    "reading": {
        "id": "6809637772874219534",
        "name": "阅读",
    },
}
