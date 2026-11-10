with open('ai_service.py', 'r', encoding='utf-8') as f:
    code = f.read()

import re
matches = [m.start() for m in re.finditer(r'openai|chatgpt|codex|api\.openai\.com|sk-', code, re.IGNORECASE)]
print(f"Matches in ai_service.py: {len(matches)}")
for p in matches[:10]:
    print(code[max(0, p-50):p+150])
    print("-" * 40)
