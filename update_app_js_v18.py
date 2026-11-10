# update_app_js_v18.py
import re

print("Reading static/app.js...")
with open('static/app.js', 'r', encoding='utf-8') as f:
    code = f.read()

# -------------------------------------------------------------------------
# A. DECOUPLED loadSubjectsAndStats() WITH CACHING
# -------------------------------------------------------------------------
old_load_fn = """async function loadSubjectsAndStats() {
  try {
    const [subRes, statRes] = await Promise.all([apiFetch('/api/subjects'), apiFetch('/api/stats')]);
    if (subRes.success) STATE.subjects = subRes.subjects || [];
    if (statRes.success) STATE.stats = statRes.stats || {};

    populateAllSubjectSelects();
    initActiveSubjectBar();
    await fetchCurrentUserProfile();
    renderDashboard();
    await onExamSubjectChange();
  } catch (err) {
    showToast('Lỗi tải dữ liệu: ' + err.message, 'error');
  }
}"""

new_load_fn = """async function loadSubjectsAndStats() {
  // 1. Instant cache hydration: Screen NEVER displays 0 subjects even on slow initial load!
  try {
    const cached = localStorage.getItem('unimaster_cached_subjects');
    if (cached) {
      const parsed = JSON.parse(cached);
      if (Array.isArray(parsed) && parsed.length > 0 && (!STATE.subjects || !STATE.subjects.length)) {
        STATE.subjects = parsed;
        populateAllSubjectSelects();
        initActiveSubjectBar();
        renderDashboard();
      }
    }
  } catch (_) {}

  // 2. Fetch fresh subjects first & render UI immediately
  try {
    const subRes = await apiFetch('/api/subjects');
    if (subRes && subRes.success && Array.isArray(subRes.subjects)) {
      STATE.subjects = subRes.subjects;
      try {
        localStorage.setItem('unimaster_cached_subjects', JSON.stringify(subRes.subjects));
      } catch (_) {}
      populateAllSubjectSelects();
      initActiveSubjectBar();
      renderDashboard();
      await onExamSubjectChange();
    }
  } catch (err) {
    console.warn('Cannot fetch fresh subjects:', err);
  }

  // 3. Fetch stats independently: Slow or failed stats NEVER blocks subjects!
  try {
    const statRes = await apiFetch('/api/stats');
    if (statRes && statRes.success && statRes.stats) {
      STATE.stats = statRes.stats;
      renderDashboard();
    }
  } catch (err) {
    console.warn('Cannot fetch stats:', err);
  }

  // 4. Hydrate profile
  try {
    await fetchCurrentUserProfile();
  } catch (_) {}
}"""

if old_load_fn in code:
    code = code.replace(old_load_fn, new_load_fn)
    print("Replaced loadSubjectsAndStats with decoupled resilient version!")
else:
    print("WARNING: old_load_fn exact text not found, trying regex...")
    pattern = r"async function loadSubjectsAndStats\(\)\s*\{[\s\S]*?renderDashboard\(\);[\s\S]*?\}"
    code = re.sub(pattern, new_load_fn, code, count=1)
    print("Replaced loadSubjectsAndStats via regex!")

# -------------------------------------------------------------------------
# B. DEFENSIVE GUARDS IN renderCurrentExamQuestion
# -------------------------------------------------------------------------
target_render_q = "function renderCurrentExamQuestion() {"
new_render_q_header = """function renderCurrentExamQuestion() {
  try {
    if (!STATE.exam || !Array.isArray(STATE.exam.questions) || !STATE.exam.questions.length) return;
    const q = STATE.exam.questions[STATE.exam.currentIndex];
    if (!q) return;

    // Bulletproof defensive checks: bookmarks, mistakes, notes always safe arrays/objects!
    if (!Array.isArray(STATE.bookmarks)) STATE.bookmarks = [];
    if (!Array.isArray(STATE.mistakes)) STATE.mistakes = [];
    if (!STATE.notes || typeof STATE.notes !== 'object') STATE.notes = {};"""

if target_render_q in code and "Bulletproof defensive checks" not in code:
    code = code.replace(
        """function renderCurrentExamQuestion() {
  const q = STATE.exam.questions[STATE.exam.currentIndex];
  if (!q) return;""",
        new_render_q_header
    )
    print("Added defensive guards to renderCurrentExamQuestion!")

# -------------------------------------------------------------------------
# C. PERSISTENT LOCAL EXAM HISTORY & CUSTOM RANGE & CTUMP 322 FUNCTIONS
# -------------------------------------------------------------------------
helper_functions_v18 = """
// =========================================================================
// UNIMASTER v18: CUSTOM RANGE EXAM, CTUMP 322 PARTS & PERSISTENT HISTORY
// =========================================================================

// --- 1. CUSTOM RANGE EXAM (Từ câu ... đến câu ...) ---
function setRangePreset(from, to) {
  const fromEl = document.getElementById('exam-range-from');
  const toEl = document.getElementById('exam-range-to');
  const total = STATE.examConfig.subjectAllQuestions?.length || 200;
  if (fromEl) fromEl.value = Math.max(1, from);
  if (toEl) toEl.value = to >= 9999 ? total : Math.min(total, to);
  updateRangePreview();
  playSound('click');
}

function updateRangePreview() {
  const fromEl = document.getElementById('exam-range-from');
  const toEl = document.getElementById('exam-range-to');
  const badge = document.getElementById('range-preview-badge');
  const from = parseInt(fromEl?.value || '1', 10);
  const to = parseInt(toEl?.value || '50', 10);
  const count = Math.max(0, to - from + 1);
  if (badge) badge.textContent = `${count} câu`;
}

async function startCustomRangeExam() {
  const sel = document.getElementById('exam-subject-select');
  const sid = Number(sel?.value || STATE.examConfig.subjectId);
  let pool = STATE.examConfig.subjectAllQuestions;
  if (!pool || !pool.length || sid !== STATE.examConfig.subjectId) {
    const res = await apiFetch(`/api/subjects/${sid}/questions?type=all`);
    pool = res.questions || [];
    STATE.examConfig.subjectAllQuestions = pool;
    STATE.examConfig.subjectId = sid;
  }

  const fromVal = Math.max(1, parseInt(document.getElementById('exam-range-from')?.value || '1', 10));
  const toVal = Math.max(fromVal, parseInt(document.getElementById('exam-range-to')?.value || String(pool.length || 50), 10));
  
  const fromIdx = fromVal - 1;
  const toIdx = Math.min(pool.length, toVal);
  const sliced = pool.slice(fromIdx, toIdx);

  if (!sliced.length) {
    showToast(`Dải câu hỏi từ ${fromVal} đến ${toVal} không có câu hỏi nào!`, 'warning');
    return;
  }

  const sub = STATE.subjects.find((s) => s.id === sid);
  const title = `${sub ? sub.name : 'Môn học'}: Câu ${fromVal} – ${toVal} (${sliced.length} câu)`;
  const shuffle = document.getElementById('exam-random-toggle')?.checked ?? false;
  let finalQuestions = [...sliced];
  if (shuffle) finalQuestions.sort(() => Math.random() - 0.5);

  launchExamWithQuestions(finalQuestions, title, !shuffle);
  showToast(`🎯 Đã nạp thành công dải câu ${fromVal} – ${toVal} (${sliced.length} câu)!`, 'success');
}

// --- 2. 322 CÂU HÓA SINH CTUMP GỐC (5 PHẦN CHUYÊN BIỆT) ---
function openCtumpOriginalPartsModal() {
  const modal = document.getElementById('modal-ctump-original-parts');
  if (modal) {
    modal.classList.remove('hidden');
    if (window.lucide) window.lucide.createIcons();
  }
}

async function startCtumpOriginalPart(partNum) {
  const hs = STATE.subjects.find((s) => s.code === 'HOASINH_CTUMP') || STATE.subjects[0];
  if (!hs) return;
  const sel = document.getElementById('exam-subject-select');
  if (sel) sel.value = String(hs.id);
  STATE.examConfig.subjectId = hs.id;
  switchTab('exam');

  let pool = STATE.examConfig.subjectAllQuestions;
  if (!pool || !pool.length || STATE.examConfig.subjectId !== hs.id) {
    const res = await apiFetch(`/api/subjects/${hs.id}/questions?type=all`);
    pool = res.questions || [];
    STATE.examConfig.subjectAllQuestions = pool;
  }

  // Filter out the 200-question packs (Bài 2, Bài 3, Bài 4) to isolate original 275/312 questions
  const coreQuestions = pool.filter((q) => {
    const tag = q.topic_tag || '';
    return !tag.startsWith('Bài 2') && !tag.startsWith('Bài 3') && !tag.startsWith('Bài 4');
  });

  let selected = [];
  let partTitle = '';

  if (partNum === 0) {
    selected = coreQuestions;
    partTitle = `CTUMP Gốc: Toàn Bộ 322 Câu (${selected.length} câu)`;
  } else if (partNum === 1) {
    selected = coreQuestions.filter((q, idx) => {
      const m = String(q.question_text || '').match(/^Câu\\s+(\\d+)/);
      const n = m ? parseInt(m[1], 10) : idx + 1;
      return n <= 27 || (q.topic_tag && q.topic_tag.includes('An toàn'));
    });
    partTitle = `CTUMP Phần 1: An Toàn PTN & Đo Quang Beer-Lambert (${selected.length} câu)`;
  } else if (partNum === 2) {
    selected = coreQuestions.filter((q, idx) => {
      const m = String(q.question_text || '').match(/^Câu\\s+(\\d+)/);
      const n = m ? parseInt(m[1], 10) : idx + 1;
      return (n >= 28 && n <= 56) || (q.topic_tag && q.topic_tag.includes('Protein') && !q.topic_tag.includes('Thận'));
    });
    partTitle = `CTUMP Phần 2: Bệnh Phẩm & Định Lượng Protein / Biuret (${selected.length} câu)`;
  } else if (partNum === 3) {
    selected = coreQuestions.filter((q, idx) => {
      const m = String(q.question_text || '').match(/^Câu\\s+(\\d+)/);
      const n = m ? parseInt(m[1], 10) : idx + 1;
      return (n >= 57 && n <= 130) || (q.topic_tag && q.topic_tag.includes('Thận'));
    });
    partTitle = `CTUMP Phần 3: Chức Năng Thận (Ure, Creatinin, Acid Uric) (${selected.length} câu)`;
  } else if (partNum === 4) {
    selected = coreQuestions.filter((q, idx) => {
      const m = String(q.question_text || '').match(/^Câu\\s+(\\d+)/);
      const n = m ? parseInt(m[1], 10) : idx + 1;
      return (n >= 131 && n <= 220) || (q.topic_tag && (q.topic_tag.includes('Enzym') || q.topic_tag.includes('Lipid')));
    });
    partTitle = `CTUMP Phần 4: Enzym Học & Bilang Lipid Máu (${selected.length} câu)`;
  } else if (partNum === 5) {
    selected = coreQuestions.filter((q, idx) => {
      const m = String(q.question_text || '').match(/^Câu\\s+(\\d+)/);
      const n = m ? parseInt(m[1], 10) : idx + 1;
      return n >= 221 || (q.topic_tag && (q.topic_tag.includes('Nước tiểu') || q.topic_tag.includes('Cặn lắng') || q.image_url));
    });
    partTitle = `CTUMP Phần 5: Nước Tiểu 10 Thông Số & Soi Cặn Lắng (${selected.length} câu)`;
  }

  if (!selected.length) selected = coreQuestions.slice(0, 35);

  launchExamWithQuestions(selected, partTitle, true);
  showToast(`🏛️ Đã nạp ${selected.length} câu thuộc ${partTitle}!`, 'success');
}

// --- 3. PERSISTENT LOCAL EXAM HISTORY ON USER MACHINE ---
const LOCAL_EXAM_HISTORY_KEY = 'unimaster_local_exam_history_v2';

function getLocalExamHistory() {
  try {
    return JSON.parse(localStorage.getItem(LOCAL_EXAM_HISTORY_KEY) || '[]');
  } catch (_) {
    return [];
  }
}

function saveLocalExamAttemptRecord(res) {
  try {
    const history = getLocalExamHistory();
    const sub = STATE.subjects.find((s) => s.id === STATE.exam.subjectId);
    const wrongList = (res.details || []).filter((d) => !d.is_correct);
    const record = {
      id: 'exam_' + Date.now(),
      timestamp: new Date().toISOString(),
      displayDate: new Date().toLocaleString('vi-VN', { hour: '2-digit', minute: '2-digit', day: '2-digit', month: '2-digit', year: 'numeric' }),
      subject_id: STATE.exam.subjectId,
      subject_name: sub ? sub.name : 'Môn học',
      exam_title: STATE.exam.subjectName || (sub ? sub.name : 'Bài thi'),
      mode: STATE.exam.mode || 'practice',
      score: Number(res.score || 0),
      correct_count: Number(res.correct_count || 0),
      total_questions: Number(res.total_questions || 0),
      elapsed_seconds: Number(STATE.exam.elapsedSeconds || 0),
      wrong_count: wrongList.length,
      wrong_questions: wrongList.map((d) => ({
        id: d.question_id,
        question_text: d.question_text,
        user_answer: d.user_answer,
        correct_option: d.correct_option,
        explanation: d.explanation,
        topic_tag: d.topic_tag,
        difficulty: d.difficulty,
        q_type: d.q_type || 'mcq',
        image_url: d.image_url || '',
        code_snippet: d.code_snippet || ''
      })),
      all_details: res.details || []
    };

    history.unshift(record);
    if (history.length > 50) history.pop();
    localStorage.setItem(LOCAL_EXAM_HISTORY_KEY, JSON.stringify(history));
  } catch (err) {
    console.warn('Cannot persist local exam attempt:', err);
  }
}

function openLocalExamHistoryModal() {
  const modal = document.getElementById('modal-exam-history');
  if (modal) {
    renderLocalExamHistoryModal();
    modal.classList.remove('hidden');
    if (window.lucide) window.lucide.createIcons();
  }
}

function renderLocalExamHistoryModal() {
  const list = getLocalExamHistory();
  const container = document.getElementById('leh-history-list');
  setText('leh-stat-count', list.length);
  const avg = list.length ? (list.reduce((a, b) => a + (b.score || 0), 0) / list.length).toFixed(1) : '0.0';
  setText('leh-stat-avg', avg);
  const totQ = list.reduce((a, b) => a + (b.total_questions || 0), 0);
  setText('leh-stat-total-q', totQ);

  if (!container) return;
  if (!list.length) {
    container.innerHTML = `
      <div class="text-center py-12 space-y-3">
        <span class="text-4xl">📂</span>
        <div class="font-extrabold text-sm txt-main">Chưa Có Lịch Sử Làm Bài Nào Được Lưu Trên Máy</div>
        <p class="text-xs txt-muted max-w-sm mx-auto">Mỗi khi bạn nộp bài thi hoặc hoàn thành luyện tập, kết quả sẽ tự động lưu lại ở đây để bạn xem lại và làm lại các câu sai!</p>
        <button onclick="closeModal('modal-exam-history'); switchTab('exam');" class="btn-primary px-4 py-2 text-xs font-bold">🚀 Vào Làm Bài Ngay</button>
      </div>
    `;
    return;
  }

  container.innerHTML = list.map((item) => {
    const isPass = item.score >= 5;
    const scoreColor = item.score >= 8 ? 'text-emerald-400' : isPass ? 'text-amber-400' : 'text-rose-400';
    const modeBadge = {
      practice: '<span class="badge-brand text-[10px] px-2 py-0.5 rounded font-bold">⚡ Luyện tập</span>',
      real: '<span class="badge-amber text-[10px] px-2 py-0.5 rounded font-bold">📝 Thi thật</span>',
      blitz: '<span class="badge-rose text-[10px] px-2 py-0.5 rounded font-bold">🔥 Blitz</span>',
      study: '<span class="badge-cyan text-[10px] px-2 py-0.5 rounded font-bold">📖 Xem giải</span>'
    }[item.mode] || '';

    return `
      <div class="p-4 rounded-2xl border transition-all hover:border-emerald-500/40 space-y-3" style="background-color: var(--bg-surface); border-color: var(--border);">
        <div class="flex flex-wrap items-center justify-between gap-2">
          <div class="flex items-center gap-2">
            ${modeBadge}
            <span class="text-xs font-black txt-main">${escapeHtml(item.exam_title)}</span>
          </div>
          <div class="flex items-center gap-2 text-xs font-mono txt-muted">
            <span>⏱️ ${formatDuration(item.elapsed_seconds)}</span>
            <span>•</span>
            <span>📅 ${escapeHtml(item.displayDate)}</span>
          </div>
        </div>

        <div class="flex flex-wrap items-center justify-between gap-3 pt-1 border-t" style="border-color: var(--border);">
          <div class="flex items-center gap-4 text-xs font-bold">
            <span class="text-base font-black ${scoreColor}">${item.score.toFixed(1)} / 10đ</span>
            <span class="txt-emerald">✔ Đúng: ${item.correct_count} / ${item.total_questions}</span>
            <span class="${item.wrong_count > 0 ? 'text-rose-400' : 'txt-muted'}">✖ Sai: ${item.wrong_count}</span>
          </div>

          <div class="flex items-center gap-1.5">
            ${item.wrong_count > 0 ? `
              <button type="button" onclick="retryWrongFromLocalExam('${item.id}')" class="btn-primary !bg-rose-600 hover:!bg-rose-700 px-3 py-1.5 text-xs font-black flex items-center gap-1 shadow-sm">
                <span>🔄</span> Làm Lại ${item.wrong_count} Câu Sai
              </button>
            ` : ''}
            <button type="button" onclick="reviewLocalExamAttempt('${item.id}')" class="btn-soft px-3 py-1.5 text-xs font-bold">
              👁️ Xem Lại
            </button>
            <button type="button" onclick="deleteLocalExamAttempt('${item.id}')" class="btn-soft p-1.5 text-xs text-rose-400 hover:text-rose-300" title="Xóa lần thi này">
              🗑️
            </button>
          </div>
        </div>
      </div>
    `;
  }).join('');
}

function retryWrongFromLocalExam(recordId) {
  const history = getLocalExamHistory();
  const attempt = history.find((h) => h.id === recordId);
  if (!attempt || !attempt.wrong_questions || !attempt.wrong_questions.length) {
    showToast('Lần thi này không có câu sai nào để làm lại!', 'info');
    return;
  }
  closeModal('modal-exam-history');
  switchTab('exam');
  launchExamWithQuestions(attempt.wrong_questions, `Luyện Lại Câu Sai: ${attempt.exam_title} (${attempt.wrong_questions.length} câu)`, true);
  showToast(`🎯 Đang làm lại ${attempt.wrong_questions.length} câu sai!`, 'success');
}

function reviewLocalExamAttempt(recordId) {
  const history = getLocalExamHistory();
  const attempt = history.find((h) => h.id === recordId);
  if (!attempt) return;
  closeModal('modal-exam-history');
  switchTab('exam');
  
  // Render into exam result screen for review
  STATE.exam.lastResult = {
    score: attempt.score,
    correct_count: attempt.correct_count,
    total_questions: attempt.total_questions,
    details: attempt.all_details
  };
  renderExamResultScreen(STATE.exam.lastResult);
}

function deleteLocalExamAttempt(recordId) {
  let history = getLocalExamHistory();
  history = history.filter((h) => h.id !== recordId);
  localStorage.setItem(LOCAL_EXAM_HISTORY_KEY, JSON.stringify(history));
  renderLocalExamHistoryModal();
  showToast('Đã xóa lần thi khỏi lịch sử máy.', 'info');
}

function clearAllLocalExamHistory() {
  if (confirm('Bạn có chắc muốn xóa toàn bộ lịch sử các lần làm bài trên máy này?')) {
    localStorage.removeItem(LOCAL_EXAM_HISTORY_KEY);
    renderLocalExamHistoryModal();
    showToast('Đã dọn sạch toàn bộ lịch sử làm bài!', 'success');
  }
}

// --- 4. PERSISTENT LOCAL AI CHAT HISTORY ON USER MACHINE ---
const LOCAL_TUTOR_CHAT_KEY = 'unimaster_tutor_chat_history_v2';

function getLocalTutorHistory() {
  try {
    return JSON.parse(localStorage.getItem(LOCAL_TUTOR_CHAT_KEY) || '[]');
  } catch (_) {
    return [];
  }
}

function saveLocalTutorMessage(role, content, contextName = '') {
  try {
    const list = getLocalTutorHistory();
    list.push({
      id: 'tmsg_' + Date.now() + '_' + Math.random().toString(36).substr(2, 4),
      role,
      content,
      context: contextName,
      timestamp: new Date().toISOString(),
      displayTime: new Date().toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' })
    });
    if (list.length > 200) list.shift();
    localStorage.setItem(LOCAL_TUTOR_CHAT_KEY, JSON.stringify(list));
  } catch (err) {
    console.warn('Cannot save tutor message:', err);
  }
}

function initTutorHistoryFromStorage() {
  try {
    const history = getLocalTutorHistory();
    const box = document.getElementById('floating-chat-messages');
    if (!box || !history.length) return;
    
    // Clear initial greeting and render last 10 messages from history
    box.innerHTML = '';
    const recent = history.slice(-10);
    recent.forEach((msg) => {
      if (msg.role === 'user') {
        box.innerHTML += `
          <div class="flex items-start justify-end gap-2 animate-fade-in">
            <div class="p-2.5 rounded-xl badge-brand max-w-[85%] font-semibold text-xs">
              ${escapeHtml(msg.content)}
            </div>
            <div class="w-6 h-6 rounded-md flex items-center justify-center bg-violet-600 text-white text-xs shrink-0">👤</div>
          </div>
        `;
      } else {
        const msgId = msg.id;
        window._tutorReplies[msgId] = msg.content;
        box.innerHTML += `
          <div class="flex items-start gap-2 animate-fade-in" id="${msgId}">
            <div class="w-6 h-6 rounded-md flex items-center justify-center bg-indigo-500/20 text-indigo-400 text-xs shrink-0 mt-0.5">🤖</div>
            <div class="p-3 rounded-xl bg-white/5 border border-white/5 txt-sub max-w-[90%] space-y-2">
              <div class="flex items-center justify-between gap-1 text-[10px] font-mono txt-muted border-b pb-1 border-white/5">
                <span class="text-indigo-400 font-extrabold flex items-center gap-1">
                  <span>🎓</span> ${escapeHtml(msg.context || 'Gia Sư AI')}
                </span>
                <span class="text-[10px] opacity-70">${msg.displayTime || ''}</span>
              </div>
              <div class="leading-relaxed ai-tutor-content">
                ${renderAcademicText(msg.content)}
              </div>
            </div>
          </div>
        `;
      }
    });
    box.scrollTop = box.scrollHeight;
    renderAllMathOnPage(box);
  } catch (err) {
    console.warn('Cannot hydrate tutor chat history:', err);
  }
}

function openTutorHistoryModal() {
  const modal = document.getElementById('modal-tutor-chat-history');
  if (modal) {
    renderTutorHistoryModal();
    modal.classList.remove('hidden');
    if (window.lucide) window.lucide.createIcons();
  }
}

function renderTutorHistoryModal(filteredList = null) {
  const list = filteredList !== null ? filteredList : getLocalTutorHistory();
  const container = document.getElementById('tutor-history-messages-list');
  setText('tutor-history-count', `${list.length} tin nhắn`);

  if (!container) return;
  if (!list.length) {
    container.innerHTML = `
      <div class="text-center py-12 space-y-3">
        <span class="text-4xl">💬</span>
        <div class="font-extrabold text-sm txt-main">Chưa Có Tin Nhắn Nào Trong Lịch Sử</div>
        <p class="text-xs txt-muted max-w-sm mx-auto">Mọi câu hỏi và giải đáp giữa bạn và Gia Sư AI sẽ được lưu trữ tự động trên thiết bị này.</p>
      </div>
    `;
    return;
  }

  container.innerHTML = list.map((msg) => {
    const isUser = msg.role === 'user';
    return `
      <div class="p-3.5 rounded-2xl border transition-all space-y-2" style="background-color: var(--bg-surface); border-color: var(--border);">
        <div class="flex items-center justify-between text-xs font-bold border-b pb-1.5" style="border-color: var(--border);">
          <span class="flex items-center gap-1.5 ${isUser ? 'text-purple-400' : 'text-indigo-400'}">
            <span>${isUser ? '👤 Bạn đã hỏi' : '🤖 Gia sư AI giải đáp'}</span>
            ${msg.context ? `<span class="badge-subtle text-[10px] px-1.5 py-0.2 rounded font-normal font-sans">${escapeHtml(msg.context)}</span>` : ''}
          </span>
          <span class="text-[10px] font-mono txt-muted">${msg.displayTime || ''}</span>
        </div>
        <div class="text-xs leading-relaxed ${isUser ? 'txt-main font-semibold' : 'ai-tutor-content'}">
          ${isUser ? escapeHtml(msg.content) : renderAcademicText(msg.content)}
        </div>
      </div>
    `;
  }).join('');
  renderAllMathOnPage(container);
}

function filterTutorHistory(keyword) {
  const q = String(keyword || '').toLowerCase().trim();
  const all = getLocalTutorHistory();
  if (!q) {
    renderTutorHistoryModal(all);
    return;
  }
  const filtered = all.filter((m) => (m.content || '').toLowerCase().includes(q) || (m.context || '').toLowerCase().includes(q));
  renderTutorHistoryModal(filtered);
}

function clearAllTutorHistory() {
  if (confirm('Bạn có chắc muốn xóa toàn bộ lịch sử hội thoại cùng Gia Sư AI trên máy này?')) {
    localStorage.removeItem(LOCAL_TUTOR_CHAT_KEY);
    renderTutorHistoryModal();
    const box = document.getElementById('floating-chat-messages');
    if (box) clearFloatingTutorChat();
    showToast('Đã xóa sạch lịch sử chat AI!', 'success');
  }
}

function exportTutorHistory() {
  const list = getLocalTutorHistory();
  if (!list.length) {
    showToast('Chưa có tin nhắn nào để xuất!', 'info');
    return;
  }
  let txt = '=== SỔ TAY GIA SƯ AI - UNIMASTER ===\\n\\n';
  list.forEach((m) => {
    txt += `[${m.displayTime || ''}] ${m.role === 'user' ? 'BẠN' : 'GIA SƯ AI'} (${m.context || 'Chung'}):\\n${m.content}\\n\\n-------------------\\n\\n`;
  });
  const blob = new Blob([txt], { type: 'text/plain;charset=utf-8' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = `UniMaster_GiaSuAI_${new Date().toISOString().slice(0, 10)}.txt`;
  a.click();
  showToast('📄 Đã tải xuống sổ tay ghi chép AI!', 'success');
}
"""

if "UNIMASTER v18: CUSTOM RANGE EXAM" not in code:
    code += "\n\n" + helper_functions_v18
    print("Appended v18 helper functions to static/app.js!")

# -------------------------------------------------------------------------
# D. WIRE saveLocalExamAttemptRecord in renderExamResultScreen
# -------------------------------------------------------------------------
if "saveLocalExamAttemptRecord(res)" not in code:
    target_result = "function renderExamResultScreen(res) {"
    if target_result in code:
        code = code.replace(
            target_result,
            target_result + "\n  saveLocalExamAttemptRecord(res);"
        )
        print("Wired saveLocalExamAttemptRecord to renderExamResultScreen!")

# -------------------------------------------------------------------------
# E. WIRE saveLocalTutorMessage in sendFloatingTutorMessage
# -------------------------------------------------------------------------
if "saveLocalTutorMessage('user'" not in code:
    target_user_push = "floatingTutorChatHistory.push({ role: 'user', content: fullPromptForAi });"
    if target_user_push in code:
        code = code.replace(
            target_user_push,
            target_user_push + "\n  saveLocalTutorMessage('user', userMsg, subName);"
        )
        print("Wired user message saving to localStorage!")

if "saveLocalTutorMessage('model'" not in code:
    target_model_push = "floatingTutorChatHistory.push({ role: 'model', content: reply });"
    if target_model_push in code:
        code = code.replace(
            target_model_push,
            target_model_push + "\n    saveLocalTutorMessage('model', reply, subName);"
        )
        print("Wired model reply saving to localStorage!")

# -------------------------------------------------------------------------
# F. HYDRATE TUTOR HISTORY ON DOMContentLoaded
# -------------------------------------------------------------------------
if "initTutorHistoryFromStorage();" not in code:
    target_init_greeting = "initTutorGreeting();"
    if target_init_greeting in code:
        code = code.replace(
            target_init_greeting,
            target_init_greeting + "\n  initTutorHistoryFromStorage();"
        )
        print("Wired initTutorHistoryFromStorage to DOMContentLoaded!")

with open('static/app.js', 'w', encoding='utf-8') as f:
    f.write(code)
print("static/app.js updated successfully!")
