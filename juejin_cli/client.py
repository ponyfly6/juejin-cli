from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional

import httpx

from .constants import (
    AID,
    API_HOST,
    DEFAULT_FEED_SORT,
    DEFAULT_SEARCH_TYPE,
    USER_AGENT,
    WEB_HOST,
)


class JuejinCliError(RuntimeError):
    pass


class JuejinClient:
    def __init__(self, timeout: float = 20.0):
        self._http = httpx.Client(
            timeout=timeout,
            follow_redirects=True,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
                "Origin": WEB_HOST,
                "Referer": f"{WEB_HOST}/",
            },
        )

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> "JuejinClient":
        return self

    def __exit__(self, *_args: object) -> None:
        self.close()

    def _common_params(self, extra: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        params: Dict[str, Any] = {
            "aid": AID,
            "uuid": uuid.uuid4().hex,
            "spider": 0,
        }
        if extra:
            params.update(extra)
        return params

    def _handle_response(self, response: httpx.Response) -> Any:
        response.raise_for_status()
        payload = response.json()
        err_no = payload.get("err_no")
        if err_no != 0:
            raise JuejinCliError(payload.get("err_msg") or f"API error: {err_no}")
        return payload

    def get_categories(self) -> List[Dict[str, Any]]:
        resp = self._http.get(
            f"{API_HOST}/tag_api/v1/query_category_briefs",
            params=self._common_params(),
        )
        payload = self._handle_response(resp)
        data = payload.get("data")
        return data if isinstance(data, list) else []

    def get_feed(
        self,
        cate_id: str,
        cursor: str = "0",
        limit: int = 20,
        sort_type: int = DEFAULT_FEED_SORT,
    ) -> Dict[str, Any]:
        resp = self._http.post(
            f"{API_HOST}/recommend_api/v1/article/recommend_cate_feed",
            params=self._common_params(),
            json={
                "id_type": 2,
                "cate_id": cate_id,
                "cursor": cursor,
                "limit": limit,
                "sort_type": sort_type,
            },
        )
        return self._handle_response(resp)

    def search_articles(
        self,
        query: str,
        cursor: str = "0",
        limit: int = 20,
        sort_type: int = 0,
        search_type: int = DEFAULT_SEARCH_TYPE,
    ) -> Dict[str, Any]:
        params = self._common_params(
            {
                "query": query,
                "id_type": 2,
                "cursor": cursor,
                "limit": limit,
                "search_type": search_type,
                "sort_type": sort_type,
                "version": 1,
            }
        )
        resp = self._http.get(f"{API_HOST}/search_api/v1/search", params=params)
        return self._handle_response(resp)

    def fetch_article_html(self, article_id: str) -> str:
        resp = self._http.get(f"{WEB_HOST}/post/{article_id}", headers={"Accept": "text/html"})
        resp.raise_for_status()
        return resp.text
