with open('static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

pos = html.find('id="stab-panel-ai"')
print(html[pos:pos+2500])
