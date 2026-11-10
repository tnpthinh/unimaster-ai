with open('static/app.js', 'r', encoding='utf-8') as f:
    js_text = f.read()

# 1. Wire rubber duck into runCodeCustomInput
old_run = '''      if (res.compile_error) {
        stdoutEl.textContent = `❌ LỖI BIÊN DỊCH (Compile Error):\\n${res.compile_error}`;
        stdoutEl.className = 'p-2.5 rounded-xl border font-mono text-xs text-rose-400 h-28 overflow-y-auto';
      }'''

new_run = '''      if (res.compile_error) {
        stdoutEl.textContent = `❌ LỖI BIÊN DỊCH (Compile Error):\\n${res.compile_error}`;
        stdoutEl.className = 'p-2.5 rounded-xl border font-mono text-xs text-rose-400 h-28 overflow-y-auto';
        if (typeof triggerRubberDuckOnFailure === 'function') {
          triggerRubberDuckOnFailure(code, lang, res.compile_error);
        }
      }'''

if old_run in js_text:
    js_text = js_text.replace(old_run, new_run)
    print("Wired Rubber Duck to compile error.")
else:
    print("old_run target not matched.")

# 2. Wire rubber duck into submitCodeTestCases
old_submit = '''    } else {
      playSound('error');
      showToast(`Đạt ${res.passed_tests}/${res.total_tests} Test Case.`, 'warning');
    }'''

new_submit = '''    } else {
      playSound('error');
      showToast(`Đạt ${res.passed_tests}/${res.total_tests} Test Case.`, 'warning');
      if (typeof triggerRubberDuckOnFailure === 'function') {
        triggerRubberDuckOnFailure(code, lang, res.memory_leak_warning || `Chỉ đạt ${res.passed_tests}/${res.total_tests} test cases.`);
      }
    }'''

if old_submit in js_text:
    js_text = js_text.replace(old_submit, new_submit)
    print("Wired Rubber Duck to test case failures.")
else:
    print("old_submit target not matched.")

with open('static/app.js', 'w', encoding='utf-8') as f:
    f.write(js_text)

# 3. Add rubber-duck-sidebar to static/index.html inside view-exercises
with open('static/index.html', 'r', encoding='utf-8') as f:
    html_text = f.read()

target_html = '''        <!-- Right: Problem Description & Interactive Code Editor & Test Runner -->
        <div id="exercise-detail-pane" class="lg:col-span-8 uni-card p-5 sm:p-6 space-y-5">'''

replacement_html = '''        <!-- Right: Problem Description & Interactive Code Editor & Test Runner -->
        <div class="lg:col-span-8 space-y-4">
          <!-- Rubber Duck Toxic AI Assistant Sticky Callout -->
          <div id="rubber-duck-sidebar" class="hidden uni-card p-4 border border-amber-500/40 bg-gradient-to-r from-amber-950/40 to-slate-900/60 space-y-2 shadow-lg animate-fade-in">
            <div id="rubber-duck-message-box"></div>
          </div>
          <div id="exercise-detail-pane" class="uni-card p-5 sm:p-6 space-y-5">'''

if target_html in html_text:
    # also close the extra div
    # Find </section> of view-exercises
    idx_end = html_text.find('</section>', html_text.find('id="view-exercises"'))
    # Replace target_html
    html_text = html_text.replace(target_html, replacement_html)
    # And close the wrapper div before </section>
    html_text = html_text[:idx_end] + '</div>\n    ' + html_text[idx_end:]
    with open('static/index.html', 'w', encoding='utf-8') as f:
        f.write(html_text)
    print("Injected rubber-duck-sidebar container into view-exercises.")
else:
    print("target_html in index.html not found.")
