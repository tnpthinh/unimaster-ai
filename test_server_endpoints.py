"""Runnable endpoint smoke-test. Run: python test_server_endpoints.py"""
import aiohttp, asyncio, sys

BASE = "http://localhost:8080"

# (method, path, expected_status)
CASES = [
    ("GET",  "/api/subjects",                          200),
    ("GET",  "/api/stats",                             200),
    ("GET",  "/api/user-state",                        200),
    ("GET",  "/api/subjects/10/questions?type=all",    200),
    ("GET",  "/api/questions/376/discussions",         200),
    ("GET",  "/api/history/archive?type=exam",         200),
    ("GET",  "/api/history/archive?type=tutor_chat",   200),
    ("GET",  "/api/exercises?subject_id=5",            200),
    ("GET",  "/api/ai/key-status",                     200),
    ("GET",  "/api/network/qr-info",                   200),
    ("GET",  "/api/flashcards?subject_id=10",          200),
    ("GET",  "/api/battle/leaderboard",                200),
    ("GET",  "/api/stem/reference",                    200),
    ("GET",  "/api/exam/ctump-parts",                  200),
]

async def run():
    failures = []
    async with aiohttp.ClientSession() as s:
        for method, path, want in CASES:
            url = f"{BASE}{path}"
            try:
                async with s.request(method, url) as r:
                    got = r.status
                    ok = got == want
                    print(f"  {'OK' if ok else 'FAIL'} {method} {path} -> {got} (want {want})")
                    if not ok:
                        failures.append(f"{method} {path}: got {got}, want {want}")
            except Exception as e:
                failures.append(f"{method} {path}: ERROR {e}")
                print(f"  FAIL {method} {path} -> ERROR {e}")
    return failures

if __name__ == "__main__":
    fails = asyncio.run(run())
    if fails:
        print(f"\n{len(fails)} FAILED:")
        for f in fails:
            print(f"  - {f}")
        sys.exit(1)
    else:
        print(f"\nAll {len(CASES)} endpoints OK.")
        sys.exit(0)
