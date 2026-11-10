with open('static/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'function\s+[a-zA-Z0-9_]*osce[a-zA-Z0-9_]*', text, re.IGNORECASE)]
print(f"Found {len(matches)} OSCE functions in app.js:")
for m in matches:
    idx_end = text.find('{', m)
    print(" -", text[m:idx_end].strip())

# Also search for selectOsce or clickOsce or answerOsce
matches2 = [m.start() for m in re.finditer(r'function\s+[a-zA-Z0-9_]*station[a-zA-Z0-9_]*', text, re.IGNORECASE)]
print(f"\nFound {len(matches2)} Station functions in app.js:")
for m in matches2:
    idx_end = text.find('{', m)
    print(" -", text[m:idx_end].strip())
