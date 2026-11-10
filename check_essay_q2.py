with open('static/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

idx = js.find("else if (q.q_type === 'essay')")
if idx != -1:
    print(js[idx:idx+800])
else:
    print("Not found")
