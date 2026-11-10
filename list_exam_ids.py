with open('static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('id="exam-config-screen"')
idx2 = html.find('id="view-exercises"')
sub = html[idx:idx2]
import re
print("IDs in view-exam:", re.findall(r'id="([^"]+)"', sub))
