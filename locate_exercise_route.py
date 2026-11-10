with open('server.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'exercise' in l.lower() and ('add_get' in l or 'add_post' in l or 'app.router' in l):
        print(f"{i+1}: {l.strip()}")
