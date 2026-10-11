"""Threads 공식 Graph API 래퍼 (검색 + 발행)."""
import time

import requests

from .config import THREADS_TOKEN

BASE = "https://graph.threads.net/v1.0"


def keyword_search(query: str, limit: int = 25) -> list[dict]:
    """인기(TOP) 게시물 검색. 조회수는 제공되지 않아 좋아요·답글로 점수화한다."""
    r = requests.get(
        f"{BASE}/keyword_search",
        params={
            "q": query,
            "search_type": "TOP",
            "fields": "id,text,permalink,like_count,reply_count,timestamp",
            "access_token": THREADS_TOKEN,
        },
        timeout=30,
    )
    r.raise_for_status()
    posts = r.json().get("data", [])
    for p in posts:
        p["score"] = p.get("like_count", 0) + 3 * p.get("reply_count", 0)
    return sorted(posts, key=lambda p: p["score"], reverse=True)[:limit]


def publish(text: str, image_url: str | None = None) -> str:
    """컨테이너 생성 → 발행. 발행된 게시물 id 반환."""
    data = {"text": text, "access_token": THREADS_TOKEN}
    if image_url:
        data.update(media_type="IMAGE", image_url=image_url)
    else:
        data["media_type"] = "TEXT"
    r = requests.post(f"{BASE}/me/threads", data=data, timeout=30)
    r.raise_for_status()
    creation_id = r.json()["id"]
    time.sleep(10)  # 미디어 처리 대기 (공식 권장: 약 30초까지)
    r = requests.post(
        f"{BASE}/me/threads_publish",
        data={"creation_id": creation_id, "access_token": THREADS_TOKEN},
        timeout=30,
    )
    r.raise_for_status()
    return r.json()["id"]
