# Script to inject comprehensive client-side modules into static/app.js:
# 1. Automated Practical Code Assessment (Monaco/Ace style editor, custom run, unit test runner, AI reviewer)
# 2. Discrete Math & Algorithms Essay Grader (2-column live LaTeX KaTeX preview, rubric, AI professor evaluation)
# 3. 60-Minute Timed Exam Simulator (40 questions, countdown timer, question palette, flag review, diagnostics)

with open(r'C:\Users\PC\.gemini\antigravity\scratch\unimaster-ai\static\app.js', 'r', encoding='utf-8') as f:
    text = f.read()

v14_modules_code = r'''
// =========================================================================
// UNIMASTER v14.0 MODULE 1: CHẤM THỰC HÀNH LẬP TRÌNH TỰ ĐỘNG (OOP & NNLT 1)
// =========================================================================
if (!STATE.exercises) {
  STATE.exercises = { list: [], selectedIndex: 0, showCode: false, userCode: {}, testResults: {}, aiReviews: {}, currentConsoleTab: 'testcases' };
}
if (!STATE.exercises.userCode) STATE.exercises.userCode = {};
if (!STATE.exercises.testResults) STATE.exercises.testResults = {};
if (!STATE.exercises.aiReviews) STATE.exercises.aiReviews = {};
if (!STATE.exercises.currentConsoleTab) STATE.exercises.currentConsoleTab = 'testcases';

async function loadExercisesView() {
  const sel = document.getElementById('exercise-subject-select');
  let sid = 5; // default OOP
  if (sel && sel.value) {
    sid = Number(sel.value);
  } else if (STATE.activeSubjectId) {
    sid = Number(STATE.activeSubjectId);
  }

  try {
    let res = await apiFetch(`/api/subjects/${sid}/exercises`);
    let list = res && res.exercises ? res.exercises : [];
    if (!list.length) {
      // Fallback: try OOP
      res = await apiFetch('/api/subjects/5/exercises');
      list = res && res.exercises ? res.exercises : [];
    }
    STATE.exercises.list = list;
    STATE.exercises.selectedIndex = 0;
    renderExerciseList();
    renderExerciseDetail();
  } catch (err) {
    console.error('Failed to load exercises:', err);
    showToast('Lỗi tải bài tập thực hành', 'error');
  }
}

function selectExerciseBySubject(subId) {
  const sel = document.getElementById('exercise-subject-select');
  if (sel) sel.value = String(subId);
  loadExercisesView();
}

function renderExerciseList() {
  const container = document.getElementById('exercise-list');
  const badge = document.getElementById('exercise-count-badge');
  const searchInput = document.getElementById('exercise-search');
  if (!container) return;

  const query = (searchInput ? searchInput.value : '').toLowerCase().trim();
  const list = STATE.exercises.list || [];
  if (badge) badge.textContent = `${list.length} bài`;

  const filtered = list.filter((ex) => {
    if (!query) return true;
    return (
      (ex.title || '').toLowerCase().includes(query) ||
      (ex.problem || '').toLowerCase().includes(query) ||
      (ex.difficulty || '').toLowerCase().includes(query)
    );
  });

  if (!filtered.length) {
    container.innerHTML = `<div class="p-4 text-center txt-muted text-xs">Không tìm thấy bài tập phù hợp.</div>`;
    return;
  }

  container.innerHTML = filtered
    .map((ex, idx) => {
      const realIdx = list.indexOf(ex);
      const isSel = realIdx === STATE.exercises.selectedIndex;
      const testRes = STATE.exercises.testResults[ex.id];
      const isPassed = testRes && testRes.all_passed;
      const diffClass = ex.difficulty === 'hard' ? 'badge-rose' : ex.difficulty === 'medium' ? 'badge-amber' : 'badge-emerald';

      return `
      <div onclick="selectExercise(${realIdx})"
        class="p-3 rounded-xl border transition-all cursor-pointer flex items-center justify-between gap-2.5 ${
          isSel
            ? 'bg-violet-600/15 border-violet-500/60 shadow-md ring-1 ring-violet-500/30'
            : 'hover:bg-white/5 border-transparent'
        }">
        <div class="flex items-center gap-2.5 min-w-0">
          <div class="w-7 h-7 rounded-lg flex items-center justify-center font-bold text-xs shrink-0 ${
            isPassed ? 'bg-emerald-500 text-white' : isSel ? 'bg-violet-600 text-white' : 'bg-white/10 txt-muted'
          }">
            ${isPassed ? '✓' : realIdx + 1}
          </div>
          <div class="truncate">
            <h4 class="text-xs font-bold txt-main truncate leading-tight">${escapeHtml(ex.title)}</h4>
            <div class="flex items-center gap-1.5 mt-0.5">
              <span class="${diffClass} text-[10px] px-1.5 py-0.2 rounded font-bold">${ex.difficulty || 'medium'}</span>
              <span class="text-[10px] txt-muted font-mono uppercase">${ex.language || 'cpp'}</span>
            </div>
          </div>
        </div>
        ${isPassed ? '<span class="text-emerald-400 text-xs font-bold shrink-0">Pass ✅</span>' : ''}
      </div>`;
    })
    .join('');
}

function selectExercise(idx) {
  // Save current code before switching
  const curEx = STATE.exercises.list[STATE.exercises.selectedIndex];
  if (curEx) {
    const editor = document.getElementById('code-editor-textarea');
    if (editor) STATE.exercises.userCode[curEx.id] = editor.value;
  }

  STATE.exercises.selectedIndex = idx;
  renderExerciseList();
  renderExerciseDetail();
  playSound('click');
}

function renderExerciseDetail() {
  const pane = document.getElementById('exercise-detail-pane');
  const ex = STATE.exercises.list[STATE.exercises.selectedIndex];
  if (!pane || !ex) return;

  const specs = Array.isArray(ex.specs) ? ex.specs : [];
  let testCases = Array.isArray(ex.test_cases) ? ex.test_cases : [];
  if (!testCases.length && ex.test_cases_json) {
    try { testCases = json.loads(ex.test_cases_json); } catch (_) {}
  }

  const currentCode = STATE.exercises.userCode[ex.id] !== undefined ? STATE.exercises.userCode[ex.id] : (ex.sample_code || '');
  const testRes = STATE.exercises.testResults[ex.id];
  const aiRev = STATE.exercises.aiReviews[ex.id];
  const activeTab = STATE.exercises.currentConsoleTab || 'testcases';

  pane.innerHTML = `
    <!-- Exercise Header -->
    <div class="space-y-3 pb-4 border-b" style="border-color: var(--border);">
      <div class="flex items-center justify-between flex-wrap gap-2">
        <div class="flex items-center gap-2">
          <span class="badge-brand text-xs px-2.5 py-0.5 rounded-md font-bold">Bài #${STATE.exercises.selectedIndex + 1}</span>
          <span class="badge-subtle text-xs px-2 py-0.5 rounded font-mono uppercase">${ex.language || 'cpp'}</span>
          ${testRes && testRes.all_passed ? '<span class="badge-emerald text-xs px-2.5 py-0.5 rounded font-bold">Passed (100%) ✅</span>' : ''}
        </div>
        <div class="flex items-center gap-2">
          <button type="button" onclick="resetExerciseCode()" class="btn-soft px-3 py-1.5 text-xs font-bold text-amber-400 hover:bg-amber-500/10" title="Khôi phục lại code khởi tạo ban đầu">
            ↺ Reset Code Mẫu
          </button>
          <button type="button" onclick="toggleSampleCode()" class="btn-soft px-3 py-1.5 text-xs font-bold">
            ${STATE.exercises.showCode ? '🙈 Ẩn Code Mẫu' : '👁️ Hiện Code Mẫu'}
          </button>
        </div>
      </div>
      <h3 class="text-xl font-extrabold txt-main">${escapeHtml(ex.title)}</h3>
      <div class="text-sm txt-sub leading-relaxed p-3.5 rounded-xl border" style="background: rgba(255,255,255,0.02); border-color: var(--border);">
        ${formatRichText(ex.problem)}
      </div>
      ${
        specs.length
          ? `<div class="space-y-1.5 pt-1">
              <span class="text-[11px] font-bold txt-muted uppercase tracking-wider">Yêu cầu kỹ thuật & Ràng buộc:</span>
              <ul class="space-y-1 text-xs txt-sub">${specs.map((s) => `<li class="flex items-start gap-2"><span class="txt-brand font-bold">▸</span><span>${formatRichText(s)}</span></li>`).join('')}</ul>
            </div>`
          : ''
      }
    </div>

    <!-- Solution Code Callout if toggled -->
    ${
      STATE.exercises.showCode && ex.solution_code
        ? `<div class="p-4 rounded-xl border border-emerald-500/30 bg-emerald-500/5 space-y-2 animate-fade-in">
            <div class="flex items-center justify-between text-xs font-bold text-emerald-400">
              <span>💡 Lời giải mẫu chuẩn (100% Passed):</span>
              <button onclick="copySolutionToEditor()" class="btn-soft !py-1 !px-2.5 text-[11px] font-bold text-emerald-400">
                📋 Dán Vào Editor
              </button>
            </div>
            <pre class="p-3 rounded-lg bg-slate-950 text-xs font-mono text-emerald-300 overflow-x-auto max-h-56"><code>${escapeHtml(ex.solution_code)}</code></pre>
          </div>`
        : ''
    }

    <!-- Interactive Code Editor Area -->
    <div class="space-y-2">
      <!-- Editor Toolbar -->
      <div class="flex items-center justify-between flex-wrap gap-2 px-1">
        <div class="flex items-center gap-2">
          <label class="text-xs font-bold txt-muted">Ngôn ngữ:</label>
          <select id="code-lang-select" class="uni-input px-2.5 py-1 text-xs font-bold font-mono">
            <option value="cpp" ${ex.language === 'cpp' ? 'selected' : ''}>C++ (C++17 / GCC)</option>
            <option value="c" ${ex.language === 'c' ? 'selected' : ''}>C (C11 / GCC)</option>
            <option value="python" ${ex.language === 'python' ? 'selected' : ''}>Python 3 (Native)</option>
            <option value="csharp" ${ex.language === 'csharp' ? 'selected' : ''}>C# (.NET)</option>
            <option value="java" ${ex.language === 'java' ? 'selected' : ''}>Java (OpenJDK)</option>
          </select>
        </div>
        <div class="flex items-center gap-2">
          <button type="button" onclick="runCodeCustomInput()" class="btn-soft px-3.5 py-1.5 text-xs font-bold flex items-center gap-1.5">
            <span>⚡</span> Chạy Thử
          </button>
          <button type="button" onclick="submitCodeTestCases()" class="btn-primary px-4 py-1.5 text-xs font-bold flex items-center gap-1.5 shadow-md">
            <span>🧪</span> Chấm Test Case (Submit)
          </button>
          <button type="button" onclick="aiReviewCurrentCode()" class="ai-chip-btn !py-1.5 !px-3 text-xs flex items-center gap-1.5 font-bold">
            <span>🤖</span> AI Soi Rò Rỉ & Review
          </button>
        </div>
      </div>

      <!-- Editor Container -->
      <div class="rounded-xl border overflow-hidden shadow-inner" style="border-color: rgba(255,255,255,0.1); background: #0b0f19;">
        <div class="px-3.5 py-2 border-b flex items-center justify-between text-xs txt-muted font-mono" style="border-color: rgba(255,255,255,0.06); background: rgba(0,0,0,0.3);">
          <span>editor.${ex.language || 'cpp'}</span>
          <span>Phím Tab = 4 khoảng trắng • Tự động lưu</span>
        </div>
        <textarea id="code-editor-textarea" spellcheck="false"
          onkeydown="handleCodeEditorKey(event)"
          oninput="saveCurrentCodeDebounced()"
          class="w-full h-80 p-4 font-mono text-xs sm:text-sm text-cyan-200 resize-y leading-relaxed outline-none border-none"
          style="background: transparent; tab-size: 4;">${escapeHtml(currentCode)}</textarea>
      </div>
    </div>

    <!-- Output & Test Runner Console Tabs -->
    <div class="uni-card p-4 space-y-3" style="background: rgba(0,0,0,0.25);">
      <!-- Console Tab Buttons -->
      <div class="flex items-center justify-between border-b pb-2 flex-wrap gap-2" style="border-color: var(--border);">
        <div class="flex items-center gap-1">
          <button type="button" onclick="switchConsoleTab('testcases')"
            class="px-3 py-1 rounded-lg text-xs font-bold transition-all ${
              activeTab === 'testcases' ? 'bg-violet-600 text-white shadow-sm' : 'txt-muted hover:text-white'
            }">
            🧪 Kết Quả Test Case ${testRes ? `(${testRes.passed_tests}/${testRes.total_tests})` : ''}
          </button>
          <button type="button" onclick="switchConsoleTab('console')"
            class="px-3 py-1 rounded-lg text-xs font-bold transition-all ${
              activeTab === 'console' ? 'bg-violet-600 text-white shadow-sm' : 'txt-muted hover:text-white'
            }">
            💻 Console & Custom Input
          </button>
          <button type="button" onclick="switchConsoleTab('aireview')"
            class="px-3 py-1 rounded-lg text-xs font-bold transition-all ${
              activeTab === 'aireview' ? 'bg-violet-600 text-white shadow-sm' : 'txt-muted hover:text-white'
            }">
            🤖 AI Review & Rò Rỉ Bộ Nhớ
          </button>
        </div>
        <div id="console-status-indicator" class="text-xs font-bold txt-muted">
          ${testRes ? (testRes.all_passed ? '<span class="text-emerald-400">✅ 100% Test Case Pass</span>' : '<span class="text-amber-400">⚠️ Chưa hoàn thành</span>') : 'Sẵn sàng'}
        </div>
      </div>

      <!-- Tab 1: Test Cases Results -->
      <div id="console-pane-testcases" class="${activeTab === 'testcases' ? '' : 'hidden'} space-y-3">
        ${renderTestCasesPane(ex, testRes)}
      </div>

      <!-- Tab 2: Custom Stdin Console -->
      <div id="console-pane-console" class="${activeTab === 'console' ? '' : 'hidden'} space-y-3">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
          <div class="space-y-1">
            <label class="text-[11px] font-bold txt-muted uppercase tracking-wider">Đầu vào (Custom STDIN):</label>
            <textarea id="custom-stdin-input" placeholder="Nhập dữ liệu stdin thử nghiệm tại đây..."
              class="uni-input w-full h-28 p-2.5 font-mono text-xs"></textarea>
          </div>
          <div class="space-y-1">
            <label class="text-[11px] font-bold txt-muted uppercase tracking-wider">Đầu ra (STDOUT / STDERR):</label>
            <pre id="custom-stdout-output" class="p-2.5 rounded-xl border font-mono text-xs text-emerald-400 h-28 overflow-y-auto"
              style="background: #07090e; border-color: var(--border);">Chưa có dữ liệu chạy.</pre>
          </div>
        </div>
      </div>

      <!-- Tab 3: AI Senior Review Pane -->
      <div id="console-pane-aireview" class="${activeTab === 'aireview' ? '' : 'hidden'} space-y-3">
        ${renderAiReviewPane(aiRev)}
      </div>
    </div>
  `;

  renderAllMathOnPage(pane);
  refreshIcons();
}

function renderTestCasesPane(ex, testRes) {
  if (!testRes) {
    let sampleCases = ex.test_cases || [];
    if (!sampleCases.length && ex.test_cases_json) {
      try { sampleCases = JSON.parse(ex.test_cases_json); } catch (_) {}
    }
    return `
      <div class="text-xs txt-muted p-4 text-center border rounded-xl" style="border-color: var(--border);">
        <p class="font-bold">Chưa có kết quả chấm.</p>
        <p class="mt-1">Bấm nút <strong>🧪 Chấm Test Case (Submit)</strong> để biên dịch và kiểm thử tự động với ${sampleCases.length || 5} test case.</p>
      </div>
    `;
  }

  const results = testRes.results || [];
  return `
    <div class="space-y-3">
      <!-- Summary Bar -->
      <div class="flex items-center justify-between p-3 rounded-xl border ${
        testRes.all_passed ? 'bg-emerald-500/10 border-emerald-500/30' : 'bg-amber-500/10 border-amber-500/30'
      }">
        <div class="flex items-center gap-2">
          <span class="text-lg">${testRes.all_passed ? '🎉' : '⚠️'}</span>
          <span class="text-xs font-extrabold ${testRes.all_passed ? 'text-emerald-400' : 'text-amber-400'}">
            ${escapeHtml(testRes.feedback || '')}
          </span>
        </div>
        <span class="badge-subtle text-xs px-2.5 py-1 rounded font-mono font-bold">
          ${testRes.passed_tests} / ${testRes.total_tests} Passed
        </span>
      </div>

      <!-- Memory leak warning banner -->
      ${
        testRes.memory_leak_warning
          ? `<div class="p-3 rounded-xl border border-rose-500/30 bg-rose-500/10 text-xs text-rose-300 font-bold space-y-1">
              <div class="flex items-center gap-1.5"><i data-lucide="alert-triangle" class="w-4 h-4 text-rose-400"></i> CẢNH BÁO BỘ NHỚ / LOGIC:</div>
              <div class="font-mono text-[11px] font-normal leading-relaxed">${escapeHtml(testRes.memory_leak_warning)}</div>
            </div>`
          : ''
      }

      <!-- Detailed Test Table -->
      <div class="border rounded-xl overflow-hidden text-xs" style="border-color: var(--border);">
        <table class="w-full text-left">
          <thead class="txt-muted border-b uppercase text-[10px] font-bold" style="background: rgba(255,255,255,0.03); border-color: var(--border);">
            <tr>
              <th class="p-2.5">Test</th>
              <th class="p-2.5">Đầu vào (Stdin)</th>
              <th class="p-2.5">Kỳ vọng (Expected)</th>
              <th class="p-2.5">Thực tế (Actual)</th>
              <th class="p-2.5">Thời gian</th>
              <th class="p-2.5 text-right">Trạng thái</th>
            </tr>
          </thead>
          <tbody class="divide-y font-mono" style="border-color: var(--border);">
            ${results
              .map(
                (tc) => `
              <tr class="${tc.passed ? 'bg-emerald-500/5' : 'bg-rose-500/5'}">
                <td class="p-2.5 font-bold txt-main">#${tc.test_idx}</td>
                <td class="p-2.5 text-slate-300 max-w-[140px] truncate" title="${escapeHtml(tc.input)}">${escapeHtml(tc.input || 'None')}</td>
                <td class="p-2.5 text-emerald-300 max-w-[140px] truncate" title="${escapeHtml(tc.expected)}">${escapeHtml(tc.expected || 'None')}</td>
                <td class="p-2.5 ${tc.passed ? 'text-emerald-400' : 'text-rose-400 font-bold'} max-w-[140px] truncate" title="${escapeHtml(tc.actual)}">
                  ${escapeHtml(tc.actual || tc.compile_error || 'Empty')}
                </td>
                <td class="p-2.5 text-slate-400 text-[11px]">${tc.runtime_ms}ms</td>
                <td class="p-2.5 text-right font-bold">
                  ${tc.passed ? '<span class="badge-emerald px-2 py-0.5 rounded text-[10px]">PASSED</span>' : '<span class="badge-rose px-2 py-0.5 rounded text-[10px]">FAILED</span>'}
                </td>
              </tr>`
              )
              .join('')}
          </tbody>
        </table>
      </div>
    </div>
  `;
}

function renderAiReviewPane(aiRev) {
  if (!aiRev) {
    return `
      <div class="text-xs txt-muted p-4 text-center border rounded-xl" style="border-color: var(--border);">
        <p class="font-bold">Chưa có đánh giá từ AI Tech Lead.</p>
        <p class="mt-1">Bấm nút <strong>🤖 AI Soi Rò Rỉ & Review</strong> để AI phân tích cấu trúc OOP, rò rỉ bộ nhớ, độ phức tạp $O(n)$ và gợi ý tối ưu.</p>
      </div>
    `;
  }

  return `
    <div class="space-y-4 animate-fade-in text-xs leading-relaxed">
      <div class="flex items-center justify-between p-3.5 rounded-xl border border-indigo-500/30 bg-indigo-500/10">
        <div>
          <span class="text-xs font-bold text-indigo-300 uppercase">Điểm Đánh Giá Tech Lead</span>
          <h4 class="text-lg font-black text-white">${aiRev.score || 8.5} / 10.0</h4>
        </div>
        <p class="text-xs text-indigo-200 italic max-w-md text-right">${escapeHtml(aiRev.verdict || '')}</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
        <div class="p-3.5 rounded-xl border space-y-1.5" style="border-color: var(--border); background: rgba(255,255,255,0.02);">
          <span class="font-bold text-violet-400 flex items-center gap-1.5">💻 Thiết Kế OOP & Cấu Trúc:</span>
          <p class="txt-sub">${escapeHtml(aiRev.oop_analysis || 'Hợp lệ')}</p>
        </div>
        <div class="p-3.5 rounded-xl border space-y-1.5" style="border-color: var(--border); background: rgba(255,255,255,0.02);">
          <span class="font-bold text-rose-400 flex items-center gap-1.5">🛡️ An Toàn Bộ Nhớ (Memory Safety):</span>
          <p class="txt-sub">${escapeHtml(aiRev.memory_safety || 'Không có rò rỉ bộ nhớ')}</p>
        </div>
      </div>

      <div class="p-3.5 rounded-xl border space-y-1.5" style="border-color: var(--border); background: rgba(255,255,255,0.02);">
        <span class="font-bold text-emerald-400 flex items-center gap-1.5">⚡ Độ Phức Tạp (Complexity):</span>
        <p class="txt-sub font-mono">${escapeHtml(aiRev.complexity || 'O(N)')}</p>
      </div>

      ${
        aiRev.refactoring_tips && aiRev.refactoring_tips.length
          ? `<div class="p-3.5 rounded-xl border space-y-2" style="border-color: var(--border); background: rgba(255,255,255,0.02);">
              <span class="font-bold text-amber-400">💡 Gợi Ý Refactor & Clean Code:</span>
              <ul class="space-y-1">${aiRev.refactoring_tips.map((t) => `<li class="flex items-start gap-2"><span class="text-amber-400">▸</span><span>${escapeHtml(t)}</span></li>`).join('')}</ul>
            </div>`
          : ''
      }
    </div>
  `;
}

function switchConsoleTab(tab) {
  STATE.exercises.currentConsoleTab = tab;
  ['testcases', 'console', 'aireview'].forEach((t) => {
    document.getElementById(`console-pane-${t}`)?.classList.toggle('hidden', t !== tab);
  });
  renderExerciseDetail();
}

function handleCodeEditorKey(e) {
  if (e.key === 'Tab') {
    e.preventDefault();
    const ta = e.target;
    const start = ta.selectionStart;
    const end = ta.selectionEnd;
    ta.value = ta.value.substring(0, start) + '    ' + ta.value.substring(end);
    ta.selectionStart = ta.selectionEnd = start + 4;
  }
}

let saveCodeTimeout = null;
function saveCurrentCodeDebounced() {
  clearTimeout(saveCodeTimeout);
  saveCodeTimeout = setTimeout(() => {
    const ex = STATE.exercises.list[STATE.exercises.selectedIndex];
    const editor = document.getElementById('code-editor-textarea');
    if (ex && editor) {
      STATE.exercises.userCode[ex.id] = editor.value;
    }
  }, 400);
}

function resetExerciseCode() {
  const ex = STATE.exercises.list[STATE.exercises.selectedIndex];
  if (!ex) return;
  const editor = document.getElementById('code-editor-textarea');
  if (editor) {
    editor.value = ex.sample_code || '';
    STATE.exercises.userCode[ex.id] = editor.value;
    showToast('Đã khôi phục lại code mẫu', 'info');
  }
}

function toggleSampleCode() {
  STATE.exercises.showCode = !STATE.exercises.showCode;
  renderExerciseDetail();
}

function copySolutionToEditor() {
  const ex = STATE.exercises.list[STATE.exercises.selectedIndex];
  if (!ex || !ex.solution_code) return;
  const editor = document.getElementById('code-editor-textarea');
  if (editor) {
    editor.value = ex.solution_code;
    STATE.exercises.userCode[ex.id] = editor.value;
    showToast('Đã dán code mẫu vào editor', 'success');
  }
}

async function runCodeCustomInput() {
  const ex = STATE.exercises.list[STATE.exercises.selectedIndex];
  const editor = document.getElementById('code-editor-textarea');
  const langSel = document.getElementById('code-lang-select');
  const stdinEl = document.getElementById('custom-stdin-input');
  const stdoutEl = document.getElementById('custom-stdout-output');
  if (!editor) return;

  const code = editor.value;
  const lang = langSel ? langSel.value : (ex.language || 'cpp');
  const inp = stdinEl ? stdinEl.value : '';

  switchConsoleTab('console');
  if (stdoutEl) stdoutEl.textContent = '⏳ Đang biên dịch và thực thi...';

  try {
    const res = await apiFetch('/api/code/run', {
      method: 'POST',
      body: JSON.stringify({ language: lang, code: code, input_data: inp })
    });

    if (stdoutEl) {
      if (res.compile_error) {
        stdoutEl.textContent = `❌ LỖI BIÊN DỊCH (Compile Error):\n${res.compile_error}`;
        stdoutEl.className = 'p-2.5 rounded-xl border font-mono text-xs text-rose-400 h-28 overflow-y-auto';
      } else {
        stdoutEl.textContent = res.stdout || res.stderr || '(Không có output)';
        stdoutEl.className = 'p-2.5 rounded-xl border font-mono text-xs text-emerald-400 h-28 overflow-y-auto';
      }
    }
    showToast(`Chạy xong trong ${res.runtime_ms || 15}ms`, 'success');
  } catch (err) {
    if (stdoutEl) stdoutEl.textContent = `Lỗi thực thi: ${err.message}`;
    showToast('Lỗi chạy code', 'error');
  }
}

async function submitCodeTestCases() {
  const ex = STATE.exercises.list[STATE.exercises.selectedIndex];
  const editor = document.getElementById('code-editor-textarea');
  const langSel = document.getElementById('code-lang-select');
  if (!ex || !editor) return;

  const code = editor.value;
  const lang = langSel ? langSel.value : (ex.language || 'cpp');

  switchConsoleTab('testcases');
  showToast('Đang chấm test case tự động...', 'info');

  try {
    const res = await apiFetch('/api/code/test', {
      method: 'POST',
      body: JSON.stringify({ exercise_id: ex.id, language: lang, code: code })
    });

    STATE.exercises.testResults[ex.id] = res;
    renderExerciseDetail();
    renderExerciseList();

    if (res.all_passed) {
      playSound('success');
      showToast('🎉 Chúc mừng! Đã vượt qua 100% Test Case!', 'success');
      if (typeof confetti === 'function') {
        confetti({ particleCount: 70, spread: 60, origin: { y: 0.7 } });
      }
    } else {
      playSound('error');
      showToast(`Đạt ${res.passed_tests}/${res.total_tests} Test Case.`, 'warning');
    }
  } catch (err) {
    showToast('Lỗi khi chấm test case: ' + err.message, 'error');
  }
}

async function aiReviewCurrentCode() {
  const ex = STATE.exercises.list[STATE.exercises.selectedIndex];
  const editor = document.getElementById('code-editor-textarea');
  const langSel = document.getElementById('code-lang-select');
  if (!ex || !editor) return;

  const code = editor.value;
  const lang = langSel ? langSel.value : (ex.language || 'cpp');

  switchConsoleTab('aireview');
  showToast('AI Tech Lead đang soi code & rò rỉ bộ nhớ...', 'info');

  try {
    const res = await apiFetch('/api/code/ai-review', {
      method: 'POST',
      body: JSON.stringify({ title: ex.title, problem: ex.problem, code: code, language: lang })
    });

    if (res.review) {
      STATE.exercises.aiReviews[ex.id] = res.review;
      renderExerciseDetail();
      showToast('Đã có đánh giá từ AI Tech Lead!', 'success');
    }
  } catch (err) {
    showToast('Lỗi gọi AI Review: ' + err.message, 'error');
  }
}


// =========================================================================
// UNIMASTER v14.0 MODULE 2: TRỢ GIẢNG CHẤM TỰ LUẬN (TOÁN RỜI RẠC & GIẢI THUẬT)
// =========================================================================
if (!STATE.essay) {
  STATE.essay = { prompts: [], currentPromptId: 'ESSAY_01', drafts: {}, results: {}, showModel: false };
}

async function loadEssayView() {
  try {
    const res = await apiFetch('/api/essay-prompts');
    const prompts = res && res.prompts ? res.prompts : [];
    STATE.essay.prompts = prompts;

    const sel = document.getElementById('essay-prompt-select');
    if (sel && prompts.length) {
      sel.innerHTML = prompts.map((p) => `<option value="${p.id}">${escapeHtml(p.title)}</option>`).join('');
      sel.value = STATE.essay.currentPromptId || prompts[0].id;
    }

    loadSelectedEssayPrompt();
  } catch (err) {
    console.error('Failed to load essay prompts:', err);
  }
}

function loadEssayPromptById(promptId) {
  STATE.essay.currentPromptId = promptId;
  const sel = document.getElementById('essay-prompt-select');
  if (sel) sel.value = promptId;
  loadSelectedEssayPrompt();
}

function loadSelectedEssayPrompt() {
  const sel = document.getElementById('essay-prompt-select');
  const pid = sel ? sel.value : STATE.essay.currentPromptId;
  STATE.essay.currentPromptId = pid;

  const prompt = STATE.essay.prompts.find((p) => p.id === pid) || STATE.essay.prompts[0];
  if (!prompt) return;

  const topicBadge = document.getElementById('essay-topic-badge');
  const titleDisplay = document.getElementById('essay-title-display');
  const questionText = document.getElementById('essay-question-text');
  const rubricList = document.getElementById('essay-rubric-list');
  const modelBox = document.getElementById('essay-model-solution-box');
  const inputEl = document.getElementById('essay-student-input');

  if (topicBadge) topicBadge.textContent = prompt.topic || 'Toán Rời Rạc';
  if (titleDisplay) titleDisplay.textContent = prompt.title || 'Đề Thi Tự Luận';
  if (questionText) questionText.innerHTML = formatRichText(prompt.question_text || '');

  // Render rubric criteria
  const rubric = prompt.rubric || {};
  const criteria = rubric.criteria || [];
  if (rubricList) {
    rubricList.innerHTML = criteria.length
      ? criteria.map((c) => `<div class="flex items-center justify-between p-2 rounded-lg bg-white/5 border border-white/5"><span>${escapeHtml(c.item)}</span><span class="badge-brand text-[10px] px-1.5 py-0.5 rounded font-bold">+${c.points}đ</span></div>`).join('')
      : '<p class="txt-muted italic">Thang điểm 10 chuẩn đại học.</p>';
  }

  if (modelBox) {
    modelBox.innerHTML = formatRichText(prompt.model_solution || '');
  }

  // Restore draft or leave empty
  if (inputEl) {
    inputEl.value = STATE.essay.drafts[pid] || '';
    updateEssayLivePreview();
  }

  // Restore previous result if any
  const resCard = document.getElementById('essay-eval-result-card');
  const cachedRes = STATE.essay.results[pid];
  if (resCard) {
    if (cachedRes) {
      renderEssayResultCard(cachedRes);
      resCard.classList.remove('hidden');
    } else {
      resCard.classList.add('hidden');
    }
  }

  renderAllMathOnPage();
}

function updateEssayLivePreview() {
  const inputEl = document.getElementById('essay-student-input');
  const previewEl = document.getElementById('essay-live-preview');
  if (!inputEl || !previewEl) return;

  const val = inputEl.value;
  STATE.essay.drafts[STATE.essay.currentPromptId] = val;

  if (!val.trim()) {
    previewEl.innerHTML = '<p class="txt-muted italic">Xem trước công thức Toán KaTeX thời gian thực...</p>';
    return;
  }

  previewEl.innerHTML = formatRichText(val);
  renderAllMathOnPage(previewEl);
}

function insertLatex(sym) {
  const ta = document.getElementById('essay-student-input');
  if (!ta) return;
  const start = ta.selectionStart;
  const end = ta.selectionEnd;
  ta.value = ta.value.substring(0, start) + sym + ta.value.substring(end);
  ta.selectionStart = ta.selectionEnd = start + sym.length;
  ta.focus();
  updateEssayLivePreview();
}

function toggleModelSolution() {
  const modelBox = document.getElementById('essay-model-solution-box');
  if (!modelBox) return;
  STATE.essay.showModel = !STATE.essay.showModel;
  modelBox.classList.toggle('hidden', !STATE.essay.showModel);
  renderAllMathOnPage(modelBox);
}

function clearEssayInput() {
  const inputEl = document.getElementById('essay-student-input');
  if (inputEl) {
    inputEl.value = '';
    STATE.essay.drafts[STATE.essay.currentPromptId] = '';
    updateEssayLivePreview();
  }
}

function loadSampleAnswerForPrompt() {
  const pid = STATE.essay.currentPromptId;
  const prompt = STATE.essay.prompts.find((p) => p.id === pid);
  if (!prompt) return;
  const inputEl = document.getElementById('essay-student-input');
  if (inputEl) {
    inputEl.value = prompt.model_solution || '';
    updateEssayLivePreview();
    showToast('Đã điền bài giải mẫu vào ô làm bài', 'info');
  }
}

async function triggerGradeEssay() {
  const pid = STATE.essay.currentPromptId;
  const prompt = STATE.essay.prompts.find((p) => p.id === pid);
  const inputEl = document.getElementById('essay-student-input');
  const resCard = document.getElementById('essay-eval-result-card');
  if (!inputEl || !resCard) return;

  const studentAns = inputEl.value.trim();
  if (!studentAns) {
    showToast('Vui lòng gõ bài làm trước khi nộp chấm!', 'warning');
    return;
  }

  resCard.classList.remove('hidden');
  resCard.innerHTML = `
    <div class="py-8 text-center space-y-3">
      <div class="w-10 h-10 border-4 border-violet-500 border-t-transparent rounded-full animate-spin mx-auto"></div>
      <p class="font-extrabold text-sm txt-main">Giáo sư AI đang phân tích từng bước logic và so khớp barem...</p>
    </div>
  `;
  resCard.scrollIntoView({ behavior: 'smooth' });

  try {
    const res = await apiFetch('/api/ai/grade-essay-advanced', {
      method: 'POST',
      body: JSON.stringify({
        prompt_id: pid,
        student_answer: studentAns,
        question_text: prompt ? prompt.question_text : '',
        rubric: prompt ? prompt.rubric : {}
      })
    });

    const gradeData = res.result || {};
    STATE.essay.results[pid] = gradeData;
    renderEssayResultCard(gradeData);
    playSound(gradeData.score >= 8.0 ? 'success' : 'click');
    if (gradeData.score >= 8.0 && typeof confetti === 'function') {
      confetti({ particleCount: 80, spread: 70, origin: { y: 0.6 } });
    }
  } catch (err) {
    resCard.innerHTML = `<div class="p-4 text-center txt-rose text-xs">Lỗi chấm bài tự luận: ${escapeHtml(err.message)}</div>`;
  }
}

function renderEssayResultCard(data) {
  const resCard = document.getElementById('essay-eval-result-card');
  if (!resCard) return;

  const score = Number(data.score || 0).toFixed(1);
  const scoreBadgeClass = score >= 8.5 ? 'text-emerald-400 border-emerald-500/40 bg-emerald-500/10' : score >= 6.5 ? 'text-amber-400 border-amber-500/40 bg-amber-500/10' : 'text-rose-400 border-rose-500/40 bg-rose-500/10';

  const steps = Array.isArray(data.logic_steps) ? data.logic_steps : [];
  const missing = Array.isArray(data.missing_cases) ? data.missing_cases : [];
  const strengths = Array.isArray(data.strengths) ? data.strengths : [];

  resCard.innerHTML = `
    <!-- Top Result Banner -->
    <div class="flex items-center justify-between p-4 rounded-xl border ${scoreBadgeClass} flex-wrap gap-3">
      <div>
        <span class="text-[11px] font-bold uppercase tracking-wider">KẾT QUẢ CHẤM THI TỰ LUẬN:</span>
        <h3 class="text-2xl font-black text-white mt-0.5">${score} / 10.0</h3>
      </div>
      <p class="text-xs italic max-w-md text-right leading-relaxed">${escapeHtml(data.verdict || '')}</p>
    </div>

    <!-- Step by Step Logic Analysis -->
    <div class="space-y-2">
      <h4 class="text-xs font-bold uppercase tracking-wider txt-muted flex items-center gap-1.5">
        <i data-lucide="git-commit" class="w-3.5 h-3.5"></i> Phân Tích Logic Từng Bước:
      </h4>
      <div class="space-y-1.5">
        ${
          steps.length
            ? steps
                .map((st) => {
                  const isPass = st.status === 'pass';
                  const isWarn = st.status === 'warning';
                  const cls = isPass ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-300' : isWarn ? 'bg-amber-500/10 border-amber-500/30 text-amber-300' : 'bg-rose-500/10 border-rose-500/30 text-rose-300';
                  const icon = isPass ? '✅' : isWarn ? '⚠️' : '❌';
                  return `
                  <div class="p-3 rounded-xl border ${cls} flex items-start gap-2.5 text-xs">
                    <span class="shrink-0 text-sm">${icon}</span>
                    <div>
                      <span class="font-bold">${escapeHtml(st.step || '')}:</span>
                      <span class="ml-1 leading-relaxed">${formatRichText(st.comment || '')}</span>
                    </div>
                  </div>`;
                })
                .join('')
            : '<p class="text-xs txt-muted italic">Lập luận mạch lạc.</p>'
        }
      </div>
    </div>

    <!-- Missing Cases & Edge Cases -->
    ${
      missing.length
        ? `<div class="p-4 rounded-xl border border-amber-500/30 bg-amber-500/5 space-y-2">
            <h4 class="text-xs font-bold text-amber-400 uppercase tracking-wider flex items-center gap-1.5">
              <span>⚠️</span> Các trường hợp còn thiếu hoặc chưa chứng minh:
            </h4>
            <ul class="space-y-1 text-xs txt-sub">${missing.map((m) => `<li class="flex items-start gap-2"><span class="text-amber-400 font-bold">▸</span><span>${formatRichText(m)}</span></li>`).join('')}</ul>
          </div>`
        : ''
    }

    <!-- Complexity Analysis -->
    ${
      data.complexity_analysis
        ? `<div class="p-3.5 rounded-xl border space-y-1 text-xs" style="border-color: var(--border); background: rgba(255,255,255,0.02);">
            <span class="font-bold text-indigo-400">⚡ Đánh giá độ phức tạp giải thuật:</span>
            <p class="txt-sub font-mono">${escapeHtml(data.complexity_analysis)}</p>
          </div>`
        : ''
    }

    <!-- Strengths -->
    ${
      strengths.length
        ? `<div class="p-3 rounded-xl border border-emerald-500/20 bg-emerald-500/5 text-xs txt-sub space-y-1">
            <span class="font-bold text-emerald-400">🌟 Điểm mạnh của bài làm:</span>
            <ul class="space-y-0.5">${strengths.map((s) => `<li>• ${escapeHtml(s)}</li>`).join('')}</ul>
          </div>`
        : ''
    }
  `;

  renderAllMathOnPage(resCard);
  refreshIcons();
}


// =========================================================================
// UNIMASTER v14.0 MODULE 3: THI THỬ GIỚI HẠN THỜI GIAN 60 PHÚT (40 CÂU)
// =========================================================================
window.TIMED_EXAM = {
  active: false,
  subjectId: 5,
  subjectName: '',
  questions: [],
  currentIndex: 0,
  answers: {},
  flags: {},
  remainingSeconds: 3600,
  timerInterval: null
};

async function startTimedExamForSubject(subjectId, durationMinutes = 60, count = 40) {
  showToast('Đang tạo đề thi thử 40 câu ngẫu nhiên...', 'info');
  try {
    const res = await apiFetch(`/api/timed-exam/start?subject_id=${subjectId}&count=${count}&duration=${durationMinutes}`);
    if (!res.success || !res.questions || !res.questions.length) {
      showToast('Không thể tải câu hỏi thi thử môn này', 'error');
      return;
    }

    window.TIMED_EXAM = {
      active: true,
      subjectId: subjectId,
      subjectName: res.subject_name || 'Môn thi',
      questions: res.questions,
      currentIndex: 0,
      answers: {},
      flags: {},
      remainingSeconds: res.duration_seconds || durationMinutes * 60,
      timerInterval: null
    };

    const modal = document.getElementById('modal-timed-exam');
    const titleEl = document.getElementById('timed-exam-title');
    const resultPane = document.getElementById('timed-exam-result-pane');
    if (resultPane) resultPane.classList.add('hidden');
    if (modal) modal.classList.remove('hidden');
    if (titleEl) titleEl.textContent = `Thi Thử 60p: ${window.TIMED_EXAM.subjectName}`;

    // Start Clock
    clearInterval(window.TIMED_EXAM.timerInterval);
    updateTimedExamClockDisplay();
    window.TIMED_EXAM.timerInterval = setInterval(() => {
      window.TIMED_EXAM.remainingSeconds--;
      updateTimedExamClockDisplay();
      if (window.TIMED_EXAM.remainingSeconds <= 0) {
        clearInterval(window.TIMED_EXAM.timerInterval);
        showToast('⏱️ Hết giờ làm bài! Hệ thống tự động nộp bài.', 'warning');
        submitTimedExamNow(true);
      }
    }, 1000);

    renderTimedExamPalette();
    renderTimedExamQuestion(0);
    playSound('start');
  } catch (err) {
    showToast('Lỗi khởi tạo phòng thi: ' + err.message, 'error');
  }
}

function updateTimedExamClockDisplay() {
  const clock = document.getElementById('timed-exam-clock');
  if (!clock) return;
  const sec = Math.max(0, window.TIMED_EXAM.remainingSeconds);
  const m = Math.floor(sec / 60);
  const s = sec % 60;
  clock.textContent = `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;

  if (sec < 300) {
    clock.className = 'px-4 py-2 rounded-xl border font-mono text-base sm:text-lg font-black tracking-wider text-rose-400 border-rose-500/60 bg-rose-500/20 animate-pulse';
  } else {
    clock.className = 'px-4 py-2 rounded-xl border font-mono text-base sm:text-lg font-black tracking-wider text-emerald-400 border-emerald-500/40 bg-emerald-500/10';
  }
}

function renderTimedExamPalette() {
  const palette = document.getElementById('timed-exam-palette');
  const progressText = document.getElementById('timed-exam-progress-text');
  if (!palette) return;

  const qs = window.TIMED_EXAM.questions || [];
  const ansCount = Object.keys(window.TIMED_EXAM.answers).length;
  if (progressText) progressText.textContent = `Đã làm ${ansCount}/${qs.length} câu`;

  palette.innerHTML = qs
    .map((q, idx) => {
      const isCur = idx === window.TIMED_EXAM.currentIndex;
      const isAnswered = window.TIMED_EXAM.answers[q.id] !== undefined;
      const isFlagged = window.TIMED_EXAM.flags[q.id] === true;

      let btnClass = 'bg-white/5 text-slate-300 border-transparent hover:bg-white/10';
      if (isAnswered) btnClass = 'bg-violet-600 text-white font-bold border-violet-400';
      if (isFlagged) btnClass = 'bg-amber-500/80 text-white font-bold border-amber-300';
      if (isCur) btnClass += ' ring-2 ring-cyan-400 scale-105';

      return `
      <button type="button" onclick="goToTimedQuestion(${idx})"
        class="h-9 rounded-lg border flex items-center justify-center text-xs font-bold transition-all ${btnClass}">
        ${idx + 1}
      </button>`;
    })
    .join('');
}

function renderTimedExamQuestion(idx) {
  window.TIMED_EXAM.currentIndex = idx;
  const q = window.TIMED_EXAM.questions[idx];
  if (!q) return;

  const idxBadge = document.getElementById('timed-q-index-badge');
  const topicBadge = document.getElementById('timed-q-topic-badge');
  const qText = document.getElementById('timed-q-text');
  const codeBox = document.getElementById('timed-q-code-container');
  const optionsBox = document.getElementById('timed-q-options-container');
  const flagText = document.getElementById('timed-flag-text');
  const flagBtn = document.getElementById('timed-flag-btn');

  if (idxBadge) idxBadge.textContent = `Câu ${idx + 1} / ${window.TIMED_EXAM.questions.length}`;
  if (topicBadge) topicBadge.textContent = q.topic_tag || 'Kiến thức chung';
  if (qText) qText.innerHTML = formatRichText(q.question_text);

  if (codeBox) {
    if (q.code_snippet && q.code_snippet.trim()) {
      codeBox.classList.remove('hidden');
      codeBox.innerHTML = `<pre class="p-3.5 rounded-xl bg-slate-950 font-mono text-xs text-cyan-300 overflow-x-auto border border-white/5"><code>${escapeHtml(q.code_snippet)}</code></pre>`;
    } else {
      codeBox.classList.add('hidden');
    }
  }

  const userChoice = window.TIMED_EXAM.answers[q.id];
  const isFlagged = window.TIMED_EXAM.flags[q.id] === true;

  if (flagText) flagText.textContent = isFlagged ? 'Đang gắn cờ (Bỏ cờ)' : 'Gắn cờ xem lại';
  if (flagBtn) flagBtn.className = isFlagged ? 'btn-soft px-3 py-1.5 text-xs w-full font-bold flex items-center justify-center gap-1.5 bg-amber-500/20 text-amber-300 border-amber-500/40' : 'btn-soft px-3 py-1.5 text-xs w-full font-bold flex items-center justify-center gap-1.5';

  const opts = [
    { key: 'A', text: q.option_a },
    { key: 'B', text: q.option_b },
    { key: 'C', text: q.option_c },
    { key: 'D', text: q.option_d }
  ].filter((o) => o.text && o.text.trim());

  if (optionsBox) {
    optionsBox.innerHTML = opts
      .map((o) => {
        const isSel = userChoice === o.key;
        return `
        <div onclick="selectTimedExamOption('${o.key}')"
          class="p-3.5 rounded-xl border transition-all cursor-pointer flex items-center gap-3.5 ${
            isSel
              ? 'bg-violet-600 text-white font-extrabold border-violet-400 shadow-md scale-[1.01]'
              : 'hover:bg-white/5 border-white/10 txt-sub'
          }">
          <div class="w-7 h-7 rounded-lg flex items-center justify-center font-bold text-xs shrink-0 ${
            isSel ? 'bg-white text-violet-700' : 'bg-white/10 text-slate-300'
          }">
            ${o.key}
          </div>
          <span class="text-xs sm:text-sm leading-relaxed">${formatRichText(o.text)}</span>
        </div>`;
      })
      .join('');
  }

  renderTimedExamPalette();
  renderAllMathOnPage();
}

function selectTimedExamOption(opt) {
  const q = window.TIMED_EXAM.questions[window.TIMED_EXAM.currentIndex];
  if (!q) return;
  window.TIMED_EXAM.answers[q.id] = opt;
  playSound('click');
  renderTimedExamQuestion(window.TIMED_EXAM.currentIndex);
}

function toggleFlagCurrentQuestion() {
  const q = window.TIMED_EXAM.questions[window.TIMED_EXAM.currentIndex];
  if (!q) return;
  window.TIMED_EXAM.flags[q.id] = !window.TIMED_EXAM.flags[q.id];
  renderTimedExamQuestion(window.TIMED_EXAM.currentIndex);
}

function goToTimedQuestion(idx) {
  renderTimedExamQuestion(idx);
}

function nextTimedQuestion() {
  if (window.TIMED_EXAM.currentIndex < window.TIMED_EXAM.questions.length - 1) {
    renderTimedExamQuestion(window.TIMED_EXAM.currentIndex + 1);
  }
}

function prevTimedQuestion() {
  if (window.TIMED_EXAM.currentIndex > 0) {
    renderTimedExamQuestion(window.TIMED_EXAM.currentIndex - 1);
  }
}

function confirmSubmitTimedExam() {
  const total = window.TIMED_EXAM.questions.length;
  const answered = Object.keys(window.TIMED_EXAM.answers).length;
  const unanswered = total - answered;

  let msg = `Bạn đã hoàn thành ${answered}/${total} câu hỏi.`;
  if (unanswered > 0) {
    msg += ` Còn ${unanswered} câu chưa chọn đáp án! Bạn có chắc chắn muốn nộp bài ngay bây giờ?`;
  } else {
    msg += ` Bạn có chắc chắn muốn nộp bài?`;
  }

  if (confirm(msg)) {
    submitTimedExamNow(false);
  }
}

function exitTimedExam() {
  if (confirm('Bạn có chắc chắn muốn thoát phòng thi? Tiến trình thi hiện tại sẽ không được lưu.')) {
    clearInterval(window.TIMED_EXAM.timerInterval);
    window.TIMED_EXAM.active = false;
    document.getElementById('modal-timed-exam')?.classList.add('hidden');
  }
}

async function submitTimedExamNow(isAuto = false) {
  clearInterval(window.TIMED_EXAM.timerInterval);
  const totalTime = 3600;
  const spent = totalTime - Math.max(0, window.TIMED_EXAM.remainingSeconds);

  showToast('Đang chấm điểm bài thi...', 'info');

  try {
    const res = await apiFetch('/api/timed-exam/submit', {
      method: 'POST',
      body: JSON.stringify({
        subject_id: window.TIMED_EXAM.subjectId,
        answers: window.TIMED_EXAM.answers,
        time_spent_seconds: spent
      })
    });

    renderTimedExamReport(res);
  } catch (err) {
    showToast('Lỗi khi nộp bài thi: ' + err.message, 'error');
  }
}

function renderTimedExamReport(res) {
  const resultPane = document.getElementById('timed-exam-result-pane');
  if (!resultPane) return;

  resultPane.classList.remove('hidden');
  const score = Number(res.score || 0).toFixed(1);
  const isHigh = score >= 8.0;

  if (isHigh && typeof confetti === 'function') {
    confetti({ particleCount: 120, spread: 80, origin: { y: 0.5 } });
  }

  const breakdown = res.breakdown || [];

  resultPane.innerHTML = `
    <div class="space-y-4">
      <div class="text-4xl">${isHigh ? '🏆' : '📚'}</div>
      <h3 class="text-2xl font-black txt-main">KẾT QUẢ BÀI THI THỬ 60 PHÚT</h3>
      <div class="inline-block p-4 rounded-2xl border ${
        isHigh ? 'bg-emerald-500/10 border-emerald-500/40 text-emerald-400' : 'bg-violet-500/10 border-violet-500/40 text-violet-400'
      }">
        <span class="text-xs uppercase font-bold tracking-wider">ĐIỂM SỐ ĐẠT ĐƯỢC (THANG 10)</span>
        <div class="text-4xl font-black mt-1">${score} / 10.0</div>
        <p class="text-xs mt-1 font-bold">${res.correct_answers} / ${res.total_questions} câu đúng (${Math.round((res.correct_answers/res.total_questions)*100)}%)</p>
      </div>

      <div class="flex items-center justify-center gap-3 pt-2">
        <button onclick="document.getElementById('modal-timed-exam').classList.add('hidden'); switchTab('dashboard');" class="btn-primary px-5 py-2.5 text-xs font-bold">
          Quay Về Trang Chủ
        </button>
        <button onclick="startTimedExamForSubject(${window.TIMED_EXAM.subjectId}, 60, 40)" class="btn-soft px-5 py-2.5 text-xs font-bold">
          Thi Lại Đề Khác
        </button>
      </div>

      <!-- Detailed Review per question -->
      <div class="pt-6 border-t text-left space-y-4 max-h-[460px] overflow-y-auto pr-1" style="border-color: var(--border);">
        <h4 class="text-xs font-extrabold uppercase txt-muted tracking-wider">CHI TIẾT TỪNG CÂU HỎI & GIẢI THÍCH:</h4>
        <div class="space-y-3">
          ${breakdown
            .map(
              (q, i) => `
            <div class="p-3.5 rounded-xl border text-xs leading-relaxed space-y-2 ${
              q.is_correct ? 'bg-emerald-500/5 border-emerald-500/20' : 'bg-rose-500/5 border-rose-500/20'
            }">
              <div class="flex items-center justify-between font-bold">
                <span>Câu #${i + 1} (${q.topic_tag || 'Tổng hợp'})</span>
                <span class="${q.is_correct ? 'text-emerald-400' : 'text-rose-400'}">${q.is_correct ? 'ĐÚNG ✅' : 'SAI ❌'}</span>
              </div>
              <p class="font-bold txt-main">${formatRichText(q.question_text)}</p>
              ${q.code_snippet ? `<pre class="p-2 rounded bg-slate-950 font-mono text-[11px] text-cyan-300"><code>${escapeHtml(q.code_snippet)}</code></pre>` : ''}
              <div class="flex items-center gap-4 text-[11px] font-bold">
                <span class="${q.is_correct ? 'text-emerald-400' : 'text-rose-400'}">Bạn chọn: ${q.user_choice || '(Bỏ trống)'}</span>
                <span class="text-emerald-400">Đáp án đúng: ${q.correct_choice}</span>
              </div>
              ${q.explanation ? `<div class="p-2.5 rounded-lg bg-black/30 border border-white/5 text-[11px] txt-sub leading-normal"><strong>Giải thích:</strong> ${formatRichText(q.explanation)}</div>` : ''}
            </div>`
            )
            .join('')}
        </div>
      </div>
    </div>
  `;

  renderAllMathOnPage(resultPane);
}
'''

with open(r'C:\Users\PC\.gemini\antigravity\scratch\unimaster-ai\static\app.js', 'a', encoding='utf-8') as f:
    f.write('\n' + v14_modules_code)

print("v14 engines injected into static/app.js successfully.")
