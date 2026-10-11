"""쿠팡 파트너스 Open API: 상품 검색 (응답의 productUrl은 이미 제휴 링크)."""
import hmac
import hashlib
from datetime import datetime, timezone
from urllib.parse import urlencode

import requests

from .config import COUPANG_ACCESS_KEY, COUPANG_SECRET_KEY

HOST = "https://api-gateway.coupang.com"
SEARCH_PATH = "/v2/providers/affiliate_open_api/apis/openapi/products/search"


def _auth(method: str, path: str, query: str) -> str:
    signed_date = datetime.now(timezone.utc).strftime("%y%m%dT%H%M%SZ")
    message = signed_date + method + path + query
    sig = hmac.new(
        COUPANG_SECRET_KEY.encode(), message.encode(), hashlib.sha256
    ).hexdigest()
    return (
        f"CEA algorithm=HmacSHA256, access-key={COUPANG_ACCESS_KEY}, "
        f"signed-date={signed_date}, signature={sig}"
    )


def search(keyword: str, limit: int = 5) -> list[dict]:
    query = urlencode({"keyword": keyword, "limit": limit})
    r = requests.get(
        f"{HOST}{SEARCH_PATH}?{query}",
        headers={"Authorization": _auth("GET", SEARCH_PATH, query)},
        timeout=30,
    )
    r.raise_for_status()
    return r.json().get("data", {}).get("productData", [])
