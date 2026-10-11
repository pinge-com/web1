"""사용법: python -m bot.main [--publish] [--count 1]
기본은 dry-run(초안만 data/state.json 의 drafts 에 저장). --publish 일 때만 실제 발행."""
import argparse
import random

from . import coupang, store, threads_api, writer
from .config import SEED_KEYWORDS, TREND_QUERIES


def discover_keywords() -> list[str]:
    texts = []
    try:
        for q in TREND_QUERIES:
            texts += [p["text"] for p in threads_api.keyword_search(q, 10) if p.get("text")]
        if texts:
            return writer.extract_keywords(texts)
    except Exception as e:  # 검색 권한 미승인 등
        print(f"[warn] Threads 검색 실패, 시드 키워드 사용: {e}")
    return random.sample(SEED_KEYWORDS, k=min(3, len(SEED_KEYWORDS)))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--publish", action="store_true")
    ap.add_argument("--count", type=int, default=1)
    args = ap.parse_args()

    state = store.load()
    done = set(state["posted_product_ids"])
    made = 0
    for kw in discover_keywords():
        if made >= args.count:
            break
        for prod in coupang.search(kw):
            pid = str(prod["productId"])
            if pid in done or not prod.get("productImage"):
                continue
            text = writer.write_post(prod)
            draft = {"keyword": kw, "productId": pid, "text": text, "image": prod["productImage"]}
            if args.publish:
                draft["threads_id"] = threads_api.publish(text, prod["productImage"])
                state["posted_product_ids"].append(pid)
            else:
                state["drafts"].append(draft)
            print(("PUBLISHED" if args.publish else "DRAFT"), "\n", text, "\n")
            done.add(pid)
            made += 1
            break
    state["drafts"] = state["drafts"][-30:]
    store.save(state)


if __name__ == "__main__":
    main()
