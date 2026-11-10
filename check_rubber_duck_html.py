with open('static/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('rubber-duck-sidebar')
print(text[idx-50:idx+400])
