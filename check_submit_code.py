with open('static/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('function submitCodeTestCases(')
if idx != -1:
    print(text[idx:idx+1500])
else:
    print('Not found')
