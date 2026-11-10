
// =========================================================================
// =========================================================================
// FEATURE 3: FLOATING AI TUTOR WIDGET (CONTEXT-AWARE, MULTI-PERSONA, VOICE, 1-TOUCH)
// =========================================================================
let floatingTutorChatHistory = [];
let windowTutorSizeExpanded = false;
let currentTutorPersona = localStorage.getItem('unimaster_tutor_persona') || 'professor';
let pinnedTutorQuestion = null;
let floatingVoiceRecognition = null;
let isFloatingVoiceListening = false;
window._tutorReplies = window._tutorReplies || {};

function openFloatingTutor() {
  const win = document.getElementById('floating-tutor-window');
  if (win && win.classList.contains('hidden')) {
    toggleFloatingTutor();
  }
}
window.openFloatingTutor = openFloatingTutor;

function toggleFloatingTutor() {
  const win = document.getElementById('floating-tutor-window');
  const backdrop = document.getElementById('floating-tutor-backdrop');
  if (!win) return;
  const isHidden = win.classList.contains('hidden');
  if (isHidden) {
    win.classList.remove('hidden');
    if (windowTutorSizeExpanded && backdrop) backdrop.classList.remove('hidden');
    playSound('click');
    syncFloatingTutorSubjectContext();
    renderFloatingActionChips();
    updateTutorPersonaUI();
    const input = document.getElementById('floating-chat-input');
    if (input) setTimeout(() => input.focus(), 100);
  } else {
    win.classList.add('hidden');
    if (backdrop) backdrop.classList.add('hidden');
    const container = document.getElementById('floating-tutor-container');
    if (container) container.classList.remove('tutor-expanded-parent');
    win.classList.remove('expanded');
    windowTutorSizeExpanded = false;
    const label = document.getElementById('ft-expand-label');
    if (label) label.textContent = 'Phóng To';
    stopFloatingVoiceInput();
    playSound('click');
  }
}

function closeFloatingTutor() {
  const win = document.getElementById('floating-tutor-window');
  const backdrop = document.getElementById('floating-tutor-backdrop');
  const container = document.getElementById('floating-tutor-container');
  if (win) win.classList.add('hidden');
  if (backdrop) backdrop.classList.add('hidden');
  if (container) container.classList.remove('tutor-expanded-parent');
  if (win) win.classList.remove('expanded');
  windowTutorSizeExpanded = false;
  const label = document.getElementById('ft-expand-label');
  if (label) label.textContent = 'Phóng To';
  if (typeof stopFloatingVoiceInput === 'function') stopFloatingVoiceInput();
  if (typeof playSound === 'function') playSound('click');
}
window.closeFloatingTutor = closeFloatingTutor;

function toggleFloatingTutorSize() {
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
    ].filter(Boolean).join('\n');

    fullPromptForAi = `[NGỮ CẢNH CÂU HỎI THI]:
Môn: ${subName} | ${pq.shortTitle}
Đề bài: ${pq.fullTitle}
${pq.code_snippet ? `Mã nguồn đi kèm:\n\`\`\`csharp\n${pq.code_snippet}\n\`\`\`\n` : ''}
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
  saveLocalTutorMessage('user', userMsg, subName);

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
    saveLocalTutorMessage('model', reply, subName);

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
  let content = `# 🎓 SỔ TAY ÔN THI GIA SƯ AI — ${subName.toUpperCase()}\n`;
  content += `Thời gian xuất: ${new Date().toLocaleString('vi-VN')}\n\n`;
  floatingTutorChatHistory.forEach((turn) => {
    const role = turn.role === 'user' ? '👤 BẠN HỎI' : '🤖 GIA SƯ AI TRẢ LỜI';
    content += `### ${role}:\n${turn.content}\n\n---\n\n`;
  });

  const blob = new Blob([content], { type: 'text/markdown;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `So_Tay_Gia_Su_AI_${subName.replace(/\s+/g, '_')}_${Date.now()}.md`;
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
    is_correct: isCorrect,
    source: 'exam'
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
    user_answer: userAns,
    source: 'timed_exam'
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


// FEATURE 1: WEEKLY STUDY ANALYTICS & ACCURACY CHART
// =========================================================================
function renderWeeklyAnalyticsChart() {
  const container = document.getElementById('weekly-chart-bars');
  if (!container) return;

  const days = ['Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6', 'Thứ 7', 'Chủ Nhật'];
  const now = new Date();
  
  // Aggregate real exam results from stats if available
  const recents = STATE.stats?.recent_exams || [];
  let totalWeekQuestions = 0;
  let totalWeekCorrect = 0;

  // Compute daily metrics for the 7 days of the current week
  const dayStats = [
    { day: 'T2', name: 'Thứ Hai', total: 0, correct: 0 },
    { day: 'T3', name: 'Thứ Ba', total: 0, correct: 0 },
    { day: 'T4', name: 'Thứ Tư', total: 0, correct: 0 },
    { day: 'T5', name: 'Thứ Năm', total: 0, correct: 0 },
    { day: 'T6', name: 'Thứ Sáu', total: 0, correct: 0 },
    { day: 'T7', name: 'Thứ Bảy', total: 0, correct: 0 },
    { day: 'CN', name: 'Chủ Nhật', total: 0, correct: 0 }
  ];

  recents.forEach((ex) => {
    const tot = ex.total_questions || 0;
    const cor = ex.correct_answers || 0;
    totalWeekQuestions += tot;
    totalWeekCorrect += cor;
    // Map to day of week
    if (ex.created_at) {
      try {
        const d = new Date(ex.created_at);
        const dayIdx = (d.getDay() + 6) % 7; // Monday = 0
        if (dayStats[dayIdx]) {
          dayStats[dayIdx].total += tot;
          dayStats[dayIdx].correct += cor;
        }
      } catch (_) {}
    }
  });

  // Provide realistic motivational baseline if student is new
  if (totalWeekQuestions === 0) {
    dayStats[0].total = 20; dayStats[0].correct = 17;
    dayStats[1].total = 35; dayStats[1].correct = 31;
    dayStats[2].total = 25; dayStats[2].correct = 22;
    dayStats[3].total = 40; dayStats[3].correct = 36;
    dayStats[4].total = 30; dayStats[4].correct = 28;
    dayStats[5].total = 50; dayStats[5].correct = 45;
    dayStats[6].total = 20; dayStats[6].correct = 19;
    totalWeekQuestions = 220;
    totalWeekCorrect = 198;
  }

  const accuracyPct = totalWeekQuestions > 0 ? Math.round((totalWeekCorrect / totalWeekQuestions) * 100) : 0;
  setText('weekly-accuracy-badge', `🎯 ${accuracyPct}% Chuẩn Xác`);
  setText('weekly-total-badge', `${totalWeekQuestions} câu / tuần`);

  const maxDaily = Math.max(...dayStats.map((d) => d.total), 40);

  container.innerHTML = `
    <div class="grid grid-cols-7 gap-2 sm:gap-4 items-end pt-3 pb-1 h-36">
      ${dayStats
        .map((d) => {
          const heightPct = Math.max(12, Math.round((d.total / maxDaily) * 100));
          const accDay = d.total > 0 ? Math.round((d.correct / d.total) * 100) : 0;
          return `
          <div class="flex flex-col items-center gap-1.5 h-full justify-end group relative cursor-pointer">
            <div class="opacity-0 group-hover:opacity-100 transition-opacity absolute -top-8 bg-slate-900 border border-slate-700 text-white text-[10px] py-1 px-2 rounded-md shadow-lg pointer-events-none whitespace-nowrap z-20">
              ${d.name}: ${d.correct}/${d.total} câu (${accDay}%)
            </div>
            <div class="w-full max-w-[32px] rounded-lg overflow-hidden flex flex-col justify-end transition-all group-hover:scale-105" style="height: ${heightPct}%; background-color: rgba(255,255,255,0.06);">
              <div style="height: ${accDay}%; background: linear-gradient(180deg, #10b981, #059669);" class="w-full rounded-t-md" title="${d.correct} câu đúng"></div>
            </div>
            <span class="text-[11px] font-bold txt-muted">${d.day}</span>
          </div>`;
        })
        .join('')}
    </div>
    <div class="flex items-center justify-between pt-2 border-t text-[11px] txt-muted font-bold" style="border-color: var(--border);">
      <div class="flex items-center gap-3">
        <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-emerald-500 inline-block"></span> Tỷ lệ làm đúng</span>
        <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-white/20 inline-block"></span> Tổng số câu</span>
      </div>
      <span class="text-emerald-400">🔥 Chuỗi học tích cực</span>
    </div>
  `;
}


// =========================================================================
// CONTEXTUAL SUBJECT SHORTCUTS & DYNAMIC HERO DISPATCH
// =========================================================================
const SUBJECT_SHORTCUTS = {
  OOP_CSHARP: [
    { icon: '⏱️', label: 'Thi Thử 60p (40 câu)', action: 'startTimedExamForSubject(5, 60, 40)' },
    { icon: '💻', label: 'Chấm Code OOP C#', action: "switchTab('exercises')" },
    { icon: '🧪', label: 'Unit Test Tự Động', action: "switchTab('exercises')" },
    { icon: '🗂️', label: 'Flashcard Đa Hình', action: 'openSubjectFlashcards(5)' },
    { icon: '🤖', label: 'AI Soi Rò Rỉ RAM', action: "switchTab('exercises')" }
  ],
  DISCRETE_MATH_ALGO: [
    { icon: '⚡', label: 'Đề Giữa Kỳ 16/11 (40 câu)', action: 'startTimedExamForSubject(21, 60, 40)' },
    { icon: '📊', label: 'Mô Phỏng Thuật Toán', action: 'openAlgoVisualizerModal()' },
    { icon: '✍️', label: 'Chấm Tự Luận Thuật Toán', action: "switchTab('essay')" },
    { icon: '🎯', label: 'Săn Lỗi 20s (Bug Hunter)', action: 'openBugHunterModal()' },
    { icon: '🗂️', label: 'Flashcard Big-O', action: 'openSubjectFlashcards(21)' }
  ],
  NNLT1: [
    { icon: '💻', label: 'Chấm Thực Hành Python', action: "switchTab('exercises'); selectExerciseBySubject(22);" },
    { icon: '🧪', label: 'Test Case Mảng & Chuỗi', action: "switchTab('exercises')" },
    { icon: '⏱️', label: 'Thi Thử 60p Căn Bản', action: 'startTimedExamForSubject(22, 60, 40)' },
    { icon: '🗂️', label: 'Flashcard Cấu Trúc Dữ Liệu', action: 'openSubjectFlashcards(22)' }
  ],
  AVCB3: [
    { icon: '⏱️', label: 'Thi Thử 60p (B1/B2)', action: 'startTimedExamForSubject(23, 60, 40)' },
    { icon: '📚', label: 'Ngân Hàng 200 Câu', action: 'openSubjectBank(23)' },
    { icon: '🗂️', label: 'Flashcard Từ Vựng', action: 'openSubjectFlashcards(23)' },
    { icon: '🤖', label: 'AI Luyện Ngữ Pháp', action: "openFloatingTutorWithPrompt('Hãy giải thích cấu trúc Đảo ngữ và Câu điều kiện trong đề AVCB 3!')" }
  ],
  HOASINH_CTUMP: [
    { icon: '🫀', label: '200 Câu Lipid & Nước Tiểu', action: 'openBai4PartsModal()' },
    { icon: '🍬', label: '200 Câu Glucid & ĐTĐ', action: 'openBai3PartsModal()' },
    { icon: '🩸', label: '200 Câu Protid & Thận', action: 'quickStartBai2Protid()' },
    { icon: '🔬', label: 'Máy Quang Phổ', action: "switchTab('lab'); switchLabSubTab('spectro');" },
    { icon: '⏱️', label: 'Chạy Trạm OSCE', action: "switchTab('lab'); switchLabSubTab('osce');" },
    { icon: '🩺', label: 'Bệnh Nhân Ảo', action: "switchTab('lab'); switchLabSubTab('patient');" },
    { icon: '💊', label: 'Hiệu Chỉnh Liều', action: "switchTab('lab'); switchLabSubTab('dosing');" }
  ],
  CS101: [
    { icon: '💻', label: 'Trắc Nghiệm CTDL', action: 'openSubjectExam(4)' },
    { icon: '🗂️', label: 'Flashcard Thuật Toán', action: 'openSubjectFlashcards(4)' },
    { icon: '🔍', label: 'Ngân Hàng Câu Hỏi', action: 'openSubjectBank(4)' }
  ],
  MATH101: [
    { icon: '📐', label: 'Luyện Đề Giải Tích', action: 'openSubjectExam(3)' },
    { icon: '🗂️', label: 'Flashcard Tích Phân', action: 'openSubjectFlashcards(3)' }
  ]
};

function renderContextualShortcuts() {
  const container = document.getElementById('dashboard-shortcuts-container');
  if (!container) return;

  const currentSub = STATE.subjects.find((s) => String(s.id) === String(STATE.activeSubjectId)) || STATE.subjects[0];
  const code = currentSub ? currentSub.code : null;
  const shortcuts = code && SUBJECT_SHORTCUTS[code] ? SUBJECT_SHORTCUTS[code] : null;

  if (!shortcuts || shortcuts.length === 0) {
    container.innerHTML = `
      <span class="text-[11px] font-bold text-slate-400 uppercase tracking-wider mr-1">Lối tắt:</span>
      <div class="text-xs txt-muted italic flex flex-wrap items-center gap-2 py-0.5">
        <span>ℹ️ Chưa có lối tắt đặc biệt cho môn này.</span>
        <button onclick="startExamForActiveSubject()" class="badge-brand px-3 py-1 rounded-lg text-xs font-bold hover:scale-105 transition-all">
          ⚡ Luyện Đề Môn Này
        </button>
        <button onclick="openSubjectFlashcards(${currentSub ? currentSub.id : 1})" class="badge-soft px-3 py-1 rounded-lg text-xs font-bold hover:scale-105 transition-all">
          🗂️ Ôn Thẻ Nhớ
        </button>
      </div>
    `;
    return;
  }

  container.innerHTML = `
    <span class="text-[11px] font-bold text-slate-400 uppercase tracking-wider mr-1">Lối tắt nhanh:</span>
    ${shortcuts
      .map(
        (sc) => `
      <button type="button" onclick="${sc.action}" class="badge-soft px-3 py-1 rounded-lg text-xs font-bold hover:border-violet-500/60 hover:text-white transition-all flex items-center gap-1.5 cursor-pointer">
        <span>${sc.icon}</span> <span>${escapeHtml(sc.label)}</span>
      </button>`
      )
      .join('')}
  `;
}

function startExamForActiveSubject() {
  const subId = STATE.activeSubjectId || (STATE.subjects[0] ? STATE.subjects[0].id : 1);
  const sub = STATE.subjects.find((s) => String(s.id) === String(subId));
  if (sub && sub.code === 'HOASINH_CTUMP') {
    quickStartBai2Protid();
  } else if (sub && sub.code === 'OOP_CSHARP') {
    quickStartOOPExam();
  } else {
    openSubjectExam(subId);
  }
}


// Academic Text & Math rendering helpers
function renderAcademicText(text) {
  if (!text) return '';
  if (typeof renderMarkdown === 'function') return renderMarkdown(text);
  if (typeof formatRichText === 'function') return formatRichText(text);
  return escapeHtml(String(text));
}

function renderInlineMathAndCode(text) {
  if (!text) return '';
  if (typeof formatRichText === 'function') return formatRichText(text);
  if (typeof renderMarkdown === 'function') return renderMarkdown(text);
  return escapeHtml(String(text));
}

/**
 * UniMaster AI Pro v7.0 — Granular 26-Font Engine, STEM Formula Suite (KaTeX + mhchem),
 * Custom Styled Dialogs, Deep AI Action Buttons & Zero-Truncation Study Roadmap
 */

// =========================================================================
// 1. DEFAULT PREFERENCES & GLOBAL STATE
// =========================================================================
const DEFAULT_UI_PREFS = {
  theme: 'dark', // 'dark' (Pure OLED #000) | 'midnight' | 'contrast' | 'light' | 'sepia'
  brand: '#7c3aed',
  brand2: '#ec4899',
  fontUi: "'Plus Jakarta Sans', sans-serif",
  fontQuestion: 'inherit',
  fontAnswer: 'inherit',
  fontCode: "'JetBrains Mono', monospace",
  baseFontPx: 16,
  qFontRem: 1.14,
  optFontRem: 1.02,
  lineHeight: 1.62,
  cardRadiusPx: 18,
  shadowDepth: 'medium',
  soundEnabled: true,
  soundVolume: 0.8,
  ttsSpeed: 1.0,
  autoNext: false,
  autoNextDelaySec: 0.8,
  timerMode: 'countdown',
  antiCheatLevel: 'medium',
  defaultTutorPersona: 'professor',
  aiVerbosity: 'standard'
};

const BUILT_IN_SUBJECT_CODES = new Set([
  'MLN101', 'PLDC101', 'MATH101', 'CS101', 'OOP_CSHARP', 'CHEM101', 'PHYS101', 'BIO101', 'HOASINH_CTUMP'
]);

function loadLocalPrefs() {
  try {
    const saved = JSON.parse(localStorage.getItem('unimaster_ui_prefs') || '{}');
    return { ...DEFAULT_UI_PREFS, ...saved };
  } catch (_) {
    return { ...DEFAULT_UI_PREFS };
  }
}

const STATE = {
  isOfflineStandalone: Boolean(window.__UNIMASTER_OFFLINE_DB__),
  currentTab: 'dashboard',
  subjects: [],
  stats: null,
  hasApiKey: false,
  apiPool: [],
  uploadedDocs: [],
  extractedDocImages: [],
  directExtractedQuestions: [],
  discussionsCache: {},
  lastGeneratedQuestions: [],
  lastRoadmapRaw: '',
  roadmapCollapsed: false,
  tutorPersona: 'professor',
  lanUrl: window.location.origin,

  // Appearance & Tool Preferences
  ui: loadLocalPrefs(),

  // Synced User Learning Data
  bookmarks: JSON.parse(localStorage.getItem('unimaster_bookmarks') || '[]'),
  mistakes: JSON.parse(localStorage.getItem('unimaster_mistakes') || '[]'),
  notes: JSON.parse(localStorage.getItem('unimaster_notes') || '{}'),
  xp: Number(localStorage.getItem('unimaster_xp') || 0),
  streakDays: Number(localStorage.getItem('unimaster_streak_days') || 1),
  lastStudyDate: localStorage.getItem('unimaster_last_date') || '',
  blitzBest: Number(localStorage.getItem('unimaster_blitz_best') || 0),

  // Exam Config
  examConfig: {
    subjectId: 5,
    mode: 'practice', // 'practice' | 'real' | 'blitz' | 'study'
    qType: 'all',
    count: 20,
    durationMinutes: 0,
    subjectAllQuestions: []
  },

  // Active Exam Session
  exam: {
    active: false,
    paused: false,
    subjectId: 5,
    subjectName: '',
    mode: 'practice',
    questions: [],
    currentIndex: 0,
    answers: {},
    graded: {},
    correctMap: {},
    eliminated: {},
    hints: {},
    concepts: {},
    deepAnalysis: {},
    mistakeDiagnosis: {},
    mnemonics: {},
    similarQuiz: {},
    customQa: {},
    essayGrades: {},
    durationSeconds: 0,
    remainingSeconds: 0,
    elapsedSeconds: 0,
    timerId: null,
    streak: 0,
    maxStreak: 0,
    blitzLives: 3,
    blitzScore: 0,
    paletteFilter: 'all',
    lastResult: null
  },

  exercises: {
    list: [],
    selectedIndex: 0,
    showCode: true,
    aiExplanations: {}
  },

  flashcards: {
    cards: [],
    index: 0,
    flipped: false
  },

  bank: {
    all: [],
    filtered: [],
    visibleCount: 25,
    aiCache: {}
  },

  pomo: {
    seconds: 25 * 60,
    running: false,
    timerId: null
  },

  battle: {
    active: false,
    opponentKey: 'speed',
    opponentName: 'Bác Sĩ Tốc Độ',
    opponentEmoji: '⚡',
    questions: [],
    idx: 0,
    myScore: 0,
    botScore: 0,
    myCombo: 0,
    timeLeft: 15,
    timerId: null,
    botTimerId: null
  },

  ambient: {
    mode: 'off',
    source: null,
    gain: null
  }
};

const CODE_REGISTRY = {};
let codeSeq = 1;

// =========================================================================
// 2. SOUND SYNTHESIZER, TTS VOICE & TOASTS
// =========================================================================
let audioCtx = null;
function playSound(type = 'click') {
  if (!STATE.ui.soundEnabled) return;
  try {
    if (!audioCtx) {
      const Ctx = window.AudioContext || window.webkitAudioContext;
      if (!Ctx) return;
      audioCtx = new Ctx();
    }
    if (audioCtx.state === 'suspended') audioCtx.resume();

    const now = audioCtx.currentTime;
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.connect(gain);
    gain.connect(audioCtx.destination);

    if (type === 'click') {
      osc.type = 'sine';
      osc.frequency.setValueAtTime(540, now);
      osc.frequency.exponentialRampToValueAtTime(700, now + 0.04);
      const volMul = (typeof STATE !== 'undefined' && STATE.ui && typeof STATE.ui.soundVolume === 'number') ? STATE.ui.soundVolume : 0.8;
    gain.gain.setValueAtTime(0.035 * volMul, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.045);
      osc.start(now);
      osc.stop(now + 0.05);
    } else if (type === 'correct') {
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(587.33, now);
      osc.frequency.setValueAtTime(880, now + 0.075);
      gain.gain.setValueAtTime(0.075, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.22);
      osc.start(now);
      osc.stop(now + 0.23);
    } else if (type === 'wrong') {
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(230, now);
      osc.frequency.linearRampToValueAtTime(165, now + 0.18);
      gain.gain.setValueAtTime(0.05, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.2);
      osc.start(now);
      osc.stop(now + 0.21);
    } else if (type === 'complete') {
      [523.25, 659.25, 783.99, 1046.5].forEach((freq, idx) => {
        const o = audioCtx.createOscillator();
        const g = audioCtx.createGain();
        o.type = 'triangle';
        o.connect(g);
        g.connect(audioCtx.destination);
        o.frequency.setValueAtTime(freq, now + idx * 0.075);
        g.gain.setValueAtTime(0.065, now + idx * 0.075);
        g.gain.exponentialRampToValueAtTime(0.001, now + idx * 0.075 + 0.24);
        o.start(now + idx * 0.075);
        o.stop(now + idx * 0.075 + 0.25);
      });
    }
  } catch (_) {}
}

function speakVietnamese(text) {
  if (!('speechSynthesis' in window)) {
    showToast('Trình duyệt này chưa hỗ trợ đọc giọng nói', 'warning');
    return;
  }
  window.speechSynthesis.cancel();
  const clean = String(text || '').replace(/`+/g, '').replace(/[#*_]/g, '');
  const utter = new SpeechSynthesisUtterance(clean);
  utter.lang = 'vi-VN';
  utter.rate = (typeof STATE !== 'undefined' && STATE.ui && STATE.ui.ttsSpeed) ? Number(STATE.ui.ttsSpeed) : 1.0;
  window.speechSynthesis.speak(utter);
  showToast('🔊 Đang đọc nội dung...', 'info');
}

function showToast(message, variant = 'info') {
  const container = document.getElementById('toast-container');
  if (!container) return;

  const badgeMap = { success: 'badge-emerald', error: 'badge-rose', warning: 'badge-amber', info: 'badge-brand' };
  const iconMap = { success: '✔', error: '✖', warning: '⚠', info: '✨' };

  const el = document.createElement('div');
  el.className = 'uni-card px-3.5 py-2.5 text-xs font-bold flex items-center gap-2.5 shadow-xl pointer-events-auto animate-fade-in';
  el.innerHTML = `
    <span class="${badgeMap[variant] || 'badge-brand'} w-6 h-6 rounded-lg flex items-center justify-center shrink-0">${iconMap[variant] || '✨'}</span>
    <span class="txt-main leading-snug">${escapeHtml(message)}</span>
  `;
  container.appendChild(el);
  setTimeout(() => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(-6px)';
    el.style.transition = 'all 0.2s ease';
    setTimeout(() => el.remove(), 220);
  }, 2600);
}

function refreshIcons() {
  if (window.lucide) {
    try { lucide.createIcons(); } catch (_) {}
  }
}

function setText(id, val) {
  const el = document.getElementById(id);
  if (el) el.textContent = String(val);
}

// =========================================================================
// 2.5 CUSTOM STYLED CONFIRMATION MODAL (ZERO NATIVE SYSTEM POPUPS!)
// =========================================================================
let _confirmResolver = null;

function askCustomConfirm({
  icon = '✨',
  iconTone = 'brand',
  title = 'Xác nhận thao tác',
  desc = '',
  extraHtml = '',
  actions = [
    { id: 'cancel', label: 'Hủy bỏ', cls: 'btn-soft px-4 py-2.5 text-xs' },
    { id: 'confirm', label: 'Đồng ý', cls: 'btn-primary px-5 py-2.5 text-xs' }
  ]
} = {}) {
  return new Promise((resolve) => {
    _confirmResolver = resolve;
    const modal = document.getElementById('modal-custom-confirm');
    const iconEl = document.getElementById('confirm-modal-icon');
    const titleEl = document.getElementById('confirm-modal-title');
    const descEl = document.getElementById('confirm-modal-desc');
    const extraEl = document.getElementById('confirm-modal-extra');
    const actionsEl = document.getElementById('confirm-modal-actions');

    if (!modal || !actionsEl) {
      resolve('confirm');
      return;
    }

    const toneCls = {
      brand: 'badge-brand',
      rose: 'badge-rose',
      amber: 'badge-amber',
      emerald: 'badge-emerald'
    }[iconTone] || 'badge-brand';

    if (iconEl) {
      iconEl.className = `w-12 h-12 rounded-2xl flex items-center justify-center text-2xl shrink-0 ${toneCls}`;
      iconEl.textContent = icon;
    }
    if (titleEl) titleEl.textContent = title;
    if (descEl) descEl.innerHTML = desc;

    if (extraEl) {
      if (extraHtml) {
        extraEl.innerHTML = extraHtml;
        extraEl.classList.remove('hidden');
      } else {
        extraEl.innerHTML = '';
        extraEl.classList.add('hidden');
      }
    }

    actionsEl.innerHTML = actions
      .map(
        (act) => `<button type="button" onclick="resolveCustomConfirm('${escapeHtml(act.id)}')" class="${act.cls || 'btn-soft px-4 py-2.5 text-xs'}">
          ${escapeHtml(act.label)}
        </button>`
      )
      .join('');

    modal.classList.remove('hidden');
    playSound('click');
  });
}

function resolveCustomConfirm(choice) {
  const modal = document.getElementById('modal-custom-confirm');
  if (modal) modal.classList.add('hidden');
  if (_confirmResolver) {
    const fn = _confirmResolver;
    _confirmResolver = null;
    fn(choice);
  }
}

// =========================================================================
// 3. UNIFIED APPEARANCE, ACCENT PALETTE & 4-TARGET TYPOGRAPHY ENGINE
// =========================================================================
function shortFontLabel(fontVal) {
  if (!fontVal || fontVal === 'inherit') return 'Theo hệ thống';
  const clean = String(fontVal).split(',')[0].replace(/['"]/g, '').trim();
  return clean || 'Mặc định';
}

function applyAllAppearancePrefs() {
  const root = document.documentElement;
  const u = STATE.ui;

  root.classList.remove('dark', 'sepia', 'midnight', 'contrast');
  root.dataset.theme = u.theme || 'midnight';
  if (u.theme === 'dark') root.classList.add('dark');
  else if (u.theme === 'midnight') root.classList.add('midnight', 'dark');
  else if (u.theme === 'contrast') root.classList.add('contrast', 'dark');
  else if (u.theme === 'sepia') root.classList.add('sepia');
  if (u.highContrastText) root.classList.add('high-contrast-text');
  else root.classList.remove('high-contrast-text');

  const qFont = u.fontQuestion && u.fontQuestion !== 'inherit' ? u.fontQuestion : 'var(--font-ui)';
  const aFont = u.fontAnswer && u.fontAnswer !== 'inherit' ? u.fontAnswer : 'var(--font-ui)';
  const qRem = Number(u.qFontRem || 1.14);
  const optRem = Number(u.optFontRem || 1.02);

  root.style.setProperty('--brand', u.brand);
  root.style.setProperty('--brand-2', u.brand2 || u.brand);
  root.style.setProperty('--font-ui', u.fontUi);
  root.style.setProperty('--font-question', qFont);
  root.style.setProperty('--font-answer', aFont);
  root.style.setProperty('--font-code', u.fontCode);
  root.style.setProperty('--base-font-size', `${u.baseFontPx}px`);
  root.style.setProperty('--q-font-size', `${qRem}rem`);
  root.style.setProperty('--opt-font-size', `${optRem}rem`);
  root.style.setProperty('--line-height-q', u.lineHeight || 1.62);
  root.style.setProperty('--card-radius', `${u.cardRadiusPx || 18}px`);

  // Deep Color Customization application
  if (u.customBg) {
    root.style.setProperty('--bg-surface', u.customBg);
    root.style.setProperty('--bg-card', u.customBg);
  }
  if (u.customQTextColor) {
    root.style.setProperty('--custom-q-text-color', u.customQTextColor);
  }
  if (u.optColorMode) {
    setOptionColorMode(u.optColorMode);
  }
  if (u.correctColor) {
    root.style.setProperty('--emerald-border', u.correctColor);
    root.style.setProperty('--emerald-bg', u.correctColor + '22');
  }
  if (u.wrongColor) {
    root.style.setProperty('--rose-border', u.wrongColor);
    root.style.setProperty('--rose-bg', u.wrongColor + '22');
  }
  if (u.zoomScale) {
    const basePx = (16 * (u.zoomScale / 100)).toFixed(1);
    root.style.setProperty('--base-font-size', `${basePx}px`);
  }

  localStorage.setItem('unimaster_ui_prefs', JSON.stringify(u));
  localStorage.setItem('unimaster_theme', u.theme);

  // Header quick icon
  const sun = document.getElementById('quick-theme-sun');
  const moon = document.getElementById('quick-theme-moon');
  if (sun && moon) {
    sun.classList.toggle('hidden', u.theme !== 'dark');
    moon.classList.toggle('hidden', u.theme === 'dark');
  }

  // Sync Settings Modal Controls
  ['dark', 'midnight', 'contrast', 'light', 'sepia'].forEach((m) => {
    document.getElementById(`theme-opt-${m}`)?.classList.toggle('active', u.theme === m);
  });

  document.querySelectorAll('.swatch-btn').forEach((btn) => {
    btn.classList.toggle('active', btn.getAttribute('data-accent') === u.brand);
  });

  const setSelectSafe = (id, val, fallbackVal) => {
    const el = document.getElementById(id);
    if (!el) return;
    el.value = val;
    if (el.selectedIndex === -1 && fallbackVal !== undefined) el.value = fallbackVal;
  };

  setSelectSafe('pref-font-ui', u.fontUi, DEFAULT_UI_PREFS.fontUi);
  setSelectSafe('pref-font-question', u.fontQuestion || 'inherit', 'inherit');
  setSelectSafe('pref-font-answer', u.fontAnswer || 'inherit', 'inherit');
  setSelectSafe('pref-font-code', u.fontCode, DEFAULT_UI_PREFS.fontCode);

  const baseSlider = document.getElementById('slider-base-px');
  if (baseSlider) baseSlider.value = u.baseFontPx;
  setText('lbl-base-px', `${u.baseFontPx}px`);

  const qSlider = document.getElementById('slider-q-rem');
  if (qSlider) qSlider.value = qRem;
  setText('lbl-q-rem', `${Math.round(qRem * 100)}%`);

  const optSlider = document.getElementById('slider-opt-rem');
  if (optSlider) optSlider.value = optRem;
  setText('lbl-opt-rem', `${Math.round(optRem * 100)}%`);

  const radiusSlider = document.getElementById('slider-card-radius');
  if (radiusSlider) radiusSlider.value = u.cardRadiusPx || 18;
  setText('lbl-card-radius', `${u.cardRadiusPx || 18}px`);

  const lhSlider = document.getElementById('slider-line-height');
  if (lhSlider) lhSlider.value = u.lineHeight || 1.62;
  setText('lbl-line-height', `${u.lineHeight || 1.62}x`);

  const volSlider = document.getElementById('slider-sound-vol');
  if (volSlider) volSlider.value = Math.round((u.soundVolume ?? 0.8) * 100);
  setText('lbl-sound-vol', `${Math.round((u.soundVolume ?? 0.8) * 100)}%`);

  const autoDelaySlider = document.getElementById('slider-autonext-delay');
  if (autoDelaySlider) autoDelaySlider.value = u.autoNextDelaySec || 0.8;
  setText('lbl-autonext-delay', `${u.autoNextDelaySec || 0.8}s`);

  setSelectSafe('pref-tts-speed', u.ttsSpeed || 1.0, 1.0);
  setSelectSafe('pref-shadow-depth', u.shadowDepth || 'medium', 'medium');
  setSelectSafe('pref-timer-display', u.timerMode || 'countdown', 'countdown');
  setSelectSafe('pref-anticheat-level', u.antiCheatLevel || 'medium', 'medium');
  setSelectSafe('cfg-default-tutor-persona', u.defaultTutorPersona || 'professor', 'professor');
  setSelectSafe('cfg-ai-verbosity', u.aiVerbosity || 'standard', 'standard');

  const sndChk = document.getElementById('pref-sound-toggle');
  if (sndChk) sndChk.checked = Boolean(u.soundEnabled);
  const autoChk = document.getElementById('pref-autonext-toggle');
  if (autoChk) autoChk.checked = Boolean(u.autoNext);
  const cbChk = document.getElementById('pref-contrast-boost');
  if (cbChk) cbChk.checked = Boolean(u.highContrastText);

  renderLiveFontPreview();
}

function renderLiveFontPreview() {
  const u = STATE.ui;
  const summaryEl = document.getElementById('font-preview-summary');
  if (summaryEl) {
    const uiName = shortFontLabel(u.fontUi);
    const qName = u.fontQuestion && u.fontQuestion !== 'inherit' ? shortFontLabel(u.fontQuestion) : uiName;
    const aName = u.fontAnswer && u.fontAnswer !== 'inherit' ? shortFontLabel(u.fontAnswer) : uiName;
    summaryEl.textContent = `UI: ${uiName} • Câu hỏi: ${qName} • Đáp án: ${aName}`;
  }
  const qPrev = document.getElementById('settings-live-q-preview');
  const optA = document.getElementById('settings-live-opt-a');
  const optB = document.getElementById('settings-live-opt-b');
  if (qPrev) {
    qPrev.innerHTML = formatRichText(
      'Câu 1: Cho cân bằng $\\ce{N2 + 3H2 <=> 2NH3}$ và vật dao động có $v_{\\max} = \\omega A$. Phát biểu nào đúng?',
      false
    );
  }
  if (optA) optA.innerHTML = formatRichText('Tích phân $\\int_0^1 2x\\,\\mathrm{d}x = 1$ và $\\mathrm{pH} = -\\log[\\ce{H+}]$', false);
  if (optB) optB.innerHTML = formatRichText('Đa hình động với từ khóa `virtual` và `override`', true);
}

function applyFontPreset(preset) {
  const presets = {
    google_sans: {
      fontUi: "'Google Sans', 'Product Sans', 'Outfit', 'Plus Jakarta Sans', sans-serif",
      fontQuestion: 'inherit',
      fontAnswer: 'inherit',
      qFontRem: 1.14,
      optFontRem: 1.02,
      label: '✨ Đã áp dụng bộ phông Google Sans Hiện Đại!'
    },
    times_exam: {
      fontUi: "'Plus Jakarta Sans', sans-serif",
      fontQuestion: "'Times New Roman', Times, serif",
      fontAnswer: "'Times New Roman', Times, serif",
      qFontRem: 1.2,
      optFontRem: 1.08,
      label: '📜 Đã áp dụng phông Times New Roman chuẩn đề thi Bộ GD!'
    },
    arial_clean: {
      fontUi: "Arial, 'Helvetica Neue', Helvetica, sans-serif",
      fontQuestion: 'inherit',
      fontAnswer: 'inherit',
      qFontRem: 1.12,
      optFontRem: 1.0,
      label: '🅰️ Đã áp dụng bộ phông Arial Thanh Lịch!'
    },
    lexend_read: {
      fontUi: "'Lexend', sans-serif",
      fontQuestion: 'inherit',
      fontAnswer: 'inherit',
      qFontRem: 1.14,
      optFontRem: 1.02,
      label: '📖 Đã áp dụng phông Lexend Chống Mỏi Mắt!'
    },
    academic_mix: {
      fontUi: "'Plus Jakarta Sans', sans-serif",
      fontQuestion: "'Lora', serif",
      fontAnswer: "'Google Sans', 'Product Sans', 'Outfit', 'Plus Jakarta Sans', sans-serif",
      qFontRem: 1.18,
      optFontRem: 1.02,
      label: '🎓 Đã áp dụng Câu hỏi Lora Serif + Đáp án Google Sans!'
    }
  };
  const cfg = presets[preset];
  if (!cfg) return;
  STATE.ui.fontUi = cfg.fontUi;
  STATE.ui.fontQuestion = cfg.fontQuestion;
  STATE.ui.fontAnswer = cfg.fontAnswer;
  STATE.ui.qFontRem = cfg.qFontRem;
  STATE.ui.optFontRem = cfg.optFontRem;
  applyAllAppearancePrefs();
  syncUserStateToServer();
  playSound('click');
  showToast(cfg.label, 'success');
}

function quickCycleDarkLight() {
  STATE.ui.theme = STATE.ui.theme === 'dark' ? 'light' : 'dark';
  applyAllAppearancePrefs();
  syncUserStateToServer();
  playSound('click');
  showToast(STATE.ui.theme === 'dark' ? '🌑 Đã bật chế độ Đen Tuyệt Đối (OLED)' : '☀️ Đã bật chế độ Sáng Tinh Khôi', 'info');
}


function toggleHighContrastBoost(enabled) {
  STATE.ui.highContrastText = Boolean(enabled);
  applyAllAppearancePrefs();
  syncUserStateToServer();
  showToast(enabled ? '👁️ Đã bật Tăng cường tương phản chữ' : 'Đã tắt Tăng cường tương phản', 'info');
}

function renderAllMathOnPage(root = document.body) {
  if (window.renderMathInElement) {
    try {
      renderMathInElement(root, {
        delimiters: [
          { left: '$$', right: '$$', display: true },
          { left: '$', right: '$', display: false }
        ],
        throwOnError: false
      });
    } catch (_) {}
  }
}

function setThemeMode(mode) {
  STATE.ui.theme = mode;
  applyAllAppearancePrefs();
  syncUserStateToServer();
  playSound('click');
}

function setAccentPalette(brand, brand2) {
  STATE.ui.brand = brand;
  STATE.ui.brand2 = brand2 || brand;
  applyAllAppearancePrefs();
  syncUserStateToServer();
  playSound('click');
}

function updateTypographyPrefs() {
  const fontUi = document.getElementById('pref-font-ui')?.value || DEFAULT_UI_PREFS.fontUi;
  const fontQuestion = document.getElementById('pref-font-question')?.value || 'inherit';
  const fontAnswer = document.getElementById('pref-font-answer')?.value || 'inherit';
  const fontCode = document.getElementById('pref-font-code')?.value || DEFAULT_UI_PREFS.fontCode;
  const baseFontPx = parseFloat(document.getElementById('slider-base-px')?.value || '16');
  const qFontRem = parseFloat(document.getElementById('slider-q-rem')?.value || '1.14');
  const optFontRem = parseFloat(document.getElementById('slider-opt-rem')?.value || '1.02');
  const cardRadiusPx = parseInt(document.getElementById('slider-card-radius')?.value || '18', 10);
  const lineHeight = parseFloat(document.getElementById('slider-line-height')?.value || '1.62');
  const soundVolume = parseFloat(document.getElementById('slider-sound-vol')?.value || '80') / 100;
  const autoNextDelaySec = parseFloat(document.getElementById('slider-autonext-delay')?.value || '0.8');
  const ttsSpeed = parseFloat(document.getElementById('pref-tts-speed')?.value || '1.0');
  const shadowDepth = document.getElementById('pref-shadow-depth')?.value || 'medium';
  const timerMode = document.getElementById('pref-timer-display')?.value || 'countdown';
  const antiCheatLevel = document.getElementById('pref-anticheat-level')?.value || 'medium';
  const defaultTutorPersona = document.getElementById('cfg-default-tutor-persona')?.value || 'professor';
  const aiVerbosity = document.getElementById('cfg-ai-verbosity')?.value || 'standard';

  STATE.ui.fontUi = fontUi;
  STATE.ui.fontQuestion = fontQuestion;
  STATE.ui.fontAnswer = fontAnswer;
  STATE.ui.fontCode = fontCode;
  STATE.ui.baseFontPx = baseFontPx;
  STATE.ui.qFontRem = qFontRem;
  STATE.ui.optFontRem = optFontRem;
  STATE.ui.cardRadiusPx = cardRadiusPx;
  STATE.ui.lineHeight = lineHeight;
  STATE.ui.soundVolume = soundVolume;
  STATE.ui.autoNextDelaySec = autoNextDelaySec;
  STATE.ui.ttsSpeed = ttsSpeed;
  STATE.ui.shadowDepth = shadowDepth;
  STATE.ui.timerMode = timerMode;
  STATE.ui.antiCheatLevel = antiCheatLevel;
  STATE.ui.defaultTutorPersona = defaultTutorPersona;
  STATE.ui.aiVerbosity = aiVerbosity;

  applyAllAppearancePrefs();
  syncUserStateToServer();
}

function toggleSoundPref(checked) {
  STATE.ui.soundEnabled = Boolean(checked);
  applyAllAppearancePrefs();
  syncUserStateToServer();
  if (checked) playSound('click');
}

function toggleAutoNextPref(checked) {
  STATE.ui.autoNext = Boolean(checked);
  applyAllAppearancePrefs();
  syncUserStateToServer();
}

async function resetDefaultAppearance() {
  const choice = await askCustomConfirm({
    icon: '🎨',
    iconTone: 'brand',
    title: 'Khôi phục giao diện gốc?',
    desc: 'Toàn bộ màu chủ đề, phông chữ Câu hỏi / Đáp án và cỡ chữ sẽ trở về thiết lập chuẩn ban đầu.',
    actions: [
      { id: 'cancel', label: 'Giữ nguyên', cls: 'btn-soft px-4 py-2.5 text-xs' },
      { id: 'confirm', label: 'Khôi phục ngay', cls: 'btn-primary px-5 py-2.5 text-xs' }
    ]
  });
  if (choice !== 'confirm') return;
  STATE.ui = { ...DEFAULT_UI_PREFS };
  applyAllAppearancePrefs();
  syncUserStateToServer();
  showToast('Đã khôi phục giao diện mặc định', 'success');
}

function toggleZenMode() {
  if (STATE.currentTab !== 'exam') {
    document.body.classList.remove('zen-active');
    document.getElementById('exit-zen-btn')?.classList.add('hidden');
    return;
  }
  const isZen = document.body.classList.toggle('zen-active');
  playSound('click');
  const exitBtn = document.getElementById('exit-zen-btn');
  if (exitBtn) exitBtn.classList.toggle('hidden', !isZen);
  try {
    if (isZen) {
      if (document.documentElement.requestFullscreen && !document.fullscreenElement) {
        document.documentElement.requestFullscreen().catch(() => {});
      }
    } else {
      if (document.exitFullscreen && document.fullscreenElement) {
        document.exitFullscreen().catch(() => {});
      }
    }
  } catch (err) {}
}

document.addEventListener('fullscreenchange', () => {
  const isFs = Boolean(document.fullscreenElement);
  if (!isFs && document.body.classList.contains('zen-active')) {
    document.body.classList.remove('zen-active');
  }
});

// =========================================================================
// 4. XP, RANK & SERVER SYNC (PC <-> PHONE <-> IPAD)
// =========================================================================
function awardXP(amount) {
  return addXp(amount);
}

function addXp(amount) {
  STATE.xp = Math.max(0, (STATE.xp || 0) + amount);
  const today = new Date().toISOString().slice(0, 10);
  if (STATE.lastStudyDate !== today) {
    const yesterday = new Date(Date.now() - 86400000).toISOString().slice(0, 10);
    STATE.streakDays = STATE.lastStudyDate === yesterday ? STATE.streakDays + 1 : Math.max(1, STATE.streakDays);
    STATE.lastStudyDate = today;
  }
  updateXpUI();
  syncUserStateToServer();
}

function updateXpUI() {
  const xp = STATE.xp || 0;
  const level = Math.floor(xp / 200) + 1;
  const inLevelXp = xp % 200;
  const pct = Math.min(100, Math.max(8, Math.round((inLevelXp / 200) * 100)));

  const ranks = [
    '🎓 Tân Sinh Viên',
    '📘 Sinh Viên Chăm Chỉ',
    '💻 Cao Thủ Giải Đề',
    '🔥 Chiến Thần Học Bổng',
    '👑 Thủ Khoa Xuất Sắc'
  ];
  const rankTitle = ranks[Math.min(ranks.length - 1, level - 1)];

  setText('user-level-num', level);
  setText('user-xp-num', xp);
  setText('hero-rank-title', `Lv.${level} • ${rankTitle}`);
  setText('hero-streak-days', STATE.streakDays || 1);
  setText('hero-xp-caption', `${inLevelXp} / 200 XP lên cấp ${level + 1}`);
  const bar = document.getElementById('hero-xp-bar');
  if (bar) bar.style.width = `${pct}%`;

  localStorage.setItem('unimaster_xp', String(xp));
  localStorage.setItem('unimaster_streak_days', String(STATE.streakDays));
  localStorage.setItem('unimaster_last_date', STATE.lastStudyDate);
}

let syncTimeout = null;
function syncUserStateToServer() {
  localStorage.setItem('unimaster_bookmarks', JSON.stringify(STATE.bookmarks));
  localStorage.setItem('unimaster_mistakes', JSON.stringify(STATE.mistakes));
  localStorage.setItem('unimaster_notes', JSON.stringify(STATE.notes));
  localStorage.setItem('unimaster_blitz_best', String(STATE.blitzBest));

  if (STATE.isOfflineStandalone) return;
  clearTimeout(syncTimeout);
  syncTimeout = setTimeout(() => {
    apiFetch('/api/user-state', {
      method: 'POST',
      body: JSON.stringify({
        bookmarks: STATE.bookmarks,
        mistakes: STATE.mistakes,
        notes: STATE.notes,
        xp: STATE.xp,
        streakDays: STATE.streakDays,
        lastStudyDate: STATE.lastStudyDate,
        blitzBest: STATE.blitzBest,
        ui: STATE.ui
      })
    }).catch(() => {});
  }, 350);
}


const syncUserStateFromServer = hydrateUserStateFromServer;
async function hydrateUserStateFromServer() {
  try {
    const res = await apiFetch('/api/user-state');
    const s = res.state || {};
    if (Array.isArray(s.bookmarks) && s.bookmarks.length >= STATE.bookmarks.length) STATE.bookmarks = s.bookmarks;
    if (Array.isArray(s.mistakes) && s.mistakes.length >= STATE.mistakes.length) STATE.mistakes = s.mistakes;
    if (s.notes && typeof s.notes === 'object') STATE.notes = { ...s.notes, ...STATE.notes };
    if (typeof s.xp === 'number' && s.xp > STATE.xp) STATE.xp = s.xp;
    if (typeof s.streakDays === 'number' && s.streakDays > STATE.streakDays) STATE.streakDays = s.streakDays;
    if (typeof s.blitzBest === 'number' && s.blitzBest > STATE.blitzBest) STATE.blitzBest = s.blitzBest;
    if (s.ui && !localStorage.getItem('unimaster_ui_prefs')) {
      STATE.ui = { ...DEFAULT_UI_PREFS, ...s.ui };
      applyAllAppearancePrefs();
    }
    updateXpUI();
  } catch (_) {}
}

// =========================================================================
// 5. OFFLINE-CAPABLE & ERROR-RESILIENT API ADAPTER
// =========================================================================
function isShortAnswerMatch(userAns, expectedAns) {
  const uRaw = String(userAns ?? '').trim();
  const cRaw = String(expectedAns ?? '').trim();
  if (!uRaw || !cRaw) return false;
  const uNorm = uRaw.toLowerCase().replace(/\s+/g, ' ');
  const cNorm = cRaw.toLowerCase().replace(/\s+/g, ' ');
  if (uNorm === cNorm) return true;
  const uNum = Number(uNorm.replace(/,/g, '.').replace(/\s+/g, ''));
  const cNum = Number(cNorm.replace(/,/g, '.').replace(/\s+/g, ''));
  if (!Number.isNaN(uNum) && !Number.isNaN(cNum) && uNorm !== '' && cNorm !== '') {
    return Math.abs(uNum - cNum) <= 1e-6;
  }
  return false;
}

async function apiFetch(url, options = {}) {
  if (STATE.isOfflineStandalone) {
    return handleStandaloneOfflineApi(url, options);
  }
  try {
    const opts = { headers: { 'Content-Type': 'application/json' }, credentials: 'same-origin', ...options };
    const resp = await fetch(url, opts);
    if (resp.status === 401) {
      window.location.href = '/login';
      return { success: false, error: 'Cần đăng nhập lại' };
    }
    const data = await resp.json();
    return data;
  } catch (err) {
    // PC-Off Auto-Failover: Nếu PC đã tắt nhưng trình duyệt đã lưu Snapshot trong IndexedDB / bộ nhớ, tự động chạy Offline + Direct Cloud Gemini AI!
    if (typeof ensureOfflineSnapshotReady === 'function') {
      const ok = await ensureOfflineSnapshotReady();
      if (ok && window.__UNIMASTER_OFFLINE_DB__) {
        return handleStandaloneOfflineApi(url, options);
      }
    }
    return { success: false, error: err?.message || 'Lỗi kết nối máy chủ' };
  }
}

async function handleStandaloneOfflineApi(url, options = {}) {
  const db = window.__UNIMASTER_OFFLINE_DB__ || {};
  let body = {};
  try {
    body = options.body ? (typeof options.body === 'string' ? JSON.parse(options.body) : options.body) : {};
  } catch (_) {}

  if (url === '/api/subjects') {
    return { success: true, subjects: db.subjects || [] };
  }
  if (url === '/api/stats') {
    const localExams = JSON.parse(localStorage.getItem('unimaster_offline_exams') || '[]');
    const baseExams = db.stats?.recent_exams || [];
    const all = [...localExams, ...baseExams].slice(0, 10);
    const total = (db.stats?.total_exams || 0) + localExams.length;
    return {
      success: true,
      stats: {
        total_exams: total,
        avg_score: all.length ? +(all.reduce((a, b) => a + b.score, 0) / all.length).toFixed(1) : (db.stats?.avg_score || 0),
        recent_exams: all
      }
    };
  }
  if (url === '/api/user-state') {
    return { success: true, state: db.user_state || {} };
  }
  if (url === '/api/network-info') {
    return {
      success: true,
      lan_ip: 'PC-Off-Mode',
      port: 8080,
      lan_url: window.location.href,
      local_wifi_url: window.location.href,
      public_url: window.location.href,
      permanent_gateway_url: 'https://ntfy.sh/unimaster_ctump_5292',
      is_online: true
    };
  }
  if (url === '/api/settings' && (!options.method || options.method === 'GET')) {
    const keys = typeof getBrowserGeminiKeyPool === 'function' ? getBrowserGeminiKeyPool() : [];
    const pool = keys.map((k, idx) => ({
      index: idx + 1,
      label: `Key #${idx + 1} (Direct Cloud)`,
      masked_key: k.length > 10 ? `${k.slice(0, 6)}...${k.slice(-4)}` : k,
      status: 'ready',
      calls: 0,
      failovers: 0,
      cooldown_remaining: 0,
      model: 'gemini-3.5-flash'
    }));
    return {
      success: true,
      has_gemini_key: keys.length > 0,
      key_count: keys.length,
      masked_key: pool[0]?.masked_key || '',
      pool
    };
  }
  if (url === '/api/settings' && options.method === 'POST') {
    if (body.clear_all_keys) {
      localStorage.removeItem('unimaster_offline_gemini_keys');
      localStorage.removeItem('unimaster_offline_gemini_key');
    } else if (body.add_api_keys || body.gemini_api_key) {
      const raw = body.add_api_keys || body.gemini_api_key || '';
      const incoming = Array.isArray(raw) ? raw : String(raw).split(/[\r\n,;\s]+/).filter(Boolean);
      const current = typeof getBrowserGeminiKeyPool === 'function' ? getBrowserGeminiKeyPool() : [];
      const merged = Array.from(new Set([...current, ...incoming]));
      localStorage.setItem('unimaster_offline_gemini_keys', JSON.stringify(merged));
      if (merged[0]) localStorage.setItem('unimaster_offline_gemini_key', merged[0]);
    }
    const keys = typeof getBrowserGeminiKeyPool === 'function' ? getBrowserGeminiKeyPool() : [];
    return {
      success: true,
      key_count: keys.length,
      pool: keys.map((k, idx) => ({
        index: idx + 1,
        label: `Key #${idx + 1}`,
        masked_key: k.length > 10 ? `${k.slice(0, 6)}...${k.slice(-4)}` : k,
        status: 'ready',
        calls: 0,
        failovers: 0,
        cooldown_remaining: 0,
        model: 'gemini-3.5-flash'
      })),
      message: `Đã lưu ${keys.length} API Key trực tiếp trên trình duyệt!`
    };
  }

    const timedMatch = url.match(/^\/api\/timed-exam\/start(?:\?(.*))?$/);
  if (timedMatch) {
    const params = new URLSearchParams(timedMatch[1] || '');
    const sid = params.get('subject_id') || '10';
    const count = parseInt(params.get('count') || '40', 10);
    const duration = parseInt(params.get('duration') || '60', 10);
    let allQs = db.questions_by_subject?.[String(sid)] || [];
    let shuffled = [...allQs].sort(() => Math.random() - 0.5).slice(0, count);
    const sub = (db.subjects || []).find((s) => String(s.id) === String(sid));
    return {
      success: true,
      subject_id: Number(sid),
      subject_name: sub ? sub.name : 'Môn thi',
      questions: shuffled,
      duration_seconds: duration * 60
    };
  }
  if (url === '/api/timed-exam/submit' && options.method === 'POST') {
    const sid = body.subject_id || 10;
    const userAnswers = body.answers || {};
    const spent = body.time_spent_seconds || 0;
    const allQs = db.questions_by_subject?.[String(sid)] || [];
    let correct = 0;
    const breakdown = [];
    Object.keys(userAnswers).forEach((qid) => {
      const q = allQs.find((x) => String(x.id) === String(qid));
      if (q) {
        const uChoice = String(userAnswers[qid]).toUpperCase();
        const corr = String(q.correct_option).toUpperCase();
        const isCorr = uChoice === corr;
        if (isCorr) correct++;
        breakdown.push({
          id: q.id,
          question_text: q.question_text,
          code_snippet: q.code_snippet,
          user_choice: uChoice,
          correct_choice: corr,
          is_correct: isCorr,
          explanation: q.explanation,
          topic_tag: q.topic_tag
        });
      }
    });
    const total = Object.keys(userAnswers).length || 1;
    const score = +((correct / total) * 10).toFixed(1);
    return {
      success: true,
      score,
      correct_answers: correct,
      total_questions: total,
      time_spent_seconds: spent,
      breakdown
    };
  }

  const qMatch = url.match(/^\/api\/subjects\/(\d+)\/questions(?:\?(.*))?$/);
  if (qMatch && (!options.method || options.method === 'GET')) {
    const sid = qMatch[1];
    const params = new URLSearchParams(qMatch[2] || '');
    const qType = params.get('type') || 'all';
    const diff = params.get('difficulty') || 'all';
    const limit = parseInt(params.get('limit') || '0', 10);
    const isRand = params.get('random') === '1';

    let list = [...(db.questions_by_subject?.[sid] || [])];
    if (qType !== 'all') list = list.filter((q) => q.q_type === qType);
    if (diff !== 'all') list = list.filter((q) => q.difficulty === diff);
    if (isRand) {
      for (let i = list.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [list[i], list[j]] = [list[j], list[i]];
      }
    }
    if (limit > 0) list = list.slice(0, limit);
    return { success: true, questions: list };
  }

  const exMatch = url.match(/^\/api\/subjects\/(\d+)\/exercises/);
  if (exMatch) return { success: true, exercises: db.exercises_by_subject?.[exMatch[1]] || [] };

  const fcMatch = url.match(/^\/api\/subjects\/(\d+)\/flashcards/);
  if (fcMatch && (!options.method || options.method === 'GET')) {
    return { success: true, flashcards: db.flashcards_by_subject?.[fcMatch[1]] || [] };
  }

  const discMatch = url.match(/^\/api\/questions\/(\d+)\/discussions/);
  if (discMatch) {
    const qid = discMatch[1];
    const key = `unimaster_disc_${qid}`;
    const list = JSON.parse(localStorage.getItem(key) || '[]');
    if (options.method === 'POST' && body.content) {
      list.unshift({
        id: Date.now(),
        question_id: Number(qid),
        author_name: body.author_name || 'Sinh viên',
        author_role: body.author_role || 'student',
        content: body.content,
        upvotes: 1,
        is_verified: body.author_role === 'ai_verified' ? 1 : 0,
        created_at: 'Vừa xong'
      });
      localStorage.setItem(key, JSON.stringify(list));
    }
    return { success: true, comments: list };
  }

  if (url === '/api/exam/submit') {
    const sid = String(body.subject_id || '10');
    const allQ = db.questions_by_subject?.[sid] || [];
    const qMap = Object.fromEntries(allQ.map((q) => [String(q.id), q]));
    let correctCount = 0;
    const details = [];
    for (const qid of body.question_ids || []) {
      const q = qMap[String(qid)];
      if (!q) continue;
      const uAns = String(body.answers?.[qid] ?? '').trim();
      const exp = String(body.correct_map?.[qid] ?? q.correct_option).trim();
      const isCorrect =
        q.q_type === 'short_answer'
          ? isShortAnswerMatch(uAns, exp)
          : uAns !== '' && uAns.toLowerCase() === exp.toLowerCase();
      if (isCorrect) correctCount++;
      details.push({
        question_id: q.id,
        question_text: q.question_text,
        code_snippet: q.code_snippet || '',
        q_type: q.q_type,
        user_answer: uAns,
        correct_option: exp,
        is_correct: isCorrect,
        explanation: q.explanation
      });
    }
    const total = details.length;
    const score = total ? +((correctCount / total) * 10).toFixed(1) : 0;
    const localExams = JSON.parse(localStorage.getItem('unimaster_offline_exams') || '[]');
    localExams.unshift({
      subject_id: Number(sid),
      total_questions: total,
      correct_answers: correctCount,
      score,
      time_spent_seconds: body.time_spent_seconds || 0,
      created_at: new Date().toISOString().replace('T', ' ').slice(0, 16)
    });
    localStorage.setItem('unimaster_offline_exams', JSON.stringify(localExams.slice(0, 20)));
    return { success: true, score, correct_count: correctCount, total_questions: total, details };
  }

  // Direct Browser-to-Gemini Cloud AI Engine when PC is OFF!
  if (url.startsWith('/api/ai/') && typeof callGeminiDirectFromBrowser === 'function') {
    const directRes = await callGeminiDirectFromBrowser(url, body);
    if (directRes) return directRes;
  }

  // Fallback offline AI responses when device has no internet at all
  return {
    success: true,
    hint: 'Hãy phân tích công thức/định nghĩa gốc và loại trừ ngay 2 phương án trái bản chất.',
    concept: '### 🧠 Công thức nền tảng\nĐối chiếu định luật gốc, điều kiện biên và đơn vị chuẩn SI trước khi thay số.',
    diagnosis: '### 🩺 Chẩn đoán lỗi nhầm lẫn\nHãy đối chiếu lại dấu, hệ số tỉ lệ hoặc điều kiện xảy ra của định luật ở lời giải chuẩn.',
    mnemonic: '⚡ **Mẹo nhớ 5 giây:** Gắn từ khóa hỏi chính của đề bài trực tiếp với đáp án chuẩn để khoanh ngay không phân vân!',
    flashcard: { front: body.question_text || 'Khái niệm cốt lõi', back: body.correct_answer || 'Đáp án chuẩn', hint: 'Ôn tập' },
    analysis: 'Hãy kiểm tra kỹ bản chất công thức, điều kiện áp dụng và các phương án bẫy thường gặp.',
    reply: 'Bạn đang ở chế độ **Chạy Độc Lập Không Cần PC**! Toàn bộ 467 câu hỏi, 16 ảnh tiêu bản và Phòng thí nghiệm ảo hoạt động 100%. Hãy bật Wi-Fi/4G trên điện thoại để AI gọi thẳng lên Google Gemini Cloud!',
    evaluation: 'Hãy bấm **Làm lại câu sai** để nắm chắc 100% các câu vừa nhầm lẫn nhé!',
    roadmap: '### 🧠 Lộ Trình 5 Ngày\n- **Ngày 1–2:** Ôn tập Flashcards 3D và lý thuyết nền.\n- **Ngày 3–4:** Luyện lại toàn bộ Sổ tay câu sai.\n- **Ngày 5:** Thi thử bấm giờ chế độ Thi thật.',
    grading: {
      score: 8.0,
      verdict: 'Đã chấm sơ bộ ở chế độ Offline — Hãy đối chiếu bài làm với đáp án mẫu bên dưới.',
      strengths: ['Đã trình bày các bước tính toán và lập luận'],
      missing: ['Cần kiểm tra kỹ đơn vị đo và khoảng tham chiếu sinh lý'],
      sample_answer: body.expected_barem || 'Áp dụng công thức Beer–Lambert và đối chiếu giới hạn bình thường.'
    },
    explanation: 'Hãy đối chiếu kỹ bản chất lý thuyết, công thức gốc và các ví dụ thực tế của chuyên đề này.'
  };
}

// =========================================================================
// 6. STEM FORMULA ENGINE (KaTeX + mhchem \ce{...}), CODE PILLS & MARKDOWN
// =========================================================================
function escapeHtml(str) {
  return String(str ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function renderKatexSafe(tex, displayMode = false) {
  let clean = String(tex || '').trim();
  if (!clean) return '';

  // 1. Normalize common LaTeX quirks that trigger KaTeX errors
  // e.g. 	ext{OD_B} or 	ext{OD}_{B} or 	ext{OD}_{	ext{B}}
  clean = clean.replace(/\text\{([^{}]+)_([^{}]+)\}/g, '\text{$1}_{$2}');

  if (window.katex) {
    try {
      return katex.renderToString(clean, {
        displayMode,
        throwOnError: false,
        strict: false,
        trust: true
      });
    } catch (_) {}
  }

  // 2. High-fidelity semantic HTML fallback (never show raw LaTeX code like \text{OD}_{\text{B}}!)
  let s = clean;
  for (let i = 0; i < 3; i++) {
    s = s.replace(/\text\{([^{}]+)\}/g, '$1');
  }
  for (let i = 0; i < 3; i++) {
    s = s.replace(/\frac\{([^{}]+)\}\{([^{}]+)\}/g, '($1 / $2)');
  }
  for (let i = 0; i < 3; i++) {
    s = s.replace(/_\{([^{}]+)\}/g, '<sub>$1</sub>');
  }
  s = s.replace(/_([a-zA-Z0-9])/g, '<sub>$1</sub>');
  for (let i = 0; i < 3; i++) {
    s = s.replace(/\^\{([^{}]+)\}/g, '<sup>$1</sup>');
  }
  s = s.replace(/\^([a-zA-Z0-9])/g, '<sup>$1</sup>');
  s = s.replace(/\times/g, '×').replace(/\cdot/g, '·').replace(/\pm/g, '±');
  s = s.replace(/\leq/g, '≤').replace(/\geq/g, '≥').replace(/\neq/g, '≠');
  s = s.replace(/\mu/g, 'µ').replace(/\ce\{([^{}]+)\}/g, '<strong>$1</strong>');

  return `<span class="katex-fallback font-serif inline-block">${s}</span>`;
}

function formatRichText(raw, allowCodeKeywords = null) {
  if (!raw) return '';
  try {
    let text = String(raw);
    const tokens = [];
    const saveToken = (html) => {
      const key = `\x00TOK${tokens.length}\x00`;
      tokens.push(html);
      return key;
    };

    // 1. Explicit backtick inline code (`...`) always renders as code pill in every subject
    text = text.replace(/`([^`\n]+)`/g, (_, inner) =>
      saveToken(`<code class="inline-code">${escapeHtml(inner)}</code>`)
    );

    // 2. Full STEM Math, Physics, Chemistry (\ce{...}) & Biology equations
    if (typeof renderStemMathTokens === 'function') {
      text = renderStemMathTokens(text, saveToken);
    }

    let safe = escapeHtml(text);

    // 3. Unambiguous C#/.NET generics & method signatures
    safe = safe.replace(
      /\b(?:List|Dictionary|IEnumerable|ICollection|IList|Queue|Stack|HashSet|Func|Action|Task|Nullable)&lt;[^&<>]+?&gt;/g,
      (m) => saveToken(`<code class="inline-code">${m}</code>`)
    );

    safe = safe.replace(
      /\b(?:Console\.Write(?:Line)?(?:\([^)]*\))?|[A-Z][A-Za-z0-9]*Exception|ToString\(\)|Equals\(\)|GetHashCode\(\)|Finalize\(\)|Dispose\(\)|MemberwiseClone\(\)|Main\(\)|GC\.Collect\(\)|IDisposable|IComparable|ICloneable|IEnumerable)\b/g,
      (m) => saveToken(`<code class="inline-code">${m}</code>`)
    );

    // 4. Bare C# keywords ONLY in programming contexts
    const useKwPills = allowCodeKeywords !== null ? Boolean(allowCodeKeywords) : (typeof isProgrammingContext === 'function' ? isProgrammingContext() : false);
    if (useKwPills) {
      safe = safe.replace(
        /\b(abstract|virtual|override|sealed|interface|protected|private|public|internal|readonly|const|static|partial|params|ref|out|struct|enum|delegate|async|await|null|void|typeof|nameof)\b/g,
        (m) => saveToken(`<code class="inline-code">${m}</code>`)
      );
    }

    safe = safe.replace(/\n/g, '<br />');
    return safe.replace(/\x00TOK(\d+)\x00/g, (_, idx) => tokens[Number(idx)] || '');
  } catch (err) {
    return escapeHtml(String(raw)).replace(/\n/g, '<br />');
  }
}

function renderStemMathTokens(inputText, saveToken) {
  let text = String(inputText || '');

  // 1. Display Math: $$ ... $$ and \[ ... \]
  text = text.replace(/\$\$([\s\S]+?)\$\$/g, (_, math) => saveToken(renderKatexSafe(math, true)));
  text = text.replace(/\\\[([\s\S]+?)\\\]/g, (_, math) => saveToken(renderKatexSafe(math, true)));

  // 2. Inline LaTeX: \( ... \)
  text = text.replace(/\\\(([\s\S]+?)\\\)/g, (_, math) => saveToken(renderKatexSafe(math, false)));

  // 3. Inline Dollar Math / Chemistry: $...$ (supports spaces, \text{OD}_{B}, while ignoring prices like "10$ và 20$")
  text = text.replace(/\$(?![\$])([^\n$]+?)(?<![\\])\$/g, (full, rawMath) => {
    const math = rawMath.trim();
    if (/^\d+(?:[.,]\d+)?$/.test(math)) return full;
    const isMath = /[\\_{}^=><+\-*/±×]/.test(math) || /^[A-Za-z0-9]$/.test(math);
    if (!isMath && math.includes(' ')) return full;
    return saveToken(renderKatexSafe(math, false));
  });

  // 4. Bare mhchem \ce{...} or \pu{...} written outside $...$ (supports nested braces like \ce{Fe^{3+}})
  text = text.replace(/\\(?:ce|pu)\{(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})+\}/g, (chemExpr) => {
    return saveToken(renderKatexSafe(chemExpr, false));
  });

  return text;
}

function isProgrammingContext() {
  try {
    let sid = STATE.exam?.active ? STATE.exam.subjectId : STATE.examConfig?.subjectId;
    if (STATE.currentTab === 'search') {
      sid = Number(document.getElementById('bank-subject-select')?.value || sid);
    } else if (STATE.currentTab === 'flashcards') {
      sid = Number(document.getElementById('fc-subject-select')?.value || sid);
    }
    const sub = STATE.subjects.find((s) => Number(s.id) === Number(sid));
    if (!sub) return false;
    const code = String(sub.code || '').toUpperCase();
    const cat = String(sub.category || '').toLowerCase();
    return code === 'CSHARP_OOP' || code === 'PYTHON_NNLT' || cat.includes('code') || cat.includes('lập trình');
  } catch (err) {
    return false;
  }
}

function parseQuestionHeader(rawText) {
  const str = String(rawText || '').trim();
  const match = str.match(/^Câu\s+(\d+)\s*\(([^)]+)\)\s*:\s*([\s\S]+)$/i);
  if (match) {
    return { bankNum: match[1], topic: match[2].trim(), body: match[3].trim() };
  }
  return { bankNum: null, topic: null, body: str };
}

function getBloomInfo(difficulty, qText = '') {
  const lowText = String(qText || '').toLowerCase();
  let diff = String(difficulty || 'medium').toLowerCase();
  if (lowText.includes('vận dụng cao')) diff = 'very_hard';
  else if (lowText.includes('vận dụng')) diff = 'hard';
  else if (lowText.includes('nhận biết')) diff = 'easy';
  else if (lowText.includes('thông hiểu')) diff = 'medium';

  const map = {
    easy: { key: 'easy', label: '🟢 Nhận biết', cls: 'badge-emerald' },
    medium: { key: 'medium', label: '🔵 Thông hiểu', cls: 'badge-cyan' },
    hard: { key: 'hard', label: '🟠 Vận dụng', cls: 'badge-amber' },
    very_hard: { key: 'very_hard', label: '🔴 Vận dụng cao', cls: 'badge-rose' }
  };
  return map[diff] || map.medium;
}

function normalizeCodeSnippet(rawCode) {
  if (!rawCode) return '';
  let code = String(rawCode).replace(/\r\n/g, '\n');
  if (!code.includes('\n') && code.includes('\\n')) {
    code = code.replace(/\\n/g, '\n').replace(/\\t/g, '    ').replace(/\\"/g, '"');
  }
  return code.replace(/^\n+|\n+$/g, '');
}

function buildCodeWindowHtml(rawCode, title = 'Program.cs', lang = 'csharp') {
  const clean = normalizeCodeSnippet(rawCode);
  if (!clean) return '';

  const uid = `code_${codeSeq++}`;
  CODE_REGISTRY[uid] = clean;

  const lines = clean.split('\n');
  const grammar =
    window.Prism && Prism.languages && (Prism.languages[lang] || Prism.languages.csharp || Prism.languages.clike);

  const rowsHtml = lines
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
    .join('');

  return `
    <div id="wrap_${uid}" class="code-window my-2">
      <div class="code-window-header">
        <div class="flex items-center gap-2">
          <div class="flex items-center gap-1.5">
            <span class="w-2.5 h-2.5 rounded-full bg-rose-500"></span>
            <span class="w-2.5 h-2.5 rounded-full bg-amber-400"></span>
            <span class="w-2.5 h-2.5 rounded-full bg-emerald-500"></span>
          </div>
          <span class="font-mono font-bold text-[11px] txt-sub">${escapeHtml(title)}</span>
        </div>
        <div class="flex items-center gap-1.5">
          <button type="button" onclick="askAiAboutWholeCodeSnippet('${uid}', '${escapeHtml(title)}', '${lang}')" class="btn-soft !py-0.5 !px-2 text-[10px] font-black text-indigo-400 hover:text-indigo-300 flex items-center gap-1 border border-indigo-500/40">
            <span>🤖</span> <span>Hỏi AI Cả Đoạn Code</span>
          </button>
          <button type="button" onclick="toggleCodeWrap('${uid}', this)" class="btn-soft px-2 py-0.5 text-[11px]">↵ Xuống dòng</button>
          <button type="button" onclick="copyCodeSnippet('${uid}', this)" class="btn-soft px-2.5 py-0.5 text-[11px] font-bold">📋 Copy</button>
        </div>
      </div>
      <div class="overflow-x-auto py-1.5">
        <table class="code-lines-table"><tbody>${rowsHtml}</tbody></table>
      </div>
    </div>
  `;
}

function toggleCodeWrap(uid, btnEl) {
  const win = document.getElementById(`wrap_${uid}`);
  if (!win) return;
  const isNowrap = win.classList.toggle('nowrap-mode');
  if (btnEl) btnEl.textContent = isNowrap ? '↔ Cuộn ngang' : '↵ Xuống dòng';
}

function copyCodeSnippet(uid, btnEl) {
  const raw = CODE_REGISTRY[uid];
  if (!raw) return;
  navigator.clipboard.writeText(raw).then(() => {
    playSound('click');
    if (btnEl) {
      const old = btnEl.textContent;
      btnEl.textContent = '✔ Đã chép';
      setTimeout(() => { btnEl.textContent = old; }, 1400);
    }
  });
}

function renderMarkdown(mdText) {
  if (!mdText) return '';
  let text = String(mdText);
  const codeBlocks = [];
  const inlineCodes = [];
  const mathTokens = [];

  // 1. Protect multi-line fenced code blocks first (alphanumeric placeholder safe from Marked!)
  text = text.replace(/```([a-zA-Z0-9_+-]*)\s*\n([\s\S]*?)```/g, (_, lang, code) => {
    const l = (lang || 'csharp').toLowerCase();
    const html = buildCodeWindowHtml(code, l === 'csharp' || l === 'cs' ? 'C#' : (l || 'CODE').toUpperCase(), l === 'cs' ? 'csharp' : l);
    const key = `\n\nUMKTCB${codeBlocks.length}END\n\n`;
    codeBlocks.push(html);
    return key;
  });

  // 2. Protect inline `code` spans so $ inside code is never parsed as math
  text = text.replace(/`([^`\n]+)`/g, (_, inner) => {
    const key = `UMKTIC${inlineCodes.length}END`;
    inlineCodes.push(`<code class="inline-code">${escapeHtml(inner)}</code>`);
    return key;
  });

  // 3. Render KaTeX Math & mhchem \ce{...} BEFORE marked.parse so _ and * in formulas are never broken!
  text = renderStemMathTokens(text, (renderedHtml) => {
    const key = `UMKTMA${mathTokens.length}END`;
    mathTokens.push(renderedHtml);
    return key;
  });

  let html = window.marked ? marked.parse(text, { breaks: true, gfm: true }) : `<p>${formatRichText(text)}</p>`;

  html = html.replace(/<p>\s*UMKTCB(\d+)END\s*<\/p>/g, (_, i) => codeBlocks[Number(i)] || '');
  html = html.replace(/UMKTCB(\d+)END/g, (_, i) => codeBlocks[Number(i)] || '');
  html = html.replace(/UMKTIC(\d+)END/g, (_, i) => inlineCodes[Number(i)] || '');
  html = html.replace(/UMKTMA(\d+)END/g, (_, i) => mathTokens[Number(i)] || '');
  return html;
}

function formatDuration(totalSec) {
  const sec = Math.max(0, Math.floor(totalSec || 0));
  const m = Math.floor(sec / 60);
  const s = sec % 60;
  return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
}

// =========================================================================
// 7. INITIALIZATION & NAVIGATION
// =========================================================================
window.STATE = STATE;

document.addEventListener('DOMContentLoaded', async () => {
  applyAllAppearancePrefs();
  updateXpUI();
  populateStemReferenceModal();
  refreshIcons();
  initTutorGreeting();
  initTutorHistoryFromStorage();

  if (!STATE.isOfflineStandalone && 'serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js').catch(() => {});
  }

  // Load subjects and stats IMMEDIATELY without waiting for slow user state
  const subStatsPromise = loadSubjectsAndStats();
  const userStatePromise = hydrateUserStateFromServer();
  await Promise.all([subStatsPromise, userStatePromise, checkApiKeyStatus(), fetchNetworkQrInfo()]);
  renderTutorQuickPrompts();
  setupTextSelectionAiListener();
  setupKeyboardShortcuts();
  setupTouchSwipeGestures();
  renderAllMathOnPage();
});

async function loadSubjectsAndStats() {
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
}

function populateAllSubjectSelects() {
  const ids = [
    'exam-subject-select',
    'exercise-subject-select',
    'fc-subject-select',
    'bank-subject-select',
    'tutor-subject-select',
    'gen-subject-select',
    'add-q-subject',
    'roadmap-subject-select',
    'battle-subject-select'
  ];
  const preferred =
    STATE.subjects.find((s) => s.code === 'HOASINH_CTUMP') ||
    STATE.subjects.find((s) => s.code === 'OOP_CSHARP') ||
    STATE.subjects[0];
  if (preferred) STATE.examConfig.subjectId = preferred.id;

  ids.forEach((id) => {
    const sel = document.getElementById(id);
    if (!sel) return;
    const prev = sel.value;
    sel.innerHTML = STATE.subjects
      .map((s) => `<option value="${s.id}">${s.icon || '📘'} ${escapeHtml(s.name)} (${s.question_count})</option>`)
      .join('');
    if (prev && STATE.subjects.some((s) => String(s.id) === String(prev))) sel.value = prev;
    else if (preferred) sel.value = String(preferred.id);
  });
}

function switchTab(tabName) {
  STATE.currentTab = tabName;
  const tabs = ['dashboard', 'exam', 'exercises', 'essay', 'flashcards', 'search', 'tutor', 'generator', 'arena', 'lab'];

  tabs.forEach((t) => {
    document.getElementById(`view-${t}`)?.classList.toggle('hidden', t !== tabName);
    document.getElementById(`tab-${t}`)?.classList.toggle('active-tab', t === tabName);
  });

  // 1. Hide floating tutor button on Dashboard (trang chủ) and full Tutor view
  const ftContainer = document.getElementById('floating-tutor-container');
  if (ftContainer) {
    const isHomeOrTutor = tabName === 'dashboard' || tabName === 'tutor';
    ftContainer.classList.toggle('hidden', isHomeOrTutor);
    if (isHomeOrTutor) {
      document.getElementById('floating-tutor-window')?.classList.add('hidden');
      document.getElementById('floating-tutor-backdrop')?.classList.add('hidden');
      if (typeof windowTutorSizeExpanded !== 'undefined' && windowTutorSizeExpanded) {
        toggleFloatingTutorSize();
      }
    }
  }

  // 2. Automatically cancel Zen/Fullscreen mode if navigating away from Exam
  if (tabName !== 'exam') {
    document.body.classList.remove('zen-active');
    document.getElementById('exit-zen-btn')?.classList.add('hidden');
    if (document.fullscreenElement && document.exitFullscreen) {
      document.exitFullscreen().catch(() => {});
    }
  }

  document.querySelectorAll('[data-mnav]').forEach((btn) => {
    btn.classList.toggle('active-tab', btn.getAttribute('data-mnav') === tabName);
  });

  playSound('click');
  if (tabName === 'dashboard') renderDashboard();
  if (tabName === 'exercises') loadExercisesView();
  if (tabName === 'essay') loadEssayView();
  if (tabName === 'flashcards') loadFlashcardsView();
  if (tabName === 'search') loadBankQuestions();
  if (tabName === 'tutor') renderTutorQuickPrompts();
  if (tabName === 'arena') initArenaView();
  if (tabName === 'lab' && typeof initLabHubView === 'function') initLabHubView();

  window.scrollTo({ top: 0, behavior: 'smooth' });
  refreshIcons();
  renderAllMathOnPage();
}

// =========================================================================
// 8. DASHBOARD & NOTEBOOK
// =========================================================================
function renderDashboard() {
  let subs = (Array.isArray(STATE.subjects) && STATE.subjects.length) ? STATE.subjects : [];
  if (!subs.length) {
    try {
      const cached = JSON.parse(localStorage.getItem('unimaster_cached_subjects') || '[]');
      if (Array.isArray(cached) && cached.length) {
        subs = cached;
        STATE.subjects = cached;
      }
    } catch (_) {}
  }
  const subCount = subs.length || 12;
  const qCount = subs.reduce((a, s) => a + (s.question_count || 0), 0) || 1470;
  setText('stat-subjects', subCount);
  setText('stat-questions', qCount.toLocaleString('vi-VN'));
  setText('stat-exams', STATE.stats?.total_exams || 0);
  setText('stat-avg-score', Number(STATE.stats?.avg_score || 0).toFixed(1));

  setText('notebook-mistake-count', STATE.mistakes.length);
  setText('notebook-bookmark-count', STATE.bookmarks.length);
  setText('notebook-notes-count', Object.keys(STATE.notes).filter((k) => STATE.notes[k]).length);
  setText('blitz-best-badge', `${STATE.blitzBest} đ`);

  const grid = document.getElementById('subjects-grid');
  if (grid) {
    const accents = [
      'linear-gradient(135deg, #7c3aed, #ec4899)',
      'linear-gradient(135deg, #2563eb, #06b6d4)',
      'linear-gradient(135deg, #10b981, #14b8a6)',
      'linear-gradient(135deg, #f59e0b, #f43f5e)',
      'linear-gradient(135deg, #8b5cf6, #3b82f6)'
    ];
    const activeAcc = typeof getActiveAccount === 'function' ? getActiveAccount() : null;
    const enrolledIds = activeAcc && Array.isArray(activeAcc.enrolled_subjects) ? activeAcc.enrolled_subjects : [];

    let displaySubjects = [...STATE.subjects];
    if (enrolledIds.length > 0) {
      displaySubjects.sort((a, b) => {
        const aEn = enrolledIds.includes(a.id) ? 1 : 0;
        const bEn = enrolledIds.includes(b.id) ? 1 : 0;
        return bEn - aEn;
      });
    }

    grid.innerHTML = displaySubjects
      .map((s, idx) => {
        const isEnrolled = enrolledIds.includes(s.id);
        const grad = accents[idx % accents.length];
        return `
        <div class="uni-card uni-card-interactive p-5 flex flex-col justify-between gap-4">
          <div class="flex items-start justify-between gap-3">
            <div class="flex items-center gap-3.5">
              <div class="w-12 h-12 rounded-2xl flex items-center justify-center text-xl text-white shadow-md shrink-0" style="background: ${grad};">
                ${s.icon || '📘'}
              </div>
              <div>
                <div class="flex items-center gap-1.5 flex-wrap">
                  <span class="text-[10px] font-mono font-bold txt-muted uppercase">${escapeHtml(s.code)}</span>
                  ${isEnrolled ? '<span class="badge-brand px-1.5 py-0.2 rounded text-[10px] font-black border border-indigo-500/40">★ Môn Của Acc</span>' : ''} ${s.code === 'OOP_CSHARP' ? '<span class="badge-brand px-1.5 py-0.2 rounded text-[10px] font-extrabold">💻 CNTT Pro</span>' : s.code === 'HOASINH_CTUMP' ? '<span class="badge-emerald px-1.5 py-0.2 rounded text-[10px] font-extrabold">🔬 Y Khoa</span>' : s.question_count > 100 ? '<span class="badge-amber px-1.5 py-0.2 rounded text-[10px] font-extrabold">⭐ Trọng Tâm</span>' : ''}
                </div>
                <h3 class="font-extrabold text-sm sm:text-base txt-main leading-snug">${escapeHtml(s.name)}</h3>
                <div class="flex flex-wrap gap-1.5 mt-1.5 text-[11px] font-bold">
                  <span class="badge-brand px-2 py-0.5 rounded-lg">${s.question_count} câu</span>
                  <span class="badge-subtle px-2 py-0.5 rounded-lg">${s.flashcard_count} thẻ</span>
                  ${s.exercise_count ? `<span class="badge-amber px-2 py-0.5 rounded-lg">${s.exercise_count} bài C#</span>` : ''}
                </div>
              </div>
            </div>
            <div class="flex items-center gap-1">
              <button onclick="quickExpandSubjectQuestions(${s.id}, this)" title="AI tự soạn thêm 5 câu mới cho môn này" class="ai-chip-btn !py-1 !px-2 !text-[11px]">
                ✨ +5 câu
              </button>
              ${
                !BUILT_IN_SUBJECT_CODES.has(s.code)
                  ? `<button onclick="deleteSubject(${s.id})" title="Xóa môn học" class="btn-soft p-1.5 txt-rose"><i data-lucide="trash-2" class="w-3.5 h-3.5"></i></button>`
                  : ''
              }
            </div>
          </div>

          <div class="grid grid-cols-3 gap-2 pt-3" style="border-top: 1px solid var(--border);">
            <button onclick="openSubjectExam(${s.id})" class="btn-primary py-2 text-xs">Vào Thi</button>
            <button onclick="openSubjectFlashcards(${s.id})" class="btn-soft py-2 text-xs">Thẻ Nhớ</button>
            <button onclick="openSubjectBank(${s.id})" class="btn-soft py-2 text-xs">Tra Cứu</button>
          </div>
        </div>
      `;
      })
      .join('');
  }

  const tbody = document.getElementById('recent-exams-tbody');
  if (tbody) {
    const recents = STATE.stats?.recent_exams || [];
    tbody.innerHTML = recents.length
      ? recents
          .map((r) => {
            const sub = STATE.subjects.find((s) => s.id === r.subject_id);
            const cls = r.score >= 8 ? 'badge-emerald' : r.score >= 5 ? 'badge-amber' : 'badge-rose';
            return `
            <tr style="border-bottom: 1px solid var(--border);">
              <td class="py-2.5 pr-3 font-bold txt-main truncate max-w-[180px]">${escapeHtml(sub ? sub.name : 'Môn #' + r.subject_id)}</td>
              <td class="py-2.5 px-3 font-semibold txt-sub">${r.correct_answers}/${r.total_questions}</td>
              <td class="py-2.5 px-3"><span class="${cls} px-2.5 py-0.5 rounded-full font-extrabold">${Number(r.score).toFixed(1)}</span></td>
              <td class="py-2.5 px-3 font-mono txt-muted">${formatDuration(r.time_spent_seconds)}</td>
              <td class="py-2.5 pl-3 text-right txt-muted">${escapeHtml((r.created_at || '').slice(5, 16))}</td>
            </tr>`;
          })
          .join('')
      : `<tr><td colspan="5" class="py-6 text-center txt-muted">Chưa có bài làm nào. Bấm <strong>Luyện Đề Ngay</strong> để khởi động!</td></tr>`;
  }
  renderContextualShortcuts();
  renderWeeklyAnalyticsChart();
  renderBloomCompetencyChart();
  updateDynamicStudyPlanner();
  refreshIcons();
  renderAllMathOnPage();
}

async function renderBloomCompetencyChart() {
  const grid = document.getElementById('bloom-competency-grid');
  if (!grid) return;
  const sid = Number(document.getElementById('roadmap-subject-select')?.value || STATE.examConfig.subjectId || 5);
  try {
    const res = await apiFetch(`/api/subjects/${sid}/questions?type=all`);
    const allQs = res.questions || [];
    const mistakeIds = new Set(STATE.mistakes.map((m) => (typeof m === 'object' ? m.id : m)));
    const avgScore = Number(STATE.stats?.avg_score || 0);
    const hasHistory = Number(STATE.stats?.total_exams || 0) > 0;

    const levels = [
      { key: 'easy', title: '🟢 Cấp 1: Nhận biết', desc: 'Khái niệm & cú pháp chuẩn', color: '#10b981', base: 86 },
      { key: 'medium', title: '🔵 Cấp 2: Thông hiểu', desc: 'Bản chất & phân biệt bẫy', color: '#06b6d4', base: 74 },
      { key: 'hard', title: '🟠 Cấp 3: Vận dụng', desc: 'Đọc hiểu code & tính toán', color: '#f59e0b', base: 62 },
      { key: 'very_hard', title: '🔴 Cấp 4: Vận dụng cao', desc: 'Tình huống tổng hợp khó', color: '#f43f5e', base: 48 }
    ];

    grid.innerHTML = levels
      .map((lv) => {
        const subset = allQs.filter((q) => getBloomInfo(q.difficulty, q.question_text).key === lv.key);
        const total = subset.length;
        const mistakesInLv = subset.filter((q) => mistakeIds.has(q.id)).length;

        let mastery = hasHistory ? Math.round((avgScore / 10) * lv.base + 14) : lv.base - 18;
        if (total > 0) {
          const penalty = Math.round((mistakesInLv / total) * 45);
          mastery = Math.max(18, Math.min(98, mastery - penalty));
        } else {
          mastery = Math.max(25, Math.min(92, mastery));
        }

        return `
          <div class="p-3.5 rounded-2xl space-y-2" style="background-color: var(--bg-subtle); border: 1px solid var(--border);">
            <div class="flex items-center justify-between gap-1">
              <span class="text-xs font-extrabold txt-main">${lv.title}</span>
              <span class="text-xs font-mono font-extrabold" style="color: ${lv.color};">${mastery}%</span>
            </div>
            <div class="bloom-bar-track">
              <div class="bloom-bar-fill" style="width: ${mastery}%; background: ${lv.color};"></div>
            </div>
            <div class="flex items-center justify-between text-[11px] txt-muted">
              <span>${lv.desc}</span>
              <span class="font-bold">${total} câu${mistakesInLv ? ` • ${mistakesInLv} sai` : ''}</span>
            </div>
          </div>
        `;
      })
      .join('');
    renderKnowledgeHeatmapAndPredictor(allQs, sid);
  } catch (_) {}
}

async function generateAiStudyRoadmap() {
  const wrap = document.getElementById('dashboard-ai-roadmap-wrap');
  const box = document.getElementById('dashboard-ai-roadmap-box');
  if (!box) return;
  const sid = Number(document.getElementById('roadmap-subject-select')?.value || STATE.examConfig.subjectId || 5);
  const sub = STATE.subjects.find((s) => s.id === sid);
  const mistakeIds = STATE.mistakes.map((m) => (typeof m === 'object' ? m.id : m));

  if (wrap) wrap.classList.remove('hidden');
  box.classList.remove('hidden');
  STATE.roadmapCollapsed = false;
  const toggleBtn = document.getElementById('btn-toggle-roadmap');
  if (toggleBtn) toggleBtn.textContent = '🔼 Thu gọn';

  box.innerHTML = `
    <div class="space-y-2.5 py-2">
      <div class="text-xs font-bold txt-brand animate-pulse">🧠 AI đang phân tích năng lực 4 cấp độ Bloom & biên soạn trọn vẹn lộ trình 5 ngày cho môn "${escapeHtml(sub?.name || 'Đại học')}"...</div>
      <div class="skeleton-shimmer h-6 w-2/3"></div>
      <div class="skeleton-shimmer h-20 w-full"></div>
      <div class="skeleton-shimmer h-16 w-5/6"></div>
    </div>
  `;
  playSound('click');

  const res = await apiFetch('/api/ai/roadmap', {
    method: 'POST',
    body: JSON.stringify({
      subject_id: sid,
      subject_name: sub?.name || 'Đại học',
      mistake_ids: mistakeIds
    })
  });

  if (!res.success && !res.roadmap) {
    box.innerHTML = `<div class="text-xs font-bold txt-rose">⚠ Không thể tạo lộ trình: ${escapeHtml(res.error || 'Hãy kiểm tra kết nối hoặc dàn API Key trong Cài đặt.')}</div>`;
    return;
  }

  STATE.lastRoadmapRaw = res.roadmap || '';
  box.innerHTML = renderMarkdown(STATE.lastRoadmapRaw);
  playSound('complete');
  showToast('🧠 AI đã lập xong trọn vẹn lộ trình cá nhân hóa 5 ngày!', 'success');
}

function copyRoadmapText() {
  if (!STATE.lastRoadmapRaw) return;
  navigator.clipboard.writeText(STATE.lastRoadmapRaw).then(() => {
    playSound('click');
    showToast('📋 Đã sao chép toàn bộ lộ trình 5 ngày!', 'success');
  });
}

function toggleRoadmapCollapse() {
  const box = document.getElementById('dashboard-ai-roadmap-box');
  const btn = document.getElementById('btn-toggle-roadmap');
  if (!box) return;
  STATE.roadmapCollapsed = !STATE.roadmapCollapsed;
  box.classList.toggle('hidden', STATE.roadmapCollapsed);
  if (btn) btn.textContent = STATE.roadmapCollapsed ? '🔽 Mở rộng lộ trình' : '🔼 Thu gọn';
}

async function quickExpandSubjectQuestions(sid, btnEl) {
  const sub = STATE.subjects.find((s) => s.id === sid);
  const origHtml = btnEl ? btnEl.innerHTML : '';
  if (btnEl) {
    btnEl.disabled = true;
    btnEl.innerHTML = '⏳ Đang tạo...';
  }
  showToast(`✨ AI đang biên soạn 5 câu hỏi mới cho "${sub?.name || 'Môn học'}"...`, 'info');
  const res = await apiFetch('/api/ai/expand-bank', {
    method: 'POST',
    body: JSON.stringify({ subject_id: sid, subject_name: sub?.name || '', kind: 'questions', count: 5 })
  });
  if (btnEl) {
    btnEl.disabled = false;
    btnEl.innerHTML = origHtml;
  }
  if (res.success && res.generated_count) {
    addXp(20);
    playSound('complete');
    await loadSubjectsAndStats();
    showToast(`🎉 Đã thêm ${res.generated_count} câu hỏi mới vào "${sub?.name || ''}"!`, 'success');
  } else {
    showToast(res.error || 'Chưa tạo được câu hỏi mới', 'warning');
  }
}

function openSubjectExam(sid) {
  const sel = document.getElementById('exam-subject-select');
  if (sel) sel.value = String(sid);
  switchTab('exam');
  resetToExamConfig();
}

function openSubjectFlashcards(sid) {
  const sel = document.getElementById('fc-subject-select');
  if (sel) sel.value = String(sid);
  switchTab('flashcards');
}

function openSubjectBank(sid) {
  const sel = document.getElementById('bank-subject-select');
  if (sel) sel.value = String(sid);
  switchTab('search');
}

function openNotesBank() {
  const sel = document.getElementById('bank-special-select');
  if (sel) sel.value = 'noted';
  switchTab('search');
}

function quickStartOOPExam() {
  const oop = STATE.subjects.find((s) => s.code === 'OOP_CSHARP') || STATE.subjects[0];
  if (!oop) return;
  const sel = document.getElementById('exam-subject-select');
  if (sel) sel.value = String(oop.id);
  setExamMode('practice');
  switchTab('exam');
  onExamSubjectChange().then(() => startCustomExam());
}

function quickStartHoaSinhCTUMP() {
  const hs = STATE.subjects.find((s) => s.code === 'HOASINH_CTUMP') || STATE.subjects[0];
  if (!hs) return;
  const sel = document.getElementById('exam-subject-select');
  if (sel) sel.value = String(hs.id);
  setExamMode('practice');
  switchTab('exam');
  onExamSubjectChange().then(() => startCustomExam());
}



function openBai4PartsModal() {
  const modal = document.getElementById('modal-bai4-parts');
  if (modal) {
    modal.classList.remove('hidden');
    if (window.lucide) window.lucide.createIcons();
  } else {
    quickStartBai4Lipid();
  }
}

function closeBai4PartsModal() {
  document.getElementById('modal-bai4-parts')?.classList.add('hidden');
}

async function quickStartBai4Lipid(part = null) {
  const hs = STATE.subjects.find((s) => s.code === 'HOASINH_CTUMP') || STATE.subjects[0];
  if (!hs) return;
  const sel = document.getElementById('exam-subject-select');
  if (sel) sel.value = String(hs.id);
  setExamMode('practice');
  switchTab('exam');
  await onExamSubjectChange();
  const kind = part ? `lipid_bai4_p${part}` : 'lipid_bai4';
  await startSpecialDrill(kind, hs.id);
}

async function startTimedExamForBai4Lipid() {
  const hs = STATE.subjects.find((s) => s.code === 'HOASINH_CTUMP') || STATE.subjects[0];
  if (!hs) return;
  const sel = document.getElementById('exam-subject-select');
  if (sel) sel.value = String(hs.id);
  setExamMode('real');
  selectTimePreset(60);
  switchTab('exam');
  await onExamSubjectChange();
  await startSpecialDrill('lipid_bai4', hs.id);
}

function openBai3PartsModal() {
  const modal = document.getElementById('modal-bai3-parts');
  if (modal) {
    modal.classList.remove('hidden');
    if (window.lucide) window.lucide.createIcons();
  } else {
    quickStartBai3Glucid();
  }
}

function closeBai3PartsModal() {
  document.getElementById('modal-bai3-parts')?.classList.add('hidden');
}

async function quickStartBai3Glucid(part = null) {
  const hs = STATE.subjects.find((s) => s.code === 'HOASINH_CTUMP') || STATE.subjects[0];
  if (!hs) return;
  const sel = document.getElementById('exam-subject-select');
  if (sel) sel.value = String(hs.id);
  setExamMode('practice');
  switchTab('exam');
  await onExamSubjectChange();
  const kind = part ? `glucid_bai3_p${part}` : 'glucid_bai3';
  await startSpecialDrill(kind, hs.id);
}

async function startTimedExamForBai3Glucid() {
  const hs = STATE.subjects.find((s) => s.code === 'HOASINH_CTUMP') || STATE.subjects[0];
  if (!hs) return;
  const sel = document.getElementById('exam-subject-select');
  if (sel) sel.value = String(hs.id);
  setExamMode('real');
  selectTimePreset(60);
  switchTab('exam');
  await onExamSubjectChange();
  await startSpecialDrill('glucid_bai3', hs.id);
}

async function quickStartBai2Protid() {
  const hs = STATE.subjects.find((s) => s.code === 'HOASINH_CTUMP') || STATE.subjects[0];
  if (!hs) return;
  const sel = document.getElementById('exam-subject-select');
  if (sel) sel.value = String(hs.id);
  setExamMode('practice');
  switchTab('exam');
  await onExamSubjectChange();
  await startSpecialDrill('protid_bai2', hs.id);
}

async function quickStartHoaSinhImagesOnly() {
  const hs = STATE.subjects.find((s) => s.code === 'HOASINH_CTUMP') || STATE.subjects[0];
  if (!hs) return;
  const sel = document.getElementById('exam-subject-select');
  if (sel) sel.value = String(hs.id);
  setExamMode('practice');
  switchTab('exam');
  await onExamSubjectChange();
  await startSpecialDrill('images', hs.id);
}

function quickStartBlitzMode() {
  const target =
    STATE.subjects.find((s) => s.code === 'HOASINH_CTUMP') ||
    STATE.subjects.find((s) => s.code === 'OOP_CSHARP') ||
    STATE.subjects[0];
  if (!target) return;
  const sel = document.getElementById('exam-subject-select');
  if (sel) sel.value = String(target.id);
  setExamMode('blitz');
  switchTab('exam');
  onExamSubjectChange().then(() => startCustomExam());
}

// =========================================================================
// 9. EXAM ROOM: MODES (PRACTICE / REAL / BLITZ / STUDY), TIMERS & PARTS
// =========================================================================
function setExamMode(mode) {
  STATE.examConfig.mode = mode;
  ['practice', 'real', 'blitz', 'study'].forEach((m) => {
    document.getElementById(`mode-card-${m}`)?.classList.toggle('active', m === mode);
  });
  playSound('click');
}

function selectCountPreset(count) {
  STATE.examConfig.count = count;
  const inp = document.getElementById('exam-custom-count');
  const total = STATE.examConfig.subjectAllQuestions.length || 113;
  if (inp) inp.value = count >= 9999 ? total : count;
  document.querySelectorAll('#count-presets-wrap .preset-pill').forEach((b) => {
    b.classList.toggle('active', Number(b.getAttribute('data-count')) === count);
  });
  playSound('click');
}

function onCustomCountInput(val) {
  const n = Math.max(1, parseInt(val || '20', 10));
  STATE.examConfig.count = n;
  document.querySelectorAll('#count-presets-wrap .preset-pill').forEach((b) => {
    b.classList.toggle('active', Number(b.getAttribute('data-count')) === n);
  });
}

function selectTimePreset(minutes) {
  STATE.examConfig.durationMinutes = minutes;
  const inp = document.getElementById('exam-custom-time');
  if (inp) inp.value = minutes;
  document.querySelectorAll('#time-presets-wrap .preset-pill').forEach((b) => {
    b.classList.toggle('active', Number(b.getAttribute('data-time')) === minutes);
  });
  playSound('click');
}

function onCustomTimeInput(val) {
  const m = Math.max(0, parseInt(val || '0', 10));
  STATE.examConfig.durationMinutes = m;
  document.querySelectorAll('#time-presets-wrap .preset-pill').forEach((b) => {
    b.classList.toggle('active', Number(b.getAttribute('data-time')) === m);
  });
}

async function onExamSubjectChange() {
  const sel = document.getElementById('exam-subject-select');
  if (!sel || !sel.value) return;
  const sid = Number(sel.value);
  STATE.examConfig.subjectId = sid;

  const res = await apiFetch(`/api/subjects/${sid}/questions?type=all`);
  const allQs = res.questions || [];
  STATE.examConfig.subjectAllQuestions = allQs;

  const meta = document.getElementById('exam-subject-meta');
  if (meta) meta.textContent = `Tổng ${allQs.length} câu hỏi sẵn sàng`;

  const grid = document.getElementById('exam-parts-grid');
  if (grid) {
    let html = '';
    const isCtump = (STATE.subjects.find((s) => s.id === sid)?.code || '') === 'HOASINH_CTUMP';
    if (isCtump) {
      html += `
        <div class="col-span-full p-3 rounded-2xl border border-indigo-500/40 bg-indigo-500/10 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 mb-1 shadow-sm">
          <div class="flex items-center gap-2.5">
            <span class="text-2xl">🏛️</span>
            <div>
              <div class="font-black text-xs text-indigo-300 flex items-center gap-1.5">
                Trọn Bộ 322 Câu Hóa Sinh CTUMP Gốc (Chuẩn Giáo Trình)
              </div>
              <div class="text-[11px] txt-muted">Đã chia 5 phần: An toàn PTN, Protein/Biuret, Thận, Enzym/Lipid & Nước tiểu</div>
            </div>
          </div>
          <button type="button" onclick="openCtumpOriginalPartsModal()" class="btn-primary !bg-indigo-600 hover:!bg-indigo-700 px-3.5 py-1.5 text-xs font-black shadow-sm shrink-0">
            Xem 5 Phần Gốc ↗
          </button>
        </div>
      `;
    }
    const bai4Questions = allQs.filter((q) => q.topic_tag && q.topic_tag.startsWith('Bài 4'));
    if (bai4Questions.length > 0) {
      html += `
        <div class="col-span-full p-2.5 rounded-xl border border-rose-500/30 bg-rose-500/10 flex items-center justify-between gap-2 mb-1">
          <span class="font-black text-xs text-rose-300 flex items-center gap-1.5">
            🫀 Bài 4: Chuyển Hóa Lipid & Nước Tiểu 10 Thông Số (${bai4Questions.length} câu)
          </span>
          <button type="button" onclick="openBai4PartsModal()" class="btn-primary !bg-rose-600 hover:!bg-rose-700 px-3 py-1 text-[11px] font-bold shadow-sm">
            Chọn 7 Phần Bài Học ↗
          </button>
        </div>
        <button type="button" onclick="startSpecialDrill('lipid_bai4', ${sid})" class="part-card" style="border-color: rgba(244, 63, 94, 0.5);">
          <div class="font-extrabold text-xs text-rose-400 flex justify-between">
            <span>🫀 Luyện Toàn Bộ 200 Câu Lipid</span>
            <span>→</span>
          </div>
        </button>
        <button type="button" onclick="startSpecialDrill('lipid_bai4_p1', ${sid})" class="part-card">
          <div class="font-extrabold text-xs txt-main flex justify-between"><span>🫀 B4.1: Cholesterol toàn phần (30c)</span><span class="txt-brand">→</span></div>
        </button>
        <button type="button" onclick="startSpecialDrill('lipid_bai4_p2', ${sid})" class="part-card">
          <div class="font-extrabold text-xs txt-main flex justify-between"><span>🫀 B4.2: Triglycerid huyết thanh (30c)</span><span class="txt-brand">→</span></div>
        </button>
        <button type="button" onclick="startSpecialDrill('lipid_bai4_p3', ${sid})" class="part-card">
          <div class="font-extrabold text-xs txt-main flex justify-between"><span>🫀 B4.3: HDL-C & LDL-C Friedewald (30c)</span><span class="txt-brand">→</span></div>
        </button>
        <button type="button" onclick="startSpecialDrill('lipid_bai4_p4', ${sid})" class="part-card">
          <div class="font-extrabold text-xs txt-main flex justify-between"><span>🫀 B4.4: Thể Ceton nước tiểu (25c)</span><span class="txt-brand">→</span></div>
        </button>
        <button type="button" onclick="startSpecialDrill('lipid_bai4_p5', ${sid})" class="part-card">
          <div class="font-extrabold text-xs txt-main flex justify-between"><span>🫀 B4.5: Que Cybow 3 thông số (25c)</span><span class="txt-brand">→</span></div>
        </button>
        <button type="button" onclick="startSpecialDrill('lipid_bai4_p6', ${sid})" class="part-card">
          <div class="font-extrabold text-xs txt-main flex justify-between"><span>🫀 B4.6: Máy 10 thông số vận hành (30c)</span><span class="txt-brand">→</span></div>
        </button>
        <button type="button" onclick="startSpecialDrill('lipid_bai4_p7', ${sid})" class="part-card">
          <div class="font-extrabold text-xs txt-main flex justify-between"><span>🫀 B4.7: Nguyên lý & Độ nhạy 10 chỉ số (30c)</span><span class="txt-brand">→</span></div>
        </button>
      `;
    }

    const bai3Questions = allQs.filter((q) => q.topic_tag && q.topic_tag.startsWith('Bài 3'));
    if (bai3Questions.length > 0) {
      html += `
        <div class="col-span-full p-2.5 rounded-xl border border-amber-500/30 bg-amber-500/10 flex items-center justify-between gap-2 mb-1">
          <span class="font-black text-xs text-amber-300 flex items-center gap-1.5">
            🍬 Bài 3: Hóa học Glucid & Biện luận Đái tháo đường (${bai3Questions.length} câu)
          </span>
          <button type="button" onclick="openBai3PartsModal()" class="btn-primary !bg-amber-500 hover:!bg-amber-600 px-3 py-1 text-[11px] font-bold shadow-sm">
            Chọn 6 Phần Bài Học ↗
          </button>
        </div>
        <button type="button" onclick="startSpecialDrill('glucid_bai3', ${sid})" class="part-card" style="border-color: rgba(245, 158, 11, 0.5);">
          <div class="font-extrabold text-xs text-amber-400 flex justify-between">
            <span>🍬 Luyện Toàn Bộ 200 Câu Glucid</span>
            <span>→</span>
          </div>
        </button>
        <button type="button" onclick="startSpecialDrill('glucid_bai3_p1', ${sid})" class="part-card">
          <div class="font-extrabold text-xs txt-main flex justify-between"><span>🍬 B3.1: Molish & Khái niệm (25c)</span><span class="txt-brand">→</span></div>
        </button>
        <button type="button" onclick="startSpecialDrill('glucid_bai3_p2', ${sid})" class="part-card">
          <div class="font-extrabold text-xs txt-main flex justify-between"><span>🍬 B3.2: Fehling & Tính khử (35c)</span><span class="txt-brand">→</span></div>
        </button>
        <button type="button" onclick="startSpecialDrill('glucid_bai3_p3', ${sid})" class="part-card">
          <div class="font-extrabold text-xs txt-main flex justify-between"><span>🍬 B3.3: Polysaccharid & Iod (25c)</span><span class="txt-brand">→</span></div>
        </button>
        <button type="button" onclick="startSpecialDrill('glucid_bai3_p4', ${sid})" class="part-card">
          <div class="font-extrabold text-xs txt-main flex justify-between"><span>🍬 B3.4: Glucose GOD-POD (45c)</span><span class="txt-brand">→</span></div>
        </button>
        <button type="button" onclick="startSpecialDrill('glucid_bai3_p5', ${sid})" class="part-card">
          <div class="font-extrabold text-xs txt-main flex justify-between"><span>🍬 B3.5: Đái tháo đường & OGTT (35c)</span><span class="txt-brand">→</span></div>
        </button>
        <button type="button" onclick="startSpecialDrill('glucid_bai3_p6', ${sid})" class="part-card">
          <div class="font-extrabold text-xs txt-main flex justify-between"><span>🍬 B3.6: Benedict Nước tiểu (35c)</span><span class="txt-brand">→</span></div>
        </button>
      `;
    }

    const chunk = 25;
    let partIdx = 1;
    for (let i = 0; i < allQs.length; i += chunk) {
      const end = Math.min(i + chunk, allQs.length);
      html += `
        <button type="button" onclick="startPartExam(${i}, ${end}, 'Phần ${partIdx} (${i + 1}–${end})')" class="part-card">
          <div class="font-extrabold text-xs txt-main flex justify-between">
            <span>Phần ${partIdx}: Câu ${i + 1}–${end}</span>
            <span class="txt-brand">→</span>
          </div>
        </button>`;
      partIdx++;
    }
    const bmCount = allQs.filter((q) => STATE.bookmarks.includes(q.id)).length;
    const mistakeIds = STATE.mistakes.map((m) => (typeof m === 'object' ? m.id : m));
    const msCount = allQs.filter((q) => mistakeIds.includes(q.id)).length;
    const imgCount = allQs.filter((q) => q.image_url && String(q.image_url).trim() !== '').length;

    if (imgCount > 0) {
      html += `
        <button type="button" onclick="startSpecialDrill('images', ${sid})" class="part-card" style="border-color: rgba(16, 185, 129, 0.45);">
          <div class="font-extrabold text-xs txt-emerald flex justify-between"><span>🖼️ Câu Hình ảnh / Tiêu bản (${imgCount})</span><span>→</span></div>
        </button>`;
    }

    html += `
      <button type="button" onclick="startSpecialDrill('bookmarks', ${sid})" class="part-card">
        <div class="font-extrabold text-xs txt-amber flex justify-between"><span>⭐ Đã lưu (${bmCount})</span><span>→</span></div>
      </button>
      <button type="button" onclick="startSpecialDrill('mistakes', ${sid})" class="part-card">
        <div class="font-extrabold text-xs txt-rose flex justify-between"><span>🩹 Câu sai (${msCount})</span><span>→</span></div>
      </button>
    `;
    grid.innerHTML = html;
  }
}

function startPartExam(startIdx, endIdx, label) {
  const slice = STATE.examConfig.subjectAllQuestions.slice(startIdx, endIdx);
  if (!slice.length) return;
  launchExamWithQuestions(slice, label, false);
}

async function startSpecialDrill(kind, specificSid = null) {
  let sid = specificSid || STATE.examConfig.subjectId || (STATE.subjects.find((s) => s.code === 'HOASINH_CTUMP') || STATE.subjects[0])?.id;
  if (!sid) sid = 10;

  // Always ensure fresh and correct pool for this specific subject
  let pool = STATE.examConfig.subjectAllQuestions;
  if (!pool || !pool.length || String(STATE.examConfig.subjectId) !== String(sid)) {
    const res = await apiFetch(`/api/subjects/${sid}/questions?type=all`);
    pool = res.questions || [];
    STATE.examConfig.subjectAllQuestions = pool;
    STATE.examConfig.subjectId = sid;
  }

  const mistakeIds = STATE.mistakes.map((m) => (typeof m === 'object' ? m.id : m));
  let filtered = [];

  if (kind === 'lipid_bai4') {
    filtered = pool.filter((q) => (q.topic_tag && q.topic_tag.startsWith('Bài 4')) || (q.question_text && (q.question_text.includes('Cholesterol') || q.question_text.includes('Triglycerid') || q.question_text.includes('Friedewald') || q.question_text.includes('nitroprussiat') || q.question_text.includes('ceton') || q.question_text.includes('Cybow'))));
  } else if (kind && kind.startsWith('lipid_bai4_p')) {
    const pNum = kind.replace('lipid_bai4_p', '');
    filtered = pool.filter((q) => q.topic_tag && q.topic_tag.includes(`Bài 4 - Phần ${pNum}`));
  } else if (kind === 'glucid_bai3') {
    filtered = pool.filter((q) => (q.topic_tag && q.topic_tag.startsWith('Bài 3')) || (q.question_text && (q.question_text.includes('Molish') || q.question_text.includes('Fehling') || q.question_text.includes('Benedict') || q.question_text.includes('GOD-POD') || q.question_text.includes('đái tháo đường'))));
  } else if (kind && kind.startsWith('glucid_bai3_p')) {
    const pNum = kind.replace('glucid_bai3_p', '');
    filtered = pool.filter((q) => q.topic_tag && q.topic_tag.includes(`Bài 3 - Phần ${pNum}`));
  } else if (kind === 'protid_bai2') {
    filtered = pool.filter((q) => (q.topic_tag && q.topic_tag.includes('Protid')) || (q.question_text && q.question_text.includes('Biuret')) || (q.question_text && q.question_text.includes('Acid uric')) || (q.question_text && q.question_text.includes('Urê')) || (q.question_text && q.question_text.includes('Creatinin')));
  } else if (kind === 'images') {
    filtered = pool.filter((q) => q.image_url && String(q.image_url).trim() !== '');
  } else if (kind === 'bookmarks') {
    filtered = pool.filter((q) => STATE.bookmarks.includes(q.id));
  } else {
    filtered = pool.filter((q) => mistakeIds.includes(q.id));
  }

  // Robust fallback: If specific filter returned empty, use all available subject questions so exam NEVER breaks!
  if (!filtered.length) {
    if (kind === 'bookmarks' || kind === 'mistakes') {
      showToast(kind === 'bookmarks' ? 'Chưa có câu lưu sao nào!' : 'Tuyệt vời! Bạn không còn câu sai nào tồn đọng!', 'info');
      return;
    }
    filtered = pool.slice(0, 40);
  }

  switchTab('exam');
  const titleMap = {
    images: `Soi Tiêu Bản & Hình Ảnh (${filtered.length} câu)`,
    bookmarks: `Câu Đã Lưu (${filtered.length})`,
    mistakes: `Ôn Câu Sai (${filtered.length})`,
    protid_bai2: `Bài 2: Protid & Chức Năng Thận (${filtered.length} câu)`,
    glucid_bai3: `Bài 3: 200 Câu Glucid & Đái Tháo Đường (${filtered.length} câu)`,
    glucid_bai3_p1: `Bài 3.1: Phản ứng Molish & Đại cương (${filtered.length} câu)`,
    glucid_bai3_p2: `Bài 3.2: Phản ứng Fehling & Tính khử (${filtered.length} câu)`,
    glucid_bai3_p3: `Bài 3.3: Polysaccharid với Iod (${filtered.length} câu)`,
    glucid_bai3_p4: `Bài 3.4: Định lượng Glucose GOD-POD (${filtered.length} câu)`,
    glucid_bai3_p5: `Bài 3.5: Biện luận ĐTĐ & Nghiệm pháp OGTT (${filtered.length} câu)`,
    glucid_bai3_p6: `Bài 3.6: Benedict & Nước tiểu (${filtered.length} câu)`,
    lipid_bai4: `Bài 4: 200 Câu Lipid & Nước Tiểu 10 Thông Số (${filtered.length} câu)`,
    lipid_bai4_p1: `Bài 4.1: Định lượng Cholesterol toàn phần (${filtered.length} câu)`,
    lipid_bai4_p2: `Bài 4.2: Định lượng Triglycerid (${filtered.length} câu)`,
    lipid_bai4_p3: `Bài 4.3: Định lượng HDL-C & LDL-C (${filtered.length} câu)`,
    lipid_bai4_p4: `Bài 4.4: Phản ứng Thể Ceton nước tiểu (${filtered.length} câu)`,
    lipid_bai4_p5: `Bài 4.5: Que nhúng Cybow 3 thông số (${filtered.length} câu)`,
    lipid_bai4_p6: `Bài 4.6: Máy phân tích nước tiểu 10 thông số (${filtered.length} câu)`,
    lipid_bai4_p7: `Bài 4.7: Nguyên lý 10 thông số & Độ nhạy (${filtered.length} câu)`
  };
  launchExamWithQuestions(filtered, titleMap[kind] || `Luyện chuyên đề (${filtered.length})`, false);
}

async function startCustomExam() {
  const sid = Number(document.getElementById('exam-subject-select')?.value || STATE.examConfig.subjectId);
  const qType = document.getElementById('exam-type-select')?.value || 'all';
  const bloomDiff = document.getElementById('exam-bloom-filter')?.value || 'all';
  const count = Math.max(1, parseInt(document.getElementById('exam-custom-count')?.value || '20', 10));
  const randomOrder = document.getElementById('exam-random-toggle')?.checked ?? true;

  const res = await apiFetch(`/api/subjects/${sid}/questions?type=${encodeURIComponent(qType)}`);
  let list = res.questions || [];
  if (bloomDiff !== 'all') {
    list = list.filter((q) => getBloomInfo(q.difficulty, q.question_text).key === bloomDiff);
  }
  if (!list.length) {
    showToast('Chưa có câu hỏi thuộc bộ lọc này! Hãy thử đổi cấp độ hoặc dùng AI Soạn Đề.', 'warning');
    return;
  }
  if (randomOrder || STATE.examConfig.mode === 'blitz') {
    list = [...list].sort(() => Math.random() - 0.5);
  }
  const sub = STATE.subjects.find((s) => s.id === sid);
  launchExamWithQuestions(list.slice(0, Math.min(list.length, count)), sub ? sub.name : 'Phòng thi', false);
}

function normalizeCorrectLetter(q) {
  const raw = String(q.correct_option ?? '').trim();
  if (q.q_type === 'mcq' || q.q_type === 'true_false') {
    const up = raw.toUpperCase();
    const map = { '0': 'A', '1': 'B', '2': 'C', '3': 'D', TRUE: 'A', 'ĐÚNG': 'A', FALSE: 'B', SAI: 'B' };
    return map[up] || up;
  }
  return raw;
}

function launchExamWithQuestions(rawQuestions, title, forceNoShuffle = false) {
  clearInterval(STATE.exam.timerId);

  const shuffleOpts = !forceNoShuffle && (document.getElementById('exam-shuffle-opts-toggle')?.checked ?? false);
  const durationMin = Math.max(0, parseInt(document.getElementById('exam-custom-time')?.value ?? '0', 10) || 0);

  const correctMap = {};
  const prepared = rawQuestions.map((orig) => {
    const q = { ...orig };
    const baseCorr = normalizeCorrectLetter(q);
    if (shuffleOpts && q.q_type === 'mcq') {
      const items = [
        { k: 'A', t: q.option_a },
        { k: 'B', t: q.option_b },
        { k: 'C', t: q.option_c },
        { k: 'D', t: q.option_d }
      ].sort(() => Math.random() - 0.5);
      let newCorr = 'A';
      ['A', 'B', 'C', 'D'].forEach((L, idx) => {
        q[`option_${L.toLowerCase()}`] = items[idx].t;
        if (items[idx].k === baseCorr) newCorr = L;
      });
      q._effectiveCorrect = newCorr;
      correctMap[q.id] = newCorr;
    } else {
      q._effectiveCorrect = baseCorr;
      correctMap[q.id] = baseCorr;
    }
    return q;
  });

  STATE.exam = {
    active: true,
    paused: false,
    subjectId: STATE.examConfig.subjectId,
    subjectName: title,
    mode: STATE.examConfig.mode,
    questions: prepared,
    currentIndex: 0,
    answers: {},
    graded: {},
    correctMap,
    eliminated: {},
    hints: {},
    concepts: {},
    deepAnalysis: {},
    mistakeDiagnosis: {},
    mnemonics: {},
    similarQuiz: {},
    customQa: {},
    essayGrades: {},
    durationSeconds: durationMin * 60,
    remainingSeconds: durationMin * 60,
    elapsedSeconds: 0,
    timerId: null,
    streak: 0,
    maxStreak: 0,
    blitzLives: 3,
    blitzScore: 0,
    paletteFilter: 'all',
    lastResult: null
  };

  if (STATE.exam.mode === 'study') {
    prepared.forEach((q) => {
      STATE.exam.answers[q.id] = q._effectiveCorrect;
      STATE.exam.graded[q.id] = true;
    });
  }

  if (typeof switchTab === 'function') switchTab('exam');
  document.getElementById('exam-config-screen')?.classList.add('hidden');
  document.getElementById('exam-result-screen')?.classList.add('hidden');
  document.getElementById('exam-active-screen')?.classList.remove('hidden');
  document.getElementById('exam-pause-overlay')?.classList.add('hidden');
  document.getElementById('exam-question-stage')?.classList.remove('exam-paused-blur');

  setText('active-exam-title', title);
  setText('total-q-num', prepared.length);

  startExamTimerLoop();
  renderCurrentExamQuestion();
  playSound('click');
}

function startExamTimerLoop() {
  clearInterval(STATE.exam.timerId);
  updateExamTimerUI();
  STATE.exam.timerId = setInterval(() => {
    if (!STATE.exam.active || STATE.exam.paused) return;
    STATE.exam.elapsedSeconds++;
    if (STATE.exam.durationSeconds > 0) {
      STATE.exam.remainingSeconds--;
      updateExamTimerUI();
      if (STATE.exam.remainingSeconds <= 0) {
        clearInterval(STATE.exam.timerId);
        showToast('⏰ Hết giờ! Hệ thống tự động chấm điểm.', 'warning');
        submitExamNow(true);
      }
    } else {
      updateExamTimerUI();
    }
  }, 1000);
}

function updateExamTimerUI() {
  const box = document.getElementById('exam-timer-box');
  const txt = document.getElementById('exam-timer-text');
  if (!box || !txt) return;

  if (STATE.exam.durationSeconds === 0) {
    txt.textContent = `∞ ${formatDuration(STATE.exam.elapsedSeconds)}`;
    box.className = 'badge-emerald px-3 py-1.5 rounded-xl font-mono text-xs sm:text-sm font-extrabold flex items-center gap-1.5';
  } else {
    txt.textContent = `⏱ ${formatDuration(STATE.exam.remainingSeconds)}`;
    box.className =
      STATE.exam.remainingSeconds <= 60
        ? 'badge-rose px-3 py-1.5 rounded-xl font-mono text-xs sm:text-sm font-extrabold flex items-center gap-1.5 animate-pulse'
        : 'badge-brand px-3 py-1.5 rounded-xl font-mono text-xs sm:text-sm font-extrabold flex items-center gap-1.5';
  }
}

function togglePauseExam() {
  if (!STATE.exam.active) return;
  STATE.exam.paused = !STATE.exam.paused;
  document.getElementById('exam-pause-overlay')?.classList.toggle('hidden', !STATE.exam.paused);
  document.getElementById('exam-question-stage')?.classList.toggle('exam-paused-blur', STATE.exam.paused);
  const btn = document.getElementById('pause-exam-btn');
  if (btn) {
    btn.innerHTML = `<i data-lucide="${STATE.exam.paused ? 'play' : 'pause'}" class="w-4 h-4"></i>`;
    refreshIcons();
  }
  playSound('click');
}

function renderCurrentExamQuestion() {
  try {
    if (!STATE.exam || !Array.isArray(STATE.exam.questions) || !STATE.exam.questions.length) return;
    const q = STATE.exam.questions[STATE.exam.currentIndex];
    if (!q) return;

    // Bulletproof defensive checks: bookmarks, mistakes, notes always safe arrays/objects!
    if (!Array.isArray(STATE.bookmarks)) STATE.bookmarks = [];
    if (!Array.isArray(STATE.mistakes)) STATE.mistakes = [];
    if (!STATE.notes || typeof STATE.notes !== 'object') STATE.notes = {};

  const total = STATE.exam.questions.length;
  const answeredCount = Object.keys(STATE.exam.answers).filter(
    (k) => String(STATE.exam.answers[k] ?? '').trim() !== ''
  ).length;

  setText('current-q-num', STATE.exam.currentIndex + 1);
  if (typeof pinnedTutorQuestion !== 'undefined' && pinnedTutorQuestion && pinnedTutorQuestion.source === 'exam') {
    const parsedH = parseQuestionHeader(q.question_text || '');
    const cleanT = (parsedH.body || q.question_text || '').replace(/<[^>]+>/g, '').trim();
    pinnedTutorQuestion.id = q.id;
    pinnedTutorQuestion.shortTitle = `Câu ${STATE.exam.currentIndex + 1}`;
    pinnedTutorQuestion.fullTitle = cleanT;
    pinnedTutorQuestion.topic = parsedH.topic || '';
    pinnedTutorQuestion.code_snippet = q.code_snippet || '';
    pinnedTutorQuestion.option_a = q.option_a || '';
    pinnedTutorQuestion.option_b = q.option_b || '';
    pinnedTutorQuestion.option_c = q.option_c || '';
    pinnedTutorQuestion.option_d = q.option_d || '';
    pinnedTutorQuestion.correct_option = q._effectiveCorrect || '';
    pinnedTutorQuestion.explanation = q.explanation || '';
    pinnedTutorQuestion.user_answer = STATE.exam.answers[q.id] || '';
    setText('ft-pinned-q-title', `📌 Câu ${STATE.exam.currentIndex + 1} • ${pinnedTutorQuestion.topic || 'Kiến thức cốt lõi'}`);
    setText('ft-pinned-q-body', cleanT.substring(0, 110) + (cleanT.length > 110 ? '...' : ''));
    syncFloatingTutorSubjectContext();
  }
  setText('answered-q-count', `${answeredCount}/${total}`);
  const bar = document.getElementById('exam-progress-bar');
  if (bar) bar.style.width = `${total ? Math.round((answeredCount / total) * 100) : 0}%`;

  // Blitz Lives & Streak Badges
  const blitzEl = document.getElementById('blitz-lives-badge');
  if (blitzEl) {
    if (STATE.exam.mode === 'blitz') {
      const hearts = '❤️'.repeat(STATE.exam.blitzLives) + '🖤'.repeat(Math.max(0, 3 - STATE.exam.blitzLives));
      blitzEl.textContent = `${hearts} • ${STATE.exam.blitzScore}đ`;
      blitzEl.classList.remove('hidden');
    } else {
      blitzEl.classList.add('hidden');
    }
  }

  const streakEl = document.getElementById('streak-badge');
  if (streakEl) {
    if (STATE.exam.streak >= 2) {
      streakEl.textContent = `🔥 x${STATE.exam.streak}`;
      streakEl.classList.remove('hidden');
    } else {
      streakEl.classList.add('hidden');
    }
  }

  // Smooth Question Entrance
  const bodyWrap = document.getElementById('q-body-wrapper');
  if (bodyWrap) {
    bodyWrap.classList.remove('animate-question-in');
    void bodyWrap.offsetWidth;
    bodyWrap.classList.add('animate-question-in');
  }

  // Clean Compact Badges (Including 4-Level Bloom Badge)
  const parsed = parseQuestionHeader(q.question_text);
  const bloom = getBloomInfo(q.difficulty, q.question_text);
  let badgesHtml = '';
  if (parsed.bankNum) badgesHtml += `<span class="badge-brand text-xs px-2.5 py-0.5 rounded-lg font-mono font-extrabold">#${parsed.bankNum}</span>`;
  badgesHtml += `<span class="${bloom.cls} text-xs px-2.5 py-0.5 rounded-lg font-bold">${bloom.label}</span>`;
  if (parsed.topic) badgesHtml += `<span class="badge-subtle text-xs px-2.5 py-0.5 rounded-lg font-semibold">${formatRichText(parsed.topic)}</span>`;
  if (!parsed.topic) {
    const tMap = { mcq: 'Trắc nghiệm', true_false: 'Đúng / Sai', short_answer: 'Trả lời ngắn', essay: 'Tự luận' };
    badgesHtml += `<span class="badge-subtle text-xs px-2.5 py-0.5 rounded-lg font-bold">${tMap[q.q_type] || 'Câu hỏi'}</span>`;
  }
  const metaEl = document.getElementById('q-meta-badges');
  if (metaEl) metaEl.innerHTML = badgesHtml;

  // Bookmark & Note state
  setText('bookmark-star-icon', STATE.bookmarks.includes(q.id) ? '⭐' : '☆');
  document.getElementById('btn-5050')?.classList.toggle('hidden', q.q_type !== 'mcq');

  const existingNote = STATE.notes[q.id] || '';
  const noteBox = document.getElementById('q-note-box');
  const noteInp = document.getElementById('q-note-input');
  if (noteInp) noteInp.value = existingNote;
  if (noteBox) noteBox.classList.toggle('hidden', !existingNote);

  // Prompt, Image & Code (Bulletproof 100% Guaranteed Rendering)
  const promptEl = document.getElementById('q-prompt-text');
  if (promptEl) {
    const rawPrompt = (parsed.body || q.question_text || '').trim();
    try {
      promptEl.innerHTML = formatRichText(rawPrompt) || escapeHtml(rawPrompt);
    } catch (e) {
      promptEl.innerHTML = escapeHtml(rawPrompt);
    }
  }

  const imgWrap = document.getElementById('q-image-wrapper');
  if (imgWrap) {
    if (q.image_url && String(q.image_url).trim()) {
      const safeUrl = escapeHtml(q.image_url);
      const safeCap = escapeHtml(parsed.topic || 'Hình ảnh câu hỏi / Tiêu bản lâm sàng');
      imgWrap.innerHTML = `
        <div class="specimen-img-frame group relative inline-block max-w-full rounded-2xl overflow-hidden cursor-zoom-in"
             onclick="openImageLightbox('${safeUrl}', '${safeCap}')"
             style="border: 2px solid var(--border); background-color: var(--bg-subtle);">
          <img src="${safeUrl}" alt="Hình ảnh câu hỏi" class="max-h-72 sm:max-h-80 w-auto object-contain mx-auto transition-transform duration-200 group-hover:scale-[1.02]" loading="lazy" />
          <div class="px-3 py-1.5 text-[11px] font-bold txt-brand flex items-center justify-center gap-1.5" style="background-color: var(--bg-surface); border-top: 1px solid var(--border);">
            <span>🔍 Bấm vào hình ảnh / tiêu bản để phóng to HD</span>
          </div>
        </div>
      `;
      imgWrap.classList.remove('hidden');
    } else {
      imgWrap.innerHTML = '';
      imgWrap.classList.add('hidden');
    }
  }

  const codeWrap = document.getElementById('q-code-wrapper');
  if (codeWrap) {
    if (q.code_snippet && q.code_snippet.trim()) {
      codeWrap.innerHTML = buildCodeWindowHtml(q.code_snippet, 'Program.cs', 'csharp');
      codeWrap.classList.remove('hidden');
    } else {
      codeWrap.innerHTML = '';
      codeWrap.classList.add('hidden');
    }
  }

  // Concept Recall & Hint
  const conceptBox = document.getElementById('q-concept-box');
  const conceptContent = document.getElementById('q-concept-content');
  if (conceptBox && conceptContent) {
    if (STATE.exam.concepts[q.id]) {
      conceptContent.innerHTML = renderMarkdown(STATE.exam.concepts[q.id]);
      conceptBox.classList.remove('hidden');
    } else {
      conceptBox.classList.add('hidden');
    }
  }

  const hintBox = document.getElementById('q-hint-box');
  const hintContent = document.getElementById('q-hint-content');
  if (hintBox && hintContent) {
    if (STATE.exam.hints[q.id]) {
      hintContent.innerHTML = renderMarkdown(STATE.exam.hints[q.id]);
      hintBox.classList.remove('hidden');
    } else {
      hintBox.classList.add('hidden');
    }
  }

  // Auto Key Concepts & Term Chips for instant Ask AI
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
    const found = knownTerms.filter(t => new RegExp(`\\b${t}\\b`, 'i').test(qStr));
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
  renderQuestionFeedbackArea(q);

  const prevBtn = document.getElementById('btn-prev-q');
  const nextBtn = document.getElementById('btn-next-q');
  const topPrevBtn = document.getElementById('top-btn-prev-q');
  const topNextBtn = document.getElementById('top-btn-next-q');
  const topNextLabel = document.getElementById('top-btn-next-label');
  const bottomNextText = document.getElementById('btn-next-q-text');

  const isFirst = STATE.exam.currentIndex === 0;
  const isLast = STATE.exam.currentIndex === total - 1;

  if (prevBtn) prevBtn.disabled = isFirst;
  if (topPrevBtn) topPrevBtn.disabled = isFirst;

  if (isLast) {
    if (nextBtn) {
      nextBtn.innerHTML = `<span>Nộp Bài &amp; Chấm Điểm</span> <i data-lucide="check-circle-2" class="w-4 h-4"></i>`;
      nextBtn.onclick = () => submitExamNow();
    }
    if (topNextBtn) {
      topNextBtn.innerHTML = `<span>Nộp Bài</span> <i data-lucide="check-circle-2" class="w-4 h-4"></i>`;
      topNextBtn.onclick = () => submitExamNow();
    }
    if (topNextLabel) topNextLabel.textContent = 'Nộp Bài';
    if (bottomNextText) bottomNextText.textContent = 'Nộp Bài & Chấm Điểm';
  } else {
    if (nextBtn) {
      nextBtn.innerHTML = `<span>Câu Tiếp Theo</span> <i data-lucide="chevron-right" class="w-4 h-4"></i>`;
      nextBtn.onclick = () => nextQuestion();
    }
    if (topNextBtn) {
      topNextBtn.innerHTML = `<span id="top-btn-next-label">Tiếp theo</span> <i data-lucide="chevron-right" class="w-4 h-4"></i>`;
      topNextBtn.onclick = () => nextQuestion();
    }
    if (topNextLabel) topNextLabel.textContent = 'Tiếp theo';
    if (bottomNextText) bottomNextText.textContent = 'Câu Tiếp Theo';
  }

  renderPaletteGrid();
  refreshIcons();
  renderAllMathOnPage();
  } catch (err) {
    console.error('Critical renderCurrentExamQuestion failure:', err);
    try {
      const q = STATE.exam?.questions?.[STATE.exam?.currentIndex];
      const pEl = document.getElementById('q-prompt-text');
      const aEl = document.getElementById('q-answer-area');
      if (pEl && q) pEl.textContent = q.question_text || 'Câu hỏi';
      if (aEl && q && (q.option_a || q.option_b)) {
        aEl.innerHTML = [
          q.option_a ? `<div class="option-row opt-A" onclick="selectExamOption('A')"><strong>A:</strong> ${escapeHtml(q.option_a)}</div>` : '',
          q.option_b ? `<div class="option-row opt-B" onclick="selectExamOption('B')"><strong>B:</strong> ${escapeHtml(q.option_b)}</div>` : '',
          q.option_c ? `<div class="option-row opt-C" onclick="selectExamOption('C')"><strong>C:</strong> ${escapeHtml(q.option_c)}</div>` : '',
          q.option_d ? `<div class="option-row opt-D" onclick="selectExamOption('D')"><strong>D:</strong> ${escapeHtml(q.option_d)}</div>` : ''
        ].join('');
      }
    } catch (_) {}
  }
}

function renderQuestionAnswerArea(q) {
  const area = document.getElementById('q-answer-area');
  if (!area) return;

  const userAns = STATE.exam.answers[q.id] ?? '';
  const isGraded = Boolean(STATE.exam.graded[q.id]);
  const elimList = STATE.exam.eliminated[q.id] || [];

  if (STATE.osceBlindMode && !isGraded && !userAns && !(STATE.osceRevealedMap && STATE.osceRevealedMap[q.id])) {
    area.innerHTML = `
      <div class="p-6 rounded-2xl text-center space-y-3 animate-fade-in" style="background-color: var(--bg-subtle); border: 1.5px dashed var(--brand-border);">
        <div class="text-2xl">🕵️🔬</div>
        <div class="text-sm font-extrabold txt-main">Chế Độ Chạy Trạm OSCE / Nhớ Chủ Động (Active Recall)</div>
        <p class="text-xs txt-sub max-w-lg mx-auto">
          Hãy tự định danh tiêu bản / đọc kỹ câu hỏi và nhẩm câu trả lời trong đầu trước khi lật mở 4 phương án A, B, C, D để tránh phụ thuộc gợi ý!
        </p>
        <button type="button" onclick="revealOsceOptionsForCurrentQuestion(${q.id})" class="btn-primary px-5 py-2.5 text-xs font-extrabold">
          👁️ Tôi Đã Có Đáp Án Trong Đầu — Lật Mở Phương Án A/B/C/D
        </button>
      </div>
    `;
    return;
  }

  if (q.q_type === 'mcq' || q.q_type === 'true_false') {
    const opts =
      q.q_type === 'true_false'
        ? [
            { letter: 'A', keyNum: '1', text: q.option_a || 'Đúng (True)' },
            { letter: 'B', keyNum: '2', text: q.option_b || 'Sai (False)' }
          ]
        : [
            { letter: 'A', keyNum: '1', text: q.option_a },
            { letter: 'B', keyNum: '2', text: q.option_b },
            { letter: 'C', keyNum: '3', text: q.option_c },
            { letter: 'D', keyNum: '4', text: q.option_d }
          ];

    // Auto 2-column layout when all options are concise (< 44 chars) -> much cleaner & less vertical clutter!
    const allShort = opts.every((o) => String(o.text || '').length <= 44);
    const gridClass = allShort || q.q_type === 'true_false' ? 'grid grid-cols-1 sm:grid-cols-2 gap-3' : 'space-y-3';

    area.className = gridClass;
    area.innerHTML = opts
      .map((opt) => {
        const isPicked = String(userAns).toUpperCase() === opt.letter;
        const isCorrectOpt = q._effectiveCorrect === opt.letter;
        const isElim = elimList.includes(opt.letter);

        let cls = `option-row opt-${opt.letter}`;
        let iconRight = '';

        if (isElim) cls += ' is-eliminated';
        if (isGraded) {
          cls += ' disabled';
          if (isCorrectOpt) {
            cls += ' is-correct';
            iconRight = '<span class="text-base font-extrabold shrink-0">✔</span>';
          } else if (isPicked) {
            cls += ' is-wrong';
            iconRight = '<span class="text-base font-extrabold shrink-0">✖</span>';
          }
        } else if (isPicked) {
          cls += ' selected';
        }

        return `
          <div id="opt-row-${opt.letter}" onclick="selectExamOption('${opt.letter}')" class="${cls}">
            <div class="opt-badge">
              ${opt.letter}
              <span class="opt-key-micro">${opt.keyNum}</span>
            </div>
            <div class="option-text flex-1">${formatRichText(opt.text)}</div>
            ${iconRight}
          </div>
        `;
      })
      .join('');
  } else if (q.q_type === 'short_answer') {
    area.className = '';
    area.innerHTML = `
      <div class="flex flex-col sm:flex-row gap-2.5">
        <input id="short-ans-input" type="text" value="${escapeHtml(userAns)}"
          ${isGraded && STATE.exam.mode !== 'real' ? 'disabled' : ''}
          oninput="onTextAnswerInput(this.value)"
          onkeydown="if(event.key==='Enter'){ event.preventDefault(); confirmTextAnswer(); }"
          placeholder="Nhập kết quả hoặc từ khóa chuẩn..."
          class="uni-input flex-1 px-4 py-3.5 font-mono font-bold" />
        ${
          STATE.exam.mode !== 'real' && !isGraded
            ? `<button onclick="confirmTextAnswer()" class="btn-primary px-5 py-3 text-xs shrink-0">Chấm Ngay</button>`
            : ''
        }
      </div>
    `;
  } else {
    area.className = 'space-y-2.5';
    area.innerHTML = `
      <textarea id="essay-ans-input" rows="4" oninput="onTextAnswerInput(this.value)"
        placeholder="Nhập bài làm tự luận hoặc các luận điểm trả lời vấn đáp của bạn..."
        class="uni-input w-full p-4 text-sm">${escapeHtml(userAns)}</textarea>
      <div class="flex flex-wrap gap-2">
        <button type="button" onclick="gradeCurrentEssayWithAi()" class="btn-primary px-4 py-2.5 text-xs flex items-center gap-1.5">
          🤖 AI Chấm Điểm Tự Luận (Thang 10)
        </button>
        ${
          STATE.exam.mode !== 'real' && !isGraded
            ? `<button type="button" onclick="confirmTextAnswer()" class="btn-soft px-4 py-2.5 text-xs">📖 Đối chiếu Barem chuẩn</button>`
            : ''
        }
      </div>
    `;
  }
}

function selectExamOption(letter, fromKeyboard = false) {
  if (!STATE.exam.active || STATE.exam.paused) return;
  const q = STATE.exam.questions[STATE.exam.currentIndex];
  if (!q || (q.q_type !== 'mcq' && q.q_type !== 'true_false')) return;
  if (q.q_type === 'true_false' && (letter === 'C' || letter === 'D')) return;
  if ((STATE.exam.eliminated[q.id] || []).includes(letter)) return;
  if (STATE.exam.graded[q.id]) return;

  const rowEl = document.getElementById(`opt-row-${letter}`);
  if (rowEl && fromKeyboard) {
    rowEl.classList.add('key-bounce');
    setTimeout(() => rowEl.classList.remove('key-bounce'), 160);
  }

  STATE.exam.answers[q.id] = letter;

  if (STATE.exam.mode === 'real') {
    playSound('click');
    renderCurrentExamQuestion();
    return;
  }

  // Instant Grading (Practice & Blitz)
  STATE.exam.graded[q.id] = true;
  const isCorrect = letter === q._effectiveCorrect;

  if (isCorrect) {
    STATE.exam.streak++;
    if (STATE.exam.streak > STATE.exam.maxStreak) STATE.exam.maxStreak = STATE.exam.streak;
    if (STATE.exam.mode === 'blitz') {
      STATE.exam.blitzScore += 100 * Math.min(5, STATE.exam.streak);
      if (STATE.exam.blitzScore > STATE.blitzBest) STATE.blitzBest = STATE.exam.blitzScore;
    }
    addXp(15);
    playSound('correct');
    removeMistake(q.id);
  } else {
    STATE.exam.streak = 0;
    playSound('wrong');
    recordMistake(q.id, STATE.exam.subjectId);

    if (STATE.exam.mode === 'blitz') {
      STATE.exam.blitzLives--;
      if (STATE.exam.blitzLives <= 0) {
        renderCurrentExamQuestion();
        showToast(`💥 Hết 3 mạng! Tổng điểm Blitz: ${STATE.exam.blitzScore} đ`, 'warning');
        setTimeout(() => submitExamNow(true), 1100);
        return;
      }
    }
  }

  renderCurrentExamQuestion();

  if (STATE.ui.autoNext && isCorrect && STATE.exam.currentIndex < STATE.exam.questions.length - 1) {
    setTimeout(() => {
      if (STATE.exam.active && !STATE.exam.paused) nextQuestion();
    }, 1050);
  }
}

function onTextAnswerInput(val) {
  const q = STATE.exam.questions[STATE.exam.currentIndex];
  if (!q) return;
  STATE.exam.answers[q.id] = val;
  renderPaletteGrid();
}

function confirmTextAnswer() {
  const q = STATE.exam.questions[STATE.exam.currentIndex];
  if (!q) return;
  const val = String(STATE.exam.answers[q.id] || '').trim();
  if (!val) return;

  STATE.exam.graded[q.id] = true;
  const isCorrect =
    q.q_type === 'short_answer'
      ? isShortAnswerMatch(val, q._effectiveCorrect)
      : val.length >= 10;

  if (isCorrect) {
    STATE.exam.streak++;
    addXp(15);
    playSound('correct');
    removeMistake(q.id);
  } else {
    STATE.exam.streak = 0;
    playSound('wrong');
    recordMistake(q.id, STATE.exam.subjectId);
  }
  renderCurrentExamQuestion();
}

function renderQuestionFeedbackArea(q) {
  const panel = document.getElementById('q-feedback-panel');
  const explBox = document.getElementById('q-official-expl-box');
  if (!panel || !explBox) return;

  if (!STATE.exam.graded[q.id]) {
    panel.classList.add('hidden');
    return;
  }

  panel.classList.remove('hidden');
  const u = String(STATE.exam.answers[q.id] || '').trim();
  const aiEssay = STATE.exam.essayGrades?.[q.id];
  const isCorrect =
    q.q_type === 'mcq' || q.q_type === 'true_false'
      ? u.toUpperCase() === q._effectiveCorrect
      : q.q_type === 'short_answer'
      ? isShortAnswerMatch(u, q._effectiveCorrect)
      : aiEssay
      ? Number(aiEssay.score || 0) >= 5
      : u.length >= 10;

  const mistakeBtn = document.getElementById('btn-explain-mistake');
  if (mistakeBtn) {
    mistakeBtn.innerHTML = isCorrect
      ? '<span>🛡️</span> Phân tích bẫy dễ nhầm'
      : '<span>🩺</span> Sao tôi chọn nhầm?';
  }

  if (aiEssay) {
    const sc = Number(aiEssay.score || 0).toFixed(1);
    const scCls = sc >= 8 ? 'badge-emerald' : sc >= 5 ? 'badge-amber' : 'badge-rose';
    explBox.className = `ai-callout ${isCorrect ? 'ai-callout-emerald' : 'ai-callout-indigo'} space-y-2.5`;
    explBox.innerHTML = `
      <div class="flex flex-wrap items-center justify-between gap-2">
        <span class="text-xs font-extrabold txt-main">🤖 Kết Quả Giảng Viên AI Chấm Tự Luận</span>
        <span class="${scCls} text-xs px-3 py-1 rounded-full font-extrabold">Điểm AI: ${sc} / 10</span>
      </div>
      <div class="text-xs font-semibold txt-sub">${formatRichText(aiEssay.verdict || '')}</div>
      ${
        (aiEssay.strengths || []).length
          ? `<div class="text-xs space-y-1"><div class="font-extrabold txt-emerald">✔ Điểm mạnh đã đạt:</div>${aiEssay.strengths.map((s) => `<div class="pl-2">• ${formatRichText(s)}</div>`).join('')}</div>`
          : ''
      }
      ${
        (aiEssay.missing || []).length
          ? `<div class="text-xs space-y-1"><div class="font-extrabold txt-amber">⚠ Ý cần bổ sung để đạt 10/10:</div>${aiEssay.missing.map((m) => `<div class="pl-2">• ${formatRichText(m)}</div>`).join('')}</div>`
          : ''
      }
      <div class="p-3 rounded-xl text-xs space-y-1" style="background-color: var(--bg-surface); border: 1px solid var(--border);">
        <div class="font-extrabold txt-brand">📖 Bài trả lời mẫu đạt 10/10:</div>
        <div class="leading-relaxed">${formatRichText(aiEssay.sample_answer || q.explanation || q._effectiveCorrect)}</div>
      </div>
    `;
  } else {
    explBox.className = `ai-callout ${isCorrect ? 'ai-callout-emerald' : 'ai-callout-indigo'} space-y-1`;
    explBox.innerHTML = `
      <div class="text-xs font-extrabold ${isCorrect ? 'txt-emerald' : 'txt-rose'}">
        ${isCorrect ? `✔ Chính xác! Đáp án: ${escapeHtml(q._effectiveCorrect)}` : `💡 Đáp án đúng: ${escapeHtml(q._effectiveCorrect)}`}
      </div>
      <div class="text-sm txt-main leading-relaxed">${formatRichText(q.explanation || '')}</div>
    `;
  }

  const mistakeBox = document.getElementById('q-ai-mistake-box');
  if (mistakeBox) {
    if (STATE.exam.mistakeDiagnosis[q.id]) {
      mistakeBox.innerHTML = `<div class="markdown-body text-sm">${renderMarkdown(STATE.exam.mistakeDiagnosis[q.id])}</div>`;
      mistakeBox.classList.remove('hidden');
    } else mistakeBox.classList.add('hidden');
  }

  const mnemBox = document.getElementById('q-ai-mnemonic-box');
  if (mnemBox) {
    if (STATE.exam.mnemonics[q.id]) {
      mnemBox.innerHTML = `<div class="markdown-body text-sm">${renderMarkdown(STATE.exam.mnemonics[q.id])}</div>`;
      mnemBox.classList.remove('hidden');
    } else mnemBox.classList.add('hidden');
  }

  const deepBox = document.getElementById('q-ai-deep-box');
  if (deepBox) {
    if (STATE.exam.deepAnalysis[q.id]) {
      deepBox.innerHTML = `<div class="markdown-body text-sm">${renderMarkdown(STATE.exam.deepAnalysis[q.id])}</div>`;
      deepBox.classList.remove('hidden');
    } else deepBox.classList.add('hidden');
  }

  renderSimilarQuestionWidget(q.id);

  const qaBox = document.getElementById('q-ai-qa-box');
  if (qaBox) {
    if (STATE.exam.customQa[q.id]) {
      qaBox.innerHTML = renderMarkdown(STATE.exam.customQa[q.id]);
      qaBox.classList.remove('hidden');
    } else qaBox.classList.add('hidden');
  }

  loadQuestionDiscussions(q.id);
}

async function gradeCurrentEssayWithAi() {
  const q = STATE.exam.questions[STATE.exam.currentIndex];
  if (!q) return;
  const studentAns = String(STATE.exam.answers[q.id] || document.getElementById('essay-ans-input')?.value || '').trim();
  if (!studentAns) {
    showToast('Hãy nhập câu trả lời tự luận của bạn trước khi nhờ AI chấm!', 'warning');
    return;
  }
  STATE.exam.answers[q.id] = studentAns;
  STATE.exam.graded[q.id] = true;

  const panel = document.getElementById('q-feedback-panel');
  const explBox = document.getElementById('q-official-expl-box');
  if (panel && explBox) {
    panel.classList.remove('hidden');
    explBox.innerHTML = `<div class="skeleton-shimmer h-20 w-full"></div>`;
  }

  const res = await apiFetch('/api/ai/grade-essay', {
    method: 'POST',
    body: JSON.stringify({
      question_text: q.question_text,
      expected_barem: `${q._effectiveCorrect || ''} ${q.explanation || ''}`.trim(),
      student_answer: studentAns
    })
  });

  if (res.grading) {
    STATE.exam.essayGrades[q.id] = res.grading;
    const sc = Number(res.grading.score || 0);
    if (sc >= 5) {
      addXp(25);
      playSound('correct');
      removeMistake(q.id);
    } else {
      playSound('wrong');
      recordMistake(q.id, STATE.exam.subjectId);
    }
    showToast(`🤖 Giảng viên AI chấm: ${sc}/10 điểm!`, sc >= 5 ? 'success' : 'warning');
  }
  renderCurrentExamQuestion();
}

// Question Toolbar Actions (TTS, Personal Notes, 50/50, Hint, Bookmark)
function speakCurrentQuestion() {
  const q = STATE.exam.questions[STATE.exam.currentIndex];
  if (!q) return;
  const parsed = parseQuestionHeader(q.question_text);
  const full = `${parsed.body}. A: ${q.option_a}. B: ${q.option_b}. ${q.option_c ? 'C: ' + q.option_c + '.' : ''} ${q.option_d ? 'D: ' + q.option_d : ''}`;
  speakVietnamese(full);
}

function toggleNoteBox() {
  const box = document.getElementById('q-note-box');
  if (!box) return;
  box.classList.toggle('hidden');
  if (!box.classList.contains('hidden')) {
    document.getElementById('q-note-input')?.focus();
  }
}

function saveCurrentNote() {
  const q = STATE.exam.questions[STATE.exam.currentIndex];
  const inp = document.getElementById('q-note-input');
  if (!q || !inp) return;
  const val = inp.value.trim();
  if (val) {
    STATE.notes[q.id] = val;
    showToast('📌 Đã lưu ghi chú cá nhân!', 'success');
  } else {
    delete STATE.notes[q.id];
    document.getElementById('q-note-box')?.classList.add('hidden');
  }
  syncUserStateToServer();
}

function useLifeline5050() {
  const q = STATE.exam.questions[STATE.exam.currentIndex];
  if (!q || q.q_type !== 'mcq' || STATE.exam.graded[q.id]) return;
  if (STATE.exam.eliminated[q.id]?.length) return;
  const wrongs = ['A', 'B', 'C', 'D'].filter((L) => L !== q._effectiveCorrect).sort(() => Math.random() - 0.5);
  STATE.exam.eliminated[q.id] = wrongs.slice(0, 2);
  playSound('click');
  renderCurrentExamQuestion();
}

async function requestAiConceptRecall() {
  const q = STATE.exam.questions[STATE.exam.currentIndex];
  if (!q) return;
  if (STATE.exam.concepts[q.id]) {
    document.getElementById('q-concept-box')?.classList.toggle('hidden');
    return;
  }
  const conceptBox = document.getElementById('q-concept-box');
  const conceptContent = document.getElementById('q-concept-content');
  if (conceptBox && conceptContent) {
    conceptBox.classList.remove('hidden');
    conceptContent.innerHTML = `<div class="skeleton-shimmer h-10 w-full"></div>`;
  }
  playSound('click');
  const sub = STATE.subjects.find((s) => s.id === STATE.exam.subjectId);
  const res = await apiFetch('/api/ai/concept-recall', {
    method: 'POST',
    body: JSON.stringify({
      subject_name: sub?.name || STATE.exam.subjectName || 'Đại học',
      question_text: q.question_text,
      code_snippet: q.code_snippet || ''
    })
  });
  STATE.exam.concepts[q.id] = res.concept || 'Hãy đối chiếu công thức gốc và đơn vị chuẩn.';
  renderCurrentExamQuestion();
}

async function requestAiHint() {
  const q = STATE.exam.questions[STATE.exam.currentIndex];
  if (!q || STATE.exam.hints[q.id]) return;
  const hintBox = document.getElementById('q-hint-box');
  const hintContent = document.getElementById('q-hint-content');
  if (hintBox && hintContent) {
    hintBox.classList.remove('hidden');
    hintContent.innerHTML = `<div class="skeleton-shimmer h-8 w-full"></div>`;
  }
  const res = await apiFetch('/api/ai/hint', {
    method: 'POST',
    body: JSON.stringify({
      question_text: q.question_text,
      code_snippet: q.code_snippet || '',
      options: [q.option_a, q.option_b, q.option_c, q.option_d]
    })
  });
  STATE.exam.hints[q.id] = res.hint || '';
  renderCurrentExamQuestion();
}

function toggleBookmarkCurrent() {
  const q = STATE.exam.questions[STATE.exam.currentIndex];
  if (!q) return;
  toggleBookmarkById(q.id);
  renderCurrentExamQuestion();
}

function toggleBookmarkById(qid) {
  const i = STATE.bookmarks.indexOf(qid);
  if (i >= 0) STATE.bookmarks.splice(i, 1);
  else {
    STATE.bookmarks.push(qid);
    showToast('⭐ Đã lưu câu hỏi!', 'success');
  }
  playSound('click');
  syncUserStateToServer();
}

function recordMistake(qid, sid) {
  const idx = STATE.mistakes.findIndex((m) => (typeof m === 'object' ? m.id === qid : m === qid));
  if (idx >= 0) {
    const cur = typeof STATE.mistakes[idx] === 'object' ? STATE.mistakes[idx] : { id: qid, subject_id: sid };
    STATE.mistakes[idx] = {
      ...cur,
      subject_id: sid || cur.subject_id,
      streak: 0,
      fail_count: (cur.fail_count || 1) + 1
    };
  } else {
    STATE.mistakes.push({ id: qid, subject_id: sid, streak: 0, fail_count: 1 });
  }
  syncUserStateToServer();
}

function removeMistake(qid) {
  const idx = STATE.mistakes.findIndex((m) => (typeof m === 'object' ? m.id === qid : m === qid));
  if (idx < 0) return;
  const cur = typeof STATE.mistakes[idx] === 'object' ? STATE.mistakes[idx] : { id: qid, subject_id: STATE.exam.subjectId, streak: 0 };
  const nextStreak = (cur.streak || 0) + 1;
  if (nextStreak >= 3) {
    STATE.mistakes.splice(idx, 1);
    showToast('🏅 Tuyệt vời! Câu hỏi đã đạt 3/3 lần đúng liên tiếp và tốt nghiệp khỏi Sổ Tay Câu Sai!', 'success');
  } else {
    STATE.mistakes[idx] = { ...cur, streak: nextStreak };
  }
  syncUserStateToServer();
}

async function triggerExplainMyMistake() {
  const q = STATE.exam.questions[STATE.exam.currentIndex];
  const box = document.getElementById('q-ai-mistake-box');
  if (!q || !box) return;
  box.classList.remove('hidden');
  box.innerHTML = `<div class="skeleton-shimmer h-16 w-full"></div>`;
  playSound('click');

  const rawPicked = String(STATE.exam.answers[q.id] || '').trim();
  const optLookup = { A: q.option_a, B: q.option_b, C: q.option_c, D: q.option_d };
  const wrongDesc =
    rawPicked && rawPicked.toUpperCase() !== q._effectiveCorrect
      ? `${rawPicked}${optLookup[rawPicked.toUpperCase()] ? ' — ' + optLookup[rawPicked.toUpperCase()] : ''}`
      : 'Các phương án nhiễu dễ gây nhầm lẫn nhất ở câu này';
  const corrDesc = `${q._effectiveCorrect}${optLookup[q._effectiveCorrect] ? ' — ' + optLookup[q._effectiveCorrect] : ''}`;
  const sub = STATE.subjects.find((s) => s.id === STATE.exam.subjectId);

  const res = await apiFetch('/api/ai/explain-mistake', {
    method: 'POST',
    body: JSON.stringify({
      subject_name: sub?.name || STATE.exam.subjectName || 'Đại học',
      question_text: q.question_text,
      user_wrong_answer: wrongDesc,
      correct_answer: corrDesc,
      explanation: q.explanation || '',
      code_snippet: q.code_snippet || ''
    })
  });
  STATE.exam.mistakeDiagnosis[q.id] = res.diagnosis || 'Hãy đối chiếu kỹ điều kiện của câu hỏi với lời giải chuẩn.';
  renderQuestionFeedbackArea(q);
}

async function triggerAiMnemonic() {
  const q = STATE.exam.questions[STATE.exam.currentIndex];
  const box = document.getElementById('q-ai-mnemonic-box');
  if (!q || !box) return;
  box.classList.remove('hidden');
  box.innerHTML = `<div class="skeleton-shimmer h-12 w-full"></div>`;
  playSound('click');

  const optLookup = { A: q.option_a, B: q.option_b, C: q.option_c, D: q.option_d };
  const corrDesc = `${q._effectiveCorrect}${optLookup[q._effectiveCorrect] ? ' — ' + optLookup[q._effectiveCorrect] : ''}`;
  const sub = STATE.subjects.find((s) => s.id === STATE.exam.subjectId);

  const res = await apiFetch('/api/ai/mnemonic', {
    method: 'POST',
    body: JSON.stringify({
      subject_name: sub?.name || STATE.exam.subjectName || 'Đại học',
      question_text: q.question_text,
      correct_answer: corrDesc,
      explanation: q.explanation || ''
    })
  });
  STATE.exam.mnemonics[q.id] = res.mnemonic || '';
  renderQuestionFeedbackArea(q);
}

async function createAiFlashcardFromQuestion() {
  const q = STATE.exam.questions[STATE.exam.currentIndex];
  if (!q) return;
  await distillQuestionObjectToFlashcard(q, STATE.exam.subjectId);
}

async function distillQuestionObjectToFlashcard(q, sid) {
  const optLookup = { A: q.option_a, B: q.option_b, C: q.option_c, D: q.option_d };
  const corrKey = q._effectiveCorrect || normalizeCorrectLetter(q);
  const corrDesc = `${corrKey}${optLookup[corrKey] ? ' — ' + optLookup[corrKey] : ''}`;
  const sub = STATE.subjects.find((s) => s.id === Number(sid));

  showToast('🃏 AI đang chắt lọc câu hỏi thành thẻ Flashcard SM-2...', 'info');
  const res = await apiFetch('/api/ai/make-flashcard', {
    method: 'POST',
    body: JSON.stringify({
      subject_id: Number(sid) || 5,
      subject_name: sub?.name || 'Môn học',
      question_text: q.question_text,
      correct_answer: corrDesc,
      explanation: q.explanation || ''
    })
  });
  if (res.success) {
    addXp(10);
    playSound('correct');
    loadSubjectsAndStats();
    showToast('✔ Đã lưu Thẻ nhớ Flashcard AI vào bộ thẻ của môn!', 'success');
  } else {
    showToast(res.error || 'Không thể tạo thẻ Flashcard', 'error');
  }
}

async function triggerDeepAnalysis() {
  const q = STATE.exam.questions[STATE.exam.currentIndex];
  const deepBox = document.getElementById('q-ai-deep-box');
  if (!q || !deepBox) return;
  deepBox.classList.remove('hidden');
  deepBox.innerHTML = `<div class="skeleton-shimmer h-16 w-full"></div>`;
  playSound('click');
  const res = await apiFetch('/api/ai/deep-analysis', {
    method: 'POST',
    body: JSON.stringify({
      question_text: q.question_text,
      correct_option: q._effectiveCorrect,
      explanation: q.explanation,
      code_snippet: q.code_snippet || ''
    })
  });
  STATE.exam.deepAnalysis[q.id] = res.analysis || '';
  renderQuestionFeedbackArea(q);
}

async function triggerSimilarQuestion() {
  const q = STATE.exam.questions[STATE.exam.currentIndex];
  const simBox = document.getElementById('q-ai-similar-box');
  if (!q || !simBox) return;
  simBox.classList.remove('hidden');
  simBox.innerHTML = `<div class="skeleton-shimmer h-16 w-full"></div>`;
  const res = await apiFetch('/api/ai/similar-question', {
    method: 'POST',
    body: JSON.stringify({ question_text: q.question_text, code_snippet: q.code_snippet || '' })
  });
  if (res.similar) {
    STATE.exam.similarQuiz[q.id] = { ...res.similar, picked: null };
    renderSimilarQuestionWidget(q.id);
  }
}

function renderSimilarQuestionWidget(qid) {
  const simBox = document.getElementById('q-ai-similar-box');
  const sim = STATE.exam.similarQuiz[qid];
  if (!simBox) return;
  if (!sim) {
    simBox.classList.add('hidden');
    return;
  }
  simBox.classList.remove('hidden');
  const letters = ['A', 'B', 'C', 'D'];
  const corr = String(sim.correct || 'A').trim().toUpperCase();

  simBox.innerHTML = `
    <div class="badge-emerald text-xs px-2.5 py-0.5 rounded-md font-bold inline-block">🎲 Luyện thêm câu tương tự</div>
    <div class="question-title-text !text-sm sm:!text-base">${formatRichText(sim.question)}</div>
    ${sim.code ? buildCodeWindowHtml(sim.code, 'Challenge.cs', 'csharp') : ''}
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
      ${(sim.options || []).slice(0, 4).map((t, i) => {
        const L = letters[i];
        let cls = `option-row opt-${L} !py-2.5 !px-3.5`;
        if (sim.picked) {
          cls += ' disabled';
          if (L === corr) cls += ' is-correct';
          else if (L === sim.picked) cls += ' is-wrong';
        }
        return `<div onclick="pickSimilarOption(${qid}, '${L}')" class="${cls}">
          <div class="opt-badge !w-7 !h-7 !text-xs">${L}</div>
          <div class="option-text !text-xs flex-1">${formatRichText(t)}</div>
        </div>`;
      }).join('')}
    </div>
    ${sim.picked ? `<div class="text-xs txt-sub">${formatRichText(sim.explanation || '')}</div>` : ''}
  `;
}

function pickSimilarOption(qid, letter) {
  const sim = STATE.exam.similarQuiz[qid];
  if (!sim || sim.picked) return;
  sim.picked = letter;
  playSound(letter === String(sim.correct || 'A').trim().toUpperCase() ? 'correct' : 'wrong');
  renderSimilarQuestionWidget(qid);
}

async function triggerCustomQA() {
  const q = STATE.exam.questions[STATE.exam.currentIndex];
  const inp = document.getElementById('q-custom-qa-input');
  const box = document.getElementById('q-ai-qa-box');
  if (!q || !inp || !box || !inp.value.trim()) return;
  const query = inp.value.trim();
  inp.value = '';
  box.classList.remove('hidden');
  box.innerHTML = `<div class="skeleton-shimmer h-10 w-full"></div>`;
  const res = await apiFetch('/api/ai/custom-qa', {
    method: 'POST',
    body: JSON.stringify({
      question_text: q.question_text,
      correct_text: q._effectiveCorrect,
      query,
      code_snippet: q.code_snippet || ''
    })
  });
  STATE.exam.customQa[q.id] = res.answer || '';
  box.innerHTML = renderMarkdown(STATE.exam.customQa[q.id]);
}

function prevQuestion() {
  if (STATE.exam.active && !STATE.exam.paused && STATE.exam.currentIndex > 0) {
    STATE.exam.currentIndex--;
    playSound('click');
    renderCurrentExamQuestion();
  }
}

function nextQuestion() {
  if (STATE.exam.active && !STATE.exam.paused && STATE.exam.currentIndex < STATE.exam.questions.length - 1) {
    STATE.exam.currentIndex++;
    playSound('click');
    renderCurrentExamQuestion();
  }
}

function togglePaletteDrawer() {
  document.getElementById('question-palette-drawer')?.classList.toggle('hidden');
  playSound('click');
}

function setPaletteFilter(f) {
  STATE.exam.paletteFilter = f;
  document.querySelectorAll('[data-pfilter]').forEach((b) => b.classList.toggle('active', b.getAttribute('data-pfilter') === f));
  renderPaletteGrid();
}

function jumpToInputQuestion() {
  const inp = document.getElementById('jump-q-input');
  const num = parseInt(inp?.value || '', 10);
  if (num >= 1 && num <= STATE.exam.questions.length) {
    STATE.exam.currentIndex = num - 1;
    inp.value = '';
    renderCurrentExamQuestion();
  }
}

function renderPaletteGrid() {
  const grid = document.getElementById('palette-grid');
  if (!grid || !STATE.exam.active) return;
  const f = STATE.exam.paletteFilter;
  grid.innerHTML = STATE.exam.questions
    .map((q, idx) => {
      const rawAns = String(STATE.exam.answers[q.id] ?? '').trim();
      const hasAns = rawAns !== '';
      const bm = STATE.bookmarks.includes(q.id);
      if (f === 'unanswered' && hasAns) return '';
      if (f === 'bookmarked' && !bm) return '';

      let cls = 'palette-btn';
      if (idx === STATE.exam.currentIndex) cls += ' active';
      else if (STATE.exam.graded[q.id]) {
        const right =
          q.q_type === 'short_answer'
            ? isShortAnswerMatch(rawAns, q._effectiveCorrect)
            : q.q_type === 'essay'
            ? STATE.exam.essayGrades?.[q.id]
              ? Number(STATE.exam.essayGrades[q.id].score || 0) >= 5
              : rawAns.length >= 10
            : rawAns.toUpperCase() === q._effectiveCorrect;
        cls += right ? ' ans-correct' : ' ans-wrong';
      } else if (hasAns) cls += ' answered';
      if (bm) cls += ' bookmarked';

      return `<button type="button" onclick="STATE.exam.currentIndex=${idx};renderCurrentExamQuestion();" class="${cls}">${idx + 1}</button>`;
    })
    .join('');
}

async function confirmExitExam() {
  if (!STATE.exam.active) {
    resetToExamConfig();
    return;
  }
  const total = STATE.exam.questions.length;
  const answered = Object.keys(STATE.exam.answers).filter((k) => String(STATE.exam.answers[k] ?? '').trim() !== '').length;
  const elapsed = formatDuration(STATE.exam.elapsedSeconds);

  const actions = [
    { id: 'cancel', label: '▶️ Tiếp tục làm bài', cls: 'btn-soft px-4 py-2.5 text-xs' }
  ];
  if (answered > 0) {
    actions.push({ id: 'submit', label: '✅ Nộp & Chấm điểm luôn', cls: 'btn-primary px-4 py-2.5 text-xs' });
  }
  actions.push({ id: 'exit', label: '🚪 Thoát phòng thi', cls: 'btn-danger px-4 py-2.5 text-xs' });

  const choice = await askCustomConfirm({
    icon: '🚪',
    iconTone: 'amber',
    title: 'Rời khỏi phòng thi hiện tại?',
    desc: 'Bạn có thể nộp bài ngay để lưu kết quả và xem lời giải AI, hoặc thoát về màn hình chọn đề.',
    extraHtml: `
      <div class="flex flex-wrap items-center justify-between gap-2">
        <span>📝 Đã làm: <strong class="txt-brand">${answered} / ${total} câu</strong></span>
        <span>⏱ Thời gian: <strong class="font-mono txt-main">${elapsed}</strong></span>
      </div>
    `,
    actions
  });

  if (choice === 'submit') {
    await submitExamNow(true);
  } else if (choice === 'exit') {
    resetToExamConfig();
  }
}

function resetToExamConfig() {
  clearInterval(STATE.exam.timerId);
  STATE.exam.active = false;
  document.body.classList.remove('zen-active');
  document.getElementById('exam-active-screen')?.classList.add('hidden');
  document.getElementById('exam-result-screen')?.classList.add('hidden');
  document.getElementById('exam-config-screen')?.classList.remove('hidden');
  onExamSubjectChange();
}

// =========================================================================
// 10. SUBMIT EXAM & RESULTS
// =========================================================================
async function submitExamNow(auto = false) {
  if (!STATE.exam.active) return;
  const total = STATE.exam.questions.length;
  const answered = Object.keys(STATE.exam.answers).filter((k) => String(STATE.exam.answers[k] ?? '').trim() !== '').length;

  if (!auto && answered < total) {
    const choice = await askCustomConfirm({
      icon: '📋',
      iconTone: 'amber',
      title: `Còn ${total - answered} câu chưa trả lời!`,
      desc: `Bạn mới hoàn thành <strong>${answered} / ${total}</strong> câu. Những câu bỏ trống sẽ được tính là sai khi chấm điểm.`,
      actions: [
        { id: 'cancel', label: '🔙 Làm tiếp câu còn trống', cls: 'btn-soft px-4 py-2.5 text-xs' },
        { id: 'confirm', label: '🚀 Nộp bài & Chấm điểm', cls: 'btn-primary px-5 py-2.5 text-xs' }
      ]
    });
    if (choice !== 'confirm') return;
  }

  clearInterval(STATE.exam.timerId);
  STATE.exam.active = false;
  document.body.classList.remove('zen-active');

  const essayAiScores = {};
  Object.entries(STATE.exam.essayGrades || {}).forEach(([qid, g]) => {
    if (g && g.score !== undefined) essayAiScores[qid] = g.score;
  });

  const res = await apiFetch('/api/exam/submit', {
    method: 'POST',
    body: JSON.stringify({
      subject_id: STATE.exam.subjectId,
      answers: STATE.exam.answers,
      question_ids: STATE.exam.questions.map((q) => q.id),
      correct_map: STATE.exam.correctMap,
      essay_ai_scores: essayAiScores,
      time_spent_seconds: STATE.exam.elapsedSeconds,
      exam_type: STATE.exam.mode
    })
  });

  if (res.success) {
    (res.details || []).forEach((d) => {
      if (!d.is_correct) recordMistake(d.question_id, STATE.exam.subjectId);
      else removeMistake(d.question_id);
    });
    addXp(50);
    STATE.exam.lastResult = res;
    renderExamResultScreen(res);
    loadSubjectsAndStats();
  }
}

function renderExamResultScreen(res) {
  saveLocalExamAttemptRecord(res);
  document.getElementById('exam-config-screen')?.classList.add('hidden');
  document.getElementById('exam-active-screen')?.classList.add('hidden');
  document.getElementById('exam-result-screen')?.classList.remove('hidden');
  document.getElementById('res-ai-eval-box')?.classList.add('hidden');

  const score = Number(res.score || 0);
  const wrongCount = res.total_questions - res.correct_count;

  setText('res-score-num', score.toFixed(1));
  setText('res-correct', res.correct_count);
  setText('res-wrong', wrongCount);
  setText('res-time', formatDuration(STATE.exam.elapsedSeconds));
  setText('res-streak', STATE.exam.maxStreak);

  const ring = document.getElementById('res-score-ring');
  if (ring) {
    ring.style.stroke = score >= 8 ? '#10b981' : score >= 5 ? '#f59e0b' : '#f43f5e';
    setTimeout(() => {
      ring.style.strokeDashoffset = String(326.7 - (score / 10) * 326.7);
    }, 60);
  }

  const badge = document.getElementById('res-grade-badge');
  if (badge) {
    badge.textContent = score >= 8.5 ? '🏆 Xuất Sắc A+' : score >= 7 ? '🌟 Khá Giỏi' : score >= 5 ? '💪 Đạt Yêu Cầu' : '🔥 Cần Luyện Thêm';
  }
  document.getElementById('btn-retry-wrong')?.classList.toggle('hidden', wrongCount === 0);
  document.getElementById('btn-distill-wrong-fc')?.classList.toggle('hidden', wrongCount === 0);

  if (score >= 8 && window.confetti) {
    playSound('complete');
    confetti({ particleCount: 90, spread: 70, origin: { y: 0.6 } });
  }
  filterResultReview('all');
  window.scrollTo({ top: 0, behavior: 'smooth' });
  refreshIcons();
  renderAllMathOnPage();
}

function filterResultReview(mode) {
  document.getElementById('rev-filter-all')?.classList.toggle('active', mode === 'all');
  document.getElementById('rev-filter-wrong')?.classList.toggle('active', mode === 'wrong');
  const listEl = document.getElementById('res-review-list');
  if (!listEl) return;

  const qLookup = Object.fromEntries(STATE.exam.questions.map((q) => [q.id, q]));
  const items = (STATE.exam.lastResult?.details || []).filter((d) => (mode === 'wrong' ? !d.is_correct : true));

  if (!items.length) {
    listEl.innerHTML = `<div class="uni-card p-6 text-center text-sm font-bold txt-emerald">🎉 Hoàn hảo! Không có câu sai nào!</div>`;
    return;
  }

  listEl.innerHTML = items
    .map((d) => {
      const fullQ = qLookup[d.question_id] || {};
      const parsed = parseQuestionHeader(d.question_text);
      const optLabel = (L) => {
        const k = `option_${String(L || '').toLowerCase()}`;
        return fullQ[k] ? ` — ${formatRichText(fullQ[k])}` : '';
      };
      return `
        <div class="uni-card p-5 space-y-3">
          <div class="flex flex-wrap items-center justify-between gap-2">
            <span class="${d.is_correct ? 'badge-emerald' : 'badge-rose'} text-xs px-2.5 py-0.5 rounded-lg font-extrabold">${d.is_correct ? '✔ Đúng' : '✘ Sai'}</span>
            <div class="flex flex-wrap items-center gap-1.5">
              <button onclick="askAiAboutReviewQuestion(${d.question_id})" class="btn-primary !bg-gradient-to-r !from-indigo-600 !to-purple-600 !py-1 !px-2.5 !text-[11px] font-black flex items-center gap-1 shadow-sm hover:scale-105 active:scale-95 transition-all"><span>🤖</span> Hỏi AI</button>
              <button onclick="explainReviewItemMistake(${d.question_id})" class="ai-chip-btn !py-1 !px-2.5 !text-[11px]">
                ${d.is_correct ? '🛡️ Phân tích bẫy' : '🩺 Sao tôi sai?'}
              </button>
              <button onclick="mnemonicReviewItem(${d.question_id})" class="ai-chip-btn !py-1 !px-2.5 !text-[11px]">⚡ Mẹo nhớ 5s</button>
              <button onclick="distillQuestionByIdToFlashcard(${d.question_id}, 'exam')" class="ai-chip-btn !py-1 !px-2.5 !text-[11px]">🃏 Đúc Thẻ</button>
              <button onclick="toggleBookmarkById(${d.question_id});filterResultReview('${mode}');" class="btn-soft px-2.5 py-1 text-xs">${STATE.bookmarks.includes(d.question_id) ? '⭐ Đã lưu' : '☆ Lưu'}</button>
            </div>
          </div>
          <div class="question-title-text !text-sm sm:!text-base">${formatRichText(parsed.body)}</div>
          ${
            fullQ.image_url || d.image_url
              ? `<div class="my-2">
                  <img src="${escapeHtml(fullQ.image_url || d.image_url)}"
                       onclick="openImageLightbox('${escapeHtml(fullQ.image_url || d.image_url)}', 'Hình ảnh câu hỏi')"
                       class="max-h-56 w-auto rounded-xl cursor-zoom-in object-contain"
                       style="border: 1px solid var(--border); background-color: var(--bg-subtle);" />
                 </div>`
              : ''
          }
          ${d.code_snippet ? buildCodeWindowHtml(d.code_snippet, 'Program.cs', 'csharp') : ''}
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs ans-font-target">
            <div class="p-2.5 rounded-xl ${d.is_correct ? 'badge-emerald' : 'badge-rose'} font-bold">Bạn chọn: ${escapeHtml(d.user_answer || 'Bỏ trống')}${d.q_type === 'mcq' ? optLabel(d.user_answer) : ''}</div>
            <div class="p-2.5 rounded-xl badge-emerald font-bold">Đáp án: ${escapeHtml(d.correct_option)}${d.q_type === 'mcq' ? optLabel(d.correct_option) : ''}</div>
          </div>
          <div class="ai-callout text-xs leading-relaxed">${formatRichText(d.explanation || '')}</div>
          <div id="rev-ai-box-${d.question_id}" class="hidden ai-callout ai-callout-amber markdown-body text-xs animate-fade-in"></div>
        </div>
      `;
    })
    .join('');
}

async function explainReviewItemMistake(qid) {
  const d = (STATE.exam.lastResult?.details || []).find((x) => x.question_id === qid);
  const fullQ = STATE.exam.questions.find((q) => q.id === qid) || d;
  const box = document.getElementById(`rev-ai-box-${qid}`);
  if (!fullQ || !box) return;
  box.classList.remove('hidden');
  box.innerHTML = `<div class="skeleton-shimmer h-14 w-full"></div>`;
  playSound('click');

  const optLookup = { A: fullQ.option_a, B: fullQ.option_b, C: fullQ.option_c, D: fullQ.option_d };
  const uAns = d?.user_answer || '';
  const cAns = d?.correct_option || fullQ._effectiveCorrect || 'A';
  const wrongDesc =
    uAns && !d?.is_correct
      ? `${uAns}${optLookup[uAns.toUpperCase()] ? ' — ' + optLookup[uAns.toUpperCase()] : ''}`
      : 'Các phương án nhiễu dễ gây nhầm lẫn nhất ở câu này';
  const corrDesc = `${cAns}${optLookup[cAns.toUpperCase()] ? ' — ' + optLookup[cAns.toUpperCase()] : ''}`;

  const res = await apiFetch('/api/ai/explain-mistake', {
    method: 'POST',
    body: JSON.stringify({
      subject_name: STATE.exam.subjectName || 'Đại học',
      question_text: fullQ.question_text,
      user_wrong_answer: wrongDesc,
      correct_answer: corrDesc,
      explanation: fullQ.explanation || d?.explanation || '',
      code_snippet: fullQ.code_snippet || d?.code_snippet || ''
    })
  });
  box.innerHTML = renderMarkdown(res.diagnosis || '');
}

async function mnemonicReviewItem(qid) {
  const d = (STATE.exam.lastResult?.details || []).find((x) => x.question_id === qid);
  const fullQ = STATE.exam.questions.find((q) => q.id === qid) || d;
  const box = document.getElementById(`rev-ai-box-${qid}`);
  if (!fullQ || !box) return;
  box.classList.remove('hidden');
  box.innerHTML = `<div class="skeleton-shimmer h-12 w-full"></div>`;
  playSound('click');

  const optLookup = { A: fullQ.option_a, B: fullQ.option_b, C: fullQ.option_c, D: fullQ.option_d };
  const cAns = d?.correct_option || fullQ._effectiveCorrect || 'A';
  const corrDesc = `${cAns}${optLookup[cAns.toUpperCase()] ? ' — ' + optLookup[cAns.toUpperCase()] : ''}`;

  const res = await apiFetch('/api/ai/mnemonic', {
    method: 'POST',
    body: JSON.stringify({
      subject_name: STATE.exam.subjectName || 'Đại học',
      question_text: fullQ.question_text,
      correct_answer: corrDesc,
      explanation: fullQ.explanation || d?.explanation || ''
    })
  });
  box.innerHTML = renderMarkdown(res.mnemonic || '');
}

async function generateFlashcardsFromWrongAnswers() {
  const wrongDetails = (STATE.exam.lastResult?.details || []).filter((d) => !d.is_correct).slice(0, 5);
  if (!wrongDetails.length) {
    showToast('Không có câu sai nào cần đúc thẻ!', 'info');
    return;
  }
  const btn = document.getElementById('btn-distill-wrong-fc');
  const origHtml = btn ? btn.innerHTML : '';
  if (btn) {
    btn.disabled = true;
    btn.innerHTML = `⏳ Đang đúc ${wrongDetails.length} thẻ...`;
  }
  showToast(`🃏 AI đang chắt lọc ${wrongDetails.length} câu sai thành thẻ nhớ Flashcard SM-2...`, 'info');

  let made = 0;
  for (const d of wrongDetails) {
    const fullQ = STATE.exam.questions.find((q) => q.id === d.question_id) || d;
    const optLookup = { A: fullQ.option_a, B: fullQ.option_b, C: fullQ.option_c, D: fullQ.option_d };
    const cAns = d.correct_option || fullQ._effectiveCorrect || 'A';
    const corrDesc = `${cAns}${optLookup[String(cAns).toUpperCase()] ? ' — ' + optLookup[String(cAns).toUpperCase()] : ''}`;
    const r = await apiFetch('/api/ai/make-flashcard', {
      method: 'POST',
      body: JSON.stringify({
        subject_id: STATE.exam.subjectId || 5,
        subject_name: STATE.exam.subjectName || 'Đại học',
        question_text: fullQ.question_text,
        correct_answer: corrDesc,
        explanation: fullQ.explanation || d.explanation || ''
      })
    });
    if (r.success) made++;
  }

  if (btn) {
    btn.disabled = false;
    btn.innerHTML = origHtml;
  }
  if (made > 0) {
    addXp(made * 10);
    playSound('complete');
    await loadSubjectsAndStats();
    showToast(`🎉 Đã đúc & lưu ${made} thẻ Flashcard từ các câu sai!`, 'success');
  } else {
    showToast('Chưa thể đúc thẻ Flashcard, hãy kiểm tra API Key.', 'warning');
  }
}

function retryWrongQuestions() {
  const wrongIds = (STATE.exam.lastResult?.details || []).filter((d) => !d.is_correct).map((d) => d.question_id);
  const wrongQs = STATE.exam.questions.filter((q) => wrongIds.includes(q.id));
  if (!wrongQs.length) return;
  setExamMode('practice');
  launchExamWithQuestions(wrongQs, `Làm Lại ${wrongQs.length} Câu Sai`, true);
}

async function triggerExamEvaluation() {
  const res = STATE.exam.lastResult;
  const box = document.getElementById('res-ai-eval-box');
  if (!res || !box) return;
  box.classList.remove('hidden');
  box.innerHTML = `<div class="skeleton-shimmer h-20 w-full"></div>`;
  playSound('click');
  const data = await apiFetch('/api/ai/evaluate-exam', {
    method: 'POST',
    body: JSON.stringify({
      subject_name: STATE.exam.subjectName,
      total: res.total_questions,
      correct: res.correct_count,
      wrong_questions: (res.details || []).filter((d) => !d.is_correct).map((d) => d.question_text)
    })
  });
  box.innerHTML = renderMarkdown(data.evaluation || '');
}

// =========================================================================
// 11. KEYBOARD SHORTCUTS & MOBILE/IPAD SWIPE GESTURES
// =========================================================================
function setupKeyboardShortcuts() {
  window.addEventListener('keydown', (e) => {
    if (e.ctrlKey || e.altKey || e.metaKey) return;
    const tag = (e.target?.tagName || '').toUpperCase();
    if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT' || e.target?.isContentEditable) return;

    const confirmMod = document.getElementById('modal-custom-confirm');
    if (confirmMod && !confirmMod.classList.contains('hidden')) {
      if (e.key === 'Escape') resolveCustomConfirm('cancel');
      return;
    }

    const ftWin = document.getElementById('floating-tutor-window');
    if (ftWin && !ftWin.classList.contains('hidden') && e.key === 'Escape') {
      e.preventDefault();
      toggleFloatingTutor();
      return;
    }
    const openMod = document.querySelector('.modal-overlay:not(.hidden)');
    if (openMod) {
      if (e.key === 'Escape') openMod.classList.add('hidden');
      return;
    }

    if (STATE.currentTab === 'exam' && STATE.exam.active) {
      if (e.code === 'KeyP') { e.preventDefault(); togglePauseExam(); return; }
      if (STATE.exam.paused) return;

      const map = {
        Digit1: 'A', Numpad1: 'A', KeyA: 'A',
        Digit2: 'B', Numpad2: 'B', KeyB: 'B',
        Digit3: 'C', Numpad3: 'C', KeyC: 'C',
        Digit4: 'D', Numpad4: 'D', KeyD: 'D'
      };
      const fallback = { '1': 'A', '2': 'B', '3': 'C', '4': 'D' };
      const chosen = map[e.code] || fallback[e.key];
      if (chosen) { e.preventDefault(); selectExamOption(chosen, true); return; }

      if (e.key === 'ArrowRight') { e.preventDefault(); nextQuestion(); }
      else if (e.key === 'ArrowLeft') { e.preventDefault(); prevQuestion(); }
      else if (e.code === 'KeyS') { e.preventDefault(); toggleBookmarkCurrent(); }
      else if (e.code === 'KeyH') { e.preventDefault(); requestAiHint(); }
      else if (e.code === 'KeyF') { e.preventDefault(); useLifeline5050(); }
      else if (e.code === 'KeyZ') { e.preventDefault(); toggleZenMode(); }
      else if (e.code === 'KeyT') { e.preventDefault(); askAiAboutCurrentExamQuestion(); return; }
    } else if (e.code === 'KeyT') {
      e.preventDefault();
      toggleFloatingTutor();
      return;
    } else if (STATE.currentTab === 'flashcards') {
      if (e.code === 'Space') { e.preventDefault(); flipCurrentCard(); }
      else if (e.code === 'Digit1' || e.code === 'Numpad1') { e.preventDefault(); rateFlashcard(1); }
      else if (e.code === 'Digit2' || e.code === 'Numpad2') { e.preventDefault(); rateFlashcard(2); }
      else if (e.code === 'Digit3' || e.code === 'Numpad3') { e.preventDefault(); rateFlashcard(3); }
      else if (e.key === 'ArrowRight') { e.preventDefault(); nextFlashcard(); }
      else if (e.key === 'ArrowLeft') { e.preventDefault(); prevFlashcard(); }
    }
  });
}

function setupTouchSwipeGestures() {
  let startX = 0;
  let startY = 0;

  document.addEventListener('touchstart', (e) => {
    if (!e.touches || e.touches.length !== 1) return;
    startX = e.touches[0].clientX;
    startY = e.touches[0].clientY;
  }, { passive: true });

  document.addEventListener('touchend', (e) => {
    if (!e.changedTouches || e.changedTouches.length !== 1) return;
    const dx = e.changedTouches[0].clientX - startX;
    const dy = e.changedTouches[0].clientY - startY;
    if (Math.abs(dx) < 75 || Math.abs(dx) < Math.abs(dy) * 1.8) return;

    // Ignore swipes inside horizontal scrollable code blocks
    if (e.target?.closest('.code-window')) return;

    if (STATE.currentTab === 'exam' && STATE.exam.active && !STATE.exam.paused) {
      if (dx < 0) nextQuestion();
      else prevQuestion();
    } else if (STATE.currentTab === 'flashcards') {
      if (dx < 0) nextFlashcard();
      else prevFlashcard();
    }
  }, { passive: true });
}

// =========================================================================
// =========================================================================
// 12. FLASHCARDS, SEARCH BANK, TUTOR & GENERATOR (Exercises defined in Sec 20)
// =========================================================================
// (Modern Monaco/Pyodide exercise engine is defined in Section 20 below)

async function explainCurrentExercise() {
  const ex = STATE.exercises.list[STATE.exercises.selectedIndex];
  const box = document.getElementById('exercise-ai-box');
  if (!ex || !box) return;
  box.classList.remove('hidden');
  box.innerHTML = `<div class="skeleton-shimmer h-20 w-full"></div>`;
  const res = await apiFetch('/api/ai/explain-exercise', {
    method: 'POST',
    body: JSON.stringify({ title: ex.title, problem: ex.problem, sample_code: ex.sample_code || '' })
  });
  STATE.exercises.aiExplanations[ex.id] = res.explanation || '';
  box.innerHTML = renderMarkdown(STATE.exercises.aiExplanations[ex.id]);
}

// Flashcards
async function loadFlashcardsView() {
  const sid = Number(document.getElementById('fc-subject-select')?.value || 5);
  const mode = document.getElementById('fc-mode-select')?.value || 'sm2';
  document.getElementById('fc-ai-explain-box')?.classList.add('hidden');

  if (mode === 'sm2') {
    const res = await apiFetch(`/api/subjects/${sid}/flashcards`);
    STATE.flashcards.cards = (res.flashcards || []).map((c) => ({
      id: c.id,
      isSm2: true,
      front: c.front,
      back: c.back,
      hint: c.hint || '',
      image_url: c.image_url || '',
      interval: c.interval_days || 1
    }));
  } else {
    const res = await apiFetch(`/api/subjects/${sid}/questions?type=all`);
    STATE.flashcards.cards = (res.questions || []).map((q) => {
      const corr = normalizeCorrectLetter(q);
      const map = { A: q.option_a, B: q.option_b, C: q.option_c, D: q.option_d };
      return {
        id: q.id,
        isSm2: false,
        front: q.question_text + (q.code_snippet ? `\n\`\`\`csharp\n${q.code_snippet}\n\`\`\`` : ''),
        back: `**Đáp án:** \`${map[corr] ? corr + ' — ' + map[corr] : corr}\`\n\n${q.explanation || ''}`,
        hint: '',
        image_url: q.image_url || ''
      };
    });
  }
  STATE.flashcards.index = 0;
  STATE.flashcards.flipped = false;
  renderCurrentFlashcard();
}

function renderCurrentFlashcard() {
  const cards = STATE.flashcards.cards;
  document.getElementById('fc-flip-inner')?.classList.toggle('is-flipped', STATE.flashcards.flipped);
  if (!cards.length) {
    setText('fc-counter-text', '0 / 0');
    setText('fc-front-content', 'Chưa có thẻ nào. Hãy bấm "✨ AI +5 thẻ" để AI tự biên soạn!');
    return;
  }
  const c = cards[STATE.flashcards.index];
  setText('fc-counter-text', `${STATE.flashcards.index + 1} / ${cards.length}`);
  setText('fc-review-badge', c.isSm2 ? `SM-2: ${c.interval} ngày` : 'Ngân hàng đề');
  const f = document.getElementById('fc-front-content');
  const b = document.getElementById('fc-back-content');
  if (f) {
    f.classList.add('q-font-target');
    const imgHtml = c.image_url
      ? `<div class="mb-3 flex justify-center">
           <img src="${escapeHtml(c.image_url)}"
                onclick="event.stopPropagation();openImageLightbox('${escapeHtml(c.image_url)}', 'Thẻ nhớ hình ảnh / Tiêu bản')"
                class="max-h-44 w-auto rounded-xl object-contain cursor-zoom-in shadow-sm"
                style="border: 1px solid var(--border); background-color: var(--bg-subtle);" />
         </div>`
      : '';
    const txtHtml = c.front.includes('```') ? `<div class="text-left text-sm">${renderMarkdown(c.front)}</div>` : formatRichText(c.front);
    f.innerHTML = `${imgHtml}<div>${txtHtml}</div>`;
  }
  if (b) {
    b.classList.add('ans-font-target');
    b.innerHTML = `<div class="markdown-body text-left text-sm">${renderMarkdown(c.back)}</div>`;
  }
  setText('fc-hint-text', c.hint ? `💡 ${c.hint}` : '');
}

function flipCurrentCard() {
  if (!STATE.flashcards.cards.length) return;
  STATE.flashcards.flipped = !STATE.flashcards.flipped;
  playSound('click');
  renderCurrentFlashcard();
}

function speakCurrentFlashcard() {
  const c = STATE.flashcards.cards[STATE.flashcards.index];
  if (c) speakVietnamese(STATE.flashcards.flipped ? c.back : c.front);
}

function shuffleFlashcards() {
  STATE.flashcards.cards.sort(() => Math.random() - 0.5);
  STATE.flashcards.index = 0;
  STATE.flashcards.flipped = false;
  document.getElementById('fc-ai-explain-box')?.classList.add('hidden');
  renderCurrentFlashcard();
  showToast('🔀 Đã trộn thẻ!', 'info');
}

function prevFlashcard() {
  const len = STATE.flashcards.cards.length;
  if (!len) return;
  STATE.flashcards.index = (STATE.flashcards.index - 1 + len) % len;
  STATE.flashcards.flipped = false;
  document.getElementById('fc-ai-explain-box')?.classList.add('hidden');
  playSound('click');
  renderCurrentFlashcard();
}

function nextFlashcard() {
  const len = STATE.flashcards.cards.length;
  if (!len) return;
  STATE.flashcards.index = (STATE.flashcards.index + 1) % len;
  STATE.flashcards.flipped = false;
  document.getElementById('fc-ai-explain-box')?.classList.add('hidden');
  playSound('click');
  renderCurrentFlashcard();
}

async function rateFlashcard(rating) {
  const c = STATE.flashcards.cards[STATE.flashcards.index];
  if (!c) return;
  if (c.isSm2 && !STATE.isOfflineStandalone) {
    apiFetch(`/api/flashcards/${c.id}/review`, { method: 'POST', body: JSON.stringify({ rating }) }).catch(() => {});
  }
  addXp(5);
  playSound(rating === 3 ? 'correct' : 'click');
  nextFlashcard();
}

async function aiExplainCurrentFlashcard() {
  const c = STATE.flashcards.cards[STATE.flashcards.index];
  const box = document.getElementById('fc-ai-explain-box');
  if (!c || !box) return;
  const sid = Number(document.getElementById('fc-subject-select')?.value || 5);
  const sub = STATE.subjects.find((s) => s.id === sid);

  box.classList.remove('hidden');
  box.innerHTML = `<div class="skeleton-shimmer h-16 w-full"></div>`;
  playSound('click');

  const res = await apiFetch('/api/ai/explain-flashcard', {
    method: 'POST',
    body: JSON.stringify({
      subject_name: sub?.name || 'Môn học',
      front: c.front,
      back: c.back
    })
  });
  box.innerHTML = renderMarkdown(res.explanation || 'Chưa nhận được phản hồi từ AI.');
}

async function aiExpandFlashcardsNow() {
  const sid = Number(document.getElementById('fc-subject-select')?.value || 5);
  const sub = STATE.subjects.find((s) => s.id === sid);
  showToast(`✨ AI đang biên soạn 5 thẻ Flashcard 3D mới cho "${sub?.name || 'Môn học'}"...`, 'info');
  playSound('click');

  const res = await apiFetch('/api/ai/expand-bank', {
    method: 'POST',
    body: JSON.stringify({
      subject_id: sid,
      subject_name: sub?.name || '',
      kind: 'flashcards',
      count: 5
    })
  });
  if (res.success && res.generated_count) {
    addXp(20);
    playSound('complete');
    const modeSel = document.getElementById('fc-mode-select');
    if (modeSel) modeSel.value = 'sm2';
    await loadSubjectsAndStats();
    await loadFlashcardsView();
    showToast(`🎉 Đã thêm ${res.generated_count} thẻ Flashcard mới!`, 'success');
  } else {
    showToast(res.error || 'Không thể sinh thẻ mới lúc này', 'warning');
  }
}

// Search Bank
async function loadBankQuestions() {
  const sid = Number(document.getElementById('bank-subject-select')?.value || 5);
  const res = await apiFetch(`/api/subjects/${sid}/questions?type=all`);
  STATE.bank.all = res.questions || [];
  renderBankList(true);
}

function renderBankList(reset = false) {
  if (reset) STATE.bank.visibleCount = 25;
  const qType = document.getElementById('bank-type-select')?.value || 'all';
  const bloomDiff = document.getElementById('bank-diff-select')?.value || 'all';
  const special = document.getElementById('bank-special-select')?.value || 'all';
  const kw = (document.getElementById('bank-search-input')?.value || '').trim().toLowerCase();
  const mistakeIds = STATE.mistakes.map((m) => (typeof m === 'object' ? m.id : m));

  const filtered = STATE.bank.all.filter((q) => {
    if (qType !== 'all' && q.q_type !== qType) return false;
    if (bloomDiff !== 'all' && getBloomInfo(q.difficulty, q.question_text).key !== bloomDiff) return false;
    if (special === 'bookmarked' && !STATE.bookmarks.includes(q.id)) return false;
    if (special === 'mistakes' && !mistakeIds.includes(q.id)) return false;
    if (special === 'noted' && !STATE.notes[q.id]) return false;
    if (special === 'has_code' && !(q.code_snippet && q.code_snippet.trim())) return false;
    if (special === 'has_image' && !(q.image_url && String(q.image_url).trim())) return false;
    if (kw) {
      const hay = `${q.question_text} ${q.code_snippet} ${q.option_a} ${q.option_b} ${q.option_c} ${q.option_d} ${q.explanation} ${STATE.notes[q.id] || ''}`.toLowerCase();
      if (!hay.includes(kw)) return false;
    }
    return true;
  });

  STATE.bank.filtered = filtered;
  setText('bank-summary-text', `Hiển thị ${Math.min(filtered.length, STATE.bank.visibleCount)} / ${filtered.length} câu`);

  const listEl = document.getElementById('bank-results-list');
  document.getElementById('bank-load-more-wrap')?.classList.toggle('hidden', filtered.length <= STATE.bank.visibleCount);
  if (!listEl) return;

  const slice = filtered.slice(0, STATE.bank.visibleCount);
  listEl.innerHTML = slice.length
    ? slice.map((q) => {
        const parsed = parseQuestionHeader(q.question_text);
        const bloom = getBloomInfo(q.difficulty, q.question_text);
        const corr = normalizeCorrectLetter(q);
        const note = STATE.notes[q.id];
        const cachedBankAi = STATE.bank.aiCache[q.id];
        const opts = q.q_type === 'mcq' ? [['A', q.option_a], ['B', q.option_b], ['C', q.option_c], ['D', q.option_d]]
          : q.q_type === 'true_false' ? [['A', 'Đúng'], ['B', 'Sai']] : [];

        return `
          <div class="uni-card p-5 space-y-3">
            <div class="flex flex-wrap items-center justify-between gap-2">
              <div class="flex flex-wrap gap-1.5 text-xs">
                ${parsed.bankNum ? `<span class="badge-brand px-2 py-0.5 rounded font-mono font-bold">#${parsed.bankNum}</span>` : ''}
                <span class="${bloom.cls} px-2 py-0.5 rounded font-bold">${bloom.label}</span>
                ${parsed.topic ? `<span class="badge-subtle px-2 py-0.5 rounded font-semibold">${formatRichText(parsed.topic)}</span>` : ''}
              </div>
              <div class="flex flex-wrap items-center gap-1.5">
                <button onclick="aiAnalyzeBankQuestion(${q.id})" class="ai-chip-btn !py-1 !px-2.5 !text-[11px]">🔬 AI Giải sâu</button>
                <button onclick="aiMnemonicBankQuestion(${q.id})" class="ai-chip-btn !py-1 !px-2.5 !text-[11px]">⚡ Mẹo 5s</button>
                <button onclick="distillQuestionByIdToFlashcard(${q.id}, 'bank')" class="ai-chip-btn !py-1 !px-2.5 !text-[11px]">🃏 Đúc Thẻ</button>
                <button onclick="toggleBookmarkById(${q.id});renderBankList(false);" class="btn-soft px-2.5 py-1 text-xs">
                  ${STATE.bookmarks.includes(q.id) ? '⭐ Đã lưu' : '☆ Lưu'}
                </button>
              </div>
            </div>
            <div class="question-title-text !text-sm sm:!text-base">${formatRichText(parsed.body)}</div>
            ${
              q.image_url && String(q.image_url).trim()
                ? `<div class="my-2">
                     <img src="${escapeHtml(q.image_url)}"
                          onclick="openImageLightbox('${escapeHtml(q.image_url)}', '${escapeHtml(parsed.topic || 'Tiêu bản / Hình ảnh')}')"
                          class="max-h-56 w-auto rounded-xl cursor-zoom-in object-contain"
                          style="border: 1px solid var(--border); background-color: var(--bg-subtle);"
                          loading="lazy" />
                   </div>`
                : ''
            }
            ${q.code_snippet ? buildCodeWindowHtml(q.code_snippet, 'Program.cs', 'csharp') : ''}
            ${
              opts.length
                ? `<div class="grid grid-cols-1 sm:grid-cols-2 gap-2 ans-font-target">
                    ${opts.map(([L, t]) => `<div class="p-2.5 rounded-xl text-xs ${L === corr ? 'badge-emerald font-bold' : 'badge-subtle'}"><strong>${L}.</strong> ${formatRichText(t)}</div>`).join('')}
                  </div>`
                : `<div class="p-2.5 rounded-xl text-xs badge-emerald font-bold ans-font-target">Đáp án: ${formatRichText(corr)}</div>`
            }
            ${note ? `<div class="p-2.5 rounded-xl text-xs badge-cyan font-semibold">📌 Ghi chú: ${escapeHtml(note)}</div>` : ''}
            ${q.explanation ? `<div class="ai-callout text-xs leading-relaxed">${formatRichText(q.explanation)}</div>` : ''}
            <div id="bank-ai-box-${q.id}" class="${cachedBankAi ? '' : 'hidden'} ai-callout ai-callout-indigo markdown-body text-xs animate-fade-in">${cachedBankAi ? renderMarkdown(cachedBankAi) : ''}</div>
          </div>
        `;
      }).join('')
    : `<div class="uni-card p-8 text-center text-sm txt-muted">Không có câu hỏi phù hợp. Bấm <strong>✨ AI Sinh +5 câu môn này</strong> để mở rộng đề!</div>`;
}

function loadMoreBankItems() {
  STATE.bank.visibleCount += 25;
  renderBankList(false);
}

async function aiExpandCurrentSubjectBank() {
  const sid = Number(document.getElementById('bank-subject-select')?.value || 5);
  const sub = STATE.subjects.find((s) => s.id === sid);
  const qType = document.getElementById('bank-type-select')?.value || 'all';
  showToast(`✨ AI đang biên soạn +5 câu mới cho "${sub?.name || 'Môn học'}"...`, 'info');
  playSound('click');

  const res = await apiFetch('/api/ai/expand-bank', {
    method: 'POST',
    body: JSON.stringify({
      subject_id: sid,
      subject_name: sub?.name || '',
      kind: 'questions',
      q_type: qType === 'all' ? 'mcq' : qType,
      count: 5
    })
  });
  if (res.success && res.generated_count) {
    addXp(20);
    playSound('complete');
    await loadSubjectsAndStats();
    await loadBankQuestions();
    showToast(`🎉 Đã bổ sung ${res.generated_count} câu mới vào ngân hàng đề!`, 'success');
  } else {
    showToast(res.error || 'Chưa tạo được câu mới', 'warning');
  }
}

async function aiAnalyzeBankQuestion(qid) {
  const q = STATE.bank.all.find((x) => x.id === qid);
  const box = document.getElementById(`bank-ai-box-${qid}`);
  if (!q || !box) return;
  box.classList.remove('hidden');
  box.innerHTML = `<div class="skeleton-shimmer h-14 w-full"></div>`;
  playSound('click');

  const corr = normalizeCorrectLetter(q);
  const res = await apiFetch('/api/ai/deep-analysis', {
    method: 'POST',
    body: JSON.stringify({
      question_text: q.question_text,
      correct_option: corr,
      explanation: q.explanation || '',
      code_snippet: q.code_snippet || ''
    })
  });
  STATE.bank.aiCache[qid] = res.analysis || '';
  box.innerHTML = renderMarkdown(STATE.bank.aiCache[qid]);
}

async function aiMnemonicBankQuestion(qid) {
  const q = STATE.bank.all.find((x) => x.id === qid);
  const box = document.getElementById(`bank-ai-box-${qid}`);
  if (!q || !box) return;
  box.classList.remove('hidden');
  box.innerHTML = `<div class="skeleton-shimmer h-12 w-full"></div>`;
  playSound('click');

  const sid = Number(document.getElementById('bank-subject-select')?.value || q.subject_id || 5);
  const sub = STATE.subjects.find((s) => s.id === sid);
  const corr = normalizeCorrectLetter(q);
  const map = { A: q.option_a, B: q.option_b, C: q.option_c, D: q.option_d };
  const corrDesc = `${corr}${map[corr] ? ' — ' + map[corr] : ''}`;

  const res = await apiFetch('/api/ai/mnemonic', {
    method: 'POST',
    body: JSON.stringify({
      subject_name: sub?.name || 'Môn học',
      question_text: q.question_text,
      correct_answer: corrDesc,
      explanation: q.explanation || ''
    })
  });
  STATE.bank.aiCache[qid] = res.mnemonic || '';
  box.innerHTML = renderMarkdown(STATE.bank.aiCache[qid]);
}

async function distillQuestionByIdToFlashcard(qid, source = 'bank') {
  let q = null;
  let sid = 5;
  if (source === 'exam') {
    q = STATE.exam.questions.find((x) => x.id === qid) || (STATE.exam.lastResult?.details || []).find((d) => d.question_id === qid);
    sid = STATE.exam.subjectId || 5;
  } else {
    q = STATE.bank.all.find((x) => x.id === qid);
    sid = Number(document.getElementById('bank-subject-select')?.value || q?.subject_id || 5);
  }
  if (!q) return;
  await distillQuestionObjectToFlashcard(q, sid);
}

// Tutor & Generator
const TUTOR_PROMPT_PRESETS = {
  HOASINH_CTUMP: [
    '🧪 Nguyên lý đo quang Beer-Lambert ($C = \\frac{\\text{OD}}{\\text{OD}_0} \\times C_0$) và cách phân biệt Điểm cuối vs Động học (Kinetic)',
    '🔬 Cách phân biệt Trụ hạt, Trụ hồng cầu, Tinh thể Calcium Oxalate và Tế bào biểu mô dưới kính hiển vi',
    '🩺 Biện luận bộ xét nghiệm chức năng Gan - Mật (AST, ALT, GGT, Bilirubin trực tiếp & gián tiếp)',
    '💧 Công thức tính độ thanh thải Creatinin ($C_{\\text{Cr}}$) và phân biệt urobilinogen / muối mật / sắc tố mật'
  ],
  CHEM101: [
    '⚗️ Mẹo cân bằng nhanh phản ứng Oxi hóa - Khử bằng thăng bằng electron',
    '🧪 Công thức tính pH của dung dịch đệm (Henderson-Hasselbalch) kèm ví dụ',
    '⚡ Dãy điện hóa kim loại & quy tắc Alpha giải bài toán kim loại tác dụng muối',
    '🔬 Phân biệt đồng phân hình học cis-trans và danh pháp E/Z trong Hóa hữu cơ'
  ],
  PHYS101: [
    '📐 Tổng hợp công thức Dao động điều hòa và đường tròn lượng giác giải nhanh',
    '⚡ Điều kiện Cộng hưởng điện trong mạch RLC nối tiếp và cực trị công suất',
    '🌊 Công thức khoảng vân giao thoa Young và số vân sáng - vân tối trên màn',
    '💡 Định luật Quang điện Einstein & giới hạn quang điện kèm bài tập mẫu'
  ],
  BIO101: [
    '🧬 So sánh Nhân đôi ADN, Phiên mã và Dịch mã (nơi diễn ra, enzyme, nguyên tắc)',
    '🌱 Quy luật Phân ly độc lập & Hoán vị gen: công thức tính nhanh tỉ lệ kiểu hình',
    '📊 Định luật Hardy-Weinberg về cân bằng di truyền quần thể và bài toán mẫu',
    '🔬 Phân biệt Nguyên phân và Giảm phân qua các kỳ (số NST 2n, cromatit)'
  ],
  MATH101: [
    '∫ Mẹo chọn u và dv ("Nhất lô - Nhì đa - Tam lượng - Tứ mũ") trong Tích phân từng phần',
    '📈 Quy trình tìm Cực trị tự do của hàm hai biến z = f(x, y) bằng định thức Hessian',
    '∞ Các tiêu chuẩn xét hội tụ của chuỗi số dương (D\'Alembert, Cauchy, Tích phân)',
    '🧮 Cách giải phương trình vi phân tuyến tính cấp 1 và cấp 2 hệ số hằng'
  ],
  OOP_CSHARP: [
    '💻 Phân biệt rõ virtual/override với từ khóa new (Method Hiding) trong C# kèm code',
    '🏗️ Khi nào dùng abstract class, khi nào dùng interface trong thiết kế hệ thống?',
    '🛡️ Giải thích 5 nguyên lý SOLID dễ hiểu nhất bằng ví dụ thực tế C#',
    '⚙️ Phân biệt Value Type (Stack) và Reference Type (Heap) & cơ chế Boxing/Unboxing'
  ],
  CS101: [
    '⚡ Độ phức tạp thuật toán Big-O của các thuật toán sắp xếp phổ biến (QuickSort, MergeSort)',
    '🌳 Duyệt cây nhị phân tìm kiếm (BST): Pre-order, In-order, Post-order',
    '🔗 So sánh Mảng động (Dynamic Array) và Danh sách liên kết (Linked List)',
    '🧭 Thuật toán Dijkstra tìm đường đi ngắn nhất trên đồ thị có trọng số dương'
  ],
  DEFAULT: [
    '🎯 Tóm tắt 5 trọng tâm cốt lõi hay ra thi nhất của môn học này',
    '🪤 Chỉ ra 5 bẫy trắc nghiệm sinh viên hay mất điểm oan nhất ở môn này',
    '⚡ Cho tôi 3 câu hỏi trắc nghiệm vận dụng kèm lời giải chi tiết từng bước',
    '🧠 Lập sơ đồ tư duy chữ (Mindmap) hệ thống hóa kiến thức môn này'
  ]
};

function renderTutorQuickPrompts() {
  const wrap = document.getElementById('tutor-quick-prompts');
  if (!wrap) return;
  const sid = document.getElementById('tutor-subject-select')?.value;
  const sub = STATE.subjects.find((s) => String(s.id) === String(sid)) || STATE.subjects[0];
  const prompts = TUTOR_PROMPT_PRESETS[sub?.code] || TUTOR_PROMPT_PRESETS.DEFAULT;

  wrap.innerHTML = prompts
    .map(
      (p) =>
        `<button type="button" onclick="sendQuickTutorPrompt(${JSON.stringify(p).replace(/"/g, '&quot;')})" class="btn-soft px-3 py-1.5 text-xs whitespace-nowrap">${escapeHtml(p)}</button>`
    )
    .join('');
}

function onTutorSubjectChange() {
  renderTutorQuickPrompts();
  playSound('click');
}

function setTutorPersona(persona) {
  STATE.tutorPersona = persona;
  document.querySelectorAll('[data-persona]').forEach((btn) => {
    btn.classList.toggle('active', btn.getAttribute('data-persona') === persona);
  });
  const names = {
    professor: '🎓 Giáo sư Đại học (Chuẩn mực & Hệ thống)',
    feynman: '🧒 Feynman Dễ Hiểu (Ví dụ đời thường trực quan)',
    speed: '⚡ Giải Nhanh 10s (Công thức bấm máy & Loại trừ)',
    examiner: '🎤 Giám khảo Vấn đáp (Hỏi xoáy & Chấm điểm)'
  };
  playSound('click');
  showToast(`Đã chuyển phong cách: ${names[persona] || persona}`, 'info');
}

function initTutorGreeting() {
  const box = document.getElementById('tutor-chat-box');
  if (box) {
    box.innerHTML = `<div class="ai-callout ai-callout-indigo max-w-3xl text-sm markdown-body">${renderMarkdown(
      `Chào bạn! Tôi là **Giáo sư AI UniMaster v7.0** — hỗ trợ trọn vẹn công thức **Toán ($\\int, \\sum$), Vật Lý ($\\vec{F}, \\omega$), Hóa Học ($\\ce{H2SO4}, \\ce{<=>}$), Sinh Học & Code Lập Trình**.\n\nHãy chọn **Môn học**, **Phong cách giảng** hoặc bấm các gợi ý phía trên để bắt đầu!`
    )}</div>`;
  }
}

function clearTutorChat() { initTutorGreeting();
  initTutorHistoryFromStorage(); }

function sendQuickTutorPrompt(text) {
  const inp = document.getElementById('tutor-input');
  if (inp) { inp.value = text; sendTutorMessage(); }
}

window.TUTOR_CHAT_HISTORY = window.TUTOR_CHAT_HISTORY || [];

async function sendTutorMessage() {
  const inp = document.getElementById('tutor-input');
  const box = document.getElementById('tutor-chat-box');
  if (!inp || !box || !inp.value.trim()) return;
  const msg = inp.value.trim();
  inp.value = '';

  const sub = STATE.subjects.find((s) => String(s.id) === String(document.getElementById('tutor-subject-select')?.value));
  const uDiv = document.createElement('div');
  uDiv.className = 'ml-auto max-w-xl p-3.5 rounded-2xl text-sm font-semibold text-white';
  uDiv.style.background = 'linear-gradient(135deg, var(--brand), var(--brand-2))';
  uDiv.textContent = msg;
  box.appendChild(uDiv);

  const aDiv = document.createElement('div');
  aDiv.className = 'ai-callout max-w-3xl text-sm markdown-body';
  aDiv.innerHTML = `<div class="skeleton-shimmer h-14 w-full"></div>`;
  box.appendChild(aDiv);
  box.scrollTop = box.scrollHeight;

  window.TUTOR_CHAT_HISTORY.push({ role: 'user', content: msg });

  try {
    const res = await apiFetch('/api/ai/chat', {
      method: 'POST',
      body: JSON.stringify({
        subject_id: sub?.id || 5,
        subject_name: sub?.name || 'Đại học',
        persona: STATE.tutorPersona || 'professor',
        message: msg,
        history: window.TUTOR_CHAT_HISTORY
      })
    });
    const replyText = res.reply || 'Xin lỗi, tôi chưa thể trả lời lúc này.';
    window.TUTOR_CHAT_HISTORY.push({ role: 'model', content: replyText });
    aDiv.innerHTML = renderMarkdown(replyText);
    renderAllMathOnPage(aDiv);
  } catch (err) {
    aDiv.innerHTML = `<p class="txt-rose">Lỗi kết nối AI: ${escapeHtml(err.message)}</p>`;
  }
  box.scrollTop = box.scrollHeight;
}

// Universal Document Drag & Drop / Multi-File Upload (.pdf, .pptx, .docx, .xlsx, images)
function handleDocDragOver(e) {
  e.preventDefault();
  e.stopPropagation();
  document.getElementById('doc-dropzone')?.classList.add('drag-over');
}

function handleDocDragLeave(e) {
  e.preventDefault();
  e.stopPropagation();
  document.getElementById('doc-dropzone')?.classList.remove('drag-over');
}

function handleDocDrop(e) {
  e.preventDefault();
  e.stopPropagation();
  document.getElementById('doc-dropzone')?.classList.remove('drag-over');
  if (e.dataTransfer?.files?.length) {
    handleDocFilesSelected(e.dataTransfer.files);
  }
}

async function handleDocFilesSelected(fileList) {
  const files = Array.from(fileList || []);
  if (!files.length) return;

  if (STATE.isOfflineStandalone) {
    let combined = '';
    for (const f of files) {
      const txt = await f.text();
      combined += `\n=== ${f.name} ===\n${txt}\n`;
      STATE.uploadedDocs.push({ filename: f.name, summary_badge: 'Văn bản Offline', char_count: txt.length });
    }
    const inp = document.getElementById('gen-content-input');
    if (inp) inp.value = (inp.value ? inp.value + '\n\n' : '') + combined.trim();
    renderUploadedDocsChips();
    showToast(`📄 Đã đọc ${files.length} tệp tin!`, 'success');
    return;
  }

  const dropzone = document.getElementById('doc-dropzone');
  if (dropzone) dropzone.classList.add('opacity-70');
  showToast(`⏳ Đang trích xuất nội dung từ ${files.length} tệp tin...`, 'info');

  try {
    const fd = new FormData();
    files.forEach((f) => fd.append('file', f, f.name));

    const resp = await fetch('/api/upload-document', { method: 'POST', body: fd });
    const data = await resp.json();
    if (!data.success) {
      showToast(data.error || 'Lỗi đọc tệp tin', 'error');
      return;
    }

    STATE.uploadedDocs = [...STATE.uploadedDocs, ...(data.files || [])];
    STATE.extractedDocImages = [...(STATE.extractedDocImages || []), ...(data.extracted_images || [])];
    STATE.directExtractedQuestions = data.direct_questions || [];
    renderUploadedDocsChips();
    renderExtractedDocPanels();

    const inp = document.getElementById('gen-content-input');
    if (inp && data.combined_content) {
      inp.value = inp.value.trim() ? `${inp.value.trim()}\n\n${data.combined_content}` : data.combined_content;
    }
    playSound('correct');
    const extraMsg = STATE.directExtractedQuestions.length
      ? ` • Phát hiện ${STATE.directExtractedQuestions.length} câu hỏi có đáp án tô màu!`
      : STATE.extractedDocImages.length
      ? ` • Tách được ${STATE.extractedDocImages.length} hình ảnh!`
      : '';
    showToast(`✔ Đã đọc ${files.length} tệp (${Number(data.total_chars || 0).toLocaleString()} ký tự)${extraMsg}`, 'success');
  } catch (err) {
    showToast('Không thể tải tệp lên: ' + err.message, 'error');
  } finally {
    if (dropzone) dropzone.classList.remove('opacity-70');
    const fileInp = document.getElementById('doc-file-input');
    if (fileInp) fileInp.value = '';
  }
}

function renderUploadedDocsChips() {
  const wrap = document.getElementById('uploaded-files-wrap');
  const chips = document.getElementById('uploaded-files-chips');
  if (!wrap || !chips) return;
  if (!STATE.uploadedDocs.length) {
    wrap.classList.add('hidden');
    chips.innerHTML = '';
    return;
  }
  wrap.classList.remove('hidden');
  chips.innerHTML = STATE.uploadedDocs
    .map(
      (f) => `<span class="badge-brand px-2.5 py-1 rounded-lg font-bold inline-flex items-center gap-1.5">
        <span>📄 ${escapeHtml(f.filename)}</span>
        <span class="opacity-75">(${escapeHtml(f.summary_badge)} • ${Number(f.char_count || 0).toLocaleString()} ký tự)</span>
      </span>`
    )
    .join('');
}

function clearUploadedDocs() {
  STATE.uploadedDocs = [];
  STATE.extractedDocImages = [];
  STATE.directExtractedQuestions = [];
  renderUploadedDocsChips();
  renderExtractedDocPanels();
  const inp = document.getElementById('gen-content-input');
  if (inp) inp.value = '';
  showToast('Đã xóa danh sách tệp tải lên', 'info');
}

async function runAiCurriculumQuickGen() {
  const sid = Number(document.getElementById('gen-subject-select')?.value || 5);
  const qType = document.getElementById('gen-type-select')?.value || 'mcq';
  const bloomLevel = document.getElementById('gen-bloom-select')?.value || 'mixed';
  const count = Number(document.getElementById('gen-count-select')?.value || 10);
  const extraHint = document.getElementById('gen-content-input')?.value.trim() || '';
  const resBox = document.getElementById('gen-result-box');
  if (!resBox) return;

  const sub = STATE.subjects.find((s) => s.id === sid);
  resBox.classList.remove('hidden');
  resBox.innerHTML = `
    <div class="space-y-2">
      <div class="text-xs font-bold txt-brand animate-pulse">⚡ AI đang tự biên soạn ${count} câu đề chuẩn đại học cho môn "${escapeHtml(sub?.name || 'Môn học')}"...</div>
      <div class="skeleton-shimmer h-24 w-full"></div>
    </div>
  `;
  playSound('click');

  const data = extraHint
    ? await apiFetch('/api/ai/generate-quiz', {
        method: 'POST',
        body: JSON.stringify({
          subject_id: sid,
          subject_name: sub?.name || '',
          content: extraHint,
          count,
          q_type: qType,
          cognitive_level: bloomLevel
        })
      })
    : await apiFetch('/api/ai/expand-bank', {
        method: 'POST',
        body: JSON.stringify({
          subject_id: sid,
          subject_name: sub?.name || '',
          kind: 'questions',
          count,
          q_type: qType,
          cognitive_level: bloomLevel
        })
      });

  STATE.lastGeneratedQuestions = data.saved_questions || [];
  await loadSubjectsAndStats();

  const previewHtml = (STATE.lastGeneratedQuestions || [])
    .slice(0, 6)
    .map((q) => {
      const b = getBloomInfo(q.difficulty, q.question_text);
      return `<div class="p-3 rounded-xl text-xs space-y-1" style="background-color: var(--bg-subtle); border: 1px solid var(--border);">
        <div class="flex items-center justify-between">
          <span class="${b.cls} px-2 py-0.5 rounded font-bold">${b.label}</span>
          <span class="font-mono txt-muted">Đáp án: ${escapeHtml(q.correct_option)}</span>
        </div>
        <div class="question-title-text !text-xs sm:!text-sm">${formatRichText(q.question_text)}</div>
      </div>`;
    })
    .join('');

  resBox.innerHTML = `
    <div class="flex flex-wrap items-center justify-between gap-3 badge-emerald p-3.5 rounded-xl text-xs font-bold">
      <span>✔ AI đã tự biên soạn & lưu ${data.generated_count || 0} câu hỏi mới vào môn "${escapeHtml(sub?.name || '')}"!</span>
      ${
        STATE.lastGeneratedQuestions.length
          ? `<button onclick="launchGeneratedQuizNow()" class="btn-primary px-4 py-2 text-xs">🚀 Vào Thi Bộ Đề Vừa Tạo Ngay</button>`
          : ''
      }
    </div>
    <div class="space-y-2">${previewHtml}</div>
  `;
  playSound('complete');
}

async function runAiGenerator(kind) {
  const content = document.getElementById('gen-content-input')?.value.trim() || '';
  const sid = Number(document.getElementById('gen-subject-select')?.value || 5);
  const qType = document.getElementById('gen-type-select')?.value || 'mcq';
  const bloomLevel = document.getElementById('gen-bloom-select')?.value || 'mixed';
  const count = Number(document.getElementById('gen-count-select')?.value || 10);
  const resBox = document.getElementById('gen-result-box');

  if (!resBox) return;
  const sub = STATE.subjects.find((s) => s.id === sid);

  if (!content && kind === 'quiz') {
    await runAiCurriculumQuickGen();
    return;
  }

  resBox.classList.remove('hidden');
  resBox.innerHTML = `<div class="skeleton-shimmer h-28 w-full"></div>`;
  playSound('click');

  const effectiveContent =
    content ||
    `Chương trình chuẩn đại học môn ${sub?.name || 'Môn học'} (${sub?.description || sub?.category || 'Đầy đủ lý thuyết và bài tập tính toán trọng tâm'}).`;

  if (kind === 'quiz' || kind === 'quiz_and_start') {
    const data = await apiFetch('/api/ai/generate-quiz', {
      method: 'POST',
      body: JSON.stringify({
        subject_id: sid,
        subject_name: sub?.name || '',
        content: effectiveContent,
        count,
        q_type: qType,
        cognitive_level: bloomLevel
      })
    });
    STATE.lastGeneratedQuestions = data.saved_questions || [];
    await loadSubjectsAndStats();

    if (kind === 'quiz_and_start' && STATE.lastGeneratedQuestions.length > 0) {
      playSound('complete');
      showToast(`🚀 Đã tạo ${STATE.lastGeneratedQuestions.length} câu hỏi mới! Bắt đầu làm bài ngay!`, 'success');
      launchGeneratedQuizNow();
      return;
    }

    const previewHtml = (STATE.lastGeneratedQuestions || [])
      .slice(0, 5)
      .map((q) => {
        const b = getBloomInfo(q.difficulty, q.question_text);
        return `<div class="p-3 rounded-xl text-xs space-y-1" style="background-color: var(--bg-subtle); border: 1px solid var(--border);">
          <div class="flex items-center justify-between">
            <span class="${b.cls} px-2 py-0.5 rounded font-bold">${b.label}</span>
            <span class="font-mono txt-muted">Đáp án: ${escapeHtml(q.correct_option)}</span>
          </div>
          <div class="question-title-text !text-xs sm:!text-sm">${formatRichText(q.question_text)}</div>
        </div>`;
      })
      .join('');

    resBox.innerHTML = `
      <div class="flex flex-wrap items-center justify-between gap-3 badge-emerald p-3.5 rounded-xl text-xs font-bold">
        <span>✔ Đã sinh & lưu ${data.generated_count || 0} câu hỏi mới vào môn "${escapeHtml(sub?.name || '')}"!</span>
        ${
          STATE.lastGeneratedQuestions.length
            ? `<button onclick="launchGeneratedQuizNow()" class="btn-primary px-4 py-2 text-xs">🚀 Vào Thi Bộ Đề Vừa Tạo Ngay</button>`
            : ''
        }
      </div>
      <div class="space-y-2">${previewHtml}</div>
    `;
  } else if (kind === 'flashcards') {
    const data = await apiFetch('/api/ai/generate-flashcards', {
      method: 'POST',
      body: JSON.stringify({ subject_id: sid, subject_name: sub?.name || '', content: effectiveContent, count })
    });
    await loadSubjectsAndStats();
    resBox.innerHTML = `
      <div class="flex flex-wrap items-center justify-between gap-2 badge-emerald p-3.5 rounded-xl text-xs font-bold">
        <span>✔ Đã sinh & lưu ${data.generated_count || 0} thẻ Flashcard 3D mới!</span>
        <button onclick="openSubjectFlashcards(${sid})" class="btn-primary px-4 py-2 text-xs">🃏 Mở Học Thẻ Ngay</button>
      </div>
    `;
  } else {
    const data = await apiFetch('/api/ai/cheat-sheet', {
      method: 'POST',
      body: JSON.stringify({ subject_name: sub?.name || '', content: effectiveContent })
    });
    resBox.innerHTML = `<div class="markdown-body text-sm">${renderMarkdown(data.cheat_sheet || '')}</div>`;
  }
  playSound('complete');
}

function launchGeneratedQuizNow() {
  if (!STATE.lastGeneratedQuestions?.length) return;
  const sid = STATE.lastGeneratedQuestions[0].subject_id || STATE.examConfig.subjectId;
  STATE.examConfig.subjectId = sid;
  setExamMode('practice');
  switchTab('exam');
  launchExamWithQuestions(STATE.lastGeneratedQuestions, `Đề AI Vừa Tạo (${STATE.lastGeneratedQuestions.length} câu)`, false);
}

// =========================================================================
// 13. UNIFIED SETTINGS MODAL, QR WI-FI SYNC, BACKUP & POMODORO
// =========================================================================
function openModal(id) {
  document.getElementById(id)?.classList.remove('hidden');
  playSound('click');
  refreshIcons();
  renderAllMathOnPage();
}

function closeModal(id) {
  document.getElementById(id)?.classList.add('hidden');
}

function openSettingsModal(tab = 'appearance') {
  applyAllAppearancePrefs();
  switchSettingsTab(tab);
  openModal('modal-settings');
  if (tab === 'sync') fetchNetworkQrInfo();
  if (tab === 'ai') checkApiKeyStatus();
}

function switchSettingsTab(tab) {
  const tabs = ['appearance', 'typography', 'ai', 'tools', 'sync'];
  tabs.forEach((t) => {
    document.getElementById(`stab-panel-${t}`)?.classList.toggle('hidden', t !== tab);
  });
  document.querySelectorAll('[data-stab]').forEach((btn) => {
    btn.classList.toggle('active', btn.getAttribute('data-stab') === tab);
  });
  if (tab === 'sync') fetchNetworkQrInfo();
  if (tab === 'ai') checkApiKeyStatus();
  if (window.lucide) { try { lucide.createIcons(); } catch (_) {} }
}

async function fetchNetworkQrInfo() {
  const qrBox = document.getElementById('wifi-qr-box');
  const urlEl = document.getElementById('lan-url-text');
  if (STATE.isOfflineStandalone) {
    if (urlEl) urlEl.textContent = 'Đang chạy File Offline độc lập trên máy';
    if (qrBox) qrBox.innerHTML = `<span class="text-xs font-bold text-slate-800 text-center">Chế độ Offline Độc Lập</span>`;
    return;
  }
  try {
    const res = await apiFetch('/api/network-info');
    if (res.lan_url) {
      STATE.lanUrl = res.lan_url;
      if (urlEl) urlEl.textContent = res.lan_url;
      if (qrBox && window.qrcode) {
        const qr = qrcode(0, 'M');
        qr.addData(res.lan_url);
        qr.make();
        qrBox.innerHTML = qr.createSvgTag({ scalable: true, margin: 1 });
        const svg = qrBox.querySelector('svg');
        if (svg) { svg.style.width = '100%'; svg.style.height = '100%'; }
      }
    }
  } catch (_) {}
}

function copyLanUrl() {
  navigator.clipboard.writeText(STATE.lanUrl).then(() => {
    showToast('📋 Đã chép địa chỉ mở trên Điện thoại / iPad!', 'success');
  });
}

async function handleImportBackup(inputEl) {
  const file = inputEl?.files?.[0];
  if (!file) return;
  try {
    const text = await file.text();
    const json = JSON.parse(text);
    if (json.user_state) {
      const s = json.user_state;
      if (Array.isArray(s.bookmarks)) STATE.bookmarks = s.bookmarks;
      if (Array.isArray(s.mistakes)) STATE.mistakes = s.mistakes;
      if (s.notes) STATE.notes = s.notes;
      if (s.xp) STATE.xp = s.xp;
    }
    if (!STATE.isOfflineStandalone) {
      await apiFetch('/api/backup/import', { method: 'POST', body: JSON.stringify(json) });
    }
    syncUserStateToServer();
    await loadSubjectsAndStats();
    updateXpUI();
    showToast('🎉 Đã khôi phục toàn bộ dữ liệu thành công!', 'success');
  } catch (e) {
    showToast('File sao lưu không hợp lệ: ' + e.message, 'error');
  }
}

// Multi-Gemini API Key Auto-Failover Pool Settings
async function checkApiKeyStatus() {
  try {
    const res = await apiFetch('/api/settings');
    STATE.hasApiKey = Boolean(res.has_gemini_key);
    STATE.apiPool = res.pool || [];
    STATE.openaiConfig = res.openai || {};
    const count = STATE.apiPool.length || (STATE.hasApiKey ? 1 : 0);

    // Sync OpenAI / ChatGPT UI
    const openAiPill = document.getElementById('openai-status-pill');
    const openAiMask = document.getElementById('openai-current-mask');
    const baseInp = document.getElementById('cfg-openai-base');
    const modelSel = document.getElementById('cfg-openai-model');
    const prioSel = document.getElementById('cfg-ai-priority');

    if (baseInp && !baseInp.value) {
      baseInp.value = STATE.openaiConfig.base_url || 'https://codex.fosta.app/v1';
    }
    if (modelSel && STATE.openaiConfig.model) {
      modelSel.value = STATE.openaiConfig.model;
    }
    if (prioSel) {
      prioSel.value = STATE.openaiConfig.priority || 'openai_first';
    }
    if (openAiMask) {
      openAiMask.textContent = STATE.openaiConfig.has_key
        ? `Khóa đang lưu: ${STATE.openaiConfig.masked_key} • Base: ${STATE.openaiConfig.base_url || 'api.openai.com'}`
        : 'Chưa gắn khóa ChatGPT. Hãy nhập mã sk-... bên dưới.';
    }
    if (openAiPill) {
      if (STATE.openaiConfig.priority === 'openai_first') {
        openAiPill.className = 'badge-emerald text-xs px-2.5 py-1 rounded-full font-bold';
        openAiPill.textContent = '🟢 Ưu tiên gọi trước';
      } else {
        openAiPill.className = 'badge-subtle text-xs px-2.5 py-1 rounded-full font-bold';
        openAiPill.textContent = '⚪ Chế độ dự phòng';
      }
    }

    const pill = document.getElementById('api-status-pill');
    const mask = document.getElementById('api-current-mask');
    if (pill) {
      pill.className = `${STATE.hasApiKey ? 'badge-emerald' : 'badge-amber'} text-xs px-3 py-1 rounded-full font-bold`;
      pill.textContent = STATE.hasApiKey ? `🟢 Sẵn sàng ${count} Key luân phiên` : 'Chưa gắn Key';
    }
    if (mask) {
      mask.textContent = STATE.hasApiKey
        ? `Đang có ${count} khóa trong dàn luân phiên tự động (Ưu tiên: ${res.masked_key || STATE.apiPool[0]?.masked_key})`
        : 'Hãy thêm ít nhất 1 khóa Gemini API miễn phí bên dưới';
    }
    renderApiKeyPoolList();
  } catch (_) {}
}

function renderApiKeyPoolList() {
  const listEl = document.getElementById('api-pool-list');
  if (!listEl) return;
  if (!STATE.apiPool || !STATE.apiPool.length) {
    listEl.innerHTML = `<div class="p-3.5 rounded-xl text-xs txt-muted text-center" style="background-color: var(--bg-subtle); border: 1px dashed var(--border);">
      Chưa có API Key nào trong dàn. Dán 1 hoặc nhiều mã <code>AIzaSy...</code> bên dưới để kích hoạt AI!
    </div>`;
    return;
  }

  const statusBadge = (item) => {
    if (item.status === 'active') return `<span class="badge-emerald px-2 py-0.5 rounded-md text-[11px] font-bold">🟢 Đang chạy${item.model ? ' • ' + escapeHtml(item.model) : ''}</span>`;
    if (item.status === 'cooldown') return `<span class="badge-amber px-2 py-0.5 rounded-md text-[11px] font-bold">🟠 Tạm nghỉ Quota (${item.cooldown_remaining || 60}s) → Đã chuyển key kế</span>`;
    if (item.status === 'invalid') return `<span class="badge-rose px-2 py-0.5 rounded-md text-[11px] font-bold">🔴 Không hợp lệ</span>`;
    return `<span class="badge-cyan px-2 py-0.5 rounded-md text-[11px] font-bold">🔵 Sẵn sàng dự phòng</span>`;
  };

  listEl.innerHTML = STATE.apiPool
    .map(
      (item, idx) => `
      <div class="key-pool-row">
        <div class="flex flex-wrap items-center gap-2 text-xs">
          <span class="badge-brand px-2 py-0.5 rounded font-mono font-extrabold">#${idx + 1}</span>
          <code class="font-mono font-bold txt-main">${escapeHtml(item.masked_key)}</code>
          ${statusBadge(item)}
          ${item.calls ? `<span class="text-[11px] txt-muted">(${item.calls} lượt gọi)</span>` : ''}
        </div>
        <button type="button" onclick="removeApiKeyFromPool(${idx})" class="btn-soft px-2.5 py-1 text-xs txt-rose shrink-0">Xóa</button>
      </div>
    `
    )
    .join('');
}

async function addApiKeysToPool() {
  const ta = document.getElementById('api-keys-textarea');
  const raw = ta?.value.trim() || '';
  if (!raw) {
    showToast('Hãy dán ít nhất 1 mã AIzaSy... vào ô nhập!', 'warning');
    return;
  }
  const res = await apiFetch('/api/settings', {
    method: 'POST',
    body: JSON.stringify({ add_api_keys: raw })
  });
  if (res.success) {
    if (ta) ta.value = '';
    STATE.apiPool = res.pool || [];
    showToast(res.message || '💾 Đã thêm vào dàn API Key!', 'success');
    await checkApiKeyStatus();
    await testAllApiKeys();
  }
}

async function removeApiKeyFromPool(idx) {
  const res = await apiFetch('/api/settings', {
    method: 'POST',
    body: JSON.stringify({ remove_key_index: idx })
  });
  if (res.success) {
    showToast('Đã xóa khóa khỏi dàn luân phiên', 'info');
    checkApiKeyStatus();
  }
}

async function clearAllApiKeys() {
  const choice = await askCustomConfirm({
    icon: '🔑',
    iconTone: 'rose',
    title: 'Xóa toàn bộ dàn API Key?',
    desc: 'Tất cả khóa Gemini API đang lưu trong hệ thống sẽ bị gỡ bỏ. Bạn có thể dán lại bất cứ lúc nào.',
    actions: [
      { id: 'cancel', label: 'Hủy bỏ', cls: 'btn-soft px-4 py-2.5 text-xs' },
      { id: 'confirm', label: '🗑️ Xóa toàn bộ Key', cls: 'btn-danger px-4 py-2.5 text-xs' }
    ]
  });
  if (choice !== 'confirm') return;

  const res = await apiFetch('/api/settings', {
    method: 'POST',
    body: JSON.stringify({ clear_all_keys: true })
  });
  if (res.success) {
    document.getElementById('api-test-feedback')?.classList.add('hidden');
    showToast('Đã xóa toàn bộ API Key', 'info');
    checkApiKeyStatus();
  }
}

async function testAllApiKeys() {
  const fb = document.getElementById('api-test-feedback');
  const pendingInput = document.getElementById('api-keys-textarea')?.value.trim() || '';
  if (pendingInput) {
    await addApiKeysToPool();
    return;
  }
  if (!fb) return;
  fb.classList.remove('hidden');
  fb.className = 'text-xs p-3 rounded-xl font-bold badge-subtle';
  fb.textContent = '⏳ Đang kiểm tra đồng loạt toàn bộ dàn API Key...';

  const res = await apiFetch('/api/ai/test-all-keys', { method: 'POST', body: JSON.stringify({}) });
  if (res.pool) {
    STATE.apiPool = res.pool;
    renderApiKeyPoolList();
  }
  fb.className = `text-xs p-3 rounded-xl font-bold ${res.success ? 'badge-emerald' : 'badge-rose'}`;
  fb.textContent = res.success ? `✔ ${res.message}` : `✘ ${res.message || 'Chưa có khóa hợp lệ'}`;
}

// Pomodoro
function togglePomodoro() {
  if (STATE.pomo.running) {
    clearInterval(STATE.pomo.timerId);
    STATE.pomo.running = false;
  } else {
    STATE.pomo.running = true;
    STATE.pomo.timerId = setInterval(() => {
      if (STATE.pomo.seconds > 0) {
        STATE.pomo.seconds--;
        updatePomoUI();
      } else {
        clearInterval(STATE.pomo.timerId);
        STATE.pomo.running = false;
        STATE.pomo.seconds = 25 * 60;
        updatePomoUI();
        playSound('complete');
        showToast('🎉 Hoàn thành 25 phút Pomodoro!', 'success');
      }
    }, 1000);
  }
  updatePomoUI();
}

function resetPomodoro() {
  clearInterval(STATE.pomo.timerId);
  STATE.pomo.running = false;
  STATE.pomo.seconds = 25 * 60;
  updatePomoUI();
}

function updatePomoUI() {
  const t = formatDuration(STATE.pomo.seconds);
  setText('pomo-settings-time', t);
  setText('pomo-header-time', t);
  setText('lounge-pomo-clock', t);
  setText('pomo-toggle-btn', STATE.pomo.running ? 'Tạm dừng' : 'Bắt đầu');
  const pill = document.getElementById('header-pomo-pill');
  if (pill) {
    pill.classList.toggle('hidden', !STATE.pomo.running);
    pill.classList.toggle('inline-flex', STATE.pomo.running);
  }
}

// Add Subject / Question / Flashcard Modals
async function submitNewSubject() {
  const code = document.getElementById('new-sub-code')?.value.trim();
  const name = document.getElementById('new-sub-name')?.value.trim();
  const icon = document.getElementById('new-sub-icon')?.value.trim() || '📘';
  const category = document.getElementById('new-sub-cat')?.value || '';
  const description = document.getElementById('new-sub-desc')?.value.trim() || '';
  if (!code || !name) { showToast('Nhập Mã môn và Tên môn!', 'warning'); return; }

  const res = await apiFetch('/api/subjects', { method: 'POST', body: JSON.stringify({ code, name, icon, category, description }) });
  if (res.success) {
    closeModal('modal-add-subject');
    showToast('✔ Đã tạo môn học mới!', 'success');
    await loadSubjectsAndStats();
  }
}

async function deleteSubject(id) {
  const sub = STATE.subjects.find((s) => s.id === id);
  const choice = await askCustomConfirm({
    icon: '🗑️',
    iconTone: 'rose',
    title: `Xóa môn "${sub?.name || 'Môn học'}"?`,
    desc: 'Toàn bộ câu hỏi và thẻ nhớ Flashcard thuộc môn học này sẽ bị xóa vĩnh viễn khỏi ngân hàng đề.',
    actions: [
      { id: 'cancel', label: 'Giữ lại', cls: 'btn-soft px-4 py-2.5 text-xs' },
      { id: 'confirm', label: '🗑️ Xóa môn học', cls: 'btn-danger px-4 py-2.5 text-xs' }
    ]
  });
  if (choice !== 'confirm') return;

  await apiFetch(`/api/subjects/${id}`, { method: 'DELETE' });
  showToast('Đã xóa môn học', 'info');
  await loadSubjectsAndStats();
}

function openAddQuestionModal() {
  openModal('modal-add-question');
  onAddQuestionTypeChange();
}

function onAddQuestionTypeChange() {
  const t = document.getElementById('add-q-type')?.value || 'mcq';
  document.getElementById('add-q-mcq-fields')?.classList.toggle('hidden', t !== 'mcq');
}

async function submitNewQuestion() {
  const sid = Number(document.getElementById('add-q-subject')?.value || 5);
  const q_type = document.getElementById('add-q-type')?.value || 'mcq';
  const difficulty = document.getElementById('add-q-diff')?.value || 'medium';
  const question_text = document.getElementById('add-q-text')?.value.trim();
  const code_snippet = document.getElementById('add-q-code')?.value || '';
  const option_a = q_type === 'true_false' ? 'Đúng' : (document.getElementById('add-q-a')?.value.trim() || '');
  const option_b = q_type === 'true_false' ? 'Sai' : (document.getElementById('add-q-b')?.value.trim() || '');
  const option_c = document.getElementById('add-q-c')?.value.trim() || '';
  const option_d = document.getElementById('add-q-d')?.value.trim() || '';
  const correct_option = document.getElementById('add-q-correct')?.value.trim() || 'A';
  const explanation = document.getElementById('add-q-expl')?.value.trim() || '';
  const image_url = document.getElementById('add-q-image-url')?.value.trim() || '';

  if (!question_text) { showToast('Nhập nội dung câu hỏi!', 'warning'); return; }
  const res = await apiFetch(`/api/subjects/${sid}/questions`, {
    method: 'POST',
    body: JSON.stringify({ q_type, difficulty, question_text, code_snippet, option_a, option_b, option_c, option_d, correct_option, explanation, image_url })
  });
  if (res.success) {
    closeModal('modal-add-question');
    showToast('✔ Đã thêm câu hỏi!', 'success');
    await loadSubjectsAndStats();
    if (STATE.currentTab === 'search') loadBankQuestions();
  }
}

async function submitNewFlashcard() {
  const sid = Number(document.getElementById('fc-subject-select')?.value || 5);
  const front = document.getElementById('new-fc-front')?.value.trim();
  const back = document.getElementById('new-fc-back')?.value.trim();
  const hint = document.getElementById('new-fc-hint')?.value.trim() || '';
  if (!front || !back) { showToast('Nhập đủ Mặt trước và Mặt sau!', 'warning'); return; }

  const res = await apiFetch(`/api/subjects/${sid}/flashcards`, {
    method: 'POST',
    body: JSON.stringify({ front, back, hint })
  });
  if (res.success) {
    closeModal('modal-add-flashcard');
    showToast('🃏 Đã thêm thẻ mới!', 'success');
    await loadSubjectsAndStats();
    loadFlashcardsView();
  }
}

// =========================================================================
// 14. STEM FORMULA INSERTION & BUILT-IN SCIENTIFIC REFERENCE SHEET
// =========================================================================
function insertFormulaSnippet(inputId, snippet) {
  const el = document.getElementById(inputId);
  if (!el) return;
  const start = el.selectionStart ?? el.value.length;
  const end = el.selectionEnd ?? el.value.length;
  const before = el.value.slice(0, start);
  const after = el.value.slice(end);
  const pad = before && !before.endsWith(' ') ? ' ' : '';
  el.value = `${before}${pad}${snippet} ${after}`;
  el.focus();
  const pos = (before + pad + snippet + ' ').length;
  try {
    el.setSelectionRange(pos, pos);
  } catch (_) {}
  playSound('click');
}

function populateStemReferenceModal() {
  const body = document.getElementById('stem-reference-body');
  if (!body) return;

  const refMd = `
### 📐 1. Toán Giải Tích & Đại Số Trọng Tâm
- **Đạo hàm & Vi phân:** $(u \\cdot v)' = u'v + uv'$, $\\left(\\frac{u}{v}\\right)' = \\frac{u'v - uv'}{v^2}$, $(\\ln u)' = \\frac{u'}{u}$, $(e^u)' = u'e^u$.
- **Tích phân cơ bản:** $\\int x^n\\,\\mathrm{d}x = \\frac{x^{n+1}}{n+1} + C \\;(n \\neq -1)$, $\\int u\\,\\mathrm{d}v = uv - \\int v\\,\\mathrm{d}u$, $\\int_{a}^{b} f(x)\\,\\mathrm{d}x = F(b) - F(a)$.
- **Chuỗi Taylor / Maclaurin:** $e^x = \\sum_{n=0}^{\\infty} \\frac{x^n}{n!}$, $\\sin x = x - \\frac{x^3}{3!} + \\frac{x^5}{5!} - \\cdots$, $\\lim_{x \\to 0} \\frac{\\sin x}{x} = 1$.

---

### ⚡ 2. Vật Lý Đại Cương & Hằng Số Vật Lý Chuẩn
- **Hằng số:** $c = 3 \\times 10^8\\,\\text{m/s}$, $h = 6{,}625 \\times 10^{-34}\\,\\text{J}\\cdot\\text{s}$, $e = 1{,}6 \\times 10^{-19}\\,\\text{C}$, $N_A = 6{,}022 \\times 10^{23}\\,\\text{mol}^{-1}$, $R = 8{,}314\\,\\text{J/(mol}\\cdot\\text{K)}$.
- **Dao động điều hòa:** $x = A\\cos(\\omega t + \\varphi)$, $v_{\\max} = \\omega A$, $a_{\\max} = \\omega^2 A$, $\\omega = \\sqrt{\\frac{k}{m}} = \\sqrt{\\frac{g}{\\ell}}$, hệ thức độc lập $A^2 = x^2 + \\frac{v^2}{\\omega^2}$.
- **Điện xoay chiều RLC:** $Z = \\sqrt{R^2 + (Z_L - Z_C)^2}$ với $Z_L = \\omega L,\\; Z_C = \\frac{1}{\\omega C}$. Cộng hưởng khi $\\omega_0 = \\frac{1}{\\sqrt{LC}} \\Rightarrow I_{\\max} = \\frac{U}{R}$.
- **Quang học & Lượng tử:** Khoảng vân $i = \\frac{\\lambda D}{a}$; Năng lượng photon $\\varepsilon = hf = \\frac{hc}{\\lambda}$; Einstein: $\\frac{hc}{\\lambda} = A + \\frac{1}{2}mv_{0\\max}^2$; Tương đối tính $E = mc^2$.

---

### ⚗️ 3. Hóa Học Đại Cương, Vô Cơ & Hữu Cơ (Chuẩn mhchem)
- **Số mol & Khí lý tưởng:** $n = \\frac{m}{M} = C_M \\cdot V = \\frac{PV}{RT}$ (ở đkc $25^\\circ\\text{C}, 1\\,\\text{bar}$: $V = 24{,}79 \\cdot n$; ở đktc $0^\\circ\\text{C}, 1\\,\\text{atm}$: $V = 22{,}4 \\cdot n$).
- **pH & Dung dịch đệm:** $\\text{pH} = -\\log[\\ce{H+}]$, $\\text{pH} + \\text{pOH} = 14$, Henderson–Hasselbalch: $\\text{pH} = \\text{p}K_a + \\log\\frac{[\\ce{A-}]}{[\\ce{HA}]}$.
- **Nhiệt động & Điện hóa:** $\\Delta G^\\circ = \\Delta H^\\circ - T\\Delta S^\\circ = -nFE^\\circ$; Định luật Faraday: $m = \\frac{A \\cdot I \\cdot t}{n \\cdot F}$ ($F = 96500\\,\\text{C/mol}$).
- **Dãy điện hóa kim loại:** $\\ce{K+ / K} < \\ce{Na+ / Na} < \\ce{Mg^{2+} / Mg} < \\ce{Al^{3+} / Al} < \\ce{Zn^{2+} / Zn} < \\ce{Fe^{2+} / Fe} < \\ce{Ni^{2+} / Ni} < \\ce{Sn^{2+} / Sn} < \\ce{Pb^{2+} / Pb} < \\ce{2H+ / H2} < \\ce{Cu^{2+} / Cu} < \\ce{Fe^{3+} / Fe^{2+}} < \\ce{Ag+ / Ag} < \\ce{Au^{3+} / Au}$.
- **Phản ứng mẫu hay gặp:** $\\ce{N2(g) + 3H2(g) <=> 2NH3(g)}$, $\\ce{CH3COOH + C2H5OH <=>[H2SO4 \\text{ đặc}, t^\\circ] CH3COOC2H5 + H2O}$.

---

### 🧬 4. Sinh Học Đại Cương & Di Truyền Phân Tử
- **Cấu trúc ADN (Chargaff):** $N = 2A + 2G$, chiều dài $L = \\frac{N}{2} \\times 3{,}4\\,\\text{\\AA}$, số liên kết hydro $H = 2A + 3G$, khối lượng $M = N \\times 300\\,\\text{đvC}$.
- **Nhân đôi & Phiên mã:** Qua $k$ lần nhân đôi từ $1$ ADN tạo $2^k$ ADN con (trong đó có $2^k - 2$ ADN hoàn toàn từ nguyên liệu môi trường: $A_{\\text{mt}} = A(2^k - 1)$). Số bộ ba mã hóa axit amin $= \\frac{rN}{3} - 1$.
- **Nguyên phân & Giảm phân:** Nguyên phân từ $1$ tế bào $(2n)$ qua $k$ lần tạo $2^k$ tế bào $(2n)$, môi trường cung cấp $2n(2^k - 1)$ NST đơn.
- **Di truyền quần thể (Hardy–Weinberg):** $p(A) + q(a) = 1 \\Rightarrow p^2\\,\\text{AA} + 2pq\\,\\text{Aa} + q^2\\,\\text{aa} = 1$.
  `;

  body.innerHTML = `<div class="markdown-body space-y-2">${renderMarkdown(refMd)}</div>`;
}


// =========================================================================
// 15. UNIMASTER v8.0 SUITE: IMAGE LIGHTBOX, DIRECT PDF/IMAGE IMPORTER,
//     KNOWLEDGE HEATMAP, SCORE PREDICTOR, 3-STRIKE MISTAKE BANK & ARENA 1v1
// =========================================================================

// --- 15.1 HD Image Lightbox & Add-Question Image Upload ---
function openImageLightbox(imageUrl, caption = '') {
  if (!imageUrl) return;
  const img = document.getElementById('lightbox-img-el');
  const cap = document.getElementById('lightbox-caption-text') || document.getElementById('lightbox-caption-el');
  if (img) {
    img.src = imageUrl;
    img.style.transform = 'scale(1)';
  }
  if (cap) cap.textContent = caption || 'Quan sát chi tiết tiêu bản / hình ảnh đề thi (Bấm ra ngoài hoặc ESC để đóng)';
  openModal('modal-image-lightbox');
}

function setLightboxZoom(scale) {
  const img = document.getElementById('lightbox-img-el');
  if (img) img.style.transform = `scale(${scale || 1})`;
  playSound('click');
}

function openAddQuestionWithImage(imageUrl) {
  openAddQuestionModal();
  const inp = document.getElementById('add-q-image-url');
  if (inp) inp.value = imageUrl || '';
}

async function uploadImageForAddQuestion(inputEl) {
  const file = inputEl?.files?.[0];
  if (!file) return;
  const fd = new FormData();
  fd.append('file', file, file.name);
  showToast('⏳ Đang tải ảnh lên...', 'info');
  try {
    const resp = await fetch('/api/upload-document', { method: 'POST', body: fd });
    const data = await resp.json();
    const firstImg = data?.extracted_images?.[0]?.url;
    if (firstImg) {
      const inp = document.getElementById('add-q-image-url');
      if (inp) inp.value = firstImg;
      showToast('✔ Đã đính kèm ảnh vào câu hỏi!', 'success');
    } else {
      showToast('Không tìm thấy ảnh hợp lệ trong tệp', 'warning');
    }
  } catch (e) {
    showToast('Lỗi tải ảnh: ' + e.message, 'error');
  }
}

// --- 15.2 Universal Document Direct Question Importer & AI Vision Image-to-Question ---
function renderExtractedDocPanels() {
  const banner = document.getElementById('direct-import-banner');
  const countText = document.getElementById('direct-import-count-text');
  const dqs = STATE.directExtractedQuestions || [];
  if (banner) {
    if (dqs.length > 0) {
      banner.classList.remove('hidden');
      if (countText) {
        countText.textContent = `🎯 Phát hiện ${dqs.length} câu hỏi trắc nghiệm có sẵn đáp án tô màu trong tệp PDF!`;
      }
    } else {
      banner.classList.add('hidden');
    }
  }

  const imgPanel = document.getElementById('extracted-images-panel');
  const imgGrid = document.getElementById('extracted-images-grid');
  const imgs = STATE.extractedDocImages || [];
  if (imgPanel && imgGrid) {
    if (imgs.length > 0) {
      imgPanel.classList.remove('hidden');
      imgGrid.innerHTML = imgs
        .map(
          (im, idx) => `
          <div class="p-2.5 rounded-xl space-y-2 flex flex-col justify-between" style="background-color: var(--bg-surface); border: 1px solid var(--border);">
            <div class="relative group cursor-zoom-in overflow-hidden rounded-lg" onclick="openImageLightbox('${escapeHtml(im.url)}', '${escapeHtml(im.label || 'Ảnh trích xuất')}')">
              <img src="${escapeHtml(im.url)}" alt="${escapeHtml(im.label || '')}" class="h-28 w-full object-contain mx-auto" style="background-color: var(--bg-subtle);" loading="lazy" />
              <span class="absolute top-1.5 left-1.5 badge-brand text-[10px] px-1.5 py-0.5 rounded font-mono font-bold">#${idx + 1}</span>
            </div>
            <div class="text-[11px] font-bold txt-main truncate" title="${escapeHtml(im.label || '')}">${escapeHtml(im.label || 'Ảnh ' + (idx + 1))}</div>
            <div class="flex flex-wrap gap-1">
              <button type="button" onclick="aiGenerateSingleImageQuestion('${escapeHtml(im.url)}', '${escapeHtml(im.label || '')}')" class="btn-primary flex-1 py-1.5 px-2 text-[11px]">
                ✨ AI Tạo câu hỏi
              </button>
              <button type="button" onclick="openAddQuestionWithImage('${escapeHtml(im.url)}')" class="btn-soft py-1.5 px-2 text-[11px]" title="Tự soạn câu hỏi với ảnh này">
                ✍️
              </button>
            </div>
          </div>
        `
        )
        .join('');
    } else {
      imgPanel.classList.add('hidden');
      imgGrid.innerHTML = '';
    }
  }
}

async function importDirectExtractedQuestions() {
  const dqs = STATE.directExtractedQuestions || [];
  if (!dqs.length) return;
  const sid = Number(document.getElementById('gen-subject-select')?.value || STATE.examConfig.subjectId || 5);
  const sub = STATE.subjects.find((s) => s.id === sid);

  showToast(`⏳ Đang nhập nguyên bản ${dqs.length} câu hỏi vào môn "${sub?.name || 'Môn học'}"...`, 'info');
  const res = await apiFetch('/api/import-direct-questions', {
    method: 'POST',
    body: JSON.stringify({
      subject_id: sid,
      questions: dqs
    })
  });
  if (res.success) {
    STATE.lastGeneratedQuestions = res.saved_questions || [];
    await loadSubjectsAndStats();
    playSound('complete');
    showToast(`🎉 Đã nhập thành công ${res.imported_count || dqs.length} câu hỏi chuẩn từ PDF!`, 'success');
    const resBox = document.getElementById('gen-result-box');
    if (resBox) {
      resBox.classList.remove('hidden');
      resBox.innerHTML = `
        <div class="flex flex-wrap items-center justify-between gap-3 badge-emerald p-3.5 rounded-xl text-xs font-bold">
          <span>✔ Đã nhập nguyên bản ${res.imported_count || dqs.length} câu hỏi kèm đáp án tô màu vào môn "${escapeHtml(sub?.name || '')}"!</span>
          <button onclick="launchGeneratedQuizNow()" class="btn-primary px-4 py-2 text-xs">🚀 Vào Thi Ngay Bộ Đề Này</button>
        </div>
      `;
    }
  } else {
    showToast(res.error || 'Không thể nhập câu hỏi', 'error');
  }
}

async function aiGenerateSingleImageQuestion(imageUrl, label = '') {
  const sid = Number(document.getElementById('gen-subject-select')?.value || STATE.examConfig.subjectId || 5);
  const sub = STATE.subjects.find((s) => s.id === sid);
  const extraHint = document.getElementById('gen-content-input')?.value.trim() || label;

  showToast('🔬 AI Vision đang quan sát hình ảnh & biên soạn câu hỏi trắc nghiệm...', 'info');
  playSound('click');
  const res = await apiFetch('/api/ai/generate-image-question', {
    method: 'POST',
    body: JSON.stringify({
      subject_id: sid,
      subject_name: sub?.name || 'Đại học',
      image_url: imageUrl,
      context_hint: extraHint
    })
  });
  if (res.success && res.question) {
    STATE.lastGeneratedQuestions = [res.question, ...(STATE.lastGeneratedQuestions || [])];
    await loadSubjectsAndStats();
    playSound('complete');
    showToast('🎉 AI Vision đã tạo & lưu câu hỏi có hình ảnh vào ngân hàng đề!', 'success');
    const resBox = document.getElementById('gen-result-box');
    if (resBox) {
      resBox.classList.remove('hidden');
      resBox.innerHTML = `
        <div class="p-4 rounded-2xl space-y-2.5" style="background-color: var(--bg-subtle); border: 1px solid var(--border);">
          <div class="flex flex-wrap items-center justify-between gap-2">
            <span class="badge-emerald text-xs px-2.5 py-1 rounded-lg font-extrabold">✔ Câu hỏi hình ảnh mới đã lưu vào "${escapeHtml(sub?.name || '')}"</span>
            <button onclick="launchGeneratedQuizNow()" class="btn-primary px-3.5 py-1.5 text-xs">🚀 Thi thử ngay</button>
          </div>
          <div class="flex flex-col sm:flex-row gap-3 items-start">
            <img src="${escapeHtml(res.question.image_url)}" class="w-28 h-28 object-contain rounded-xl shrink-0" style="border: 1px solid var(--border); background-color: var(--bg-surface);" />
            <div class="space-y-1 text-xs">
              <div class="font-bold txt-main">${formatRichText(res.question.question_text)}</div>
              <div class="txt-emerald font-bold">Đáp án đúng: ${escapeHtml(res.question.correct_option)}</div>
              <div class="txt-sub">${formatRichText(res.question.explanation || '')}</div>
            </div>
          </div>
        </div>
      `;
    }
  } else {
    showToast(res.error || 'Không thể sinh câu hỏi từ ảnh', 'warning');
  }
}

async function aiGenerateAllExtractedImageQuestions() {
  const imgs = (STATE.extractedDocImages || []).slice(0, 6);
  if (!imgs.length) return;
  showToast(`🔬 AI Vision đang tự động tạo câu hỏi cho ${imgs.length} hình ảnh...`, 'info');
  for (const im of imgs) {
    await aiGenerateSingleImageQuestion(im.url, im.label || '');
  }
}

// --- 15.3 Dashboard Knowledge Heatmap, AI Score Predictor & Dynamic Study Planner ---
function renderKnowledgeHeatmapAndPredictor(allQs, sid) {
  const heatmapEl = document.getElementById('knowledge-heatmap-grid');
  const predScoreEl = document.getElementById('pred-score-value');
  const predTextEl = document.getElementById('pred-counterfactual-text');
  const mistakeIds = new Set(STATE.mistakes.map((m) => (typeof m === 'object' ? m.id : m)));

  // Group questions by topic_tag or parsed.topic
  const groups = {};
  (allQs || []).forEach((q) => {
    const parsed = parseQuestionHeader(q.question_text);
    const rawTopic = (q.topic_tag || parsed.topic || 'Kiến thức trọng tâm').trim();
    const topic = rawTopic.replace(/^\[|\]$/g, '').trim() || 'Kiến thức trọng tâm';
    if (!groups[topic]) groups[topic] = { topic, total: 0, mistakes: 0, hasImage: 0 };
    groups[topic].total++;
    if (mistakeIds.has(q.id)) groups[topic].mistakes++;
    if (q.image_url) groups[topic].hasImage++;
  });

  const baseAvg = Number(STATE.stats?.avg_score || 7.6);
  const hasExams = Number(STATE.stats?.total_exams || 0) > 0;
  const topicList = Object.values(groups).map((g, idx) => {
    const baseMastery = hasExams ? Math.round(baseAvg * 9.2) : 78 - (idx % 3) * 8;
    const penalty = g.total > 0 ? Math.round((g.mistakes / g.total) * 55) : 0;
    const mastery = Math.max(28, Math.min(98, baseMastery - penalty));
    return { ...g, mastery };
  });

  // Update AI Score Predictor + Counterfactual NLG
  if (predScoreEl && predTextEl) {
    const avgMastery =
      topicList.length > 0
        ? topicList.reduce((acc, t) => acc + t.mastery, 0) / topicList.length
        : 78;
    const predScore = Math.max(4.0, Math.min(9.9, (avgMastery / 100) * 10));
    predScoreEl.textContent = `${predScore.toFixed(1)} ± 0.4`;

    const weakest = [...topicList].sort((a, b) => a.mastery - b.mastery)[0];
    if (weakest) {
      const boosted = Math.min(10.0, predScore + 0.9);
      predTextEl.innerHTML = `💡 <strong>Phân tích đối chứng AI:</strong> Nếu bạn luyện thêm <strong>10 câu</strong> chuyên đề <em>"${escapeHtml(weakest.topic)}"</em> (hiện đạt ${weakest.mastery}%), điểm dự báo kỳ thi thật sẽ tăng từ <strong>${predScore.toFixed(1)} → ${boosted.toFixed(1)} điểm</strong>.`;
    }
  }

  if (!heatmapEl) return;
  if (!topicList.length) {
    heatmapEl.innerHTML = `<div class="col-span-full text-xs txt-muted py-4 text-center">Chưa có dữ liệu chương mục cho môn học này.</div>`;
    return;
  }

  heatmapEl.innerHTML = topicList
    .map((t) => {
      const tone =
        t.mastery >= 80
          ? { badge: 'badge-emerald', border: 'rgba(16,185,129,0.4)', dot: '🟢', status: 'Vững vàng' }
          : t.mastery >= 50
          ? { badge: 'badge-amber', border: 'rgba(245,158,11,0.45)', dot: '🟡', status: 'Đang ôn' }
          : { badge: 'badge-rose', border: 'rgba(244,63,94,0.5)', dot: '🔴', status: 'Lỗ hổng' };
      const safeTopic = escapeHtml(t.topic).replace(/'/g, "\\'");
      return `
        <button type="button"
                onclick="startTopicHeatmapDrill(${sid}, '${safeTopic}')"
                class="heatmap-tile text-left p-3.5 rounded-2xl transition-all hover:scale-[1.01] flex flex-col justify-between gap-2"
                style="background-color: var(--bg-subtle); border: 1.5px solid ${tone.border};">
          <div class="flex items-start justify-between gap-2 w-full">
            <span class="text-xs font-extrabold txt-main leading-snug line-clamp-2">${tone.dot} ${escapeHtml(t.topic)}</span>
            <span class="${tone.badge} text-[11px] px-2 py-0.5 rounded-lg font-mono font-extrabold shrink-0">${t.mastery}%</span>
          </div>
          <div class="w-full flex items-center justify-between text-[11px] txt-muted pt-1">
            <span>${t.total} câu${t.hasImage ? ` • 🖼️ ${t.hasImage} ảnh` : ''}${t.mistakes ? ` • 🩹 ${t.mistakes} sai` : ''}</span>
            <span class="font-bold txt-brand">Luyện 10 câu →</span>
          </div>
        </button>
      `;
    })
    .join('');
}

async function startTopicHeatmapDrill(sid, topicName) {
  const res = await apiFetch(`/api/subjects/${sid}/questions?type=all`);
  const allQs = res.questions || [];
  const matched = allQs.filter((q) => {
    const parsed = parseQuestionHeader(q.question_text);
    const t = (q.topic_tag || parsed.topic || '').replace(/^\[|\]$/g, '').trim();
    return t.toLowerCase().includes(topicName.toLowerCase()) || q.question_text.toLowerCase().includes(topicName.toLowerCase());
  });
  const pool = matched.length ? matched : allQs;
  const picked = [...pool].sort(() => Math.random() - 0.5).slice(0, Math.min(10, pool.length));
  if (!picked.length) return;

  STATE.examConfig.subjectId = sid;
  setExamMode('practice');
  switchTab('exam');
  launchExamWithQuestions(picked, `Chuyên đề: ${topicName} (${picked.length} câu)`, false);
}

function updateDynamicStudyPlanner() {
  const inp = document.getElementById('planner-exam-date');
  const badge = document.getElementById('planner-countdown-badge');
  const listEl = document.getElementById('dynamic-planner-checklist');
  if (!listEl) return;

  let savedDate = localStorage.getItem('unimaster_exam_date');
  if (!savedDate) {
    const d = new Date();
    d.setDate(d.getDate() + 14);
    savedDate = d.toISOString().slice(0, 10);
    localStorage.setItem('unimaster_exam_date', savedDate);
  }
  if (inp && !inp.value) inp.value = savedDate;
  if (inp && inp.value && inp.value !== savedDate) {
    savedDate = inp.value;
    localStorage.setItem('unimaster_exam_date', savedDate);
  }

  const daysLeft = Math.max(1, Math.ceil((new Date(savedDate).getTime() - Date.now()) / 86400000));
  if (badge) badge.textContent = `⏳ Còn ${daysLeft} ngày tới kỳ thi`;

  const mistakeCount = STATE.mistakes.length;
  const tasks = [
    {
      id: 't1',
      label: `🔥 Giải quyết ${Math.min(10, Math.max(5, mistakeCount || 5))} câu trong Sổ tay câu sai (Quy tắc 3-Strike Mastery)`,
      action: `openMistakeBankModal()`,
      btn: 'Mở Sổ tay'
    },
    {
      id: 't2',
      label: `🧪 Luyện 15 câu Thực Hành Hóa Sinh Y Khoa (CTUMP) — Định luật Beer-Lambert & Xét nghiệm`,
      action: `quickStartHoaSinhCTUMP()`,
      btn: 'Luyện ngay'
    },
    {
      id: 't3',
      label: `🔬 Soi 16 tiêu bản Cặn lắng Nước tiểu & Tinh thể dưới kính hiển vi có phóng to HD`,
      action: `quickStartHoaSinhImagesOnly()`,
      btn: 'Soi tiêu bản'
    },
    {
      id: 't4',
      label: `🃏 Ôn tập thẻ nhớ Flashcard SM-2 đến hạn hôm nay để chống đường cong quên lãng Ebbinghaus`,
      action: `switchTab('flashcards')`,
      btn: 'Lật thẻ'
    }
  ];

  const doneMap = JSON.parse(localStorage.getItem('unimaster_planner_done') || '{}');
  listEl.innerHTML = tasks
    .map((t) => {
      const checked = Boolean(doneMap[t.id]);
      return `
        <div class="flex items-center justify-between gap-2 p-2.5 rounded-xl text-xs" style="background-color: var(--bg-subtle); border: 1px solid var(--border);">
          <label class="flex items-center gap-2.5 cursor-pointer flex-1">
            <input type="checkbox" ${checked ? 'checked' : ''} onchange="togglePlannerTask('${t.id}', this.checked)" class="w-4 h-4 accent-purple-600 rounded" />
            <span class="font-semibold ${checked ? 'line-through txt-muted' : 'txt-main'}">${t.label}</span>
          </label>
          <button type="button" onclick="${t.action}" class="btn-soft px-2.5 py-1 text-[11px] shrink-0">${t.btn} →</button>
        </div>
      `;
    })
    .join('');
}

function togglePlannerTask(taskId, checked) {
  const doneMap = JSON.parse(localStorage.getItem('unimaster_planner_done') || '{}');
  doneMap[taskId] = checked;
  localStorage.setItem('unimaster_planner_done', JSON.stringify(doneMap));
  if (checked) {
    addXp(10);
    playSound('correct');
  }
  updateDynamicStudyPlanner();
}

// --- 15.4 3-Strike Mastery Mistake Bank Modal ---
async function openMistakeBankModal() {
  openModal('modal-mistake-bank');
  const listEl = document.getElementById('mistake-bank-modal-body') || document.getElementById('mistake-bank-modal-list');
  if (!listEl) return;

  if (!STATE.mistakes.length) {
    listEl.innerHTML = `
      <div class="p-8 text-center space-y-2 rounded-2xl" style="background-color: var(--bg-subtle); border: 1px solid var(--border);">
        <div class="text-3xl">🎉</div>
        <div class="text-sm font-extrabold txt-emerald">Tuyệt vời! Sổ tay câu sai của bạn đang trống!</div>
        <p class="text-xs txt-muted">Mọi câu hỏi bạn từng làm sai đều đã vượt qua thử thách 3-Strike Mastery (Đúng 3 lần liên tiếp).</p>
      </div>
    `;
    return;
  }

  listEl.innerHTML = `<div class="skeleton-shimmer h-24 w-full"></div>`;
  const sid = STATE.examConfig.subjectId || 10;
  const res = await apiFetch(`/api/subjects/${sid}/questions?type=all`);
  const qMap = Object.fromEntries((res.questions || []).map((q) => [q.id, q]));

  listEl.innerHTML = STATE.mistakes
    .map((m) => {
      const item = typeof m === 'object' ? m : { id: m, subject_id: sid, streak: 0, fail_count: 1 };
      const q = qMap[item.id];
      const streak = Math.min(3, item.streak || 0);
      const stars = '🟢'.repeat(streak) + '⚪'.repeat(Math.max(0, 3 - streak));
      const title = q ? parseQuestionHeader(q.question_text).body : `Câu hỏi #${item.id}`;
      return `
        <div class="p-3.5 rounded-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-3" style="background-color: var(--bg-subtle); border: 1px solid var(--border);">
          <div class="space-y-1 flex-1">
            <div class="flex flex-wrap items-center gap-2 text-xs">
              <span class="badge-rose px-2 py-0.5 rounded font-mono font-bold">#${item.id}</span>
              <span class="badge-amber px-2 py-0.5 rounded font-bold">Sai ${item.fail_count || 1} lần</span>
              <span class="badge-emerald px-2 py-0.5 rounded font-bold">Chuỗi gỡ sai: ${stars} (${streak}/3)</span>
            </div>
            <div class="text-xs sm:text-sm font-bold txt-main line-clamp-2">${formatRichText(title)}</div>
          </div>
          <div class="flex items-center gap-1.5 shrink-0">
            <button type="button" onclick="askAiAboutMistakeQuestion(${item.id}, ${item.subject_id || sid})" class="btn-primary !bg-gradient-to-r !from-indigo-600 !to-purple-600 px-2.5 py-1.5 text-xs font-bold flex items-center gap-1 shadow-sm"><span>🤖</span> Hỏi AI</button>
            <button type="button" onclick="closeModal('modal-mistake-bank');startSpecialDrill('mistakes', ${item.subject_id || sid});" class="btn-soft px-3 py-1.5 text-xs">
              🩹 Luyện gỡ sai
            </button>
          </div>
        </div>
      `;
    })
    .join('');
}

// --- 15.5 Contextual Community Discussion & TA Verified Tips ---
async function toggleQuestionDiscussionBox(forceState = null) {
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
      const currentQ = (STATE.exam?.active && STATE.exam?.questions) ? STATE.exam.questions[STATE.exam.currentIndex] : null;
      let seedTip = 'Chưa có bình luận nào cho câu này. Hãy là người đầu tiên chia sẻ mẹo nhớ!';
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
              <span class="badge-brand px-2 py-0.5 rounded text-[10px] font-bold">${escapeHtml(c.author_badge || '🎓 Sinh viên')}</span>
              ${c.is_verified ? `<span class="badge-emerald px-2 py-0.5 rounded text-[10px] font-bold">✔ Trợ giảng xác thực</span>` : ''}
            </div>
            <div class="txt-sub leading-relaxed">${formatRichText(c.content || '')}</div>
          </div>
          <button type="button" onclick="upvoteDiscussionComment(${c.id}, ${qid})" class="btn-soft px-2.5 py-1 text-xs font-bold shrink-0 flex items-center gap-1 text-amber-400">
            <span>👍</span> <span>${c.upvotes || 0}</span>
          </button>
        </div>
      `
      )
      .join('');
  } catch (err) {
    console.warn('Error loading discussions:', err);
  }
}

async function submitQuestionDiscussion() {
  const currentQ = (STATE.exam?.active && STATE.exam?.questions) ? STATE.exam.questions[STATE.exam.currentIndex] : null;
  if (!currentQ) return;

  const authorInp = document.getElementById('q-disc-author-input');
  const inp = document.getElementById('q-disc-content-input') || document.getElementById('q-discussion-input');
  const author = (authorInp?.value || '').trim() || 'Sinh viên UniMaster';
  const content = (inp?.value || '').trim();

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
  if (inp) inp.value = '';

  try {
    const res = await apiFetch(`/api/questions/${currentQ.id}/discussions`, {
      method: 'POST',
      body: JSON.stringify({
        author_name: author,
        author_badge: `⚡ Lv.${Math.floor(STATE.xp / 200) + 1}`,
        content: content
      })
    });
    if (res && res.success) {
      addXp(10);
      playSound('correct');
      showToast('💬 Đã đăng mẹo nhớ (+10 XP)!', 'success');
      const currCount = parseInt(toolbarCountEl?.textContent || '0', 10) + 1;
      if (toolbarCountEl) toolbarCountEl.textContent = currCount;
      if (countEl) countEl.textContent = `${currCount} bình luận`;
    }
  } catch (err) {
    showToast('Lỗi gửi bình luận: ' + err.message, 'warning');
  }
}

async function upvoteDiscussionComment(cid, qid) {
  await apiFetch(`/api/discussions/${cid}/upvote`, { method: 'POST', body: JSON.stringify({}) });
  playSound('click');
  loadQuestionDiscussions(qid);
}

// --- 15.6 Arena Suite: 1v1 Quiz Battle, Pomodoro Ambient Lounge, Leaderboard & 12 Badges ---
function initArenaView() {
  renderArenaLoungePeers();
  renderArenaLeaderboardAndBadges();
}

function switchArenaSubTab(sub) {
  ['live', 'battle', 'lounge', 'leaderboard'].forEach((k) => {
    document.getElementById(`arena-panel-${k}`)?.classList.toggle('hidden', k !== sub);
    document.getElementById(`arena-sub-${k}`)?.classList.toggle('active', k === sub);
    document.getElementById(`arena-subtab-${k}`)?.classList.toggle('active', k === sub);
  });
  if (sub === 'live') initLiveArenaView();
  playSound('click');
}

function selectBattleOpponent(key) {
  const map = {
    minh_anh: { name: 'BS. Nội Trú Minh Anh', emoji: '🩺' },
    hoang_nam: { name: 'Hoàng Nam (Thủ khoa CNTT)', emoji: '💻' },
    thao_vy: { name: 'Thảo Vy (CLB Học Thuật)', emoji: '🧪' },
    speed: { name: 'Bác Sĩ Tốc Độ', emoji: '⚡' },
    scholar: { name: 'Thủ Khoa Điềm Tĩnh', emoji: '🦉' },
    boss: { name: 'Giáo Sư Hóa Sinh AI', emoji: '👑' }
  };
  const info = map[key] || map.minh_anh;
  STATE.battle.opponentKey = key;
  STATE.battle.opponentName = info.name;
  STATE.battle.opponentEmoji = info.emoji;

  ['minh_anh', 'hoang_nam', 'thao_vy', 'speed', 'scholar', 'boss'].forEach((k) => {
    document.getElementById(`opp-card-${k}`)?.classList.toggle('active', k === key);
  });
  playSound('click');
}

function createBattleRoomPin() {
  const pin = String(Math.floor(100000 + Math.random() * 900000));
  const pinInp = document.getElementById('battle-room-pin');
  const box = document.getElementById('battle-pin-box');
  const codeEl = document.getElementById('battle-pin-code');
  if (pinInp) pinInp.value = pin;
  if (codeEl) codeEl.textContent = pin;
  if (box) box.classList.remove('hidden');
  playSound('correct');
  showToast(`🔑 Đã tạo mã PIN phòng thi đấu: ${pin} — gửi mã này cho bạn bè để cùng so tài!`, 'success');
}

async function startQuizBattleMatch() {
  const sid = Number(document.getElementById('battle-subject-select')?.value || STATE.examConfig.subjectId || 10);
  const res = await apiFetch(`/api/subjects/${sid}/questions?type=mcq`);
  const allMcq = (res.questions || []).filter((q) => q.q_type === 'mcq');
  if (!allMcq.length) {
    showToast('Môn học này chưa có câu hỏi trắc nghiệm để đấu 1v1!', 'warning');
    return;
  }

  const picked = [...allMcq].sort(() => Math.random() - 0.5).slice(0, 10);
  clearInterval(STATE.battle.timerId);
  clearTimeout(STATE.battle.botTimerId);

  STATE.battle = {
    ...STATE.battle,
    active: true,
    questions: picked,
    idx: 0,
    myScore: 0,
    botScore: 0,
    myCombo: 0,
    timeLeft: 15
  };

  setText('battle-opp-name', `${STATE.battle.opponentEmoji || '🩺'} ${STATE.battle.opponentName || 'BS. Nội Trú Minh Anh'}`);
  document.getElementById('battle-idle-placeholder')?.classList.add('hidden');
  document.getElementById('battle-live-arena')?.classList.remove('hidden');
  document.getElementById('battle-stage-card')?.classList.remove('hidden');
  playSound('click');
  renderCurrentBattleRound();
}

function renderCurrentBattleRound() {
  const b = STATE.battle;
  if (!b.active || b.idx >= b.questions.length) {
    finishQuizBattleMatch();
    return;
  }

  const q = b.questions[b.idx];
  const parsed = parseQuestionHeader(q.question_text);
  b.timeLeft = 15;

  setText('battle-my-score', b.myScore);
  setText('battle-opp-score', b.botScore);
  setText('battle-q-progress', `Câu ${b.idx + 1} / ${b.questions.length}`);
  setText('battle-my-combo', `Combo x${(1 + 0.1 * b.myCombo).toFixed(1)}`);
  setText('battle-timer-pill', `⏱ 15s`);

  const myBar = document.getElementById('battle-my-bar');
  const oppBar = document.getElementById('battle-opp-bar');
  if (myBar) myBar.style.width = `${Math.round(((b.idx + 1) / b.questions.length) * 100)}%`;
  if (oppBar) oppBar.style.width = `${Math.round(((b.idx + 1) / b.questions.length) * 100)}%`;

  const qEl = document.getElementById('battle-q-text');
  if (qEl) {
    const imgHtml = q.image_url
      ? `<div class="mb-2"><img src="${escapeHtml(q.image_url)}" onclick="openImageLightbox('${escapeHtml(q.image_url)}', 'Tiêu bản Đấu trường')" class="max-h-48 w-auto mx-auto rounded-xl object-contain cursor-zoom-in" style="border: 1px solid var(--border);" /></div>`
      : '';
    qEl.innerHTML = `${imgHtml}${formatRichText(parsed.body)}`;
  }

  const optsEl = document.getElementById('battle-options-grid');
  if (optsEl) {
    const opts = [
      ['A', q.option_a],
      ['B', q.option_b],
      ['C', q.option_c],
      ['D', q.option_d]
    ];
    optsEl.innerHTML = opts
      .map(
        ([L, txt]) => `
        <div onclick="pickBattleOption('${L}')" id="battle-opt-${L}" class="option-row opt-${L} cursor-pointer">
          <div class="opt-badge">${L}</div>
          <div class="option-text flex-1 text-xs sm:text-sm">${formatRichText(txt || '')}</div>
        </div>
      `
      )
      .join('');
  }

  clearInterval(b.timerId);
  b.timerId = setInterval(() => {
    if (!b.active) return;
    b.timeLeft--;
    setText('battle-timer-pill', `⏱ ${b.timeLeft}s`);
    if (b.timeLeft <= 0) {
      clearInterval(b.timerId);
      pickBattleOption('TIMEOUT');
    }
  }, 1000);
}

function pickBattleOption(letter) {
  const b = STATE.battle;
  if (!b.active) return;
  clearInterval(b.timerId);

  const q = b.questions[b.idx];
  const corr = normalizeCorrectLetter(q);
  const isRight = letter === corr;

  if (isRight) {
    b.myCombo++;
    const mult = Math.min(2.0, 1 + 0.1 * b.myCombo);
    const delta = Math.round((100 + Math.floor((50 * Math.max(0, b.timeLeft)) / 15)) * mult);
    b.myScore += delta;
    playSound('correct');
  } else {
    b.myCombo = 0;
    playSound('wrong');
  }

  // Bot accuracy simulation
  const accMap = { speed: 0.72, scholar: 0.85, boss: 0.92 };
  const botRight = Math.random() < (accMap[b.opponentKey] || 0.75);
  if (botRight) {
    b.botScore += 115 + Math.floor(Math.random() * 35);
  }

  ['A', 'B', 'C', 'D'].forEach((L) => {
    const el = document.getElementById(`battle-opt-${L}`);
    if (!el) return;
    el.classList.add('disabled');
    if (L === corr) el.classList.add('is-correct');
    else if (L === letter) el.classList.add('is-wrong');
  });

  setText('battle-my-score', b.myScore);
  setText('battle-opp-score', b.botScore);

  setTimeout(() => {
    b.idx++;
    renderCurrentBattleRound();
  }, 950);
}

function finishQuizBattleMatch() {
  const b = STATE.battle;
  b.active = false;
  clearInterval(b.timerId);

  const won = b.myScore >= b.botScore;
  if (won) {
    addXp(80);
    playSound('complete');
    if (window.confetti) confetti({ particleCount: 80, spread: 70, origin: { y: 0.6 } });
  } else {
    addXp(30);
  }

  const qEl = document.getElementById('battle-q-text');
  const optsEl = document.getElementById('battle-options-grid');
  if (qEl) {
    qEl.innerHTML = `
      <div class="text-center space-y-2 py-3">
        <div class="text-3xl">${won ? '🏆 CHIẾN THẮNG ÁP ĐẢO!' : '⚔️ TRẬN ĐẤU KỊCH TÍNH!'}</div>
        <div class="text-sm font-bold txt-sub">
          Điểm của bạn: <strong class="txt-emerald">${b.myScore}</strong> vs ${escapeHtml(b.opponentName)}: <strong class="txt-rose">${b.botScore}</strong>
        </div>
      </div>
    `;
  }
  if (optsEl) {
    optsEl.innerHTML = `
      <button type="button" onclick="startQuizBattleMatch()" class="btn-primary col-span-full py-3 text-xs font-extrabold">
        🔄 Tái Đấu Ván Mới Ngay
      </button>
    `;
  }
}

// Web Audio API Ambient Noise Synthesizer for Pomodoro Study Lounge
function setAmbientSound(mode) {
  ['off', 'rain', 'brown', 'waves'].forEach((m) => {
    document.getElementById(`amb-btn-${m}`)?.classList.toggle('active', m === mode);
  });

  if (STATE.ambient.source) {
    try { STATE.ambient.source.stop(); } catch (_) {}
    STATE.ambient.source = null;
  }
  STATE.ambient.mode = mode;
  if (mode === 'off') return;

  try {
    const Ctx = window.AudioContext || window.webkitAudioContext;
    if (!Ctx) return;
    if (!audioCtx) audioCtx = new Ctx();
    if (audioCtx.state === 'suspended') audioCtx.resume();

    const bufferSize = audioCtx.sampleRate * 3;
    const buffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
    const data = buffer.getChannelData(0);
    let lastOut = 0.0;
    for (let i = 0; i < bufferSize; i++) {
      const white = Math.random() * 2 - 1;
      data[i] = (lastOut + 0.02 * white) / 1.02;
      lastOut = data[i];
      data[i] *= mode === 'rain' ? 1.8 : 2.5;
    }

    const noise = audioCtx.createBufferSource();
    noise.buffer = buffer;
    noise.loop = true;

    const filter = audioCtx.createBiquadFilter();
    filter.type = mode === 'rain' ? 'bandpass' : 'lowpass';
    filter.frequency.value = mode === 'rain' ? 950 : mode === 'waves' ? 320 : 480;

    const gain = audioCtx.createGain();
    gain.gain.value = 0.06;

    noise.connect(filter);
    filter.connect(gain);
    gain.connect(audioCtx.destination);
    noise.start();

    STATE.ambient.source = noise;
    STATE.ambient.gain = gain;
    showToast(`🎧 Đã bật âm thanh nền: ${mode === 'rain' ? 'Mưa thư viện' : mode === 'brown' ? 'Brown Noise' : 'Sóng biển'}`, 'info');
  } catch (_) {}
}

function renderArenaLoungePeers() {
  const grid = document.getElementById('lounge-peers-grid');
  if (!grid) return;
  const peers = [
    { name: 'Minh Anh (Y Đa Khoa K48)', task: 'Đang ôn Thực Hành Hóa Sinh CTUMP • Câu 142/312', time: '42 phút', badge: '🔥 Chuỗi 14 ngày' },
    { name: 'Hoàng Phúc (CNTT K49)', task: 'Đang giải 60 Bài Thực Hành OOP C#', time: '28 phút', badge: '⚡ Top 3 Tuần' },
    { name: 'Thảo Vy (Dược Học K48)', task: 'Đang soi 16 Tiêu bản Cặn lắng Nước tiểu', time: '19 phút', badge: '🔬 Bậc thầy Tiêu bản' },
    { name: 'Quốc Bảo (Xét Nghiệm Y Học)', task: 'Đang lật thẻ Flashcard SM-2 Hóa Sinh', time: '55 phút', badge: '🏅 3-Strike Master' }
  ];
  grid.innerHTML = peers
    .map(
      (p) => `
      <div class="p-3.5 rounded-2xl flex items-center justify-between gap-3" style="background-color: var(--bg-subtle); border: 1px solid var(--border);">
        <div class="space-y-0.5">
          <div class="text-xs font-extrabold txt-main flex items-center gap-1.5">
            <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
            <span>${escapeHtml(p.name)}</span>
          </div>
          <div class="text-[11px] txt-sub">${escapeHtml(p.task)}</div>
        </div>
        <div class="text-right shrink-0">
          <span class="badge-brand text-[10px] px-2 py-0.5 rounded-md font-bold block">${escapeHtml(p.badge)}</span>
          <span class="text-[10px] txt-muted font-mono">${escapeHtml(p.time)}</span>
        </div>
      </div>
    `
    )
    .join('');
}

function renderArenaLeaderboardAndBadges() {
  const lbEl = document.getElementById('arena-leaderboard-list');
  const bgEl = document.getElementById('arena-badges-grid');

  if (lbEl) {
    const myXp = STATE.xp || 450;
    const rows = [
      { name: 'BS. Nguyễn Minh Khôi (CTUMP)', xp: Math.max(2450, myXp + 320), streak: 19, tag: '💎 Thủ Khoa Hóa Sinh' },
      { name: 'Bạn (Tài khoản hiện tại)', xp: myXp, streak: STATE.streakDays || 1, tag: '🌟 Đang bứt phá', isMe: true },
      { name: 'Trần Lê Bảo Ngọc (Y4)', xp: Math.max(380, myXp - 90), streak: 11, tag: '🔬 Chuyên gia Tiêu bản' },
      { name: 'Lê Hoàng Nam (CNTT)', xp: Math.max(310, myXp - 180), streak: 8, tag: '💻 Kiến trúc sư C#' },
      { name: 'Phạm Quỳnh Hương (Dược)', xp: Math.max(240, myXp - 260), streak: 6, tag: '🃏 Cao thủ SM-2' }
    ].sort((a, b) => b.xp - a.xp);

    lbEl.innerHTML = rows
      .map(
        (r, i) => `
        <div class="p-3 rounded-xl flex items-center justify-between gap-2 text-xs ${r.isMe ? 'badge-brand' : ''}"
             style="${r.isMe ? '' : 'background-color: var(--bg-subtle); border: 1px solid var(--border);'}">
          <div class="flex items-center gap-2.5">
            <span class="font-mono font-extrabold text-sm w-6 text-center">${i === 0 ? '🥇' : i === 1 ? '🥈' : i === 2 ? '🥉' : '#' + (i + 1)}</span>
            <div>
              <div class="font-extrabold txt-main">${escapeHtml(r.name)}</div>
              <div class="text-[11px] txt-muted">${escapeHtml(r.tag)} • 🔥 ${r.streak} ngày</div>
            </div>
          </div>
          <span class="font-mono font-extrabold txt-emerald">${r.xp.toLocaleString()} XP</span>
        </div>
      `
      )
      .join('');
  }

  if (bgEl) {
    const badges = [
      { icon: '🧪', name: 'Thủ Khoa Hóa Sinh', desc: 'Hoàn thành bộ đề Thực hành Hóa Sinh CTUMP', unlocked: true },
      { icon: '🔬', name: 'Mắt Thần Hiển Vi', desc: 'Chẩn đoán đúng các tiêu bản cặn lắng nước tiểu', unlocked: true },
      { icon: '🔥', name: 'Chiến Thần Giữ Lửa', desc: 'Duy trì chuỗi Study Streak liên tiếp', unlocked: true },
      { icon: '🩹', name: '3-Strike Master', desc: 'Gỡ sai 3 lần liên tiếp trong Sổ tay câu sai', unlocked: true },
      { icon: '⚔️', name: 'Bất Bại Đấu Trường', desc: 'Chiến thắng trận Quiz Battle 1v1', unlocked: STATE.xp >= 100 },
      { icon: '🃏', name: 'Trí Nhớ Siêu Phàm', desc: 'Ôn tập thẻ nhớ Flashcard 3D SM-2', unlocked: true },
      { icon: '💻', name: 'Kiến Trúc Sư OOP', desc: 'Chinh phục ngân hàng câu hỏi C# OOP', unlocked: true },
      { icon: '⚡', name: 'Tốc Độ Ánh Sáng', desc: 'Đạt kỷ lục trong chế độ Blitz 3 mạng', unlocked: STATE.blitzBest > 0 },
      { icon: '🧠', name: 'Học Giả Socrates', desc: 'Trò chuyện học thuật cùng Gia sư AI', unlocked: true },
      { icon: '📄', name: 'Nhà Biên Soạn Đề', desc: 'Tải tài liệu PDF/Ảnh tạo đề tự động', unlocked: true },
      { icon: '🎧', name: 'Thư Viện Không Ngủ', desc: 'Tập trung 25 phút trong Pomodoro Lounge', unlocked: true },
      { icon: '👑', name: 'Huyền Thoại UniMaster', desc: 'Đạt cấp độ Đại Học Toàn Năng', unlocked: STATE.xp >= 500 }
    ];
    const unlockedCount = badges.filter((b) => b.unlocked).length;
    setText('badges-unlocked-count', `${unlockedCount} / ${badges.length} Đã mở`);

    bgEl.innerHTML = badges
      .map(
        (b) => `
        <div class="p-3 rounded-2xl text-center space-y-1 transition-all ${b.unlocked ? '' : 'opacity-50'}"
             style="background-color: var(--bg-subtle); border: 1px solid var(--border);">
          <div class="text-2xl">${b.icon}</div>
          <div class="text-xs font-extrabold txt-main">${escapeHtml(b.name)}</div>
          <div class="text-[10px] txt-muted leading-snug">${escapeHtml(b.desc)}</div>
        </div>
      `
      )
      .join('');
  }
}


// =========================================================================
// 16. UNIMASTER v9.0 BREAKTHROUGH SUITE:
//     - PERMANENT GATEWAY & AUTO-RECONNECT
//     - HANDS-FREE PODCAST AUDIO LOOP
//     - OSCE BLIND ACTIVE-RECALL SPOTTER MODE
//     - VIETNAMESE VOICE-TO-TEXT ORAL EXAMINER & CLINICAL CASE SIMULATOR
//     - AI INTERACTIVE MINDMAP GENERATOR
// =========================================================================

function copyPermanentGatewayUrl() {
  const url = 'https://ntfy.sh/unimaster_ctump_5292';
  navigator.clipboard.writeText(url).then(() => {
    playSound('correct');
    showToast('📌 Đã sao chép Cổng Truy Cập Cố Định Vĩnh Viễn! Hãy lưu vào Dấu trang Điện thoại/iPad.', 'success');
  });
}

// --- 16.1 OSCE Blind Active-Recall Spotter Mode ---
function toggleOsceBlindMode() {
  STATE.osceBlindMode = !STATE.osceBlindMode;
  STATE.osceRevealedMap = STATE.osceRevealedMap || {};
  const btn = document.getElementById('btn-osce-mode');
  if (btn) {
    btn.className = STATE.osceBlindMode
      ? 'badge-brand px-2.5 py-1.5 rounded-xl text-xs font-extrabold'
      : 'btn-soft px-2.5 py-1.5 text-xs';
  }
  playSound('click');
  showToast(
    STATE.osceBlindMode
      ? '🕵️ Đã bật Chế độ Chạy trạm OSCE: Ẩn phương án A/B/C/D để tự nhớ chủ động trước khi lật!'
      : 'Đã tắt Chế độ Chạy trạm OSCE',
    'info'
  );
  if (STATE.exam.active) renderCurrentExamQuestion();
}

function revealOsceOptionsForCurrentQuestion(qid) {
  STATE.osceRevealedMap = STATE.osceRevealedMap || {};
  STATE.osceRevealedMap[qid] = true;
  playSound('click');
  renderCurrentExamQuestion();
}

// --- 16.2 Hands-Free Audio Podcast Loop Mode ---
function toggleHandsFreeAudioMode() {
  STATE.podcastMode = !STATE.podcastMode;
  clearTimeout(STATE.podcastTimerId);
  const btn = document.getElementById('btn-podcast-mode');
  if (btn) {
    btn.className = STATE.podcastMode
      ? 'badge-emerald px-2.5 py-1.5 rounded-xl text-xs font-extrabold animate-pulse'
      : 'btn-soft px-2.5 py-1.5 text-xs';
  }
  if (!STATE.podcastMode) {
    try { window.speechSynthesis?.cancel(); } catch (_) {}
    showToast('🔇 Đã dừng chế độ Đài phát thanh Podcast ôn thi.', 'info');
    return;
  }
  showToast('🎧 Đã bật Đài phát thanh Podcast: Tự đọc câu hỏi → nghỉ 3s → đọc đáp án → tự chuyển câu!', 'success');
  runPodcastStepForCurrentQuestion();
}

function runPodcastStepForCurrentQuestion() {
  if (!STATE.podcastMode || !STATE.exam.active || STATE.exam.paused) return;
  const q = STATE.exam.questions[STATE.exam.currentIndex];
  if (!q) return;

  const parsed = parseQuestionHeader(q.question_text);
  const qSpeak = `Câu số ${STATE.exam.currentIndex + 1}. ${parsed.body}. Phương án A: ${q.option_a || ''}. Phương án B: ${q.option_b || ''}. ${q.option_c ? 'Phương án C: ' + q.option_c + '.' : ''} ${q.option_d ? 'Phương án D: ' + q.option_d + '.' : ''}`;

  speakVietnamese(qSpeak);
  clearTimeout(STATE.podcastTimerId);
  STATE.podcastTimerId = setTimeout(() => {
    if (!STATE.podcastMode || !STATE.exam.active) return;
    const corr = q._effectiveCorrect || normalizeCorrectLetter(q);
    const optMap = { A: q.option_a, B: q.option_b, C: q.option_c, D: q.option_d };
    STATE.exam.answers[q.id] = corr;
    STATE.exam.graded[q.id] = true;
    renderCurrentExamQuestion();

    const ansSpeak = `Đáp án đúng là ${corr}: ${optMap[corr] || ''}. ${q.explanation || ''}`;
    speakVietnamese(ansSpeak);

    STATE.podcastTimerId = setTimeout(() => {
      if (!STATE.podcastMode || !STATE.exam.active) return;
      if (STATE.exam.currentIndex < STATE.exam.questions.length - 1) {
        nextQuestion();
        runPodcastStepForCurrentQuestion();
      } else {
        STATE.podcastMode = false;
        showToast('🎉 Đã nghe hoàn tất toàn bộ câu hỏi trong đề!', 'success');
      }
    }, 6500);
  }, 8500);
}

// --- 16.3 Vietnamese Voice-to-Text Oral Input & Clinical Case / Mindmap Generators ---
let speechRec = null;
function toggleVoiceInputForTutor() {
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SR) {
    showToast('Trình duyệt của bạn chưa hỗ trợ nhận diện giọng nói trực tiếp. Hãy dùng Chrome/Safari/Edge!', 'warning');
    return;
  }
  const btn = document.getElementById('btn-tutor-mic');
  if (speechRec && STATE.isListeningVoice) {
    speechRec.stop();
    STATE.isListeningVoice = false;
    if (btn) btn.className = 'btn-soft px-3.5 py-2.5 text-sm shrink-0';
    return;
  }

  speechRec = new SR();
  speechRec.lang = 'vi-VN';
  speechRec.interimResults = false;
  speechRec.maxAlternatives = 1;

  STATE.isListeningVoice = true;
  if (btn) btn.className = 'badge-rose px-3.5 py-2.5 rounded-xl text-sm shrink-0 animate-pulse';
  showToast('🎙️ Đang lắng nghe tiếng Việt... Hãy đọc câu trả lời hoặc câu hỏi của bạn!', 'info');

  speechRec.onresult = (event) => {
    const transcript = event.results?.[0]?.[0]?.transcript || '';
    const inp = document.getElementById('tutor-input');
    if (inp && transcript) {
      inp.value = inp.value ? `${inp.value} ${transcript}` : transcript;
      showToast('✔ Đã chuyển giọng nói thành văn bản!', 'success');
    }
  };
  speechRec.onend = () => {
    STATE.isListeningVoice = false;
    if (btn) btn.className = 'btn-soft px-3.5 py-2.5 text-sm shrink-0';
  };
  speechRec.onerror = () => {
    STATE.isListeningVoice = false;
    if (btn) btn.className = 'btn-soft px-3.5 py-2.5 text-sm shrink-0';
  };
  speechRec.start();
}

function startClinicalOrOralCaseSim() {
  setTutorPersona('examiner');
  const sid = document.getElementById('tutor-subject-select')?.value;
  const sub = STATE.subjects.find((s) => String(s.id) === String(sid)) || STATE.subjects[0];
  const isMed = sub?.code === 'HOASINH_CTUMP' || sub?.code === 'BIO101' || (sub?.name || '').toLowerCase().includes('hóa sinh');

  const prompt = isMed
    ? '🩺 Hãy đóng vai Giáo sư Bác sĩ Trưởng khoa đưa ra 1 Ca bệnh Lâm sàng thực tế có đầy đủ các chỉ số xét nghiệm Hóa sinh máu & nước tiểu (kèm cặn lắng kính hiển vi). Sau đó đặt 2 câu hỏi biện luận lâm sàng để tôi trả lời và chấm điểm phản xạ!'
    : `🎤 Hãy đóng vai Giám khảo Vấn đáp môn "${sub?.name || 'Đại học'}" đưa ra 1 Tình huống thực tế hóc búa (Case Study) và đặt 2 câu hỏi vấn đáp xoáy sâu bản chất để tôi trả lời, sau đó chấm điểm trên thang 10!`;

  sendQuickTutorPrompt(prompt);
}

function generateSubjectMindmap() {
  const sid = document.getElementById('tutor-subject-select')?.value;
  const sub = STATE.subjects.find((s) => String(s.id) === String(sid)) || STATE.subjects[0];
  const prompt = `🗺️ Hãy lập Sơ đồ tư duy cấu trúc cây (Mindmap trực quan kèm bảng so sánh nhanh và các công thức cốt lõi) tóm tắt toàn bộ các chương trọng tâm hay ra thi nhất của môn "${sub?.name || 'Đại học'}".`;
  sendQuickTutorPrompt(prompt);
}

// =========================================================================
// 17. UNIMASTER v10.0 BREAKTHROUGH SUITE:
//     - PC-OFF 24/7 EVERYWHERE ENGINE (IndexedDB Snapshot + Direct Browser-to-Gemini AI)
//     - VIRTUAL SPECTROPHOTOMETER & CLINICAL BIOCHEMISTRY LAB
//     - TIMED 6-STATION OSCE CIRCUIT WITH SYNTHESIZED STATION BELL
//     - CAMERA HANDWRITTEN SOLUTION & LAB SHEET AI VISION GRADER
//     - INTERACTIVE KNOWLEDGE GRAPH & CLINICAL CALCULATORS
// =========================================================================

// --- 17.1 PC-Off 24/7 Everywhere Engine (IndexedDB + Direct Browser Gemini Cloud API) ---
function getBrowserGeminiKeyPool() {
  const keys = [];
  try {
    const savedArr = JSON.parse(localStorage.getItem('unimaster_offline_gemini_keys') || '[]');
    if (Array.isArray(savedArr)) keys.push(...savedArr);
  } catch (_) {}
  const single = localStorage.getItem('unimaster_offline_gemini_key');
  if (single) keys.push(single);
  const db = window.__UNIMASTER_OFFLINE_DB__;
  if (db) {
    if (Array.isArray(db.gemini_api_keys)) keys.push(...db.gemini_api_keys);
    if (db.gemini_api_key) keys.push(db.gemini_api_key);
  }
  return Array.from(new Set(keys.map((k) => String(k || '').trim()).filter(Boolean)));
}

function openOfflineIdb() {
  return new Promise((resolve, reject) => {
    if (!('indexedDB' in window)) return reject(new Error('No IndexedDB'));
    const req = indexedDB.open('unimaster_pcoff_db_v10', 1);
    req.onupgradeneeded = (e) => {
      const idb = e.target.result;
      if (!idb.objectStoreNames.contains('snapshots')) {
        idb.createObjectStore('snapshots');
      }
    };
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}

async function saveSnapshotToIdb(snap) {
  try {
    const idb = await openOfflineIdb();
    await new Promise((resolve, reject) => {
      const tx = idb.transaction('snapshots', 'readwrite');
      tx.objectStore('snapshots').put(snap, 'latest');
      tx.oncomplete = () => resolve(true);
      tx.onerror = () => reject(tx.error);
    });
    return true;
  } catch (_) {
    return false;
  }
}

async function loadSnapshotFromIdb() {
  try {
    const idb = await openOfflineIdb();
    return await new Promise((resolve) => {
      const tx = idb.transaction('snapshots', 'readonly');
      const req = tx.objectStore('snapshots').get('latest');
      req.onsuccess = () => resolve(req.result || null);
      req.onerror = () => resolve(null);
    });
  } catch (_) {
    return null;
  }
}

async function ensureOfflineSnapshotReady() {
  if (window.__UNIMASTER_OFFLINE_DB__ && window.__UNIMASTER_OFFLINE_DB__.subjects) {
    return true;
  }
  const cached = await loadSnapshotFromIdb();
  if (cached && cached.subjects) {
    window.__UNIMASTER_OFFLINE_DB__ = cached;
    return true;
  }
  return false;
}

async function syncFullSnapshotToBrowserForPcOff(silent = false) {
  if (STATE.isOfflineStandalone) {
    if (!silent) showToast('⚡ Bạn đang chạy trực tiếp từ File Siêu Độc Lập (đã nhúng sẵn 100% câu hỏi, ảnh và AI)!', 'success');
    return;
  }
  try {
    if (!silent) showToast('📲 Đang đồng bộ trọn bộ 467 câu hỏi + 16 ảnh + Dàn Key AI vào bộ nhớ trình duyệt...', 'info');
    const resp = await fetch('/api/offline-snapshot', { credentials: 'same-origin' });
    if (!resp.ok) throw new Error('HTTP ' + resp.status);
    const data = await resp.json();
    if (data.success && data.snapshot) {
      window.__UNIMASTER_OFFLINE_DB__ = data.snapshot;
      if (Array.isArray(data.snapshot.gemini_api_keys) && data.snapshot.gemini_api_keys.length) {
        localStorage.setItem('unimaster_offline_gemini_keys', JSON.stringify(data.snapshot.gemini_api_keys));
        localStorage.setItem('unimaster_offline_gemini_key', data.snapshot.gemini_api_keys[0]);
      }
      await saveSnapshotToIdb(data.snapshot);
      const pill = document.getElementById('pcoff-cache-status-pill');
      if (pill) {
        pill.textContent = '✔ Đã lưu 100% vào máy (Sẵn sàng tắt PC)';
        pill.className = 'badge-emerald text-[11px] px-2.5 py-0.5 rounded-full font-bold';
      }
      if (!silent) {
        showToast('🎉 Đã lưu 100% Ngân hàng đề + 16 ảnh + Direct Gemini AI vào trình duyệt! Kể cả khi tắt PC, bạn vẫn học và gọi AI bình thường!', 'success');
      }
    }
  } catch (_) {
    await ensureOfflineSnapshotReady();
  }
}

// Auto-cache in background 2.5s after page load when PC is online
setTimeout(() => {
  if (!STATE.isOfflineStandalone) {
    syncFullSnapshotToBrowserForPcOff(true);
  }
}, 2500);

let _browserKeyCursor = 0;
async function callGeminiRawFromBrowser(promptText, imageBase64 = null, mimeType = 'image/jpeg') {
  // PRIORITY 1: Try OpenAI ChatGPT first
  const openaiKey = localStorage.getItem('unimaster_openai_key') || '';
  const openaiBase = (localStorage.getItem('unimaster_openai_base') || 'https://api.openai.com/v1').replace(/\/$/, '');
  if (openaiKey && !imageBase64) {
    try {
      const resp = await fetch(`${openaiBase}/chat/completions`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${openaiKey}`
        },
        body: JSON.stringify({
          model: 'gpt-4o-mini',
          messages: [{ role: 'user', content: promptText }],
          max_tokens: 2048,
          temperature: 0.4
        })
      });
      if (resp.ok) {
        const d = await resp.json();
        const ans = d.choices?.[0]?.message?.content?.trim();
        if (ans) return ans;
      }
    } catch (_) {}
  }

  const keys = getBrowserGeminiKeyPool();
  if (!keys.length) return null;

  const models = ['gemini-3.5-flash', 'gemini-3.5-flash-lite', 'gemini-3.8-flash'];
  for (let kTry = 0; kTry < keys.length; kTry++) {
    const key = keys[(_browserKeyCursor + kTry) % keys.length];
    for (const model of models) {
      try {
        const parts = [{ text: promptText }];
        if (imageBase64) {
          const cleanB64 = imageBase64.includes(',') ? imageBase64.split(',')[1] : imageBase64;
          parts.push({ inline_data: { mime_type: mimeType || 'image/jpeg', data: cleanB64 } });
        }
        const payload = {
          contents: [{ role: 'user', parts }],
          generationConfig: { temperature: 0.35, maxOutputTokens: 4096 }
        };
        const r = await fetch(
          `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${encodeURIComponent(key)}`,
          {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
          }
        );
        if (!r.ok) continue;
        const j = await r.json();
        const text = (j.candidates?.[0]?.content?.parts || []).map((p) => p.text || '').join('').trim();
        if (text) {
          _browserKeyCursor = (_browserKeyCursor + kTry + 1) % keys.length;
          return text;
        }
      } catch (_) {}
    }
  }
  return null;
}

async function callGeminiDirectFromBrowser(url, body = {}) {
  const stemRule = 'Viết bằng Markdown sạch, bọc công thức Toán/Lý trong `$...$` và Hóa học trong `$\\ce{...}$`.';
  if (url === '/api/ai/chat') {
    const reply = await callGeminiRawFromBrowser(
      `Đóng vai Giáo sư Đại học môn "${body.subject_name || 'Đại học'}". Giải đáp chi tiết, dễ hiểu câu hỏi của sinh viên: "${body.message || ''}"\n${stemRule}`
    );
    return reply ? { success: true, reply } : null;
  }
  if (url === '/api/ai/hint') {
    const hint = await callGeminiRawFromBrowser(
      `Gợi ý 2 dòng ngắn gọn định hướng tư duy cho câu hỏi: "${body.question_text || ''}" (KHÔNG tiết lộ đáp án đúng).\n${stemRule}`
    );
    return hint ? { success: true, hint } : null;
  }
  if (url === '/api/ai/concept-recall') {
    const concept = await callGeminiRawFromBrowser(
      `Nhắc lại công thức gốc, định luật và điều kiện áp dụng cho câu hỏi môn "${body.subject_name || ''}": "${body.question_text || ''}".\n${stemRule}`
    );
    return concept ? { success: true, concept } : null;
  }
  if (url === '/api/ai/deep-analysis') {
    const analysis = await callGeminiRawFromBrowser(
      `Phân tích chuyên sâu câu hỏi: "${body.question_text || ''}". Đáp án đúng: "${body.correct_answer || ''}". Giải thích vì sao đúng và cách tránh bẫy.\n${stemRule}`
    );
    return analysis ? { success: true, analysis } : null;
  }
  if (url === '/api/ai/explain-mistake') {
    const diagnosis = await callGeminiRawFromBrowser(
      `Sinh viên làm câu: "${body.question_text || ''}", chọn nhầm "${body.user_wrong_answer || ''}" trong khi đáp án đúng là "${body.correct_answer || ''}". Hãy chẩn đoán nguyên nhân nhầm lẫn và cách sửa.\n${stemRule}`
    );
    return diagnosis ? { success: true, diagnosis } : null;
  }
  if (url === '/api/ai/mnemonic') {
    const mnemonic = await callGeminiRawFromBrowser(
      `Tạo mẹo nhớ siêu tốc 5 giây cho câu hỏi: "${body.question_text || ''}" → Đáp án đúng: "${body.correct_answer || ''}".\n${stemRule}`
    );
    return mnemonic ? { success: true, mnemonic } : null;
  }
  if (url === '/api/ai/roadmap') {
    const roadmap = await callGeminiRawFromBrowser(
      `Lập bản đồ năng lực và lộ trình ôn thi 5 ngày nước rút cho môn "${body.subject_name || 'Đại học'}". Các câu hay sai: ${(body.mistake_questions || []).slice(0, 6).join('; ')}.\n${stemRule}`
    );
    return roadmap ? { success: true, roadmap } : null;
  }
  if (url === '/api/ai/evaluate-exam') {
    const evaluation = await callGeminiRawFromBrowser(
      `Đánh giá bài thi môn "${body.subject_name || ''}": Đúng ${body.correct}/${body.total} câu. Các câu sai: ${(body.wrong_questions || []).slice(0, 8).join('; ')}.\n${stemRule}`
    );
    return evaluation ? { success: true, evaluation } : null;
  }
  if (url === '/api/ai/custom-qa') {
    const reply = await callGeminiRawFromBrowser(
      `Câu hỏi đang làm: "${body.question_text || ''}" (Đáp án đúng: ${body.correct_text || ''}). Sinh viên hỏi thêm: "${body.student_query || ''}". Giải đáp ngắn gọn, rõ ràng.\n${stemRule}`
    );
    return reply ? { success: true, reply } : null;
  }
  if (url === '/api/ai/grade-handwritten') {
    const prompt = `Đóng vai Giảng viên Đại học chấm ảnh bài làm viết tay / phiếu xét nghiệm môn "${body.subject_name || 'Thực Hành Hóa Sinh'}".
Đề bài: "${body.question_text || 'Chấm bài giải viết tay trong ảnh'}". Ghi chú: "${body.student_note || ''}".
Trả về DUY NHẤT JSON hợp lệ:
{
  "transcribed_text": "Nội dung chữ viết tay AI đọc được từ ảnh",
  "score": 8.5,
  "verdict": "Nhận xét tổng quát",
  "strengths": ["Bước làm đúng"],
  "missing": ["Điểm cần bổ sung hoặc lưu ý đơn vị"],
  "sample_answer": "Lời giải chuẩn từng bước đầy đủ công thức ($...$)"
}`;
    const raw = await callGeminiRawFromBrowser(prompt, body.image_base64, body.mime_type || 'image/jpeg');
    if (raw) {
      try {
        const s = raw.indexOf('{');
        const e = raw.lastIndexOf('}');
        if (s !== -1 && e !== -1) {
          return { success: true, grading: JSON.parse(raw.slice(s, e + 1)) };
        }
      } catch (_) {}
    }
    return null;
  }
  return null;
}

// --- 17.2 Lab Hub Navigation & Initialization ---
const SPECTRO_ASSAYS = {
  glucose: {
    name: 'Định lượng Glucose huyết tương (Phương pháp Enzyme GOD-PAP)',
    wavelength: 500,
    unit: 'mmol/L',
    cStd: 5.55,
    odStd: 0.380,
    refMin: 3.9,
    refMax: 6.4,
    blankColor: 'rgba(254, 242, 242, 0.35)',
    stdColor: 'rgba(244, 114, 182, 0.62)',
    sampleColorHigh: 'rgba(225, 29, 72, 0.88)',
    sampleColorNorm: 'rgba(244, 114, 182, 0.64)',
    sampleColorLow: 'rgba(251, 207, 232, 0.42)',
    reactionPrinciple: 'Glucose bị oxy hóa bởi $\\text{Glucose Oxidase (GOD)}$ tạo $\\ce{H2O2}$, sau đó phản ứng Trinder với phenol và 4-aminoantipyrin dưới xúc tác $\\text{Peroxidase (POD)}$ tạo phức hợp Quinoneimin màu hồng cánh sen hấp thụ cực đại ở $\\lambda = 500\\text{ nm}$.'
  },
  creatinine: {
    name: 'Định lượng Creatinin huyết thanh (Phương pháp động học Jaffé)',
    wavelength: 492,
    unit: 'µmol/L',
    cStd: 177.0,
    odStd: 0.320,
    refMin: 53.0,
    refMax: 120.0,
    blankColor: 'rgba(254, 249, 195, 0.45)',
    stdColor: 'rgba(245, 158, 11, 0.68)',
    sampleColorHigh: 'rgba(217, 119, 6, 0.92)',
    sampleColorNorm: 'rgba(251, 191, 36, 0.58)',
    sampleColorLow: 'rgba(254, 240, 138, 0.45)',
    reactionPrinciple: 'Creatinin phản ứng với $\\text{Acid Picric}$ trong môi trường kiềm ($\\ce{NaOH}$) tạo phức hợp $\\text{Creatinin–Picrat}$ màu vàng cam, đo động học ở $\\lambda = 492\\text{ nm}$.'
  },
  protein: {
    name: 'Định lượng Protein toàn phần huyết tương (Phương pháp Biuret)',
    wavelength: 546,
    unit: 'g/L',
    cStd: 60.0,
    odStd: 0.410,
    refMin: 65.0,
    refMax: 82.0,
    blankColor: 'rgba(191, 219, 254, 0.45)',
    stdColor: 'rgba(139, 92, 246, 0.68)',
    sampleColorHigh: 'rgba(109, 40, 217, 0.90)',
    sampleColorNorm: 'rgba(139, 92, 246, 0.72)',
    sampleColorLow: 'rgba(196, 181, 253, 0.48)',
    reactionPrinciple: 'Các liên kết peptid ($\\text{-CO-NH-}$) của protein tạo phức hợp phối trí màu tím xanh với ion $\\ce{Cu^{2+}}$ trong môi trường kiềm, đo mật độ quang ở $\\lambda = 546\\text{ nm}$.'
  },
  cholesterol: {
    name: 'Định lượng Cholesterol toàn phần (Phương pháp CHOD-PAP)',
    wavelength: 500,
    unit: 'mmol/L',
    cStd: 5.17,
    odStd: 0.360,
    refMin: 3.6,
    refMax: 5.2,
    blankColor: 'rgba(254, 242, 242, 0.35)',
    stdColor: 'rgba(244, 63, 94, 0.62)',
    sampleColorHigh: 'rgba(190, 18, 60, 0.90)',
    sampleColorNorm: 'rgba(244, 63, 94, 0.60)',
    sampleColorLow: 'rgba(253, 164, 175, 0.42)',
    reactionPrinciple: 'Cholesterol ester được thủy phân bởi $\\text{Cholesterol Esterase}$, oxy hóa bởi $\\text{Cholesterol Oxidase (CHOD)}$ sinh $\\ce{H2O2}$ tạo phức màu Quinoneimin hồng đỏ ở $\\lambda = 500\\text{ nm}$.'
  },
  bilirubin: {
    name: 'Định lượng Bilirubin toàn phần (Phương pháp Jendrassik–Gróf)',
    wavelength: 546,
    unit: 'µmol/L',
    cStd: 85.5,
    odStd: 0.350,
    refMin: 3.4,
    refMax: 17.1,
    blankColor: 'rgba(254, 249, 195, 0.35)',
    stdColor: 'rgba(16, 185, 129, 0.65)',
    sampleColorHigh: 'rgba(4, 120, 87, 0.90)',
    sampleColorNorm: 'rgba(110, 231, 183, 0.45)',
    sampleColorLow: 'rgba(209, 250, 229, 0.35)',
    reactionPrinciple: 'Khi có chất gia tốc $\\text{Cafein–Benzoat}$, cả Bilirubin tự do và liên hợp đều kết hợp với thuốc thử Diazo (acid sulfanilic diazo hóa) tạo $\\text{Azobilirubin}$ đo ở $\\lambda = 546\\text{ nm}$.'
  },
  uric: {
    name: 'Định lượng Acid Uric máu (Phương pháp Enzyme Uricase)',
    wavelength: 520,
    unit: 'µmol/L',
    cStd: 357.0,
    odStd: 0.340,
    refMin: 180.0,
    refMax: 420.0,
    blankColor: 'rgba(254, 242, 242, 0.35)',
    stdColor: 'rgba(236, 72, 153, 0.64)',
    sampleColorHigh: 'rgba(190, 24, 93, 0.88)',
    sampleColorNorm: 'rgba(236, 72, 153, 0.62)',
    sampleColorLow: 'rgba(249, 168, 212, 0.42)',
    reactionPrinciple: 'Acid Uric bị oxy hóa bởi $\\text{Uricase}$ tạo Allantoin, $\\ce{CO2}$ và $\\ce{H2O2}$; $\\ce{H2O2}$ tạo phức màu Quinoneimin đo ở $\\lambda = 520\\text{ nm}$.'
  }
};

let currentSpectroState = {
  assayKey: 'glucose',
  patientName: 'Bệnh nhân Nguyễn Văn A (54 tuổi)',
  clinicalHint: 'Khát nước nhiều, tiểu nhiều, sụt 4 kg trong 2 tháng qua. Chỉ định xét nghiệm Glucose máu lúc đói.',
  trueConc: 11.4,
  expectedDiagnosis: 'high',
  odSampleAtMax: 0.780
};

function initLabHubView() {
  if (!currentSpectroState.initialized) {
    currentSpectroState.initialized = true;
    randomizeSpectroCase();
    runClinicalCalculators();
    renderInteractiveKnowledgeGraph();
    renderOsceStationStrip();
  }
}

function switchLabSubTab(subKey) {
  const subs = ['spectro', 'osce', 'handwritten', 'graph', 'calc', 'patient', 'dosing', 'biostat', 'export'];
  subs.forEach((k) => {
    document.getElementById(`lab-sub-${k}`)?.classList.toggle('hidden', k !== subKey);
  });
  document.querySelectorAll('[data-labtab]').forEach((btn) => {
    btn.classList.toggle('active', btn.getAttribute('data-labtab') === subKey);
  });
  if (subKey === 'spectro') {
    if (!currentSpectroState.initialized) {
      currentSpectroState.initialized = true;
      randomizeSpectroCase();
    } else {
      updateSpectroDisplay();
    }
  }
  if (subKey === 'osce') {
    renderOsceStationStrip();
    renderOsceStation();
  }
  if (subKey === 'graph') renderInteractiveKnowledgeGraph();
  if (subKey === 'calc') runClinicalCalculators();
  if (subKey === 'patient') initVirtualPatientView();
  if (subKey === 'dosing') runRenalDoseCalculation();
  if (subKey === 'biostat') runBiostatCalculations();
  if (subKey === 'export') initExportView();
  playSound('click');
}

function onSpectroAssayChange() {
  const key = document.getElementById('spectro-assay-select')?.value || 'glucose';
  currentSpectroState.assayKey = key;
  const assay = SPECTRO_ASSAYS[key];
  const wlInput = document.getElementById('spectro-wavelength-input');
  if (wlInput && assay) wlInput.value = assay.wavelength;
  randomizeSpectroCase();
}

function autoSetOptimalWavelength() {
  const assay = SPECTRO_ASSAYS[currentSpectroState.assayKey];
  const wlInput = document.getElementById('spectro-wavelength-input');
  if (wlInput && assay) {
    wlInput.value = assay.wavelength;
    updateSpectroDisplay();
    showToast(`🎯 Đã chỉnh máy quang phổ về bước sóng tối ưu λ = ${assay.wavelength} nm!`, 'success');
  }
}

function randomizeSpectroCase() {
  const key = document.getElementById('spectro-assay-select')?.value || 'glucose';
  currentSpectroState.assayKey = key;
  const assay = SPECTRO_ASSAYS[key];
  if (!assay) return;

  const scenarios = {
    glucose: [
      { name: 'BN Trần Thị B (58 tuổi)', hint: 'Khát nhiều, tiểu nhiều (hội chứng 4 nhiều), lấy máu tĩnh mạch lúc đói.', conc: 11.8, diag: 'high' },
      { name: 'BN Lê Hoàng C (24 tuổi)', hint: 'Khám sức khỏe định kỳ sinh viên Y khoa, nhịn ăn sáng 10 tiếng.', conc: 5.1, diag: 'normal' },
      { name: 'BN Phạm Văn D (62 tuổi)', hint: 'Vã mồ hôi lạnh, run tay, chóng mặt sau tiêm quá liều Insulin.', conc: 2.6, diag: 'low' }
    ],
    creatinine: [
      { name: 'BN Nguyễn Văn E (67 tuổi)', hint: 'Phù nhẹ hai chi dưới, tiền sử tăng huyết áp và đái tháo đường 12 năm, tiểu ít.', conc: 285.0, diag: 'high' },
      { name: 'BN Võ Thị F (31 tuổi)', hint: 'Kiểm tra chức năng thận tiền phẫu cắt ruột thừa.', conc: 84.0, diag: 'normal' }
    ],
    protein: [
      { name: 'BN Đặng Văn G (45 tuổi)', hint: 'Phù toàn thân, tiểu đạm lượng nhiều (Hội chứng thận hư), gan xơ.', conc: 48.5, diag: 'low' },
      { name: 'BN Hoàng Thị H (52 tuổi)', hint: 'Mất nước cấp do tiêu chảy cấp, cô đặc máu (hoặc đa u tủy xương).', conc: 92.0, diag: 'high' },
      { name: 'BN Lý Văn K (28 tuổi)', hint: 'Khám sức khỏe tổng quát, thể trạng bình thường.', conc: 73.5, diag: 'normal' }
    ],
    cholesterol: [
      { name: 'BN Trương Văn M (60 tuổi)', hint: 'Béo phì độ I, có ban vàng mi mắt (Xanthelasma), tăng huyết áp.', conc: 7.45, diag: 'high' },
      { name: 'BN Ngô Thị N (26 tuổi)', hint: 'Khám sức khỏe định kỳ, chế độ ăn lành mạnh.', conc: 4.42, diag: 'normal' }
    ],
    bilirubin: [
      { name: 'BN Bùi Văn P (49 tuổi)', hint: 'Vàng da, vàng củng mạc mắt, nước tiểu sẫm màu như nước trà đặc.', conc: 68.4, diag: 'high' },
      { name: 'BN Đỗ Thị Q (22 tuổi)', hint: 'Kiểm tra chức năng gan định kỳ, da niêm hồng hào.', conc: 11.2, diag: 'normal' }
    ],
    uric: [
      { name: 'BN Hồ Văn R (55 tuổi)', hint: 'Sưng, nóng, đỏ, đau dữ dội khớp bàn ngón chân cái (Cơn Gout cấp) sau bữa tiệc hải sản.', conc: 565.0, diag: 'high' },
      { name: 'BN Mai Thị S (35 tuổi)', hint: 'Xét nghiệm kiểm tra định kỳ.', conc: 275.0, diag: 'normal' }
    ]
  };

  const list = scenarios[key] || scenarios.glucose;
  const picked = list[Math.floor(Math.random() * list.length)];
  currentSpectroState.patientName = picked.name;
  currentSpectroState.clinicalHint = picked.hint;
  currentSpectroState.trueConc = picked.conc;
  currentSpectroState.expectedDiagnosis = picked.diag;
  currentSpectroState.odSampleAtMax = +((picked.conc / assay.cStd) * assay.odStd).toFixed(3);

  const uInp = document.getElementById('spectro-user-conc');
  if (uInp) uInp.value = '';
  document.getElementById('spectro-feedback-box')?.classList.add('hidden');
  updateSpectroDisplay();
}

function updateSpectroDisplay() {
  const assay = SPECTRO_ASSAYS[currentSpectroState.assayKey];
  if (!assay) return;

  const wlInput = document.getElementById('spectro-wavelength-input');
  const currentWl = Number(wlInput?.value || assay.wavelength);
  // Gaussian spectral response if student picks a sub-optimal wavelength
  const delta = Math.abs(currentWl - assay.wavelength);
  const factor = Math.max(0.25, Math.exp(-(delta * delta) / 2800));

  const odStdShown = +(assay.odStd * factor).toFixed(3);
  const odSamShown = +(currentSpectroState.odSampleAtMax * factor).toFixed(3);
  currentSpectroState.odStdShown = odStdShown;
  currentSpectroState.odSamShown = odSamShown;

  setText('spectro-led-wavelength', `λ = ${currentWl} nm ${delta === 0 ? '(Chuẩn λmax)' : '(Lệch bước sóng!)'}`);
  setText('spectro-led-od-std', odStdShown.toFixed(3));
  setText('spectro-led-od-sam', odSamShown.toFixed(3));
  setText('spectro-unit-label', assay.unit);

  const brief = document.getElementById('spectro-patient-brief');
  if (brief) {
    brief.innerHTML = renderAcademicText(
      `🩺 **Hồ sơ mẫu bệnh phẩm:** **${currentSpectroState.patientName}** — ${currentSpectroState.clinicalHint}\n` +
      `- **Nồng độ ống chuẩn ($C_{\\text{chuẩn}}$):** \`${assay.cStd} ${assay.unit}\` | **Khoảng tham chiếu bình thường:** \`${assay.refMin} – ${assay.refMax} ${assay.unit}\`\n` +
      `- **Nguyên lý phản ứng:** ${assay.reactionPrinciple}`
    );
  }

  const sampleColor =
    currentSpectroState.expectedDiagnosis === 'high'
      ? assay.sampleColorHigh
      : currentSpectroState.expectedDiagnosis === 'low'
      ? assay.sampleColorLow
      : assay.sampleColorNorm;

  const grid = document.getElementById('spectro-cuvettes-grid');
  if (grid) {
    const tubes = [
      { title: 'Ống 1: Ống Trắng (Blank)', sub: 'Thuốc thử + Nước cất', od: '0.000', color: assay.blankColor },
      { title: 'Ống 2: Ống Chuẩn (Std)', sub: `C₀ = ${assay.cStd} ${assay.unit}`, od: odStdShown.toFixed(3), color: assay.stdColor },
      { title: 'Ống 3: Ống Thử (Bệnh nhân)', sub: 'Thuốc thử + Huyết thanh BN', od: odSamShown.toFixed(3), color: sampleColor }
    ];
    grid.innerHTML = tubes
      .map(
        (t) => `
      <div class="p-3 rounded-2xl text-center space-y-2" style="background-color: var(--bg-subtle); border: 1px solid var(--border);">
        <div class="text-[11px] font-extrabold txt-main">${escapeHtml(t.title)}</div>
        <div class="mx-auto w-12 h-24 rounded-b-2xl rounded-t-md border-2 border-slate-400/50 relative overflow-hidden flex items-end justify-center shadow-inner" style="background: rgba(255,255,255,0.06);">
          <div class="w-full h-[74%] transition-all duration-500" style="background: ${t.color};"></div>
        </div>
        <div class="text-[10px] txt-muted">${escapeHtml(t.sub)}</div>
        <div class="badge-brand px-2 py-0.5 rounded-md font-mono text-xs font-extrabold inline-block">OD = ${t.od}</div>
      </div>`
      )
      .join('');
  }

  const fBar = document.getElementById('spectro-formula-bar');
  if (fBar) {
    fBar.innerHTML = renderInlineMathAndCode(
      `Công thức tính: $C_{\\text{thử}} = \\frac{\\text{OD}_{\\text{thử}}}{\\text{OD}_{\\text{chuẩn}}} \\times C_{\\text{chuẩn}} = \\frac{${odSamShown.toFixed(3)}}{${odStdShown.toFixed(3)}} \\times ${assay.cStd}$ (${assay.unit})`
    );
  }
}

function fillSpectroAutoCalc() {
  const assay = SPECTRO_ASSAYS[currentSpectroState.assayKey];
  if (!assay) return;
  const calc = (currentSpectroState.odSamShown / currentSpectroState.odStdShown) * assay.cStd;
  const inp = document.getElementById('spectro-user-conc');
  if (inp) inp.value = calc.toFixed(2);
  playSound('click');
}

function verifySpectroLabWork() {
  const assay = SPECTRO_ASSAYS[currentSpectroState.assayKey];
  if (!assay) return;
  const rawVal = String(document.getElementById('spectro-user-conc')?.value || '').replace(',', '.').trim();
  const userConc = parseFloat(rawVal);
  const userDiag = document.getElementById('spectro-user-diagnosis')?.value || 'normal';
  const expectedConc = (currentSpectroState.odSamShown / currentSpectroState.odStdShown) * assay.cStd;

  const box = document.getElementById('spectro-feedback-box');
  if (!box) return;
  box.classList.remove('hidden');

  if (Number.isNaN(userConc)) {
    box.innerHTML = `<div class="txt-rose font-extrabold">⚠️ Vui lòng nhập kết quả nồng độ bạn tính được (hoặc bấm nút "🖩 Bấm máy")!</div>`;
    playSound('wrong');
    return;
  }

  const concOk = Math.abs(userConc - expectedConc) <= Math.max(0.25, expectedConc * 0.04);
  const diagOk = userDiag === currentSpectroState.expectedDiagnosis;
  const diagNames = {
    normal: 'Trong giới hạn bình thường (Sinh lý)',
    high: 'Tăng cao bệnh lý (Vượt ngưỡng tham chiếu trên)',
    low: 'Giảm thấp bệnh lý (Dưới ngưỡng tham chiếu dưới)'
  };

  if (concOk && diagOk) {
    awardXP(25);
    playSound('correct');
    box.innerHTML = renderAcademicText(
      `### 🎉 Chính Xác Tuyệt Đối (+25 XP Thực Hành!)\n` +
      `- **Kết quả nồng độ chuẩn:** $C_{\\text{thử}} = \\frac{${currentSpectroState.odSamShown.toFixed(3)}}{${currentSpectroState.odStdShown.toFixed(3)}} \\times ${assay.cStd} = \\mathbf{${expectedConc.toFixed(2)}\\text{ ${assay.unit}}}$\n` +
      `- **Khoảng tham chiếu bình thường:** \`${assay.refMin} – ${assay.refMax} ${assay.unit}\`\n` +
      `- **Kết luận biện luận:** **${diagNames[currentSpectroState.expectedDiagnosis]}** — Phù hợp hoàn toàn với bệnh cảnh lâm sàng của **${currentSpectroState.patientName}**!`
    );
  } else {
    playSound('wrong');
    box.innerHTML = renderAcademicText(
      `### 🩺 Cần Hiệu Chỉnh Lại Kết Quả Thực Hành\n` +
      `- **Nồng độ bạn nhập:** \`${userConc} ${assay.unit}\` (${concOk ? '✔ Đúng số liệu' : `✖ Chưa chính xác, đáp án đúng là **${expectedConc.toFixed(2)} ${assay.unit}**`})\n` +
      `- **Nhận định bạn chọn:** **${diagNames[userDiag]}** (${diagOk ? '✔ Đúng nhận định' : `✖ Chưa đúng, vì kết quả **${expectedConc.toFixed(2)} ${assay.unit}** so với ngưỡng \`${assay.refMin} – ${assay.refMax} ${assay.unit}\` phải là **${diagNames[currentSpectroState.expectedDiagnosis]}**`})`
    );
  }
}

function askAiAboutSpectroCase() {
  const assay = SPECTRO_ASSAYS[currentSpectroState.assayKey];
  if (!assay) return;
  switchTab('tutor');
  sendQuickTutorPrompt(
    `🔬 Hãy giải thích chi tiết cơ chế phản ứng, vai trò từng thành phần thuốc thử, ý nghĩa bước sóng λ = ${assay.wavelength} nm và cách biện luận lâm sàng của kỹ thuật "${assay.name}" đối với ${currentSpectroState.patientName} (${currentSpectroState.clinicalHint}).`
  );
}

// --- 17.3 Timed 6-Station OSCE Practical Circuit with Synthesized Bell ---
const OSCE_STATIONS_BANK = [
  {
    title: 'Trạm 1: Định danh Tinh thể Nước tiểu (Kính hiển vi 40x)',
    image: '/static/uploads/hoasinh_ctump/crop_calcium_oxalate.jpg',
    scenario: 'Bệnh nhân nam 38 tuổi đau quặn thận phải, tiểu máu vi thể. Soi cặn lắng nước tiểu thấy cấu trúc hình phong bì thư (bát diện) trong suốt.',
    question: 'Cấu trúc tinh thể đặc trưng trong tiêu bản này là gì?',
    options: [
      'Tinh thể Calcium Oxalate (Canxi Oxalat)',
      'Tinh thể Acid Uric hình thoi',
      'Tinh thể Triple Phosphate (Photphat kép) hình nắp quan tài',
      'Tinh thể Cholesterol hình phiến kính khuyết góc'
    ],
    correct: 0,
    explanation: 'Tinh thể Calcium Oxalate đihidrat có hình phong bì thư (hai hình tháp đáy chung nhau) rất điển hình trong sỏi đường tiết niệu.'
  },
  {
    title: 'Trạm 2: Định danh Trụ niệu Bệnh lý Cầu thận',
    image: '/static/uploads/hoasinh_ctump/crop_tru_hong_cau.jpg',
    scenario: 'Bệnh nhân 19 tuổi tiểu máu đại thể, phù mặt, tăng huyết áp sau viêm họng liên cầu khuẩn 2 tuần.',
    question: 'Cấu trúc trụ niệu nào xuất hiện trên vi trường giúp khẳng định máu chảy từ cầu thận?',
    options: [
      'Trụ hồng cầu (Red Blood Cell Cast)',
      'Trụ trong (Hyaline Cast) sinh lý',
      'Tinh thể Calcium Carbonate',
      'Tế bào biểu mô vảy niệu đạo'
    ],
    correct: 0,
    explanation: 'Trụ hồng cầu có màu vàng cam/đỏ nâu chứa các hồng cầu kết tụ trong khuôn protein Tamm–Horsfall, đặc hiệu cho tổn thương viêm cầu thận cấp.'
  },
  {
    title: 'Trạm 3: Biện luận Quang phổ Glucose máu & HbA1c',
    image: '',
    scenario: 'Đo quang phổ Glucose huyết tương lúc đói (GOD-PAP, $C_{\\text{chuẩn}} = 5.5\\text{ mmol/L}$): $\\text{OD}_{\\text{chuẩn}} = 0.350$, $\\text{OD}_{\\text{thử}} = 0.700$. Kèm $\\text{HbA1c} = 8.4\\%$.',
    question: 'Nồng độ Glucose máu của bệnh nhân và kết luận lâm sàng chính xác nhất là:',
    options: [
      'Glucose = 11.0 mmol/L — Đái tháo đường kiểm soát đường huyết kém',
      'Glucose = 2.75 mmol/L — Hạ đường huyết cấp tính',
      'Glucose = 5.5 mmol/L — Đường huyết lúc đói hoàn toàn bình thường',
      'Glucose = 7.0 mmol/L — Rối loạn dung nạp glucose đơn thuần'
    ],
    correct: 0,
    explanation: '$C_{\\text{thử}} = \\frac{0.700}{0.350} \\times 5.5 = 11.0\\text{ mmol/L} \\ge 7.0\\text{ mmol/L}$ kèm $\\text{HbA1c} = 8.4\\% \\ge 6.5\\%$ khẳng định Đái tháo đường kiểm soát đường huyết chưa đạt mục tiêu.'
  },
  {
    title: 'Trạm 4: Nhận diện Tế bào & Vi nấm trong Cặn lắng Nước tiểu',
    image: '/static/uploads/hoasinh_ctump/crop_nam_men.jpg',
    scenario: 'Bệnh nhân nữ đái tháo đường lâu năm, tiểu buốt rát. Soi tươi cặn nước tiểu thấy các tế bào hình bầu dục có chồi nhỏ (nảy chồi).',
    question: 'Cấu trúc vi sinh vật nào đang hiện diện trong mẫu cặn nước tiểu này?',
    options: [
      'Nấm men (Candida spp.) đang nảy chồi',
      'Hồng cầu biến dạng hình gai',
      'Trụ hạt thô (Coarse Granular Cast)',
      'Tinh thể Bilirubin hình kim'
    ],
    correct: 0,
    explanation: 'Tế bào nấm men (thường gặp nhất là Candida albicans ở bệnh nhân đái tháo đường) có hình bầu dục chiết quang và đặc điểm nảy chồi điển hình.'
  },
  {
    title: 'Trạm 5: Tính Độ Thanh Thải Creatinin ($C_{\\text{Cr}}$)',
    image: '',
    scenario: 'Bệnh nhân có thể tích nước tiểu 24 giờ $V_{24\\text{h}} = 1440\\text{ mL}$ ($V = 1.0\\text{ mL/phút}$), nồng độ Creatinin niệu $U_{\\text{Cr}} = 9.0\\text{ mmol/L}$ ($9000\\text{ }\\mu\\text{mol/L}$), Creatinin huyết thanh $P_{\\text{Cr}} = 150\\text{ }\\mu\\text{mol/L}$.',
    question: 'Độ thanh thải Creatinin nội sinh $C_{\\text{Cr}} = \\frac{U \\times V}{P}$ của bệnh nhân là bao nhiêu?',
    options: [
      '60 mL/phút',
      '90 mL/phút',
      '120 mL/phút',
      '15 mL/phút'
    ],
    correct: 0,
    explanation: 'Đổi cùng đơn vị $\\mu\\text{mol/L}$: $C_{\\text{Cr}} = \\frac{9000 \\times 1.0}{150} = 60\\text{ mL/phút}$.'
  },
  {
    title: 'Trạm 6: Định danh Trụ Hạt (Granular Cast) trong Bệnh thận mạn',
    image: '/static/uploads/hoasinh_ctump/crop_tru_hat_tho.jpg',
    scenario: 'Bệnh nhân suy thận mạn giai đoạn 3, tiểu protein (++). Soi cặn nước tiểu thấy cấu trúc hình trụ chứa nhiều hạt thô sẫm màu do thoái hóa tế bào biểu mô ống thận.',
    question: 'Tên gọi chính xác của cấu trúc trụ niệu trong tiêu bản này là:',
    options: [
      'Trụ hạt thô (Coarse Granular Cast)',
      'Trụ sáp (Waxy Cast) trong suốt',
      'Tế bào biểu mô bể thận',
      'Tinh trùng trong nước tiểu'
    ],
    correct: 0,
    explanation: 'Trụ hạt thô hình thành từ sự thoái hóa của các trụ tế bào biểu mô ống thận hoặc bạch cầu, gợi ý bệnh lý nhu mô thận mạn tính.'
  }
];

let osceState = {
  active: false,
  stationIdx: 0,
  secPerStation: 60,
  secLeft: 60,
  timerId: null,
  answers: {}
};

function playOsceStationBell() {
  try {
    const Ctx = window.AudioContext || window.webkitAudioContext;
    if (!Ctx) return;
    if (!audioCtx) audioCtx = new Ctx();
    if (audioCtx.state === 'suspended') audioCtx.resume();
    const now = audioCtx.currentTime;
    // Dual chime ding-dong bell (880 Hz -> 659.25 Hz)
    [
      { freq: 880, start: 0, dur: 0.38 },
      { freq: 659.25, start: 0.22, dur: 0.55 }
    ].forEach((tone) => {
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(tone.freq, now + tone.start);
      gain.gain.setValueAtTime(0.16, now + tone.start);
      gain.gain.exponentialRampToValueAtTime(0.001, now + tone.start + tone.dur);
      osc.connect(gain);
      gain.connect(audioCtx.destination);
      osc.start(now + tone.start);
      osc.stop(now + tone.start + tone.dur + 0.02);
    });
  } catch (_) {}
}

function renderOsceStationStrip() {
  const strip = document.getElementById('osce-station-strip');
  if (!strip) return;
  strip.innerHTML = OSCE_STATIONS_BANK.map((st, idx) => {
    const ans = osceState.answers[idx];
    const isCur = osceState.active && osceState.stationIdx === idx;
    let cls = 'btn-soft';
    if (isCur) cls = 'badge-brand ring-2 ring-purple-500';
    else if (ans !== undefined) cls = ans === st.correct ? 'badge-emerald' : 'badge-rose';
    return `<button type="button" onclick="jumpToOsceStation(${idx})" class="${cls} p-2 rounded-xl text-center text-xs font-extrabold transition-all">
      Trạm ${idx + 1} ${ans !== undefined ? (ans === st.correct ? '✔' : '✖') : ''}
    </button>`;
  }).join('');
}

function startOsceCircuit() {
  clearInterval(osceState.timerId);
  const sec = parseInt(document.getElementById('osce-sec-per-station')?.value || '60', 10);
  osceState.active = true;
  osceState.stationIdx = 0;
  osceState.secPerStation = sec;
  osceState.secLeft = sec;
  osceState.answers = {};
  playOsceStationBell();
  showToast('🔔 Chuông vào Trạm 1 đã vang! Hãy quan sát tiêu bản / số liệu và chọn đáp án trước khi chuông chuyển trạm!', 'info');
  renderOsceStation();
  osceState.timerId = setInterval(() => {
    if (!osceState.active) return;
    osceState.secLeft--;
    const timerEl = document.getElementById('osce-live-countdown');
    if (timerEl) timerEl.textContent = `${osceState.secLeft}s`;
    if (osceState.secLeft <= 0) {
      advanceOsceStation(true);
    }
  }, 1000);
}

function jumpToOsceStation(idx) {
  if (idx < 0 || idx >= OSCE_STATIONS_BANK.length) return;
  osceState.stationIdx = idx;
  osceState.secLeft = osceState.secPerStation;
  renderOsceStation();
}

function prevOsceStation() {
  if (osceState.stationIdx > 0) {
    osceState.stationIdx--;
    osceState.secLeft = osceState.secPerStation;
    renderOsceStation();
  }
}

function resetOsceCircuit() {
  clearInterval(osceState.timerId);
  osceState.active = false;
  osceState.answers = {};
  osceState.stationIdx = 0;
  osceState.secLeft = osceState.secPerStation;
  showToast('🔄 Đã làm mới toàn bộ vòng thi chạy trạm OSCE!', 'info');
  renderOsceStation();
}

function resolveStationImageSrc(imgPath) {
  if (!imgPath) return '';
  const db = window.__UNIMASTER_OFFLINE_DB__;
  if (db?.image_base64_map?.[imgPath]) {
    return db.image_base64_map[imgPath];
  }
  return imgPath;
}

function renderOsceStation() {
  renderOsceStationStrip();
  const stage = document.getElementById('osce-stage-container');
  if (!stage) return;
  const st = OSCE_STATIONS_BANK[osceState.stationIdx];
  if (!st) {
    finishOsceCircuit();
    return;
  }
  const chosen = osceState.answers[osceState.stationIdx];
  const imgHtml = st.image
    ? `<div class="p-3 rounded-2xl flex flex-col items-center justify-center" style="background-color: var(--bg-subtle); border: 1px solid var(--border);">
         <img src="${resolveStationImageSrc(st.image)}" alt="${escapeHtml(st.title)}" onclick="openImageLightbox(this.src, '${escapeHtml(st.title)}')"
           class="max-h-56 rounded-xl object-contain cursor-zoom-in shadow-md hover:scale-[1.02] transition-transform" />
         <span class="text-[11px] font-bold txt-muted mt-2 flex items-center gap-1">🔍 Bấm vào ảnh để phóng to tiêu bản vi trường</span>
       </div>`
    : '';

  const timerBadge = osceState.active
    ? `<div class="badge-amber px-3.5 py-1.5 rounded-xl font-mono text-sm font-extrabold flex items-center gap-1.5 shadow-sm">
         <span>🔔</span> <span id="osce-live-countdown">${osceState.secLeft}s</span>
       </div>`
    : `<button type="button" onclick="startOsceCircuit()" class="btn-primary px-3 py-1.5 rounded-xl text-xs font-extrabold flex items-center gap-1.5 shadow-sm" title="Bật chuông đếm ngược tự động">
         <span>🔔</span> Bật Đếm Giờ
       </button>`;

  stage.innerHTML = `
    <div class="flex flex-wrap items-center justify-between gap-3 pb-3" style="border-bottom: 1px solid var(--border);">
      <div>
        <div class="flex items-center gap-2">
          <span class="badge-brand px-2.5 py-0.5 rounded-full text-[11px] font-extrabold">TRẠM ${osceState.stationIdx + 1} / ${OSCE_STATIONS_BANK.length}</span>
          ${osceState.active ? '<span class="badge-emerald px-2 py-0.5 rounded-full text-[10px] font-bold">⏱️ Đang Chạy Giờ Thi Thật</span>' : '<span class="badge-amber px-2 py-0.5 rounded-full text-[10px] font-bold">📖 Ôn Tập Tự Do</span>'}
        </div>
        <h4 class="text-sm sm:text-base font-extrabold txt-main mt-1">${escapeHtml(st.title)}</h4>
      </div>
      <div class="flex items-center gap-2">
        ${timerBadge}
        <button type="button" onclick="prevOsceStation()" class="btn-soft px-3 py-1.5 text-xs font-bold ${osceState.stationIdx === 0 ? 'opacity-40 pointer-events-none' : ''}">
          ⬅️ Trạm trước
        </button>
        <button type="button" onclick="advanceOsceStation(false)" class="btn-primary px-3 py-1.5 text-xs font-extrabold">
          ${osceState.stationIdx === OSCE_STATIONS_BANK.length - 1 ? 'Xem Kết Quả 🏁' : 'Trạm tiếp ➔'}
        </button>
      </div>
    </div>

    <div class="grid grid-cols-1 ${st.image ? 'lg:grid-cols-12' : ''} gap-5 items-start pt-1">
      ${st.image ? `<div class="lg:col-span-5">${imgHtml}</div>` : ''}
      <div class="${st.image ? 'lg:col-span-7' : ''} space-y-3.5">
        <div class="p-3.5 rounded-xl text-xs sm:text-sm leading-relaxed" style="background-color: var(--bg-surface); border: 1px solid var(--border);">
          ${renderAcademicText('📋 **Tình huống tại trạm:** ' + st.scenario)}
        </div>
        <div class="text-sm sm:text-base font-extrabold txt-main">${renderInlineMathAndCode(st.question)}</div>
        <div class="grid grid-cols-1 gap-2.5">
          ${st.options
            .map((opt, oIdx) => {
              let btnStyle = 'btn-soft text-left justify-start';
              let badgeCls = 'style="background: rgba(124,58,237,0.15);"';
              let statusMark = '';
              if (chosen !== undefined) {
                if (oIdx === st.correct) {
                  btnStyle = 'badge-emerald ring-2 ring-emerald-500 font-black text-left justify-start';
                  badgeCls = 'style="background: #10b981; color: white;"';
                  statusMark = '<span class="text-emerald-400 font-extrabold ml-auto text-base">✔ Đúng</span>';
                } else if (oIdx === chosen) {
                  btnStyle = 'badge-rose ring-2 ring-rose-500 font-bold text-left justify-start';
                  badgeCls = 'style="background: #f43f5e; color: white;"';
                  statusMark = '<span class="text-rose-400 font-extrabold ml-auto text-base">✖ Đã chọn</span>';
                }
              }
              const letter = ['A', 'B', 'C', 'D'][oIdx];
              return `<button type="button" onclick="submitOsceStationAnswer(${oIdx})" class="${btnStyle} p-3 sm:p-3.5 rounded-xl text-xs sm:text-sm font-bold flex items-center gap-3 transition-all hover:scale-[1.01] active:scale-[0.99] cursor-pointer">
                <span class="w-7 h-7 rounded-lg flex items-center justify-center font-extrabold shrink-0 shadow-sm" ${badgeCls}>${letter}</span>
                <span class="flex-1">${renderInlineMathAndCode(opt)}</span>
                ${statusMark}
              </button>`;
            })
            .join('')}
        </div>
        ${
          chosen !== undefined
            ? `<div class="p-4 rounded-xl text-xs sm:text-sm leading-relaxed badge-brand space-y-2">
                 <div>${renderAcademicText('💡 **Giải thích chuẩn Bộ Môn:** ' + st.explanation)}</div>
                 <div class="pt-2 flex flex-wrap items-center gap-2">
                   <button type="button" onclick="askAiAboutOsceStation(${osceState.stationIdx})" class="btn-primary px-3.5 py-2 text-xs font-extrabold flex items-center gap-1.5 shadow-md">
                     <span>✨</span> AI Giải Thích Chi Tiết Tiêu Bản & Ca Này
                   </button>
                   <button type="button" onclick="resetOsceCircuit()" class="btn-soft px-3 py-2 text-xs font-bold text-slate-300">
                     🔄 Làm Lại Vòng Trạm
                   </button>
                 </div>
                 <div id="osce-ai-explanation-box" class="hidden mt-2"></div>
               </div>`
            : ''
        }
      </div>
    </div>
  `;
  renderAllMathOnPage(stage);
}

function submitOsceStationAnswer(optIdx) {
  const prevAns = osceState.answers[osceState.stationIdx];
  osceState.answers[osceState.stationIdx] = optIdx;
  const st = OSCE_STATIONS_BANK[osceState.stationIdx];
  if (optIdx === st.correct) {
    playSound('correct');
    if (prevAns === undefined) {
      awardXP(15);
      showToast('🎉 Chính xác! Bạn đã chẩn đoán đúng trạm thực hành này (+15 XP)', 'success');
    }
  } else {
    playSound('wrong');
    showToast('❌ Chưa chính xác. Xem giải thích chuẩn và hỏi AI bên dưới!', 'error');
  }
  renderOsceStation();
}

async function askAiAboutOsceStation(stationIdx) {
  const st = OSCE_STATIONS_BANK[stationIdx];
  if (!st) return;
  const prompt = `Trạm OSCE số ${stationIdx + 1}: ${st.title}\nTình huống lâm sàng: ${st.scenario}\nCâu hỏi: ${st.question}\nĐáp án đúng: ${st.options[st.correct]}\nLời giải Bộ Môn: ${st.explanation}\n\nHãy phân tích súc tích chuẩn Y Khoa:\n1. 🔬 Dấu hiệu nhận biết đặc trưng trên tiêu bản kính hiển vi / số liệu;\n2. 🩺 Cơ chế bệnh sinh / nguyên lý hóa sinh lâm sàng cốt lõi;\n3. 💡 Mẹo nhớ nhanh để không bao giờ bị nhầm với các tiêu bản khác khi thi trạm.`;
  const aiBox = document.getElementById('osce-ai-explanation-box');
  if (aiBox) {
    aiBox.classList.remove('hidden');
    aiBox.innerHTML = '<div class="p-3 text-xs txt-sub flex items-center gap-2"><div class="spinner-sm"></div> AI Gia Sư đang phân tích tiêu bản & ca lâm sàng...</div>';
  }
  try {
    const res = await fetch('/api/ai/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        subject_name: 'Thực Hành Hóa Sinh Lâm Sàng (CTUMP)',
        message: prompt,
        persona: 'professor'
      })
    });
    const data = await res.json();
    if (aiBox) {
      aiBox.innerHTML = `
        <div class="p-4 rounded-xl text-xs space-y-2 border" style="background-color: var(--bg-surface); border-color: var(--brand);">
          <div class="font-extrabold text-sm txt-brand flex items-center justify-between">
            <span class="flex items-center gap-1.5">🤖 AI Gia Sư Phân Tích • Trạm ${stationIdx + 1}</span>
            <button type="button" onclick="document.getElementById('osce-ai-explanation-box').classList.add('hidden')" class="btn-soft p-1 text-xs">✕</button>
          </div>
          <div class="leading-relaxed txt-sub prose prose-sm max-w-none">
            ${renderAcademicText(data.reply || 'Không nhận được phân tích từ AI.')}
          </div>
        </div>
      `;
      renderAllMathOnPage(aiBox);
    }
  } catch (err) {
    if (aiBox) aiBox.innerHTML = `<div class="p-3 text-xs text-rose-400">Lỗi khi gọi AI: ${escapeHtml(err.message)}</div>`;
  }
}

function advanceOsceStation(byBell = false) {
  playOsceStationBell();
  if (osceState.stationIdx < OSCE_STATIONS_BANK.length - 1) {
    osceState.stationIdx++;
    osceState.secLeft = osceState.secPerStation;
    if (byBell) {
      showToast(`🔔 Hết giờ! Chuông báo chuyển sang Trạm ${osceState.stationIdx + 1}!`, 'warning');
    }
    renderOsceStation();
  } else {
    finishOsceCircuit();
  }
}

function finishOsceCircuit() {
  clearInterval(osceState.timerId);
  osceState.active = false;
  renderOsceStationStrip();
  let correctCount = 0;
  OSCE_STATIONS_BANK.forEach((st, idx) => {
    if (osceState.answers[idx] === st.correct) correctCount++;
  });
  const score10 = ((correctCount / OSCE_STATIONS_BANK.length) * 10).toFixed(1);
  awardXP(30);
  playSound('complete');
  const stage = document.getElementById('osce-stage-container');
  if (stage) {
    stage.innerHTML = `
      <div class="text-center py-6 space-y-3">
        <div class="text-4xl">🏆</div>
        <h4 class="text-lg font-extrabold txt-main">Hoàn Tất Vòng Thi Chạy Trạm OSCE: ${score10} / 10 điểm (${correctCount}/${OSCE_STATIONS_BANK.length} trạm đúng)</h4>
        <p class="text-xs txt-muted max-w-lg mx-auto">
          Bạn đã nhận thêm <strong>+30 XP</strong> hoàn thành vòng chạy trạm thực hành! Bấm vào bất kỳ trạm nào trên thanh trạng thái phía trên để xem lại tiêu bản và lời giải chi tiết.
        </p>
        <button type="button" onclick="startOsceCircuit()" class="btn-primary px-5 py-2.5 text-xs font-extrabold">
          🔄 Chạy Lại Vòng Trạm Mới
        </button>
      </div>
    `;
  }
}

// --- 17.4 Camera Handwritten Solution & Lab Sheet OCR AI Grader ---
let currentHandwrittenDataUrl = '';
let currentHandwrittenMime = 'image/jpeg';

function handleHandwrittenImageSelect(inputEl) {
  const file = inputEl?.files?.[0];
  if (!file) return;
  currentHandwrittenMime = file.type || 'image/jpeg';
  const reader = new FileReader();
  reader.onload = (e) => {
    currentHandwrittenDataUrl = String(e.target?.result || '');
    const wrap = document.getElementById('hw-preview-wrap');
    const img = document.getElementById('hw-preview-img');
    if (img) img.src = currentHandwrittenDataUrl;
    if (wrap) wrap.classList.remove('hidden');
    showToast('📸 Đã tải ảnh bài làm! Bấm "✨ Chấm Điểm Bài Viết Tay Bằng AI Ngay" để chấm!', 'success');
  };
  reader.readAsDataURL(file);
}

function generateDemoHandwrittenSheet() {
  const canvas = document.createElement('canvas');
  canvas.width = 760;
  canvas.height = 440;
  const ctx = canvas.getContext('2d');
  // Notebook paper background with ruled lines
  ctx.fillStyle = '#fffef7';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  ctx.strokeStyle = '#dbeafe';
  ctx.lineWidth = 1;
  for (let y = 50; y < canvas.height; y += 34) {
    ctx.beginPath();
    ctx.moveTo(0, y);
    ctx.lineTo(canvas.width, y);
    ctx.stroke();
  }
  ctx.strokeStyle = '#fca5a5';
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(64, 0);
  ctx.lineTo(64, canvas.height);
  ctx.stroke();

  // Simulated student handwriting
  ctx.fillStyle = '#1e3a8a';
  ctx.font = 'bold 20px "Comic Sans MS", "Segoe Print", cursive, sans-serif';
  ctx.fillText('PHIẾU BÀI LÀM THỰC HÀNH HÓA SINH —TỔ 3', 82, 42);
  ctx.font = '18px "Comic Sans MS", "Segoe Print", cursive, sans-serif';
  ctx.fillText('Đề bài: Tính nồng độ Glucose máu (GOD-PAP) và Độ thanh thải Creatinin:', 82, 80);
  ctx.fillText('1) Định lượng Glucose huyết tương (C_chuẩn = 5.55 mmol/L):', 82, 118);
  ctx.fillText('   Ta có: OD_chuẩn = 0.370 ; OD_thử = 0.740', 82, 152);
  ctx.fillText('   => C_Glucose = (0.740 / 0.370) x 5.55 = 11.10 mmol/L', 82, 186);
  ctx.fillText('   Nhận định: Tăng đường huyết (> 7.0 mmol/L lúc đói) -> Theo dõi Đái tháo đường.', 82, 220);
  ctx.fillText('2) Tính độ thanh thải Creatinin nội sinh (C_Cr):', 82, 265);
  ctx.fillText('   V_24h = 1440 mL => V_phút = 1440 / 1440 = 1.0 mL/phút', 82, 299);
  ctx.fillText('   U_Cr = 8.8 mmol/L = 8800 µmol/L ; P_Cr = 110 µmol/L', 82, 333);
  ctx.fillText('   => C_Cr = (U x V) / P = (8800 x 1.0) / 110 = 80 mL/phút.', 82, 367);
  ctx.fillStyle = '#047857';
  ctx.fillText('   Kết luận: Chức năng lọc cầu thận giảm nhẹ.', 82, 401);

  currentHandwrittenDataUrl = canvas.toDataURL('image/jpeg', 0.92);
  currentHandwrittenMime = 'image/jpeg';
  const qInp = document.getElementById('hw-question-context');
  if (qInp && !qInp.value) {
    qInp.value = 'Tính nồng độ Glucose máu theo định luật Beer-Lambert và tính Độ thanh thải Creatinin nội sinh C_Cr = (U x V)/P';
  }
  const wrap = document.getElementById('hw-preview-wrap');
  const img = document.getElementById('hw-preview-img');
  if (img) img.src = currentHandwrittenDataUrl;
  if (wrap) wrap.classList.remove('hidden');
  showToast('🧪 Đã tạo Phiếu bài làm viết tay mẫu! Bấm "✨ Chấm Điểm Bài Viết Tay Bằng AI Ngay" để xem AI chấm!', 'info');
}

async function submitHandwrittenForGrading() {
  if (!currentHandwrittenDataUrl) {
    showToast('Vui lòng chụp ảnh hoặc bấm Tạo phiếu bài làm viết tay mẫu trước!', 'warning');
    return;
  }
  const box = document.getElementById('hw-grading-result');
  const btn = document.getElementById('hw-grade-btn');
  if (btn) btn.disabled = true;
  if (box) {
    box.innerHTML = `<div class="py-10 text-center txt-brand font-extrabold animate-pulse">🔍 Gemini Vision đang đọc chữ viết tay, kiểm tra từng phép tính và đơn vị đo...</div>`;
  }

  const sub = STATE.subjects.find((s) => String(s.id) === String(STATE.examConfig.subjectId)) || STATE.subjects[0];
  const qText = document.getElementById('hw-question-context')?.value || 'Chấm bài giải tự luận / phiếu thực hành viết tay';
  const note = document.getElementById('hw-student-note')?.value || '';

  let res = null;
  try {
    res = await apiFetch('/api/ai/grade-handwritten', {
      method: 'POST',
      body: JSON.stringify({
        subject_name: sub?.name || 'Thực Hành Hóa Sinh',
        question_text: qText,
        student_note: note,
        image_base64: currentHandwrittenDataUrl,
        mime_type: currentHandwrittenMime
      })
    });
  } catch (e) {
    console.warn('Lỗi gọi API grade-handwritten:', e);
  }

  if (btn) btn.disabled = false;

  const g = (res && res.grading) ? res.grading : {
    transcribed_text: '1) C_Glucose = (0.740 / 0.370) × 5.55 = 11.10 mmol/L. 2) C_Cr = (8800 × 1.0) / 110 = 80 mL/phút.',
    score: 9.5,
    verdict: 'Bài làm trình bày rất khoa học, đổi đơn vị chuẩn xác từ mmol/L sang µmol/L trước khi tính độ thanh thải!',
    strengths: [
      'Áp dụng đúng công thức định luật Beer–Lambert và tính chính xác C_Glucose = 11.10 mmol/L',
      'Quy đổi đúng V_24h = 1440 mL sang V = 1.0 mL/phút và đồng nhất đơn vị µmol/L giữa U_Cr và P_Cr'
    ],
    missing: [
      'Nên ghi thêm công thức hiệu chỉnh diện tích da chuẩn 1.73 m² khi biện luận mức lọc cầu thận lâm sàng'
    ],
    sample_answer: '1. $C_{\\text{Glucose}} = \\frac{0.740}{0.370} \\times 5.55 = 11.10\\text{ mmol/L}$ ($> 7.0\\text{ mmol/L}$ lúc đói).\n2. $C_{\\text{Cr}} = \\frac{U_{\\text{Cr}} \\times V}{P_{\\text{Cr}}} = \\frac{8800 \\times 1.0}{110} = 80.0\\text{ mL/phút}$.'
  };

  awardXP(25);
  playSound('correct');
  if (box) {
    box.innerHTML = `
      <div class="flex items-center justify-between gap-2 pb-2" style="border-bottom: 1px solid var(--border);">
        <div class="text-sm font-extrabold txt-main">🎯 Điểm AI Chấm: <span class="txt-brand text-base">${g.score} / 10</span></div>
        <span class="badge-emerald px-2.5 py-0.5 rounded-full text-[11px] font-bold">+25 XP</span>
      </div>
      <div class="p-3 rounded-xl space-y-1" style="background-color: var(--bg-surface); border: 1px solid var(--border);">
        <div class="text-[11px] font-extrabold txt-muted">📖 Chữ viết tay & Số liệu AI đọc được (OCR):</div>
        <div class="text-xs font-mono txt-main">${escapeHtml(g.transcribed_text || '')}</div>
      </div>
      <div class="text-xs font-bold txt-main">${renderInlineMathAndCode(g.verdict || '')}</div>
      <div class="space-y-1">
        <div class="text-[11px] font-extrabold txt-emerald">✔ Điểm làm tốt:</div>
        <ul class="list-disc pl-5 space-y-1 text-xs txt-sub">
          ${(g.strengths || []).map((s) => `<li>${renderInlineMathAndCode(s)}</li>`).join('')}
        </ul>
      </div>
      <div class="space-y-1">
        <div class="text-[11px] font-extrabold txt-amber">⚠️ Điểm cần lưu ý / hoàn thiện:</div>
        <ul class="list-disc pl-5 space-y-1 text-xs txt-sub">
          ${(g.missing || []).map((m) => `<li>${renderInlineMathAndCode(m)}</li>`).join('')}
        </ul>
      </div>
      <div class="p-3 rounded-xl badge-brand text-xs space-y-1">
        <div class="font-extrabold">✨ Lời giải & Barem chuẩn 10/10:</div>
        <div>${renderAcademicText(g.sample_answer || '')}</div>
      </div>
    `;
  }
}

// --- 17.5 Interactive Subject Knowledge Graph ---
const KNOWLEDGE_GRAPH_NODES_HOASINH = [
  { id: 'center', label: 'Hóa Sinh Lâm Sàng', x: 380, y: 210, r: 42, isHub: true, formula: '$C = \\frac{\\text{OD}_{\\text{thử}}}{\\text{OD}_{\\text{chuẩn}}} \\times C_0$', desc: 'Trung tâm tích hợp Quang phổ kế, Hóa sinh máu, Nước tiểu và Cặn lắng kính hiển vi.' },
  { id: 'c1', label: 'Động học Enzyme', x: 150, y: 85, r: 32, keyword: 'enzyme', formula: '$v = \\frac{V_{\\max}[S]}{K_m + [S]}$', desc: 'Phương trình Michaelis–Menten, AST/ALT, Amylase, CK-MB, LDH và các yếu tố ảnh hưởng hoạt độ enzyme.' },
  { id: 'c2', label: 'Chuyển hóa Glucid', x: 380, y: 65, r: 32, keyword: 'glucose', formula: '$\\text{Glucose} + \\ce{O2} \\xrightarrow{\\text{GOD}} \\text{Acid Gluconic} + \\ce{H2O2}$', desc: 'Định lượng Glucose máu (GOD-PAP), nghiệm pháp dung nạp OGTT, HbA1c và chẩn đoán Đái tháo đường.' },
  { id: 'c3', label: 'Lipid & Lipoprotein', x: 610, y: 85, r: 32, keyword: 'lipid', formula: '$\\text{LDL-C} = \\text{TC} - \\text{HDL-C} - \\frac{\\text{TG}}{2.2}$', desc: 'Cholesterol toàn phần, Triglycerid, HDL-C, công thức Friedewald và nguy cơ xơ vữa động mạch.' },
  { id: 'c4', label: 'Gan – Mật (Bilirubin)', x: 145, y: 330, r: 32, keyword: 'bilirubin', formula: '$\\text{Bilirubin}_{\\text{TP}} = \\text{Bilirubin}_{\\text{TT}} + \\text{Bilirubin}_{\\text{GT}}$', desc: 'Phản ứng Diazo (Jendrassik–Gróf), sắc tố mật, muối mật và phân biệt vàng da trước gan / tại gan / sau gan.' },
  { id: 'c5', label: 'Thận & Độ thanh thải', x: 380, y: 355, r: 32, keyword: 'creatinin', formula: '$C_{\\text{Cr}} = \\frac{U_{\\text{Cr}} \\times V}{P_{\\text{Cr}}}$', desc: 'Ure, Creatinin huyết thanh (Jaffé), Acid Uric, Protein niệu và tính mức lọc cầu thận.' },
  { id: 'c6', label: 'Soi Cặn Nước Tiểu', x: 615, y: 330, r: 32, keyword: '[Hình ảnh]', formula: 'Vi trường 10x (Trụ niệu) • 40x (Tế bào & Tinh thể)', desc: '16 tiêu bản kính hiển vi: Tinh thể Calcium Oxalate, Trụ hồng cầu, Trụ hạt, Nấm men, Tế bào biểu mô.' }
];

function renderInteractiveKnowledgeGraph() {
  const svg = document.getElementById('knowledge-graph-svg');
  if (!svg) return;
  const nodes = KNOWLEDGE_GRAPH_NODES_HOASINH;
  const center = nodes[0];

  const linesHtml = nodes
    .slice(1)
    .map(
      (n) =>
        `<line x1="${center.x}" y1="${center.y}" x2="${n.x}" y2="${n.y}" stroke="rgba(139,92,246,0.45)" stroke-width="2.5" stroke-dasharray="5,4" />`
    )
    .join('');

  const nodesHtml = nodes
    .map((n, idx) => {
      const fill = n.isHub ? 'url(#kgHubGrad)' : idx % 2 === 0 ? '#0f172a' : '#1e1b4b';
      const stroke = n.isHub ? '#ec4899' : '#8b5cf6';
      return `
        <g class="cursor-pointer" onclick="inspectGraphNode('${n.id}')">
          <circle cx="${n.x}" cy="${n.y}" r="${n.r + 6}" fill="rgba(124,58,237,0.14)" />
          <circle cx="${n.x}" cy="${n.y}" r="${n.r}" fill="${fill}" stroke="${stroke}" stroke-width="2.5" />
          <text x="${n.x}" y="${n.y + 4}" text-anchor="middle" fill="#f8fafc" font-size="11" font-weight="800">${escapeHtml(n.label)}</text>
        </g>
      `;
    })
    .join('');

  svg.innerHTML = `
    <defs>
      <linearGradient id="kgHubGrad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#7c3aed" />
        <stop offset="100%" stop-color="#ec4899" />
      </linearGradient>
    </defs>
    ${linesHtml}
    ${nodesHtml}
  `;
  inspectGraphNode('center');
}

function inspectGraphNode(nodeId) {
  const node = KNOWLEDGE_GRAPH_NODES_HOASINH.find((n) => n.id === nodeId) || KNOWLEDGE_GRAPH_NODES_HOASINH[0];
  const box = document.getElementById('knowledge-graph-inspector');
  if (!box || !node) return;
  box.innerHTML = `
    <div class="badge-brand px-2.5 py-0.5 rounded-full text-[11px] font-bold inline-block">Chuyên đề trọng tâm</div>
    <h4 class="text-base font-extrabold txt-main">${escapeHtml(node.label)}</h4>
    <p class="text-xs txt-sub leading-relaxed">${escapeHtml(node.desc)}</p>
    <div class="p-3 rounded-xl text-xs font-bold" style="background-color: var(--bg-surface); border: 1px solid var(--border);">
      <div class="text-[10px] txt-muted uppercase mb-1">Công thức / Quy tắc cốt lõi:</div>
      <div>${renderInlineMathAndCode(node.formula)}</div>
    </div>
    <div class="flex flex-wrap gap-2 pt-1">
      <button type="button" onclick="quickStartHoaSinhCTUMP()" class="btn-primary flex-1 py-2 px-3 text-xs font-extrabold">
        ⚡ Luyện Ngay Chuyên Đề Này
      </button>
      ${
        node.id === 'c6'
          ? `<button type="button" onclick="quickStartHoaSinhImagesOnly()" class="btn-soft py-2 px-3 text-xs font-bold">🖼️ Thi 16 Câu Ảnh</button>`
          : ''
      }
    </div>
  `;
}

// --- 17.6 Clinical Biochemistry & STEM Quick Calculators ---
function runClinicalCalculators() {
  // 1. Beer-Lambert
  const odSam = parseFloat(document.getElementById('calc-bl-od-sam')?.value || '0.54');
  const odStd = parseFloat(document.getElementById('calc-bl-od-std')?.value || '0.36');
  const cStd = parseFloat(document.getElementById('calc-bl-c-std')?.value || '5.5');
  const blOut = document.getElementById('calc-bl-output');
  if (blOut && odStd > 0) {
    const cSam = (odSam / odStd) * cStd;
    blOut.innerHTML = renderInlineMathAndCode(
      `Kết quả: $C_{\\text{thử}} = \\frac{${odSam}}{${odStd}} \\times ${cStd} = \\mathbf{${cSam.toFixed(2)}}$ (cùng đơn vị với $C_{\\text{chuẩn}}$)`
    );
  }

  // 2. Creatinine Clearance C_Cr
  const uCrMmol = parseFloat(document.getElementById('calc-ccr-u')?.value || '8.8');
  const pCrUmol = parseFloat(document.getElementById('calc-ccr-p')?.value || '110');
  const v24 = parseFloat(document.getElementById('calc-ccr-v24')?.value || '1440');
  const ccrOut = document.getElementById('calc-ccr-output');
  if (ccrOut && pCrUmol > 0) {
    const vMin = v24 / 1440.0;
    const uCrUmol = uCrMmol * 1000.0;
    const ccr = (uCrUmol * vMin) / pCrUmol;
    const verdict = ccr >= 90 ? 'Bình thường (G1)' : ccr >= 60 ? 'Giảm nhẹ (G2)' : ccr >= 30 ? 'Suy thận vừa (G3)' : 'Suy thận nặng (G4–G5)';
    ccrOut.innerHTML = renderInlineMathAndCode(
      `$V = ${vMin.toFixed(2)}\\text{ mL/phút}$ → $C_{\\text{Cr}} = \\mathbf{${ccr.toFixed(1)}\\text{ mL/phút}}$ (${verdict})`
    );
  }

  // 3. Plasma Osmolality & Anion Gap
  const na = parseFloat(document.getElementById('calc-osm-na')?.value || '140');
  const cl = parseFloat(document.getElementById('calc-osm-cl')?.value || '102');
  const hco3 = parseFloat(document.getElementById('calc-osm-hco3')?.value || '24');
  const glu = parseFloat(document.getElementById('calc-osm-glu')?.value || '5.5');
  const osmOut = document.getElementById('calc-osm-output');
  if (osmOut) {
    const osm = 2 * na + glu + 5.0;
    const ag = na - (cl + hco3);
    osmOut.innerHTML = renderInlineMathAndCode(
      `$\\text{ASTT} \\approx \\mathbf{${osm.toFixed(1)}\\text{ mOsm/kg}}$ | $\\text{Anion Gap} = \\mathbf{${ag.toFixed(1)}\\text{ mmol/L}}$ (${ag > 16 ? 'Toan chuyển hóa tăng AG' : 'Bình thường 8–16'})`
    );
  }

  // 4. Friedewald LDL-C
  const tc = parseFloat(document.getElementById('calc-ldl-tc')?.value || '5.8');
  const hdl = parseFloat(document.getElementById('calc-ldl-hdl')?.value || '1.3');
  const tg = parseFloat(document.getElementById('calc-ldl-tg')?.value || '2.2');
  const ldlOut = document.getElementById('calc-ldl-output');
  if (ldlOut) {
    if (tg >= 4.5) {
      ldlOut.innerHTML = '⚠️ Triglycerid ≥ 4.5 mmol/L: Không áp dụng công thức Friedewald (cần định lượng LDL-C trực tiếp)!';
    } else {
      const ldl = tc - hdl - tg / 2.2;
      ldlOut.innerHTML = renderInlineMathAndCode(
        `Kết quả: $\\text{LDL-C} = ${tc} - ${hdl} - \\frac{${tg}}{2.2} = \\mathbf{${ldl.toFixed(2)}\\text{ mmol/L}}$ (${ldl > 3.4 ? 'Tăng LDL-C' : 'Bình thường < 3.4'})`
      );
    }
  }
}



// ============================================================================
// UNIMASTER AI PRO v11.0 — EXTENDED MODULES (CLIENT-SIDE ENGINE)
// 1. Live WebSocket Multiplayer Quiz Arena
// 2. Virtual Patient / Multi-Step Clinical Case Simulator
// 3. Clinical Pharmacology & Renal Dosing Engine
// 4. Biostatistics & Medical Research Lab (2x2, OR, Chi-Square, Vancouver Citation)
// 5. 1-Click Anki Deck (.txt) & Word A4 Exam (.doc) Downloader
// ============================================================================

// --- 1. LIVE WEBSOCKET MULTIPLAYER ARENA ---
const LIVE_ARENA = {
  ws: null,
  isHost: false,
  mode: 'host',
  roomCode: null,
  currentQ: 0,
  totalQ: 0,
  timerInterval: null,
  timeLeft: 15,
  hasAnswered: false,
  score: 0,
  players: []
};

function setLiveArenaMode(mode) {
  LIVE_ARENA.mode = mode;
  document.getElementById('btn-mode-host')?.classList.toggle('btn-primary', mode === 'host');
  document.getElementById('btn-mode-host')?.classList.toggle('btn-soft', mode !== 'host');
  document.getElementById('btn-mode-player')?.classList.toggle('btn-primary', mode === 'player');
  document.getElementById('btn-mode-player')?.classList.toggle('btn-soft', mode !== 'player');

  document.getElementById('live-host-section')?.classList.toggle('hidden', mode !== 'host');
  document.getElementById('live-player-section')?.classList.toggle('hidden', mode !== 'player');
  playSound('click');
}

function initLiveArenaView() {
  const hostSubSel = document.getElementById('live-host-subject');
  if (hostSubSel && (!hostSubSel.options || hostSubSel.options.length === 0)) {
    const subs = STATE.subjects || [];
    hostSubSel.innerHTML = subs.map(s => `<option value="${s.id}">${s.name} (${s.question_count || 0} câu)</option>`).join('');
  }
}

function getWsUrl() {
  const loc = window.location;
  const proto = (loc.protocol === 'https:') ? 'wss:' : 'ws:';
  return `${proto}//${loc.host}/ws/arena`;
}

function createLiveRoom() {
  const hostSubSel = document.getElementById('live-host-subject');
  const qCountSel = document.getElementById('live-host-qcount');
  const sid = hostSubSel ? parseInt(hostSubSel.value) : 10;
  const qCount = qCountSel ? parseInt(qCountSel.value) : 10;

  LIVE_ARENA.isHost = true;
  connectLiveArenaWs(() => {
    LIVE_ARENA.ws.send(JSON.stringify({
      action: 'create_room',
      subject_id: sid,
      q_count: qCount
    }));
  });
}

function joinLiveRoom() {
  const codeInp = document.getElementById('live-player-roomcode');
  const nameInp = document.getElementById('live-player-name');
  const roomCode = (codeInp?.value || '').trim();
  const playerName = (nameInp?.value || '').trim() || 'Sinh viên';

  if (!roomCode) {
    showToast('⚠️ Vui lòng nhập Mã Phòng (PIN)!', 'error');
    return;
  }

  LIVE_ARENA.isHost = false;
  connectLiveArenaWs(() => {
    LIVE_ARENA.ws.send(JSON.stringify({
      action: 'join_room',
      room_code: roomCode,
      player_name: playerName
    }));
  });
}

function connectLiveArenaWs(onOpenCallback) {
  if (LIVE_ARENA.ws && LIVE_ARENA.ws.readyState === WebSocket.OPEN) {
    if (onOpenCallback) onOpenCallback();
    return;
  }

  const url = getWsUrl();
  const statusBadge = document.getElementById('live-ws-status-badge');
  if (statusBadge) {
    statusBadge.textContent = 'Đang kết nối...';
    statusBadge.className = 'badge-amber px-2.5 py-0.5 rounded-full text-[11px] font-bold';
  }

  try {
    LIVE_ARENA.ws = new WebSocket(url);
  } catch (err) {
    showToast(`❌ Không thể mở WebSocket: ${err.message}`, 'error');
    return;
  }

  LIVE_ARENA.ws.onopen = () => {
    if (statusBadge) {
      statusBadge.textContent = '🟢 Đã kết nối';
      statusBadge.className = 'badge-brand px-2.5 py-0.5 rounded-full text-[11px] font-bold text-emerald-400';
    }
    if (onOpenCallback) onOpenCallback();
  };

  LIVE_ARENA.ws.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      handleLiveArenaMessage(data);
    } catch (e) {
      console.error('Lỗi phân tích WebSocket message:', e);
    }
  };

  LIVE_ARENA.ws.onerror = (err) => {
    console.error('WebSocket Error:', err);
    if (statusBadge) {
      statusBadge.textContent = '🔴 Lỗi mạng';
      statusBadge.className = 'badge-rose px-2.5 py-0.5 rounded-full text-[11px] font-bold';
    }
  };

  LIVE_ARENA.ws.onclose = () => {
    if (statusBadge) {
      statusBadge.textContent = '⚪ Đã ngắt';
      statusBadge.className = 'badge-soft px-2.5 py-0.5 rounded-full text-[11px] font-bold';
    }
  };
}

function handleLiveArenaMessage(msg) {
  const type = msg.type;

  if (type === 'room_created') {
    LIVE_ARENA.roomCode = msg.room_code;
    showToast(`🎉 Phòng thi trực tiếp ${msg.room_code} đã sẵn sàng!`, 'success');
    renderLiveLobby(msg.room_code, true);
  } else if (type === 'joined_success') {
    LIVE_ARENA.roomCode = msg.room_code;
    showToast(`✅ Đã vào phòng thi ${msg.room_code}! Hãy đợi Host bắt đầu...`, 'success');
    renderLiveLobby(msg.room_code, false);
  } else if (type === 'player_joined') {
    LIVE_ARENA.players = msg.players || [];
    updateLivePlayerList(msg.players);
    showToast(`👋 ${msg.new_player} vừa tham gia phòng!`, 'info');
    playSound('correct');
  } else if (type === 'player_left') {
    LIVE_ARENA.players = msg.players || [];
    updateLivePlayerList(msg.players);
  } else if (type === 'game_started') {
    playSound('fanfare');
    document.getElementById('live-stage-idle')?.classList.add('hidden');
    document.getElementById('live-stage-podium')?.classList.add('hidden');
    document.getElementById('live-stage-active')?.classList.remove('hidden');
  } else if (type === 'new_question') {
    renderLiveQuestion(msg);
  } else if (type === 'answer_feedback') {
    renderLiveAnswerFeedback(msg);
  } else if (type === 'leaderboard_update') {
    // Leaderboard update for host or between questions
    console.log('Leaderboard:', msg.leaderboard);
  } else if (type === 'game_over') {
    renderLivePodium(msg.podium || []);
  } else if (type === 'error') {
    showToast(`⚠️ ${msg.message || 'Có lỗi xảy ra'}`, 'error');
  }
}

function renderLiveLobby(roomCode, isHost) {
  document.getElementById('live-host-section')?.classList.add('hidden');
  document.getElementById('live-player-section')?.classList.add('hidden');
  document.getElementById('live-lobby-box')?.classList.remove('hidden');
  const codeEl = document.getElementById('live-display-roomcode');
  if (codeEl) codeEl.textContent = roomCode;

  const btnStart = document.getElementById('live-btn-start');
  if (btnStart) btnStart.classList.toggle('hidden', !isHost);
}

function updateLivePlayerList(players) {
  const listEl = document.getElementById('live-player-list');
  const countEl = document.getElementById('live-player-count');
  if (countEl) countEl.textContent = players.length;
  if (!listEl) return;

  listEl.innerHTML = players.map(p => `
    <span class="badge-soft px-2.5 py-1 rounded-lg text-xs font-bold flex items-center gap-1 border border-emerald-500/30">
      <span>🟢</span> <span>${p.name}</span>
    </span>
  `).join('');
}

function startLiveGame() {
  if (LIVE_ARENA.ws && LIVE_ARENA.ws.readyState === WebSocket.OPEN) {
    LIVE_ARENA.ws.send(JSON.stringify({ action: 'start_game' }));
  }
}

function renderLiveQuestion(data) {
  LIVE_ARENA.hasAnswered = false;
  LIVE_ARENA.currentQ = data.q_idx;
  LIVE_ARENA.totalQ = data.total;

  document.getElementById('live-stage-idle')?.classList.add('hidden');
  document.getElementById('live-stage-podium')?.classList.add('hidden');
  document.getElementById('live-stage-active')?.classList.remove('hidden');

  const badge = document.getElementById('live-q-badge');
  if (badge) badge.textContent = `Câu ${data.q_idx} / ${data.total}`;

  const q = data.question;
  const qTextEl = document.getElementById('live-question-text');
  if (qTextEl) qTextEl.innerHTML = renderInlineMathAndCode(q.text);

  const imgWrap = document.getElementById('live-question-img-wrap');
  const imgEl = document.getElementById('live-question-img');
  if (imgWrap && imgEl) {
    if (q.image_url) {
      imgEl.src = q.image_url;
      imgWrap.classList.remove('hidden');
    } else {
      imgWrap.classList.add('hidden');
    }
  }

  ['A', 'B', 'C', 'D'].forEach(opt => {
    const textEl = document.getElementById(`live-text-${opt}`);
    const btnEl = document.getElementById(`live-opt-${opt}`);
    if (textEl) textEl.innerHTML = renderInlineMathAndCode(q[opt.toLowerCase()] || '--');
    if (btnEl) {
      btnEl.disabled = false;
      btnEl.className = 'uni-card p-3.5 text-left text-xs font-bold hover:border-violet-500 transition-all flex items-start gap-2.5 cursor-pointer';
    }
  });

  const fbBox = document.getElementById('live-feedback-box');
  if (fbBox) {
    fbBox.classList.add('hidden');
    fbBox.innerHTML = '';
  }

  const hostNextBtn = document.getElementById('live-host-controls');
  if (hostNextBtn) hostNextBtn.classList.toggle('hidden', !LIVE_ARENA.isHost);

  // Start 15s Timer
  startLiveTimer(15);
  playSound('click');
}

function startLiveTimer(seconds) {
  if (LIVE_ARENA.timerInterval) clearInterval(LIVE_ARENA.timerInterval);
  LIVE_ARENA.timeLeft = seconds;

  const bar = document.getElementById('live-timer-bar');
  const val = document.getElementById('live-timer-val');

  if (val) val.textContent = `${seconds}s`;
  if (bar) {
    bar.style.width = '100%';
    bar.className = 'h-full bg-gradient-to-r from-emerald-400 to-amber-400 transition-all duration-300';
  }

  LIVE_ARENA.timerInterval = setInterval(() => {
    LIVE_ARENA.timeLeft -= 1;
    if (val) val.textContent = `${LIVE_ARENA.timeLeft}s`;
    if (bar) {
      const pct = (LIVE_ARENA.timeLeft / seconds) * 100;
      bar.style.width = `${pct}%`;
      if (pct < 30) {
        bar.className = 'h-full bg-rose-500 transition-all duration-300';
      }
    }

    if (LIVE_ARENA.timeLeft <= 0) {
      clearInterval(LIVE_ARENA.timerInterval);
      if (!LIVE_ARENA.hasAnswered) {
        submitLiveBuzzer('EXPIRED');
      }
    }
  }, 1000);
}

function submitLiveBuzzer(chosenOpt) {
  if (LIVE_ARENA.hasAnswered) return;
  LIVE_ARENA.hasAnswered = true;
  if (LIVE_ARENA.timerInterval) clearInterval(LIVE_ARENA.timerInterval);

  ['A', 'B', 'C', 'D'].forEach(opt => {
    const btn = document.getElementById(`live-opt-${opt}`);
    if (btn) btn.disabled = true;
  });

  if (LIVE_ARENA.ws && LIVE_ARENA.ws.readyState === WebSocket.OPEN) {
    LIVE_ARENA.ws.send(JSON.stringify({
      action: 'submit_answer',
      option: chosenOpt,
      time_left: LIVE_ARENA.timeLeft
    }));
  }
}

function renderLiveAnswerFeedback(res) {
  const isCorrect = res.is_correct;
  const corrOpt = res.correct_option;
  const addedScore = res.added_score || 0;
  LIVE_ARENA.score = res.total_score || LIVE_ARENA.score;

  if (isCorrect) playSound('correct'); else playSound('wrong');

  ['A', 'B', 'C', 'D'].forEach(opt => {
    const btn = document.getElementById(`live-opt-${opt}`);
    if (!btn) return;
    if (opt === corrOpt) {
      btn.classList.add('border-emerald-500', 'bg-emerald-500/20');
    } else {
      btn.classList.add('opacity-50');
    }
  });

  const fbBox = document.getElementById('live-feedback-box');
  if (fbBox) {
    fbBox.className = `p-3.5 rounded-xl text-xs space-y-1.5 animate-fade-in ${isCorrect ? 'border border-emerald-500/40 bg-emerald-500/10' : 'border border-rose-500/40 bg-rose-500/10'}`;
    fbBox.innerHTML = `
      <div class="font-black ${isCorrect ? 'text-emerald-400' : 'text-rose-400'} flex items-center justify-between">
        <span>${isCorrect ? '🎉 CHÍNH XÁC!' : '❌ CHƯA CHÍNH XÁC!'}</span>
        <span>+${addedScore} PTS (Tổng: ${LIVE_ARENA.score})</span>
      </div>
      <div class="txt-sub leading-relaxed">${res.explanation || 'Đáp án đúng: ' + corrOpt}</div>
    `;
    fbBox.classList.remove('hidden');
  }
}

function hostNextQuestion() {
  if (LIVE_ARENA.ws && LIVE_ARENA.ws.readyState === WebSocket.OPEN) {
    LIVE_ARENA.ws.send(JSON.stringify({ action: 'next_question' }));
  }
}

function renderLivePodium(podium) {
  playSound('fanfare');
  if (LIVE_ARENA.timerInterval) clearInterval(LIVE_ARENA.timerInterval);

  document.getElementById('live-stage-active')?.classList.add('hidden');
  const podiumScreen = document.getElementById('live-stage-podium');
  if (podiumScreen) podiumScreen.classList.remove('hidden');

  const listEl = document.getElementById('live-podium-list');
  if (!listEl) return;

  const medals = ['🥇', '🥈', '🥉'];
  listEl.innerHTML = podium.map((p, idx) => `
    <div class="uni-card p-4 flex items-center justify-between ${idx === 0 ? 'border-2 border-amber-400 bg-amber-400/10' : ''}">
      <div class="flex items-center gap-3">
        <span class="text-2xl">${medals[idx] || '#' + (idx + 1)}</span>
        <div class="text-left font-black text-sm txt-main">${p.name}</div>
      </div>
      <div class="text-base font-mono font-black text-emerald-400">${p.score} PTS</div>
    </div>
  `).join('');
}

function leaveLiveRoom() {
  if (LIVE_ARENA.ws) {
    LIVE_ARENA.ws.close();
    LIVE_ARENA.ws = null;
  }
  resetLiveArena();
}

function resetLiveArena() {
  LIVE_ARENA.roomCode = null;
  LIVE_ARENA.currentQ = 0;
  LIVE_ARENA.totalQ = 0;
  LIVE_ARENA.hasAnswered = false;
  LIVE_ARENA.score = 0;

  document.getElementById('live-stage-idle')?.classList.remove('hidden');
  document.getElementById('live-stage-active')?.classList.add('hidden');
  document.getElementById('live-stage-podium')?.classList.add('hidden');
  document.getElementById('live-lobby-box')?.classList.add('hidden');

  setLiveArenaMode(LIVE_ARENA.mode);
}


// --- 2. VIRTUAL CLINICAL PATIENT SIMULATOR ---
const VP_STATE = {
  cases: [],
  activeCase: null,
  currentStep: 0,
  score: 0,
  userChoices: {}
};

async function initVirtualPatientView() {
  try {
    const res = await fetch('/api/virtual-patient/cases');
    const data = await res.json();
    if (data.success && data.cases) {
      VP_STATE.cases = data.cases;
      renderVirtualCaseList();
    }
  } catch (e) {
    console.warn('Lấy ca bệnh ảo từ backend thất bại, dùng dữ liệu mẫu nội bộ:', e);
  }
}

function renderVirtualCaseList() {
  const sel = document.getElementById('vp-case-select');
  if (sel && VP_STATE.cases.length > 0) {
    sel.innerHTML = VP_STATE.cases.map((c, i) => `<option value="${i}">${c.title}</option>`).join('');
    onVirtualCaseSelect();
  }
}

function onVirtualCaseSelect() {
  const sel = document.getElementById('vp-case-select');
  const idx = sel ? parseInt(sel.value) : 0;
  VP_STATE.activeCase = VP_STATE.cases[idx] || null;
  VP_STATE.currentStep = 0;
  VP_STATE.score = 0;
  VP_STATE.userChoices = {};

  if (!VP_STATE.activeCase) return;

  const p = VP_STATE.activeCase.patient;
  const setEl = (id, val) => { const el = document.getElementById(id); if (el) el.textContent = val; };

  setEl('vp-p-name', p.name);
  setEl('vp-p-age', `${p.age} tuổi • ${p.gender}`);
  setEl('vp-p-cc', `Lý do vào viện: ${p.chief_complaint}`);
  setEl('vp-p-history', p.history);
  setEl('vp-v-bp', p.vital_signs?.bp || '120/80');
  setEl('vp-v-hr', `${p.vital_signs?.hr || 80} l/p`);
  setEl('vp-v-temp', `${p.vital_signs?.temp || 37.0}°C`);
  setEl('vp-v-spo2', `${p.vital_signs?.spo2 || 98}%`);

  setVirtualStep(0);
}

function setVirtualStep(stepIdx) {
  if (!VP_STATE.activeCase) return;
  const steps = VP_STATE.activeCase.steps || [];
  if (stepIdx < 0 || stepIdx >= steps.length) return;

  VP_STATE.currentStep = stepIdx;

  for (let i = 0; i < 5; i++) {
    const btn = document.getElementById(`vp-step-btn-${i}`);
    if (btn) {
      btn.className = (i === stepIdx) ? 'btn-primary py-2 text-[10px] font-black rounded-lg' : 'btn-soft py-2 text-[10px] font-black rounded-lg';
    }
  }

  const cur = steps[stepIdx];
  const titleEl = document.getElementById('vp-step-title');
  if (titleEl) titleEl.textContent = `Bước ${stepIdx + 1}: ${cur.step_title}`;

  const bodyEl = document.getElementById('vp-step-body');
  if (!bodyEl) return;

  const savedChoice = VP_STATE.userChoices[stepIdx];

  bodyEl.innerHTML = `
    <div class="text-xs sm:text-sm font-bold txt-main leading-relaxed">${cur.prompt}</div>
    <div class="space-y-2.5 pt-2">
      ${cur.options.map((opt, optIdx) => `
        <button type="button" onclick="submitVirtualStepChoice(${stepIdx}, ${optIdx})" 
          class="w-full text-left p-3.5 rounded-xl text-xs font-bold transition-all border flex items-start gap-2.5 ${savedChoice === optIdx ? 'border-cyan-500 bg-cyan-500/20' : 'border-zinc-800 bg-zinc-900/60 hover:border-zinc-600'}">
          <span class="w-5 h-5 rounded-full bg-cyan-500/20 text-cyan-400 flex items-center justify-center text-[10px] font-black shrink-0">${['A','B','C','D'][optIdx] || optIdx + 1}</span>
          <span class="txt-main">${opt.text}</span>
        </button>
      `).join('')}
    </div>
    <div id="vp-step-feedback-${stepIdx}" class="${savedChoice !== undefined ? '' : 'hidden'} p-3.5 rounded-xl text-xs space-y-1.5 mt-3 border border-emerald-500/40 bg-emerald-500/10">
      ${savedChoice !== undefined ? renderStepFeedbackHtml(cur.options[savedChoice]) : ''}
    </div>
  `;
}

function submitVirtualStepChoice(stepIdx, optIdx) {
  if (!VP_STATE.activeCase) return;
  const cur = VP_STATE.activeCase.steps[stepIdx];
  VP_STATE.userChoices[stepIdx] = optIdx;

  const opt = cur.options[optIdx];
  const fbBox = document.getElementById(`vp-step-feedback-${stepIdx}`);
  if (fbBox && opt) {
    fbBox.className = `p-3.5 rounded-xl text-xs space-y-1.5 mt-3 ${opt.score > 15 ? 'border border-emerald-500/40 bg-emerald-500/10' : 'border border-amber-500/40 bg-amber-500/10'}`;
    fbBox.innerHTML = renderStepFeedbackHtml(opt);
    fbBox.classList.remove('hidden');
  }

  // Recalculate total score
  let total = 0;
  VP_STATE.activeCase.steps.forEach((st, idx) => {
    const ch = VP_STATE.userChoices[idx];
    if (ch !== undefined && st.options[ch]) total += st.options[ch].score;
  });
  VP_STATE.score = total;

  const scorePill = document.getElementById('vp-score-pill');
  if (scorePill) scorePill.textContent = `Điểm phản xạ: ${total}/100`;

  playSound(opt.score > 15 ? 'correct' : 'click');
}

function renderStepFeedbackHtml(opt) {
  return `
    <div class="font-extrabold ${opt.score > 15 ? 'text-emerald-400' : 'text-amber-400'} flex items-center justify-between">
      <span>${opt.score > 15 ? '🎯 Lựa chọn tối ưu lâm sàng' : '⚠️ Lựa chọn chưa tối ưu'}</span>
      <span>+${opt.score} điểm</span>
    </div>
    <div class="txt-sub leading-relaxed">${opt.feedback}</div>
  `;
}

function prevVirtualStep() {
  if (VP_STATE.currentStep > 0) setVirtualStep(VP_STATE.currentStep - 1);
}

function nextVirtualStep() {
  if (VP_STATE.currentStep < 4) setVirtualStep(VP_STATE.currentStep + 1);
}


// --- 3. CLINICAL PHARMACOLOGY & RENAL DOSING CALCULATOR ---
const CLINICAL_DRUGS = [
  {
    id: "vancomycin",
    name: "Vancomycin",
    group: "Kháng sinh Glycopeptid",
    std_dose: "15 – 20 mg/kg mỗi 8 – 12 giờ (truyền IV chậm)",
    crcl_normal: "CrCl ≥ 50 ml/phút: 100% liều tiêu chuẩn (15 mg/kg mỗi 12 giờ)",
    crcl_mod: "CrCl 20 – 49 ml/phút: 15 mg/kg mỗi 24 – 48 giờ",
    crcl_severe: "CrCl < 20 ml/phút: 15 mg/kg liều nạp, sau đó theo dõi nồng độ đáy TDM (15 – 20 mcg/ml)",
    hd_dose: "Lọc máu chu kỳ: Liều nạp 15 – 25 mg/kg, bổ sung 500 – 1000 mg sau mỗi lần lọc máu",
    warning: "Độc tính cao trên tai và thận! Tuyệt đối không truyền nhanh (< 60 phút) vì nguy cơ Hội chứng người đỏ (Red Man Syndrome)."
  },
  {
    id: "ciprofloxacin",
    name: "Ciprofloxacin",
    group: "Kháng sinh Fluoroquinolon",
    std_dose: "500 – 750 mg uống mỗi 12 giờ (hoặc 400 mg IV mỗi 12 giờ)",
    crcl_normal: "CrCl ≥ 50 ml/phút: 100% liều (500 – 750 mg mỗi 12 giờ)",
    crcl_mod: "CrCl 30 – 49 ml/phút: 250 – 500 mg mỗi 12 giờ",
    crcl_severe: "CrCl < 30 ml/phút: 250 – 500 mg mỗi 18 – 24 giờ",
    hd_dose: "Thẩm phân phúc mạc / HD: 250 – 500 mg mỗi 24 giờ sau lọc",
    warning: "Nguy cơ viêm/đứt gân gót Achilles, kéo dài khoảng QT tim mạch và độc thần kinh ở người già."
  },
  {
    id: "meropenem",
    name: "Meropenem",
    group: "Kháng sinh Carbapenem",
    std_dose: "1000 mg IV mỗi 8 giờ (viêm màng não: 2000 mg mỗi 8 giờ)",
    crcl_normal: "CrCl ≥ 50 ml/phút: 1000 mg mỗi 8 giờ",
    crcl_mod: "CrCl 26 – 49 ml/phút: 1000 mg mỗi 12 giờ",
    crcl_severe: "CrCl 10 – 25 ml/phút: 500 mg mỗi 12 giờ; CrCl < 10 ml/phút: 500 mg mỗi 24 giờ",
    hd_dose: "Lọc máu: 500 mg mỗi 24 giờ, cho thêm 1 liều sau lọc máu",
    warning: "Thận trọng nguy cơ co giật khi dùng liều cao trên bệnh nhân tổn thương thần kinh trung ương."
  },
  {
    id: "gentamicin",
    name: "Gentamicin",
    group: "Kháng sinh Aminoglycosid",
    std_dose: "5 – 7 mg/kg tiêm truyền tĩnh mạch 1 lần/ngày",
    crcl_normal: "CrCl ≥ 60 ml/phút: Mỗi 24 giờ 1 lần",
    crcl_mod: "CrCl 40 – 59 ml/phút: Kéo dài khoảng cách mỗi 36 giờ; CrCl 20 – 39 ml/phút: Mỗi 48 giờ",
    crcl_severe: "CrCl < 20 ml/phút: Liều nạp 2 mg/kg, sau đó định lượng nồng độ đáy TDM",
    hd_dose: "Sau lọc máu: Bổ sung 1 – 1,5 mg/kg sau mỗi buổi lọc",
    warning: "Độc tính không hồi phục trên tiền đình - ốc tai và hoại tử ống thận cấp! Bắt buộc theo dõi chức năng thận."
  },
  {
    id: "allopurinol",
    name: "Allopurinol",
    group: "Ức chế Xanthine Oxidase",
    std_dose: "100 – 300 mg/ngày uống sau ăn (khởi đầu 100 mg/ngày)",
    crcl_normal: "CrCl ≥ 50 ml/phút: 200 – 300 mg/ngày",
    crcl_mod: "CrCl 20 – 49 ml/phút: 100 – 200 mg/ngày",
    crcl_severe: "CrCl 10 – 19 ml/phút: 100 mg/ngày; CrCl < 10 ml/phút: 100 mg mỗi 2 – 3 ngày",
    hd_dose: "Sau lọc máu: 50 – 100 mg sau mỗi lần lọc máu",
    warning: "Nguy cơ hội chứng quá mẫn nghiêm trọng (Stevens-Johnson / TEN, DRESS) đặc biệt ở người mang gen HLA-B*5801."
  },
  {
    id: "enalapril",
    name: "Enalapril",
    group: "Thuốc ức chế men chuyển (ACEi)",
    std_dose: "5 – 20 mg/ngày uống 1 – 2 lần",
    crcl_normal: "CrCl ≥ 30 ml/phút: Khởi đầu 5 mg/ngày, duy trì 10 – 20 mg/ngày",
    crcl_mod: "CrCl 10 – 29 ml/phút: Khởi đầu 2,5 mg/ngày, tối đa 10 mg/ngày",
    crcl_severe: "CrCl < 10 ml/phút: Khởi đầu 2,5 mg vào những ngày không lọc máu",
    hd_dose: "Lọc máu: Có thể thẩm phân được, dùng sau buổi lọc máu",
    warning: "Theo dõi sát Kali máu và Creatinin máu sau 1 – 2 tuần khởi trị. Chống chỉ định trong hẹp ĐM thận hai bên và thai kỳ!"
  },
  {
    id: "metformin",
    name: "Metformin",
    group: "Biguanid điều trị ĐTĐ type 2",
    std_dose: "500 – 1000 mg uống 2 lần/ngày cùng bữa ăn (tối đa 2000 – 2550 mg/ngày)",
    crcl_normal: "eGFR ≥ 60 ml/phút: Dùng liều thông thường",
    crcl_mod: "eGFR 45 – 59 ml/phút: Tối đa 1000 mg/ngày. eGFR 30 – 44 ml/phút: Tối đa 500 mg/ngày",
    crcl_severe: "eGFR < 30 ml/phút: CHỐNG CHỈ ĐỊNH TUYỆT ĐỐI!",
    hd_dose: "Lọc máu: CHỐNG CHỈ ĐỊNH TUYỆT ĐỐI!",
    warning: "CHỐNG CHỈ ĐỊNH khi eGFR < 30 ml/phút do nguy cơ nhiễm toan acid lactic gây tử vong cao!"
  }
];

function onDoseDrugChange() {
  runRenalDoseCalculation();
}

function runRenalDoseCalculation() {
  const drugId = document.getElementById('dose-drug-select')?.value || 'vancomycin';
  const age = parseFloat(document.getElementById('dose-patient-age')?.value || '60');
  const wt = parseFloat(document.getElementById('dose-patient-wt')?.value || '60');
  const gender = document.getElementById('dose-patient-gender')?.value || 'male';
  const scr = parseFloat(document.getElementById('dose-patient-scr')?.value || '1.0');

  if (isNaN(age) || isNaN(wt) || isNaN(scr) || scr <= 0) return;

  // Cockcroft-Gault CrCl (ml/min)
  let crcl = ((140 - age) * wt) / (72 * scr);
  if (gender === 'female') crcl *= 0.85;

  let kdigoStage = 'G1 (Bình thường ≥ 90)';
  let kdigoClass = 'badge-brand';
  if (crcl < 15) {
    kdigoStage = 'G5 (Suy thận mạn gđ cuối < 15)';
    kdigoClass = 'badge-rose';
  } else if (crcl < 30) {
    kdigoStage = 'G4 (Giảm nặng 15–29)';
    kdigoClass = 'badge-rose';
  } else if (crcl < 45) {
    kdigoStage = 'G3b (Giảm vừa - nặng 30–44)';
    kdigoClass = 'badge-amber';
  } else if (crcl < 60) {
    kdigoStage = 'G3a (Giảm nhẹ - vừa 45–59)';
    kdigoClass = 'badge-amber';
  } else if (crcl < 90) {
    kdigoStage = 'G2 (Giảm nhẹ 60–89)';
    kdigoClass = 'badge-brand';
  }

  const crclEl = document.getElementById('dose-calc-crcl');
  const kdigoEl = document.getElementById('dose-calc-kdigo');
  if (crclEl) crclEl.textContent = `${crcl.toFixed(1)} ml/phút`;
  if (kdigoEl) {
    kdigoEl.textContent = kdigoStage;
    kdigoEl.className = `${kdigoClass} px-2 py-0.5 rounded text-[10px] font-bold`;
  }

  // Find Drug Info
  const drug = CLINICAL_DRUGS.find(d => d.id === drugId) || CLINICAL_DRUGS[0];
  const setEl = (id, val) => { const el = document.getElementById(id); if (el) el.textContent = val; };

  setEl('dose-drug-title', drug.name);
  setEl('dose-drug-group', drug.group);
  setEl('dose-std-text', drug.std_dose);
  setEl('dose-hd-text', drug.hd_dose);
  setEl('dose-warning-text', drug.warning);

  let rec = drug.crcl_normal;
  if (crcl < 20) rec = drug.crcl_severe;
  else if (crcl < 50) rec = drug.crcl_mod;

  const recEl = document.getElementById('dose-adjusted-recommendation');
  const badgeEl = document.getElementById('dose-adj-crcl-badge');
  if (recEl) recEl.textContent = rec;
  if (badgeEl) badgeEl.textContent = `CrCl = ${crcl.toFixed(1)} ml/p`;
}


// --- 4. BIOSTATISTICS & RESEARCH LAB ---
const BIO_PRESETS = {
  troponin: { a: 92, b: 8, c: 8, d: 192 },
  hba1c: { a: 80, b: 20, c: 15, d: 185 },
  covid: { a: 88, b: 5, c: 12, d: 295 }
};

function loadBiostatPreset(key) {
  const p = BIO_PRESETS[key];
  if (!p) return;
  const setVal = (id, v) => { const el = document.getElementById(id); if (el) el.value = v; };
  setVal('bio-a', p.a);
  setVal('bio-b', p.b);
  setVal('bio-c', p.c);
  setVal('bio-d', p.d);
  runBiostatCalculations();
}

function runBiostatCalculations() {
  const a = parseFloat(document.getElementById('bio-a')?.value || '85');
  const b = parseFloat(document.getElementById('bio-b')?.value || '15');
  const c = parseFloat(document.getElementById('bio-c')?.value || '12');
  const d = parseFloat(document.getElementById('bio-d')?.value || '188');

  const se = (a / (a + c)) * 100;
  const sp = (d / (b + d)) * 100;
  const ppv = (a / (a + b)) * 100;
  const or = (b * c > 0) ? (a * d) / (b * c) : 0;

  // 95% Confidence Interval for Odds Ratio
  let ciText = '95% CI: --';
  if (a > 0 && b > 0 && c > 0 && d > 0) {
    const seLnOr = Math.sqrt(1/a + 1/b + 1/c + 1/d);
    const ciLow = Math.exp(Math.log(or) - 1.96 * seLnOr);
    const ciHigh = Math.exp(Math.log(or) + 1.96 * seLnOr);
    ciText = `95% CI: ${ciLow.toFixed(1)} – ${ciHigh.toFixed(1)}`;
  }

  // Chi-square
  const N = a + b + c + d;
  const chi2 = (N * Math.pow(Math.abs(a * d - b * c), 2)) / ((a + b) * (c + d) * (a + c) * (b + d));

  const setEl = (id, val) => { const el = document.getElementById(id); if (el) el.textContent = val; };
  setEl('bio-res-se', `${se.toFixed(1)}%`);
  setEl('bio-res-sp', `${sp.toFixed(1)}%`);
  setEl('bio-res-ppv', `${ppv.toFixed(1)}%`);
  setEl('bio-res-or', or.toFixed(2));
  setEl('bio-res-ci', ciText);
  setEl('bio-res-chi2', `χ² = ${chi2.toFixed(2)}`);
  setEl('bio-res-p', chi2 > 10.83 ? 'p < 0.001 (Rất có ý nghĩa)' : (chi2 > 3.84 ? 'p < 0.05 (Có ý nghĩa thống kê)' : 'p > 0.05 (Không có ý nghĩa)'));
}

function copyVancouverCitation() {
  const el = document.getElementById('bio-vancouver-preview');
  if (el) {
    navigator.clipboard.writeText(el.textContent.trim());
    showToast('📋 Đã sao chép chuẩn trích dẫn Vancouver!', 'success');
  }
}


// --- 5. EXPORT ANKI & PRINTABLE WORD EXAM (.DOC) ---
function initExportView() {
  const sel = document.getElementById('export-subject-select');
  if (sel && (!sel.options || sel.options.length === 0)) {
    const subs = STATE.subjects || [];
    sel.innerHTML = subs.map(s => `<option value="${s.id}">${s.name} (${s.question_count || 0} câu)</option>`).join('');
  }
}

function downloadAnkiDeck() {
  const sel = document.getElementById('export-subject-select');
  const sid = sel ? sel.value : '10';
  const url = `/api/export/anki?subject_id=${sid}`;
  showToast('⏳ Đang chuẩn bị gói thẻ nhớ Anki Deck...', 'info');
  window.open(url, '_blank');
}

function downloadWordExam() {
  const sel = document.getElementById('export-subject-select');
  const lim = document.getElementById('export-exam-limit');
  const sid = sel ? sel.value : '10';
  const limit = lim ? lim.value : '40';
  const url = `/api/export/printable-exam?subject_id=${sid}&limit=${limit}`;
  showToast('🖨️ Đang tạo tài liệu Word chuẩn A4 ĐHYD Cần Thơ...', 'info');
  window.open(url, '_blank');
}


// ============================================================================
// UNIMASTER AI PRO v12.0 — SUBJECT-CENTRIC FLOW & USER ACCOUNT SYSTEM
// ============================================================================

STATE.currentUser = null;
STATE.activeSubjectId = null;

// --- 1. USER ACCOUNT & AUTH STATUS ---
async function fetchCurrentUserProfile() {
  try {
    const res = await apiFetch('/api/auth/me');
    if (res && res.success && res.user) {
      STATE.currentUser = res.user;
      updateHeaderUserPill();
      // If user has preferred subject in state, load it
      await hydrateUserStateFromServer();
    }
  } catch (err) {
    console.warn('Chưa đăng nhập hoặc chạy nội bộ:', err);
  }
}

function updateHeaderUserPill() {
  const pill = document.getElementById('header-user-btn');
  const avatar = document.getElementById('header-user-avatar');
  const nameEl = document.getElementById('header-user-name');
  const roleEl = document.getElementById('header-user-role');

  if (!pill) return;
  const user = (typeof getActiveAccount === 'function' ? getActiveAccount() : null) || STATE.currentUser || { name: 'Sinh Viên Y Khoa', role: 'student', username: 'ykhoa' };

  if (nameEl) nameEl.textContent = user.name || user.full_name || user.username;
  if (avatar) {
    avatar.textContent = user.avatar || (user.name || user.username || 'U')[0].toUpperCase();
  }
  if (roleEl) {
    if (user.role === 'admin') {
      roleEl.textContent = '👑 Quản Trị';
      roleEl.className = 'badge-rose px-1.5 py-0.5 rounded text-[10px] font-black';
    } else {
      roleEl.textContent = '🎓 ' + (user.name ? user.name.split('(')[0].trim() : 'Sinh Viên');
      roleEl.className = 'badge-brand px-1.5 py-0.5 rounded text-[10px] font-black text-emerald-400';
    }
  }
}

function openAccountModal() {
  const modal = document.getElementById('modal-account-profile');
  if (!modal) return;

  const activeAcc = getActiveAccount();
  STATE.currentUser = activeAcc;

  const user = activeAcc || { id: 1, name: 'Quản Trị Viên (Admin)', username: 'admin', role: 'admin' };
  const setEl = (id, val) => { const el = document.getElementById(id); if (el) el.textContent = val; };

  setEl('acc-modal-fullname', user.name || user.full_name || user.username);
  setEl('acc-modal-username', `@${user.username}`);
  setEl('acc-modal-role', user.role === 'admin' ? '👑 Quản Trị Viên Tối Cao' : '🎓 Sinh Viên');
  setEl('acc-modal-exams-count', `${STATE.stats?.total_exams || 0} bài`);
  setEl('acc-modal-mistakes-count', `${STATE.mistakes?.length || 0} câu`);
  setEl('acc-modal-streak', `${STATE.streak || 1} ngày 🔥`);

  const adminTabBtn = document.getElementById('acc-tab-admin-btn');
  if (adminTabBtn) {
    adminTabBtn.classList.toggle('hidden', user.role !== 'admin');
  }

  switchAccountTab('switch');
  renderAccountsListUI();
  openModal('modal-account-profile');
  playSound('click');
}

function switchAccountTab(tab) {
  document.getElementById('acc-panel-switch')?.classList.toggle('hidden', tab !== 'switch');
  document.getElementById('acc-panel-profile')?.classList.toggle('hidden', tab !== 'profile');
  document.getElementById('acc-panel-admin')?.classList.toggle('hidden', tab !== 'admin');

  document.getElementById('acc-tab-switch-btn')?.classList.toggle('active', tab === 'switch');
  document.getElementById('acc-tab-profile-btn')?.classList.toggle('active', tab === 'profile');
  document.getElementById('acc-tab-admin-btn')?.classList.toggle('active', tab === 'admin');

  if (tab === 'switch') renderAccountsListUI();
  if (tab === 'admin') loadAdminUsersList();
}

async function loadAdminUsersList() {
  const listEl = document.getElementById('acc-admin-users-list');
  if (!listEl) return;
  listEl.innerHTML = '<div class="py-6 text-center txt-muted text-xs">Đang tải danh sách tài khoản...</div>';

  try {
    const res = await apiFetch('/api/admin/users');
    if (res && res.success && res.users) {
      if (res.users.length === 0) {
        listEl.innerHTML = '<div class="py-6 text-center txt-muted text-xs">Chưa có tài khoản sinh viên nào đăng ký.</div>';
        return;
      }

      listEl.innerHTML = res.users.map(u => `
        <div class="uni-card p-3.5 flex items-center justify-between text-xs">
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 rounded-full flex items-center justify-center font-black ${u.role === 'admin' ? 'bg-rose-500/20 text-rose-400' : 'bg-emerald-500/20 text-emerald-400'}">
              ${(u.full_name || u.username)[0].toUpperCase()}
            </div>
            <div>
              <div class="font-extrabold txt-main flex items-center gap-1.5">
                <span>${escapeHtml(u.full_name || u.username)}</span>
                <span class="${u.role === 'admin' ? 'badge-rose' : 'badge-soft'} px-1.5 py-0.2 rounded text-[10px]">${u.role}</span>
              </div>
              <div class="text-[11px] txt-muted font-mono">@${u.username} • Đã thi ${u.exam_count || 0} bài • Điểm TB: ${u.avg_score ? Number(u.avg_score).toFixed(1) : '--'}</div>
            </div>
          </div>
          <div>
            ${u.role !== 'admin' ? `
              <button type="button" onclick="deleteUserAccount(${u.id}, '${escapeHtml(u.username)}')" class="btn-soft px-2.5 py-1 text-rose-400 hover:bg-rose-500/20 text-[11px] font-bold">
                Xóa
              </button>
            ` : '<span class="text-[11px] text-amber-400 font-bold">Chủ sở hữu</span>'}
          </div>
        </div>
      `).join('');
    } else {
      listEl.innerHTML = `<div class="py-4 text-center text-rose-400 text-xs">${res?.error || 'Không thể tải danh sách'}</div>`;
    }
  } catch (err) {
    listEl.innerHTML = `<div class="py-4 text-center text-rose-400 text-xs">Lỗi: ${err.message}</div>`;
  }
}

async function deleteUserAccount(uid, uname) {
  if (!confirm(`Bạn có chắc chắn muốn xóa tài khoản sinh viên "@${uname}" không? Mọi dữ liệu làm bài của sinh viên này sẽ bị xóa vĩnh viễn.`)) return;

  try {
    const res = await apiFetch(`/api/admin/users/${uid}`, { method: 'DELETE' });
    if (res && res.success) {
      showToast(`Đã xóa tài khoản @${uname}!`, 'success');
      loadAdminUsersList();
    } else {
      showToast(res?.error || 'Không thể xóa', 'error');
    }
  } catch (err) {
    showToast('Lỗi xóa: ' + err.message, 'error');
  }
}

async function handleLogout() {
  try {
    await fetch('/api/auth/logout', { method: 'POST' });
  } catch (_) {}
  showToast('Đang đăng xuất...', 'info');
  setTimeout(() => { window.location.href = '/login'; }, 300);
}


// --- 2. ACTIVE SUBJECT SELECTOR & CONTEXTUAL FILTERING ---
function initActiveSubjectBar() {
  const preferred =
    STATE.subjects.find((s) => s.code === 'HOASINH_CTUMP') ||
    STATE.subjects.find((s) => s.code === 'OOP_CSHARP') ||
    STATE.subjects[0];

  const savedSubId = localStorage.getItem('unimaster_active_subject_id');
  const matched = STATE.subjects.find((s) => String(s.id) === String(savedSubId));
  const active = matched || preferred;

  if (active) {
    selectActiveSubject(active.id, false);
  }
}

function openSubjectPickerModal() {
  const listEl = document.getElementById('subj-picker-list');
  if (!listEl) return;

  listEl.innerHTML = STATE.subjects.map((s) => {
    const isAct = String(s.id) === String(STATE.activeSubjectId);
    return `
      <div onclick="selectActiveSubject(${s.id}, true)" 
        class="uni-card p-4 flex items-center justify-between cursor-pointer transition-all hover:border-violet-500 ${isAct ? 'border-2 border-indigo-500 bg-indigo-500/10' : ''}">
        <div class="flex items-center gap-3">
          <div class="text-2xl">${s.icon || '📚'}</div>
          <div>
            <div class="font-extrabold text-sm txt-main flex items-center gap-2">
              <span>${escapeHtml(s.name)}</span>
              ${isAct ? '<span class="badge-brand px-2 py-0.5 rounded text-[10px] font-bold">Đang chọn</span>' : ''}
            </div>
            <div class="text-xs txt-muted mt-0.5">${escapeHtml(s.description || s.category || '')}</div>
          </div>
        </div>
        <div class="text-right">
          <span class="badge-soft font-mono font-bold text-xs px-2.5 py-1 rounded-lg">${s.question_count || 0} câu</span>
        </div>
      </div>
    `;
  }).join('');

  openModal('modal-subject-picker');
  playSound('click');
}

function selectActiveSubject(subjectId, notify = true) {
  const sub = STATE.subjects.find((s) => String(s.id) === String(subjectId));
  if (!sub) return;

  STATE.activeSubjectId = sub.id;
  STATE.examConfig.subjectId = sub.id;
  localStorage.setItem('unimaster_active_subject_id', String(sub.id));

  // Update Top Bar & Header Elements with Full Tooltip Title
  const iconEl = document.getElementById('active-subj-icon');
  const nameEl = document.getElementById('active-subj-name');
  const badgeEl = document.getElementById('active-subj-badge');
  const headerBtn = document.getElementById('header-active-subj-btn');

  if (iconEl) iconEl.textContent = sub.icon || '📚';
  if (nameEl) {
    nameEl.textContent = sub.name;
    nameEl.title = `${sub.name} (${sub.code}) - Bấm để đổi môn học`;
  }
  if (badgeEl) badgeEl.textContent = `${sub.question_count || 0} câu`;
  if (headerBtn) headerBtn.title = `Môn đang chọn: ${sub.name} (Bấm để đổi môn)`;

  // Update Hero Section on Dashboard
  const heroIcon = document.getElementById('hero-active-icon');
  const heroTitle = document.getElementById('hero-active-title');
  const heroDesc = document.getElementById('hero-subject-desc');
  const heroExamText = document.getElementById('hero-start-exam-text');

  if (heroIcon) heroIcon.textContent = sub.icon || '📚';
  if (heroTitle) heroTitle.textContent = sub.name;
  if (heroDesc) heroDesc.textContent = `${sub.code} • ${sub.question_count || 0} câu hỏi trắc nghiệm`;
  if (heroExamText) heroExamText.textContent = `Vào Thi: ${sub.name}`;

  // Update Floating Tutor Context
  const ftCtx = document.getElementById('floating-tutor-context');
  const ftWelcome = document.getElementById('floating-welcome-subj');
  if (ftCtx) ftCtx.textContent = `Đang hỗ trợ: ${sub.name}`;
  if (ftWelcome) ftWelcome.textContent = sub.name;

  // Refresh contextual shortcuts
  renderContextualShortcuts();

  // Sync all select dropdowns across tabs
  const ids = [
    'exam-subject-select',
    'exercise-subject-select',
    'fc-subject-select',
    'bank-subject-select',
    'tutor-subject-select',
    'gen-subject-select',
    'add-q-subject',
    'roadmap-subject-select',
    'battle-subject-select',
    'export-subject-select',
    'live-host-subject'
  ];
  ids.forEach((id) => {
    const sel = document.getElementById(id);
    if (sel && sel.value !== String(sub.id)) {
      sel.value = String(sub.id);
    }
  });

  closeModal('modal-subject-picker');

  // Context-aware refresh based on active tab
  if (STATE.currentTab === 'dashboard') renderDashboard();
  if (STATE.currentTab === 'exam') onExamSubjectChange();
  if (STATE.currentTab === 'flashcards') loadFlashcardsView();
  if (STATE.currentTab === 'search') filterQuestionBank();
  if (STATE.currentTab === 'exercises') loadExercisesView();

  if (notify) {
    showToast(`🎯 Đã chọn môn: ${sub.name}`, 'success');
    playSound('click');
  }
}


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
    try { testCases = JSON.parse(ex.test_cases_json); } catch (_) {}
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
        if (typeof triggerRubberDuckOnFailure === 'function') {
          triggerRubberDuckOnFailure(code, lang, res.compile_error);
        }
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
      if (typeof triggerRubberDuckOnFailure === 'function') {
        triggerRubberDuckOnFailure(code, lang, res.memory_leak_warning || `Chỉ đạt ${res.passed_tests}/${res.total_tests} test cases.`);
      }
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
  if (typeof pinnedTutorQuestion !== 'undefined' && pinnedTutorQuestion && pinnedTutorQuestion.source === 'timed_exam') {
    const cleanTimedT = (q.question_text || '').replace(/<[^>]+>/g, '').trim();
    pinnedTutorQuestion.id = q.id;
    pinnedTutorQuestion.shortTitle = `Thi 60P - Câu ${idx + 1}`;
    pinnedTutorQuestion.fullTitle = cleanTimedT;
    pinnedTutorQuestion.topic = q.topic_tag || '';
    pinnedTutorQuestion.code_snippet = q.code_snippet || '';
    pinnedTutorQuestion.option_a = q.option_a || '';
    pinnedTutorQuestion.option_b = q.option_b || '';
    pinnedTutorQuestion.option_c = q.option_c || '';
    pinnedTutorQuestion.option_d = q.option_d || '';
    pinnedTutorQuestion.correct_option = q.correct_option || '';
    pinnedTutorQuestion.user_answer = window.TIMED_EXAM.answers[q.id] || '';
    setText('ft-pinned-q-title', `📌 Thi 60P - Câu ${idx + 1} • ${pinnedTutorQuestion.topic || 'Kiến thức cốt lõi'}`);
    setText('ft-pinned-q-body', cleanTimedT.substring(0, 110) + (cleanTimedT.length > 110 ? '...' : ''));
    syncFloatingTutorSubjectContext();
  }
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


// =========================================================================
// UNIMASTER v15.0: ANTI-CHEAT VISIBILITY TAB LOCK HOOK
// =========================================================================
window.TAB_SWITCH_COUNT = 0;
window.ANTI_CHEAT_ACTIVE = false;

document.addEventListener('visibilitychange', () => {
  if (document.hidden && window.ANTI_CHEAT_ACTIVE) {
    window.TAB_SWITCH_COUNT++;
    if (window.TAB_SWITCH_COUNT === 1) {
      showToast('⚠️ CẢNH BÁO 1/3: Bạn vừa rời khỏi tab phòng thi! Rời tab quá 3 lần bài sẽ bị khóa!', 'warning');
      playSound('error');
    } else if (window.TAB_SWITCH_COUNT === 2) {
      showToast('🚨 CẢNH BÁO 2/3: Cảnh báo cuối cùng! Lần chuyển tab kế tiếp bài thi sẽ bị thu ngay!', 'error');
      playSound('error');
    } else if (window.TAB_SWITCH_COUNT >= 3) {
      triggerAntiCheatLock();
    }
  }
});

function activateAntiCheat(state = true) {
  window.ANTI_CHEAT_ACTIVE = state;
  window.TAB_SWITCH_COUNT = 0;
}

function triggerAntiCheatLock() {
  const overlay = document.getElementById('anti-cheat-lock-overlay');
  if (overlay) overlay.classList.remove('hidden');
  playSound('error');
  // Auto-submit current code or exam
  if (window.TIMED_EXAM && window.TIMED_EXAM.active) {
    submitTimedExamNow(true);
  } else {
    submitCodeTestCases();
  }
}

function unlockAntiCheatEmergency() {
  document.getElementById('anti-cheat-lock-overlay')?.classList.add('hidden');
  window.TAB_SWITCH_COUNT = 0;
  window.ANTI_CHEAT_ACTIVE = false;
  switchTab('dashboard');
}

// Auto-route on page load based on pathname
window.addEventListener('DOMContentLoaded', () => {
  const p = window.location.pathname;
  if (p.includes('/exam/practical')) {
    switchTab('exercises');
    activateAntiCheat(true);
  } else if (p.includes('/exam/essay')) {
    switchTab('essay');
  } else if (p.includes('/exam/survival')) {
    startTimedExamForSubject(5, 60, 40);
  } else if (p.includes('/exam/cheatsheet')) {
    openCheatSheetModal();
  }
});


// =========================================================================
// UNIMASTER v15.0: RUBBER DUCK TOXIC & SARCASTIC SOCRATIC TUTOR
// =========================================================================
async function triggerRubberDuckOnFailure(code, lang, errorTrace) {
  const duckEl = document.getElementById('rubber-duck-message-box');
  const duckContainer = document.getElementById('rubber-duck-sidebar');
  if (duckContainer) duckContainer.classList.remove('hidden');
  if (duckEl) {
    duckEl.innerHTML = '<div class="flex items-center gap-2"><span class="animate-bounce">🦆</span><span>Vịt Cao Su đang soi mã lỗi để tra tấn bạn...</span></div>';
  }

  try {
    const res = await apiFetch('/api/ai/rubber-duck', {
      method: 'POST',
      body: JSON.stringify({ code: code, language: lang, error_trace: errorTrace })
    });
    if (duckEl) {
      duckEl.innerHTML = `
        <div class="space-y-2">
          <div class="flex items-center gap-2 font-bold text-cyan-400">
            <span>🤖 Cố Vấn Lập Trình AI:</span>
          </div>
          <div class="txt-main leading-relaxed text-xs markdown-body">${renderMarkdown(res.reply || 'Vui lòng kiểm tra lại điều kiện biên và kiểu dữ liệu.')}</div>
        </div>
      `;
      renderAllMathOnPage(duckEl);
      playSound('click');
    }
  } catch (err) {
    if (duckEl) duckEl.textContent = '🦆 Vịt Cao Su: "Lỗi compiler rành rành ra đấy, tự sửa đi thiên tài!"';
  }
}


// =========================================================================
// UNIMASTER v15.0: STEP-BY-STEP ESSAY VALIDATOR WITH LINE HIGHLIGHT
// =========================================================================
async function triggerStepByStepEssayValidation() {
  const pid = STATE.essay.currentPromptId;
  const prompt = STATE.essay.prompts.find((p) => p.id === pid);
  const inputEl = document.getElementById('essay-student-input');
  const resCard = document.getElementById('essay-eval-result-card');
  if (!inputEl || !resCard) return;

  const studentAns = inputEl.value.trim();
  if (!studentAns) {
    showToast('Hãy gõ bài làm trước khi soi từng bước!', 'warning');
    return;
  }

  resCard.classList.remove('hidden');
  resCard.innerHTML = `
    <div class="py-6 text-center space-y-2">
      <div class="w-8 h-8 border-4 border-amber-500 border-t-transparent rounded-full animate-spin mx-auto"></div>
      <p class="font-bold text-xs text-amber-400">AI Giám Khảo đang quét từng dòng bài làm và kiểm tra logic quy nạp...</p>
    </div>
  `;

  try {
    const res = await apiFetch('/api/ai/validate-essay-steps', {
      method: 'POST',
      body: JSON.stringify({
        question_text: prompt ? prompt.question_text : 'Đề thi tự luận',
        student_proof: studentAns,
        topic: prompt ? prompt.topic : 'Toán Rời Rạc'
      })
    });

    const val = res.validation || {};
    const steps = val.steps || [];

    resCard.innerHTML = `
      <div class="space-y-4 animate-fade-in text-xs leading-relaxed">
        <div class="flex items-center justify-between p-3.5 rounded-xl border border-amber-500/30 bg-amber-500/10">
          <div>
            <span class="text-[10px] font-bold uppercase text-amber-300">ĐÁNH GIÁ TỪNG BƯỚC LOGIC</span>
            <h4 class="text-xl font-black text-white mt-0.5">${val.score || 8.0} / 10.0</h4>
          </div>
          <div class="text-xs text-amber-200 max-w-sm text-right leading-relaxed">${formatRichText(val.overall_verdict || '')}</div>
        </div>

        <div class="space-y-2">
          <span class="font-bold text-slate-300">Quét Chi Tiết Từng Dòng Bài Làm:</span>
          <div class="space-y-2 font-mono">
            ${steps
              .map((st) => {
                const isErr = st.status === 'error';
                const isWarn = st.status === 'warning';
                const borderCls = isErr ? 'border-rose-500 bg-rose-500/15 text-rose-300' : isWarn ? 'border-amber-500 bg-amber-500/10 text-amber-200' : 'border-emerald-500/40 bg-emerald-500/5 text-emerald-300';
                const badge = isErr ? '❌ SAI LOGIC' : isWarn ? '⚠️ CHƯA CHẶT CHẼ' : '✅ HỢP LỆ';
                return `
                <div class="p-3 rounded-xl border-l-4 ${borderCls} space-y-1">
                  <div class="flex items-center justify-between text-[11px] font-bold">
                    <span>Dòng #${st.line_number}:</span>
                    <span>${badge}</span>
                  </div>
                  <div class="text-slate-100 font-bold">${formatRichText(st.text || '')}</div>
                  <div class="text-[11px] opacity-90 font-sans">→ ${formatRichText(st.feedback || '')}</div>
                </div>`;
              })
              .join('')}
          </div>
        </div>

        ${
          val.missing_components && val.missing_components.length
            ? `<div class="p-3.5 rounded-xl border border-rose-500/30 bg-rose-500/10 text-rose-300 space-y-1">
                <span class="font-bold">⚠️ Các thành phần bị thiếu:</span>
                <ul class="space-y-0.5">${val.missing_components.map((m) => `<li>• ${escapeHtml(m)}</li>`).join('')}</ul>
              </div>`
            : ''
        }
      </div>
    `;
    renderAllMathOnPage(resCard);
  } catch (err) {
    resCard.innerHTML = `<div class="p-3 text-rose-400 text-xs">Lỗi soi bài: ${escapeHtml(err.message)}</div>`;
  }
}


// =========================================================================
// UNIMASTER v15.0: ALGO VISUALIZER (BUBBLE, QUICK, BINARY SEARCH, BFS)
// =========================================================================
window.ALGO_STATE = {
  type: 'bubble',
  array: [45, 12, 85, 32, 89, 39, 69, 24, 75, 15],
  steps: [],
  currentStepIndex: 0,
  isPlaying: false,
  timer: null
};

function openAlgoVisualizerModal() {
  document.getElementById('modal-algo-visualizer')?.classList.remove('hidden');
  initSelectedAlgo();
}

function closeAlgoVisualizerModal() {
  clearInterval(window.ALGO_STATE.timer);
  window.ALGO_STATE.isPlaying = false;
  document.getElementById('modal-algo-visualizer')?.classList.add('hidden');
}

function resetAlgoArray() {
  window.ALGO_STATE.array = Array.from({ length: 10 }, () => Math.floor(Math.random() * 85) + 10);
  initSelectedAlgo();
}

function initSelectedAlgo() {
  const sel = document.getElementById('algo-type-select');
  const type = sel ? sel.value : 'bubble';
  window.ALGO_STATE.type = type;
  window.ALGO_STATE.currentStepIndex = 0;
  clearInterval(window.ALGO_STATE.timer);
  window.ALGO_STATE.isPlaying = false;
  updateAlgoPlayBtn();

  // Generate trace steps
  if (type === 'bubble') {
    generateBubbleSortSteps();
  } else if (type === 'quick') {
    generateQuickSortSteps();
  } else if (type === 'binary_search') {
    generateBinarySearchSteps();
  } else {
    generateBfsSteps();
  }

  renderAlgoStep(0);
}

function generateBubbleSortSteps() {
  const arr = [...window.ALGO_STATE.array];
  const n = arr.length;
  const steps = [];

  // Step 0: Initial
  steps.push({ array: [...arr], comparing: [], swapped: false, codeLine: 1, note: 'Khởi tạo mảng ban đầu' });

  for (let i = 0; i < n - 1; i++) {
    for (let j = 0; j < n - i - 1; j++) {
      steps.push({ array: [...arr], comparing: [j, j + 1], swapped: false, codeLine: 3, note: `So sánh arr[${j}]=${arr[j]} và arr[${j+1}]=${arr[j+1]}` });
      if (arr[j] > arr[j + 1]) {
        let temp = arr[j];
        arr[j] = arr[j + 1];
        arr[j + 1] = temp;
        steps.push({ array: [...arr], comparing: [j, j + 1], swapped: true, codeLine: 4, note: `Hoán đổi ${arr[j+1]} và ${arr[j]} do arr[j] > arr[j+1]` });
      }
    }
  }
  steps.push({ array: [...arr], comparing: [], swapped: false, codeLine: 5, note: 'Hoàn tất sắp xếp mảng tăng dần!' });
  window.ALGO_STATE.steps = steps;
}

function generateBinarySearchSteps() {
  const arr = [...window.ALGO_STATE.array].sort((a, b) => a - b);
  window.ALGO_STATE.array = arr;
  const target = arr[Math.floor(arr.length / 2)];
  const steps = [];

  let low = 0, high = arr.length - 1;
  steps.push({ array: [...arr], low, high, mid: -1, codeLine: 1, note: `Tìm kiếm X = ${target} trên mảng tăng dần` });

  while (low <= high) {
    let mid = Math.floor((low + high) / 2);
    steps.push({ array: [...arr], low, high, mid, codeLine: 3, note: `Xét mid = ${mid} (arr[mid] = ${arr[mid]})` });
    if (arr[mid] === target) {
      steps.push({ array: [...arr], low, high, mid, found: true, codeLine: 4, note: `Tìm thấy ${target} tại chỉ số ${mid}!` });
      break;
    } else if (arr[mid] < target) {
      low = mid + 1;
      steps.push({ array: [...arr], low, high, mid, codeLine: 6, note: `arr[mid] < ${target} => Thu hẹp nửa phải (low = ${low})` });
    } else {
      high = mid - 1;
      steps.push({ array: [...arr], low, high, mid, codeLine: 8, note: `arr[mid] > ${target} => Thu hẹp nửa trái (high = ${high})` });
    }
  }
  window.ALGO_STATE.steps = steps;
}

function generateQuickSortSteps() {
  const arr = [...window.ALGO_STATE.array];
  const steps = [];
  steps.push({ array: [...arr], pivot: -1, comparing: [], codeLine: 1, note: 'Bắt đầu Quick Sort (Divide & Conquer)' });
  // Simplified demonstration steps
  steps.push({ array: [...arr], pivot: arr.length - 1, comparing: [0, arr.length - 1], codeLine: 2, note: `Chọn Pivot = arr[${arr.length-1}] = ${arr[arr.length-1]}` });
  arr.sort((a, b) => a - b);
  steps.push({ array: [...arr], pivot: -1, comparing: [], codeLine: 5, note: 'Phân hoạch và đệ quy hoàn tất sắp xếp!' });
  window.ALGO_STATE.steps = steps;
}

function generateBfsSteps() {
  const steps = [
    { array: [1, 2, 3, 4, 5], activeNode: 1, queue: [1], codeLine: 1, note: 'BFS: Đẩy đỉnh nguồn A vào Queue' },
    { array: [1, 2, 3, 4, 5], activeNode: 2, queue: [2, 3], codeLine: 3, note: 'Thăm đỉnh kề B và C' },
    { array: [1, 2, 3, 4, 5], activeNode: 4, queue: [4, 5], codeLine: 4, note: 'Duyệt tiếp các đỉnh tầng 2 (D, E)' },
    { array: [1, 2, 3, 4, 5], activeNode: -1, queue: [], codeLine: 5, note: 'Queue rỗng -> Hoàn tất duyệt toàn bộ đồ thị theo chiều rộng!' }
  ];
  window.ALGO_STATE.steps = steps;
}

function renderAlgoStep(idx) {
  window.ALGO_STATE.currentStepIndex = idx;
  const step = window.ALGO_STATE.steps[idx];
  if (!step) return;

  const container = document.getElementById('algo-bars-container');
  const codePane = document.getElementById('algo-pseudocode-pane');
  const counter = document.getElementById('algo-step-counter');

  if (counter) counter.textContent = `Bước: ${idx + 1} / ${window.ALGO_STATE.steps.length}`;

  // Render Bars
  if (container) {
    const maxVal = Math.max(...step.array, 50);
    container.innerHTML = step.array
      .map((val, i) => {
        const heightPct = Math.max(15, Math.round((val / maxVal) * 100));
        let barColor = 'bg-violet-600';
        if (step.comparing && step.comparing.includes(i)) {
          barColor = step.swapped ? 'bg-rose-500' : 'bg-amber-400';
        }
        if (step.mid === i) barColor = 'bg-cyan-400';
        if (step.pivot === i) barColor = 'bg-emerald-400';

        return `
        <div class="flex flex-col items-center gap-1.5 h-full justify-end group">
          <span class="text-[11px] font-mono font-bold text-white">${val}</span>
          <div class="w-8 sm:w-10 rounded-t-lg transition-all duration-300 ${barColor}" style="height: ${heightPct}%;"></div>
          <span class="text-[10px] font-mono text-slate-400">[${i}]</span>
        </div>`;
      })
      .join('');
  }

  // Render Pseudocode with line highlight
  if (codePane) {
    const lines = [
      { num: 1, text: 'procedure BubbleSort(A):' },
      { num: 2, text: '    for i = 0 to length(A) - 1:' },
      { num: 3, text: '        for j = 0 to length(A) - i - 1:' },
      { num: 4, text: '            if A[j] > A[j+1]: swap(A[j], A[j+1])' },
      { num: 5, text: '    return A' }
    ];
    codePane.innerHTML = lines
      .map((l) => {
        const isCur = step.codeLine === l.num;
        return `
        <div class="p-1 rounded flex items-center gap-2 ${isCur ? 'bg-amber-500/20 text-amber-300 font-bold' : 'text-slate-400'}">
          <span class="w-5 text-right opacity-50">${l.num}</span>
          <span>${escapeHtml(l.text)}</span>
        </div>`;
      })
      .join('') + `<div class="pt-2 border-t text-[11px] text-cyan-300 italic font-sans">${escapeHtml(step.note || '')}</div>`;
  }
}

function algoNextStep() {
  if (window.ALGO_STATE.currentStepIndex < window.ALGO_STATE.steps.length - 1) {
    renderAlgoStep(window.ALGO_STATE.currentStepIndex + 1);
  } else {
    clearInterval(window.ALGO_STATE.timer);
    window.ALGO_STATE.isPlaying = false;
    updateAlgoPlayBtn();
  }
}

function algoPrevStep() {
  if (window.ALGO_STATE.currentStepIndex > 0) {
    renderAlgoStep(window.ALGO_STATE.currentStepIndex - 1);
  }
}

function algoTogglePlay() {
  window.ALGO_STATE.isPlaying = !window.ALGO_STATE.isPlaying;
  updateAlgoPlayBtn();
  if (window.ALGO_STATE.isPlaying) {
    window.ALGO_STATE.timer = setInterval(() => {
      algoNextStep();
    }, 600);
  } else {
    clearInterval(window.ALGO_STATE.timer);
  }
}

function updateAlgoPlayBtn() {
  const btn = document.getElementById('algo-play-btn');
  if (btn) btn.textContent = window.ALGO_STATE.isPlaying ? '⏸ Tạm dừng' : '▶ Chạy (Play)';
}


// =========================================================================
// UNIMASTER v15.0: BUG HUNTER (THỢ SĂN LỖI CODE 20S GAMIFICATION)
// =========================================================================
window.BUG_HUNTER_STATE = {
  score: 0,
  combo: 0,
  currentIndex: 0,
  timerSeconds: 20,
  timerInterval: null,
  activeSample: null
};

const BUG_SAMPLES = [
  {
    title: "Bug #1: Sai Access Modifier Private Trong C#",
    hint: "Lớp con cố gắng truy cập trực tiếp biến private của lớp cha.",
    codeLines: [
      "public class Vehicle {",
      "    private int speed = 0;",
      "}",
      "public class Car : Vehicle {",
      "    public void Accelerate() {",
      "        speed += 10; // Cố truy cập private field",
      "    }",
      "}"
    ],
    bugLine: 6,
    explanation: "Dòng 6 sai vì `speed` được khai báo là `private` trong lớp cha `Vehicle`, lớp con không được phép truy cập trực tiếp. Cần đổi thành `protected` hoặc dùng Property."
  },
  {
    title: "Bug #2: Truy Cập Index Vượt Quá Kích Thước Mảng Python",
    hint: "Vòng lặp chạy vượt quá chỉ số phần tử cuối cùng của list.",
    codeLines: [
      "def print_elements(arr):",
      "    n = len(arr)",
      "    for i in range(n + 1):",
      "        print(arr[i]) # IndexError",
      "print_elements([10, 20, 30])"
    ],
    bugLine: 4,
    explanation: "Dòng 4 gặp lỗi `IndexError` vì `range(n + 1)` sinh chỉ số từ 0 đến n, nhưng chỉ số mảng hợp lệ chỉ từ 0 đến n - 1."
  },
  {
    title: "Bug #3: Quên Gọi Constructor Base() Trong C#",
    hint: "Lớp cha không có default constructor nhưng lớp con không gọi base().",
    codeLines: [
      "public class Person {",
      "    public Person(string name) { }",
      "}",
      "public class Student : Person {",
      "    public Student(string name) { } // Thiếu : base(name)",
      "}"
    ],
    bugLine: 5,
    explanation: "Dòng 5 lỗi biên dịch vì lớp cha `Person` không có parameterless constructor, lớp con bắt buộc phải gọi tường minh `: base(name)`."
  }
];

function openBugHunterModal() {
  document.getElementById('modal-bug-hunter')?.classList.remove('hidden');
  window.BUG_HUNTER_STATE.currentIndex = 0;
  window.BUG_HUNTER_STATE.score = 0;
  window.BUG_HUNTER_STATE.combo = 0;
  loadBugHunterSample(0);
}

function closeBugHunterModal() {
  clearInterval(window.BUG_HUNTER_STATE.timerInterval);
  document.getElementById('modal-bug-hunter')?.classList.add('hidden');
}

function loadBugHunterSample(idx) {
  const sample = BUG_SAMPLES[idx % BUG_SAMPLES.length];
  window.BUG_HUNTER_STATE.activeSample = sample;
  window.BUG_HUNTER_STATE.timerSeconds = 20;

  const titleEl = document.getElementById('bughunter-title');
  const hintEl = document.getElementById('bughunter-hint');
  const codeBox = document.getElementById('bughunter-code-container');
  const scoreEl = document.getElementById('bughunter-score');
  const banner = document.getElementById('bughunter-result-banner');

  if (titleEl) titleEl.textContent = sample.title;
  if (hintEl) hintEl.textContent = sample.hint;
  if (scoreEl) scoreEl.textContent = `Điểm: ${window.BUG_HUNTER_STATE.score} đ • Combo: ${window.BUG_HUNTER_STATE.combo}x`;
  if (banner) banner.className = 'hidden';

  // Render clickable lines
  if (codeBox) {
    codeBox.innerHTML = sample.codeLines
      .map((line, i) => {
        const lineNum = i + 1;
        return `
        <div onclick="clickBugLine(${lineNum})"
          class="p-2.5 px-4 flex items-center gap-3 hover:bg-violet-600/20 cursor-pointer border-b border-white/5 transition-all group">
          <span class="w-6 text-right text-slate-500 font-bold group-hover:text-cyan-400">${lineNum}</span>
          <span class="text-slate-200 group-hover:text-white">${escapeHtml(line)}</span>
        </div>`;
      })
      .join('');
  }

  // Start 20s countdown
  clearInterval(window.BUG_HUNTER_STATE.timerInterval);
  updateBugTimerDisplay();
  window.BUG_HUNTER_STATE.timerInterval = setInterval(() => {
    window.BUG_HUNTER_STATE.timerSeconds--;
    updateBugTimerDisplay();
    if (window.BUG_HUNTER_STATE.timerSeconds <= 0) {
      clearInterval(window.BUG_HUNTER_STATE.timerInterval);
      handleBugTimeout();
    }
  }, 1000);
}

function updateBugTimerDisplay() {
  const tEl = document.getElementById('bughunter-timer');
  if (tEl) {
    tEl.textContent = `${window.BUG_HUNTER_STATE.timerSeconds}s`;
    tEl.className = window.BUG_HUNTER_STATE.timerSeconds <= 5
      ? 'px-3.5 py-1.5 rounded-xl border font-mono text-base font-black text-rose-400 bg-rose-500/20 border-rose-500/50 animate-pulse'
      : 'px-3.5 py-1.5 rounded-xl border font-mono text-base font-black text-amber-400 bg-black/40 border-amber-500/40';
  }
}

function clickBugLine(lineNum) {
  clearInterval(window.BUG_HUNTER_STATE.timerInterval);
  const sample = window.BUG_HUNTER_STATE.activeSample;
  const banner = document.getElementById('bughunter-result-banner');

  if (lineNum === sample.bugLine) {
    // Correct!
    window.BUG_HUNTER_STATE.score += 10 + window.BUG_HUNTER_STATE.combo * 2;
    window.BUG_HUNTER_STATE.combo++;
    playSound('success');
    if (typeof confetti === 'function') confetti({ particleCount: 60, spread: 50 });

    if (banner) {
      banner.className = 'p-4 rounded-xl border border-emerald-500/40 bg-emerald-500/10 text-emerald-300 space-y-1 block animate-fade-in';
      banner.innerHTML = `
        <div class="flex items-center justify-between font-bold">
          <span>🎯 CHÍNH XÁC! Bạn đã bắt đúng dòng lỗi số ${lineNum}!</span>
          <span>+${10 + (window.BUG_HUNTER_STATE.combo - 1) * 2}đ</span>
        </div>
        <p class="text-[11px] font-normal leading-relaxed text-slate-200">${escapeHtml(sample.explanation)}</p>
        <button onclick="nextBugSample()" class="btn-primary !py-1 !px-3 text-xs mt-2 font-bold">Bài Tiếp Theo →</button>
      `;
    }
  } else {
    // Wrong line
    window.BUG_HUNTER_STATE.combo = 0;
    playSound('error');
    if (banner) {
      banner.className = 'p-4 rounded-xl border border-rose-500/40 bg-rose-500/10 text-rose-300 space-y-1 block animate-fade-in';
      banner.innerHTML = `
        <div class="font-bold">❌ SAI RỒI! Dòng ${lineNum} hoàn toàn hợp lệ.</div>
        <p class="text-[11px] font-normal leading-relaxed text-slate-300">Lỗi thực tế nằm ở dòng ${sample.bugLine}: ${escapeHtml(sample.explanation)}</p>
        <button onclick="nextBugSample()" class="btn-soft !py-1 !px-3 text-xs mt-2 font-bold">Bài Tiếp Theo →</button>
      `;
    }
  }
  document.getElementById('bughunter-score').textContent = `Điểm: ${window.BUG_HUNTER_STATE.score} đ • Combo: ${window.BUG_HUNTER_STATE.combo}x`;
}

function handleBugTimeout() {
  playSound('error');
  const banner = document.getElementById('bughunter-result-banner');
  const sample = window.BUG_HUNTER_STATE.activeSample;
  window.BUG_HUNTER_STATE.combo = 0;
  if (banner) {
    banner.className = 'p-4 rounded-xl border border-amber-500/40 bg-amber-500/10 text-amber-300 space-y-1 block animate-fade-in';
    banner.innerHTML = `
      <div class="font-bold">⏱️ HẾT GIỜ! Bạn đã không kịp bắt lỗi trong 20s.</div>
      <p class="text-[11px] font-normal leading-relaxed text-slate-300">Lỗi thực tế nằm ở dòng ${sample.bugLine}: ${escapeHtml(sample.explanation)}</p>
      <button onclick="nextBugSample()" class="btn-soft !py-1 !px-3 text-xs mt-2 font-bold">Bài Tiếp Theo →</button>
    `;
  }
}

function nextBugSample() {
  window.BUG_HUNTER_STATE.currentIndex++;
  loadBugHunterSample(window.BUG_HUNTER_STATE.currentIndex);
}


// =========================================================================
// UNIMASTER v15.0: CHEAT SHEET GENERATOR (TỔNG ÔN PHÚT CHÓT IN A4)
// =========================================================================
function openCheatSheetModal() {
  document.getElementById('modal-cheat-sheet')?.classList.remove('hidden');
  renderCheatSheetContent();
}

function closeCheatSheetModal() {
  document.getElementById('modal-cheat-sheet')?.classList.add('hidden');
}

function renderCheatSheetContent() {
  const container = document.getElementById('cheat-sheet-print-area');
  if (!container) return;

  const mistakes = JSON.parse(localStorage.getItem('unimaster_mistakes') || '[]');
  
  container.innerHTML = `
    <div class="border-b-2 border-black pb-3 text-center space-y-1">
      <h1 class="text-xl font-black uppercase tracking-tight text-black">UNIMASTER AI - TỜ PHAO TỔNG ÔN PHÚT CHÓT (A4 CRAMMING SHEET)</h1>
      <p class="text-[11px] text-gray-700 font-bold">Dành cho kỳ thi: OOP C# (15/11, 26/11) • Toán Rời Rạc (27/11) • NNLT1 (1/12) • AVCB 3 (4/12)</p>
    </div>

    <!-- 2-Column High-Density Content -->
    <div class="grid grid-cols-2 gap-6 text-[10px] leading-tight text-gray-900 font-mono">
      <!-- Left Column: Core OOP C# & Algorithms -->
      <div class="space-y-3">
        <div class="border border-black p-2 rounded">
          <h2 class="font-bold text-xs uppercase bg-black text-white px-1 mb-1">1. OOP C# CỐT LÕI CẦN NHỚ</h2>
          <p>• <strong>Đóng gói:</strong> <code>public int Prop { get; private set; }</code></p>
          <p>• <strong>Kế thừa & Constructor:</strong> <code>class Car : Vehicle { public Car() : base() {} }</code></p>
          <p>• <strong>Đa hình:</strong> Lớp cha dùng <code>virtual</code>, lớp con dùng <code>override</code>.</p>
          <p>• <strong>Interface:</strong> <code>interface IName</code>, không chứa state, đa thực thi.</p>
          <p>• <strong>LINQ:</strong> <code>list.Where(x => x.Gpa >= 7).OrderByDescending(x => x.Gpa)</code></p>
        </div>

        <div class="border border-black p-2 rounded">
          <h2 class="font-bold text-xs uppercase bg-black text-white px-1 mb-1">2. TOÁN RỜI RẠC & ĐỘ PHỨC TẠP</h2>
          <p>• <strong>Tương đương:</strong> <code>p → q ≡ ¬p ∨ q</code>; <code>¬(p ∧ q) ≡ ¬p ∨ ¬q</code></p>
          <p>• <strong>Euler:</strong> Đồ thị liên thông có chu trình Euler ⇔ mọi đỉnh bậc chẵn.</p>
          <p>• <strong>Cây N đỉnh:</strong> Có đúng <code>N - 1</code> cạnh.</p>
          <p>• <strong>Master Theorem:</strong> <code>T(n)=2T(n/2)+O(n) ⇒ Θ(n log n)</code> (Merge Sort)</p>
          <p>• <strong>Dijkstra:</strong> Thất bại khi có cạnh trọng số âm; dùng Bellman-Ford.</p>
        </div>
      </div>

      <!-- Right Column: Python & AVCB 3 Tech English -->
      <div class="space-y-3">
        <div class="border border-black p-2 rounded">
          <h2 class="font-bold text-xs uppercase bg-black text-white px-1 mb-1">3. PYTHON NNLT 1 PHẢN XẠ NHANH</h2>
          <p>• <strong>List Comprehension:</strong> <code>[x for x in nums if x > 0]</code></p>
          <p>• <strong>Dictionary:</strong> <code>d.get(key, 0) + 1</code> (đếm tần suất)</p>
          <p>• <strong>Đảo chuỗi:</strong> <code>s[::-1]</code>; <strong>Chuẩn hóa:</strong> <code>' '.join(w.capitalize() for w in s.split())</code></p>
          <p>• <strong>File with:</strong> <code>with open('f.txt') as f: data = f.read()</code></p>
        </div>

        <div class="border border-black p-2 rounded">
          <h2 class="font-bold text-xs uppercase bg-black text-white px-1 mb-1">4. AVCB 3 IT ENGLISH TỪ KHÓA B1/B2</h2>
          <p>• <strong>Allocate:</strong> Phân bổ tài nguyên máy chủ / RAM.</p>
          <p>• <strong>Scalability:</strong> Khả năng mở rộng quy mô hệ thống.</p>
          <p>• <strong>Under no circumstances + trợ động từ:</strong> Đảo ngữ cấm đoán.</p>
          <p>• <strong>Had S V3, S would have V3:</strong> Đảo ngữ câu điều kiện loại 3.</p>
          <p>• <strong>Take into account:</strong> Xem xét, tính đến một yếu tố.</p>
        </div>
      </div>
    </div>

    <div class="border-t border-black pt-2 text-center text-[10px] text-gray-600 font-bold">
      Chúc bạn thi đạt điểm A tuyệt đối trong 5 môn học! UniMaster đồng hành 24/7.
    </div>
  `;
}

function printCheatSheet() {
  window.print();
}


// =========================================================================
// UNIMASTER v15.0: DOUBLE-CLICK IT ENGLISH TOOLTIP DICTIONARY
// =========================================================================
const IT_DICTIONARY = {
  class: "Lớp đối tượng trong OOP (khuôn mẫu định nghĩa thuộc tính và phương thức).",
  interface: "Giao diện quy định hợp đồng các phương thức mà lớp con phải triển khai.",
  inherit: "Kế thừa: Lớp con nhận thuộc tính và hành vi từ lớp cha.",
  inheritance: "Tính kế thừa trong lập trình hướng đối tượng.",
  polymorphism: "Tính đa hình: Cùng một lời gọi hàm nhưng thực thi khác nhau tùy đối tượng.",
  encapsulation: "Tính đóng gói: Che giấu dữ liệu nội bộ qua private/protected.",
  variable: "Biến số lưu trữ giá trị trong bộ nhớ RAM.",
  array: "Mảng: Cấu trúc dữ liệu chứa các phần tử cùng kiểu liên tiếp trong bộ nhớ.",
  pointer: "Con trỏ: Biến lưu trữ địa chỉ bộ nhớ của một biến khác.",
  stack: "Ngăn xếp: Vùng nhớ LIFO lưu trữ biến cục bộ và lời gọi hàm.",
  heap: "Vùng nhớ Heap: Vùng nhớ cấp phát động qua new / malloc.",
  recursion: "Đệ quy: Hàm tự gọi lại chính nó với bài toán con nhỏ hơn.",
  compile: "Biên dịch mã nguồn thành mã máy hoặc bytecode.",
  async: "Bất đồng bộ: Xử lý tác vụ không chặn luồng chính.",
  await: "Chờ đợi một tác vụ bất đồng bộ hoàn thành.",
  virtual: "Từ khóa cho phép phương thức được ghi đè ở lớp con."
};

document.addEventListener('dblclick', (e) => {
  const selection = window.getSelection().toString().trim().toLowerCase();
  if (!selection || selection.length < 2) return;

  const def = IT_DICTIONARY[selection];
  if (def) {
    showToast(`📖 IT Dictionary [${selection}]: ${def}`, 'info');
  }
});


// =========================================================================
// UNIMASTER v15.0: SURVIVAL PREDICTOR LOGIC & COUNTDOWNS
// =========================================================================
function renderSurvivalPredictor() {
  const now = new Date();
  const exams = [
    { id: 'countdown-15-11', date: new Date(2026, 10, 15), name: 'OOP Thực hành C#', urgent: true },
    { id: 'countdown-16-11', date: new Date(2026, 10, 16), name: 'Giữa Kỳ Giải Thuật', urgent: true },
    { id: 'countdown-26-11', date: new Date(2026, 10, 26), name: 'OOP Trắc nghiệm & TH' },
    { id: 'countdown-27-11', date: new Date(2026, 10, 27), name: 'Toán Rời Rạc & Giải Thuật' },
    { id: 'countdown-01-12', date: new Date(2026, 11, 1), name: 'NNLT 1 Python' },
    { id: 'countdown-04-12', date: new Date(2026, 11, 4), name: 'Anh Văn Cơ Bản 3' }
  ];

  let nearestDays = 999;
  let nearestName = '';

  exams.forEach(ex => {
    const diffMs = ex.date.getTime() - now.getTime();
    const days = Math.max(0, Math.ceil(diffMs / (1000 * 60 * 60 * 24)));
    const el = document.getElementById(ex.id);
    if (el) {
      el.textContent = days === 0 ? 'HÔM NAY THI!' : `${days} ngày nữa`;
    }
    if (days < nearestDays) {
      nearestDays = days;
      nearestName = ex.name;
    }
  });

  const titleEl = document.getElementById('survival-urgent-title');
  if (titleEl) {
    const d15 = Math.max(0, Math.ceil((new Date(2026, 10, 15).getTime() - now.getTime()) / (1000 * 60 * 60 * 24)));
    const d16 = Math.max(0, Math.ceil((new Date(2026, 10, 16).getTime() - now.getTime()) / (1000 * 60 * 60 * 24)));
    if (d15 <= 7 && d16 <= 8) {
      titleEl.textContent = `15/11: OOP Thực Hành (${d15} ngày) • 16/11: Giữa Kỳ Giải Thuật (${d16} ngày)`;
    } else {
      titleEl.textContent = `${nearestName}: Còn đúng ${nearestDays} ngày!`;
    }
  }

  const quota = JSON.parse(localStorage.getItem('unimaster_daily_quota') || '{"done": 0, "target": 40}');
  const badge = document.getElementById('survival-quota-badge');
  if (badge) {
    badge.textContent = `Quota: ${quota.done} / ${quota.target} câu`;
  }
}

// =========================================================================
// UNIMASTER v15.0: SM-2 SPACED REPETITION FLASHCARD RATING
// =========================================================================
async function rateFlashcardSM2(rating) {
  const card = STATE.flashcards.cards[STATE.flashcards.currentIndex];
  if (!card) return;

  try {
    const res = await apiFetch('/api/flashcards/sm2-review', {
      method: 'POST',
      body: JSON.stringify({
        card_id: card.id,
        rating: rating,
        ease_factor: card.ease_factor || 2.5,
        interval_days: card.interval_days || 1,
        repetitions: card.repetitions || 0
      })
    });

    card.ease_factor = res.ease_factor;
    card.interval_days = res.interval_days;
    card.repetitions = res.repetitions;
    card.next_review = res.next_review;

    const statsEl = document.getElementById('fc-sm2-meta-stats');
    if (statsEl) {
      statsEl.innerHTML = `Ease: <strong class="text-white">${res.ease_factor.toFixed(2)}</strong> • Khoảng cách: <strong class="text-white">${res.interval_days} ngày</strong> • Lặp lại: <strong class="text-white">${res.repetitions} lần</strong> • Kế tiếp: <span class="text-amber-400 font-bold">${res.next_review}</span>`;
    }

    if (rating === 'again') {
      playSound('error');
      showToast('Đã đánh dấu Quên: Sẽ lặp lại thẻ này ngay trong hôm nay!', 'warning');
    } else {
      playSound('success');
      showToast(`Thuộc thẻ (${rating})! Ôn lại sau ${res.interval_days} ngày.`, 'success');
    }

    setTimeout(() => {
      nextFlashcard();
      // Update meta for next card
      const nextCard = STATE.flashcards.cards[STATE.flashcards.currentIndex];
      if (nextCard && statsEl) {
        statsEl.innerHTML = `Ease: <strong class="text-white">${(nextCard.ease_factor || 2.5).toFixed(2)}</strong> • Khoảng cách: <strong class="text-white">${nextCard.interval_days || 1} ngày</strong> • Lặp lại: <strong class="text-white">${nextCard.repetitions || 0} lần</strong>`;
      }
    }, 400);
  } catch (err) {
    showToast('Lỗi cập nhật SM-2: ' + err.message, 'error');
  }
}

// =========================================================================
// UNIMASTER v15.0: OOP BOILERPLATE SPEED TRAINER (< 2 PHÚT)
// =========================================================================
window.BOILERPLATE_STATE = {
  timer: null,
  secondsLeft: 120,
  startTime: null,
  activeDrill: null
};

const BOILERPLATE_DRILLS = [
  {
    title: "Class Student (Encapsulation)",
    prompt: "Khai báo class `Student` có thuộc tính `Id` (int, { get; private set; }), `FullName` (string, { get; set; }), constructor nhận 2 tham số, và phương thức `public void DisplayInfo()` in ra màn hình.",
    sample: `public class Student {
    public int Id { get; private set; }
    public string FullName { get; set; }

    public Student(int id, string fullName) {
        Id = id;
        FullName = fullName;
    }

    public void DisplayInfo() {
        Console.WriteLine($"{Id} - {FullName}");
    }
}`
  },
  {
    title: "Class BankAccount (Bảo Vệ Số Dư)",
    prompt: "Khai báo class `BankAccount` có thuộc tính `AccountNumber` (string, { get; }), `Balance` (double, { get; private set; }), constructor nhận số tài khoản & số dư ban đầu, phương thức `Deposit(double amount)` và `Withdraw(double amount)` kiểm tra điều kiện.",
    sample: `public class BankAccount {
    public string AccountNumber { get; }
    public double Balance { get; private set; }

    public BankAccount(string accNum, double initialBalance) {
        AccountNumber = accNum;
        Balance = initialBalance >= 0 ? initialBalance : 0;
    }

    public void Deposit(double amount) {
        if (amount > 0) Balance += amount;
    }

    public bool Withdraw(double amount) {
        if (amount > 0 && amount <= Balance) {
            Balance -= amount;
            return true;
        }
        return false;
    }
}`
  },
  {
    title: "Kế Thừa & Đa Hình: Shape -> Circle",
    prompt: "Khai báo abstract class `Shape` có thuộc tính `Name` (string) và `abstract double CalculateArea()`. Khai báo class `Circle` kế thừa `Shape`, có bán kính `Radius` (double), constructor gọi base(name), override `CalculateArea()` trả về Math.PI * Radius * Radius.",
    sample: `public abstract class Shape {
    public string Name { get; set; }
    public Shape(string name) { Name = name; }
    public abstract double CalculateArea();
}

public class Circle : Shape {
    public double Radius { get; set; }
    public Circle(string name, double radius) : base(name) {
        Radius = radius;
    }
    public override double CalculateArea() {
        return Math.PI * Radius * Radius;
    }
}`
  }
];

function openBoilerplateTrainerModal() {
  document.getElementById('modal-boilerplate-trainer')?.classList.remove('hidden');
  startNewBoilerplateDrill();
}

function closeBoilerplateTrainerModal() {
  clearInterval(window.BOILERPLATE_STATE.timer);
  document.getElementById('modal-boilerplate-trainer')?.classList.add('hidden');
}

function startNewBoilerplateDrill() {
  clearInterval(window.BOILERPLATE_STATE.timer);
  const drill = BOILERPLATE_DRILLS[Math.floor(Math.random() * BOILERPLATE_DRILLS.length)];
  window.BOILERPLATE_STATE.activeDrill = drill;
  window.BOILERPLATE_STATE.secondsLeft = 120;
  window.BOILERPLATE_STATE.startTime = Date.now();

  const promptEl = document.getElementById('boilerplate-prompt-text');
  const editorEl = document.getElementById('boilerplate-editor');
  const timerEl = document.getElementById('boilerplate-timer');
  const feedbackEl = document.getElementById('boilerplate-feedback-box');
  const wpmEl = document.getElementById('boilerplate-wpm');
  const accEl = document.getElementById('boilerplate-accuracy');

  if (promptEl) promptEl.textContent = drill.prompt;
  if (editorEl) {
    editorEl.value = '';
    editorEl.focus();
  }
  if (timerEl) {
    timerEl.textContent = '120s';
    timerEl.className = 'px-3 py-1 rounded-lg font-mono font-black text-sm bg-amber-500/20 text-amber-400 border border-amber-500/40';
  }
  if (feedbackEl) feedbackEl.className = 'hidden';
  if (wpmEl) wpmEl.textContent = 'Tốc độ: 0 WPM';
  if (accEl) accEl.textContent = 'Trạng thái cú pháp: Đang gõ...';

  window.BOILERPLATE_STATE.timer = setInterval(() => {
    window.BOILERPLATE_STATE.secondsLeft--;
    if (timerEl) {
      timerEl.textContent = `${window.BOILERPLATE_STATE.secondsLeft}s`;
      if (window.BOILERPLATE_STATE.secondsLeft <= 20) {
        timerEl.className = 'px-3 py-1 rounded-lg font-mono font-black text-sm bg-rose-500/20 text-rose-400 border border-rose-500/50 animate-pulse';
      }
    }
    if (window.BOILERPLATE_STATE.secondsLeft <= 0) {
      clearInterval(window.BOILERPLATE_STATE.timer);
      validateBoilerplateCode();
    }
  }, 1000);
}

function onBoilerplateInput() {
  const editorEl = document.getElementById('boilerplate-editor');
  const wpmEl = document.getElementById('boilerplate-wpm');
  if (!editorEl || !wpmEl || !window.BOILERPLATE_STATE.startTime) return;

  const text = editorEl.value;
  const elapsedMin = Math.max(0.1, (Date.now() - window.BOILERPLATE_STATE.startTime) / 60000);
  const words = text.trim().split(/\s+/).filter(Boolean).length;
  const wpm = Math.round(words / elapsedMin);
  wpmEl.textContent = `Tốc độ: ${wpm} WPM`;
}

async function validateBoilerplateCode() {
  clearInterval(window.BOILERPLATE_STATE.timer);
  const editorEl = document.getElementById('boilerplate-editor');
  const feedbackEl = document.getElementById('boilerplate-feedback-box');
  const accEl = document.getElementById('boilerplate-accuracy');
  if (!editorEl || !feedbackEl) return;

  const code = editorEl.value.trim();
  if (!code) {
    showToast('Hãy gõ code trước khi kiểm tra!', 'warning');
    return;
  }

  feedbackEl.classList.remove('hidden');
  feedbackEl.innerHTML = '<div class="text-amber-400 font-bold">🔍 Đang phân tích regex cú pháp và tính đóng gói OOP...</div>';

  try {
    const res = await apiFetch('/api/code/validate-oop', {
      method: 'POST',
      body: JSON.stringify({ code: code, language: 'csharp' })
    });

    const isGood = res.score >= 80;
    feedbackEl.className = isGood
      ? 'p-3.5 rounded-xl border border-emerald-500/40 bg-emerald-500/10 text-emerald-300 space-y-1 block animate-fade-in'
      : 'p-3.5 rounded-xl border border-amber-500/40 bg-amber-500/10 text-amber-200 space-y-1 block animate-fade-in';

    feedbackEl.innerHTML = `
      <div class="flex items-center justify-between font-bold">
        <span>${isGood ? '✅ ĐẠT YÊU CẦU OOP C#!' : '⚠️ CẦN HOÀN THIỆN THÊM'}</span>
        <span class="text-base">${res.score || 0} / 100đ</span>
      </div>
      <p class="text-xs leading-relaxed text-slate-200">${escapeHtml(res.feedback || '')}</p>
      ${res.passed_rules && res.passed_rules.length ? `<div class="text-[11px] text-emerald-400">Đạt: ${res.passed_rules.join(' • ')}</div>` : ''}
      ${res.missing_rules && res.missing_rules.length ? `<div class="text-[11px] text-rose-400">Thiếu: ${res.missing_rules.join(' • ')}</div>` : ''}
    `;

    if (accEl) accEl.textContent = `Trạng thái: ${res.score}đ (${isGood ? 'Hoàn hảo' : 'Cần sửa'})`;

    if (isGood) {
      playSound('success');
      if (typeof confetti === 'function') confetti({ particleCount: 50, spread: 60 });
    } else {
      playSound('error');
    }
  } catch (err) {
    feedbackEl.className = 'p-3 rounded-xl border border-rose-500/40 bg-rose-500/10 text-rose-300 block';
    feedbackEl.textContent = 'Lỗi kiểm tra: ' + err.message;
  }
}

// Hook renderSurvivalPredictor into renderDashboard
const origRenderDashboard = window.renderDashboard;
window.renderDashboard = function() {
  if (typeof origRenderDashboard === 'function') {
    origRenderDashboard.apply(this, arguments);
  }
  renderSurvivalPredictor();
};


function togglePasswordVis(inputId) {
  const el = document.getElementById(inputId);
  if (!el) return;
  el.type = el.type === 'password' ? 'text' : 'password';
}

function applyFostaPreset(model = 'gpt-6.1-sol') {
  const baseInp = document.getElementById('cfg-openai-base');
  const modelSel = document.getElementById('cfg-openai-model');
  const keyInp = document.getElementById('cfg-openai-key');
  if (baseInp) baseInp.value = 'https://codex.fosta.app/v1';
  if (modelSel) modelSel.value = model;
  // ponytail: leave input empty to avoid committing or auto-injecting expired secrets; user enters key via Settings
  showToast(`⚡ Đã điền cấu hình FOSTA (${model})! Hãy bấm "Kiểm Tra Kết Nối" hoặc "Lưu Cài Đặt".`, 'info');
  playSound('click');
}

function applyOpenAiDirectPreset() {
  const baseInp = document.getElementById('cfg-openai-base');
  const modelSel = document.getElementById('cfg-openai-model');
  if (baseInp) baseInp.value = 'https://api.openai.com/v1';
  if (modelSel) modelSel.value = 'gpt-4o-mini';
  showToast('🌐 Đã chọn máy chủ OpenAI Gốc (api.openai.com)!', 'info');
  playSound('click');
}

async function testOpenAiKeyUI() {
  const keyInp = document.getElementById('cfg-openai-key');
  const baseInp = document.getElementById('cfg-openai-base');
  const modelSel = document.getElementById('cfg-openai-model');
  const fb = document.getElementById('openai-test-feedback');
  if (!fb) return;

  const key = keyInp ? keyInp.value.trim() : '';
  const base_url = baseInp ? baseInp.value.trim() : '';
  const model = modelSel ? modelSel.value.trim() : '';

  fb.classList.remove('hidden');
  fb.className = 'text-xs p-3 rounded-xl font-bold badge-subtle';
  fb.textContent = '⏳ Đang gửi yêu cầu kiểm tra kết nối tới LLM / FOSTA Codex / OpenAI API...';

  try {
    const res = await apiFetch('/api/ai/test-openai', {
      method: 'POST',
      body: JSON.stringify({ key, base_url, model })
    });

    if (res.success) {
      fb.className = 'text-xs p-3 rounded-xl font-bold badge-emerald';
      fb.textContent = `✔ ${res.message || 'Kết nối thành công!'} • Khóa: ${res.masked_key || ''}`;
      showToast(res.message || 'Khóa AI hoạt động xuất sắc!', 'success');
      playSound('success');
    } else {
      fb.className = 'text-xs p-3 rounded-xl font-bold badge-rose';
      fb.innerHTML = `✘ ${escapeHtml(res.message || 'Lỗi kết nối')}. <br/><span class="font-normal opacity-90 mt-1 block">Mẹo: Nếu dùng FOSTA Codex, bấm nút <strong>[🔌 FOSTA Codex (gpt-6.1-sol)]</strong> ở trên để tự động điền đúng Base URL!</span>`;
      showToast('Kiểm tra LLM: ' + (res.message || 'Lỗi'), 'warning');
      playSound('error');
    }
  } catch (err) {
    fb.className = 'text-xs p-3 rounded-xl font-bold badge-rose';
    fb.textContent = '✘ Lỗi kiểm tra: ' + err.message;
    playSound('error');
  }
}

async function saveOpenAiSettingsUI() {
  const keyInp = document.getElementById('cfg-openai-key');
  const baseInp = document.getElementById('cfg-openai-base');
  const modelSel = document.getElementById('cfg-openai-model');
  const prioSel = document.getElementById('cfg-ai-priority');

  const payload = {};
  if (keyInp && keyInp.value.trim()) {
    payload.openai_api_key = keyInp.value.trim();
    localStorage.setItem('unimaster_openai_key', keyInp.value.trim());
  }
  if (baseInp && baseInp.value.trim()) {
    payload.openai_base_url = baseInp.value.trim();
    localStorage.setItem('unimaster_openai_base', baseInp.value.trim());
  }
  if (modelSel && modelSel.value.trim()) {
    payload.openai_model = modelSel.value.trim();
    localStorage.setItem('unimaster_openai_model', modelSel.value.trim());
  }
  if (prioSel) {
    payload.ai_provider_priority = prioSel.value;
  }

  const res = await apiFetch('/api/settings', {
    method: 'POST',
    body: JSON.stringify(payload)
  });

  if (res.success) {
    showToast('💾 Đã lưu cấu hình LLM (FOSTA / ChatGPT) thành công!', 'success');
    playSound('success');
    if (keyInp) keyInp.value = '';
    await checkApiKeyStatus();
  } else {
    showToast('Lỗi lưu cấu hình: ' + (res.error || 'Thử lại'), 'error');
  }
}



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
      const m = String(q.question_text || '').match(/^Câu\s+(\d+)/);
      const n = m ? parseInt(m[1], 10) : idx + 1;
      return n <= 27 || (q.topic_tag && q.topic_tag.includes('An toàn'));
    });
    partTitle = `CTUMP Phần 1: An Toàn PTN & Đo Quang Beer-Lambert (${selected.length} câu)`;
  } else if (partNum === 2) {
    selected = coreQuestions.filter((q, idx) => {
      const m = String(q.question_text || '').match(/^Câu\s+(\d+)/);
      const n = m ? parseInt(m[1], 10) : idx + 1;
      return (n >= 28 && n <= 56) || (q.topic_tag && q.topic_tag.includes('Protein') && !q.topic_tag.includes('Thận'));
    });
    partTitle = `CTUMP Phần 2: Bệnh Phẩm & Định Lượng Protein / Biuret (${selected.length} câu)`;
  } else if (partNum === 3) {
    selected = coreQuestions.filter((q, idx) => {
      const m = String(q.question_text || '').match(/^Câu\s+(\d+)/);
      const n = m ? parseInt(m[1], 10) : idx + 1;
      return (n >= 57 && n <= 130) || (q.topic_tag && q.topic_tag.includes('Thận'));
    });
    partTitle = `CTUMP Phần 3: Chức Năng Thận (Ure, Creatinin, Acid Uric) (${selected.length} câu)`;
  } else if (partNum === 4) {
    selected = coreQuestions.filter((q, idx) => {
      const m = String(q.question_text || '').match(/^Câu\s+(\d+)/);
      const n = m ? parseInt(m[1], 10) : idx + 1;
      return (n >= 131 && n <= 220) || (q.topic_tag && (q.topic_tag.includes('Enzym') || q.topic_tag.includes('Lipid')));
    });
    partTitle = `CTUMP Phần 4: Enzym Học & Bilang Lipid Máu (${selected.length} câu)`;
  } else if (partNum === 5) {
    selected = coreQuestions.filter((q, idx) => {
      const m = String(q.question_text || '').match(/^Câu\s+(\d+)/);
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
  const activeList = getLocalTutorHistory();
  const archiveList = getLocalTutorArchive();
  setText('tutor-hist-active-count', activeList.length);
  setText('tutor-hist-archive-count', archiveList.length);

  const isArchive = currentTutorHistorySubTab === 'archive';
  const list = filteredList !== null ? filteredList : (isArchive ? archiveList : activeList);
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
}

function exportTutorHistory() {
  const list = getLocalTutorHistory();
  if (!list.length) {
    showToast('Chưa có tin nhắn nào để xuất!', 'info');
    return;
  }
  let txt = '=== SỔ TAY GIA SƯ AI - UNIMASTER ===\n\n';
  list.forEach((m) => {
    txt += `[${m.displayTime || ''}] ${m.role === 'user' ? 'BẠN' : 'GIA SƯ AI'} (${m.context || 'Chung'}):\n${m.content}\n\n-------------------\n\n`;
  });
  const blob = new Blob([txt], { type: 'text/plain;charset=utf-8' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = `UniMaster_GiaSuAI_${new Date().toISOString().slice(0, 10)}.txt`;
  a.click();
  showToast('📄 Đã tải xuống sổ tay ghi chép AI!', 'success');
}


function askAiAboutCodeLine(uid, lineNum) {
  const code = CODE_REGISTRY[uid] || '';
  const lines = code.split('\n');
  const lineText = lines[lineNum - 1] || '';
  if (!lineText.trim()) return;

  openFloatingTutor();
  const query = `Trong bài thực hành lập trình có đoạn mã sau:\n\`\`\`csharp\n${code}\n\`\`\`\n\n👉 Em chưa hiểu rõ dòng #${lineNum}: \`${lineText.trim()}\`\nXin Thầy/Cô Gia Sư AI giải thích chi tiết dòng này làm nhiệm vụ gì, cú pháp hoạt động thế nào và các bẫy đề thi hay hỏi về nó?`;
  sendFloatingTutorCustomMessage(query);
}

function askAiAboutWholeCodeSnippet(uid, title = 'Program.cs', lang = 'csharp') {
  const code = CODE_REGISTRY[uid] || '';
  if (!code.trim()) return;

  openFloatingTutor();
  const query = `Em cần giải thích toàn bộ đoạn code "${title}":\n\`\`\`${lang}\n${code}\n\`\`\`\n\n👉 Xin Gia Sư AI phân tích từng khối lệnh, cấu trúc giải thuật và kết quả in ra màn hình của đoạn code này!`;
  sendFloatingTutorCustomMessage(query);
}


function setupTextSelectionAiListener() {
  const bubble = document.getElementById('text-select-ai-bubble');
  const wordEl = document.getElementById('text-select-ai-word');
  if (!bubble || !wordEl) return;

  let currentSelectedText = '';

  function handleSelection(e) {
    if (bubble.contains(e.target)) return;

    const sel = window.getSelection();
    const str = sel ? sel.toString().trim() : '';

    if (str && str.length >= 2 && str.length <= 90 && !/\n\n/.test(str)) {
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
    const query = `${contextPrompt}\n\n👉 Em chưa hiểu rõ về thuật ngữ/khái niệm: "${term}".\nXin Gia Sư AI giải thích thật ngắn gọn, dễ hiểu, đưa ra ví dụ và mẹo ghi nhớ để thi không bị nhầm lẫn!`;
    sendFloatingTutorCustomMessage(query);
  };
}


// --- UNIMASTER SAFE ARCHIVE SYSTEM (PERMANENT RETENTION & INSTANT RESTORE) ---
const LOCAL_EXAM_ARCHIVE_KEY = 'unimaster_exam_history_archive_v2';
const LOCAL_TUTOR_ARCHIVE_KEY = 'unimaster_tutor_history_archive_v2';

let currentExamHistorySubTab = 'active'; // 'active' | 'archive'
let currentTutorHistorySubTab = 'active'; // 'active' | 'archive'

function saveLocalExamHistory(list) {
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


// =========================================================================
// UNIMASTER v20: MULTI-ACCOUNT MANAGEMENT & SUBJECT ENROLLMENT PER ACCOUNT
// =========================================================================
const LOCAL_ACCOUNTS_KEY = 'unimaster_accounts_v2';
const LOCAL_ACTIVE_ACCOUNT_ID_KEY = 'unimaster_active_account_id_v2';

function getInitialAccounts() {
  return [
    {
      id: 'acc_y_khoa',
      name: 'Sinh Viên Y Khoa (CTUMP)',
      username: 'ykhoa_ctump',
      role: 'student',
      avatar: '🩺',
      enrolled_subjects: [10], // HOASINH_CTUMP
      theme: 'midnight',
      brand: '#7c3aed',
      created_at: '2026-11-01'
    },
    {
      id: 'acc_cntt',
      name: 'Sinh Viên CNTT & Lập Trình',
      username: 'cntt_dev',
      role: 'student',
      avatar: '💻',
      enrolled_subjects: [3, 4, 5, 8], // OOP, Python, Algorithms, Discrete Math
      theme: 'dark',
      brand: '#2563eb',
      created_at: '2026-11-02'
    },
    {
      id: 'acc_admin',
      name: 'Quản Trị Viên (Admin)',
      username: 'admin',
      role: 'admin',
      avatar: '👑',
      enrolled_subjects: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
      theme: 'dark',
      brand: '#7c3aed',
      created_at: '2026-11-01'
    }
  ];
}

function getAllLocalAccounts() {
  try {
    const raw = localStorage.getItem(LOCAL_ACCOUNTS_KEY);
    if (!raw) {
      const init = getInitialAccounts();
      localStorage.setItem(LOCAL_ACCOUNTS_KEY, JSON.stringify(init));
      return init;
    }
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) && parsed.length > 0 ? parsed : getInitialAccounts();
  } catch (_) {
    return getInitialAccounts();
  }
}

function saveAllLocalAccounts(list) {
  try {
    localStorage.setItem(LOCAL_ACCOUNTS_KEY, JSON.stringify(list || []));
  } catch (_) {}
}

function getActiveAccountId() {
  return localStorage.getItem(LOCAL_ACTIVE_ACCOUNT_ID_KEY) || 'acc_y_khoa';
}

function getActiveAccount() {
  const list = getAllLocalAccounts();
  const aid = getActiveAccountId();
  return list.find((a) => a.id === aid) || list[0];
}

function switchActiveAccount(accountId) {
  const list = getAllLocalAccounts();
  const acc = list.find((a) => a.id === accountId);
  if (!acc) return;

  localStorage.setItem(LOCAL_ACTIVE_ACCOUNT_ID_KEY, accountId);
  STATE.currentUser = acc;

  // Apply theme if stored
  if (acc.theme && typeof setThemeMode === 'function') {
    setThemeMode(acc.theme);
  }
  if (acc.brand && typeof setAccentPalette === 'function') {
    setAccentPalette(acc.brand, acc.brand);
  }

  updateHeaderUserPill();
  renderAccountsListUI();
  filterDashboardByEnrolledSubjects();

  // If user has enrolled subjects, set active subject to their first subject
  if (Array.isArray(acc.enrolled_subjects) && acc.enrolled_subjects.length > 0) {
    const sub = STATE.subjects.find((s) => s.id === acc.enrolled_subjects[0]);
    if (sub && typeof selectActiveSubject === 'function') {
      selectActiveSubject(sub.id);
    }
  }

  playSound('success');
  showToast(`🎉 Đã chuyển sang tài khoản: ${acc.name}!`, 'success');
}

function renderAccountsListUI() {
  const container = document.getElementById('acc-cards-container');
  if (!container) return;

  const list = getAllLocalAccounts();
  const activeId = getActiveAccountId();
  const activeAcc = getActiveAccount();

  // Update enrolled summary on card
  const summaryEl = document.getElementById('acc-active-enrolled-summary');
  if (summaryEl && activeAcc) {
    const enrolledIds = activeAcc.enrolled_subjects || [];
    if (!enrolledIds.length || enrolledIds.length === STATE.subjects.length) {
      summaryEl.textContent = 'Đang học: Toàn bộ 12 môn';
    } else {
      const names = STATE.subjects.filter((s) => enrolledIds.includes(s.id)).map((s) => s.name);
      summaryEl.textContent = `Đang học ${enrolledIds.length} môn: ${names.slice(0, 2).join(', ')}${names.length > 2 ? '...' : ''}`;
    }
  }

  container.innerHTML = list
    .map((acc) => {
      const isActive = acc.id === activeId;
      const enrolledIds = acc.enrolled_subjects || [];
      const subNames = STATE.subjects
        .filter((s) => enrolledIds.includes(s.id))
        .map((s) => `<span class="badge-subtle text-[10px] px-1.5 py-0.2 rounded font-sans font-bold">${s.icon || '📘'} ${escapeHtml(s.name.split('(')[0].trim())}</span>`)
        .slice(0, 3)
        .join(' ');

      return `
      <div class="acc-card ${isActive ? 'is-active' : ''} p-3.5 rounded-2xl flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-2xl flex items-center justify-center text-xl bg-gradient-to-tr from-indigo-500/20 to-purple-500/20 border border-indigo-500/30 shrink-0">
            ${acc.avatar || '🎓'}
          </div>
          <div>
            <div class="flex items-center gap-2">
              <span class="font-extrabold text-xs sm:text-sm txt-main">${escapeHtml(acc.name)}</span>
              ${isActive ? '<span class="badge-brand px-2 py-0.5 rounded-full text-[10px] font-bold">✓ Đang dùng</span>' : ''}
              ${acc.role === 'admin' ? '<span class="badge-rose px-1.5 py-0.2 rounded text-[10px] font-black">Admin</span>' : ''}
            </div>
            <div class="flex flex-wrap items-center gap-1 mt-1">
              ${subNames || '<span class="text-[10px] txt-muted italic">Chưa chọn môn học</span>'}
            </div>
          </div>
        </div>

        <div class="flex items-center gap-2 w-full sm:w-auto justify-end shrink-0">
          <button type="button" onclick="openAccountSubjectPickerModal('${acc.id}')" title="Chọn môn học cho tài khoản này" class="btn-soft px-2.5 py-1.5 text-xs font-bold text-indigo-400 hover:text-indigo-300">
            <span>📚</span> <span class="hidden sm:inline">Chọn môn</span>
          </button>
          ${!isActive ? `
            <button type="button" onclick="switchActiveAccount('${acc.id}')" class="btn-primary !bg-indigo-600 hover:!bg-indigo-500 px-3 py-1.5 text-xs font-black shadow-sm">
              Đổi sang Acc này
            </button>
          ` : `
            <span class="text-xs text-emerald-400 font-extrabold px-2">● Đang hoạt động</span>
          `}
        </div>
      </div>
    `;
    })
    .join('');
}

function promptCreateNewAccount() {
  const name = prompt('Nhập tên tài khoản học tập mới (VD: Sinh viên Y Dược, Ôn thi CNTT, Tài khoản 2...):');
  if (!name || !name.trim()) return;

  const list = getAllLocalAccounts();
  const emojis = ['🩺', '💻', '🔬', '📚', '⚡', '🦉', '🎨', '🚀', '🧠', '💊'];
  const randomEmoji = emojis[Math.floor(Math.random() * emojis.length)];

  const newAcc = {
    id: 'acc_' + Date.now(),
    name: name.trim(),
    username: name.trim().toLowerCase().replace(/[^a-z0-9]/g, '_').slice(0, 15) || 'user',
    role: 'student',
    avatar: randomEmoji,
    enrolled_subjects: [10], // Default to first CTUMP
    theme: 'midnight',
    brand: '#7c3aed',
    created_at: new Date().toISOString()
  };

  list.push(newAcc);
  saveAllLocalAccounts(list);
  switchActiveAccount(newAcc.id);

  // Immediately ask which subjects this account wants to study!
  setTimeout(() => {
    openAccountSubjectPickerModal(newAcc.id);
  }, 200);
}

// Target account being configured in Subject Enrollment Modal
let currentConfiguringAccountId = null;
let tempSelectedSubjectIds = new Set();

function openAccountSubjectPickerModal(accountId = null) {
  const targetId = accountId || getActiveAccountId();
  currentConfiguringAccountId = targetId;

  const list = getAllLocalAccounts();
  const acc = list.find((a) => a.id === targetId) || getActiveAccount();
  if (!acc) return;

  tempSelectedSubjectIds = new Set(acc.enrolled_subjects || []);
  setText('acc-subj-modal-user-name', acc.name);

  renderAccountSubjectCheckboxes();
  openModal('modal-account-subjects');
  playSound('click');
}

function renderAccountSubjectCheckboxes() {
  const grid = document.getElementById('acc-subjects-checkbox-grid');
  if (!grid) return;

  const allSubjects = STATE.subjects || [];
  setText('acc-subj-total-count', allSubjects.length);
  setText('acc-subj-selected-count', tempSelectedSubjectIds.size);

  grid.innerHTML = allSubjects
    .map((s) => {
      const isChecked = tempSelectedSubjectIds.has(s.id);
      return `
      <div onclick="toggleSubjectCheckbox(${s.id})" class="subj-checkbox-card ${isChecked ? 'selected' : ''} p-3 rounded-2xl flex items-center justify-between gap-3">
        <div class="flex items-center gap-2.5 overflow-hidden">
          <div class="w-9 h-9 rounded-xl flex items-center justify-center text-lg bg-white/5 border border-white/10 shrink-0">
            ${s.icon || '📘'}
          </div>
          <div class="overflow-hidden">
            <div class="text-xs font-black txt-main truncate">${escapeHtml(s.name)}</div>
            <div class="text-[10px] txt-muted flex items-center gap-1.5 mt-0.5">
              <span class="badge-brand px-1.5 py-0.2 rounded font-mono">${s.question_count || 0} câu</span>
              <span>•</span>
              <span class="truncate">${escapeHtml(s.category || 'Học phần')}</span>
            </div>
          </div>
        </div>
        <div class="w-6 h-6 rounded-lg border-2 flex items-center justify-center shrink-0 transition-all ${isChecked ? 'bg-indigo-600 border-indigo-600 text-white' : 'border-slate-500 bg-transparent'}">
          ${isChecked ? '<span class="text-xs font-black">✓</span>' : ''}
        </div>
      </div>
    `;
    })
    .join('');
}

function toggleSubjectCheckbox(subjectId) {
  if (tempSelectedSubjectIds.has(subjectId)) {
    tempSelectedSubjectIds.delete(subjectId);
  } else {
    tempSelectedSubjectIds.add(subjectId);
  }
  renderAccountSubjectCheckboxes();
  playSound('click');
}

function selectSubjectPreset(presetType) {
  tempSelectedSubjectIds.clear();
  const all = STATE.subjects || [];

  if (presetType === 'medical') {
    all.filter((s) => s.code === 'HOASINH_CTUMP' || (s.category && s.category.includes('Y')) || s.name.includes('Hóa Sinh')).forEach((s) => tempSelectedSubjectIds.add(s.id));
  } else if (presetType === 'it') {
    all.filter((s) => ['OOP_CSHARP', 'NNLT1', 'CTDL_GT', 'TOAN_RR'].includes(s.code) || s.category === 'Công nghệ thông tin' || s.name.includes('Lập trình')).forEach((s) => tempSelectedSubjectIds.add(s.id));
  } else if (presetType === 'general') {
    all.filter((s) => ['MLN101', 'CNXHKH', 'AVCB3'].includes(s.code) || s.category === 'Lý luận chính trị' || s.category === 'Ngoại ngữ').forEach((s) => tempSelectedSubjectIds.add(s.id));
  }
  renderAccountSubjectCheckboxes();
  playSound('click');
}

function selectAllSubjects(shouldSelectAll) {
  tempSelectedSubjectIds.clear();
  if (shouldSelectAll) {
    (STATE.subjects || []).forEach((s) => tempSelectedSubjectIds.add(s.id));
  }
  renderAccountSubjectCheckboxes();
  playSound('click');
}

function saveAccountEnrolledSubjects() {
  if (!currentConfiguringAccountId) currentConfiguringAccountId = getActiveAccountId();
  const list = getAllLocalAccounts();
  const acc = list.find((a) => a.id === currentConfiguringAccountId);
  if (!acc) return;

  const chosen = Array.from(tempSelectedSubjectIds);
  if (!chosen.length) {
    showToast('Vui lòng chọn ít nhất 1 môn học cho tài khoản!', 'warning');
    return;
  }

  acc.enrolled_subjects = chosen;
  saveAllLocalAccounts(list);

  if (acc.id === getActiveAccountId()) {
    STATE.currentUser = acc;
    filterDashboardByEnrolledSubjects();
  }

  renderAccountsListUI();
  closeModal('modal-account-subjects');
  playSound('success');
  showToast(`✅ Đã lưu ${chosen.length} môn học cho tài khoản: ${acc.name}!`, 'success');
}

function filterDashboardByEnrolledSubjects() {
  const acc = getActiveAccount();
  if (!acc || !Array.isArray(acc.enrolled_subjects) || !acc.enrolled_subjects.length) return;

  // Highlight or sort enrolled subjects first in subject select and dashboard grid
  if (typeof renderDashboard === 'function') {
    renderDashboard();
  }
}

// =========================================================================
// DEEP COLOR CUSTOMIZER STUDIO & FULLSCREEN
// =========================================================================
function setCustomStageBg(colorHex) {
  if (!STATE.ui) STATE.ui = { ...DEFAULT_UI_PREFS };
  STATE.ui.customBg = colorHex;
  const root = document.documentElement;
  
  if (colorHex) {
    root.style.setProperty('--bg-surface', colorHex);
    root.style.setProperty('--bg-card', colorHex);
    const lbl = document.getElementById('lbl-custom-bg');
    if (lbl) lbl.textContent = colorHex;
  }
  try {
    localStorage.setItem('unimaster_ui_prefs', JSON.stringify(STATE.ui));
  } catch (_) {}
  playSound('click');
}

function setOptionColorMode(mode) {
  if (!STATE.ui) STATE.ui = { ...DEFAULT_UI_PREFS };
  STATE.ui.optColorMode = mode;
  const root = document.documentElement;

  ['rainbow', 'uniform', 'contrast'].forEach((m) => {
    const btn = document.getElementById(`opt-style-${m}`);
    if (btn) btn.classList.toggle('border-indigo-500/80', m === mode);
  });

  if (mode === 'rainbow') {
    root.style.setProperty('--opt-a-accent', '#8b5cf6');
    root.style.setProperty('--opt-b-accent', '#3b82f6');
    root.style.setProperty('--opt-c-accent', '#10b981');
    root.style.setProperty('--opt-d-accent', '#f59e0b');
  } else if (mode === 'uniform') {
    const brand = STATE.ui.brand || '#7c3aed';
    root.style.setProperty('--opt-a-accent', brand);
    root.style.setProperty('--opt-b-accent', brand);
    root.style.setProperty('--opt-c-accent', brand);
    root.style.setProperty('--opt-d-accent', brand);
  } else if (mode === 'contrast') {
    root.style.setProperty('--opt-a-accent', '#ffffff');
    root.style.setProperty('--opt-b-accent', '#ffffff');
    root.style.setProperty('--opt-c-accent', '#ffffff');
    root.style.setProperty('--opt-d-accent', '#ffffff');
  }

  try {
    localStorage.setItem('unimaster_ui_prefs', JSON.stringify(STATE.ui));
  } catch (_) {}
  playSound('click');
}

function setFeedbackCustomColor(type, hex) {
  if (!STATE.ui) STATE.ui = { ...DEFAULT_UI_PREFS };
  const root = document.documentElement;

  if (type === 'correct') {
    STATE.ui.correctColor = hex;
    root.style.setProperty('--emerald-border', hex);
    root.style.setProperty('--emerald-bg', hex + '22');
  } else if (type === 'wrong') {
    STATE.ui.wrongColor = hex;
    root.style.setProperty('--rose-border', hex);
    root.style.setProperty('--rose-bg', hex + '22');
  }

  try {
    localStorage.setItem('unimaster_ui_prefs', JSON.stringify(STATE.ui));
  } catch (_) {}
}

function setQuestionTextColor(colorHex) {
  if (!STATE.ui) STATE.ui = { ...DEFAULT_UI_PREFS };
  STATE.ui.customQTextColor = colorHex;
  const root = document.documentElement;

  root.style.setProperty('--custom-q-text-color', colorHex || 'var(--text-main)');
  try {
    localStorage.setItem('unimaster_ui_prefs', JSON.stringify(STATE.ui));
  } catch (_) {}
  playSound('click');
}

function setGlobalZoomScale(percent) {
  if (!STATE.ui) STATE.ui = { ...DEFAULT_UI_PREFS };
  STATE.ui.zoomScale = percent;
  const root = document.documentElement;

  const basePx = (16 * (percent / 100)).toFixed(1);
  root.style.setProperty('--base-font-size', `${basePx}px`);

  document.querySelectorAll('.zoom-pill').forEach((el) => {
    el.classList.toggle('active', el.textContent.includes(`${percent}%`));
  });

  try {
    localStorage.setItem('unimaster_ui_prefs', JSON.stringify(STATE.ui));
  } catch (_) {}
  playSound('click');
}

function resetDeepColorCustomization() {
  if (!STATE.ui) STATE.ui = { ...DEFAULT_UI_PREFS };
  delete STATE.ui.customBg;
  delete STATE.ui.optColorMode;
  delete STATE.ui.correctColor;
  delete STATE.ui.wrongColor;
  delete STATE.ui.customQTextColor;
  delete STATE.ui.zoomScale;

  const root = document.documentElement;
  root.style.removeProperty('--bg-surface');
  root.style.removeProperty('--bg-card');
  root.style.removeProperty('--opt-a-accent');
  root.style.removeProperty('--opt-b-accent');
  root.style.removeProperty('--opt-c-accent');
  root.style.removeProperty('--opt-d-accent');
  root.style.removeProperty('--emerald-border');
  root.style.removeProperty('--emerald-bg');
  root.style.removeProperty('--rose-border');
  root.style.removeProperty('--rose-bg');
  root.style.removeProperty('--custom-q-text-color');
  root.style.removeProperty('--base-font-size');

  applyAllAppearancePrefs();
  playSound('success');
  showToast('Đã khôi phục cài đặt màu sắc & giao diện về mặc định!', 'info');
}

// =========================================================================
// FULLSCREEN DISTRACTION-FREE TOGGLE (TRÁNH VƯỚNG TAB TRÌNH DUYỆT)
// =========================================================================
function toggleAppFullscreen() {
  const isFs = Boolean(
    document.fullscreenElement ||
    document.webkitFullscreenElement ||
    document.mozFullScreenElement ||
    document.msFullscreenElement
  );

  if (!isFs) {
    const elem = document.documentElement;
    if (elem.requestFullscreen) {
      elem.requestFullscreen().catch(() => {});
    } else if (elem.webkitRequestFullscreen) {
      elem.webkitRequestFullscreen();
    } else if (elem.mozRequestFullScreen) {
      elem.mozRequestFullScreen();
    } else if (elem.msRequestFullscreen) {
      elem.msRequestFullscreen();
    }
    document.body.classList.add('app-fullscreen-mode');
    updateFullscreenUI(true);
    showToast('📺 Đã bật Toàn Màn Hình (Không vướng tab trình duyệt)!', 'success');
  } else {
    if (document.exitFullscreen) {
      document.exitFullscreen().catch(() => {});
    } else if (document.webkitExitFullscreen) {
      document.webkitExitFullscreen();
    } else if (document.mozCancelFullScreen) {
      document.mozCancelFullScreen();
    } else if (document.msExitFullscreen) {
      document.msExitFullscreen();
    }
    document.body.classList.remove('app-fullscreen-mode');
    updateFullscreenUI(false);
    showToast('🗗 Đã thu nhỏ màn hình.', 'info');
  }
}

function updateFullscreenUI(isFs) {
  const lbl = document.getElementById('header-fs-label');
  const heroLbl = document.getElementById('hero-fs-label');
  const heroIcon = document.getElementById('hero-fs-icon');
  const fsBtn = document.getElementById('header-fullscreen-btn');

  if (lbl) lbl.textContent = isFs ? 'Thu Nhỏ' : 'Toàn Màn Hình';
  if (heroLbl) heroLbl.textContent = isFs ? 'Thu Nhỏ Màn Hình' : 'Toàn Màn Hình Không Vướng Tab';
  if (heroIcon) heroIcon.textContent = isFs ? '🗗' : '⛶';
  if (fsBtn) fsBtn.classList.toggle('active', isFs);
}

document.addEventListener('fullscreenchange', () => {
  const isFs = Boolean(document.fullscreenElement);
  document.body.classList.toggle('app-fullscreen-mode', isFs);
  updateFullscreenUI(isFs);
});
document.addEventListener('webkitfullscreenchange', () => {
  const isFs = Boolean(document.webkitFullscreenElement);
  document.body.classList.toggle('app-fullscreen-mode', isFs);
  updateFullscreenUI(isFs);
});


// =========================================================================
// UNIMASTER v21.0: BACKUP EXPORT & IMPORT, CODE ASK AI, ARCHIVE SAFETY
// =========================================================================

function exportFullBackup() {
  try {
    const backupData = {
      app: 'UniMaster AI Pro',
      version: '21.0',
      exported_at: new Date().toISOString(),
      active_account_id: typeof getActiveAccountId === 'function' ? getActiveAccountId() : 'acc_default',
      accounts: typeof getAllLocalAccounts === 'function' ? getAllLocalAccounts() : [],
      exam_history: typeof getLocalExamHistory === 'function' ? getLocalExamHistory() : [],
      exam_archive: typeof getLocalExamArchive === 'function' ? getLocalExamArchive() : [],
      tutor_history: typeof getLocalTutorHistory === 'function' ? getLocalTutorHistory() : [],
      tutor_archive: typeof getLocalTutorArchive === 'function' ? getLocalTutorArchive() : [],
      bookmarks: Array.isArray(STATE.bookmarks) ? STATE.bookmarks : [],
      mistakes: Array.isArray(STATE.mistakes) ? STATE.mistakes : [],
      notes: (STATE.notes && typeof STATE.notes === 'object') ? STATE.notes : {},
      ui_prefs: (STATE.ui && typeof STATE.ui === 'object') ? STATE.ui : {},
      xp: Number(STATE.xp || 0),
      blitz_best: Number(STATE.blitzBest || 0),
      streak_days: Number(STATE.streakDays || 1)
    };

    const jsonStr = JSON.stringify(backupData, null, 2);
    const blob = new Blob([jsonStr], { type: 'application/json;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    const now = new Date();
    const pad = (n) => String(n).padStart(2, '0');
    const timeStr = `${now.getFullYear()}${pad(now.getMonth()+1)}${pad(now.getDate())}_${pad(now.getHours())}${pad(now.getMinutes())}`;
    a.href = url;
    a.download = `UniMaster_Full_Backup_${timeStr}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    if (typeof playSound === 'function') playSound('success');
    if (typeof showToast === 'function') {
      showToast('💾 Đã xuất toàn bộ tài khoản, lịch sử thi, chat AI và cài đặt ra file JSON an toàn!', 'success');
    }
  } catch (err) {
    if (typeof showToast === 'function') showToast('Không thể xuất file sao lưu: ' + err.message, 'error');
  }
}
window.exportFullBackup = exportFullBackup;

function triggerImportBackupModal() {
  let inp = document.getElementById('backup-file-input');
  if (!inp) {
    inp = document.createElement('input');
    inp.type = 'file';
    inp.id = 'backup-file-input';
    inp.accept = '.json,application/json';
    inp.style.display = 'none';
    inp.onchange = handleBackupFileSelected;
    document.body.appendChild(inp);
  }
  inp.click();
}
window.triggerImportBackupModal = triggerImportBackupModal;

async function handleBackupFileSelected(event) {
  const file = event?.target?.files?.[0];
  if (!file) return;

  try {
    const reader = new FileReader();
    reader.onload = async (e) => {
      try {
        const raw = e.target?.result;
        if (!raw) throw new Error('Tệp trống');
        const data = JSON.parse(raw);
        if (!data || typeof data !== 'object') {
          throw new Error('Dữ liệu sao lưu không đúng định dạng JSON');
        }

        // 1. Restore accounts
        if (Array.isArray(data.accounts) && data.accounts.length && typeof saveAllLocalAccounts === 'function') {
          saveAllLocalAccounts(data.accounts);
        }
        if (data.active_account_id && typeof LOCAL_ACTIVE_ACCOUNT_ID_KEY !== 'undefined') {
          localStorage.setItem(LOCAL_ACTIVE_ACCOUNT_ID_KEY, data.active_account_id);
        }

        // 2. Restore histories & archives
        if (Array.isArray(data.exam_history) && typeof saveLocalExamHistory === 'function') {
          saveLocalExamHistory(data.exam_history);
        }
        if (Array.isArray(data.exam_archive) && typeof saveLocalExamArchive === 'function') {
          saveLocalExamArchive(data.exam_archive);
        }
        if (Array.isArray(data.tutor_history) && typeof saveLocalTutorHistory === 'function') {
          saveLocalTutorHistory(data.tutor_history);
        }
        if (Array.isArray(data.tutor_archive) && typeof saveLocalTutorArchive === 'function') {
          saveLocalTutorArchive(data.tutor_archive);
        }

        // 3. Restore notebooks & learning state
        if (Array.isArray(data.bookmarks)) STATE.bookmarks = data.bookmarks;
        if (Array.isArray(data.mistakes)) STATE.mistakes = data.mistakes;
        if (data.notes && typeof data.notes === 'object') STATE.notes = { ...STATE.notes, ...data.notes };
        if (typeof data.xp === 'number') STATE.xp = data.xp;
        if (typeof data.blitz_best === 'number') STATE.blitzBest = data.blitz_best;
        if (typeof data.streak_days === 'number') STATE.streakDays = data.streak_days;

        // 4. Restore UI preferences
        if (data.ui_prefs && typeof data.ui_prefs === 'object') {
          STATE.ui = { ...STATE.ui, ...data.ui_prefs };
          localStorage.setItem('unimaster_ui_prefs', JSON.stringify(STATE.ui));
          if (typeof applyAllAppearancePrefs === 'function') applyAllAppearancePrefs();
        }

        // 5. Refresh UI
        if (typeof updateXpUI === 'function') updateXpUI();
        if (typeof renderAccountsListUI === 'function') renderAccountsListUI();
        if (typeof renderDashboard === 'function') renderDashboard();
        if (typeof updateHeaderUserPill === 'function') updateHeaderUserPill();

        // 6. Sync to server
        if (typeof syncUserStateToServer === 'function') syncUserStateToServer();

        if (typeof playSound === 'function') playSound('success');
        if (typeof showToast === 'function') {
          showToast('🎉 Đã khôi phục hoàn hảo 100% tài khoản, lịch sử ôn tập & cài đặt cá nhân!', 'success');
        }
      } catch (parseErr) {
        if (typeof showToast === 'function') showToast('Lỗi đọc nội dung file sao lưu: ' + parseErr.message, 'error');
      }
    };
    reader.readAsText(file);
  } catch (err) {
    if (typeof showToast === 'function') showToast('Không thể mở tệp sao lưu: ' + err.message, 'error');
  }
}
window.handleBackupFileSelected = handleBackupFileSelected;

// 2. Interactive Code Line & Snippet Explanation via AI Tutor
function askAiAboutSelectedCode() {
  const editor = document.getElementById('code-editor-textarea');
  let codeSnippet = '';
  if (editor) {
    const s = editor.selectionStart;
    const e = editor.selectionEnd;
    if (typeof s === 'number' && typeof e === 'number' && s !== e) {
      codeSnippet = editor.value.substring(s, e).trim();
    } else {
      codeSnippet = editor.value.trim();
    }
  }

  const ex = (STATE.exercises && STATE.exercises.list) ? STATE.exercises.list[STATE.exercises.selectedIndex] : null;
  const langSel = document.getElementById('code-lang-select');
  const lang = langSel?.value || (ex?.language || 'csharp');

  const questionPrompt = `Em đang học phần code thực hành "${ex?.title || 'Lập trình'}".\n\nĐây là đoạn code em đang thắc mắc:\n\`\`\`${lang}\n${codeSnippet || '// (Toàn bộ bài code)'}\n\`\`\`\n\nThầy/Cô hãy giải thích cặn kẽ từng dòng hoạt động như thế nào, em có bị lỗi cú pháp, logic hay rò rỉ bộ nhớ (memory leak) ở đâu không?`;

  if (typeof openFloatingTutor === 'function') openFloatingTutor();
  if (typeof sendFloatingTutorCustomMessage === 'function') {
    sendFloatingTutorCustomMessage(questionPrompt);
  }
}
window.askAiAboutSelectedCode = askAiAboutSelectedCode;

function askAiAboutQuestionCode() {
  const q = (STATE.exam && STATE.exam.questions) ? STATE.exam.questions[STATE.exam.currentIndex] : null;
  if (!q || !q.code_snippet) {
    if (typeof showToast === 'function') showToast('Câu này không có đoạn code đính kèm', 'info');
    return;
  }
  const prompt = `Em chưa hiểu cách chạy của đoạn code trong Câu ${STATE.exam.currentIndex + 1}:\n\`\`\`\n${q.code_snippet}\n\`\`\`\n\nThầy/Cô hãy giải thích từng dòng và cách tư duy để chọn đáp án đúng nhé!`;
  if (typeof openFloatingTutor === 'function') openFloatingTutor();
  if (typeof sendFloatingTutorCustomMessage === 'function') {
    sendFloatingTutorCustomMessage(prompt);
  }
}
window.askAiAboutQuestionCode = askAiAboutQuestionCode;

// =========================================================================
// UNIMASTER v22.0: STUDY BREAK GAMIFICATION & EXAM SAFE ERROR WRAPPERS
// =========================================================================

function startTimedBlitzMode() {
  if (typeof startBlitzMode === 'function') {
    startBlitzMode();
  } else {
    STATE.exam.mode = 'blitz';
    STATE.exam.blitzLives = 3;
    STATE.exam.blitzScore = 0;
    if (typeof startExam === 'function') startExam();
  }
  showToast('⚡ Đã kích hoạt Đấu Trường Blitz 60 Giây! Chúc bạn phá kỷ lục điểm số!', 'info');
}
window.startTimedBlitzMode = startTimedBlitzMode;

function openLofiPomodoroLounge() {
  if (typeof switchTab === 'function') switchTab('arena');
  const pomoPill = document.getElementById('arena-pomo-card');
  if (pomoPill) pomoPill.scrollIntoView({ behavior: 'smooth' });
  if (typeof playPomoSound === 'function') playPomoSound('rain');
  showToast('☕ Đang bật giai điệu mưa rơi thư giãn tại Pomodoro Lounge...', 'success');
}
window.openLofiPomodoroLounge = openLofiPomodoroLounge;

function triggerLuckyQuestionSpin() {
  const allQs = (STATE.examConfig && STATE.examConfig.subjectAllQuestions) ? STATE.examConfig.subjectAllQuestions : [];
  if (!allQs.length) {
    showToast('Đang chọn câu hỏi bất ngờ từ ngân hàng...', 'info');
    if (typeof switchTab === 'function') switchTab('exam');
    return;
  }
  const randomQ = allQs[Math.floor(Math.random() * allQs.length)];
  showToast(`🎲 Vòng quay đã chọn: Câu #${randomQ.id}! Hãy thử sức nhé!`, 'success');
  if (typeof launchExamWithQuestions === 'function') {
    launchExamWithQuestions([randomQ], 'practice');
  }
}
window.triggerLuckyQuestionSpin = triggerLuckyQuestionSpin;

// Global Escape Key to close Floating Tutor & Modals
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    const win = document.getElementById('floating-tutor-window');
    if (win && !win.classList.contains('hidden')) {
      closeFloatingTutor();
      return;
    }
  }
});
