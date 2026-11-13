import os
import sys

needle = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("SEARCH_PATTERN", "")
if not needle:
    print("Usage: python search_user_key.py <pattern>")
    raise SystemExit(0)

for root, dirs, files in os.walk("."):
    for f in files:
        if f.endswith((".py", ".json", ".txt", ".md", ".html", ".js")):
            p = os.path.join(root, f)
            try:
                with open(p, "r", encoding="utf-8") as fp:
                    content = fp.read()
                    if needle in content:
                        print(f"Found in: {p}")
            except Exception:
                pass
