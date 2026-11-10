# scan_all_non_async_awaits.py
import re

with open('static/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Match any "function name(...) {" or "name(...) {"
matches = list(re.finditer(r'(async\s+)?function\s+([a-zA-Z0-9_]+)\s*\(([^)]*)\)\s*\{', text))
print(f"Total function declarations: {len(matches)}")

bugs = []
for m in matches:
    is_async = bool(m.group(1))
    fn_name = m.group(2)
    start_pos = m.end()

    # Find matching closing brace
    depth = 1
    i = start_pos
    in_string = False
    quote_char = ''
    while i < len(text) and depth > 0:
        c = text[i]
        if not in_string:
            if c in ("'", '"', '`'):
                in_string = True
                quote_char = c
            elif c == '{':
                depth += 1
            elif c == '}':
                depth -= 1
        else:
            if c == '\\':
                i += 1  # skip escaped char
            elif c == quote_char:
                in_string = False
        i += 1

    fn_body = text[start_pos:i]

    # Look for await that is not inside a nested async function
    # Simple check: search for r'\bawait\s+' in fn_body
    if not is_async:
        # Check if fn_body contains await
        await_matches = list(re.finditer(r'\bawait\s+', fn_body))
        if await_matches:
            # Check if all awaits are inside nested functions
            # Let's inspect where the awaits are
            bugs.append((fn_name, m.start(), len(await_matches)))

print(f"\nFound {len(bugs)} non-async functions containing 'await':")
for b, pos, cnt in bugs:
    line_no = text.count('\n', 0, pos) + 1
    print(f"  Line {line_no}: function {b}() has {cnt} await call(s) without async!")
