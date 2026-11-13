# -*- coding: utf-8 -*-
import sys
import os

app_path = os.path.join(os.path.dirname(__file__), 'static', 'app.js')
with open(app_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Target block for Editor Viewport in renderExerciseDetail
marker_1_start = '<!-- Code Editor Viewport (Line Numbers Gutter + Textarea) -->'
marker_1_end = '<!-- Bottom Panel (Terminal / Test Runner / AI Output Tabs) -->'

idx_start = content.find(marker_1_start)
idx_end = content.find(marker_1_end, idx_start)

if idx_start == -1 or idx_end == -1:
    print(f'Error finding markers: start={idx_start}, end={idx_end}')
    sys.exit(1)

new_viewport = '''<!-- Code Editor Viewport (Line Numbers Gutter + Textarea + Copilot Banner + Line Inspector) -->
          <div class="flex-1 relative flex flex-col overflow-hidden bg-[#1e1e1e]" style="min-height: 320px;">
            <!-- Line Inspector Action Bar (hiện khi click vào số dòng ở Gutter) -->
            <div id="vscode-line-inspector" class="vscode-line-inspector-bar hidden flex items-center justify-between px-3 py-1.5 bg-[#252526] border-b border-[#007acc] text-[11px] font-mono animate-fadeIn z-10">
              <div class="flex items-center gap-2 overflow-hidden">
                <span class="text-cyan-400 font-bold whitespace-nowrap">📍 Dòng <span id="inspector-line-num">1</span>:</span>
                <span id="inspector-line-preview" class="text-slate-300 truncate max-w-xs md:max-w-md italic"></span>
              </div>
              <div class="flex items-center gap-2 flex-shrink-0">
                <button type="button" onclick="askAiAboutCurrentLine()" class="px-2 py-0.5 rounded bg-blue-600 hover:bg-blue-500 text-white flex items-center gap-1 transition-colors" title="Hỏi AI giải thích cặn kẽ dòng này">
                  <span>💬</span> Hỏi AI dòng này
                </button>
                <button type="button" onclick="fixAiCurrentLine()" class="px-2 py-0.5 rounded bg-emerald-600 hover:bg-emerald-500 text-white flex items-center gap-1 transition-colors" title="Nhờ AI chẩn đoán và tự sửa lỗi dòng này">
                  <span>⚡</span> Sửa lỗi dòng này
                </button>
                <button type="button" onclick="document.getElementById('vscode-line-inspector').classList.add('hidden')" class="text-slate-400 hover:text-white px-1.5">✕</button>
              </div>
            </div>

            <!-- Main Gutter + Textarea Area -->
            <div class="flex-1 relative flex overflow-hidden">
              <!-- Line Numbers Gutter (Click để chọn dòng thanh tra) -->
              <div id="vscode-gutter-lines" onclick="handleVscodeGutterClick(event)" class="vscode-gutter w-12 bg-[#1e1e1e] text-[#858585] font-mono text-xs py-3 pr-2 text-right select-none border-r border-[#252526] overflow-hidden flex-shrink-0 leading-relaxed cursor-pointer" style="font-family: 'Cascadia Code', Consolas, 'Courier New', monospace; line-height: 1.5rem;" title="Click vào số dòng để Hỏi AI hoặc Sửa lỗi dòng đó">
                <!-- Generated dynamically -->
              </div>

              <!-- Code Textarea -->
              <textarea id="code-editor-textarea" spellcheck="false"
                onkeydown="handleVscodeEditorKeydown(event)"
                oninput="handleVscodeCodeInput()"
                onscroll="syncVscodeGutterScroll()"
                onclick="handleVscodeEditorClick(event)"
                onkeyup="handleVscodeEditorKeyup(event)"
                class="w-full flex-1 p-3 font-mono text-xs sm:text-sm text-[#9cdcfe] bg-[#1e1e1e] leading-relaxed outline-none border-none resize-none custom-scrollbar"
                style="font-family: 'Cascadia Code', Consolas, 'Fira Code', monospace; tab-size: 4; line-height: 1.5rem;"
                placeholder="// Viết code giải thuật của bạn tại đây...&#10;// Mẹo: Gõ code hoặc nhấn Alt+\\ để AI Copilot gợi ý dòng tiếp theo!">${escapeHtml(currentCode)}</textarea>
            </div>

            <!-- Copilot Floating Suggestion Banner -->
            <div id="vscode-copilot-banner" class="hidden absolute bottom-3 right-4 max-w-md bg-[#252526] border border-[#007acc] rounded-lg shadow-2xl p-2.5 z-20 text-xs font-mono animate-slideUp">
              <div class="flex items-center justify-between text-[11px] mb-1.5 border-b border-[#3c3c3c] pb-1">
                <span class="text-cyan-400 font-bold flex items-center gap-1">
                  <span>✨</span> AI Copilot Gợi ý dòng tiếp:
                </span>
                <div class="flex items-center gap-1">
                  <span class="px-1.5 py-0.5 rounded bg-[#007acc] text-white text-[10px] font-bold">Phím Tab</span>
                  <button type="button" onclick="dismissVscodeCopilotSuggestion()" class="text-slate-400 hover:text-white ml-1">✕</button>
                </div>
              </div>
              <pre id="copilot-suggestion-text" class="text-emerald-300 font-mono text-[11px] bg-[#1e1e1e] p-2 rounded border border-[#333333] whitespace-pre-wrap overflow-x-auto max-h-24"></pre>
              <div class="flex items-center justify-between mt-2 pt-1 text-[10px] text-slate-400">
                <span>Bấm <strong>Tab</strong> để chèn</span>
                <button type="button" onclick="acceptVscodeCopilotSuggestion()" class="px-2.5 py-0.5 rounded bg-emerald-600 hover:bg-emerald-500 text-white font-bold">Chèn Code (Tab)</button>
              </div>
            </div>
          </div>

          '''

content = content[:idx_start] + new_viewport + content[idx_end:]
print('Viewport replaced successfully')

# 2. Add Fullscreen AI response button to tabs bar
old_block_2 = '''              <!-- Console Status Indicator -->
              <div id="console-status-indicator" class="text-[11px] font-bold text-[#858585]">'''

new_block_2 = '''              <!-- Fullscreen AI Console button -->
              <div class="flex items-center gap-2">
                <button type="button" onclick="openAiFullscreenForCurrentTab()" class="px-2.5 py-1 rounded bg-[#333333] hover:bg-[#444444] text-cyan-300 hover:text-white flex items-center gap-1.5 text-[11px] font-mono transition-colors shadow-sm" title="Mở rộng toàn màn hình phần AI trả lời">
                  <span>⛶</span> Toàn Màn Hình AI
                </button>
                <!-- Console Status Indicator -->
                <div id="console-status-indicator" class="text-[11px] font-bold text-[#858585]">'''

if old_block_2 in content:
    content = content.replace(old_block_2, new_block_2, 1)
    print('Block 2 replaced successfully')
else:
    print('Warning: old_block_2 not found')

# 3. Replace Bottom Controllers
controllers_marker = '// VISUAL STUDIO / VS CODE IDE CONTROLLERS'
marker_pos = content.find(controllers_marker)
if marker_pos == -1:
    print('Error: controllers_marker not found!')
    sys.exit(1)

comment_start = content.rfind('// ===', 0, marker_pos)
if comment_start == -1:
    comment_start = marker_pos

new_controllers = '''// ==========================================
// VISUAL STUDIO / VS CODE IDE CONTROLLERS & AI COPILOT
// ==========================================

let vscodeActiveLine = 1;
let vscodeCopilotSuggestion = '';
let vscodeCopilotTimer = null;
let vscodeLastInspectedLine = null;

function updateVscodeLineNumbers() {
  const textarea = document.getElementById('code-editor-textarea');
  const gutter = document.getElementById('vscode-gutter-lines');
  if (!textarea || !gutter) return;

  const lines = (textarea.value || '').split('\\n');
  const count = Math.max(lines.length, 1);
  let html = '';
  for (let i = 1; i <= count; i++) {
    const isActive = (i === vscodeActiveLine);
    html += `<div class="vscode-gutter-line ${isActive ? 'vscode-gutter-line-active text-amber-300 font-bold bg-white/10' : ''}" data-line="${i}">${i}</div>`;
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
  const lines = textBefore.split('\\n');
  const lineNum = lines.length;
  const colNum = lines[lines.length - 1].length + 1;
  vscodeActiveLine = lineNum;

  if (posEl) {
    posEl.textContent = `Ln ${lineNum}, Col ${colNum}`;
  }
}

function handleVscodeEditorClick(e) {
  updateVscodeCursorPosition();
  updateVscodeLineNumbers();
}

function handleVscodeEditorKeyup(e) {
  if (e.key === 'ArrowUp' || e.key === 'ArrowDown' || e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
    updateVscodeCursorPosition();
    updateVscodeLineNumbers();
  }
}

function handleVscodeGutterClick(e) {
  const lineEl = e.target.closest('[data-line]');
  if (!lineEl) return;
  const lineNum = parseInt(lineEl.getAttribute('data-line'), 10);
  if (isNaN(lineNum)) return;
  selectVscodeGutterLine(lineNum);
}

function selectVscodeGutterLine(lineNum) {
  const textarea = document.getElementById('code-editor-textarea');
  if (!textarea) return;

  vscodeActiveLine = lineNum;
  vscodeLastInspectedLine = lineNum;
  updateVscodeLineNumbers();

  const lines = (textarea.value || '').split('\\n');
  const targetLineText = lines[lineNum - 1] || '';

  // Show Inspector Bar
  const inspector = document.getElementById('vscode-line-inspector');
  const numEl = document.getElementById('inspector-line-num');
  const prevEl = document.getElementById('inspector-line-preview');

  if (inspector && numEl && prevEl) {
    numEl.textContent = lineNum;
    prevEl.textContent = targetLineText.trim() || '(Dòng trống)';
    inspector.classList.remove('hidden');
  }

  // Calculate position in textarea to move cursor
  let charPos = 0;
  for (let i = 0; i < lineNum - 1; i++) {
    charPos += (lines[i] ? lines[i].length : 0) + 1;
  }
  textarea.focus();
  textarea.setSelectionRange(charPos, charPos + targetLineText.length);
  updateVscodeCursorPosition();
}

function handleVscodeCodeInput() {
  saveCurrentCodeDebounced();
  updateVscodeLineNumbers();
  updateVscodeCursorPosition();

  // Trigger Copilot suggestion with debounce (650ms)
  if (vscodeCopilotTimer) clearTimeout(vscodeCopilotTimer);
  vscodeCopilotTimer = setTimeout(() => {
    triggerVscodeCopilotSuggest();
  }, 650);
}

function handleVscodeEditorKeydown(e) {
  const textarea = document.getElementById('code-editor-textarea');
  if (!textarea) return;

  // 1. If Copilot suggestion is open and user presses Tab -> Accept suggestion
  if (e.key === 'Tab' && vscodeCopilotSuggestion) {
    e.preventDefault();
    acceptVscodeCopilotSuggestion();
    return;
  }

  // 2. Escape closes suggestion or inspector
  if (e.key === 'Escape') {
    if (vscodeCopilotSuggestion) {
      dismissVscodeCopilotSuggestion();
      return;
    }
    const inspector = document.getElementById('vscode-line-inspector');
    if (inspector && !inspector.classList.contains('hidden')) {
      inspector.classList.add('hidden');
      return;
    }
  }

  // 3. Manual Copilot trigger: Alt + \\ or Ctrl + Space
  if ((e.altKey && e.key === '\\\\') || (e.ctrlKey && e.code === 'Space')) {
    e.preventDefault();
    triggerVscodeCopilotSuggest(true);
    return;
  }

  // 4. Standard 4 spaces indentation for Tab key
  if (e.key === 'Tab') {
    e.preventDefault();
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const val = textarea.value;

    if (e.shiftKey) {
      // Shift+Tab unindent
      const before = val.substring(0, start);
      const after = val.substring(end);
      const lineStart = before.lastIndexOf('\\n') + 1;
      const currentLine = val.substring(lineStart, end);
      if (currentLine.startsWith('    ')) {
        textarea.value = val.substring(0, lineStart) + currentLine.substring(4) + after;
        textarea.selectionStart = textarea.selectionEnd = Math.max(lineStart, start - 4);
      }
    } else {
      // Tab indent 4 spaces
      textarea.value = val.substring(0, start) + '    ' + val.substring(end);
      textarea.selectionStart = textarea.selectionEnd = start + 4;
    }
    handleVscodeCodeInput();
  }
}

async function triggerVscodeCopilotSuggest(force = false) {
  const textarea = document.getElementById('code-editor-textarea');
  const ex = STATE.exercises.list[STATE.exercises.selectedIndex];
  if (!textarea || !ex) return;

  const code = textarea.value || '';
  if (!force && code.trim().length < 8) return;

  const selStart = textarea.selectionStart || 0;
  const textBefore = code.substring(0, selStart);
  const lines = textBefore.split('\\n');
  const lineNum = lines.length;
  const colNum = lines[lines.length - 1].length + 1;

  try {
    const res = await fetch('/api/code/suggest', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        code: code,
        language: ex.language || 'cpp',
        line: lineNum,
        column: colNum,
        problem_title: ex.title || ''
      })
    });
    const data = await res.json();
    if (data.ok && data.suggestion && data.suggestion.trim()) {
      showVscodeCopilotSuggestion(data.suggestion);
    } else {
      dismissVscodeCopilotSuggestion();
    }
  } catch (err) {
    console.warn('Copilot error:', err);
    dismissVscodeCopilotSuggestion();
  }
}

function showVscodeCopilotSuggestion(text) {
  vscodeCopilotSuggestion = text;
  const banner = document.getElementById('vscode-copilot-banner');
  const textEl = document.getElementById('copilot-suggestion-text');
  if (banner && textEl) {
    textEl.textContent = text;
    banner.classList.remove('hidden');
  }
}

function dismissVscodeCopilotSuggestion() {
  vscodeCopilotSuggestion = '';
  const banner = document.getElementById('vscode-copilot-banner');
  if (banner) banner.classList.add('hidden');
}

function acceptVscodeCopilotSuggestion() {
  if (!vscodeCopilotSuggestion) return;
  const textarea = document.getElementById('code-editor-textarea');
  if (!textarea) return;

  const start = textarea.selectionStart;
  const end = textarea.selectionEnd;
  const val = textarea.value;

  const insertion = vscodeCopilotSuggestion;
  textarea.value = val.substring(0, start) + insertion + val.substring(end);
  textarea.selectionStart = textarea.selectionEnd = start + insertion.length;

  dismissVscodeCopilotSuggestion();
  handleVscodeCodeInput();
  showToast('Đã áp dụng gợi ý AI Copilot! ⚡', 'success');
}

// ==========================================
// LINE-LEVEL AI INSPECTOR & FULLSCREEN VIEWER
// ==========================================

async function askAiAboutCurrentLine() {
  const lineNum = vscodeLastInspectedLine || vscodeActiveLine;
  await callAiLineInspector(lineNum, 'explain');
}

async function fixAiCurrentLine() {
  const lineNum = vscodeLastInspectedLine || vscodeActiveLine;
  await callAiLineInspector(lineNum, 'fix');
}

async function callAiLineInspector(lineNum, action) {
  const textarea = document.getElementById('code-editor-textarea');
  const ex = STATE.exercises.list[STATE.exercises.selectedIndex];
  if (!textarea || !ex) return;

  const code = textarea.value || '';
  const testRes = STATE.exercises.testResults[ex.id];
  const currentError = (testRes && !testRes.all_passed)
    ? (testRes.compile_error || (testRes.results && testRes.results.find(r => !r.passed)?.output) || '')
    : '';

  showToast(`Đang gửi yêu cầu phân tích dòng ${lineNum} tới AI... 🧠`, 'info');

  try {
    const res = await fetch('/api/code/inspect-line', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        code: code,
        language: ex.language || 'cpp',
        line: lineNum,
        action: action,
        problem_title: ex.title || '',
        current_error: currentError
      })
    });

    const data = await res.json();
    if (!data.ok) {
      showToast(data.error || 'Lỗi khi gọi AI phân tích dòng!', 'error');
      return;
    }

    renderAiFullscreenInspectorResult(data, code, lineNum, action);
  } catch (err) {
    showToast(`Không thể kết nối AI: ${err.message}`, 'error');
  }
}

function renderAiFullscreenInspectorResult(data, sourceCode, targetLine, action) {
  const existing = document.getElementById('ai-fullscreen-inspector-overlay');
  if (existing) existing.remove();

  const lines = sourceCode.split('\\n');
  const codeLinesHtml = lines.map((line, idx) => {
    const ln = idx + 1;
    const isTarget = (ln === targetLine);
    return `<div class="flex items-start text-xs font-mono leading-relaxed px-3 py-0.5 ${isTarget ? 'bg-amber-500/20 border-l-4 border-amber-400 font-bold' : 'hover:bg-white/5'}">
      <span class="w-10 select-none text-right pr-4 text-slate-500 font-mono">${ln}</span>
      <span class="${isTarget ? 'text-amber-200' : 'text-slate-300'} whitespace-pre overflow-x-auto">${escapeHtml(line || ' ')}</span>
    </div>`;
  }).join('');

  const overlay = document.createElement('div');
  overlay.id = 'ai-fullscreen-inspector-overlay';
  overlay.className = 'fixed inset-0 z-50 bg-[#121212] text-slate-100 flex flex-col animate-fadeIn overflow-hidden';

  overlay.innerHTML = `
    <!-- Fullscreen Header -->
    <div class="flex items-center justify-between px-6 py-3 bg-[#1e1e1e] border-b border-[#2d2d2d] shadow-lg flex-shrink-0">
      <div class="flex items-center gap-3">
        <div class="w-9 h-9 rounded-xl bg-gradient-to-tr from-[#4285f4] via-[#9b72cf] to-[#d96570] flex items-center justify-center shadow-md">
          <svg class="w-5 h-5 text-white animate-spin-slow" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 2L14.5 9.5L22 12L14.5 14.5L12 22L9.5 14.5L2 12L9.5 9.5L12 2Z"/>
          </svg>
        </div>
        <div>
          <div class="flex items-center gap-2">
            <h3 class="text-base font-bold text-white">
              ${action === 'fix' ? '⚡ AI Chẩn Đoán & Sửa Lỗi Dòng' : '💬 AI Phân Tích & Giải Thích Dòng'} ${targetLine}
            </h3>
            <span class="px-2 py-0.5 rounded text-[11px] font-mono font-bold ${action === 'fix' ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' : 'bg-blue-500/20 text-blue-400 border border-blue-500/30'}">
              ${action === 'fix' ? 'AUTO-FIX MODE' : 'EXPLANATION MODE'}
            </span>
          </div>
          <p class="text-xs text-slate-400">Chế độ toàn màn hình: Góc nhìn chuyên sâu từ AI Senior Architect</p>
        </div>
      </div>

      <div class="flex items-center gap-3">
        ${data.patched_code ? `
          <button type="button" onclick="applyAiFullscreenFixedCode()" class="px-4 py-2 rounded-lg bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-bold text-xs flex items-center gap-2 shadow-lg transition-transform active:scale-95">
            <span>🚀</span> Áp Dụng Toàn Bộ Code Sửa
          </button>
        ` : ''}
        <button type="button" onclick="document.getElementById('ai-fullscreen-inspector-overlay').remove()" class="px-3 py-2 rounded-lg bg-[#2a2a2a] hover:bg-[#383838] text-slate-300 hover:text-white text-xs font-bold flex items-center gap-1.5 transition-colors">
          <span>✕</span> Đóng Toàn Màn Hình
        </button>
      </div>
    </div>

    <!-- Fullscreen Dual Pane Body -->
    <div class="flex-1 flex flex-col lg:flex-row overflow-hidden">
      <!-- Left Pane: Source Code with Target Line Highlighted -->
      <div class="w-full lg:w-5/12 bg-[#181818] border-r border-[#2d2d2d] flex flex-col overflow-hidden">
        <div class="px-4 py-2.5 bg-[#1f1f1f] border-b border-[#2d2d2d] flex items-center justify-between text-xs font-mono text-slate-400">
          <span class="flex items-center gap-1.5">
            <span>📄</span> Mã nguồn hiện tại
          </span>
          <span class="text-amber-400 font-bold">Đang xét: Dòng ${targetLine}</span>
        </div>
        <div class="flex-1 overflow-y-auto py-3 custom-scrollbar">
          ${codeLinesHtml}
        </div>
      </div>

      <!-- Right Pane: Deep AI Analysis & Lessons -->
      <div class="w-full lg:w-7/12 bg-[#141414] flex flex-col overflow-hidden">
        <div class="px-5 py-2.5 bg-[#1a1a1a] border-b border-[#2d2d2d] flex items-center justify-between text-xs text-slate-400">
          <span class="flex items-center gap-2 font-bold text-slate-200">
            <span>✨</span> Lời giải thích & Hướng dẫn học tập
          </span>
          <span class="text-[11px] font-mono text-cyan-400">Google Gemini Pro Engine</span>
        </div>

        <div class="flex-1 overflow-y-auto p-6 space-y-4 custom-scrollbar">
          <!-- Target Line Card -->
          <div class="p-4 rounded-xl bg-[#1e1e1e] border border-[#333333] shadow-sm">
            <div class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-1">Mã lệnh tại dòng ${targetLine}:</div>
            <pre class="text-xs font-mono text-amber-300 bg-[#121212] p-2.5 rounded-lg border border-[#2b2b2b] overflow-x-auto">${escapeHtml(data.target_line_text || lines[targetLine - 1] || '')}</pre>
          </div>

          <!-- Explanation Box -->
          <div class="p-5 rounded-xl bg-[#1a1c23] border border-[#2b3548] shadow-md">
            <div class="flex items-center gap-2 text-sm font-bold text-cyan-300 mb-2">
              <span>💡</span> Chi tiết phân tích kỹ thuật:
            </div>
            <div class="text-xs sm:text-sm text-slate-200 leading-relaxed space-y-2">
              ${formatRichText(data.explanation || '')}
            </div>
          </div>

          <!-- If Patched Code Exists: Side-by-side or Replacement snippet -->
          ${data.patched_line ? `
            <div class="p-4 rounded-xl bg-emerald-950/20 border border-emerald-500/30">
              <div class="flex items-center justify-between mb-2">
                <span class="text-xs font-bold text-emerald-400 flex items-center gap-1.5">
                  <span>✅</span> Dòng code đã được sửa tối ưu:
                </span>
                <button type="button" onclick="applySingleLineFix(${targetLine}, ${escapeJsString(data.patched_line)})" class="px-2.5 py-1 rounded bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold">
                  Thay thế riêng dòng này
                </button>
              </div>
              <pre class="text-xs font-mono text-emerald-300 bg-[#0e1612] p-3 rounded-lg border border-emerald-800/40 overflow-x-auto">${escapeHtml(data.patched_line)}</pre>
            </div>
          ` : ''}

          <!-- Learning Takeaway Card -->
          <div class="p-4 rounded-xl bg-purple-950/20 border border-purple-500/30">
            <div class="flex items-center gap-2 text-xs font-bold text-purple-300 uppercase tracking-wider mb-1.5">
              <span>🎓</span> Bài học cốt lõi cần nhớ:
            </div>
            <p class="text-xs text-slate-300 leading-relaxed">
              Khi viết code thuật toán, hãy luôn kiểm tra điều kiện biên, giới hạn của biến chỉ số mảng, và đảm bảo mọi biến được khởi tạo trước khi truy xuất bộ nhớ.
            </p>
          </div>
        </div>
      </div>
    </div>
  `;

  document.body.appendChild(overlay);
  window.__LAST_PATCHED_CODE = data.patched_code || '';
}

function escapeJsString(str) {
  if (!str) return '""';
  return JSON.stringify(str);
}

function applySingleLineFix(lineNum, newLineText) {
  const textarea = document.getElementById('code-editor-textarea');
  if (!textarea) return;

  const lines = (textarea.value || '').split('\\n');
  if (lineNum >= 1 && lineNum <= lines.length) {
    lines[lineNum - 1] = newLineText;
    textarea.value = lines.join('\\n');
    handleVscodeCodeInput();
    showToast(`Đã thay thế thành công dòng ${lineNum}! 🚀`, 'success');
    const overlay = document.getElementById('ai-fullscreen-inspector-overlay');
    if (overlay) overlay.remove();
  }
}

function applyAiFullscreenFixedCode() {
  if (!window.__LAST_PATCHED_CODE) {
    showToast('Không có bản code sửa đổi để áp dụng!', 'warning');
    return;
  }

  const textarea = document.getElementById('code-editor-textarea');
  const ex = STATE.exercises.list[STATE.exercises.selectedIndex];
  if (textarea && ex) {
    textarea.value = window.__LAST_PATCHED_CODE;
    STATE.exercises.userCode[ex.id] = window.__LAST_PATCHED_CODE;
    saveCurrentCodeDebounced();
    updateVscodeLineNumbers();
    updateVscodeCursorPosition();
    showToast('Đã áp dụng toàn bộ code sửa vào Editor! 🚀', 'success');

    const overlay = document.getElementById('ai-fullscreen-inspector-overlay');
    if (overlay) overlay.remove();
  }
}

// ==========================================
// FULLSCREEN TOGGLES FOR CONSOLE AND TUTOR
// ==========================================

function openAiFullscreenForCurrentTab() {
  const activeTab = STATE.exercises.currentConsoleTab || 'testcases';
  const ex = STATE.exercises.list[STATE.exercises.selectedIndex];
  if (!ex) return;

  let title = 'AI Toàn Màn Hình';
  let contentHtml = '';

  if (activeTab === 'aireview') {
    title = '🤖 AI Senior Code Review';
    const aiRev = STATE.exercises.aiReviews[ex.id];
    contentHtml = renderAiReviewPane(aiRev);
  } else if (activeTab === 'aifix') {
    title = '🛠️ AI Sửa Lỗi & Nâng Cấp Code';
    const upgrade = STATE.exercises.aiUpgrades ? STATE.exercises.aiUpgrades[ex.id] : null;
    contentHtml = renderAiFixPane(upgrade);
  } else if (activeTab === 'testcases') {
    title = '🧪 Test Cases & Kết Quả Chấm';
    const testRes = STATE.exercises.testResults[ex.id];
    contentHtml = renderTestCasesPane(ex, testRes);
  } else {
    title = '💻 Terminal & Stdin/Stdout';
    const stdout = document.getElementById('custom-stdout-output');
    contentHtml = `<pre class="p-4 rounded-xl bg-[#1e1e1e] font-mono text-xs text-emerald-300">${stdout ? stdout.textContent : 'Chưa có output'}</pre>`;
  }

  const existing = document.getElementById('ai-fullscreen-reader-overlay');
  if (existing) existing.remove();

  const overlay = document.createElement('div');
  overlay.id = 'ai-fullscreen-reader-overlay';
  overlay.className = 'fixed inset-0 z-50 bg-[#121212] text-slate-100 flex flex-col animate-fadeIn overflow-hidden';

  overlay.innerHTML = `
    <div class="flex items-center justify-between px-6 py-3.5 bg-[#1e1e1e] border-b border-[#2d2d2d] shadow-lg flex-shrink-0">
      <div class="flex items-center gap-3">
        <div class="w-9 h-9 rounded-xl bg-gradient-to-tr from-[#4285f4] via-[#9b72cf] to-[#d96570] flex items-center justify-center shadow-md">
          <span class="text-white font-bold">✨</span>
        </div>
        <div>
          <h3 class="text-base font-bold text-white">${title}</h3>
          <p class="text-xs text-slate-400">Bài tập: ${escapeHtml(ex.title)}</p>
        </div>
      </div>
      <button type="button" onclick="document.getElementById('ai-fullscreen-reader-overlay').remove()" class="px-3 py-1.5 rounded-lg bg-[#2a2a2a] hover:bg-[#383838] text-slate-300 hover:text-white text-xs font-bold transition-colors">
        ✕ Thoát Toàn Màn Hình
      </button>
    </div>
    <div class="flex-1 overflow-y-auto p-6 max-w-5xl mx-auto w-full custom-scrollbar space-y-4">
      ${contentHtml}
    </div>
  `;

  document.body.appendChild(overlay);
  renderAllMathOnPage(overlay);
  refreshIcons();
}

function toggleVscodePanelFullscreen() {
  openAiFullscreenForCurrentTab();
}

function toggleVscodeSidebar() {
  const sidebar = document.getElementById('vscode-sidebar-pane');
  if (!sidebar) return;
  sidebar.classList.toggle('hidden');
}

function toggleVscodeFullscreen() {
  const ide = document.getElementById('vscode-ide-root');
  if (!ide) return;
  if (!document.fullscreenElement) {
    if (ide.requestFullscreen) ide.requestFullscreen();
    else if (ide.webkitRequestFullscreen) ide.webkitRequestFullscreen();
  } else {
    if (document.exitFullscreen) document.exitFullscreen();
  }
}

function toggleTutorFullscreen() {
  const tutorPane = document.getElementById('view-tutor') || document.getElementById('modal-exercise-tutor');
  if (!tutorPane) return;

  if (!document.fullscreenElement) {
    if (tutorPane.requestFullscreen) tutorPane.requestFullscreen();
    else if (tutorPane.webkitRequestFullscreen) tutorPane.webkitRequestFullscreen();
  } else {
    if (document.exitFullscreen) document.exitFullscreen();
  }
}
'''

content = content[:comment_start] + new_controllers
with open(app_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Successfully patched static/app.js!')
