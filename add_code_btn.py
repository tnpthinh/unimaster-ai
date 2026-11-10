app_path = r'C:\Users\PC\.gemini\antigravity\scratch\unimaster-ai\static\app.js'
with open(app_path, 'r', encoding='utf-8') as f:
    js = f.read()

target = '<div class="flex items-center gap-1.5">\n          <button type="button" onclick="toggleCodeWrap'
replacement = '<div class="flex items-center gap-1.5">\n          <button type="button" onclick="askAiAboutWholeCodeSnippet(\'${uid}\', \'${escapeHtml(title)}\', \'${lang}\')" class="btn-soft !py-0.5 !px-2 text-[10px] font-black text-indigo-400 hover:text-indigo-300 flex items-center gap-1 border border-indigo-500/40">\n            <span>🤖</span> <span>Hỏi AI Cả Đoạn Code</span>\n          </button>\n          <button type="button" onclick="toggleCodeWrap'

if target in js:
    js = js.replace(target, replacement, 1)
    with open(app_path, 'w', encoding='utf-8') as f:
        f.write(js)
    print("Added Ask AI Whole Code button to buildCodeWindowHtml header!")
else:
    print("Target not found")
