import json
import os
import sys

needle = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("SEARCH_PATTERN", "")
transcript_path = sys.argv[2] if len(sys.argv) > 2 else os.environ.get("TRANSCRIPT_PATH", "")
if not needle or not transcript_path or not os.path.exists(transcript_path):
    print("Usage: python check_key_origin.py <pattern> <transcript_path>")
    raise SystemExit(0)

with open(transcript_path, "r", encoding="utf-8") as f:
    for line in f:
        if needle in line:
            obj = json.loads(line)
            print("Step index:", obj.get("step_index"))
            print("Source:", obj.get("source"))
            print("Type:", obj.get("type"))
            print("Content:", str(obj.get("content"))[:500])
            print("=" * 50)
