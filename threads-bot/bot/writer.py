"""Claude로 (1) 트렌드에서 상품 검색어 추출 (2) 상품 정보로 새 글 작성."""
import json
import re

import anthropic

from .config import ANTHROPIC_API_KEY, DISCLOSURE, MAX_TEXT, MODEL

_client = None


def _ask(prompt: str, max_tokens: int = 1500) -> str:
    global _client
    _client = _client or anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    msg = _client.messages.create(
        model=MODEL, max_tokens=max_tokens, messages=[{"role": "user", "content": prompt}]
    )
    return msg.content[0].text


def _json(text: str):
    m = re.search(r"[\[{].*[\]}]", text, re.S)
    return json.loads(m.group(0))


def extract_keywords(trend_texts: list[str], n: int = 5) -> list[str]:
    """인기글에서 '어떤 종류의 제품이 화제인지'만 뽑는다. 원문 문장은 쓰지 않는다."""
    joined = "\n---\n".join(t[:300] for t in trend_texts[:15])
    out = _ask(
        f"아래는 SNS에서 반응이 좋은 글들이다. 여기서 언급되거나 암시된 '신기하고 재밌는 "
        f"실물 제품 카테고리'를 쿠팡 검색어 {n}개로 뽑아 JSON 문자열 배열로만 답해라. "
        f"브랜드 상표/문장 인용 금지, 구체적이고 짧은 일반명사로.\n\n{joined}"
    )
    return _json(out)


def write_post(product: dict) -> str:
    """상품 정보만으로 새 글을 쓴다. 쿠팡 파트너스 고지문은 코드가 강제로 붙인다."""
    info = {k: product.get(k) for k in ("productName", "productPrice", "isRocket")}
    body = _ask(
        "Threads용 짧은 홍보글을 한국어로 써라. 조건: 첫 줄은 호기심을 끄는 후킹, "
        "친근한 말투, 이모지 2개 이하, 과장·허위·의학적 효능 주장 금지, 링크와 고지문은 "
        "쓰지 마라(별도로 붙임), 본문 220자 이내. 본문 텍스트만 출력.\n\n"
        f"상품: {json.dumps(info, ensure_ascii=False)}"
    ).strip()
    tail = f"\n\n👉 {product['productUrl']}\n\n{DISCLOSURE}"
    return body[: MAX_TEXT - len(tail)] + tail
