import os
import sys

needle = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("SEARCH_PATTERN", "")
if not needle:
    print("Usage: python read_key_in_app_js.py <pattern>")
    raise SystemExit(0)

with open("static/app.js", "r", encoding="utf-8") as f:
    js = f.read()

pos = js.find(needle)
print(js[max(0, pos - 200):pos + 300] if pos != -1 else "Not found")
