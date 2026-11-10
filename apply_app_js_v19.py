import re

app_path = r'C:\Users\PC\.gemini\antigravity\scratch\unimaster-ai\static\app.js'
with open(app_path, 'r', encoding='utf-8') as f:
    js = f.read()

# =========================================================================
# 1. Update loadQuestionDiscussions & Add toggleQuestionDiscussionBox & submitQuestionDiscussion
# =========================================================================
disc_fn_old = '''function loadQuestionDiscussions(qid) {
  const listEl = document.getElementById('q-discussion-list');
  const countEl = document.getElementById('q-discussion-count-badge') || document.getElementById('q-discussion-count');
  if (!listEl || !qid) return;

  try {
    const res = await apiFetch(`/api/questions/${qid}/discussions`);
    const items = res.discussions || [];
    STATE.discussionsCache[qid] = items;
    if (countEl) countEl.textContent = `${items.length} bình luận`;

    if (!items.length) {
      listEl.innerHTML = `<div class="text-xs txt-muted italic py-1">Chưa có mẹo nhớ cộng đồng nào cho câu này. Hãy là người đầu tiên chia sẻ mẹo giải nhanh!</div>`;
      return;
    }

    listEl.innerHTML = items
      .map(
        (c) => `
        <div class="p-3 rounded-xl flex items-start justify-between gap-3 text-xs" style="background-color: var(--bg-surface); border: 1px solid var(--border);">
          <div class="space-y-1">
            <div class="flex flex-wrap items-center gap-1.5">
              <span class="font-extrabold txt-main">👤 ${escapeHtml(c.author_name || 'Sinh viên')}</span>
              <span class="badge-brand px-2 py-0.5 rounded text-[10px] font-bold">${c.author_role === 'ta' ? '⭐ Trợ giảng' : 'Học viên'}</span>
              <span class="text-[10px] txt-muted">${escapeHtml(c.created_at || 'Vừa xong')}</span>
            </div>
            <div class="txt-sub text-xs leading-relaxed">${escapeHtml(c.content || '')}</div>
          </div>
          <button type="button" onclick="upvoteQuestionDiscussion(${c.id}, ${qid})" class="btn-soft px-2 py-1 text-[11px] font-bold flex items-center gap-1 shrink-0 text-amber-400">
            <span>👍</span> <span>${c.upvotes || 0}</span>
          </button>
        </div>
      `
      )
      .join('');
  } catch (err) {
    console.warn('Error loading discussions:', err);
  }
}'''

disc_fn_new = '''function toggleQuestionDiscussionBox(forceState = null) {
  const box = document.getElementById('q-community-discussion-box');
  if (!box) return;

  const willShow = forceState !== null ? forceState : box.classList.contains('hidden');
  if (willShow) {
    box.classList.remove('hidden');
    const q = (STATE.exam?.active && STATE.exam?.questions) ? STATE.exam.questions[STATE.exam.currentIndex] : null;
    if (q) {
      loadQuestionDiscussions(q.id);
      setTimeout(() => document.getElementById('q-disc-content-input')?.focus(), 120);
    }
  } else {
    box.classList.add('hidden');
  }
}

async function loadQuestionDiscussions(qid) {
  const listEl = document.getElementById('q-discussion-list');
  const countEl = document.getElementById('q-discussion-count-badge');
  const toolbarCountEl = document.getElementById('q-toolbar-disc-count');
  if (!listEl || !qid) return;

  try {
    const res = await apiFetch(`/api/questions/${qid}/discussions`);
    const items = res.comments || res.discussions || [];
    STATE.discussionsCache[qid] = items;

    const countText = `${items.length} bình luận`;
    if (countEl) countEl.textContent = countText;
    if (toolbarCountEl) toolbarCountEl.textContent = items.length;

    if (!items.length) {
      // High-yield verified peer/TA tips for CTUMP/Medical or Programming questions
      const currentQ = (STATE.exam?.active && STATE.exam?.questions) ? STATE.exam.questions[STATE.exam.currentIndex] : null;
      let seedTip = 'Chưa có bình luận nào cho câu này. Hãy chia sẻ mẹo nhớ hoặc câu hỏi của bạn!';
      if (currentQ) {
        const text = currentQ.question_text || '';
        if (text.includes('Cholesterol') || text.includes('Lipid')) {
          seedTip = '💡 Mẹo nhớ CTUMP: Công thức Friedewald: LDL-C = TC - HDL-C - (TG/5). Chỉ áp dụng khi TG < 400 mg/dL!';
        } else if (text.includes('Biuret') || text.includes('Protein')) {
          seedTip = '💡 Mẹo nhớ CTUMP: Phản ứng Biuret đặc trưng cho liên kết peptid (-CO-NH-), tạo phức màu tím sim với Cu2+ trong môi trường kiềm.';
        } else if (text.includes('Molish') || text.includes('Glucid')) {
          seedTip = '💡 Mẹo nhớ CTUMP: Thuốc thử Molish gồm alpha-naphthol trong cồn, tạo phức màu tím ở mặt phân cách giữa 2 lớp chất lỏng!';
        } else if (text.includes('class') || text.includes('virtual') || text.includes('override')) {
          seedTip = '💡 Mẹo nhớ OOP: Phương thức ở lớp cha phải có từ khóa "virtual" thì lớp con mới dùng "override" để ghi đè đa hình được!';
        }
      }
      listEl.innerHTML = `
        <div class="p-3 rounded-xl flex items-start gap-2.5 text-xs border border-indigo-500/30 bg-indigo-500/10 text-indigo-300">
          <span class="text-base">💡</span>
          <div>
            <div class="font-bold text-white">Gợi ý từ Trợ Giảng UniMaster AI:</div>
            <div>${seedTip}</div>
          </div>
        </div>
      `;
      return;
    }

    listEl.innerHTML = items
      .map(
        (c) => `
        <div class="p-3 rounded-xl flex items-start justify-between gap-3 text-xs" style="background-color: var(--bg-surface); border: 1px solid var(--border);">
          <div class="space-y-1">
            <div class="flex flex-wrap items-center gap-1.5">
              <span class="font-extrabold txt-main">👤 ${escapeHtml(c.author_name || 'Sinh viên')}</span>
              <span class="badge-brand px-2 py-0.5 rounded text-[10px] font-bold">${c.author_role === 'ta' ? '⭐ Trợ giảng' : 'Học viên'}</span>
              <span class="text-[10px] txt-muted">${escapeHtml(c.created_at || 'Vừa xong')}</span>
            </div>
            <div class="txt-sub text-xs leading-relaxed">${escapeHtml(c.content || '')}</div>
          </div>
          <button type="button" onclick="upvoteQuestionDiscussion(${c.id}, ${qid})" class="btn-soft px-2 py-1 text-[11px] font-bold flex items-center gap-1 shrink-0 text-amber-400">
            <span>👍</span> <span>${c.upvotes || 0}</span>
          </button>
        </div>
      `
      )
      .join('');
  } catch (err) {
    console.warn('Error loading discussions:', err);
  }
}'''

if disc_fn_old in js:
    js = js.replace(disc_fn_old, disc_fn_new, 1)
    print("1. Updated loadQuestionDiscussions and toggleQuestionDiscussionBox")
else:
    print("WARNING: disc_fn_old not found!")

# =========================================================================
# 2. Update submitQuestionDiscussion with Optimistic UI
# =========================================================================
submit_old = '''async function submitQuestionDiscussion() {
  const q = STATE.exam.questions[STATE.exam.currentIndex];
  if (!q) return;

  const authorInp = document.getElementById('q-disc-author-input');
  const contentInp = document.getElementById('q-disc-content-input');
  const author = authorInp?.value.trim() || 'Sinh viên';
  const content = contentInp?.value.trim();

  if (!content) {
    showToast('Vui lòng nhập nội dung bình luận!', 'warning');
    return;
  }

  const res = await apiFetch(`/api/questions/${q.id}/discussions`, {
    method: 'POST',
    body: JSON.stringify({
      author_name: author,
      content,
      author_role: 'student'
    })
  });

  if (res.success) {
    showToast('Đã đăng thảo luận thành công!', 'success');
    if (contentInp) contentInp.value = '';
    loadQuestionDiscussions(q.id);
  } else {
    showToast(res.error || 'Lỗi gửi thảo luận', 'error');
  }
}'''

submit_new = '''async function submitQuestionDiscussion() {
  const currentQ = (STATE.exam?.active && STATE.exam?.questions) ? STATE.exam.questions[STATE.exam.currentIndex] : null;
  if (!currentQ) return;

  const authorInp = document.getElementById('q-disc-author-input');
  const contentInp = document.getElementById('q-disc-content-input');
  const author = (authorInp?.value || '').trim() || 'Sinh viên UniMaster';
  const content = (contentInp?.value || '').trim();

  if (!content) {
    showToast('Vui lòng nhập nội dung bình luận!', 'warning');
    return;
  }

  // Instant Optimistic UI
  const listEl = document.getElementById('q-discussion-list');
  const countEl = document.getElementById('q-discussion-count-badge');
  const toolbarCountEl = document.getElementById('q-toolbar-disc-count');
  
  const tempCommentHtml = `
    <div class="p-3 rounded-xl flex items-start justify-between gap-3 text-xs animate-fade-in" style="background-color: var(--bg-surface); border: 1px solid var(--brand-border);">
      <div class="space-y-1">
        <div class="flex flex-wrap items-center gap-1.5">
          <span class="font-extrabold txt-main">👤 ${escapeHtml(author)}</span>
          <span class="badge-brand px-2 py-0.5 rounded text-[10px] font-bold">Vừa xong</span>
        </div>
        <div class="txt-sub text-xs leading-relaxed">${escapeHtml(content)}</div>
      </div>
      <span class="text-xs text-emerald-400 font-bold shrink-0">✓ Đã gửi</span>
    </div>
  `;
  if (listEl) {
    if (listEl.innerHTML.includes('Chưa có bình luận nào')) {
      listEl.innerHTML = tempCommentHtml;
    } else {
      listEl.innerHTML = tempCommentHtml + listEl.innerHTML;
    }
  }
  if (contentInp) contentInp.value = '';

  try {
    const res = await apiFetch(`/api/questions/${currentQ.id}/discussions`, {
      method: 'POST',
      body: JSON.stringify({
        author_name: author,
        content: content,
        author_role: 'student'
      })
    });
    if (res && res.success) {
      showToast('Đã đăng bình luận thành công!', 'success');
      const currCount = parseInt(toolbarCountEl?.textContent || '0', 10) + 1;
      if (toolbarCountEl) toolbarCountEl.textContent = currCount;
      if (countEl) countEl.textContent = `${currCount} bình luận`;
    }
  } catch (err) {
    showToast('Lỗi gửi bình luận: ' + err.message, 'warning');
  }
}'''

if submit_old in js:
    js = js.replace(submit_old, submit_new, 1)
    print("2. Updated submitQuestionDiscussion with Optimistic UI")
else:
    print("WARNING: submit_old not found!")

# =========================================================================
# 3. Update toggleFloatingTutorSize with Full-Screen Centering
# =========================================================================
toggle_size_old = '''function toggleFloatingTutorSize() {
  const win = document.getElementById('floating-tutor-window');
  const btn = document.getElementById('btn-ft-expand');
  const backdrop = document.getElementById('floating-tutor-backdrop');
  if (!win) return;
  windowTutorSizeExpanded = !windowTutorSizeExpanded;
  win.classList.toggle('expanded', windowTutorSizeExpanded);
  if (backdrop) backdrop.classList.toggle('hidden', !windowTutorSizeExpanded);
  if (btn) btn.textContent = windowTutorSizeExpanded ? '🗗' : '⛶';
  playSound('click');
}'''

toggle_size_new = '''function toggleFloatingTutorSize() {
  const container = document.getElementById('floating-tutor-container');
  const win = document.getElementById('floating-tutor-window');
  const btn = document.getElementById('btn-ft-expand');
  const label = document.getElementById('ft-expand-label');
  const svg = document.getElementById('ft-expand-svg');
  if (!win) return;

  windowTutorSizeExpanded = !windowTutorSizeExpanded;

  if (container) {
    container.classList.toggle('tutor-expanded-parent', windowTutorSizeExpanded);
  }
  win.classList.toggle('expanded', windowTutorSizeExpanded);

  if (label) {
    label.textContent = windowTutorSizeExpanded ? 'Thu Nhỏ' : 'Phóng To';
  }
  if (svg) {
    svg.innerHTML = windowTutorSizeExpanded
      ? '<path d="M4 14h6v6M20 10h-6V4M14 10l7-7M3 21l7-7"/>'
      : '<path d="M15 3h6v6M9 21H3v-6M21 3l-7 7M3 21l7-7"/>';
  }
  if (btn) {
    btn.title = windowTutorSizeExpanded ? 'Thu nhỏ cửa sổ AI' : 'Phóng to hết nguyên màn hình';
  }

  const chatMsgs = document.getElementById('floating-chat-messages');
  if (chatMsgs) {
    setTimeout(() => {
      chatMsgs.scrollTop = chatMsgs.scrollHeight;
    }, 100);
  }
  playSound('click');
}

async function sendFloatingTutorCustomMessage(customText) {
  const input = document.getElementById('floating-chat-input');
  if (input) {
    input.value = customText;
    await sendFloatingTutorMessage();
  }
}'''

if toggle_size_old in js:
    js = js.replace(toggle_size_old, toggle_size_new, 1)
    print("3. Updated toggleFloatingTutorSize and added sendFloatingTutorCustomMessage")
else:
    print("WARNING: toggle_size_old not found!")

# =========================================================================
# 4. Update buildCodeWindowHtml with Interactive Code Lines & Whole-Code Ask AI
# =========================================================================
code_fn_old = '''  const rowsHtml = lines
    .map((line, i) => {
      let contentHtml = '&nbsp;';
      if (line.trim() !== '') {
        try {
          contentHtml = grammar ? Prism.highlight(line, grammar, lang) : escapeHtml(line);
        } catch (_) {
          contentHtml = escapeHtml(line);
        }
      }
      return `<tr class="code-line-row">
        <td class="code-line-num">${i + 1}</td>
        <td class="code-line-content font-mono">${contentHtml}</td>
      </tr>`;
    })
    .join('');'''

code_fn_new = '''  const rowsHtml = lines
    .map((line, i) => {
      let contentHtml = '&nbsp;';
      if (line.trim() !== '') {
        try {
          contentHtml = grammar ? Prism.highlight(line, grammar, lang) : escapeHtml(line);
        } catch (_) {
          contentHtml = escapeHtml(line);
        }
      }
      return `<tr class="code-line-tr group" onclick="askAiAboutCodeLine('${uid}', ${i + 1})" title="Bấm vào dòng code này để hỏi Gia Sư AI">
        <td class="code-line-num select-none text-right pr-3">${i + 1}</td>
        <td class="code-line-content font-mono">${contentHtml}</td>
        <td class="text-right pr-2 whitespace-nowrap select-none">
          <span class="code-line-ai-pill text-[10px] font-bold text-indigo-300 bg-indigo-900/80 border border-indigo-500/40 px-2 py-0.5 rounded-lg shadow-sm">
            🤖 Hỏi AI
          </span>
        </td>
      </tr>`;
    })
    .join('');'''

if code_fn_old in js:
    js = js.replace(code_fn_old, code_fn_new, 1)
    print("4. Updated buildCodeWindowHtml rows with interactive click & AI pills")
else:
    print("WARNING: code_fn_old not found!")

# Also add askAiAboutCodeLine and askAiAboutWholeCodeSnippet
code_actions_js = '''
function askAiAboutCodeLine(uid, lineNum) {
  const code = CODE_REGISTRY[uid] || '';
  const lines = code.split('\\n');
  const lineText = lines[lineNum - 1] || '';
  if (!lineText.trim()) return;

  openFloatingTutor();
  const query = `Trong bài thực hành lập trình có đoạn mã sau:\\n\\`\\`\\`csharp\\n${code}\\n\\`\\`\\`\\n\\n👉 Em chưa hiểu rõ dòng #${lineNum}: \\`${lineText.trim()}\\`\\nXin Thầy/Cô Gia Sư AI giải thích chi tiết dòng này làm nhiệm vụ gì, cú pháp hoạt động thế nào và các bẫy đề thi hay hỏi về nó?`;
  sendFloatingTutorCustomMessage(query);
}

function askAiAboutWholeCodeSnippet(uid, title = 'Program.cs', lang = 'csharp') {
  const code = CODE_REGISTRY[uid] || '';
  if (!code.trim()) return;

  openFloatingTutor();
  const query = `Em cần giải thích toàn bộ đoạn code "${title}":\\n\\`\\`\\`${lang}\\n${code}\\n\\`\\`\\`\\n\\n👉 Xin Gia Sư AI phân tích từng khối lệnh, cấu trúc giải thuật và kết quả in ra màn hình của đoạn code này!`;
  sendFloatingTutorCustomMessage(query);
}
'''
if 'function askAiAboutCodeLine' not in js:
    js += '\n' + code_actions_js
    print("4b. Appended askAiAboutCodeLine & askAiAboutWholeCodeSnippet")

# In buildCodeWindowHtml header, add "Hỏi AI Cả Đoạn Code Này" button
code_hdr_old = '''<div class="flex items-center gap-1.5">
          <button type="button" onclick="copyCodeSnippet('${uid}')" class="btn-soft !py-0.5 !px-2 text-[10px] flex items-center gap-1">'''

code_hdr_new = '''<div class="flex items-center gap-1.5">
          <button type="button" onclick="askAiAboutWholeCodeSnippet('${uid}', '${escapeHtml(title)}', '${lang}')" class="btn-soft !py-0.5 !px-2 text-[10px] font-black text-indigo-400 hover:text-indigo-300 flex items-center gap-1 border border-indigo-500/40">
            <span>🤖</span> <span>Hỏi AI Cả Đoạn Code</span>
          </button>
          <button type="button" onclick="copyCodeSnippet('${uid}')" class="btn-soft !py-0.5 !px-2 text-[10px] flex items-center gap-1">'''

if code_hdr_old in js:
    js = js.replace(code_hdr_old, code_hdr_new, 1)
    print("4c. Added 'Hỏi AI Cả Đoạn Code' button to code window header")

# =========================================================================
# 5. Text Selection Floating AI Bubble Setup
# =========================================================================
text_select_js = '''
function setupTextSelectionAiListener() {
  const bubble = document.getElementById('text-select-ai-bubble');
  const wordEl = document.getElementById('text-select-ai-word');
  if (!bubble || !wordEl) return;

  let currentSelectedText = '';

  function handleSelection(e) {
    if (bubble.contains(e.target)) return;

    const sel = window.getSelection();
    const str = sel ? sel.toString().trim() : '';

    if (str && str.length >= 2 && str.length <= 90 && !/\\n\\n/.test(str)) {
      currentSelectedText = str;
      wordEl.textContent = `"${str.length > 22 ? str.slice(0, 22) + '...' : str}"`;

      try {
        const range = sel.getRangeAt(0);
        const rect = range.getBoundingClientRect();
        bubble.style.left = `${Math.max(120, Math.min(window.innerWidth - 120, rect.left + rect.width / 2))}px`;
        bubble.style.top = `${Math.max(20, rect.top - 6)}px`;
        bubble.classList.remove('hidden');
      } catch (_) {
        bubble.classList.add('hidden');
      }
    } else {
      currentSelectedText = '';
      bubble.classList.add('hidden');
    }
  }

  document.addEventListener('mouseup', handleSelection);
  document.addEventListener('touchend', () => setTimeout(handleSelection, 60));

  window.askAiAboutSelectedTerm = function(directTerm = null) {
    const term = directTerm || currentSelectedText;
    bubble.classList.add('hidden');
    if (!term) return;

    openFloatingTutor();
    const currentQ = (STATE.exam?.active && STATE.exam?.questions) ? STATE.exam.questions[STATE.exam.currentIndex] : null;
    const contextPrompt = currentQ ? `Trong câu hỏi thi: "${(currentQ.question_text || '').replace(/<[^>]+>/g, '').trim().slice(0, 140)}..."` : 'Trong bài học';
    const query = `${contextPrompt}\\n\\n👉 Em chưa hiểu rõ về thuật ngữ/khái niệm: "${term}".\\nXin Gia Sư AI giải thích thật ngắn gọn, dễ hiểu, đưa ra ví dụ và mẹo ghi nhớ để thi không bị nhầm lẫn!`;
    sendFloatingTutorCustomMessage(query);
  };
}
'''
if 'function setupTextSelectionAiListener' not in js:
    js += '\n' + text_select_js
    print("5. Appended setupTextSelectionAiListener")

# Add setupTextSelectionAiListener() to DOMContentLoaded
dom_target = 'setupKeyboardShortcuts();'
if dom_target in js and 'setupTextSelectionAiListener();' not in js:
    js = js.replace(dom_target, 'setupTextSelectionAiListener();\n  ' + dom_target, 1)
    print("5b. Added setupTextSelectionAiListener() call to DOMContentLoaded")

# =========================================================================
# 6. Safe Archive & Restore for Exam History & Tutor Chat History
# =========================================================================
archive_history_js = '''
// --- UNIMASTER SAFE ARCHIVE SYSTEM (PERMANENT RETENTION & INSTANT RESTORE) ---
const LOCAL_EXAM_ARCHIVE_KEY = 'unimaster_exam_history_archive_v2';
const LOCAL_TUTOR_ARCHIVE_KEY = 'unimaster_tutor_history_archive_v2';

let currentExamHistorySubTab = 'active'; // 'active' | 'archive'
let currentTutorHistorySubTab = 'active'; // 'active' | 'archive'

function getLocalExamArchive() {
  try {
    return JSON.parse(localStorage.getItem(LOCAL_EXAM_ARCHIVE_KEY) || '[]');
  } catch (_) {
    return [];
  }
}

function saveLocalExamArchive(list) {
  try {
    localStorage.setItem(LOCAL_EXAM_ARCHIVE_KEY, JSON.stringify(list || []));
  } catch (_) {}
}

function getLocalTutorArchive() {
  try {
    return JSON.parse(localStorage.getItem(LOCAL_TUTOR_ARCHIVE_KEY) || '[]');
  } catch (_) {
    return [];
  }
}

function saveLocalTutorArchive(list) {
  try {
    localStorage.setItem(LOCAL_TUTOR_ARCHIVE_KEY, JSON.stringify(list || []));
  } catch (_) {}
}

function switchExamHistoryTab(tab) {
  currentExamHistorySubTab = tab;
  const activeBtn = document.getElementById('tab-exam-hist-active');
  const archiveBtn = document.getElementById('tab-exam-hist-archive');
  const archiveActions = document.getElementById('exam-hist-archive-actions');

  if (tab === 'active') {
    activeBtn?.classList.add('bg-indigo-600', 'text-white');
    activeBtn?.classList.remove('text-indigo-300');
    archiveBtn?.classList.remove('bg-amber-600', 'text-white');
    archiveBtn?.classList.add('text-amber-400');
    archiveActions?.classList.add('hidden');
  } else {
    archiveBtn?.classList.add('bg-amber-600', 'text-white');
    archiveBtn?.classList.remove('text-amber-400');
    activeBtn?.classList.remove('bg-indigo-600', 'text-white');
    activeBtn?.classList.add('text-indigo-300');
    archiveActions?.classList.remove('hidden');
  }
  renderLocalExamHistoryModal();
}

function switchTutorHistoryTab(tab) {
  currentTutorHistorySubTab = tab;
  const activeBtn = document.getElementById('tab-tutor-hist-active');
  const archiveBtn = document.getElementById('tab-tutor-hist-archive');
  const archiveActions = document.getElementById('tutor-hist-archive-actions');

  if (tab === 'active') {
    activeBtn?.classList.add('bg-indigo-600', 'text-white');
    archiveBtn?.classList.remove('bg-amber-600', 'text-white');
    archiveActions?.classList.add('hidden');
  } else {
    archiveBtn?.classList.add('bg-amber-600', 'text-white');
    activeBtn?.classList.remove('bg-indigo-600', 'text-white');
    archiveActions?.classList.remove('hidden');
  }
  renderTutorHistoryModal();
}

function restoreAllLocalExamHistory() {
  const archive = getLocalExamArchive();
  if (!archive.length) {
    showToast('Kho lưu trữ bài thi đang trống!', 'info');
    return;
  }
  const activeList = getLocalExamHistory();
  const merged = [...archive, ...activeList];
  saveLocalExamHistory(merged);
  saveLocalExamArchive([]);

  switchExamHistoryTab('active');
  showToast(`✅ Đã khôi phục thành công ${archive.length} bài thi vào danh sách!`, 'success');
}

function restoreSingleExamHistory(examId) {
  const archive = getLocalExamArchive();
  const itemIndex = archive.findIndex((x) => x.id === examId);
  if (itemIndex === -1) return;

  const item = archive[itemIndex];
  archive.splice(itemIndex, 1);
  saveLocalExamArchive(archive);

  const activeList = getLocalExamHistory();
  activeList.unshift(item);
  saveLocalExamHistory(activeList);

  renderLocalExamHistoryModal();
  showToast('✅ Đã khôi phục bài thi này vào danh sách!', 'success');
}

function restoreAllTutorHistory() {
  const archive = getLocalTutorArchive();
  if (!archive.length) {
    showToast('Kho lưu trữ đoạn chat đang trống!', 'info');
    return;
  }
  const activeList = getLocalTutorHistory();
  const merged = [...archive, ...activeList];
  saveLocalTutorHistory(merged);
  saveLocalTutorArchive([]);

  switchTutorHistoryTab('active');
  showToast(`✅ Đã khôi phục ${archive.length} tin nhắn cùng Gia Sư AI!`, 'success');
}

function restoreSingleTutorHistory(chatId) {
  const archive = getLocalTutorArchive();
  const itemIndex = archive.findIndex((x) => x.id === chatId);
  if (itemIndex === -1) return;

  const item = archive[itemIndex];
  archive.splice(itemIndex, 1);
  saveLocalTutorArchive(archive);

  const activeList = getLocalTutorHistory();
  activeList.unshift(item);
  saveLocalTutorHistory(activeList);

  renderTutorHistoryModal();
  showToast('✅ Đã khôi phục đoạn chat này vào danh sách!', 'success');
}
'''

if 'const LOCAL_EXAM_ARCHIVE_KEY' not in js:
    js += '\n' + archive_history_js
    print("6. Appended Safe Archive & Restore functions")

# Replace clearAllLocalExamHistory with safe archive logic
clear_exam_old = '''function clearAllLocalExamHistory() {
  if (confirm('Bạn có chắc muốn xóa toàn bộ lịch sử các lần làm bài trên máy này?')) {
    localStorage.removeItem(LOCAL_EXAM_HISTORY_KEY);
    renderLocalExamHistoryModal();
    showToast('Đã dọn sạch toàn bộ lịch sử làm bài!', 'success');
  }
}'''

clear_exam_new = '''function clearAllLocalExamHistory() {
  const activeList = getLocalExamHistory();
  if (!activeList.length) {
    showToast('Không có bài thi nào trong danh sách đang hiển thị!', 'info');
    return;
  }

  // Safe Archive: NEVER lose user records!
  const archive = getLocalExamArchive();
  const merged = [...activeList, ...archive];
  saveLocalExamArchive(merged);
  saveLocalExamHistory([]);

  // Sync to backend SQLite archive
  activeList.forEach((item) => {
    apiFetch('/api/history/archive', {
      method: 'POST',
      body: JSON.stringify({
        history_type: 'exam',
        item_id: item.id || `exam_${Date.now()}`,
        payload_json: JSON.stringify(item)
      })
    }).catch(() => {});
  });

  renderLocalExamHistoryModal();
  showToast('🛡️ Đã chuyển các bài thi vào Kho Lưu Trữ An Toàn! Bạn có thể xem lại hoặc Khôi Phục bất cứ lúc nào.', 'success');
}'''

if clear_exam_old in js:
    js = js.replace(clear_exam_old, clear_exam_new, 1)
    print("6b. Updated clearAllLocalExamHistory to safe archiving")

# Replace clearAllTutorHistory with safe archive logic
clear_tutor_old = '''function clearAllTutorHistory() {
  if (confirm('Bạn có chắc muốn xóa toàn bộ lịch sử hội thoại cùng Gia Sư AI trên máy này?')) {
    localStorage.removeItem(LOCAL_TUTOR_CHAT_KEY);
    renderTutorHistoryModal();
    const box = document.getElementById('floating-chat-messages');
    if (box) clearFloatingTutorChat();
    showToast('Đã xóa sạch lịch sử chat AI!', 'success');
  }
}'''

clear_tutor_new = '''function clearAllTutorHistory() {
  const activeList = getLocalTutorHistory();
  if (!activeList.length) {
    showToast('Không có tin nhắn nào trong danh sách đang hiển thị!', 'info');
    return;
  }

  // Safe Archive: NEVER lose user records!
  const archive = getLocalTutorArchive();
  const merged = [...activeList, ...archive];
  saveLocalTutorArchive(merged);
  saveLocalTutorHistory([]);

  // Sync to backend SQLite archive
  activeList.forEach((item) => {
    apiFetch('/api/history/archive', {
      method: 'POST',
      body: JSON.stringify({
        history_type: 'tutor_chat',
        item_id: item.id || `tmsg_${Date.now()}`,
        payload_json: JSON.stringify(item)
      })
    }).catch(() => {});
  });

  renderTutorHistoryModal();
  const box = document.getElementById('floating-chat-messages');
  if (box) clearFloatingTutorChat();
  showToast('🛡️ Đã lưu tin nhắn vào Kho Lưu Trữ An Toàn! Không lo mất đoạn chat.', 'success');
}'''

if clear_tutor_old in js:
    js = js.replace(clear_tutor_old, clear_tutor_new, 1)
    print("6c. Updated clearAllTutorHistory to safe archiving")

# =========================================================================
# 7. Update renderLocalExamHistoryModal and renderTutorHistoryModal
# =========================================================================
render_exam_hist_old = '''function renderLocalExamHistoryModal() {
  const list = getLocalExamHistory();
  const container = document.getElementById('leh-history-list');
  setText('leh-stat-count', list.length);
  const avg = list.length ? (list.reduce((a, b) => a + (b.score || 0), 0) / list.length).toFixed(1) : '0.0';
  setText('leh-stat-avg', avg);
  const totQ = list.reduce((a, b) => a + (b.total_questions || 0), 0);
  setText('leh-stat-total-q', totQ);'''

render_exam_hist_new = '''function renderLocalExamHistoryModal() {
  const activeList = getLocalExamHistory();
  const archiveList = getLocalExamArchive();
  setText('exam-hist-active-count', activeList.length);
  setText('exam-hist-archive-count', archiveList.length);

  const isArchive = currentExamHistorySubTab === 'archive';
  const list = isArchive ? archiveList : activeList;

  const container = document.getElementById('leh-history-list');
  setText('leh-stat-count', list.length);
  const avg = list.length ? (list.reduce((a, b) => a + (b.score || 0), 0) / list.length).toFixed(1) : '0.0';
  setText('leh-stat-avg', avg);
  const totQ = list.reduce((a, b) => a + (b.total_questions || 0), 0);
  setText('leh-stat-total-q', totQ);'''

if render_exam_hist_old in js:
    js = js.replace(render_exam_hist_old, render_exam_hist_new, 1)
    print("7a. Updated renderLocalExamHistoryModal for archive subtabs")

# Also add Restore button next to items in archive mode for exam history
hist_action_target = '''<div class="flex items-center gap-2">
            <button onclick="reviewLocalExamHistoryItem('${item.id}')" class="btn-primary !bg-indigo-600 hover:!bg-indigo-700 px-3.5 py-1.5 text-xs font-bold flex items-center gap-1 shadow-sm">
              <span>🔍</span> <span>Xem Lại & Luyện Lại</span>
            </button>
          </div>'''

hist_action_replacement = '''<div class="flex items-center gap-2">
            ${isArchive ? `
              <button onclick="restoreSingleExamHistory('${item.id}')" class="btn-primary !bg-emerald-600 hover:!bg-emerald-500 px-3.5 py-1.5 text-xs font-black flex items-center gap-1 shadow-sm">
                <span>🔄</span> <span>Khôi Phục</span>
              </button>
            ` : `
              <button onclick="reviewLocalExamHistoryItem('${item.id}')" class="btn-primary !bg-indigo-600 hover:!bg-indigo-700 px-3.5 py-1.5 text-xs font-bold flex items-center gap-1 shadow-sm">
                <span>🔍</span> <span>Xem Lại & Luyện Lại</span>
              </button>
            `}
          </div>'''

if hist_action_target in js:
    js = js.replace(hist_action_target, hist_action_replacement, 1)
    print("7b. Added conditional Khôi Phục button in exam history")

# Enhance renderTutorHistoryModal for archive mode
render_tutor_hist_old = '''function renderTutorHistoryModal(filteredList = null) {
  const list = filteredList !== null ? filteredList : getLocalTutorHistory();
  const container = document.getElementById('tutor-history-messages-list');
  setText('tutor-history-count', `${list.length} tin nhắn`);'''

render_tutor_hist_new = '''function renderTutorHistoryModal(filteredList = null) {
  const activeList = getLocalTutorHistory();
  const archiveList = getLocalTutorArchive();
  setText('tutor-hist-active-count', activeList.length);
  setText('tutor-hist-archive-count', archiveList.length);

  const isArchive = currentTutorHistorySubTab === 'archive';
  const list = filteredList !== null ? filteredList : (isArchive ? archiveList : activeList);
  const container = document.getElementById('tutor-history-messages-list');
  setText('tutor-history-count', `${list.length} tin nhắn`);'''

if render_tutor_hist_old in js:
    js = js.replace(render_tutor_hist_old, render_tutor_hist_new, 1)
    print("7c. Updated renderTutorHistoryModal for archive subtabs")

# =========================================================================
# 8. Extract & Render Key Concept Chips in renderCurrentExamQuestion
# =========================================================================
render_q_target = '''  renderQuestionAnswerArea(q);
  renderQuestionFeedbackArea(q);'''

render_q_chips = '''  // Auto Key Concepts & Term Chips for instant Ask AI
  const keyRow = document.getElementById('q-key-terms-row');
  if (keyRow) {
    const qStr = (q.question_text || '') + ' ' + (q.topic_tag || '');
    const knownTerms = [
      'Cholesterol', 'Triglycerid', 'HDL-C', 'LDL-C', 'Friedewald',
      'GOD-POD', 'Fehling', 'Molish', 'Benedict', 'Biuret', 'Jaffé',
      'Creatinin', 'Acid uric', 'Urê', 'Protein niệu', 'Cybow',
      'Ketone', 'Bilirubin', 'Urobilinogen', 'Cặn lắng', 'Hồng cầu',
      'Bạch cầu', 'Trụ niệu', 'Enzym', 'AST', 'ALT', 'LDH', 'Amylase',
      'Class', 'Inheritance', 'Polymorphism', 'Encapsulation',
      'Virtual', 'Override', 'Interface', 'Static', 'List'
    ];
    const found = knownTerms.filter(t => new RegExp(`\\\\b${t}\\\\b`, 'i').test(qStr));
    if (found.length) {
      keyRow.innerHTML = `<span class="text-[11px] font-bold txt-muted mr-1">🔍 Bấm từ để hỏi AI:</span>` +
        found.slice(0, 5).map(t => `<button type="button" onclick="askAiAboutSelectedTerm('${t}')" class="q-concept-chip"><span>✨</span> ${t} <span class="text-[10px] opacity-75">🤖 Hỏi</span></button>`).join(' ');
      keyRow.classList.remove('hidden');
    } else {
      keyRow.classList.add('hidden');
    }
  }

  // Sync toolbar discussion count
  if (q && q.id) {
    const cachedDisc = STATE.discussionsCache[q.id] || [];
    const tBadge = document.getElementById('q-toolbar-disc-count');
    if (tBadge) tBadge.textContent = cachedDisc.length;
  }

  renderQuestionAnswerArea(q);
  renderQuestionFeedbackArea(q);'''

if render_q_target in js:
    js = js.replace(render_q_target, render_q_chips, 1)
    print("8. Added key concept chips and toolbar disc count sync in renderCurrentExamQuestion")

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(js)

print("Done writing updates to static/app.js!")
