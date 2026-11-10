# list_ai_routes.py
import re

with open('server.py', 'r', encoding='utf-8') as f:
    text = f.read()

matches = re.findall(r'app\.router\.add_[a-z]+\([\'"](/api/ai/[^\'"]+)[\'"]\s*,\s*([a-zA-Z0-9_]+)', text)
print(f"Found {len(matches)} AI endpoints in server.py:")
for r, handler in matches:
    print(f"  {r} -> {handler}")
