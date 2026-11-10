with open('static/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="view-exercises"')
print(text[idx+1200:idx+3000])
