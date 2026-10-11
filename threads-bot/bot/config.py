import os

THREADS_TOKEN = os.environ.get("THREADS_ACCESS_TOKEN", "")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
COUPANG_ACCESS_KEY = os.environ.get("COUPANG_ACCESS_KEY", "")
COUPANG_SECRET_KEY = os.environ.get("COUPANG_SECRET_KEY", "")

MODEL = os.environ.get("CLAUDE_MODEL", "claude-sonnet-5-5")

# 쓰레드 키워드 검색이 막혔을 때(앱 리뷰 전 등) 쓰는 기본 주제
SEED_KEYWORDS = [
    k.strip()
    for k in os.environ.get(
        "SEED_KEYWORDS", "신기한 주방템,이색 가젯,자취 꿀템,책상 정리템,캠핑 신상템"
    ).split(",")
    if k.strip()
]
TREND_QUERIES = ["신기한 제품", "꿀템 추천", "이거 실화냐 제품"]

DISCLOSURE = "이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다."
MAX_TEXT = 500
STATE_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "state.json")
