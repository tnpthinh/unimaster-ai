# -*- coding: utf-8 -*-
"""
UniMaster v11.0 — Update static/app.js with full client logic for:
1. Live WebSocket Multiplayer Quiz Arena
2. Multi-step Virtual Clinical Patient Simulator
3. Clinical Pharmacology & Renal Dose Adjustment
4. Biostatistics & Research Lab (2x2 Table, OR, Chi-Square, Vancouver Citation)
5. 1-Click Anki Deck (.txt) & Word A4 Exam (.doc) Exporter
"""

import os

APP_JS_PATH = r"C:\Users\PC\.gemini\antigravity\scratch\unimaster-ai\static\app.js"

with open(APP_JS_PATH, "r", encoding="utf-8") as f:
    js_content = f.read()

# 1. Update switchArenaSubTab to support 'live'
old_switch_arena = """function switchArenaSubTab(sub) {
  ['battle', 'lounge', 'leaderboard'].forEach((k) => {
    document.getElementById(`arena-panel-${k}`)?.classList.toggle('hidden', k !== sub);
    document.getElementById(`arena-subtab-${k}`)?.classList.toggle('active', k === sub);
  });
  playSound('click');
}"""

new_switch_arena = """function switchArenaSubTab(sub) {
  ['live', 'battle', 'lounge', 'leaderboard'].forEach((k) => {
    document.getElementById(`arena-panel-${k}`)?.classList.toggle('hidden', k !== sub);
    document.getElementById(`arena-sub-${k}`)?.classList.toggle('active', k === sub);
    document.getElementById(`arena-subtab-${k}`)?.classList.toggle('active', k === sub);
  });
  if (sub === 'live') initLiveArenaView();
  playSound('click');
}"""

if "['live', 'battle', 'lounge', 'leaderboard']" not in js_content:
    js_content = js_content.replace(old_switch_arena, new_switch_arena, 1)

# 2. Update switchLabSubTab to support 'patient', 'dosing', 'biostat', 'export'
old_switch_lab = """function switchLabSubTab(subKey) {
  const subs = ['spectro', 'osce', 'handwritten', 'graph', 'calc'];
  subs.forEach((k) => {
    document.getElementById(`lab-sub-${k}`)?.classList.toggle('hidden', k !== subKey);
  });
  document.querySelectorAll('[data-labtab]').forEach((btn) => {
    btn.classList.toggle('active', btn.getAttribute('data-labtab') === subKey);
  });
  if (subKey === 'graph') renderInteractiveKnowledgeGraph();
  if (subKey === 'calc') runClinicalCalculators();
  playSound('click');
}"""

new_switch_lab = """function switchLabSubTab(subKey) {
  const subs = ['spectro', 'osce', 'handwritten', 'graph', 'calc', 'patient', 'dosing', 'biostat', 'export'];
  subs.forEach((k) => {
    document.getElementById(`lab-sub-${k}`)?.classList.toggle('hidden', k !== subKey);
  });
  document.querySelectorAll('[data-labtab]').forEach((btn) => {
    btn.classList.toggle('active', btn.getAttribute('data-labtab') === subKey);
  });
  if (subKey === 'graph') renderInteractiveKnowledgeGraph();
  if (subKey === 'calc') runClinicalCalculators();
  if (subKey === 'patient') initVirtualPatientView();
  if (subKey === 'dosing') runRenalDoseCalculation();
  if (subKey === 'biostat') runBiostatCalculations();
  if (subKey === 'export') initExportView();
  playSound('click');
}"""

if "'patient', 'dosing', 'biostat', 'export'" not in js_content:
    js_content = js_content.replace(old_switch_lab, new_switch_lab, 1)

# 3. Append the new v11.0 logic at the end of static/app.js
v11_js_extension = """
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
"""

js_content += "\n" + v11_js_extension

with open(APP_JS_PATH, "w", encoding="utf-8") as f:
    f.write(js_content)

print("Updated static/app.js successfully! Total characters:", len(js_content))
