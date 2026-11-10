# print_all_long_p.py
import re

with open('static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

matches = list(re.finditer(r'<p([^>]*)>([\s\S]*?)</p>', html))
print(f"Total <p> tags: {len(matches)}")
long_ps = []
for m in matches:
    content = m.group(2)
    # clean tags
    clean = ' '.join(re.sub(r'<[^>]+>', '', content).split())
    if len(clean) > 40:
        long_ps.append((m.group(0), clean))

print(f"Long <p> tags (>40 chars): {len(long_ps)}")
for i, (orig, clean) in enumerate(long_ps):
    print(f"--- #{i+1} ---")
    print("CLEAN:", clean)
