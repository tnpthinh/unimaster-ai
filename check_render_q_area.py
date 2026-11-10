with open('static/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

idx = js.find('function renderQuestionAnswerArea(q)')
idx_next = js.find('function renderQuestionFeedbackArea(q)')
print(js[idx:idx_next])
