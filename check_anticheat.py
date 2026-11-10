with open('static/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re
matches = [m.start() for m in re.finditer(r'activateAntiCheat', js)]
print('activateAntiCheat matches:', len(matches))
for m in matches:
    print(js[max(0, m-50):min(len(js), m+150)])
    print('---')
