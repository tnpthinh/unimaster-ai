import os, re, json, glob

html_path = r'C:\Users\PC\.gemini\antigravity\scratch\unimaster-ai\static\index.html'
app_path = r'C:\Users\PC\.gemini\antigravity\scratch\unimaster-ai\static\app.js'
server_path = r'C:\Users\PC\.gemini\antigravity\scratch\unimaster-ai\server.py'

with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

with open(app_path, 'r', encoding='utf-8') as f:
    app_content = f.read()

with open(server_path, 'r', encoding='utf-8') as f:
    server_content = f.read()

print("="*60)
print("AUDIT 1: ONCLICK / EVENT HANDLERS IN HTML VS APP.JS")
print("="*60)

# Extract event handlers from HTML
event_attrs = re.findall(r'(?:onclick|onchange|oninput|onsubmit|onkeydown)=["\']([^"\']+)["\']', html_content)
missing_handlers = set()
for handler in event_attrs:
    # Extract function calls e.g. switchTab('exam') -> switchTab
    fn_matches = re.findall(r'([a-zA-Z0-9_$]+)\s*\(', handler)
    for fn in fn_matches:
        if fn in ['alert', 'confirm', 'prompt', 'parseInt', 'parseFloat', 'Boolean', 'String', 'Number', 'console', 'setTimeout', 'clearTimeout', 'setInterval', 'clearInterval']:
            continue
        # Check if function exists in app.js
        pattern = rf'(?:function\s+{fn}\b|const\s+{fn}\s*=|let\s+{fn}\s*=|var\s+{fn}\s*=|window\.{fn}\s*=)'
        if not re.search(pattern, app_content):
            missing_handlers.add(fn)

print(f"Total event handlers found: {len(event_attrs)}")
print(f"Missing functions in app.js ({len(missing_handlers)}):")
for m in sorted(missing_handlers):
    print(f"  ❌ {m}")

print("\n" + "="*60)
print("AUDIT 2: document.getElementById CALLS IN APP.JS VS HTML")
print("="*60)

get_elem_ids = set(re.findall(r'document\.getElementById\(["\']([^"\']+)["\']\)', app_content))
missing_ids = set()
for eid in get_elem_ids:
    if f'id="{eid}"' not in html_content and f"id='{eid}'" not in html_content:
        missing_ids.add(eid)

print(f"Total getElementById calls: {len(get_elem_ids)}")
print(f"IDs missing in index.html ({len(missing_ids)}):")
for m in sorted(missing_ids):
    print(f"  ⚠️ {m}")

print("\n" + "="*60)
print("AUDIT 3: API ENDPOINTS IN APP.JS VS SERVER.PY")
print("="*60)

api_calls = set(re.findall(r'apiFetch\(["\']([^"\'?]+)', app_content))
server_routes = set(re.findall(r'add_(?:get|post|put|delete)\(["\']([^"\']+)', server_content))

print(f"Total apiFetch calls in app.js: {len(api_calls)}")
print(f"Total server routes in server.py: {len(server_routes)}")

# Check matching
missing_routes = []
for call in api_calls:
    if call.startswith('http'):
        continue
    # Normalize regex path
    pattern = re.sub(r'\{[^}]+\}', r'[^/]+', call)
    found = False
    for r in server_routes:
        r_norm = re.sub(r'\{[^}]+\}', r'[^/]+', r)
        if re.fullmatch(r_norm, call) or call == r:
            found = True
            break
    if not found:
        missing_routes.append(call)

print(f"API calls missing in server.py ({len(missing_routes)}):")
for r in sorted(missing_routes):
    print(f"  ❌ {r}")
