with open('server.py', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('async def api_exam_shuffle(')
if idx != -1:
    print(text[idx:idx+600])
