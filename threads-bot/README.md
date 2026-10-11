# Threads × 쿠팡 파트너스 자동 발행 봇

흐름: Threads 인기글(TOP 검색)에서 **화제가 되는 제품 카테고리만** 추출 → 쿠팡 파트너스 API로 상품 검색
→ 상품 정보만으로 Claude가 새 글 작성(원문/타인 사진 재사용 없음) → 고지문 자동 부착 → 발행.

## 안전장치
- 기본은 **dry-run**(초안만 저장). `--publish` 또는 워크플로 수동 실행의 `publish=true`일 때만 발행.
- 쿠팡 파트너스 고지문은 코드가 항상 붙임(`config.DISCLOSURE`).
- 이미지는 쿠팡 API가 주는 상품 이미지만 사용. 같은 상품 중복 발행 방지(`data/state.json`).
- Threads 검색 권한(`threads_keyword_search`)이 없으면 `SEED_KEYWORDS`로 자동 대체.

## 필요한 시크릿 (GitHub → Settings → Secrets → Actions)
`THREADS_ACCESS_TOKEN`, `ANTHROPIC_API_KEY`, `COUPANG_ACCESS_KEY`, `COUPANG_SECRET_KEY`

## 로컬 실행
```
pip install -r requirements.txt
python -m bot.main            # 초안만
python -m bot.main --publish  # 실제 발행
```
