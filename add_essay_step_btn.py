with open('static/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

target = '''          <button onclick="triggerGradeEssay()" class="btn-primary px-4 py-2 text-xs flex items-center gap-1.5 font-bold shadow-md">
            <span>✨</span> Giám Khảo Chấm Thi (Thang 10)
          </button>'''

replacement = '''          <button onclick="triggerGradeEssay()" class="btn-primary px-4 py-2 text-xs flex items-center gap-1.5 font-bold shadow-md">
            <span>✨</span> Giám Khảo Chấm Thi (Thang 10)
          </button>
          <button onclick="triggerStepByStepEssayValidation()" class="btn-primary !bg-gradient-to-r !from-amber-600 !to-rose-600 px-4 py-2 text-xs flex items-center gap-1.5 font-bold shadow-md">
            <span>🔍</span> Soi Từng Bước &amp; Đánh Dấu Lỗi Sai
          </button>'''

if target in text:
    text = text.replace(target, replacement)
    with open('static/index.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Added triggerStepByStepEssayValidation button to view-essay.")
else:
    print("Target triggerGradeEssay button not found!")
