with open('static/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="stab-content-ai"')
if idx != -1:
    print(text[idx:idx+1500])
else:
    print('Not found')
