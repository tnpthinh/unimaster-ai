import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app_path = os.path.join(BASE_DIR, "static", "app.js")

with open(app_path, "r", encoding="utf-8") as f:
    app_content = f.read()

start_marker = "function renderExerciseDetail(ex) {"
end_marker = "function renderInitialTestCases(testCases) {"

s_idx = app_content.find(start_marker)
e_idx = app_content.find(end_marker)

print(f"s_idx: {s_idx}, e_idx: {e_idx}")
if s_idx == -1 or e_idx == -1:
    print("Error: Could not locate markers in static/app.js")
    sys.exit(1)

new_impl = r'''function renderExerciseDetail(ex) {
  const container = document.getElementById('exercise-detail-content');
  if (!container) return;

  const currentCode = (state.userCode[ex.id] !== undefined)
    ? state.userCode[ex.id]
    : (ex.initial_code || '');

  const langNames = {
    csharp: 'C# (Roslyn .NET 8)',
    python: 'Python 3.12 (CPython)',
    cpp: 'C++20 (GCC)'
  };
  const langFiles = {
    csharp: 'Program.cs',
    python: 'solution.py',
    cpp: 'main.cpp'
  };

  const currLang = ex.language || 'csharp';
  const currFile = langFiles[currLang] || 'solution.cs';

  container.innerHTML = `
    <!-- VISUAL STUDIO / VS CODE IDE CONTAINER -->
    <div class="vscode-ide-container" id="vscode-ide-workspace">
      <!-- TITLEBAR -->
      <div class="vscode-titlebar">
        <div class="vscode-titlebar-controls">
          <span class="mac-btn mac-close" onclick="closeExerciseModal()" title="Đóng bài tập"></span>
          <span class="mac-btn mac-min" onclick="toggleVscodeSidebar()" title="Ẩn/Hiện đề bài"></span>
          <span class="mac-btn mac-max" onclick="toggleVscodeFullscreen()" title="Chế độ IDE toàn màn hình"></span>
        </div>
        <div class="vscode-titlebar-title truncate max-w-md">
          <span>UniMaster IDE</span>
          <span class="text-slate-600">—</span>
          <span>${escapeHtml(ex.title)}</span>
          <span class="text-slate-600">—</span>
          <span class="text-[#858585]">${currFile}</span>
        </div>
        <div class="flex items-center gap-2">
          <button onclick="resetCurrentExerciseCode()" title="Khôi phục mã nguồn ban đầu" class="px-2 py-0.5 text-xs text-slate-400 hover:text-white bg-[#252526] hover:bg-[#333] border border-[#3c3c3c] rounded transition">
            ↺ Reset
          </button>
          <button onclick="toggleExerciseSampleCode()" title="Xem bài giải mẫu" class="px-2 py-0.5 text-xs text-amber-400 hover:text-amber-300 bg-[#252526] hover:bg-[#333] border border-[#3c3c3c] rounded transition">
            💡 Giải mẫu
          </button>
          <button onclick="toggleVscodeFullscreen()" title="Phóng to IDE toàn màn hình" class="px-2 py-0.5 text-xs text-blue-400 hover:text-blue-300 bg-[#252526] hover:bg-[#333] border border-[#3c3c3c] rounded transition">
            ⛶ Phóng to IDE
          </button>
        </div>
      </div>

      <!-- WORKBENCH BODY -->
      <div class="vscode-workbench">
        <!-- ACTIVITY BAR -->
        <div class="vscode-activitybar">
          <div class="vscode-activity-icon active" id="act-explorer" onclick="switchActivityBar('explorer')" title="Explorer (Đề bài & Ràng buộc)">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>
          </div>
          <div class="vscode-activity-icon" id="act-run" onclick="switchConsoleTab('terminal'); runExerciseCode();" title="Chạy chương trình (Ctrl+F5)">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
          </div>
          <div class="vscode-activity-icon" id="act-test" onclick="switchConsoleTab('testcases'); submitExerciseSolution();" title="Chấm điểm Test Cases">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
          </div>
          <div class="vscode-activity-icon" id="act-ai-review" onclick="switchConsoleTab('review'); runExerciseAiReview();" title="Senior AI Review Code">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/></svg>
          </div>
          <div class="vscode-activity-icon" id="act-tutor" onclick="openExerciseTutor()" title="Hỏi gia sư AI Gemini">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"/></svg>
          </div>
        </div>

        <!-- SIDEBAR (EXPLORER) -->
        <div class="vscode-sidebar" id="vscode-sidebar">
          <div class="vscode-sidebar-header flex items-center justify-between">
            <span>EXPLORER: ĐỀ BÀI</span>
            <button onclick="toggleVscodeSidebar()" class="text-slate-400 hover:text-white text-xs">✕</button>
          </div>
          <div class="vscode-sidebar-content space-y-4">
            <div>
              <div class="flex items-center gap-1.5 font-bold text-white text-sm mb-1">
                <span>📄</span>
                <span>${escapeHtml(ex.title)}</span>
              </div>
              <div class="flex items-center gap-2 mb-3">
                <span class="px-2 py-0.5 rounded text-[11px] font-semibold ${getDifficultyBadgeClass(ex.difficulty)}">${escapeHtml(ex.difficulty_text || ex.difficulty)}</span>
                <span class="text-xs text-slate-400 font-mono">${escapeHtml(currLang.toUpperCase())}</span>
                <span class="text-xs text-amber-400 font-semibold">+${ex.points || 10} pts</span>
              </div>
              <div class="prose prose-invert text-xs text-slate-300 leading-relaxed max-h-60 overflow-y-auto pr-1 border-b border-[#3c3c3c] pb-3">
                ${formatMarkdown(ex.description || 'Chưa có mô tả chi tiết.')}
              </div>
            </div>

            ${(ex.constraints && ex.constraints.length) ? `
            <div>
              <div class="text-[11px] font-bold uppercase tracking-wider text-slate-400 mb-1.5 flex items-center gap-1">
                <span>⚡</span> Ràng buộc (Constraints)
              </div>
              <ul class="text-xs text-slate-300 space-y-1 font-mono bg-[#181818] p-2.5 rounded border border-[#333]">
                ${ex.constraints.map(c => `<li>• ${escapeHtml(c)}</li>`).join('')}
              </ul>
            </div>` : ''}

            ${(ex.test_cases && ex.test_cases.length) ? `
            <div>
              <div class="text-[11px] font-bold uppercase tracking-wider text-slate-400 mb-1.5 flex items-center gap-1">
                <span>🧪</span> Ví dụ mẫu (Sample I/O)
              </div>
              <div class="space-y-2">
                ${ex.test_cases.slice(0, 2).map((tc, idx) => `
                <div class="bg-[#181818] p-2 rounded border border-[#333] text-xs font-mono">
                  <div class="text-[10px] text-slate-400 uppercase font-semibold mb-1">Ví dụ #${idx + 1}</div>
                  <div class="text-slate-400">Input: <span class="text-slate-200 font-semibold">${escapeHtml(tc.input || '(trống)')}</span></div>
                  <div class="text-slate-400">Output: <span class="text-emerald-400 font-semibold">${escapeHtml(tc.expected_output || tc.output || '')}</span></div>
                </div>`).join('')}
              </div>
            </div>` : ''}
          </div>
        </div>

        <!-- EDITOR STAGE -->
        <div class="vscode-editor-stage">
          <!-- TABS BAR -->
          <div class="vscode-tabs-bar">
            <div class="vscode-tab active" id="tab-active-file">
              <span class="text-blue-400 text-xs">${currLang === 'csharp' ? '🔷' : (currLang === 'python' ? '🐍' : '⚙️')}</span>
              <span>${currFile}</span>
              <span class="text-slate-500 hover:text-white text-xs cursor-pointer ml-1" title="Đóng">✕</span>
            </div>
            <div class="ml-auto flex items-center gap-2 pr-3">
              <select onchange="changeExerciseLanguage(this.value)" class="bg-[#252526] text-slate-200 text-xs px-2 py-1 rounded border border-[#3c3c3c] focus:outline-none focus:border-[#007acc]">
                <option value="csharp" ${currLang === 'csharp' ? 'selected' : ''}>C# (.NET 8)</option>
                <option value="python" ${currLang === 'python' ? 'selected' : ''}>Python 3.12</option>
                <option value="cpp" ${currLang === 'cpp' ? 'selected' : ''}>C++20</option>
              </select>
            </div>
          </div>

          <!-- BREADCRUMBS -->
          <div class="vscode-breadcrumbs">
            <span>src</span>
            <span>›</span>
            <span>exercises</span>
            <span>›</span>
            <span>${escapeHtml(currLang)}</span>
            <span>›</span>
            <span class="text-white font-semibold">${currFile}</span>
          </div>

          <!-- TOOLBAR -->
          <div class="vscode-action-toolbar">
            <button onclick="switchConsoleTab('terminal'); runExerciseCode();" class="vscode-tool-btn btn-run shadow-sm" title="Biên dịch và chạy thử (Ctrl+Enter)">
              <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clip-rule="evenodd"/></svg>
              <span>Chạy code</span>
            </button>
            <button onclick="switchConsoleTab('testcases'); submitExerciseSolution();" class="vscode-tool-btn btn-submit shadow-sm" title="Nộp bài chấm điểm testcase">
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
              <span>Chấm test</span>
            </button>
            <div class="h-4 w-px bg-[#3c3c3c] mx-0.5"></div>
            <button onclick="triggerVscodeCopilotSuggest()" class="vscode-tool-btn btn-tutor" title="AI Copilot gợi ý dòng code tiếp theo (Phím tắt: Alt+\\ hoặc Tab)">
              <span>✨ Gợi ý tiếp (Tab)</span>
            </button>
            <button onclick="switchConsoleTab('review'); runExerciseAiReview();" class="vscode-tool-btn btn-ai" title="Nhờ AI Senior Architect chấm điểm và nhận xét thuật toán">
              <span>🤖 AI Review</span>
            </button>
            <button onclick="switchConsoleTab('fix'); runExerciseFixAndUpgrade();" class="vscode-tool-btn btn-fix" title="Tự động chẩn đoán lỗi cú pháp/logic và nâng cấp Clean Code">
              <span>🛠️ Sửa & Tối ưu</span>
            </button>
            <button onclick="openExerciseTutor()" class="vscode-tool-btn btn-tutor" title="Mở gia sư AI Gemini đồng hành">
              <span>💬 Gia sư AI</span>
            </button>
            <button onclick="toggleVscodePanelFullscreen()" class="ml-auto px-2.5 py-1 text-slate-300 hover:text-white bg-[#252526] hover:bg-[#333] border border-[#3c3c3c] rounded text-xs flex items-center gap-1.5 transition" title="Phóng to bảng AI toàn màn hình">
              <span>⛶ Toàn màn hình</span>
            </button>
          </div>

          <!-- LINE-LEVEL INSPECTOR BAR -->
          <div class="vscode-line-inspector-bar" id="vscode-line-inspector-bar">
            <div class="flex items-center gap-2 overflow-hidden">
              <span class="text-xs text-sky-400 font-mono font-bold flex items-center gap-1.5">
                <span class="w-2 h-2 rounded-full bg-sky-400 animate-pulse"></span>
                Dòng <span id="vscode-selected-line-num" class="text-white underline decoration-sky-500">1</span>:
              </span>
              <code id="vscode-selected-line-preview" class="text-slate-300 truncate max-w-xs md:max-w-md font-mono text-[11px] bg-[#1a1a1a] px-2 py-0.5 rounded border border-[#333]">(đang tải...)</code>
            </div>
            <div class="flex items-center gap-1.5 flex-shrink-0">
              <button onclick="askAiAboutCurrentLine()" title="AI giải thích sâu từng từ khóa, luồng dữ liệu và vai trò dòng này" class="px-2.5 py-1 bg-[#1e293b] hover:bg-[#2e405b] text-[#38bdf8] border border-sky-700/50 rounded text-xs font-semibold flex items-center gap-1 transition shadow-sm">
                <span>💬 Hỏi AI dòng này</span>
              </button>
              <button onclick="fixAiCurrentLine()" title="AI chẩn đoán lỗi tại dòng này và sinh bản vá sửa chuẩn" class="px-2.5 py-1 bg-[#2e1d0f] hover:bg-[#4d2f16] text-[#fbbf24] border border-amber-700/50 rounded text-xs font-semibold flex items-center gap-1 transition shadow-sm">
                <span>🛠️ Sửa lỗi dòng này</span>
              </button>
            </div>
          </div>

          <!-- COPILOT BANNER (INLINE SUGGESTION) -->
          <div id="vscode-copilot-banner" class="vscode-copilot-banner m-3 hidden">
            <div class="flex items-center justify-between pb-2 border-b border-[#3c3c4f]">
              <div class="flex items-center gap-2">
                <span class="copilot-badge">✨ AI Copilot Suggestion</span>
                <span class="text-xs text-slate-300 font-medium">Gợi ý dòng tiếp theo:</span>
              </div>
              <div class="flex items-center gap-1.5 text-[11px] text-slate-400 font-mono">
                <span>Nhấn <kbd class="px-1.5 py-0.5 bg-[#2d2d3f] border border-[#444] rounded text-emerald-300 font-bold">Tab</kbd> để chèn</span>
                <span>•</span>
                <span><kbd class="px-1 py-0.5 bg-[#2d2d3f] border border-[#444] rounded">Esc</kbd> để hủy</span>
              </div>
            </div>
            <pre id="vscode-copilot-code" class="copilot-code"></pre>
            <div id="vscode-copilot-explain" class="text-xs text-slate-300 mt-1 italic"></div>
            <div class="flex items-center gap-2 mt-2 pt-2 border-t border-[#3c3c4f]/50">
              <button onclick="acceptVscodeCopilotSuggestion()" class="px-3 py-1 bg-emerald-600 hover:bg-emerald-500 text-white rounded text-xs font-semibold flex items-center gap-1.5 shadow transition">
                <span>✓ Chấp nhận</span>
                <kbd class="text-[10px] bg-emerald-700 px-1 rounded">Tab</kbd>
              </button>
              <button onclick="dismissVscodeCopilotSuggestion()" class="px-2.5 py-1 bg-[#2d2d3f] hover:bg-[#3d3d52] text-slate-300 rounded text-xs font-medium transition">
                ✕ Bỏ qua (Esc)
              </button>
            </div>
          </div>

          <!-- MAIN EDITOR AREA -->
          <div class="vscode-editor-main relative">
            <div class="vscode-gutter">
              <div class="vscode-gutter-lines" id="vscode-gutter-lines">1</div>
            </div>
            <textarea
              id="code-editor-textarea"
              class="vscode-code-textarea"
              spellcheck="false"
              autocomplete="off"
              autocorrect="off"
              autocapitalize="off"
              placeholder="// Nhập mã nguồn của bạn tại đây..."
            >${escapeHtml(currentCode)}</textarea>
          </div>

          <!-- BOTTOM CONSOLE / TERMINAL PANEL -->
          <div class="vscode-bottom-panel" id="vscode-bottom-panel">
            <div class="vscode-panel-tabs" id="console-tabs">
              <button onclick="switchConsoleTab('testcases')" class="vscode-panel-tab active" id="tab-btn-testcases">
                <span>🧪 Test Cases</span>
                <span class="badge bg-slate-700 text-slate-300 text-[10px] px-1.5 py-0.2 rounded-full" id="testcase-count-badge">${(ex.test_cases || []).length}</span>
              </button>
              <button onclick="switchConsoleTab('terminal')" class="vscode-panel-tab" id="tab-btn-terminal">
                <span>📟 Terminal & Output</span>
              </button>
              <button onclick="switchConsoleTab('review')" class="vscode-panel-tab" id="tab-btn-review">
                <span>🤖 Senior AI Review</span>
              </button>
              <button onclick="switchConsoleTab('fix')" class="vscode-panel-tab" id="tab-btn-fix">
                <span>🛠️ Sửa lỗi & Nâng cấp</span>
              </button>
              <div class="ml-auto flex items-center gap-1.5 pr-2">
                <button onclick="toggleVscodePanelFullscreen()" class="px-2 py-0.5 text-xs text-slate-400 hover:text-white bg-[#252526] hover:bg-[#333] border border-[#3c3c3c] rounded flex items-center gap-1 transition" title="Phóng to toàn màn hình">
                  <span>⛶ Toàn màn hình</span>
                </button>
                <button onclick="toggleVscodePanelMinimize()" class="text-slate-400 hover:text-white text-xs px-1" title="Thu nhỏ">_</button>
              </div>
            </div>

            <div class="vscode-panel-content" id="console-tab-content">
              <!-- TAB 1: TEST CASES -->
              <div id="pane-testcases" class="space-y-3">
                <div class="flex items-center justify-between text-xs text-slate-400 border-b border-[#333] pb-2">
                  <span>Danh sách bộ kiểm thử tự động của hệ thống:</span>
                  <button onclick="submitExerciseSolution()" class="px-2.5 py-1 bg-emerald-600 hover:bg-emerald-500 text-white font-medium rounded text-xs transition flex items-center gap-1 shadow-sm">
                    <span>▶ Chấm tất cả testcase</span>
                  </button>
                </div>
                <div id="testcase-results-list" class="space-y-2">
                  ${renderInitialTestCases(ex.test_cases || [])}
                </div>
              </div>

              <!-- TAB 2: TERMINAL / STDIN / STDOUT -->
              <div id="pane-terminal" class="hidden space-y-3">
                <div class="flex items-center justify-between text-xs text-slate-400 border-b border-[#333] pb-2">
                  <span class="font-mono">Console: stdin / stdout / stderr</span>
                  <div class="flex items-center gap-2">
                    <button onclick="clearVscodeTerminal()" class="text-slate-400 hover:text-white text-xs">Xóa màn hình</button>
                    <button onclick="runExerciseCode()" class="px-2 py-0.5 bg-[#007acc] text-white rounded text-xs">Chạy lại</button>
                  </div>
                </div>
                <div>
                  <label class="block text-[11px] font-mono text-slate-400 mb-1">Dữ liệu đầu vào (STDIN tùy chỉnh):</label>
                  <input type="text" id="custom-stdin-input" placeholder="Ví dụ: 5 10 20 hoặc nhập chuỗi test..." class="w-full bg-[#181818] border border-[#333] rounded px-3 py-1.5 text-xs font-mono text-white focus:outline-none focus:border-[#007acc]">
                </div>
                <div>
                  <div class="text-[11px] font-mono text-slate-400 mb-1">Kết quả thực thi (STDOUT):</div>
                  <pre id="terminal-stdout" class="vscode-terminal-view"><span class="text-slate-500">[UniMaster Engine] Sẵn sàng chạy chương trình. Nhấn 'Chạy code' (Ctrl+Enter) để thực thi.</span></pre>
                </div>
              </div>

              <!-- TAB 3: SENIOR AI REVIEW -->
              <div id="pane-review" class="hidden">
                <div class="flex items-center justify-between text-xs text-slate-400 border-b border-[#333] pb-2 mb-3">
                  <span class="flex items-center gap-1.5 font-bold text-slate-200">
                    <span>✨</span> Google Gemini & Senior Architect Code Review
                  </span>
                  <div class="flex items-center gap-2">
                    <button onclick="openAiFullscreenForCurrentTab('review')" class="px-2.5 py-0.5 bg-[#252526] hover:bg-[#383838] border border-[#444] rounded text-slate-200 text-xs flex items-center gap-1 transition">
                      <span>⛶ Đọc toàn màn hình</span>
                    </button>
                    <button onclick="runExerciseAiReview()" class="px-2.5 py-0.5 bg-purple-600 hover:bg-purple-500 text-white rounded text-xs transition">
                      Chấm lại
                    </button>
                  </div>
                </div>
                <div id="ai-review-result" class="text-xs text-slate-300 leading-relaxed font-sans">
                  <div class="p-4 text-center text-slate-500">
                    Nhấn nút '🤖 AI Review' trên thanh công cụ để nhận nhận xét chuyên sâu từ Senior Architect.
                  </div>
                </div>
              </div>

              <!-- TAB 4: BUG FIX & UPGRADE -->
              <div id="pane-fix" class="hidden">
                <div class="flex items-center justify-between text-xs text-slate-400 border-b border-[#333] pb-2 mb-3">
                  <span class="flex items-center gap-1.5 font-bold text-slate-200">
                    <span>🛠️</span> Chẩn đoán lỗi & Nâng cấp Clean Code 1-Click
                  </span>
                  <div class="flex items-center gap-2">
                    <button onclick="openAiFullscreenForCurrentTab('fix')" class="px-2.5 py-0.5 bg-[#252526] hover:bg-[#383838] border border-[#444] rounded text-slate-200 text-xs flex items-center gap-1 transition">
                      <span>⛶ Đọc toàn màn hình</span>
                    </button>
                    <button onclick="runExerciseFixAndUpgrade()" class="px-2.5 py-0.5 bg-amber-600 hover:bg-amber-500 text-white rounded text-xs transition">
                      Phân tích lại
                    </button>
                  </div>
                </div>
                <div id="ai-fix-result" class="text-xs text-slate-300 leading-relaxed font-sans">
                  <div class="p-4 text-center text-slate-500">
                    Nhấn '🛠️ Sửa & Tối ưu' để AI phân tích lỗi biên dịch, logic và tự động tái cấu trúc mã nguồn.
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- STATUS BAR -->
          <div class="vscode-statusbar">
            <div class="vscode-status-item">
              <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
              <span>main*</span>
            </div>
            <div class="vscode-status-item" id="vscode-status-errors">
              <span>✓ 0 errors</span>
            </div>
            <div class="vscode-status-item cursor-pointer" onclick="triggerVscodeCopilotSuggest()" title="AI Copilot sẵn sàng gợi ý">
              <span>✨ Copilot Ready</span>
            </div>
            <div class="ml-auto flex items-center">
              <div class="vscode-status-item" id="vscode-cursor-pos">Ln 1, Col 1</div>
              <div class="vscode-status-item">Spaces: 4</div>
              <div class="vscode-status-item">UTF-8</div>
              <div class="vscode-status-item font-semibold text-white">${currLang.toUpperCase()}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  `;

  // Initialize listeners and line numbers
  setTimeout(() => {
    updateVscodeLineNumbers();
    syncVscodeGutterScroll();
    updateVscodeCursorPosition();

    const textarea = document.getElementById('code-editor-textarea');
    if (textarea) {
      textarea.addEventListener('input', () => {
        updateVscodeLineNumbers();
        syncVscodeGutterScroll();
        updateVscodeCursorPosition();
        saveCurrentExerciseCode();
      });
      textarea.addEventListener('scroll', syncVscodeGutterScroll);
      textarea.addEventListener('click', updateVscodeCursorPosition);
      textarea.addEventListener('keyup', updateVscodeCursorPosition);
      textarea.addEventListener('keydown', handleVscodeEditorKeydown);
    }
  }, 50);
}

// Global Copilot & Line Inspector state
window.__vscodeCopilotCurrentSuggestion = null;
window.__vscodeSelectedLine = 1;
window.__vscodeLastInspection = null;

function updateVscodeLineNumbers() {
  const textarea = document.getElementById('code-editor-textarea');
  const gutter = document.getElementById('vscode-gutter-lines');
  if (!textarea || !gutter) return;
  const lines = (textarea.value || '').split('\n').length;
  let html = '';
  const currentSel = window.__vscodeSelectedLine || 1;
  for (let i = 1; i <= Math.max(lines, 1); i++) {
    const activeClass = (i === currentSel) ? 'vscode-gutter-line-active' : '';
    html += `<div class="${activeClass}" onclick="selectVscodeGutterLine(${i})" title="Dòng ${i} • Click để hỏi hoặc sửa">${i}</div>`;
  }
  gutter.innerHTML = html;
}

function syncVscodeGutterScroll() {
  const textarea = document.getElementById('code-editor-textarea');
  const gutter = document.getElementById('vscode-gutter-lines');
  if (textarea && gutter) {
    gutter.scrollTop = textarea.scrollTop;
  }
}

function updateVscodeCursorPosition() {
  const textarea = document.getElementById('code-editor-textarea');
  const posEl = document.getElementById('vscode-cursor-pos');
  if (!textarea) return;
  const selStart = textarea.selectionStart || 0;
  const textBefore = textarea.value.substring(0, selStart);
  const lines = textBefore.split('\n');
  const lineNum = lines.length;
  const colNum = lines[lines.length - 1].length + 1;
  if (posEl) posEl.textContent = `Ln ${lineNum}, Col ${colNum}`;

  window.__vscodeSelectedLine = lineNum;

  // Update Line Inspector Preview Bar
  const lineNumEl = document.getElementById('vscode-selected-line-num');
  const linePrevEl = document.getElementById('vscode-selected-line-preview');
  if (lineNumEl) lineNumEl.textContent = lineNum;
  if (linePrevEl) {
    const allLines = textarea.value.split('\n');
    const currentLineText = allLines[lineNum - 1] || '';
    linePrevEl.textContent = currentLineText.trim() || '(dòng trống)';
  }

  // Update active gutter line
  const gutter = document.getElementById('vscode-gutter-lines');
  if (gutter) {
    const divs = gutter.children;
    for (let i = 0; i < divs.length; i++) {
      if (i + 1 === lineNum) {
        divs[i].classList.add('vscode-gutter-line-active');
      } else {
        divs[i].classList.remove('vscode-gutter-line-active');
      }
    }
  }
}

function selectVscodeGutterLine(lineNum) {
  const textarea = document.getElementById('code-editor-textarea');
  if (!textarea) return;
  const lines = textarea.value.split('\n');
  let charCount = 0;
  for (let i = 0; i < lineNum - 1 && i < lines.length; i++) {
    charCount += lines[i].length + 1;
  }
  textarea.focus();
  textarea.setSelectionRange(charCount, charCount + (lines[lineNum - 1] ? lines[lineNum - 1].length : 0));
  updateVscodeCursorPosition();
}

// Handle Keydown in Editor: Tab for Copilot or Indentation, Esc for cancel, Alt+\ for Copilot trigger
function handleVscodeEditorKeydown(e) {
  // If Copilot suggestion is visible and user presses TAB
  if (e.key === 'Tab' && window.__vscodeCopilotCurrentSuggestion) {
    e.preventDefault();
    acceptVscodeCopilotSuggestion();
    return;
  }

  // Standard VS Code Tab handling: insert 4 spaces instead of losing focus
  if (e.key === 'Tab' && !e.shiftKey && !e.ctrlKey && !e.altKey) {
    e.preventDefault();
    const textarea = e.target;
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    textarea.value = textarea.value.substring(0, start) + '    ' + textarea.value.substring(end);
    textarea.selectionStart = textarea.selectionEnd = start + 4;
    updateVscodeLineNumbers();
    syncVscodeGutterScroll();
    updateVscodeCursorPosition();
    saveCurrentExerciseCode();
    return;
  }

  // Escape: dismiss Copilot or Fullscreen
  if (e.key === 'Escape') {
    if (window.__vscodeCopilotCurrentSuggestion) {
      dismissVscodeCopilotSuggestion();
      return;
    }
    const fs = document.getElementById('ai-fullscreen-workspace');
    if (fs && !fs.classList.contains('hidden')) {
      closeAiFullscreenOverlay();
      return;
    }
  }

  // Alt+\ or Ctrl+I to trigger AI Copilot
  if ((e.altKey && (e.key === '\\' || e.code === 'Backslash')) || (e.ctrlKey && e.key.toLowerCase() === 'i')) {
    e.preventDefault();
    triggerVscodeCopilotSuggest();
  }
}

// AI COPILOT: Suggest Next Line
async function triggerVscodeCopilotSuggest() {
  const textarea = document.getElementById('code-editor-textarea');
  if (!textarea) return;
  const ex = state.currentExercise;
  const banner = document.getElementById('vscode-copilot-banner');
  const codeEl = document.getElementById('vscode-copilot-code');
  const explainEl = document.getElementById('vscode-copilot-explain');

  if (!banner || !codeEl) return;

  banner.classList.remove('hidden');
  codeEl.textContent = '✨ AI Copilot đang phân tích ngữ cảnh và dự đoán dòng code tiếp theo...';
  if (explainEl) explainEl.textContent = 'Vui lòng chờ trong giây lát...';

  try {
    const payload = {
      code: textarea.value,
      language: (ex && ex.language) || 'csharp',
      line_number: window.__vscodeSelectedLine || 1,
      column: 1,
      title: (ex && ex.title) || ''
    };

    const res = await fetchJson('/api/code/suggest', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (res && res.success && res.data) {
      window.__vscodeCopilotCurrentSuggestion = res.data.suggestion;
      codeEl.textContent = res.data.suggestion;
      if (explainEl) explainEl.textContent = res.data.explanation || 'Dòng gợi ý tối ưu theo ngữ cảnh hiện tại.';
    } else {
      codeEl.textContent = '// Không thể sinh gợi ý lúc này.';
      if (explainEl) explainEl.textContent = (res && res.error) || 'Vui lòng thử lại sau.';
    }
  } catch (err) {
    codeEl.textContent = '// Lỗi kết nối AI Copilot.';
    if (explainEl) explainEl.textContent = err.message || '';
  }
}

function acceptVscodeCopilotSuggestion() {
  const textarea = document.getElementById('code-editor-textarea');
  const suggestion = window.__vscodeCopilotCurrentSuggestion;
  if (!textarea || !suggestion) return;

  const start = textarea.selectionStart;
  const val = textarea.value;

  // Insert suggestion at cursor or on a new line
  let insertText = suggestion;
  if (start > 0 && val[start - 1] !== '\n') {
    insertText = '\n' + suggestion;
  }

  textarea.value = val.substring(0, start) + insertText + val.substring(start);
  textarea.selectionStart = textarea.selectionEnd = start + insertText.length;
  textarea.focus();

  dismissVscodeCopilotSuggestion();
  updateVscodeLineNumbers();
  syncVscodeGutterScroll();
  updateVscodeCursorPosition();
  saveCurrentExerciseCode();

  if (typeof showToast === 'function') {
    showToast('✓ Đã áp dụng dòng gợi ý từ AI Copilot!', 'success');
  }
}

function dismissVscodeCopilotSuggestion() {
  window.__vscodeCopilotCurrentSuggestion = null;
  const banner = document.getElementById('vscode-copilot-banner');
  if (banner) banner.classList.add('hidden');
}

// LINE-LEVEL AI INSPECTOR: Ask AI about current line
async function askAiAboutCurrentLine() {
  const textarea = document.getElementById('code-editor-textarea');
  if (!textarea) return;
  const lineNum = window.__vscodeSelectedLine || 1;
  const ex = state.currentExercise;

  openAiFullscreenInspectorLoading(lineNum, 'Đang giải thích dòng code...');

  try {
    const payload = {
      code: textarea.value,
      language: (ex && ex.language) || 'csharp',
      line_number: lineNum,
      action: 'ask',
      title: (ex && ex.title) || ''
    };

    const res = await fetchJson('/api/code/inspect-line', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (res && res.success && res.data) {
      renderAiFullscreenInspectorResult(res.data, textarea.value);
    } else {
      renderAiFullscreenError(res.error || 'Không thể kết nối dịch vụ AI');
    }
  } catch (err) {
    renderAiFullscreenError(err.message || 'Lỗi mạng');
  }
}

// LINE-LEVEL AI INSPECTOR: Fix bug on current line
async function fixAiCurrentLine() {
  const textarea = document.getElementById('code-editor-textarea');
  if (!textarea) return;
  const lineNum = window.__vscodeSelectedLine || 1;
  const ex = state.currentExercise;

  openAiFullscreenInspectorLoading(lineNum, 'Đang chẩn đoán và sửa lỗi dòng...');

  try {
    const payload = {
      code: textarea.value,
      language: (ex && ex.language) || 'csharp',
      line_number: lineNum,
      action: 'fix',
      title: (ex && ex.title) || ''
    };

    const res = await fetchJson('/api/code/inspect-line', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (res && res.success && res.data) {
      renderAiFullscreenInspectorResult(res.data, textarea.value);
    } else {
      renderAiFullscreenError(res.error || 'Không thể phân tích lỗi dòng này');
    }
  } catch (err) {
    renderAiFullscreenError(err.message || 'Lỗi mạng');
  }
}

// FULLSCREEN AI WORKSPACE
function getOrCreateAiFullscreenOverlay() {
  let overlay = document.getElementById('ai-fullscreen-workspace');
  if (!overlay) {
    overlay = document.createElement('div');
    overlay.id = 'ai-fullscreen-workspace';
    overlay.className = 'ai-fullscreen-overlay hidden';
    document.body.appendChild(overlay);
  }
  return overlay;
}

function closeAiFullscreenOverlay() {
  const overlay = document.getElementById('ai-fullscreen-workspace');
  if (overlay) {
    overlay.classList.add('hidden');
  }
}

function openAiFullscreenInspectorLoading(lineNum, msg) {
  const overlay = getOrCreateAiFullscreenOverlay();
  overlay.classList.remove('hidden');
  overlay.innerHTML = `
    <div class="ai-fullscreen-header">
      <div class="flex items-center gap-3">
        <span class="gemini-sparkle-icon">✦</span>
        <div>
          <div class="text-sm font-bold text-white flex items-center gap-2">
            <span>UNIMASTER SENIOR AI INSPECTOR</span>
            <span class="copilot-badge">Dòng ${lineNum}</span>
          </div>
          <div class="text-xs text-slate-400">Chế độ giải thích & sửa lỗi toàn màn hình</div>
        </div>
      </div>
      <button onclick="closeAiFullscreenOverlay()" class="px-3 py-1 bg-[#27272a] hover:bg-[#3f3f46] text-white rounded text-xs transition">
        ✕ Đóng (Esc)
      </button>
    </div>
    <div class="ai-fullscreen-body items-center justify-center p-12">
      <div class="text-center space-y-4 max-w-md">
        <div class="w-12 h-12 mx-auto rounded-full bg-gradient-to-tr from-blue-500 via-purple-500 to-pink-500 animate-spin flex items-center justify-center p-1 shadow-lg">
          <div class="w-full h-full bg-[#18181b] rounded-full flex items-center justify-center">
            <span class="text-lg">✦</span>
          </div>
        </div>
        <div class="text-base font-bold text-white">${escapeHtml(msg || 'AI đang phân tích...')}</div>
        <div class="text-xs text-slate-400">Đang trích xuất 10 dòng ngữ cảnh, tra cứu nguyên lý OOP và kiến trúc Clean Code...</div>
      </div>
    </div>
  `;
}

function renderAiFullscreenError(errMsg) {
  const overlay = getOrCreateAiFullscreenOverlay();
  overlay.innerHTML = `
    <div class="ai-fullscreen-header">
      <div class="text-sm font-bold text-red-400">LỖI PHÂN TÍCH AI</div>
      <button onclick="closeAiFullscreenOverlay()" class="px-3 py-1 bg-[#27272a] hover:bg-[#3f3f46] text-white rounded text-xs transition">✕ Đóng (Esc)</button>
    </div>
    <div class="p-12 text-center text-slate-300">
      <p class="text-red-400 mb-4">${escapeHtml(errMsg)}</p>
      <button onclick="closeAiFullscreenOverlay()" class="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded text-sm">Quay lại Editor</button>
    </div>
  `;
}

function renderAiFullscreenInspectorResult(data, currentSourceCode) {
  window.__vscodeLastInspection = data;
  const overlay = getOrCreateAiFullscreenOverlay();
  overlay.classList.remove('hidden');

  const lines = (currentSourceCode || '').split('\n');
  const targetLine = data.line_number || 1;

  let codeRowsHtml = '';
  lines.forEach((lineText, idx) => {
    const lineIndex = idx + 1;
    const isTarget = (lineIndex === targetLine);
    const rowClass = isTarget ? 'ai-target-line-highlight font-bold' : 'text-slate-300';
    const targetBadge = isTarget ? '<span class="text-amber-400 text-[10px] mr-1">▶</span>' : '';
    codeRowsHtml += `
      <div class="flex items-center px-3 py-0.5 hover:bg-[#252528] ${rowClass}">
        <span class="w-10 text-right pr-3 text-slate-500 font-mono text-xs select-none">${lineIndex}</span>
        <pre class="font-mono text-xs overflow-x-auto flex-1 whitespace-pre">${targetBadge}${escapeHtml(lineText || ' ')}</pre>
      </div>
    `;
  });

  const isFix = (data.action === 'fix' || data.has_error_on_line);

  overlay.innerHTML = `
    <div class="ai-fullscreen-header">
      <div class="flex items-center gap-3">
        <span class="gemini-sparkle-icon">✦</span>
        <div>
          <div class="text-sm font-bold text-white flex items-center gap-2">
            <span>${isFix ? '🛠️ CHẨN ĐOÁN & SỬA LỖI DÒNG' : '💬 GIẢI THÍCH CHI TIẾT DÒNG CODE'}</span>
            <span class="px-2 py-0.5 rounded text-[11px] font-mono ${isFix ? 'bg-amber-900/60 text-amber-300 border border-amber-700/60' : 'bg-sky-900/60 text-sky-300 border border-sky-700/60'}">
              Dòng ${targetLine}
            </span>
          </div>
          <div class="text-xs text-slate-400 font-mono truncate max-w-md">
            ${escapeHtml(data.target_code || '')}
          </div>
        </div>
      </div>
      <div class="flex items-center gap-2">
        ${data.full_fixed_code ? `
        <button onclick="applyAiFullscreenFixedCode()" class="px-3 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white font-semibold rounded text-xs flex items-center gap-1.5 shadow transition">
          <span>⚡ Áp dụng sửa vào Editor</span>
        </button>` : ''}
        <button onclick="copyAiFullscreenContent()" class="px-3 py-1.5 bg-[#27272a] hover:bg-[#3f3f46] text-slate-200 rounded text-xs flex items-center gap-1 transition">
          <span>⎘ Sao chép</span>
        </button>
        <button onclick="closeAiFullscreenOverlay()" class="px-3 py-1.5 bg-[#27272a] hover:bg-[#3f3f46] text-white rounded text-xs transition">
          ✕ Thu nhỏ / Đóng (Esc)
        </button>
      </div>
    </div>

    <div class="ai-fullscreen-body">
      <!-- LEFT PANE: SOURCE CODE -->
      <div class="ai-fullscreen-code-pane">
        <div class="px-4 py-2.5 bg-[#1a1a1e] border-b border-[#2e2e38] text-xs font-semibold text-slate-300 flex items-center justify-between">
          <span class="flex items-center gap-1.5">
            <span>📄</span>
            <span>Mã nguồn chương trình</span>
          </span>
          <span class="text-[11px] text-amber-400 font-mono">Dòng target: #${targetLine}</span>
        </div>
        <div class="flex-1 overflow-y-auto font-mono py-2">
          ${codeRowsHtml}
        </div>
      </div>

      <!-- RIGHT PANE: DEEP AI EXPLANATION & FIX -->
      <div class="ai-fullscreen-content-pane" id="ai-fullscreen-text-container">
        <!-- TITLE CARD -->
        <div class="ai-knowledge-card border-l-4 ${isFix ? 'border-amber-500' : 'border-sky-500'}">
          <div class="ai-knowledge-card-title ${isFix ? 'text-amber-400' : 'text-sky-400'}">
            <span>${isFix ? '🛠️' : '💡'}</span>
            <span>${escapeHtml(data.title || 'Phân tích dòng code')}</span>
          </div>
          <div class="text-sm text-slate-200 leading-relaxed font-sans">
            ${formatMarkdown(data.detailed_explanation || '')}
          </div>
        </div>

        <!-- IF ERROR / FIX CARD -->
        ${isFix ? `
        <div class="ai-knowledge-card border-l-4 border-rose-500 bg-[#241c1e]">
          <div class="ai-knowledge-card-title text-rose-400">
            <span>⚠️</span>
            <span>Chẩn đoán nguyên nhân lỗi:</span>
          </div>
          <p class="text-sm text-slate-200 mb-3">${escapeHtml(data.error_diagnostic || 'Phát hiện điểm cần cải thiện cú pháp hoặc logic.')}</p>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-3 mt-3">
            <div class="bg-[#18181b] p-3 rounded border border-rose-900/40">
              <div class="text-[11px] font-bold text-rose-400 uppercase mb-1">Dòng gốc ban đầu:</div>
              <pre class="font-mono text-xs text-rose-300 whitespace-pre-wrap">${escapeHtml(data.target_code || '')}</pre>
            </div>
            <div class="bg-[#18181b] p-3 rounded border border-emerald-900/40">
              <div class="text-[11px] font-bold text-emerald-400 uppercase mb-1">Dòng sau khi sửa chuẩn:</div>
              <pre class="font-mono text-xs text-emerald-300 whitespace-pre-wrap">${escapeHtml(data.fixed_line || '')}</pre>
            </div>
          </div>
        </div>` : ''}

        <!-- LEARNING LESSON CARD -->
        ${(data.learning_points && data.learning_points.length) ? `
        <div class="ai-knowledge-card border-l-4 border-indigo-500">
          <div class="ai-knowledge-card-title text-indigo-400">
            <span>🎓</span>
            <span>Bài học then chốt & Kiến thức Đại học cần nhớ:</span>
          </div>
          <ul class="space-y-2 text-sm text-slate-300">
            ${data.learning_points.map(pt => `
              <li class="flex items-start gap-2">
                <span class="text-indigo-400 font-bold">✓</span>
                <span>${escapeHtml(pt)}</span>
              </li>
            `).join('')}
          </ul>
        </div>` : ''}

        <!-- QUICK 5-SECOND TIP -->
        ${data.quick_tip ? `
        <div class="ai-knowledge-card border-l-4 border-emerald-500 bg-[#16221c]">
          <div class="ai-knowledge-card-title text-emerald-400">
            <span>⚡</span>
            <span>Mẹo nhớ nhanh 5 giây:</span>
          </div>
          <p class="text-sm text-emerald-200 font-medium">${escapeHtml(data.quick_tip)}</p>
        </div>` : ''}
      </div>
    </div>
  `;
}

function applyAiFullscreenFixedCode() {
  if (!window.__vscodeLastInspection || !window.__vscodeLastInspection.full_fixed_code) return;
  const textarea = document.getElementById('code-editor-textarea');
  if (!textarea) return;

  textarea.value = window.__vscodeLastInspection.full_fixed_code;
  updateVscodeLineNumbers();
  syncVscodeGutterScroll();
  updateVscodeCursorPosition();
  saveCurrentExerciseCode();

  closeAiFullscreenOverlay();
  if (typeof showToast === 'function') {
    showToast('✓ Đã áp dụng bản vá mã nguồn vào Visual Studio Editor!', 'success');
  }
}

function copyAiFullscreenContent() {
  if (!window.__vscodeLastInspection) return;
  const text = (window.__vscodeLastInspection.full_fixed_code)
    || (window.__vscodeLastInspection.detailed_explanation)
    || '';
  if (navigator.clipboard && text) {
    navigator.clipboard.writeText(text);
    if (typeof showToast === 'function') {
      showToast('✓ Đã sao chép vào bộ nhớ tạm!', 'success');
    }
  }
}

// FULLSCREEN VIEW FOR CONSOLE TABS (AI Review & Fix & Upgrade)
function openAiFullscreenForCurrentTab(tabName) {
  const currentTab = tabName || 'review';
  const overlay = getOrCreateAiFullscreenOverlay();
  overlay.classList.remove('hidden');

  const textarea = document.getElementById('code-editor-textarea');
  const srcCode = textarea ? textarea.value : '';
  const ex = state.currentExercise;

  const contentSourceId = (currentTab === 'review') ? 'ai-review-result' : 'ai-fix-result';
  const contentEl = document.getElementById(contentSourceId);
  const contentHtml = contentEl ? contentEl.innerHTML : '<p class="text-slate-400">Chưa có dữ liệu phân tích.</p>';

  const titleText = (currentTab === 'review')
    ? 'SENIOR ARCHITECT AI REVIEW — TOÀN MÀN HÌNH'
    : 'CHẨN ĐOÁN LỖI & NÂNG CẤP MÃ NGUỒN — TOÀN MÀN HÌNH';

  const lines = (srcCode || '').split('\n');
  let codeRowsHtml = '';
  lines.forEach((lineText, idx) => {
    codeRowsHtml += `
      <div class="flex items-center px-3 py-0.5 hover:bg-[#252528] text-slate-300">
        <span class="w-10 text-right pr-3 text-slate-500 font-mono text-xs select-none">${idx + 1}</span>
        <pre class="font-mono text-xs overflow-x-auto flex-1 whitespace-pre">${escapeHtml(lineText || ' ')}</pre>
      </div>
    `;
  });

  overlay.innerHTML = `
    <div class="ai-fullscreen-header">
      <div class="flex items-center gap-3">
        <span class="gemini-sparkle-icon">✦</span>
        <div>
          <div class="text-sm font-bold text-white">${titleText}</div>
          <div class="text-xs text-slate-400">Bài tập: ${escapeHtml((ex && ex.title) || '')}</div>
        </div>
      </div>
      <button onclick="closeAiFullscreenOverlay()" class="px-3 py-1.5 bg-[#27272a] hover:bg-[#3f3f46] text-white rounded text-xs transition">
        ✕ Thu nhỏ / Đóng (Esc)
      </button>
    </div>
    <div class="ai-fullscreen-body">
      <div class="ai-fullscreen-code-pane">
        <div class="px-4 py-2.5 bg-[#1a1a1e] border-b border-[#2e2e38] text-xs font-semibold text-slate-300">
          <span>📄 Mã nguồn bài làm</span>
        </div>
        <div class="flex-1 overflow-y-auto font-mono py-2">
          ${codeRowsHtml}
        </div>
      </div>
      <div class="ai-fullscreen-content-pane">
        <div class="ai-knowledge-card">
          ${contentHtml}
        </div>
      </div>
    </div>
  `;
}

function toggleVscodePanelFullscreen() {
  const panel = document.getElementById('vscode-bottom-panel');
  if (!panel) return;
  if (panel.classList.contains('fixed') && panel.classList.contains('inset-0')) {
    panel.classList.remove('fixed', 'inset-0', 'z-50', 'h-screen');
    panel.style.height = '';
  } else {
    panel.classList.add('fixed', 'inset-0', 'z-50', 'h-screen');
  }
}

function toggleVscodePanelMinimize() {
  const panel = document.getElementById('vscode-bottom-panel');
  if (!panel) return;
  if (panel.style.height === '40px') {
    panel.style.height = '320px';
  } else {
    panel.style.height = '40px';
  }
}

function switchConsoleTab(tab) {
  const tabs = ['testcases', 'terminal', 'review', 'fix'];
  tabs.forEach(t => {
    const pane = document.getElementById('pane-' + t);
    const btn = document.getElementById('tab-btn-' + t);
    if (pane) {
      if (t === tab) pane.classList.remove('hidden');
      else pane.classList.add('hidden');
    }
    if (btn) {
      if (t === tab) {
        btn.classList.add('active');
        btn.style.color = '#ffffff';
        btn.style.borderBottom = '2px solid #007acc';
      } else {
        btn.classList.remove('active');
        btn.style.color = '#969696';
        btn.style.borderBottom = 'none';
      }
    }
  });
}
'''

new_app = app_content[:s_idx] + new_impl + "\n\n" + app_content[e_idx:]

with open(app_path, "w", encoding="utf-8") as f:
    f.write(new_app)

print("static/app.js updated successfully!")
