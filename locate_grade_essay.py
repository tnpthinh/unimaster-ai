with open('static/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('triggerGradeEssay()')
if idx != -1:
    print(text[idx-50:idx+250])
