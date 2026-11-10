# update_v16_app_and_ui.py
import re

print("Starting update_v16_app_and_ui...")

# -------------------------------------------------------------
# 1. Update static/app.js
# -------------------------------------------------------------
with open('static/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Update renderSurvivalPredictor
old_survival = """function renderSurvivalPredictor() {
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
}"""

new_survival = """function renderSurvivalPredictor() {
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
}"""

if old_survival in js:
    js = js.replace(old_survival, new_survival)
    print("Updated renderSurvivalPredictor in static/app.js")
else:
    print("Warning: old_survival pattern not found in app.js")

# Update DISCRETE_MATH_ALGO shortcuts
old_algo_sc = """  DISCRETE_MATH_ALGO: [
    { icon: '🎓', label: 'Trợ Giảng Chấm Tự Luận (5 Đề)', action: "switchTab('essay')" },
    { icon: '⏱️', label: 'Thi Thử 60p (40 câu Toán & GT)', action: 'startTimedExamForSubject(21, 60, 40)' },
    { icon: '📐', label: 'Đề 1: Logic & Quy Tắc Suy Diễn', action: "switchTab('essay'); loadEssayPromptById('ESSAY_01');" },
    { icon: '🌲', label: 'Đề 3: Cây Khung Kruskal & Prim', action: "switchTab('essay'); loadEssayPromptById('ESSAY_03');" },
    { icon: '⚡', label: 'Đề 4: Merge Sort & Master Theorem', action: "switchTab('essay'); loadEssayPromptById('ESSAY_04');" }
  ],"""

new_algo_sc = """  DISCRETE_MATH_ALGO: [
    { icon: '⚡', label: 'Thi Thử Giữa Kỳ 16/11 (40 câu)', action: 'startTimedExamForSubject(21, 60, 40)' },
    { icon: '📊', label: 'Mô Phỏng Thuật Toán Trực Quan', action: 'openAlgoVisualizerModal()' },
    { icon: '✍️', label: 'Trợ Giảng Chấm Tự Luận Thuật Toán', action: "switchTab('essay')" },
    { icon: '🎯', label: 'Săn Lỗi Thuật Toán 20s (Bug Hunter)', action: 'openBugHunterModal()' },
    { icon: '🗂️', label: 'Flashcard Bảng Độ Phức Tạp Big-O', action: 'openSubjectFlashcards(21)' }
  ],"""

if old_algo_sc in js:
    js = js.replace(old_algo_sc, new_algo_sc)
    print("Updated DISCRETE_MATH_ALGO shortcuts in static/app.js")
else:
    print("Warning: old_algo_sc pattern not found in app.js")

# Streamline hero description in selectActiveSubject
js = js.replace(
    "heroDesc.textContent = sub.description || `${sub.category || 'Môn học trọng tâm'} • ${sub.question_count || 0} câu hỏi trắc nghiệm`;",
    "heroDesc.textContent = `${sub.code} • ${sub.question_count || 0} câu hỏi trắc nghiệm`;"
)

with open('static/app.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("static/app.js written successfully.")


# -------------------------------------------------------------
# 2. Update static/index.html (streamlined luxury UI, less clutter)
# -------------------------------------------------------------
with open('static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 2A: Streamline Hero Card text
html = html.replace(
    'Hệ thống cá nhân hóa bám sát chương trình • Luyện đề thích ứng theo chủ đề',
    'Học phần trọng tâm • Luyện đề thông minh'
)

# 2B: Streamline survival button to directly trigger 16/11 timed exam
html = html.replace(
    '<button onclick="openSubjectExam(21)" class="btn-primary !bg-gradient-to-r !from-indigo-600 !to-cyan-600 px-3 py-1.5 text-xs font-bold flex items-center gap-1.5 shadow-md hover:scale-105 transition-all">\n              <span>⚡</span> Đề Giải Thuật (16/11)\n            </button>',
    '<button onclick="startTimedExamForSubject(21, 60, 40)" class="btn-primary !bg-gradient-to-r !from-indigo-600 !to-cyan-600 px-3 py-1.5 text-xs font-bold flex items-center gap-1.5 shadow-md hover:scale-105 transition-all">\n              <span>⚡</span> Đề Giải Thuật 60m (16/11)\n            </button>'
)

# 2C: Streamline subtitles and verbose headers
replacements = [
    (
        'Báo Cáo Tiến Độ Tuần & Tỷ Lệ Chuẩn Xác',
        'Tiến Độ 7 Ngày Qua'
    ),
    (
        '<p class="text-[11px] txt-muted">Thống kê số câu đã luyện và tỷ lệ trả lời đúng trong 7 ngày gần nhất</p>',
        '<p class="text-[11px] txt-muted">Số câu đã luyện và tỷ lệ chuẩn xác trong tuần</p>'
    ),
    (
        'Phân Tích Năng Lực 4 Cấp Độ & Lộ Trình AI Cá Nhân Hóa',
        'Năng Lực Bloom & Lộ Trình Ôn Tập'
    ),
    (
        '<p class="text-xs txt-muted mt-0.5">Chẩn đoán tự động theo thang nhận thức Bloom & Sổ tay câu sai của riêng bạn</p>',
        '<p class="text-xs txt-muted mt-0.5">Thống kê mức độ thông hiểu & lấp lỗ hổng kiến thức</p>'
    ),
    (
        '🎯 Dự Báo Điểm Thi Thật (AI Regression)',
        '🎯 Dự Báo Điểm Thi Thật'
    ),
    (
        '🔥 Bản Đồ Nhiệt Kiến Thức Theo Chương (Knowledge Heatmap)',
        '🔥 Bản Đồ Kiến Thức Theo Chuyên Đề'
    ),
    (
        'Bấm vào bất kỳ ô chuyên đề nào để luyện ngay 10 câu trọng tâm lấp lỗ hổng',
        'Chạm vào chuyên đề để luyện ngay câu sai'
    ),
    (
        'Mở Sổ Tay Câu Sai (Quy tắc 3-Strike Mastery)',
        'Sổ Tay Câu Sai (Mastery)'
    ),
    (
        'Chế độ sinh tử 3 tim ❤️❤️❤️',
        'Thử thách 3 tim ❤️❤️❤️'
    )
]

for old, new in replacements:
    if old in html:
        html = html.replace(old, new)
        print(f"Replaced text: '{old[:30]}...' -> '{new[:30]}...'")

# 2D: In modal-mobile-more, add button for 16/11 exam if not present
if "startTimedExamForSubject(21, 60, 40)" not in html:
    mobile_more_target = '<button onclick="switchTab(\'exercises\'); closeModal(\'modal-mobile-more\'); activateAntiCheat(true);"'
    mobile_btn_code = '''<button onclick="startTimedExamForSubject(21, 60, 40); closeModal('modal-mobile-more');" class="btn-soft p-3 rounded-xl flex flex-col items-center justify-center gap-1 text-center border-indigo-500/40 hover:border-indigo-500 bg-indigo-500/10">
          <span class="text-xl">⚡</span>
          <span class="text-xs font-extrabold text-indigo-300">Đề GT 16/11</span>
          <span class="text-[10px] txt-muted">40 câu thi thử 60p</span>
        </button>
        '''
    if mobile_more_target in html:
        html = html.replace(mobile_more_target, mobile_btn_code + mobile_more_target, 1)
        print("Added 16/11 quick exam button to modal-mobile-more")

with open('static/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("static/index.html written successfully.")
