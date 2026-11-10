with open('static/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

idx = js.find("'hero-xp-bar'")
if idx != -1:
    print(js[idx-100:idx+300])
