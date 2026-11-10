with open('static/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

idx_start = js.find('function renderExerciseDetail()')
idx_end = js.find('async function explainCurrentExercise()')

new_render_code = """function renderExerciseDetail() {
  const pane = document.getElementById('exercise-detail-pane');
  const ex = STATE.exercises.list[STATE.exercises.selectedIndex];
  if (!pane || !ex) return;

  const specs = Array.isArray(ex.specs) ? ex.specs : [];
  const cachedAi = STATE.exercises.aiExplanations[ex.id];
  const userCode = STATE.exercises.userCode[ex.id] || ex.starter_code || `using System;\\n\\nclass Program {\\n    static void Main(string[] args) {\\n        // Viết code giải bài tập tại đây\\n    }\\n}`;
  const testRes = STATE.exercises.testResults[ex.id];

  // Test Results Table HTML
  let testHtml = '';
  if (testRes && testRes.success) {
    const passed = testRes.passed_tests || 0;
    const total = testRes.total_tests || 5;
    const isPassAll = testRes.all_passed;
    testHtml = `
      <div class="mt-4 p-4 rounded-2xl border ${isPassAll ? 'border-emerald-500/40 bg-emerald-950/20' : 'border-rose-500/40 bg-rose-950/20'} space-y-3 animate-fade-in">
        <div class="flex items-center justify-between flex-wrap gap-2">
          <div class="flex items-center gap-2">
            <span class="text-xl">${isPassAll ? '🎉' : '⚠️'}</span>
            <span class="font-extrabold text-sm ${isPassAll ? 'text-emerald-400' : 'text-rose-400'}">
              Kết Quả Chấm: ${passed}/${total} Test Case Đạt
            </span>
          </div>
          <span class="text-xs font-mono txt-muted">${testRes.feedback || ''}</span>
        </div>

        ${testRes.memory_leak_warning ? `<div class="p-2.5 rounded-xl border border-amber-500/40 bg-amber-500/10 text-amber-300 text-xs font-bold">${escapeHtml(testRes.memory_leak_warning)}</div>` : ''}

        <div class="space-y-2 pt-1">
          ${(testRes.results || []).map((tr) => `
            <div class="p-3 rounded-xl border text-xs space-y-1.5" style="background-color: var(--bg-surface); border-color: ${tr.passed ? 'rgba(16,185,129,0.3)' : 'rgba(244,63,94,0.3)'};">
              <div class="flex items-center justify-between font-bold">
                <span class="flex items-center gap-1.5">
                  <span>${tr.passed ? '✅' : '❌'}</span>
                  <span>Test Case #${tr.test_idx} ${tr.is_hidden ? '<span class="badge-amber text-[10px] px-1.5 py-0.2 rounded font-mono">ẨN</span>' : '<span class="badge-brand text-[10px] px-1.5 py-0.2 rounded font-mono">CÔNG KHAI</span>'}</span>
                </span>
                <span class="${tr.passed ? 'text-emerald-400' : 'text-rose-400'} font-extrabold uppercase">${tr.passed ? 'Passed' : 'Failed'} • ${tr.runtime_ms || 0}ms</span>
              </div>
              ${!tr.is_hidden ? `
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-[11px] font-mono pt-1 text-slate-300">
                  <div class="bg-black/30 p-2 rounded-lg"><strong>Input:</strong>\\n${escapeHtml(tr.input || '(Trống)')}</div>
                  <div class="bg-black/30 p-2 rounded-lg"><strong>Kỳ vọng:</strong>\\n${escapeHtml(tr.expected || '')}</div>
                </div>
                ${tr.actual ? `<div class="text-[11px] font-mono bg-black/40 p-2 rounded-lg text-rose-300"><strong>Thực tế trả về:</strong>\\n${escapeHtml(tr.actual)}</div>` : ''}
              ` : `
                <div class="text-[11px] italic txt-muted">Dữ liệu test case được bảo mật để chống hardcode kết quả.</div>
              `}
              ${tr.compile_error ? `<div class="text-[11px] font-mono p-2 rounded-lg bg-rose-500/10 text-rose-300 border border-rose-500/30"><strong>Lỗi biên dịch / Runtime:</strong>\\n${escapeHtml(tr.compile_error)}</div>` : ''}
            </div>
          `).join('')}
        </div>
      </div>
    `;
  }

  pane.innerHTML = `
    <div class="space-y-2 pb-4" style="border-bottom: 1px solid var(--border);">
      <div class="flex items-center justify-between flex-wrap gap-2">
        <span class="badge-brand text-xs px-2.5 py-0.5 rounded-md font-bold">Bài Thực Hành #${STATE.exercises.selectedIndex + 1}</span>
        <div class="flex items-center gap-2">
          <label class="text-xs txt-muted font-bold">Ngôn ngữ:</label>
          <select id="code-lang-select" class="uni-input px-2.5 py-1 text-xs font-bold font-mono">
            <option value="csharp" selected>C# (.NET 8.0)</option>
            <option value="python">Python 3</option>
            <option value="cpp">C++ 17</option>
          </select>
        </div>
      </div>
      <h3 class="text-xl font-extrabold txt-main">${escapeHtml(ex.title)}</h3>
      <p class="text-sm txt-sub leading-relaxed">${formatRichText(ex.problem)}</p>
    </div>

    ${specs.length ? `<ul class="space-y-1.5 text-sm txt-sub">${specs.map((s) => `<li class="flex gap-2"><span class="txt-brand font-bold">▸</span><span>${formatRichText(s)}</span></li>`).join('')}</ul>` : ''}

    <!-- Interactive Code Editor -->
    <div class="space-y-2 pt-2">
      <div class="flex items-center justify-between text-xs font-bold">
        <span class="txt-main flex items-center gap-1.5">
          <span>💻</span> Khu Vực Viết Code &amp; Test Case
        </span>
        <div class="flex items-center gap-2">
          <button type="button" onclick="loadStarterCodeForCurrentExercise()" class="text-[11px] txt-brand underline hover:opacity-80">
            Khôi phục khung code
          </button>
        </div>
      </div>

      <div class="relative rounded-2xl overflow-hidden border border-slate-700 bg-slate-950 shadow-inner">
        <div class="px-3.5 py-2 bg-slate-900 border-b border-slate-800 flex items-center justify-between text-[11px] text-slate-400 font-mono">
          <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-emerald-500 inline-block"></span> Solution.cs</span>
          <span>Phím Tab: Thụt dòng</span>
        </div>
        <textarea id="code-editor-textarea" spellcheck="false"
          class="w-full h-80 p-4 font-mono text-xs sm:text-sm bg-slate-950 text-emerald-400 leading-relaxed resize-y focus:outline-none focus:ring-1 focus:ring-indigo-500 font-medium"
          oninput="saveCurrentExerciseCode(this.value)">${escapeHtml(userCode)}</textarea>
      </div>

      <!-- Action Cluster -->
      <div class="flex flex-wrap items-center justify-between gap-2.5 pt-2">
        <div class="flex flex-wrap items-center gap-2">
          <button type="button" onclick="submitCodeTestCases()" class="btn-primary px-5 py-2.5 text-xs font-black flex items-center gap-2 shadow-lg">
            <span>🧪</span> Chạy 5 Test Case (2 Hiện + 3 Ẩn)
          </button>
          <button type="button" onclick="aiReviewCurrentCode()" class="btn-soft px-3.5 py-2.5 text-xs font-bold flex items-center gap-1.5">
            <span>🤖</span> AI Soi Rò Rỉ &amp; Kiến Trúc
          </button>
          <button type="button" onclick="askRubberDuckCurrentCode()" class="btn-soft text-amber-400 px-3.5 py-2.5 text-xs font-bold flex items-center gap-1.5">
            <span>🦆</span> Vịt Cao Su Trợ Giảng
          </button>
        </div>
        <button type="button" onclick="STATE.exercises.showCode=!STATE.exercises.showCode;renderExerciseDetail();" class="btn-soft px-3.5 py-2 text-xs font-bold">
          ${STATE.exercises.showCode ? '🙈 Ẩn Đáp Án Mẫu' : '👁️ Xem Đáp Án Mẫu'}
        </button>
      </div>
    </div>

    ${testHtml}
    <div id="exercise-ai-box" class="${cachedAi ? '' : 'hidden'} ai-callout ai-callout-indigo markdown-body text-sm mt-3">${cachedAi ? renderMarkdown(cachedAi) : ''}</div>
    <div class="${STATE.exercises.showCode ? '' : 'hidden'} mt-3">${buildCodeWindowHtml(ex.sample_code || '', 'Solution.cs', 'csharp')}</div>
  `;

  setupCodeEditorTabKey();
}

function saveCurrentExerciseCode(val) {
  const ex = STATE.exercises.list[STATE.exercises.selectedIndex];
  if (ex) STATE.exercises.userCode[ex.id] = val;
}

function loadStarterCodeForCurrentExercise() {
  const ex = STATE.exercises.list[STATE.exercises.selectedIndex];
  if (!ex) return;
  const starter = ex.starter_code || ex.sample_code || `using System;\\n\\nclass Program {\\n    static void Main(string[] args) {\\n        // Code của bạn\\n    }\\n}`;
  const editor = document.getElementById('code-editor-textarea');
  if (editor) {
    editor.value = starter;
    saveCurrentExerciseCode(starter);
    showToast('Đã tải khung code ban đầu!', 'info');
  }
}

function setupCodeEditorTabKey() {
  const editor = document.getElementById('code-editor-textarea');
  if (!editor || editor._hasTabListener) return;
  editor._hasTabListener = true;
  editor.addEventListener('keydown', (e) => {
    if (e.key === 'Tab') {
      e.preventDefault();
      const start = editor.selectionStart;
      const end = editor.selectionEnd;
      editor.value = editor.value.substring(0, start) + '    ' + editor.value.substring(end);
      editor.selectionStart = editor.selectionEnd = start + 4;
      saveCurrentExerciseCode(editor.value);
    }
  });
}

async function askRubberDuckCurrentCode() {
  const ex = STATE.exercises.list[STATE.exercises.selectedIndex];
  const editor = document.getElementById('code-editor-textarea');
  if (!ex || !editor) return;
  const code = editor.value;
  const lang = document.getElementById('code-lang-select')?.value || 'csharp';
  showToast('🦆 Vịt Cao Su đang soi code của bạn...', 'info');
  if (typeof triggerRubberDuckOnFailure === 'function') {
    triggerRubberDuckOnFailure(code, lang, 'Sinh viên chủ động nhờ Vịt Cao Su soi lỗi và đặt câu hỏi gợi mở cho bài tập.');
  }
}

"""

if idx_start != -1 and idx_end != -1:
    js = js[:idx_start] + new_render_code + js[idx_end:]
    with open('static/app.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("Replaced renderExerciseDetail in static/app.js!")
else:
    print("Start or End index not found in static/app.js")
