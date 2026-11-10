app_path = r'C:\Users\PC\.gemini\antigravity\scratch\unimaster-ai\static\app.js'
with open(app_path, 'r', encoding='utf-8') as f:
    js = f.read()

target = 'function getLocalExamArchive() {'
addition = '''function saveLocalExamHistory(list) {
  try {
    localStorage.setItem(LOCAL_EXAM_HISTORY_KEY, JSON.stringify(list || []));
  } catch (_) {}
}
window.saveLocalExamHistory = saveLocalExamHistory;

function saveLocalTutorHistory(list) {
  try {
    localStorage.setItem(LOCAL_TUTOR_CHAT_KEY, JSON.stringify(list || []));
  } catch (_) {}
}
window.saveLocalTutorHistory = saveLocalTutorHistory;

function getLocalExamArchive() {'''

if target in js and 'function saveLocalExamHistory(' not in js:
    js = js.replace(target, addition, 1)
    with open(app_path, 'w', encoding='utf-8') as f:
        f.write(js)
    print("Added saveLocalExamHistory and saveLocalTutorHistory to app.js")
else:
    print("Already added or target not found")
