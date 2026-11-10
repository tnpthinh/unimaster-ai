import os

app_js_path = r'static/app.js'
with open(app_js_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

v15_extra_js = r'''
// =========================================================================
// UNIMASTER v15.0: SURVIVAL PREDICTOR LOGIC & COUNTDOWNS
// =========================================================================
function renderSurvivalPredictor() {
  const now = new Date();
  const exams = [
    { id: 'countdown-15-11', date: new Date(2026, 10, 15), name: 'OOP Thực hành C#', urgent: true },
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
    titleEl.textContent = `${nearestName}: Còn đúng ${nearestDays} ngày!`;
  }

  const quota = JSON.parse(localStorage.getItem('unimaster_daily_quota') || '{"done": 0, "target": 40}');
  const badge = document.getElementById('survival-quota-badge');
  if (badge) {
    badge.textContent = `Quota hôm nay: ${quota.done} / ${quota.target} câu`;
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
'''

# Append to app.js
with open(app_js_path, 'a', encoding='utf-8') as f:
    f.write('\n' + v15_extra_js)

print("Appended v15 extra JS functions to static/app.js.")
