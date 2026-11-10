app_path = r'C:\Users\PC\.gemini\antigravity\scratch\unimaster-ai\static\app.js'
with open(app_path, 'r', encoding='utf-8') as f:
    js = f.read()

target = 'function toggleFloatingTutor() {'
addition = '''function openFloatingTutor() {
  const win = document.getElementById('floating-tutor-window');
  if (win && win.classList.contains('hidden')) {
    toggleFloatingTutor();
  }
}
window.openFloatingTutor = openFloatingTutor;

function toggleFloatingTutor() {'''

if target in js and 'function openFloatingTutor()' not in js:
    js = js.replace(target, addition, 1)
    with open(app_path, 'w', encoding='utf-8') as f:
        f.write(js)
    print("Added openFloatingTutor to app.js")
else:
    print("Already added or target not found")
