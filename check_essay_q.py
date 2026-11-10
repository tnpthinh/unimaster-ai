with open('static/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

idx = js.find("q.q_type === 'essay'")
if idx != -1:
    print(js[idx-100:idx+600])
else:
    print("Not found")
