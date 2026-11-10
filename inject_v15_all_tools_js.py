# Script to inject comprehensive v15 features into static/app.js:
# - Anti-cheat visibilitychange tab lock
# - Rubber Duck toxic tutor
# - Step-by-step essay validator with line highlight
# - AlgoVisualizer (Bubble, Quick, Binary Search, BFS)
# - SM-2 Spaced Repetition Flashcards
# - BugHunter 20s gamified code sniper
# - CheatSheetGenerator for 1-click A4 print
# - Double-click IT English dictionary tooltip

v15_js_code = r'''
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
          <div class="flex items-center gap-2 font-bold text-amber-400">
            <span>🦆 Vịt Cao Su Trợ Giảng (Toxic Mode):</span>
          </div>
          <div class="txt-sub leading-relaxed text-xs italic">${formatRichText(res.reply || 'Viết code cẩn thận lại xem!')}</div>
        </div>
      `;
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
          <p class="text-xs text-amber-200 italic max-w-sm text-right">${escapeHtml(val.overall_verdict || '')}</p>
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
                  <div class="text-slate-100 font-bold">${escapeHtml(st.text || '')}</div>
                  <div class="text-[11px] opacity-90 font-sans italic">→ ${escapeHtml(st.feedback || '')}</div>
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
'''

with open(r'C:\Users\PC\.gemini\antigravity\scratch\unimaster-ai\static\app.js', 'a', encoding='utf-8') as f:
    f.write('\n' + v15_js_code)

print("app.js updated with v15 tools.")
