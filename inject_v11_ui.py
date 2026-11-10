# -*- coding: utf-8 -*-
import os
import re

INDEX_PATH = r"C:\Users\PC\.gemini\antigravity\scratch\unimaster-ai\static\index.html"

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add Quick Export button in Desktop Header next to Công thức
export_header_btn = """        <!-- Quick Export Anki & Word Exam Button -->
        <button onclick="switchTab('lab'); switchLabSubTab('export');" title="Xuất Anki Deck & Đề Thi A4 In Ấn"
          class="btn-soft px-2.5 py-2 text-xs flex items-center gap-1.5">
          <span>📥</span>
          <span class="hidden xl:inline">Xuất Anki/In</span>
        </button>
"""
if "switchLabSubTab('export')" not in content:
    target_hdr = '<!-- Quick STEM Formula Sheet Button -->'
    content = content.replace(target_hdr, export_header_btn + "\n        " + target_hdr, 1)

# 2. Add arena-sub-live button if not present
if 'id="arena-sub-live"' not in content:
    target_arena_btn = '<button type="button" onclick="switchArenaSubTab(\'battle\')"'
    live_arena_btn = """<button type="button" onclick="switchArenaSubTab('live')" id="arena-sub-live" class="preset-pill !px-3.5 !py-2 !text-xs bg-gradient-to-r from-amber-500/20 to-rose-500/20 border border-amber-500/40">🔥 Đấu Trường Trực Tiếp (Multiplayer WS)</button>
          """
    content = content.replace(target_arena_btn, live_arena_btn + target_arena_btn, 1)

# 3. Add arena-panel-live
arena_panel_live_html = """
      <!-- SUB-PANEL 4: LIVE WEBSOCKET MULTIPLAYER ARENA -->
      <div id="arena-panel-live" class="hidden space-y-5">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-5">
          <!-- Setup & Lobby Card -->
          <div class="lg:col-span-5 uni-card p-5 space-y-4">
            <div class="flex items-center justify-between">
              <h3 class="text-sm font-extrabold txt-main flex items-center gap-2">
                <span>🔥</span> Đấu Trường Trực Tiếp (Live WebSocket)
              </h3>
              <span id="live-ws-status-badge" class="badge-amber px-2.5 py-0.5 rounded-full text-[11px] font-bold">Chưa kết nối</span>
            </div>
            <p class="text-xs txt-muted">
              Kết nối thời gian thực qua WebSocket. Chủ phòng tạo phòng thi, sinh viên trên điện thoại nhập PIN để cùng đua top tức thì!
            </p>

            <!-- Mode Switch: Host vs Player -->
            <div class="grid grid-cols-2 gap-2 p-1 rounded-xl" style="background: var(--bg-card-sub);">
              <button type="button" id="btn-mode-host" onclick="setLiveArenaMode('host')" class="btn-primary py-2 text-xs font-bold rounded-lg text-center">
                👑 Chủ Phòng (Host)
              </button>
              <button type="button" id="btn-mode-player" onclick="setLiveArenaMode('player')" class="btn-soft py-2 text-xs font-bold rounded-lg text-center">
                📱 Tham Gia (Player)
              </button>
            </div>

            <!-- Host Config Section -->
            <div id="live-host-section" class="space-y-3">
              <div>
                <label class="text-[11px] font-bold txt-sub">Môn thi đấu</label>
                <select id="live-host-subject" class="uni-input w-full px-3 py-2 text-xs font-bold mt-1"></select>
              </div>
              <div>
                <label class="text-[11px] font-bold txt-sub">Số lượng câu hỏi</label>
                <select id="live-host-qcount" class="uni-input w-full px-3 py-2 text-xs font-bold mt-1">
                  <option value="5">5 câu (Đấu tốc độ)</option>
                  <option value="10" selected>10 câu (Tiêu chuẩn)</option>
                  <option value="15">15 câu (Chuyên sâu)</option>
                  <option value="20">20 câu (Toàn diện)</option>
                </select>
              </div>
              <button type="button" onclick="createLiveRoom()" class="btn-primary w-full py-2.5 text-xs font-extrabold flex items-center justify-center gap-2 shadow-lg">
                <span>🚀</span> Tạo Phòng Thi Đấu Trực Tiếp
              </button>
            </div>

            <!-- Player Join Section -->
            <div id="live-player-section" class="hidden space-y-3">
              <div>
                <label class="text-[11px] font-bold txt-sub">Mã Phòng (PIN gồm 4 chữ số)</label>
                <input id="live-player-roomcode" type="text" maxlength="6" placeholder="VD: 5821" class="uni-input w-full px-3 py-2.5 text-center text-lg font-mono font-extrabold tracking-widest mt-1" />
              </div>
              <div>
                <label class="text-[11px] font-bold txt-sub">Biệt danh / Tên hiển thị</label>
                <input id="live-player-name" type="text" maxlength="20" placeholder="VD: BS. Minh Tuấn" class="uni-input w-full px-3 py-2 text-xs font-bold mt-1" />
              </div>
              <button type="button" onclick="joinLiveRoom()" class="btn-primary w-full py-2.5 text-xs font-extrabold flex items-center justify-center gap-2 shadow-lg">
                <span>⚡</span> Vào Phòng Đấu Ngay
              </button>
            </div>

            <!-- Lobby Status Box (when in a room) -->
            <div id="live-lobby-box" class="hidden p-4 rounded-xl space-y-3" style="background: var(--bg-card-sub); border: 1px solid var(--border);">
              <div class="flex items-center justify-between">
                <div>
                  <div class="text-[11px] uppercase tracking-wider txt-muted font-bold">Mã phòng thi</div>
                  <div id="live-display-roomcode" class="text-2xl font-black font-mono text-emerald-400">----</div>
                </div>
                <button type="button" onclick="leaveLiveRoom()" class="btn-soft px-2.5 py-1 text-xs text-rose-400 font-bold">Rời phòng</button>
              </div>
              <div>
                <div class="text-xs font-bold txt-sub mb-2 flex items-center justify-between">
                  <span>Người chơi trong phòng:</span>
                  <span id="live-player-count" class="badge-brand px-2 py-0.5 rounded text-[10px]">0</span>
                </div>
                <div id="live-player-list" class="flex flex-wrap gap-1.5 max-h-32 overflow-y-auto"></div>
              </div>
              <button id="live-btn-start" type="button" onclick="startLiveGame()" class="hidden btn-primary w-full py-2 text-xs font-extrabold bg-gradient-to-r from-emerald-500 to-teal-600">
                🏁 Bắt Đầu Trận Đấu (Host)
              </button>
            </div>
          </div>

          <!-- Live Battle Stage & Question Card -->
          <div class="lg:col-span-7 uni-card p-5 space-y-4">
            <!-- Game Inactive Placeholder -->
            <div id="live-stage-idle" class="py-16 text-center space-y-3">
              <div class="text-5xl animate-bounce">⚔️</div>
              <h4 class="text-base font-extrabold txt-main">Đấu Trường Trực Tiếp Sẵn Sàng</h4>
              <p class="text-xs txt-muted max-w-sm mx-auto">
                Tạo mã phòng hoặc nhập mã phòng của bạn bè để bắt đầu trận đấu trắc nghiệm thời gian thực!
              </p>
            </div>

            <!-- Game Active Screen -->
            <div id="live-stage-active" class="hidden space-y-4">
              <!-- Top Live Header: Question Index + Timer Bar -->
              <div class="flex items-center justify-between">
                <span id="live-q-badge" class="badge-brand px-3 py-1 rounded-full text-xs font-extrabold">Câu 1 / 10</span>
                <div class="flex items-center gap-2">
                  <span class="text-xs font-bold txt-muted">⏱️ Còn lại:</span>
                  <span id="live-timer-val" class="text-sm font-mono font-black text-amber-400">15s</span>
                </div>
              </div>
              <!-- Timer Progress Bar -->
              <div class="w-full h-2 rounded-full overflow-hidden" style="background: var(--bg-card-sub);">
                <div id="live-timer-bar" class="h-full bg-gradient-to-r from-emerald-400 to-amber-400 transition-all duration-300" style="width: 100%;"></div>
              </div>

              <!-- Question Display -->
              <div class="p-4 rounded-xl" style="background: var(--bg-card-sub); border: 1px solid var(--border);">
                <h4 id="live-question-text" class="text-sm sm:text-base font-bold txt-main leading-relaxed">Đang tải câu hỏi...</h4>
                <div id="live-question-img-wrap" class="hidden mt-3 text-center">
                  <img id="live-question-img" src="" class="max-h-48 mx-auto rounded-lg border" />
                </div>
              </div>

              <!-- 4 Interactive Option Buttons -->
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <button type="button" onclick="submitLiveBuzzer('A')" id="live-opt-A" class="uni-card p-3.5 text-left text-xs font-bold hover:border-violet-500 transition-all flex items-start gap-2.5">
                  <span class="w-6 h-6 rounded-lg bg-violet-500/20 text-violet-400 flex items-center justify-center font-black shrink-0">A</span>
                  <span id="live-text-A">--</span>
                </button>
                <button type="button" onclick="submitLiveBuzzer('B')" id="live-opt-B" class="uni-card p-3.5 text-left text-xs font-bold hover:border-violet-500 transition-all flex items-start gap-2.5">
                  <span class="w-6 h-6 rounded-lg bg-blue-500/20 text-blue-400 flex items-center justify-center font-black shrink-0">B</span>
                  <span id="live-text-B">--</span>
                </button>
                <button type="button" onclick="submitLiveBuzzer('C')" id="live-opt-C" class="uni-card p-3.5 text-left text-xs font-bold hover:border-violet-500 transition-all flex items-start gap-2.5">
                  <span class="w-6 h-6 rounded-lg bg-amber-500/20 text-amber-400 flex items-center justify-center font-black shrink-0">C</span>
                  <span id="live-text-C">--</span>
                </button>
                <button type="button" onclick="submitLiveBuzzer('D')" id="live-opt-D" class="uni-card p-3.5 text-left text-xs font-bold hover:border-violet-500 transition-all flex items-start gap-2.5">
                  <span class="w-6 h-6 rounded-lg bg-emerald-500/20 text-emerald-400 flex items-center justify-center font-black shrink-0">D</span>
                  <span id="live-text-D">--</span>
                </button>
              </div>

              <!-- Instant Feedback Banner -->
              <div id="live-feedback-box" class="hidden p-3.5 rounded-xl text-xs space-y-1.5 animate-fade-in"></div>

              <!-- Host Control: Next Question Button -->
              <div id="live-host-controls" class="hidden pt-2 flex justify-end">
                <button type="button" onclick="hostNextQuestion()" class="btn-primary px-4 py-2 text-xs font-bold flex items-center gap-1.5">
                  <span>➡️</span> Câu Tiếp Theo
                </button>
              </div>
            </div>

            <!-- Game Over / Podium Screen -->
            <div id="live-stage-podium" class="hidden py-8 text-center space-y-4">
              <div class="text-4xl">🏆</div>
              <h3 class="text-lg font-black text-amber-400">KẾT THÚC TRẬN ĐẤU! BẢNG VINH DANH</h3>
              <div id="live-podium-list" class="max-w-md mx-auto space-y-2"></div>
              <button type="button" onclick="resetLiveArena()" class="btn-primary px-5 py-2 text-xs font-bold">
                🔄 Quay Lại Sảnh Đấu
              </button>
            </div>
          </div>
        </div>
      </div>
"""
if 'id="arena-panel-live"' not in content:
    # Insert right before the closing tag of section id="view-arena"
    arena_close = re.search(r'(<div id="arena-badges-grid"[^>]*>.*?</div>\s*</div>\s*</div>\s*</div>\s*)(</section>)', content, re.DOTALL)
    if arena_close:
        content = content[:arena_close.start(2)] + arena_panel_live_html + "\n    " + content[arena_close.start(2):]
    else:
        print("Warning: arena_close not found by regex")

# 4. Add sub-tab buttons in view-lab header
lab_subtab_btns = """            <button type="button" onclick="switchLabSubTab('patient')" data-labtab="patient" class="preset-pill text-xs">
              🩺 6. Bệnh Nhân Ảo Đa Bước
            </button>
            <button type="button" onclick="switchLabSubTab('dosing')" data-labtab="dosing" class="preset-pill text-xs">
              💊 7. Dược Lý & Liều Thận
            </button>
            <button type="button" onclick="switchLabSubTab('biostat')" data-labtab="biostat" class="preset-pill text-xs">
              📊 8. Thống Kê Y Sinh
            </button>
            <button type="button" onclick="switchLabSubTab('export')" data-labtab="export" class="preset-pill text-xs">
              📥 9. Xuất Anki & In Đề A4
            </button>
"""
if "data-labtab=\"patient\"" not in content:
    target_calc_btn = '🧮 5. Máy Tính Y Khoa & Thực Hành\n            </button>'
    if target_calc_btn in content:
        content = content.replace(target_calc_btn, target_calc_btn + "\n" + lab_subtab_btns, 1)
    else:
        # Try with CRLF
        target_calc_btn_crlf = '🧮 5. Máy Tính Y Khoa & Thực Hành\r\n            </button>'
        content = content.replace(target_calc_btn_crlf, target_calc_btn_crlf + "\r\n" + lab_subtab_btns.replace("\n", "\r\n"), 1)

# 5. Add 4 sub-modules to view-lab: lab-sub-patient, lab-sub-dosing, lab-sub-biostat, lab-sub-export
lab_sub_modules_html = """
      <!-- SUB-MODULE 6: VIRTUAL PATIENT / CLINICAL CASE SIMULATOR -->
      <div id="lab-sub-patient" class="hidden space-y-5">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-5">
          <!-- Case Info & Timeline Navigation -->
          <div class="lg:col-span-5 uni-card p-5 space-y-4">
            <div class="flex items-center justify-between">
              <h3 class="text-sm font-extrabold txt-main flex items-center gap-2">
                <span>🩺</span> Bệnh Nhân Ảo Lâm Sàng Đa Bước
              </h3>
              <span id="vp-badge" class="badge-brand px-2.5 py-0.5 rounded-full text-[11px] font-bold">5 Bước Ra Quyết Định</span>
            </div>
            
            <div>
              <label class="text-[11px] font-extrabold uppercase txt-muted">Chọn bệnh án thực hành</label>
              <select id="vp-case-select" onchange="onVirtualCaseSelect()" class="uni-input w-full px-3 py-2 text-xs font-bold mt-1">
                <option value="case_nephrotic_01">Ca 1: Hội chứng thận hư nguyên phát ở người trẻ</option>
                <option value="case_gout_02">Ca 2: Cơn Gout cấp trên nền suy thận mạn do tăng acid uric</option>
              </select>
            </div>

            <!-- Patient Profile Card -->
            <div id="vp-patient-card" class="p-4 rounded-xl space-y-2.5" style="background: var(--bg-card-sub); border: 1px solid var(--border);">
              <div class="flex items-center justify-between">
                <div class="font-black text-sm text-cyan-400" id="vp-p-name">Nguyễn Văn A</div>
                <div class="badge-amber px-2 py-0.5 rounded text-[10px] font-bold" id="vp-p-age">24 tuổi • Nam</div>
              </div>
              <div class="text-xs text-rose-400 font-extrabold" id="vp-p-cc">Lý do vào viện: Phù 2 chân và mí mắt</div>
              <div class="text-[11px] txt-muted line-clamp-3" id="vp-p-history">Bệnh sử tóm tắt...</div>
              <!-- Vitals -->
              <div class="grid grid-cols-4 gap-1.5 pt-2 text-center text-[10px]">
                <div class="p-1 rounded bg-black/20"><div class="txt-muted">Huyết áp</div><div class="font-mono font-bold text-emerald-400" id="vp-v-bp">120/80</div></div>
                <div class="p-1 rounded bg-black/20"><div class="txt-muted">Mạch</div><div class="font-mono font-bold text-amber-400" id="vp-v-hr">82 l/p</div></div>
                <div class="p-1 rounded bg-black/20"><div class="txt-muted">Nhiệt độ</div><div class="font-mono font-bold text-blue-400" id="vp-v-temp">37.0°C</div></div>
                <div class="p-1 rounded bg-black/20"><div class="txt-muted">SpO2</div><div class="font-mono font-bold text-violet-400" id="vp-v-spo2">98%</div></div>
              </div>
            </div>

            <!-- 5 Steps Stepper Navigation -->
            <div class="space-y-1.5">
              <label class="text-[11px] font-bold txt-sub">Lộ trình ra quyết định lâm sàng:</label>
              <div class="grid grid-cols-5 gap-1 text-center">
                <button type="button" onclick="setVirtualStep(0)" id="vp-step-btn-0" class="btn-primary py-2 text-[10px] font-black rounded-lg">1. Bệnh sử</button>
                <button type="button" onclick="setVirtualStep(1)" id="vp-step-btn-1" class="btn-soft py-2 text-[10px] font-black rounded-lg">2. Khám</button>
                <button type="button" onclick="setVirtualStep(2)" id="vp-step-btn-2" class="btn-soft py-2 text-[10px] font-black rounded-lg">3. Cận LS</button>
                <button type="button" onclick="setVirtualStep(3)" id="vp-step-btn-3" class="btn-soft py-2 text-[10px] font-black rounded-lg">4. C.Đoán</button>
                <button type="button" onclick="setVirtualStep(4)" id="vp-step-btn-4" class="btn-soft py-2 text-[10px] font-black rounded-lg">5. Đ.Trị</button>
              </div>
            </div>
          </div>

          <!-- Step Interaction Arena -->
          <div class="lg:col-span-7 uni-card p-5 space-y-4">
            <div class="flex items-center justify-between">
              <h4 id="vp-step-title" class="text-sm sm:text-base font-extrabold txt-main">Bước 1: Khai thác bệnh sử & Tiền căn</h4>
              <span id="vp-score-pill" class="badge-amber px-2.5 py-0.5 rounded-full text-[11px] font-bold">Điểm phản xạ: --/100</span>
            </div>

            <!-- Step Content Container -->
            <div id="vp-step-body" class="p-4 rounded-xl space-y-4" style="background: var(--bg-card-sub); border: 1px solid var(--border);">
              <!-- Rendered dynamically -->
            </div>

            <!-- Navigation Buttons between steps -->
            <div class="flex items-center justify-between pt-2">
              <button type="button" onclick="prevVirtualStep()" id="vp-btn-prev" class="btn-soft px-4 py-2 text-xs font-bold flex items-center gap-1.5">
                <span>⬅️</span> Bước Trước
              </button>
              <button type="button" onclick="nextVirtualStep()" id="vp-btn-next" class="btn-primary px-4 py-2 text-xs font-bold flex items-center gap-1.5">
                <span>Bước Tiếp</span> <span>➡️</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- SUB-MODULE 7: CLINICAL PHARMACOLOGY & RENAL DOSING CALCULATOR -->
      <div id="lab-sub-dosing" class="hidden space-y-5">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-5">
          <!-- Left: Patient Profile Input & Renal Function -->
          <div class="lg:col-span-5 uni-card p-5 space-y-4">
            <div class="flex items-center justify-between">
              <h3 class="text-sm font-extrabold txt-main flex items-center gap-2">
                <span>💊</span> Dược Lý & Hiệu Chỉnh Liều Thận
              </h3>
              <span class="badge-brand px-2.5 py-0.5 rounded-full text-[11px] font-bold">CrCl & eGFR</span>
            </div>
            <p class="text-xs txt-muted">
              Tra cứu nomogram hiệu chỉnh liều theo thanh thải Creatinin (Cockcroft-Gault & CKD-EPI) cho bệnh nhân suy giảm chức năng thận.
            </p>

            <div class="space-y-3">
              <div>
                <label class="text-[11px] font-bold txt-sub">Chọn thuốc cần hiệu chỉnh</label>
                <select id="dose-drug-select" onchange="onDoseDrugChange()" class="uni-input w-full px-3 py-2 text-xs font-bold mt-1">
                  <option value="vancomycin">Vancomycin (Kháng sinh Glycopeptid)</option>
                  <option value="ciprofloxacin">Ciprofloxacin (Kháng sinh Fluoroquinolon)</option>
                  <option value="meropenem">Meropenem (Kháng sinh Carbapenem)</option>
                  <option value="gentamicin">Gentamicin (Kháng sinh Aminoglycosid)</option>
                  <option value="allopurinol">Allopurinol (Ức chế Xanthine Oxidase)</option>
                  <option value="enalapril">Enalapril (Ức chế men chuyển ACEi)</option>
                  <option value="metformin">Metformin (Biguanid hạ đường huyết)</option>
                </select>
              </div>

              <div class="grid grid-cols-2 gap-3">
                <div>
                  <label class="text-[11px] font-bold txt-sub">Tuổi bệnh nhân</label>
                  <input id="dose-patient-age" type="number" value="62" min="18" max="110" oninput="runRenalDoseCalculation()" class="uni-input w-full px-3 py-2 text-xs font-mono font-bold mt-1" />
                </div>
                <div>
                  <label class="text-[11px] font-bold txt-sub">Cân nặng (kg)</label>
                  <input id="dose-patient-wt" type="number" value="60" min="30" max="200" oninput="runRenalDoseCalculation()" class="uni-input w-full px-3 py-2 text-xs font-mono font-bold mt-1" />
                </div>
              </div>

              <div class="grid grid-cols-2 gap-3">
                <div>
                  <label class="text-[11px] font-bold txt-sub">Giới tính</label>
                  <select id="dose-patient-gender" onchange="runRenalDoseCalculation()" class="uni-input w-full px-3 py-2 text-xs font-bold mt-1">
                    <option value="male">Nam (x 1.00)</option>
                    <option value="female">Nữ (x 0.85)</option>
                  </select>
                </div>
                <div>
                  <label class="text-[11px] font-bold txt-sub">Creatinin máu (mg/dL)</label>
                  <input id="dose-patient-scr" type="number" step="0.1" value="2.1" min="0.3" max="25" oninput="runRenalDoseCalculation()" class="uni-input w-full px-3 py-2 text-xs font-mono font-bold mt-1" />
                </div>
              </div>
            </div>

            <!-- Real-time Renal Function Badges -->
            <div class="p-3.5 rounded-xl space-y-2" style="background: var(--bg-card-sub); border: 1px solid var(--border);">
              <div class="flex items-center justify-between text-xs">
                <span class="txt-muted">Cockcroft-Gault CrCl:</span>
                <span id="dose-calc-crcl" class="font-mono font-black text-rose-400">26.3 ml/phút</span>
              </div>
              <div class="flex items-center justify-between text-xs">
                <span class="txt-muted">Phân độ suy thận KDIGO:</span>
                <span id="dose-calc-kdigo" class="badge-rose px-2 py-0.5 rounded text-[10px] font-bold">G4 (Nặng: 15-29)</span>
              </div>
            </div>
          </div>

          <!-- Right: Drug Dosing Recommendation Card -->
          <div class="lg:col-span-7 uni-card p-5 space-y-4">
            <div class="flex items-center justify-between">
              <div>
                <h4 id="dose-drug-title" class="text-base font-extrabold text-cyan-400">Vancomycin</h4>
                <div id="dose-drug-group" class="text-xs txt-muted">Kháng sinh Glycopeptid</div>
              </div>
              <span class="badge-brand px-2.5 py-1 rounded-lg text-xs font-mono font-extrabold">Dược thư Quốc gia</span>
            </div>

            <!-- Standard Normal Dose -->
            <div class="p-3.5 rounded-xl text-xs space-y-1" style="background: var(--bg-card-sub); border: 1px solid var(--border);">
              <div class="font-bold txt-sub">📋 Liều chuẩn ở người có chức năng thận bình thường (CrCl ≥ 50 ml/p):</div>
              <div id="dose-std-text" class="text-xs font-mono font-bold txt-main">15 – 20 mg/kg mỗi 8 – 12 giờ (truyền IV chậm)</div>
            </div>

            <!-- Tailored Adjusted Dose (Key Output) -->
            <div class="p-4 rounded-xl text-xs space-y-2 border-2 border-emerald-500/50 bg-emerald-500/10">
              <div class="flex items-center justify-between">
                <span class="font-black text-emerald-400 uppercase tracking-wide">🎯 Khuyến cáo hiệu chỉnh liều cho ca này:</span>
                <span id="dose-adj-crcl-badge" class="badge-amber px-2 py-0.5 rounded text-[10px] font-bold">CrCl = 26.3 ml/p</span>
              </div>
              <div id="dose-adjusted-recommendation" class="text-sm font-extrabold text-white leading-relaxed">
                CrCl 20 – 49 ml/phút: 15 mg/kg mỗi 24 – 48 giờ.
              </div>
            </div>

            <!-- Dialysis / HD Dose -->
            <div class="p-3.5 rounded-xl text-xs space-y-1" style="background: var(--bg-card-sub); border: 1px solid var(--border);">
              <div class="font-bold text-amber-400">🩸 Liều lọc máu nhân tạo chu kỳ (Hemodialysis):</div>
              <div id="dose-hd-text" class="txt-main">Liều nạp 15 – 25 mg/kg, bổ sung 500 – 1000 mg sau mỗi lần lọc máu.</div>
            </div>

            <!-- Black Box Warning -->
            <div class="p-3.5 rounded-xl text-xs space-y-1 border border-rose-500/40 bg-rose-500/10">
              <div class="font-bold text-rose-400">⚠️ Cảnh báo an toàn dược lâm sàng:</div>
              <div id="dose-warning-text" class="txt-main">Độc tính cao trên tai và thận! Tuyệt đối không truyền nhanh...</div>
            </div>
          </div>
        </div>
      </div>

      <!-- SUB-MODULE 8: BIOSTATISTICS & RESEARCH LAB -->
      <div id="lab-sub-biostat" class="hidden space-y-5">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-5">
          <!-- 2x2 Contingency Table Input -->
          <div class="lg:col-span-6 uni-card p-5 space-y-4">
            <div class="flex items-center justify-between">
              <h3 class="text-sm font-extrabold txt-main flex items-center gap-2">
                <span>📊</span> Bảng 2x2 Tiếp Liên & Đánh Giá Nghiệm Pháp
              </h3>
              <span class="badge-brand px-2.5 py-0.5 rounded-full text-[11px] font-bold">Se, Sp, PPV, NPV, OR, RR</span>
            </div>
            <p class="text-xs txt-muted">
              Nhập số liệu nghiên cứu dịch tễ & y sinh để tự động tính độ nhạy, độ đặc hiệu, tỷ số chênh Odds Ratio (95% CI) và Chi-Square.
            </p>

            <!-- 2x2 Grid -->
            <div class="p-4 rounded-xl space-y-3" style="background: var(--bg-card-sub); border: 1px solid var(--border);">
              <div class="grid grid-cols-3 gap-2 text-center text-xs font-bold">
                <div></div>
                <div class="p-1 rounded bg-rose-500/20 text-rose-400">Bệnh (+)</div>
                <div class="p-1 rounded bg-emerald-500/20 text-emerald-400">Không bệnh (-)</div>
              </div>
              <div class="grid grid-cols-3 gap-2 items-center">
                <div class="text-xs font-bold text-violet-400">XN / Phơi nhiễm (+)</div>
                <input id="bio-a" type="number" value="85" min="0" oninput="runBiostatCalculations()" class="uni-input px-3 py-2 text-center font-mono font-bold text-xs" title="True Positive (a)" />
                <input id="bio-b" type="number" value="15" min="0" oninput="runBiostatCalculations()" class="uni-input px-3 py-2 text-center font-mono font-bold text-xs" title="False Positive (b)" />
              </div>
              <div class="grid grid-cols-3 gap-2 items-center">
                <div class="text-xs font-bold text-zinc-400">XN / Phơi nhiễm (-)</div>
                <input id="bio-c" type="number" value="12" min="0" oninput="runBiostatCalculations()" class="uni-input px-3 py-2 text-center font-mono font-bold text-xs" title="False Negative (c)" />
                <input id="bio-d" type="number" value="188" min="0" oninput="runBiostatCalculations()" class="uni-input px-3 py-2 text-center font-mono font-bold text-xs" title="True Negative (d)" />
              </div>
            </div>

            <!-- Quick Preset Buttons -->
            <div class="flex gap-2">
              <button type="button" onclick="loadBiostatPreset('troponin')" class="btn-soft px-3 py-1.5 text-xs font-bold">Xét nghiệm Troponin T</button>
              <button type="button" onclick="loadBiostatPreset('hba1c')" class="btn-soft px-3 py-1.5 text-xs font-bold">Sàng lọc HbA1c</button>
              <button type="button" onclick="loadBiostatPreset('covid')" class="btn-soft px-3 py-1.5 text-xs font-bold">Test nhanh Kháng nguyên</button>
            </div>
          </div>

          <!-- Calculated Biostatistical Metrics -->
          <div class="lg:col-span-6 uni-card p-5 space-y-4">
            <h4 class="text-sm font-extrabold txt-main flex items-center gap-2">
              <span>🎯</span> Kết Quả Thống Kê & Ý Nghĩa Nghiên Cứu
            </h4>

            <div class="grid grid-cols-2 gap-3">
              <div class="p-3 rounded-xl bg-violet-500/10 border border-violet-500/20">
                <div class="text-[11px] font-bold text-violet-400">Độ nhạy (Sensitivity):</div>
                <div id="bio-res-se" class="text-lg font-mono font-black text-violet-300">87.6%</div>
                <div class="text-[10px] txt-muted mt-0.5">Khả năng phát hiện đúng người có bệnh</div>
              </div>
              <div class="p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/20">
                <div class="text-[11px] font-bold text-emerald-400">Độ đặc hiệu (Specificity):</div>
                <div id="bio-res-sp" class="text-lg font-mono font-black text-emerald-300">92.6%</div>
                <div class="text-[10px] txt-muted mt-0.5">Khả năng loại trừ người khỏe mạnh</div>
              </div>
              <div class="p-3 rounded-xl bg-cyan-500/10 border border-cyan-500/20">
                <div class="text-[11px] font-bold text-cyan-400">Giá trị tiên đoán dương (PPV):</div>
                <div id="bio-res-ppv" class="text-lg font-mono font-black text-cyan-300">85.0%</div>
                <div class="text-[10px] txt-muted mt-0.5">Xác suất mắc bệnh khi XN dương tính</div>
              </div>
              <div class="p-3 rounded-xl bg-amber-500/10 border border-amber-500/20">
                <div class="text-[11px] font-bold text-amber-400">Tỷ số chênh Odds Ratio (OR):</div>
                <div id="bio-res-or" class="text-lg font-mono font-black text-amber-300">88.78</div>
                <div id="bio-res-ci" class="text-[10px] txt-muted mt-0.5">95% CI: 41.2 – 191.1</div>
              </div>
            </div>

            <div class="p-3.5 rounded-xl text-xs space-y-1.5" style="background: var(--bg-card-sub); border: 1px solid var(--border);">
              <div class="flex items-center justify-between">
                <span class="font-bold txt-sub">Kiểm định Khi bình phương (Chi-square):</span>
                <span id="bio-res-chi2" class="font-mono font-bold text-emerald-400">χ² = 194.25</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="font-bold txt-sub">Mức ý nghĩa thống kê (p-value):</span>
                <span id="bio-res-p" class="font-mono font-bold text-emerald-400">p < 0.001 (Rất có ý nghĩa)</span>
              </div>
            </div>

            <!-- Vancouver Citation Quick Tool -->
            <div class="pt-2 border-t" style="border-color: var(--border);">
              <div class="text-xs font-bold txt-main mb-1.5 flex items-center justify-between">
                <span>📚 Trích Dẫn Chuẩn Vancouver (Y Học Quốc Tế / CTUMP):</span>
                <button type="button" onclick="copyVancouverCitation()" class="btn-soft px-2 py-0.5 text-[10px] font-bold">📋 Sao chép</button>
              </div>
              <div id="bio-vancouver-preview" class="p-2.5 rounded-lg text-[11px] font-mono txt-sub" style="background: var(--bg-card-sub);">
                Nguyen VA, Tran BT. Biochemical markers in kidney diseases. Can Tho J Med Pharm. 2026;12(3):45-52.
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- SUB-MODULE 9: EXPORT ANKI & PRINTABLE A4 WORD EXAM -->
      <div id="lab-sub-export" class="hidden space-y-5">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-5">
          <!-- Selection & Configuration -->
          <div class="lg:col-span-5 uni-card p-5 space-y-4">
            <div class="flex items-center justify-between">
              <h3 class="text-sm font-extrabold txt-main flex items-center gap-2">
                <span>📥</span> Trung Tâm Xuất Anki Deck & Đề Thi A4
              </h3>
              <span class="badge-brand px-2.5 py-0.5 rounded-full text-[11px] font-bold">1-Click Tải Về</span>
            </div>
            <p class="text-xs txt-muted">
              Chuyển đổi toàn bộ ngân hàng câu hỏi trắc nghiệm thành bộ thẻ nhớ Anki trên điện thoại hoặc file Word in ấn chuẩn Bộ GD.
            </p>

            <div>
              <label class="text-[11px] font-bold txt-sub">Chọn môn học cần xuất</label>
              <select id="export-subject-select" class="uni-input w-full px-3 py-2 text-xs font-bold mt-1"></select>
            </div>

            <div>
              <label class="text-[11px] font-bold txt-sub">Số lượng câu hỏi (dành cho đề thi in ấn)</label>
              <select id="export-exam-limit" class="uni-input w-full px-3 py-2 text-xs font-bold mt-1">
                <option value="20">20 câu (Kiểm tra 15-30 phút)</option>
                <option value="40" selected>40 câu (Thi giữa kỳ 45 phút)</option>
                <option value="60">60 câu (Thi kết thúc học phần 60 phút)</option>
                <option value="100">100 câu (Đề tổng hợp ôn tập)</option>
              </select>
            </div>
          </div>

          <!-- 2 Export Options Cards -->
          <div class="lg:col-span-7 grid grid-cols-1 sm:grid-cols-2 gap-4">
            <!-- Anki Deck Card -->
            <div class="uni-card p-5 space-y-3 flex flex-col justify-between border-2 border-violet-500/40 bg-violet-500/5">
              <div class="space-y-2">
                <div class="w-10 h-10 rounded-xl bg-violet-500/20 text-violet-400 flex items-center justify-center text-xl font-black">🎴</div>
                <h4 class="text-sm font-extrabold txt-main">Xuất Thẻ Nhớ Anki Deck (.txt / TSV)</h4>
                <p class="text-xs txt-muted">
                  Định dạng chuẩn Anki UTF-8 (HTML tabs, công thức KaTeX & hình ảnh). Nhập 1-click vào app Anki Mobile (iOS/Android) hoặc Anki PC.
                </p>
                <div class="text-[11px] text-emerald-400 font-bold">✅ Hỗ trợ đầy đủ 522+ câu Hóa Sinh CTUMP</div>
              </div>
              <button type="button" onclick="downloadAnkiDeck()" class="btn-primary w-full py-2.5 text-xs font-extrabold flex items-center justify-center gap-2">
                <span>⬇️</span> Tải File Anki Deck (.txt)
              </button>
            </div>

            <!-- Printable Word Exam Card -->
            <div class="uni-card p-5 space-y-3 flex flex-col justify-between border-2 border-cyan-500/40 bg-cyan-500/5">
              <div class="space-y-2">
                <div class="w-10 h-10 rounded-xl bg-cyan-500/20 text-cyan-400 flex items-center justify-center text-xl font-black">📄</div>
                <h4 class="text-sm font-extrabold txt-main">Đề Thi In Ấn Chuẩn Bộ GD (.doc)</h4>
                <p class="text-xs txt-muted">
                  Định dạng văn bản Word A4 chuẩn Khoa Y ĐH Y Dược Cần Thơ: Tiêu đề Quốc hiệu, 2 cột chữ rõ đẹp, bảng đáp án riêng ở trang cuối.
                </p>
                <div class="text-[11px] text-cyan-400 font-bold">✅ Mở và in trực tiếp bằng Microsoft Word</div>
              </div>
              <button type="button" onclick="downloadWordExam()" class="btn-primary w-full py-2.5 text-xs font-extrabold bg-gradient-to-r from-cyan-500 to-blue-600 flex items-center justify-center gap-2">
                <span>🖨️</span> Tải Đề Thi Word (.doc)
              </button>
            </div>
          </div>
        </div>
      </div>
"""
if 'id="lab-sub-patient"' not in content:
    # Insert right before the closing tag of section id="view-lab"
    lab_close = re.search(r'(<div id="calc-ldl-output"[^>]*>.*?</div>\s*</div>\s*</div>\s*</div>\s*)(</section>)', content, re.DOTALL)
    if lab_close:
        content = content[:lab_close.start(2)] + lab_sub_modules_html + "\n    " + content[lab_close.start(2):]
    else:
        print("Warning: lab_close not found by regex")

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("Injected UI sections successfully! New length:", len(content))
