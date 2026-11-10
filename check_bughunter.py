with open('static/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

idx = js.find('function openBugHunterModal(')
if idx != -1:
    print(js[idx:idx+1500])
else:
    print('Not found')
