import os

for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith(('.py', '.json', '.txt', '.md', '.html', '.js')):
            p = os.path.join(root, f)
            try:
                with open(p, 'r', encoding='utf-8') as fp:
                    content = fp.read()
                    if '00eab046c62fd5b2' in content:
                        print(f"Found in: {p}")
            except Exception:
                pass
