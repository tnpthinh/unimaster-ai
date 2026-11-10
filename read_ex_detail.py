with open('static/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

idx = js.find('function renderExerciseDetail()')
print(js[idx:idx+1200])
