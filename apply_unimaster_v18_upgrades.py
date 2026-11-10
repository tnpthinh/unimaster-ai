# apply_unimaster_v18_upgrades.py
import re

print("Starting UniMaster v18 Upgrades...")

# -------------------------------------------------------------
# 1. UPGRADE static/index.html
# -------------------------------------------------------------
with open('static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# A. Insert Range Picker Card & History Button in #exam-config-screen
range_picker_html = """
        <!-- HERO EXAM ACTION BAR: Range Picker + Local History + CTUMP 322 Parts -->
        <div class="grid grid-cols-1 md:grid-cols-12 gap-3.5">
          <!-- Card: Tự chọn thi từ câu mấy đến câu mấy (Custom Question Range) -->
          <div class="md:col-span-8 uni-card p-4 sm:p-5 space-y-3" style="border: 1.5px solid var(--brand-border); background: var(--bg-surface);">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2">
                <span class="text-xl">🎯</span>
                <div>
                  <h4 class="text-sm font-black txt-main">Tự Chọn Dải Câu Hỏi Ôn Thi (Từ câu ... đến câu ...)</h4>
                  <p class="text-[11px] txt-muted">Chủ động khoanh vùng bất kỳ đoạn câu nào muốn cày sâu (VD: từ câu 1 đến 50, hoặc 100 đến 150)</p>
                </div>
              </div>
              <span id="range-preview-badge" class="badge-brand px-2.5 py-1 rounded-lg text-xs font-mono font-bold">50 câu</span>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-12 gap-3 items-center">
              <div class="sm:col-span-5 flex items-center gap-2">
                <label class="text-xs font-bold txt-muted shrink-0">Từ câu #:</label>
                <input id="exam-range-from" type="number" min="1" value="1" oninput="updateRangePreview()" class="uni-input w-full px-3 py-2 text-center font-mono font-extrabold text-sm" />
              </div>

              <div class="sm:col-span-5 flex items-center gap-2">
                <label class="text-xs font-bold txt-muted shrink-0">Đến câu #:</label>
                <input id="exam-range-to" type="number" min="1" value="50" oninput="updateRangePreview()" class="uni-input w-full px-3 py-2 text-center font-mono font-extrabold text-sm" />
              </div>

              <div class="sm:col-span-2">
                <button type="button" onclick="startCustomRangeExam()" class="btn-primary w-full py-2.5 px-3 text-xs font-black shadow-md flex items-center justify-center gap-1.5 whitespace-nowrap">
                  <span>🚀</span> Vào Thi Dải Này
                </button>
              </div>
            </div>

            <!-- Quick Range Presets -->
            <div class="flex flex-wrap items-center gap-1.5 pt-1">
              <span class="text-[11px] font-bold txt-muted">Dải gợi ý:</span>
              <button type="button" onclick="setRangePreset(1, 30)" class="btn-soft px-2.5 py-1 text-[11px] font-semibold">1 – 30</button>
              <button type="button" onclick="setRangePreset(31, 60)" class="btn-soft px-2.5 py-1 text-[11px] font-semibold">31 – 60</button>
              <button type="button" onclick="setRangePreset(61, 100)" class="btn-soft px-2.5 py-1 text-[11px] font-semibold">61 – 100</button>
              <button type="button" onclick="setRangePreset(101, 150)" class="btn-soft px-2.5 py-1 text-[11px] font-semibold">101 – 150</button>
              <button type="button" onclick="setRangePreset(151, 200)" class="btn-soft px-2.5 py-1 text-[11px] font-semibold">151 – 200</button>
              <button type="button" onclick="setRangePreset(201, 250)" class="btn-soft px-2.5 py-1 text-[11px] font-semibold">201 – 250</button>
              <button type="button" onclick="setRangePreset(1, 9999)" class="btn-soft px-2.5 py-1 text-[11px] font-semibold txt-brand">Toàn bộ môn</button>
            </div>
          </div>

          <!-- Card: Quick Access to Local Exam History & CTUMP 322 Parts -->
          <div class="md:col-span-4 flex flex-col gap-2.5 justify-between">
            <button type="button" onclick="openLocalExamHistoryModal()" class="uni-card p-4 flex items-center justify-between gap-3 text-left hover:scale-[1.01] transition-all" style="border: 1.5px solid rgba(16, 185, 129, 0.4); background: var(--bg-surface);">
              <div class="flex items-center gap-2.5">
                <span class="text-2xl">📜</span>
                <div>
                  <div class="text-xs font-black txt-main">Lịch Sử Làm Bài Của Tôi</div>
                  <div class="text-[10px] txt-muted">Lưu trên máy • Làm lại câu sai</div>
                </div>
              </div>
              <span class="badge-emerald text-xs px-2 py-1 rounded-lg font-bold">Mở ↗</span>
            </button>

            <button type="button" onclick="openCtumpOriginalPartsModal()" class="uni-card p-4 flex items-center justify-between gap-3 text-left hover:scale-[1.01] transition-all" style="border: 1.5px solid rgba(99, 102, 241, 0.4); background: var(--bg-surface);">
              <div class="flex items-center gap-2.5">
                <span class="text-2xl">🏛️</span>
                <div>
                  <div class="text-xs font-black txt-main">Bộ 322 Câu Hóa Sinh Gốc</div>
                  <div class="text-[10px] txt-muted">Chia 5 phần chuẩn giáo trình CTUMP</div>
                </div>
              </div>
              <span class="badge-brand text-xs px-2 py-1 rounded-lg font-bold">Xem ↗</span>
            </button>
          </div>
        </div>
"""

target_exam_parts = '        <!-- Quick Sequential Parts -->\n        <div class="space-y-2.5">\n          <label class="text-xs font-extrabold uppercase tracking-wider txt-muted">Ôn nhanh theo phần</label>\n          <div id="exam-parts-grid" class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-2.5"></div>\n        </div>'
if target_exam_parts in html and "exam-range-from" not in html:
    html = html.replace(target_exam_parts, target_exam_parts + "\n\n" + range_picker_html)
    print("Added Custom Range Picker & History Hero Cards to Exam screen!")

# B. Add "Lịch Sử Làm Bài" button in Dashboard hero section
dash_hero_btn = '<button onclick="openLocalExamHistoryModal()" class="btn-soft px-3.5 py-2 text-xs font-bold rounded-xl flex items-center gap-1.5 shadow-sm"><span>📜</span> <span>Lịch Sử Làm Bài</span></button>'
if dash_hero_btn not in html:
    target_dash = '<button onclick="openSubjectPickerModal()" class="btn-soft px-4 py-2.5 text-xs font-bold rounded-xl flex items-center gap-2 shadow-sm">'
    if target_dash in html:
        html = html.replace(target_dash, dash_hero_btn + '\n          ' + target_dash)
        print("Added Lịch Sử Làm Bài button to Dashboard hero!")

# C. Add "Lịch Sử Chat" button in Floating Tutor header
if "openTutorHistoryModal()" not in html:
    target_ft_head = '<button type="button" onclick="toggleFloatingTutorSize()" id="btn-ft-expand"'
    if target_ft_head in html:
        html = html.replace(
            target_ft_head,
            '<button type="button" onclick="openTutorHistoryModal()" id="btn-ft-history" class="btn-soft p-1.5 text-xs" title="Lịch sử chat AI (Lưu trên máy)">📜</button>\n          ' + target_ft_head
        )
        print("Added Lịch Sử Chat button to Floating Tutor header!")

# D. Add the 3 New Modals before the closing </body> tag:
# 1. modal-ctump-original-parts (5 Parts breakdown for CTUMP 322 original questions)
# 2. modal-exam-history (Full local exam history on user machine)
# 3. modal-tutor-chat-history (Full local AI chat history on user machine)

new_modals_html = """
  <!-- =====================================================================
       MODAL: 322 CÂU HÓA SINH CTUMP GỐC CHIA THEO 5 PHẦN RIÊNG BIỆT
       ===================================================================== -->
  <div id="modal-ctump-original-parts" class="hidden fixed inset-0 z-50 modal-overlay flex items-center justify-center p-3 sm:p-5">
    <div class="uni-card w-full max-w-2xl max-h-[90vh] flex flex-col overflow-hidden animate-fade-in shadow-2xl" style="border: 1.5px solid var(--brand-border);">
      <!-- Header -->
      <div class="p-4 sm:p-5 flex items-center justify-between border-b shrink-0" style="border-color: var(--border); background-color: var(--bg-surface);">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-2xl flex items-center justify-center text-xl shadow-sm text-white" style="background: linear-gradient(135deg, #6366f1, #a855f7);">
            🏛️
          </div>
          <div>
            <h3 class="text-base font-black txt-main">Trọn Bộ 322 Câu Hóa Sinh CTUMP Gốc</h3>
            <p class="text-xs txt-muted">Phân chia rõ ràng theo 5 phần chuyên đề chuẩn tài liệu thực hành ĐHYD Cần Thơ</p>
          </div>
        </div>
        <button onclick="closeModal('modal-ctump-original-parts')" class="btn-soft p-1.5"><i data-lucide="x" class="w-4 h-4"></i></button>
      </div>

      <!-- Body: 5 Clean Part Cards -->
      <div class="p-4 sm:p-6 overflow-y-auto space-y-3.5 flex-1">
        <!-- Hero Button: Practice All 322 Questions -->
        <button type="button" onclick="startCtumpOriginalPart(0); closeModal('modal-ctump-original-parts');" class="w-full p-4 rounded-2xl text-left transition-all hover:scale-[1.01] flex items-center justify-between gap-3 shadow-md" style="background: linear-gradient(135deg, rgba(99,102,241,0.18), rgba(168,85,247,0.18)); border: 1.5px solid var(--brand-border);">
          <div class="flex items-center gap-3">
            <span class="text-2xl">⚡</span>
            <div>
              <div class="font-black text-sm text-indigo-400">Thi Toàn Bộ 322 Câu Gốc (Câu 1 – 312)</div>
              <div class="text-xs txt-muted">Luyện tổng thể toàn bộ giáo trình thực hành hóa sinh y khoa</div>
            </div>
          </div>
          <span class="btn-primary px-3.5 py-1.5 text-xs font-bold shrink-0">Bắt đầu thi →</span>
        </button>

        <!-- Part 1 -->
        <div class="p-4 rounded-2xl border transition-all hover:border-indigo-500/50 flex flex-col sm:flex-row sm:items-center justify-between gap-3" style="background-color: var(--bg-subtle); border-color: var(--border);">
          <div class="space-y-1">
            <div class="flex items-center gap-2">
              <span class="badge-brand text-xs px-2 py-0.5 rounded font-mono font-bold">Phần 1</span>
              <h4 class="text-xs font-black txt-main">An Toàn PTN & Kỹ Thuật Đo Quang Beer-Lambert</h4>
            </div>
            <p class="text-[11px] txt-muted">Quy tắc phỏng acid/kiềm, độc chất, máy quang phổ, định luật Beer-Lambert, bước sóng λ (Câu 1 – 27)</p>
          </div>
          <button type="button" onclick="startCtumpOriginalPart(1); closeModal('modal-ctump-original-parts');" class="btn-soft px-3 py-1.5 text-xs font-bold txt-brand shrink-0">
            Luyện Phần 1 (37c) →
          </button>
        </div>

        <!-- Part 2 -->
        <div class="p-4 rounded-2xl border transition-all hover:border-indigo-500/50 flex flex-col sm:flex-row sm:items-center justify-between gap-3" style="background-color: var(--bg-subtle); border-color: var(--border);">
          <div class="space-y-1">
            <div class="flex items-center gap-2">
              <span class="badge-brand text-xs px-2 py-0.5 rounded font-mono font-bold">Phần 2</span>
              <h4 class="text-xs font-black txt-main">Bệnh Phẩm & Định Lượng Protein / Phản Ứng Biuret</h4>
            </div>
            <p class="text-[11px] txt-muted">Thu thập & bảo quản huyết thanh/nước tiểu, phản ứng Biuret, Rivalta phân biệt dịch thấm/dịch tiết (Câu 28 – 56)</p>
          </div>
          <button type="button" onclick="startCtumpOriginalPart(2); closeModal('modal-ctump-original-parts');" class="btn-soft px-3 py-1.5 text-xs font-bold txt-brand shrink-0">
            Luyện Phần 2 (10c) →
          </button>
        </div>

        <!-- Part 3 -->
        <div class="p-4 rounded-2xl border transition-all hover:border-indigo-500/50 flex flex-col sm:flex-row sm:items-center justify-between gap-3" style="background-color: var(--bg-subtle); border-color: var(--border);">
          <div class="space-y-1">
            <div class="flex items-center gap-2">
              <span class="badge-brand text-xs px-2 py-0.5 rounded font-mono font-bold">Phần 3</span>
              <h4 class="text-xs font-black txt-main">Chức Năng Thận: Định Lượng Ure, Creatinin & Acid Uric</h4>
            </div>
            <p class="text-[11px] txt-muted">Đo động học 2 điểm Jaffé, Urease-GLDH, Uricase, độ thanh thải creatinin nội sinh, suy thận cấp & mạn (Câu 57 – 130)</p>
          </div>
          <button type="button" onclick="startCtumpOriginalPart(3); closeModal('modal-ctump-original-parts');" class="btn-soft px-3 py-1.5 text-xs font-bold txt-brand shrink-0">
            Luyện Phần 3 (72c) →
          </button>
        </div>

        <!-- Part 4 -->
        <div class="p-4 rounded-2xl border transition-all hover:border-indigo-500/50 flex flex-col sm:flex-row sm:items-center justify-between gap-3" style="background-color: var(--bg-subtle); border-color: var(--border);">
          <div class="space-y-1">
            <div class="flex items-center gap-2">
              <span class="badge-brand text-xs px-2 py-0.5 rounded font-mono font-bold">Phần 4</span>
              <h4 class="text-xs font-black txt-main">Enzym Học Lâm Sàng (AST, ALT, Amylase) & Bilang Lipid Máu</h4>
            </div>
            <p class="text-[11px] txt-muted">Tổn thương tế bào gan, viêm tụy cấp, định lượng Cholesterol toàn phần, Triglycerid, công thức Friedewald (Câu 131 – 220)</p>
          </div>
          <button type="button" onclick="startCtumpOriginalPart(4); closeModal('modal-ctump-original-parts');" class="btn-soft px-3 py-1.5 text-xs font-bold txt-brand shrink-0">
            Luyện Phần 4 (81c) →
          </button>
        </div>

        <!-- Part 5 -->
        <div class="p-4 rounded-2xl border transition-all hover:border-indigo-500/50 flex flex-col sm:flex-row sm:items-center justify-between gap-3" style="background-color: var(--bg-subtle); border-color: var(--border);">
          <div class="space-y-1">
            <div class="flex items-center gap-2">
              <span class="badge-brand text-xs px-2 py-0.5 rounded font-mono font-bold">Phần 5</span>
              <h4 class="text-xs font-black txt-main">Tổng Phân Tích Nước Tiểu & Soi Cặn Lắng Kính Hiển Vi</h4>
            </div>
            <p class="text-[11px] txt-muted">Que nhúng 10 thông số, ceton, sắc tố mật, nhận diện tiêu bản trụ hạt, hồng cầu, tinh thể canxi oxalat (Câu 221 – 312)</p>
          </div>
          <button type="button" onclick="startCtumpOriginalPart(5); closeModal('modal-ctump-original-parts');" class="btn-soft px-3 py-1.5 text-xs font-bold txt-brand shrink-0">
            Luyện Phần 5 (78c) →
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- =====================================================================
       MODAL: LỊCH SỬ LÀM BÀI CỦA TÔI (PERSISTENT LOCAL EXAM HISTORY)
       ===================================================================== -->
  <div id="modal-exam-history" class="hidden fixed inset-0 z-50 modal-overlay flex items-center justify-center p-3 sm:p-5">
    <div class="uni-card w-full max-w-4xl h-[88vh] max-h-[850px] flex flex-col overflow-hidden animate-fade-in shadow-2xl">
      <!-- Header -->
      <div class="p-4 sm:p-5 flex items-center justify-between border-b shrink-0" style="border-color: var(--border); background-color: var(--bg-surface);">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-2xl flex items-center justify-center text-xl shadow-sm text-white" style="background: linear-gradient(135deg, #10b981, #06b6d4);">
            📜
          </div>
          <div>
            <h3 class="text-base font-black txt-main">Lịch Sử Làm Bài & Ôn Thi Của Tôi</h3>
            <p class="text-xs txt-muted">Lưu trực tiếp trên máy của bạn — Xem lại từng câu đúng/sai & Luyện lại tức thì</p>
          </div>
        </div>
        <div class="flex items-center gap-2">
          <button type="button" onclick="clearAllLocalExamHistory()" class="btn-soft px-3 py-1.5 text-xs text-rose-400 hover:text-rose-300">
            🗑️ Xóa Lịch Sử
          </button>
          <button onclick="closeModal('modal-exam-history')" class="btn-soft p-1.5"><i data-lucide="x" class="w-4 h-4"></i></button>
        </div>
      </div>

      <!-- Quick Stats Strip -->
      <div class="px-5 py-3 border-b shrink-0 flex items-center justify-between gap-4 flex-wrap text-xs font-bold" style="background-color: var(--bg-subtle); border-color: var(--border);">
        <div class="flex items-center gap-4">
          <span>Tổng số lượt thi: <strong id="leh-stat-count" class="txt-brand font-mono">0</strong></span>
          <span>Điểm trung bình: <strong id="leh-stat-avg" class="txt-emerald font-mono">0.0</strong>/10</span>
          <span>Tổng câu đã làm: <strong id="leh-stat-total-q" class="txt-cyan font-mono">0</strong> câu</span>
        </div>
        <div class="text-[11px] txt-muted">Dữ liệu được lưu an toàn trong trình duyệt của bạn</div>
      </div>

      <!-- History List Container -->
      <div id="leh-history-list" class="p-4 sm:p-6 overflow-y-auto space-y-3 flex-1">
        <!-- Rendered dynamically via renderLocalExamHistoryModal() -->
      </div>
    </div>
  </div>

  <!-- =====================================================================
       MODAL: LỊCH SỬ CHAT GIA SƯ AI (PERSISTENT LOCAL AI CHAT HISTORY)
       ===================================================================== -->
  <div id="modal-tutor-chat-history" class="hidden fixed inset-0 z-50 modal-overlay flex items-center justify-center p-3 sm:p-5">
    <div class="uni-card w-full max-w-3xl h-[88vh] max-h-[850px] flex flex-col overflow-hidden animate-fade-in shadow-2xl">
      <!-- Header -->
      <div class="p-4 sm:p-5 flex items-center justify-between border-b shrink-0" style="border-color: var(--border); background-color: var(--bg-surface);">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-2xl flex items-center justify-center text-xl shadow-sm text-white" style="background: linear-gradient(135deg, #6366f1, #a855f7);">
            🤖
          </div>
          <div>
            <h3 class="text-base font-black txt-main">Lịch Sử Trò Chuyện Cùng Gia Sư AI</h3>
            <p class="text-xs txt-muted">Lưu tự động trên máy — Tra cứu lại mọi mẹo nhớ, công thức và lời giảng của AI</p>
          </div>
        </div>
        <div class="flex items-center gap-2">
          <button type="button" onclick="exportTutorHistory()" class="btn-soft px-3 py-1.5 text-xs">
            📄 Xuất Sổ Tay
          </button>
          <button type="button" onclick="clearAllTutorHistory()" class="btn-soft px-3 py-1.5 text-xs text-rose-400 hover:text-rose-300">
            🗑️ Xóa Lịch Sử
          </button>
          <button onclick="closeModal('modal-tutor-chat-history')" class="btn-soft p-1.5"><i data-lucide="x" class="w-4 h-4"></i></button>
        </div>
      </div>

      <!-- Search & Filter Bar -->
      <div class="p-3 sm:p-4 border-b shrink-0 flex items-center gap-2" style="background-color: var(--bg-subtle); border-color: var(--border);">
        <div class="relative flex-1">
          <input id="tutor-history-search" type="text" placeholder="🔍 Tìm lại kiến thức đã hỏi (VD: Friedewald, Biuret, Creatinin, OGTT...)" oninput="filterTutorHistory(this.value)" class="uni-input w-full pl-3.5 pr-8 py-2 text-xs" style="background-color: var(--bg-surface);" />
        </div>
        <span id="tutor-history-count" class="badge-brand text-xs px-2.5 py-1.5 rounded-lg font-mono font-bold shrink-0">0 tin nhắn</span>
      </div>

      <!-- Messages List -->
      <div id="tutor-history-messages-list" class="p-4 sm:p-6 overflow-y-auto space-y-3.5 flex-1">
        <!-- Rendered dynamically via renderTutorHistoryModal() -->
      </div>
    </div>
  </div>
"""

if "modal-ctump-original-parts" not in html:
    html = html.replace('</body>', new_modals_html + '\n</body>')
    print("Added modal-ctump-original-parts, modal-exam-history, and modal-tutor-chat-history to index.html!")

with open('static/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("static/index.html updated successfully!")
