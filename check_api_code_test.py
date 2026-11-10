with open('server.py', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('async def api_code_test(')
if idx != -1:
    print(text[idx:idx+1500])
else:
    print('Not found')
