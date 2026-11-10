with open('static/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find("switchSettingsTab('ai')")
print(text[idx:idx+1500])
