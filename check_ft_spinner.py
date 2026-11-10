with open('static/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

idx = js.find("'ft-spinner'")
print(js[idx-300:idx+400])
