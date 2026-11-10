with open('server.py', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('/api/code/test')
if idx != -1:
    print(text[idx-50:idx+600])
else:
    print('Not found')
