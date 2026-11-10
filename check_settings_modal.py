with open('static/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="modal-settings"')
if idx != -1:
    print(text[idx:idx+1500])
else:
    print('Not found')
