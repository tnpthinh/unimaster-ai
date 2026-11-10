with open('static/app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'function renderOsceStation' in l:
        print(f"renderOsceStation line: {i+1}")
    if 'function submitOsceStationAnswer' in l:
        print(f"submitOsceStationAnswer line: {i+1}")
