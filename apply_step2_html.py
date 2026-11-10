html_path = r'C:\Users\PC\.gemini\antigravity\scratch\unimaster-ai\static\index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Add #modal-account-subjects after modal-account-profile
account_modal_end = '<!-- =====================================================================\n       FLOATING AI TUTOR WIDGET'

modal_subjects_html = '''<!-- =====================================================================
       ACCOUNT SUBJECT ENROLLMENT MODAL (HỎI ACC ĐÓ CHỌN NHỮNG MÔN NÀO ĐỂ HỌC)
       ===================================================================== -->
  <div id="modal-account-subjects" class="hidden fixed inset-0 z-50 modal-overlay flex items-center justify-center p-3 sm:p-5">
    <div class="uni-card w-full max-w-2xl max-h-[90vh] flex flex-col overflow-hidden animate-fade-in shadow-2xl">
      <!-- Modal Header -->
      <div class="p-4 sm:p-5 flex items-center justify-between border-b shrink-0" style="border-color: var(--border); background-color: var(--bg-surface);">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-2xl flex items-center justify-center text-xl shadow-sm text-white" style="background: linear-gradient(135deg, #6366f1, #8b5cf6);">
            📚
          </div>
          <div>
            <h3 class="text-base font-black txt-main flex items-center gap-2">
              <span>Chọn Môn Học Cho:</span>
              <span id="acc-subj-modal-user-name" class="text-indigo-400 underline decoration-indigo-500 font-extrabold">Tài Khoản</span>
            </h3>
            <p class="text-xs txt-muted">Đánh dấu những môn bạn muốn học. Hệ thống sẽ cá nhân hóa Dashboard và kho đề thi theo các môn này!</p>
          </div>
        </div>
        <button onclick="closeModal('modal-account-subjects')" class="btn-soft p-1.5"><i data-lucide="x" class="w-4 h-4"></i></button>
      </div>

      <!-- Quick Preset Selector Pills -->
      <div class="px-4 sm:px-5 py-2.5 border-b shrink-0 flex items-center gap-2 overflow-x-auto no-scrollbar text-xs font-bold" style="background-color: var(--bg-subtle); border-color: var(--border);">
        <span class="txt-muted text-[11px] whitespace-nowrap">Chọn nhanh theo khối:</span>
        <button type="button" onclick="selectSubjectPreset('medical')" class="px-2.5 py-1 rounded-xl bg-indigo-500/10 text-indigo-300 border border-indigo-500/30 hover:bg-indigo-500/20 whitespace-nowrap">
          🩺 Khối Y Dược
        </button>
        <button type="button" onclick="selectSubjectPreset('it')" class="px-2.5 py-1 rounded-xl bg-cyan-500/10 text-cyan-300 border border-cyan-500/30 hover:bg-cyan-500/20 whitespace-nowrap">
          💻 Khối CNTT
        </button>
        <button type="button" onclick="selectSubjectPreset('general')" class="px-2.5 py-1 rounded-xl bg-amber-500/10 text-amber-300 border border-amber-500/30 hover:bg-amber-500/20 whitespace-nowrap">
          📖 Khối Đại Cương
        </button>
        <button type="button" onclick="selectAllSubjects(true)" class="px-2.5 py-1 rounded-xl bg-emerald-500/10 text-emerald-300 border border-emerald-500/30 hover:bg-emerald-500/20 whitespace-nowrap">
          ✨ Chọn Tất Cả (12 môn)
        </button>
        <button type="button" onclick="selectAllSubjects(false)" class="px-2.5 py-1 rounded-xl btn-soft whitespace-nowrap text-rose-400">
          🧹 Bỏ Chọn
        </button>
      </div>

      <!-- Scrollable Checkbox Grid -->
      <div class="p-4 sm:p-5 overflow-y-auto space-y-3 flex-1">
        <div id="acc-subjects-checkbox-grid" class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
          <!-- Populated dynamically via renderAccountSubjectCheckboxes() -->
        </div>
      </div>

      <!-- Modal Footer -->
      <div class="p-4 sm:px-5 py-3 border-t shrink-0 flex items-center justify-between gap-3 flex-wrap" style="border-color: var(--border); background-color: var(--bg-surface);">
        <div class="text-xs font-bold txt-muted flex items-center gap-1.5">
          <span>Đã chọn:</span>
          <span id="acc-subj-selected-count" class="badge-brand px-2 py-0.5 rounded-full text-xs font-mono font-black text-white">0</span>
          <span>/ <span id="acc-subj-total-count">12</span> môn</span>
        </div>
        <div class="flex items-center gap-2">
          <button type="button" onclick="closeModal('modal-account-subjects')" class="btn-soft px-3.5 py-2 text-xs font-bold">
            Hủy
          </button>
          <button type="button" onclick="saveAccountEnrolledSubjects()" class="btn-primary !bg-indigo-600 hover:!bg-indigo-500 px-5 py-2 text-xs font-black flex items-center gap-1.5 shadow-md">
            <span>💾</span> <span>Lưu Môn Học Của Tài Khoản</span>
          </button>
        </div>
      </div>
    </div>
  </div>

  ''' + account_modal_end

if account_modal_end in c and 'id="modal-account-subjects"' not in c:
    c = c.replace(account_modal_end, modal_subjects_html, 1)
    print("1. Added #modal-account-subjects to index.html")
else:
    print("WARNING: account_modal_end not found or modal-account-subjects already present!")

# 2. Add Deep Color Studio into stab-panel-appearance
appearance_end_target = '''            </div>
          </div>
        </div>

        <!-- ==========================================
             TAB 2: CỠ CHỮ & GIÃN DÒNG'''

deep_color_studio_html = '''            </div>
          </div>

          <!-- ===================================================================
               STUDIO TINH CHỈNH MÀU SẮC SÂU & CHI TIẾT TỪNG PHẦN (DEEP COLOR STUDIO)
               =================================================================== -->
          <div class="p-5 rounded-2xl space-y-4 border border-indigo-500/30" style="background: color-mix(in srgb, var(--bg-surface) 96%, transparent);">
            <div class="flex items-center justify-between border-b pb-2.5" style="border-color: var(--border);">
              <div class="flex items-center gap-2">
                <span class="text-xl">🎨</span>
                <div>
                  <h4 class="text-xs font-black txt-main">Studio Tinh Chỉnh Màu Sắc Sâu & Chi Tiết Từng Phần</h4>
                  <p class="text-[10px] txt-muted">Tùy biến màu nền câu hỏi, 4 phương án A-B-C-D, màu đúng/sai và độ tương phản</p>
                </div>
              </div>
              <button type="button" onclick="resetDeepColorCustomization()" class="btn-soft px-2.5 py-1 text-[11px] font-bold text-rose-400 hover:text-rose-300">
                🔄 Đặt Lại Mặc Định
              </button>
            </div>

            <!-- Custom Surface Background Tone -->
            <div class="space-y-2">
              <label class="text-[11px] font-extrabold uppercase tracking-wider txt-sub flex justify-between">
                <span>Màu Nền Thẻ Câu Hỏi & Khung Bài Thi (Surface Tone)</span>
                <span id="lbl-custom-bg" class="txt-brand font-mono font-bold">Mặc định</span>
              </label>
              <div class="flex flex-wrap items-center gap-2">
                <button type="button" onclick="setCustomStageBg('#000000')" class="px-2.5 py-1.5 rounded-xl text-xs font-bold border border-white/20 bg-black text-white">Pure OLED (#000)</button>
                <button type="button" onclick="setCustomStageBg('#0b0f19')" class="px-2.5 py-1.5 rounded-xl text-xs font-bold border border-white/20 bg-[#0b0f19] text-white">Midnight Navy</button>
                <button type="button" onclick="setCustomStageBg('#181824')" class="px-2.5 py-1.5 rounded-xl text-xs font-bold border border-white/20 bg-[#181824] text-white">Deep Indigo</button>
                <button type="button" onclick="setCustomStageBg('#1e293b')" class="px-2.5 py-1.5 rounded-xl text-xs font-bold border border-white/20 bg-[#1e293b] text-white">Slate Dark</button>
                <button type="button" onclick="setCustomStageBg('#fbf0d9')" class="px-2.5 py-1.5 rounded-xl text-xs font-bold border border-amber-900/30 bg-[#fbf0d9] text-amber-950">Kem Sepia</button>
                <button type="button" onclick="setCustomStageBg('#ffffff')" class="px-2.5 py-1.5 rounded-xl text-xs font-bold border border-slate-300 bg-white text-slate-900">Trắng Sáng</button>
                <label class="btn-soft px-2.5 py-1.5 text-xs flex items-center gap-1.5 cursor-pointer">
                  <input type="color" id="picker-custom-bg" oninput="setCustomStageBg(this.value)" class="w-5 h-5 rounded cursor-pointer border-0 bg-transparent" />
                  <span>Chọn Màu Hex</span>
                </label>
              </div>
            </div>

            <!-- Option Styling Mode & Custom Colors -->
            <div class="space-y-2 pt-1 border-t" style="border-color: var(--border);">
              <label class="text-[11px] font-extrabold uppercase tracking-wider txt-sub">Phong Cách Màu 4 Phương Án A - B - C - D</label>
              <div class="grid grid-cols-1 sm:grid-cols-3 gap-2">
                <button type="button" id="opt-style-rainbow" onclick="setOptionColorMode('rainbow')" class="p-2.5 rounded-xl border text-left text-xs font-bold transition-all bg-white/5 border-indigo-500/40">
                  <div class="flex items-center gap-1.5 text-indigo-300 font-black">🌈 Sắc Cầu Vồng</div>
                  <div class="text-[10px] txt-muted mt-0.5">A Tím • B Lam • C Lục • D Hổ phách</div>
                </button>
                <button type="button" id="opt-style-uniform" onclick="setOptionColorMode('uniform')" class="p-2.5 rounded-xl border text-left text-xs font-bold transition-all bg-white/5 border-white/10">
                  <div class="flex items-center gap-1.5 txt-main font-black">🎨 Đồng Bộ Màu Chủ Đề</div>
                  <div class="text-[10px] txt-muted mt-0.5">Theo màu Accent đang chọn</div>
                </button>
                <button type="button" id="opt-style-contrast" onclick="setOptionColorMode('contrast')" class="p-2.5 rounded-xl border text-left text-xs font-bold transition-all bg-white/5 border-white/10">
                  <div class="flex items-center gap-1.5 text-emerald-300 font-black">🔲 Siêu Tương Phản</div>
                  <div class="text-[10px] txt-muted mt-0.5">Viền đậm nét, chống lóa mắt</div>
                </button>
              </div>
            </div>

            <!-- Custom Correct & Wrong Feedback Colors -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-1 border-t" style="border-color: var(--border);">
              <div class="p-3 rounded-xl bg-white/5 border border-white/10 flex items-center justify-between">
                <div>
                  <div class="text-xs font-bold text-emerald-400 flex items-center gap-1"><span>✔</span> Màu Báo Đúng</div>
                  <div class="text-[10px] txt-muted">Khi trả lời chính xác</div>
                </div>
                <label class="flex items-center gap-2 cursor-pointer">
                  <input type="color" id="picker-correct-color" value="#10b981" oninput="setFeedbackCustomColor('correct', this.value)" class="w-8 h-8 rounded-lg cursor-pointer border-0 bg-transparent" />
                </label>
              </div>
              <div class="p-3 rounded-xl bg-white/5 border border-white/10 flex items-center justify-between">
                <div>
                  <div class="text-xs font-bold text-rose-400 flex items-center gap-1"><span>✖</span> Màu Báo Sai</div>
                  <div class="text-[10px] txt-muted">Khi trả lời nhầm</div>
                </div>
                <label class="flex items-center gap-2 cursor-pointer">
                  <input type="color" id="picker-wrong-color" value="#f43f5e" oninput="setFeedbackCustomColor('wrong', this.value)" class="w-8 h-8 rounded-lg cursor-pointer border-0 bg-transparent" />
                </label>
              </div>
            </div>

            <!-- Custom Question Title Color -->
            <div class="p-3 rounded-xl bg-white/5 border border-white/10 flex items-center justify-between">
              <div>
                <div class="text-xs font-bold txt-main flex items-center gap-1.5"><span>🔤</span> Màu Chữ Tiêu Đề Câu Hỏi</div>
                <div class="text-[10px] txt-muted">Tùy biến chữ câu hỏi rõ ràng theo sở thích</div>
              </div>
              <div class="flex items-center gap-1.5">
                <button type="button" onclick="setQuestionTextColor('')" class="btn-soft px-2 py-1 text-[10px]">Tự động</button>
                <button type="button" onclick="setQuestionTextColor('#ffffff')" class="w-6 h-6 rounded-md bg-white border" title="Trắng tinh"></button>
                <button type="button" onclick="setQuestionTextColor('#fef08a')" class="w-6 h-6 rounded-md bg-[#fef08a] border" title="Vàng kem nhẹ"></button>
                <button type="button" onclick="setQuestionTextColor('#a5b4fc')" class="w-6 h-6 rounded-md bg-[#a5b4fc] border" title="Xanh Lavender"></button>
                <input type="color" id="picker-q-text-color" oninput="setQuestionTextColor(this.value)" class="w-7 h-7 rounded cursor-pointer border-0 bg-transparent" />
              </div>
            </div>

            <!-- Global Fast Zoom Presets -->
            <div class="space-y-1.5 pt-1 border-t" style="border-color: var(--border);">
              <label class="text-[11px] font-extrabold uppercase tracking-wider txt-sub">Phóng To Toàn Màn Hình & Cỡ Chữ Nhanh</label>
              <div class="flex flex-wrap items-center gap-2">
                <button type="button" onclick="setGlobalZoomScale(90)" class="zoom-pill px-3 py-1.5 rounded-xl text-xs font-bold btn-soft">90% Nhỏ gọn</button>
                <button type="button" onclick="setGlobalZoomScale(100)" class="zoom-pill px-3 py-1.5 rounded-xl text-xs font-bold btn-soft active">100% Chuẩn</button>
                <button type="button" onclick="setGlobalZoomScale(110)" class="zoom-pill px-3 py-1.5 rounded-xl text-xs font-bold btn-soft">110% Dễ đọc</button>
                <button type="button" onclick="setGlobalZoomScale(120)" class="zoom-pill px-3 py-1.5 rounded-xl text-xs font-bold btn-soft">120% Cỡ To</button>
                <button type="button" onclick="setGlobalZoomScale(130)" class="zoom-pill px-3 py-1.5 rounded-xl text-xs font-bold btn-soft">130% Siêu To</button>
              </div>
            </div>
          </div>
        </div>

        <!-- ==========================================
             TAB 2: CỠ CHỮ & GIÃN DÒNG'''

if appearance_end_target in c and 'STUDIO TINH CHỈNH MÀU SẮC SÂU' not in c:
    c = c.replace(appearance_end_target, deep_color_studio_html, 1)
    print("2. Added Deep Color Studio into stab-panel-appearance")
else:
    print("WARNING: appearance_end_target not found or Deep Color Studio already present!")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(c)

print("Step 2 HTML updates applied successfully!")
