import re

with open('static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

with open('static/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Check onclick handlers
onclick_matches = re.findall(r'onclick="([^"(]+)\(', html)
print(f"Total onclick handlers found: {len(onclick_matches)}")

missing_fns = []
for fn in set(onclick_matches):
    fn_clean = fn.strip().replace('window.', '').replace('return ', '')
    if not fn_clean or fn_clean in ('alert', 'confirm', 'setTimeout', 'console.log', 'event.stopPropagation'):
        continue
    # check if defined in js
    pattern = rf'(?:function\s+{fn_clean}|const\s+{fn_clean}\s*=|let\s+{fn_clean}\s*=|window\.{fn_clean}\s*=)'
    if not re.search(pattern, js):
        missing_fns.append(fn_clean)

print(f"Missing onclick functions ({len(missing_fns)}):", missing_fns)

# 2. Check getElementById calls in app.js
get_el_matches = re.findall(r'document\.getElementById\([\'"]([a-zA-Z0-9_\-]+)[\'"]\)', js)
print(f"Total document.getElementById calls: {len(get_el_matches)}")

missing_ids = []
for el_id in set(get_el_matches):
    if f'id="{el_id}"' not in html and f"id='{el_id}'" not in html and f'id={el_id}' not in html:
        missing_ids.append(el_id)

print(f"Element IDs referenced in JS but missing in HTML ({len(missing_ids)}):")
for m_id in sorted(missing_ids):
    print("  ", m_id)
