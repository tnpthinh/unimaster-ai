import os
import re

BASE_DIR = r"C:\Users\PC\.gemini\antigravity\scratch\unimaster-ai"
os.chdir(BASE_DIR)

with open("static/app.js", "r", encoding="utf-8") as f:
    code = f.read()

# =========================================================================
# 1. NEW COMPREHENSIVE FLOATING AI TUTOR SUITE
# =========================================================================
new_tutor_code = '''// =========================================================================
// FEATURE 3: FLOATING AI TUTOR WIDGET (CONTEXT-AWARE, MULTI-PERSONA, VOICE, 1-TOUCH)
// =========================================================================
let floatingTutorChatHistory = [];
let windowTutorSizeExpanded = false;
let currentTutorPersona = localStorage.getItem('unimaster_tutor_persona') || 'professor';
let pinnedTutorQuestion = null;
let floatingVoiceRecognition = null;
let isFloatingVoiceListening = false;
window._tutorReplies = window._tutorReplies || {};

function toggleFloatingTutor() {
  const win = document.getElementById('floating-tutor-window');
  if (!win) return;
  const isHidden = win.classList.contains('hidden');
  if (isHidden) {
    win.classList.remove('hidden');
    playSound('click');
    syncFloatingTutorSubjectContext();
    renderFloatingActionChips();
    updateTutorPersonaUI();
    const input = document.getElementById('floating-chat-input');
    if (input) setTimeout(() => input.focus(), 100);
  } else {
    win.classList.add('hidden');
    stopFloatingVoiceInput();
  }
}

function toggleFloatingTutorSize() {
  const win = document.getElementById('floating-tutor-window');
  const btn = document.getElementById('btn-ft-expand');
  if (!win) return;
  windowTutorSizeExpanded = !windowTutorSizeExpanded;
  win.classList.toggle('expanded', windowTutorSizeExpanded);
  if (btn) btn.textContent = windowTutorSizeExpanded ? '🗗' : '⛶';
  playSound('click');
}

function syncFloatingTutorSubjectContext() {
  const currentSub = STATE.subjects.find((s) => String(s.id) === String(STATE.activeSubjectId));
  const subName = currentSub ? currentSub.name : 'Tổng hợp Đại học';
  setText('floating-tutor-context', pinnedTutorQuestion ? `📌 Đang hỏi: ${pinnedTutorQuestion.shortTitle}` : `Đang hỗ trợ: ${subName}`);
  setText('floating-welcome-subj', subName);
  const qBadge = document.getElementById('floating-btn-q-badge');
  if (qBadge) {
    if (pinnedTutorQuestion) {
      qBadge.textContent = pinnedTutorQuestion.shortTitle;
      qBadge.classList.remove('hidden');
    } else {
      qBadge.classList.add('hidden');
    }
  }
}

function setFloatingPersona(persona) {
  currentTutorPersona = persona;
  localStorage.setItem('unimaster_tutor_persona', persona);
  updateTutorPersonaUI();
  playSound('click');
  const personaNames = {
    professor: 'Giáo Sư Chuẩn Mực',
    feynman: 'Richard Feynman (Dễ Hiểu)',
    speed: 'Giải Nhanh 10 Giây',
    examiner: 'Giảng Viên Vấn Đáp'
  };
  showToast(`Đã chuyển phong cách: ${personaNames[persona] || persona}`, 'info');
}

function updateTutorPersonaUI() {
  ['professor', 'feynman', 'speed', 'examiner'].forEach((p) => {
    const el = document.getElementById(`ft-persona-${p}`);
    if (el) {
      el.classList.toggle('active', p === currentTutorPersona);
    }
  });
}

function pinQuestionToTutor(q, meta = {}) {
  if (!q) return;
  const parsed = parseQuestionHeader(q.question_text || '');
  const rawTitle = parsed.body || q.question_text || 'Câu hỏi';
  const cleanTitle = rawTitle.replace(/<[^>]+>/g, '').trim();
  const shortTitle = meta.label || (parsed.bankNum ? `Câu #${parsed.bankNum}` : `Câu hỏi`);

  pinnedTutorQuestion = {
    id: q.id,
    shortTitle: shortTitle,
    fullTitle: cleanTitle,
    topic: parsed.topic || q.topic_tag || '',
    code_snippet: q.code_snippet || '',
    option_a: q.option_a || '',
    option_b: q.option_b || '',
    option_c: q.option_c || '',
    option_d: q.option_d || '',
    correct_option: q._effectiveCorrect || q.correct_option || '',
    explanation: q.explanation || '',
    user_answer: meta.user_answer || '',
    is_correct: meta.is_correct
  };

  const container = document.getElementById('ft-pinned-question-container');
  if (container) {
    container.classList.remove('hidden');
    setText('ft-pinned-q-title', `📌 ${shortTitle} • ${pinnedTutorQuestion.topic || 'Kiến thức cốt lõi'}`);
    setText('ft-pinned-q-body', cleanTitle.substring(0, 110) + (cleanTitle.length > 110 ? '...' : ''));
  }

  syncFloatingTutorSubjectContext();
  renderFloatingActionChips();

  const win = document.getElementById('floating-tutor-window');
  if (win && win.classList.contains('hidden')) {
    toggleFloatingTutor();
  }

  const box = document.getElementById('floating-chat-messages');
  if (box) {
    box.innerHTML += `
      <div class="flex items-start gap-2 animate-fade-in">
        <div class="w-6 h-6 rounded-md flex items-center justify-center bg-indigo-500/20 text-indigo-400 text-xs shrink-0">📌</div>
        <div class="p-2.5 rounded-xl border border-indigo-500/30 text-xs txt-sub max-w-[90%]" style="background: rgba(99, 102, 241, 0.08);">
          <div class="font-extrabold text-indigo-300">Đã nạp ${shortTitle}:</div>
          <div class="italic py-0.5 line-clamp-2">"${escapeHtml(cleanTitle.substring(0, 130))}..."</div>
          <div class="text-[11px] txt-muted pt-1">Bấm 1 trong 4 chip bên trên để AI phân tích ngay tức thì!</div>
        </div>
      </div>
    `;
    box.scrollTop = box.scrollHeight;
  }
}

function unpinTutorQuestion() {
  pinnedTutorQuestion = null;
  const container = document.getElementById('ft-pinned-question-container');
  if (container) container.classList.add('hidden');
  syncFloatingTutorSubjectContext();
  renderFloatingActionChips();
  showToast('Đã chuyển về chế độ hỏi đáp môn học chung.', 'info');
}

function renderFloatingActionChips() {
  const container = document.getElementById('ft-action-chips');
  if (!container) return;

  if (pinnedTutorQuestion) {
    container.innerHTML = `
      <button type="button" onclick="sendFloatingPrompt('Tại sao đáp án này đúng? Hãy giải thích chi tiết bản chất và phương pháp suy luận.')"
        class="badge-brand px-2.5 py-1 rounded-md text-[11px] font-bold shrink-0 shadow-sm hover:scale-105 transition-all">
        🔍 Tại sao đúng?
      </button>
      <button type="button" onclick="sendFloatingPrompt('Chỉ ra các bẫy đề thi và phân tích tại sao các đáp án còn lại là sai?')"
        class="badge-soft px-2.5 py-1 rounded-md text-[11px] font-bold shrink-0 hover:text-white">
        ⚠️ Bẫy đề & Đáp án sai
      </button>
      <button type="button" onclick="sendFloatingPrompt('Cho tôi mẹo nhớ nhanh 5 giây hoặc quy tắc vàng để không bao giờ quên câu này!')"
        class="badge-soft px-2.5 py-1 rounded-md text-[11px] font-bold shrink-0 hover:text-white">
        💡 Mẹo nhớ 5s
      </button>
      <button type="button" onclick="sendFloatingPrompt('Hướng dẫn từng bước cách giải chi tiết và dạng bài tương tự có thể ra thi!')"
        class="badge-soft px-2.5 py-1 rounded-md text-[11px] font-bold shrink-0 hover:text-white">
        📐 Hướng dẫn từng bước
      </button>
    `;
  } else {
    container.innerHTML = `
      <button type="button" onclick="sendFloatingPrompt('Tóm tắt 3 ý quan trọng nhất môn này để ôn thi cấp tốc!')"
        class="badge-soft px-2.5 py-1 rounded-md text-[11px] font-bold shrink-0 hover:text-white">
        ✨ 3 Ý Cốt Lõi
      </button>
      <button type="button" onclick="sendFloatingPrompt('Cho tôi 1 câu hỏi trắc nghiệm thử thách môn này kèm đáp án và phân tích!')"
        class="badge-soft px-2.5 py-1 rounded-md text-[11px] font-bold shrink-0 hover:text-white">
        💡 Đố 1 Câu Nhanh
      </button>
      <button type="button" onclick="sendFloatingPrompt('Những bẫy thi và lỗi sai sinh viên hay gặp nhất ở môn này?')"
        class="badge-soft px-2.5 py-1 rounded-md text-[11px] font-bold shrink-0 hover:text-white">
        ⚠️ Bẫy Đề Thi
      </button>
      <button type="button" onclick="sendFloatingPrompt('Lập kế hoạch ôn tập nước rút 3 ngày cho môn này!')"
        class="badge-soft px-2.5 py-1 rounded-md text-[11px] font-bold shrink-0 hover:text-white">
        🗺️ Kế Hoạch Nước Rút
      </button>
    `;
  }
}

function openFloatingTutorWithPrompt(promptText) {
  const win = document.getElementById('floating-tutor-window');
  if (win && win.classList.contains('hidden')) {
    toggleFloatingTutor();
  }
  sendFloatingPrompt(promptText);
}

function clearFloatingTutorChat() {
  floatingTutorChatHistory = [];
  const box = document.getElementById('floating-chat-messages');
  const currentSub = STATE.subjects.find((s) => String(s.id) === String(STATE.activeSubjectId));
  const subName = currentSub ? currentSub.name : 'này';
  if (box) {
    box.innerHTML = `
      <div class="flex items-start gap-2">
        <div class="w-6 h-6 rounded-md flex items-center justify-center bg-indigo-500/20 text-indigo-400 text-xs shrink-0">🤖</div>
        <div class="p-2.5 rounded-xl bg-white/5 border border-white/5 txt-sub max-w-[85%]">
          Đã xóa hội thoại. Hãy hỏi tôi bất kỳ điều gì về môn <strong class="txt-brand">${escapeHtml(subName)}</strong>!
        </div>
      </div>
    `;
  }
  showToast('Đã làm mới cuộc hội thoại với Gia sư AI.', 'info');
}

async function sendFloatingPrompt(promptText) {
  const input = document.getElementById('floating-chat-input');
  if (input) input.value = promptText;
  await sendFloatingTutorMessage();
}

async function sendFloatingTutorMessage() {
  const input = document.getElementById('floating-chat-input');
  const userMsg = (input?.value || '').trim();
  if (!userMsg) return;
  input.value = '';

  const currentSub = STATE.subjects.find((s) => String(s.id) === String(STATE.activeSubjectId));
  const subName = currentSub ? currentSub.name : 'Tổng hợp Đại học';

  // Build complete context prompt for AI
  let fullPromptForAi = userMsg;
  if (pinnedTutorQuestion) {
    const pq = pinnedTutorQuestion;
    const opts = [
      pq.option_a ? `A. ${pq.option_a}` : '',
      pq.option_b ? `B. ${pq.option_b}` : '',
      pq.option_c ? `C. ${pq.option_c}` : '',
      pq.option_d ? `D. ${pq.option_d}` : ''
    ].filter(Boolean).join('\\n');

    fullPromptForAi = `[NGỮ CẢNH CÂU HỎI THI]:
Môn: ${subName} | ${pq.shortTitle}
Đề bài: ${pq.fullTitle}
${pq.code_snippet ? `Mã nguồn đi kèm:\\n\`\`\`csharp\\n${pq.code_snippet}\\n\`\`\`\\n` : ''}
Các phương án:
${opts || 'Tự luận / Trả lời ngắn'}
Đáp án chuẩn: ${pq.correct_option || 'Chưa công bố'}
${pq.explanation ? `Lời giải tham chiếu: ${pq.explanation}` : ''}
${pq.user_answer ? `Sinh viên chọn: ${pq.user_answer}` : ''}

[YÊU CẦU CỦA SINH VIÊN]:
${userMsg}`;
  }

  const box = document.getElementById('floating-chat-messages');
  if (box) {
    box.innerHTML += `
      <div class="flex items-start justify-end gap-2 animate-fade-in">
        <div class="p-2.5 rounded-xl badge-brand max-w-[85%] font-semibold">
          ${escapeHtml(userMsg)}
        </div>
        <div class="w-6 h-6 rounded-md flex items-center justify-center bg-violet-600 text-white text-xs shrink-0">👤</div>
      </div>
      <div id="ft-spinner" class="flex items-center gap-2 text-xs txt-muted pt-1">
        <div class="spinner-sm"></div> AI Gia Sư đang tư duy...
      </div>
    `;
    box.scrollTop = box.scrollHeight;
  }

  floatingTutorChatHistory.push({ role: 'user', content: fullPromptForAi });

  try {
    const res = await fetch('/api/ai/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        subject_name: subName,
        message: fullPromptForAi,
        persona: currentTutorPersona,
        history: floatingTutorChatHistory.slice(-8)
      })
    });
    const data = await res.json();
    document.getElementById('ft-spinner')?.remove();

    const reply = data.reply || 'Không có phản hồi từ AI.';
    floatingTutorChatHistory.push({ role: 'model', content: reply });

    const msgId = 'ft-msg-' + Date.now();
    window._tutorReplies[msgId] = reply;

    if (box) {
      box.innerHTML += `
        <div class="flex items-start gap-2 animate-fade-in" id="${msgId}">
          <div class="w-6 h-6 rounded-md flex items-center justify-center bg-indigo-500/20 text-indigo-400 text-xs shrink-0 mt-0.5">🤖</div>
          <div class="p-3 rounded-xl bg-white/5 border border-white/5 txt-sub max-w-[90%] space-y-2">
            <div class="flex items-center justify-between gap-1 text-[10px] font-mono txt-muted border-b pb-1 border-white/5">
              <span class="text-indigo-400 font-extrabold flex items-center gap-1">
                <span>🎓</span> ${escapeHtml(subName)}
              </span>
              <div class="flex items-center gap-1">
                <button type="button" onclick="speakAiReply('${msgId}')" class="btn-soft p-1 text-[11px]" title="Đọc bằng giọng nói">🔊</button>
                <button type="button" onclick="saveAiReplyAsFlashcard('${msgId}')" class="btn-soft px-1.5 py-0.5 text-[10px] font-bold text-amber-300" title="Lưu thành Flashcard">🃏 Đúc Thẻ</button>
                <button type="button" onclick="copyAiReply('${msgId}')" class="btn-soft p-1 text-[11px]" title="Sao chép">📋</button>
              </div>
            </div>
            <div class="leading-relaxed ai-tutor-content">
              ${renderAcademicText(reply)}
            </div>
          </div>
        </div>
      `;
      box.scrollTop = box.scrollHeight;
      renderAllMathOnPage(box);
    }
  } catch (err) {
    document.getElementById('ft-spinner')?.remove();
    if (box) {
      box.innerHTML += `
        <div class="p-2.5 rounded-xl badge-rose text-xs">
          Lỗi kết nối AI: ${escapeHtml(err.message)}
        </div>
      `;
    }
  }
}

function speakAiReply(msgId) {
  const text = window._tutorReplies?.[msgId];
  if (!text) return;
  if (!window.speechSynthesis) {
    showToast('Trình duyệt không hỗ trợ phát giọng nói.', 'warning');
    return;
  }
  window.speechSynthesis.cancel();
  const clean = text.replace(/<[^>]+>/g, '').replace(/[*_#`$~]/g, '').trim();
  const utter = new SpeechSynthesisUtterance(clean);
  utter.lang = 'vi-VN';
  utter.rate = 1.05;
  window.speechSynthesis.speak(utter);
  showToast('🔊 Đang đọc lời giải thích của AI...', 'info');
}

async function saveAiReplyAsFlashcard(msgId) {
  const text = window._tutorReplies?.[msgId];
  if (!text) return;

  const currentSub = STATE.subjects.find((s) => String(s.id) === String(STATE.activeSubjectId));
  const sid = currentSub ? currentSub.id : (STATE.activeSubjectId || 10);
  const subName = currentSub ? currentSub.name : 'Môn học';

  let front = '';
  let hint = '';
  if (pinnedTutorQuestion) {
    front = `${pinnedTutorQuestion.shortTitle}: ${pinnedTutorQuestion.fullTitle}`;
    hint = pinnedTutorQuestion.topic || 'Ôn tập câu hỏi';
  } else {
    front = `Khái niệm ôn thi (${subName})`;
    hint = 'Kiến thức cốt lõi';
  }

  const cleanBack = text.replace(/<[^>]+>/g, '').trim();

  try {
    const res = await apiFetch(`/api/subjects/${sid}/flashcards`, {
      method: 'POST',
      body: JSON.stringify({
        front: front.substring(0, 250),
        back: cleanBack.substring(0, 500),
        hint: hint.substring(0, 100)
      })
    });
    if (res.success || res.id) {
      playSound('correct');
      showToast(`🎉 Đã đúc thành công 1 thẻ Flashcard vào môn "${subName}"!`, 'success');
    } else {
      showToast('Không thể lưu thẻ: ' + (res.error || 'Lỗi không xác định'), 'warning');
    }
  } catch (err) {
    showToast('Lỗi lưu thẻ: ' + err.message, 'warning');
  }
}

function copyAiReply(msgId) {
  const text = window._tutorReplies?.[msgId];
  if (!text) return;
  navigator.clipboard.writeText(text).then(() => {
    showToast('📋 Đã sao chép nội dung giải thích!', 'success');
  }).catch(() => {
    showToast('Không thể sao chép tự động.', 'warning');
  });
}

function exportFloatingTutorNotes() {
  if (!floatingTutorChatHistory.length) {
    showToast('Chưa có hội thoại nào để xuất sổ tay!', 'warning');
    return;
  }
  const currentSub = STATE.subjects.find((s) => String(s.id) === String(STATE.activeSubjectId));
  const subName = currentSub ? currentSub.name : 'UniMaster';
  let content = `# 🎓 SỔ TAY ÔN THI GIA SƯ AI — ${subName.toUpperCase()}\\n`;
  content += `Thời gian xuất: ${new Date().toLocaleString('vi-VN')}\\n\\n`;
  floatingTutorChatHistory.forEach((turn) => {
    const role = turn.role === 'user' ? '👤 BẠN HỎI' : '🤖 GIA SƯ AI TRẢ LỜI';
    content += `### ${role}:\\n${turn.content}\\n\\n---\\n\\n`;
  });

  const blob = new Blob([content], { type: 'text/markdown;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `So_Tay_Gia_Su_AI_${subName.replace(/\\s+/g, '_')}_${Date.now()}.md`;
  a.click();
  URL.revokeObjectURL(url);
  showToast('📄 Đã tải xuống sổ tay ghi chú ôn thi!', 'success');
}

function toggleFloatingVoiceInput() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    showToast('Trình duyệt chưa hỗ trợ nhận diện giọng nói. Hãy dùng Google Chrome hoặc Edge!', 'warning');
    return;
  }

  if (isFloatingVoiceListening) {
    stopFloatingVoiceInput();
    return;
  }

  try {
    floatingVoiceRecognition = new SpeechRecognition();
    floatingVoiceRecognition.lang = 'vi-VN';
    floatingVoiceRecognition.continuous = false;
    floatingVoiceRecognition.interimResults = false;

    floatingVoiceRecognition.onstart = () => {
      isFloatingVoiceListening = true;
      document.getElementById('ft-voice-listening-bar')?.classList.remove('hidden');
      document.getElementById('btn-ft-mic')?.classList.add('badge-rose');
      showToast('🎙️ Đang nghe... Hãy nói câu hỏi của bạn!', 'info');
    };

    floatingVoiceRecognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      const input = document.getElementById('floating-chat-input');
      if (input) {
        input.value = transcript;
        sendFloatingTutorMessage();
      }
    };

    floatingVoiceRecognition.onerror = (e) => {
      console.warn('Speech recognition error:', e.error);
      stopFloatingVoiceInput();
      showToast('Lỗi nhận giọng nói: ' + e.error, 'warning');
    };

    floatingVoiceRecognition.onend = () => {
      stopFloatingVoiceInput();
    };

    floatingVoiceRecognition.start();
  } catch (err) {
    showToast('Không thể bật micro: ' + err.message, 'warning');
    stopFloatingVoiceInput();
  }
}

function stopFloatingVoiceInput() {
  isFloatingVoiceListening = false;
  document.getElementById('ft-voice-listening-bar')?.classList.add('hidden');
  document.getElementById('btn-ft-mic')?.classList.remove('badge-rose');
  if (floatingVoiceRecognition) {
    try { floatingVoiceRecognition.stop(); } catch (e) {}
    floatingVoiceRecognition = null;
  }
}

// -------------------------------------------------------------------------
// 1-TOUCH TRIGGERS FOR EXAM QUESTIONS & REVIEW
// -------------------------------------------------------------------------
function askAiAboutCurrentExamQuestion() {
  const q = STATE.exam.questions[STATE.exam.currentIndex];
  if (!q) {
    toggleFloatingTutor();
    return;
  }
  const idx = STATE.exam.currentIndex + 1;
  const userAns = STATE.exam.answers[q.id] || '';
  const isCorrect = STATE.exam.graded[q.id] ? (userAns.toUpperCase() === String(q._effectiveCorrect).toUpperCase()) : undefined;

  pinQuestionToTutor(q, {
    label: `Câu ${idx}`,
    user_answer: userAns,
    is_correct: isCorrect
  });
}

function askAiAboutCurrentTimedQuestion() {
  if (!window.TIMED_EXAM || !window.TIMED_EXAM.questions) return;
  const q = window.TIMED_EXAM.questions[window.TIMED_EXAM.currentIndex];
  if (!q) return;
  const idx = window.TIMED_EXAM.currentIndex + 1;
  const userAns = window.TIMED_EXAM.answers[q.id] || '';

  pinQuestionToTutor(q, {
    label: `Thi 60P - Câu ${idx}`,
    user_answer: userAns
  });
}

function askAiAboutReviewQuestion(qid) {
  const d = (STATE.exam.lastResult?.details || []).find((x) => x.question_id === qid);
  const fullQ = STATE.exam.questions.find((q) => q.id === qid) || d;
  if (!fullQ) return;

  pinQuestionToTutor(fullQ, {
    label: `Xem lại Câu #${qid}`,
    user_answer: d?.user_answer || '',
    is_correct: d?.is_correct
  });
}

async function askAiAboutMistakeQuestion(qid, sid) {
  closeModal('modal-mistake-bank');
  let q = STATE.exam.questions.find((x) => x.id === qid);
  if (!q) {
    try {
      const res = await apiFetch(`/api/subjects/${sid || 10}/questions?type=all`);
      q = (res.questions || []).find((x) => x.id === qid);
    } catch (e) {}
  }
  if (!q) {
    q = { id: qid, question_text: `Câu hỏi sai #${qid}` };
  }
  pinQuestionToTutor(q, {
    label: `Câu sai #${qid}`
  });
}
'''

# Replace old tutor section
old_tutor_start = code.find('// FEATURE 3: FLOATING AI TUTOR WIDGET')
old_tutor_end = code.find('// FEATURE 1: WEEKLY STUDY ANALYTICS & ACCURACY CHART')

if old_tutor_start != -1 and old_tutor_end != -1:
    code = code[:old_tutor_start] + new_tutor_code + '\n\n' + code[old_tutor_end:]
    print("Old tutor section replaced with new comprehensive tutor suite!")
else:
    print("Could not find old tutor section bounds")

# 2. Add askAiAboutReviewQuestion button in filterResultReview
old_rev_btn = '<button onclick="explainReviewItemMistake(${d.question_id})"'
new_rev_btn = '<button onclick="askAiAboutReviewQuestion(${d.question_id})" class="btn-primary !bg-gradient-to-r !from-indigo-600 !to-purple-600 !py-1 !px-2.5 !text-[11px] font-black flex items-center gap-1 shadow-sm hover:scale-105 active:scale-95 transition-all"><span>🤖</span> Hỏi AI</button>\n              <button onclick="explainReviewItemMistake(${d.question_id})"'

if 'askAiAboutReviewQuestion' not in code and old_rev_btn in code:
    code = code.replace(old_rev_btn, new_rev_btn, 1)
    print("askAiAboutReviewQuestion added to filterResultReview!")

# 3. Add askAiAboutMistakeQuestion button in openMistakeBankModal
old_ms_btn = '<button type="button" onclick="closeModal(\'modal-mistake-bank\');startSpecialDrill(\'mistakes\''
new_ms_btn = '<button type="button" onclick="askAiAboutMistakeQuestion(${item.id}, ${item.subject_id || sid})" class="btn-primary !bg-gradient-to-r !from-indigo-600 !to-purple-600 px-2.5 py-1.5 text-xs font-bold flex items-center gap-1 shadow-sm"><span>🤖</span> Hỏi AI</button>\n            <button type="button" onclick="closeModal(\'modal-mistake-bank\');startSpecialDrill(\'mistakes\''

if 'askAiAboutMistakeQuestion' not in code and old_ms_btn in code:
    code = code.replace(old_ms_btn, new_ms_btn, 1)
    print("askAiAboutMistakeQuestion added to openMistakeBankModal!")

# 4. Add KeyT and Escape shortcut in setupKeyboardShortcuts
old_shortcut_z = "else if (e.code === 'KeyZ') { e.preventDefault(); toggleZenMode(); }"
new_shortcut_zt = "else if (e.code === 'KeyZ') { e.preventDefault(); toggleZenMode(); }\n      else if (e.code === 'KeyT') { e.preventDefault(); askAiAboutCurrentExamQuestion(); return; }"

if "e.code === 'KeyT'" not in code and old_shortcut_z in code:
    code = code.replace(old_shortcut_z, new_shortcut_zt)
    print("KeyT shortcut added to exam shortcuts!")

# Add global KeyT when not in exam
old_flashcard_shortcut = "} else if (STATE.currentTab === 'flashcards') {"
new_flashcard_shortcut = "} else if (e.code === 'KeyT') {\n      e.preventDefault();\n      toggleFloatingTutor();\n      return;\n    } else if (STATE.currentTab === 'flashcards') {"

if "e.preventDefault();\n      toggleFloatingTutor();" not in code and old_flashcard_shortcut in code:
    code = code.replace(old_flashcard_shortcut, new_flashcard_shortcut)
    print("Global KeyT shortcut added!")

# Add Escape to close tutor window
old_open_mod = "const openMod = document.querySelector('.modal-overlay:not(.hidden)');"
new_open_mod = """const ftWin = document.getElementById('floating-tutor-window');
    if (ftWin && !ftWin.classList.contains('hidden') && e.key === 'Escape') {
      e.preventDefault();
      toggleFloatingTutor();
      return;
    }
    const openMod = document.querySelector('.modal-overlay:not(.hidden)');"""

if "ftWin && !ftWin.classList.contains('hidden')" not in code and old_open_mod in code:
    code = code.replace(old_open_mod, new_open_mod)
    print("Escape key for tutor window added!")

with open("static/app.js", "w", encoding="utf-8") as f:
    f.write(code)

print("static/app.js updated successfully!")
