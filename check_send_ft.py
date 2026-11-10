with open('static/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

idx = js.find("sendFloatingTutorMessage()")
print(js[idx:idx+1500])
