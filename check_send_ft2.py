with open('static/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

idx = js.find("sendFloatingTutorMessage()")
print(js[idx+1400:idx+2500])
