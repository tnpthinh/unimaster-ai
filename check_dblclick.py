with open('static/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

idx = js.find("'dblclick'")
if idx == -1:
    idx = js.find('"dblclick"')
print('dblclick index:', idx)
if idx != -1:
    print(js[idx-100:idx+600])
