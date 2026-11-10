with open('static/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

pos = js.find('00eab046c62fd5b2')
print(js[pos-200:pos+300])
