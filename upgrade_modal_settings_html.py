import re

html_path = r'C:\Users\PC\.gemini\antigravity\scratch\unimaster-ai\static\index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Pattern matching modal-settings from comment to before modal-add-subject
pattern = r'<!-- =+\s*MODAL 2: CENTRAL SETTINGS.*?(?=<!-- Modal: Add Subject -->)'

new_modal_settings = """<!-- =====================================================================
       MODAL 2: CENTRAL SETTINGS & PERSONALIZATION HUB (LUXURY PRO SUITE)
       ===================================================================== -->
  <div id="modal-settings" class="hidden fixed inset-0 z-50 modal-overlay flex items-center justify-center p-2.5 sm:p-4">
    <div class="uni-card w-full max-w-4xl h-[88vh] max-h-[850px] flex flex-col overflow-hidden animate-fade-in shadow-2xl">
      <!-- Modal Header (Fixed, never squeezed) -->
      <div class="px-5 py-3.5 shrink-0 flex items-center justify-between border-b" style="border-color: var(--border); background-color: var(--bg-surface);">
        <div class="flex items-center gap-2.5">
          <div class="w-8 h-8 rounded-xl flex items-center justify-center text-white text-sm shadow-sm shrink-0" style="background: linear-gradient(135deg, var(--brand), var(--brand-2));">
            ⚙️
          </div>
          <div>
            <h3 class="text-base font-extrabold txt-main flex items-center gap-2">
              Trung Tâm Cài Đặt & Cá Nhân Hóa
            </h3>
            <div class="text-[11px] txt-muted font-medium">Tự do điều chỉnh giao diện, phông chữ, âm thanh, AI và chống gian lận theo ý bạn</div>
          </div>
        </div>
        <button onclick="closeModal('modal-settings')" class="btn-soft p-1.5" title="Đóng cài đặt"><i data-lucide="x" class="w-4 h-4"></i></button>
      </div>

      <!-- Settings Sub-Tabs (Clean Segmented Nav, Never Squeezed) -->
      <div class="px-4 py-2.5 shrink-0 flex items-center gap-1.5 overflow-x-auto no-scrollbar border-b" style="border-color: var(--border); background-color: var(--bg-subtle);">
        <button type="button" onclick="switchSettingsTab('appearance')" data-stab="appearance" class="settings-tab-btn active px-3.5 py-2 rounded-xl text-xs font-bold whitespace-nowrap transition-all flex items-center gap-1.5">
          <span>🎨</span> <span>Giao diện & Màu sắc</span>
        </button>
        <button type="button" onclick="switchSettingsTab('typography')" data-stab="typography" class="settings-tab-btn px-3.5 py-2 rounded-xl text-xs font-bold whitespace-nowrap transition-all flex items-center gap-1.5">
          <span>🔤</span> <span>Cỡ Chữ & Giãn Dòng</span>
        </button>
        <button type="button" onclick="switchSettingsTab('ai')" data-stab="ai" class="settings-tab-btn px-3.5 py-2 rounded-xl text-xs font-bold whitespace-nowrap transition-all flex items-center gap-1.5">
          <span>⚡</span> <span>AI: ChatGPT & Gemini</span>
        </button>
        <button type="button" onclick="switchSettingsTab('tools')" data-stab="tools" class="settings-tab-btn px-3.5 py-2 rounded-xl text-xs font-bold whitespace-nowrap transition-all flex items-center gap-1.5">
          <span>⏱️</span> <span>Âm thanh & Đồng hồ</span>
        </button>
        <button type="button" onclick="switchSettingsTab('sync')" data-stab="sync" class="settings-tab-btn px-3.5 py-2 rounded-xl text-xs font-bold whitespace-nowrap transition-all flex items-center gap-1.5">
          <span>🛡️</span> <span>Chống Gian Lận & Đồng Bộ</span>
        </button>
      </div>

      <!-- Settings Body (Smooth Scroll, Roomy, Never Overlapping) -->
      <div class="p-5 sm:p-7 overflow-y-auto space-y-6 flex-1">

        <!-- ==========================================
             TAB 1: GIAO DIỆN & MÀU SẮC
             ========================================== -->
        <div id="stab-panel-appearance" class="space-y-6">
          <!-- Surface Theme -->
          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <label class="text-xs font-extrabold uppercase tracking-wider txt-muted">1. Chế độ nền & Màu sắc màn hình</label>
              <span class="text-[11px] font-bold txt-brand">5 Chế độ chuyên biệt</span>
            </div>
            <div class="grid grid-cols-2 sm:grid-cols-5 gap-2.5">
              <button onclick="setThemeMode('midnight')" id="theme-opt-midnight" class="mode-card text-center p-2.5">
                <div class="text-lg">🌌</div>
                <div class="text-xs font-extrabold txt-main mt-1">Xanh Midnight</div>
                <div class="text-[10px] txt-muted">Dịu mắt ban đêm</div>
              </button>
              <button onclick="setThemeMode('dark')" id="theme-opt-dark" class="mode-card text-center p-2.5">
                <div class="text-lg">🌑</div>
                <div class="text-xs font-extrabold txt-main mt-1">Đen Tuyệt Đối</div>
                <div class="text-[10px] txt-muted">Pure OLED #000</div>
              </button>
              <button onclick="setThemeMode('contrast')" id="theme-opt-contrast" class="mode-card text-center p-2.5">
                <div class="text-lg">⚡</div>
                <div class="text-xs font-extrabold txt-main mt-1">Siêu Tương Phản</div>
                <div class="text-[10px] txt-muted">Chuẩn WCAG AAA</div>
              </button>
              <button onclick="setThemeMode('light')" id="theme-opt-light" class="mode-card text-center p-2.5">
                <div class="text-lg">☀️</div>
                <div class="text-xs font-extrabold txt-main mt-1">Sáng Rõ Ràng</div>
                <div class="text-[10px] txt-muted">Sắc nét ban ngày</div>
              </button>
              <button onclick="setThemeMode('sepia')" id="theme-opt-sepia" class="mode-card text-center p-2.5">
                <div class="text-lg">📜</div>
                <div class="text-xs font-extrabold txt-main mt-1">Giấy Kem Sepia</div>
                <div class="text-[10px] txt-muted">Chống cận thị</div>
              </button>
            </div>

            <!-- Accessibility High-Contrast Boost -->
            <div class="p-3.5 rounded-2xl flex items-center justify-between" style="background-color: var(--bg-subtle); border: 1px solid var(--border);">
              <div class="space-y-0.5">
                <div class="text-xs font-extrabold txt-main flex items-center gap-1.5">
                  <span>👁️</span> Tăng Cường Độ Tương Phản Chữ (High-Contrast Boost)
                </div>
                <div class="text-[11px] txt-muted">Làm chữ phụ và viền đáp án luôn sáng rõ nét, chống mờ trên màn hình điện thoại</div>
              </div>
              <label class="relative inline-flex items-center cursor-pointer">
                <input type="checkbox" id="pref-contrast-boost" onchange="toggleHighContrastBoost(this.checked)" class="sr-only peer" />
                <div class="w-11 h-6 bg-slate-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-emerald-500"></div>
              </label>
            </div>
          </div>

          <!-- Accent Color Swatches + Custom Color -->
          <div class="space-y-2.5">
            <label class="text-xs font-extrabold uppercase tracking-wider txt-muted">2. Màu chủ đề rực rỡ</label>
            <div class="flex flex-wrap items-center gap-3">
              <button onclick="setAccentPalette('#7c3aed', '#ec4899')" data-accent="#7c3aed" title="Neon Violet" class="swatch-btn" style="background: linear-gradient(135deg, #7c3aed, #ec4899);"></button>
              <button onclick="setAccentPalette('#2563eb', '#06b6d4')" data-accent="#2563eb" title="Cyber Ocean" class="swatch-btn" style="background: linear-gradient(135deg, #2563eb, #06b6d4);"></button>
              <button onclick="setAccentPalette('#10b981', '#14b8a6')" data-accent="#10b981" title="Emerald Mint" class="swatch-btn" style="background: linear-gradient(135deg, #10b981, #14b8a6);"></button>
              <button onclick="setAccentPalette('#f97316', '#f43f5e')" data-accent="#f97316" title="Sunset Coral" class="swatch-btn" style="background: linear-gradient(135deg, #f97316, #f43f5e);"></button>
              <button onclick="setAccentPalette('#ec4899', '#8b5cf6')" data-accent="#ec4899" title="Sakura Pink" class="swatch-btn" style="background: linear-gradient(135deg, #ec4899, #8b5cf6);"></button>
              <button onclick="setAccentPalette('#eab308', '#f97316')" data-accent="#eab308" title="Royal Gold" class="swatch-btn" style="background: linear-gradient(135deg, #eab308, #f97316);"></button>
              <button onclick="setAccentPalette('#ef4444', '#ec4899')" data-accent="#ef4444" title="Crimson Ruby" class="swatch-btn" style="background: linear-gradient(135deg, #ef4444, #ec4899);"></button>
              <button onclick="setAccentPalette('#06b6d4', '#6366f1')" data-accent="#06b6d4" title="Electric Cyan" class="swatch-btn" style="background: linear-gradient(135deg, #06b6d4, #6366f1);"></button>

              <label class="btn-soft px-3 py-1.5 text-xs flex items-center gap-1.5 cursor-pointer">
                <input type="color" id="custom-accent-picker" oninput="setAccentPalette(this.value, this.value)" class="w-5 h-5 rounded cursor-pointer border-0 bg-transparent" />
                <span>Tự chọn màu</span>
              </label>
            </div>
          </div>

          <!-- UI Shape & Corner Radius -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div class="p-4 rounded-2xl space-y-2.5" style="background-color: var(--bg-subtle); border: 1px solid var(--border);">
              <div class="flex justify-between items-center text-xs font-bold">
                <span class="txt-main flex items-center gap-1.5"><span>📐</span> Bo tròn góc khung thẻ (Radius)</span>
                <span id="lbl-card-radius" class="txt-brand font-mono font-extrabold">18px</span>
              </div>
              <input id="slider-card-radius" type="range" min="8" max="28" step="1" value="18"
                oninput="updateTypographyPrefs()" class="range-slider-modern" />
              <div class="flex justify-between text-[10px] txt-muted font-bold">
                <span>8px (Vuông)</span>
                <span>18px (Cân đối)</span>
                <span>28px (Siêu tròn)</span>
              </div>
            </div>

            <div class="p-4 rounded-2xl space-y-2.5" style="background-color: var(--bg-subtle); border: 1px solid var(--border);">
              <div class="flex justify-between items-center text-xs font-bold">
                <span class="txt-main flex items-center gap-1.5"><span>🔮</span> Độ sâu bóng đổ 3D (Shadow)</span>
                <span class="text-[11px] txt-brand font-bold">Nổi khối</span>
              </div>
              <select id="pref-shadow-depth" onchange="updateTypographyPrefs()" class="uni-input w-full px-3 py-2 text-xs font-bold" style="background-color: var(--bg-surface);">
                <option value="subtle">Nhẹ nhàng thanh thoát</option>
                <option value="medium" selected>Tiêu chuẩn 3D hiện đại</option>
                <option value="deep">Sâu đậm cao cấp (Nổi bật tối đa)</option>
              </select>
            </div>
          </div>
        </div>

        <!-- ==========================================
             TAB 2: CỠ CHỮ & GIÃN DÒNG
             ========================================== -->
        <div id="stab-panel-typography" class="hidden space-y-6">
          <!-- 1-Click Font Style Presets -->
          <div class="space-y-2">
            <label class="text-xs font-extrabold uppercase tracking-wider txt-muted">1. Bộ Phông Chữ Gợi Ý Nhanh (1-Chạm)</label>
            <div class="flex flex-wrap gap-1.5">
              <button type="button" onclick="applyFontPreset('google_sans')" class="preset-pill !text-xs">✨ Google Sans Hiện Đại</button>
              <button type="button" onclick="applyFontPreset('times_exam')" class="preset-pill !text-xs" style="font-family: 'Times New Roman', serif;">📜 Chuẩn Đề Bộ GD (Times New Roman)</button>
              <button type="button" onclick="applyFontPreset('arial_clean')" class="preset-pill !text-xs" style="font-family: Arial, sans-serif;">🅰️ Arial Thanh Lịch</button>
              <button type="button" onclick="applyFontPreset('lexend_read')" class="preset-pill !text-xs" style="font-family: 'Lexend', sans-serif;">📖 Lexend Chống Mỏi Mắt</button>
              <button type="button" onclick="applyFontPreset('academic_mix')" class="preset-pill !text-xs">🎓 Câu Hỏi Serif + Đáp Án Google Sans</button>
            </div>
          </div>

          <!-- Granular Font Family Selectors -->
          <div class="p-4 rounded-2xl space-y-3.5" style="background-color: var(--bg-subtle); border: 1px solid var(--border);">
            <div class="flex items-center justify-between">
              <label class="text-xs font-extrabold uppercase tracking-wider txt-main">2. Tùy Chỉnh Phông Chữ Chi Tiết (26 Phông Chữ)</label>
              <span class="text-[11px] font-semibold txt-brand">Đổi riêng Câu hỏi, Đáp án hoặc Toàn bộ</span>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
              <!-- Global System Font -->
              <div class="space-y-1">
                <label class="text-xs font-bold txt-sub">🌐 Toàn bộ hệ thống (Mặc định chung)</label>
                <select id="pref-font-ui" onchange="updateTypographyPrefs()" class="uni-input w-full px-3 py-2 text-xs font-bold" style="background-color: var(--bg-surface);">
                  <optgroup label="Phông Google & Hiện đại">
                    <option value="'Google Sans', 'Product Sans', 'Outfit', 'Plus Jakarta Sans', sans-serif">Google Sans (Chuẩn Google hiện đại)</option>
                    <option value="'Plus Jakarta Sans', sans-serif">Plus Jakarta Sans (Trẻ trung, nịnh mắt)</option>
                    <option value="'Inter', sans-serif">Inter (Sắc nét chuẩn UI quốc tế)</option>
                    <option value="'Roboto', sans-serif">Roboto (Chuẩn Android / Material)</option>
                    <option value="'Open Sans', sans-serif">Open Sans (Thoáng đãng, trung tính)</option>
                    <option value="'Be Vietnam Pro', sans-serif">Be Vietnam Pro (Tối ưu dấu Tiếng Việt)</option>
                    <option value="'Lexend', sans-serif">Lexend (Đọc siêu nhanh, chống mỏi mắt)</option>
                    <option value="'Montserrat', sans-serif">Montserrat (Hình học cá tính)</option>
                    <option value="'Nunito', sans-serif">Nunito (Bo tròn mềm mại)</option>
                    <option value="'Quicksand', sans-serif">Quicksand (Thanh mảnh, tinh tế)</option>
                    <option value="'Outfit', sans-serif">Outfit (Hiện đại, gọn gàng)</option>
                    <option value="'DM Sans', sans-serif">DM Sans (Tối giản cao cấp)</option>
                  </optgroup>
                  <optgroup label="Phông Văn Phòng & Đề Thi Chuẩn (Windows / Mac)">
                    <option value="Arial, 'Helvetica Neue', Helvetica, sans-serif">Arial (Kinh điển, rõ ràng)</option>
                    <option value="'Times New Roman', Times, serif">Times New Roman (Chuẩn đề thi Bộ GD)</option>
                    <option value="'Segoe UI', system-ui, sans-serif">Segoe UI (Chuẩn Windows 11)</option>
                    <option value="Calibri, 'Segoe UI', sans-serif">Calibri (Chuẩn Microsoft Office)</option>
                    <option value="Tahoma, Geneva, sans-serif">Tahoma (Đậm nét, dễ nhìn)</option>
                    <option value="Verdana, Geneva, sans-serif">Verdana (Chữ rộng, cực dễ đọc)</option>
                    <option value="'Trebuchet MS', sans-serif">Trebuchet MS (Thanh thoát)</option>
                  </optgroup>
                  <optgroup label="Phông Sách In Học Thuật (Serif)">
                    <option value="Georgia, serif">Georgia (Sách giáo khoa phương Tây)</option>
                    <option value="'Lora', serif">Lora Serif (Sách in nghệ thuật)</option>
                    <option value="'Merriweather', serif">Merriweather (Chuyên đọc tài liệu dài)</option>
                    <option value="'Source Serif 4', serif">Source Serif 4 (Tạp chí khoa học)</option>
                    <option value="'Playfair Display', serif">Playfair Display (Sang trọng cổ điển)</option>
                    <option value="'Palatino Linotype', 'Book Antiqua', Palatino, serif">Palatino Linotype (Đề thi học thuật)</option>
                  </optgroup>
                  <optgroup label="Phông Máy Đánh Chữ (Monospace)">
                    <option value="'Courier New', Courier, monospace">Courier New (Máy đánh chữ cổ điển)</option>
                  </optgroup>
                </select>
              </div>

              <!-- Dedicated Question Font -->
              <div class="space-y-1">
                <label class="text-xs font-bold txt-sub">❓ Phông chữ riêng cho CÂU HỎI</label>
                <select id="pref-font-question" onchange="updateTypographyPrefs()" class="uni-input w-full px-3 py-2 text-xs font-bold" style="background-color: var(--bg-surface);">
                  <option value="inherit">🔗 Giống phông Toàn hệ thống</option>
                  <optgroup label="Phông Đề Thi & Văn Phòng Phổ Biến">
                    <option value="'Times New Roman', Times, serif">Times New Roman (Chuẩn đề thi giấy)</option>
                    <option value="Arial, 'Helvetica Neue', Helvetica, sans-serif">Arial (Rõ nét, quen thuộc)</option>
                    <option value="'Google Sans', 'Product Sans', 'Outfit', 'Plus Jakarta Sans', sans-serif">Google Sans (Hiện đại)</option>
                    <option value="'Segoe UI', system-ui, sans-serif">Segoe UI</option>
                    <option value="Calibri, 'Segoe UI', sans-serif">Calibri</option>
                    <option value="Tahoma, Geneva, sans-serif">Tahoma</option>
                    <option value="Verdana, Geneva, sans-serif">Verdana</option>
                    <option value="Georgia, serif">Georgia</option>
                    <option value="'Palatino Linotype', 'Book Antiqua', Palatino, serif">Palatino Linotype</option>
                  </optgroup>
                  <optgroup label="Phông Hiện Đại & Học Thuật">
                    <option value="'Plus Jakarta Sans', sans-serif">Plus Jakarta Sans</option>
                    <option value="'Inter', sans-serif">Inter</option>
                    <option value="'Roboto', sans-serif">Roboto</option>
                    <option value="'Open Sans', sans-serif">Open Sans</option>
                    <option value="'Be Vietnam Pro', sans-serif">Be Vietnam Pro</option>
                    <option value="'Lexend', sans-serif">Lexend</option>
                    <option value="'Montserrat', sans-serif">Montserrat</option>
                    <option value="'Nunito', sans-serif">Nunito</option>
                    <option value="'Quicksand', sans-serif">Quicksand</option>
                    <option value="'Outfit', sans-serif">Outfit</option>
                    <option value="'DM Sans', sans-serif">DM Sans</option>
                    <option value="'Lora', serif">Lora Serif</option>
                    <option value="'Merriweather', serif">Merriweather</option>
                    <option value="'Source Serif 4', serif">Source Serif 4</option>
                    <option value="'Playfair Display', serif">Playfair Display</option>
                    <option value="'Courier New', Courier, monospace">Courier New</option>
                  </optgroup>
                </select>
              </div>

              <!-- Dedicated Answer Option Font -->
              <div class="space-y-1">
                <label class="text-xs font-bold txt-sub">☑️ Phông chữ riêng cho ĐÁP ÁN (A, B, C, D)</label>
                <select id="pref-font-answer" onchange="updateTypographyPrefs()" class="uni-input w-full px-3 py-2 text-xs font-bold" style="background-color: var(--bg-surface);">
                  <option value="inherit">🔗 Giống phông Toàn hệ thống</option>
                  <optgroup label="Phông Đáp Án Dễ Nhìn Nhất">
                    <option value="'Google Sans', 'Product Sans', 'Outfit', 'Plus Jakarta Sans', sans-serif">Google Sans (Gọn, sáng, dễ quét mắt)</option>
                    <option value="Arial, 'Helvetica Neue', Helvetica, sans-serif">Arial (Chuẩn trắc nghiệm máy tính)</option>
                    <option value="'Times New Roman', Times, serif">Times New Roman (Chuẩn đề thi Bộ GD)</option>
                    <option value="'Lexend', sans-serif">Lexend (Chống nhầm dòng)</option>
                    <option value="'Inter', sans-serif">Inter</option>
                    <option value="'Roboto', sans-serif">Roboto</option>
                    <option value="'Be Vietnam Pro', sans-serif">Be Vietnam Pro</option>
                    <option value="'Plus Jakarta Sans', sans-serif">Plus Jakarta Sans</option>
                    <option value="'Open Sans', sans-serif">Open Sans</option>
                    <option value="'Nunito', sans-serif">Nunito</option>
                    <option value="'Montserrat', sans-serif">Montserrat</option>
                    <option value="'Quicksand', sans-serif">Quicksand</option>
                    <option value="'Outfit', sans-serif">Outfit</option>
                    <option value="'DM Sans', sans-serif">DM Sans</option>
                    <option value="'Segoe UI', system-ui, sans-serif">Segoe UI</option>
                    <option value="Calibri, 'Segoe UI', sans-serif">Calibri</option>
                    <option value="Tahoma, Geneva, sans-serif">Tahoma</option>
                    <option value="Verdana, Geneva, sans-serif">Verdana</option>
                    <option value="Georgia, serif">Georgia</option>
                    <option value="'Lora', serif">Lora Serif</option>
                    <option value="'Merriweather', serif">Merriweather</option>
                    <option value="'Source Serif 4', serif">Source Serif 4</option>
                    <option value="'Playfair Display', serif">Playfair Display</option>
                    <option value="'Courier New', Courier, monospace">Courier New</option>
                  </optgroup>
                </select>
              </div>

              <!-- Code Block Font -->
              <div class="space-y-1">
                <label class="text-xs font-bold txt-sub">💻 Phông chữ Khối Code (C# & Python)</label>
                <select id="pref-font-code" onchange="updateTypographyPrefs()" class="uni-input w-full px-3 py-2 text-xs font-mono font-bold" style="background-color: var(--bg-surface);">
                  <option value="'JetBrains Mono', monospace">JetBrains Mono (Chuẩn IDE hiện đại)</option>
                  <option value="'Fira Code', monospace">Fira Code (Mượt mà, sắc nét)</option>
                  <option value="'Source Code Pro', monospace">Source Code Pro (Adobe Coding)</option>
                  <option value="Consolas, 'Courier New', monospace">Consolas (Chuẩn Visual Studio)</option>
                  <option value="'Courier New', Courier, monospace">Courier New (Cổ điển)</option>
                </select>
              </div>
            </div>
          </div>

          <!-- Quad Font Size & Line Height Sliders -->
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
            <div class="p-3.5 rounded-2xl space-y-2" style="background-color: var(--bg-subtle); border: 1px solid var(--border);">
              <div class="flex justify-between text-xs font-bold">
                <span class="txt-sub">Cỡ toàn hệ thống</span>
                <span id="lbl-base-px" class="txt-brand font-mono">16px</span>
              </div>
              <input id="slider-base-px" type="range" min="13" max="21" step="0.5" value="16"
                oninput="updateTypographyPrefs()" class="range-slider-modern" />
            </div>

            <div class="p-3.5 rounded-2xl space-y-2" style="background-color: var(--bg-subtle); border: 1px solid var(--border);">
              <div class="flex justify-between text-xs font-bold">
                <span class="txt-sub">Cỡ riêng Câu hỏi</span>
                <span id="lbl-q-rem" class="txt-brand font-mono">114%</span>
              </div>
              <input id="slider-q-rem" type="range" min="0.88" max="1.6" step="0.03" value="1.14"
                oninput="updateTypographyPrefs()" class="range-slider-modern" />
            </div>

            <div class="p-3.5 rounded-2xl space-y-2" style="background-color: var(--bg-subtle); border: 1px solid var(--border);">
              <div class="flex justify-between text-xs font-bold">
                <span class="txt-sub">Cỡ riêng Đáp án</span>
                <span id="lbl-opt-rem" class="txt-brand font-mono">102%</span>
              </div>
              <input id="slider-opt-rem" type="range" min="0.86" max="1.5" step="0.03" value="1.02"
                oninput="updateTypographyPrefs()" class="range-slider-modern" />
            </div>

            <div class="p-3.5 rounded-2xl space-y-2" style="background-color: var(--bg-subtle); border: 1px solid var(--border);">
              <div class="flex justify-between text-xs font-bold">
                <span class="txt-sub">Khoảng cách dòng</span>
                <span id="lbl-line-height" class="txt-brand font-mono">1.62x</span>
              </div>
              <input id="slider-line-height" type="range" min="1.4" max="2.0" step="0.05" value="1.62"
                oninput="updateTypographyPrefs()" class="range-slider-modern" />
            </div>
          </div>

          <!-- Live Dual Preview (Question + STEM Formula + Answer Options) -->
          <div class="p-4 rounded-2xl space-y-3" style="background-color: var(--bg-subtle); border: 1px solid var(--border);">
            <div class="flex items-center justify-between text-[11px] font-bold txt-muted uppercase">
              <span>Xem trước trực tiếp (Câu hỏi & Đáp án):</span>
              <span id="font-preview-summary" class="txt-brand normal-case"></span>
            </div>
            <div id="settings-live-q-preview" class="question-title-text p-3 rounded-xl" style="background-color: var(--bg-surface); border: 1px solid var(--border);">
              Câu 1: Cho phản ứng thuận nghịch dung dịch và dao động điều hòa — phát biểu nào dưới đây chính xác?
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
              <div class="option-row opt-A !cursor-default !py-2.5 !px-3.5">
                <div class="opt-badge !w-8 !h-8 !text-xs">A<span class="opt-key-micro">1</span></div>
                <div id="settings-live-opt-a" class="option-text">Vận tốc cực đại tại vị trí cân bằng</div>
              </div>
              <div class="option-row opt-B !cursor-default !py-2.5 !px-3.5">
                <div class="opt-badge !w-8 !h-8 !text-xs">B<span class="opt-key-micro">2</span></div>
                <div id="settings-live-opt-b" class="option-text">Đa hình động với <code class="inline-code">override</code></div>
              </div>
            </div>
          </div>
        </div>

        <!-- ==========================================
             TAB 3: TRÍ TUỆ NHÂN TẠO (CHATGPT & GEMINI)
             ========================================== -->
        <div id="stab-panel-ai" class="hidden space-y-5">
          <!-- CARD 1: CHATGPT / OPENAI (PRIORITY 1) -->
          <div class="p-4 sm:p-5 rounded-2xl space-y-3.5" style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.08), rgba(99, 102, 241, 0.08)); border: 1.5px solid rgba(16, 185, 129, 0.35);">
            <div class="flex flex-wrap items-center justify-between gap-2">
              <div class="flex items-center gap-2.5">
                <div class="w-9 h-9 rounded-xl flex items-center justify-center text-white text-base shadow-sm shrink-0" style="background: linear-gradient(135deg, #10b981, #059669);">
                  ⚡
                </div>
                <div>
                  <div class="text-sm font-black txt-main flex items-center gap-2">
                    <span>ChatGPT / OpenAI API</span>
                    <span class="badge-emerald text-[10px] px-2 py-0.5 rounded-full font-black uppercase">Ưu Tiên Số 1</span>
                  </div>
                  <div id="openai-current-mask" class="text-xs txt-muted mt-0.5">Khóa mặc định: sk-00e...2119</div>
                </div>
              </div>
              <span id="openai-status-pill" class="badge-emerald text-xs px-2.5 py-1 rounded-full font-bold">🟢 Ưu tiên gọi trước</span>
            </div>

            <p class="text-xs txt-sub leading-relaxed">
              Tất cả tính năng AI (Gia Sư AI, Gợi ý, Phân tích lỗi, Công thức nền, Chấm tự luận) sẽ được <strong>ưu tiên gửi tới ChatGPT trước</strong>. Khi hạn mức hết hoặc gặp sự cố mạng, hệ thống tự động chuyển tiếp liền mạch sang dàn Google Gemini mà không ngắt quãng bài thi!
            </p>

            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-1">
              <div class="space-y-1">
                <label class="text-[11px] font-bold txt-sub">Khóa API ChatGPT (Key):</label>
                <div class="relative flex items-center">
                  <input id="cfg-openai-key" type="password" placeholder="sk-..." class="uni-input w-full px-3 py-2 pr-10 text-xs font-mono" />
                  <button type="button" onclick="togglePasswordVis('cfg-openai-key')" class="absolute right-2 text-xs txt-muted hover:text-white" title="Hiện/ẩn khóa">👁️</button>
                </div>
              </div>
              <div class="space-y-1">
                <label class="text-[11px] font-bold txt-sub">API Base URL (Máy chủ OpenAI / Proxy Relay):</label>
                <input id="cfg-openai-base" type="text" placeholder="https://api.openai.com/v1" class="uni-input w-full px-3 py-2 text-xs font-mono" />
              </div>
            </div>

            <div class="space-y-1">
              <label class="text-[11px] font-bold txt-sub">Chế độ điều phối AI:</label>
              <select id="cfg-ai-priority" class="uni-input w-full px-3 py-2 text-xs font-bold">
                <option value="openai_first">⚡ Ưu tiên ChatGPT trước (Hết quota/lỗi tự động sang Gemini) — Khuyên Dùng</option>
                <option value="gemini_only">🤖 Chỉ dùng dàn Google Gemini</option>
              </select>
            </div>

            <div id="openai-test-feedback" class="hidden text-xs p-3 rounded-xl font-bold"></div>

            <div class="flex flex-wrap gap-2 pt-1">
              <button type="button" onclick="testOpenAiKeyUI()" class="btn-primary px-4 py-2 text-xs flex items-center gap-1.5 shadow-sm">
                <span>🔌</span> Kiểm Tra Kết Nối ChatGPT
              </button>
              <button type="button" onclick="saveOpenAiSettingsUI()" class="btn-soft px-4 py-2 text-xs txt-emerald font-bold flex items-center gap-1.5">
                <span>💾</span> Lưu Cài Đặt ChatGPT
              </button>
            </div>
          </div>

          <!-- CARD 2: DEFAULT TUTOR PERSONA & VERBOSITY -->
          <div class="p-4 rounded-2xl space-y-3" style="background-color: var(--bg-subtle); border: 1px solid var(--border);">
            <div class="text-xs font-extrabold uppercase tracking-wider txt-main flex items-center gap-1.5">
              <span>🧠</span> Cấu Hình Tính Cách & Độ Dài Trả Lời Của Gia Sư AI
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-1">
              <div class="space-y-1">
                <label class="text-[11px] font-bold txt-sub">Tính cách Gia sư mặc định:</label>
                <select id="cfg-default-tutor-persona" onchange="updateTypographyPrefs()" class="uni-input w-full px-3 py-2 text-xs font-bold" style="background-color: var(--bg-surface);">
                  <option value="professor" selected>🎓 Giáo Sư (Hàn lâm, giải thích cơ chế sâu sắc)</option>
                  <option value="feynman">🧒 Feynman (Ví von thực tế, dễ hiểu tuyệt đối)</option>
                  <option value="speed">⚡ Giải Nhanh (Mẹo loại suy, bấm máy 5s)</option>
                  <option value="examiner">🎤 Vấn Đáp (Đặt câu hỏi ngược thử thách tư duy)</option>
                </select>
              </div>

              <div class="space-y-1">
                <label class="text-[11px] font-bold txt-sub">Độ dài lời giải thích AI:</label>
                <select id="cfg-ai-verbosity" onchange="updateTypographyPrefs()" class="uni-input w-full px-3 py-2 text-xs font-bold" style="background-color: var(--bg-surface);">
                  <option value="concise">Siêu Ngắn Gọn (3 ý cốt lõi, tiết kiệm thời gian)</option>
                  <option value="standard" selected>Tiêu Chuẩn (1 đoạn súc tích + vì sao đúng/sai)</option>
                  <option value="deep">Chuyên Sâu (Đầy đủ cơ chế phản ứng / mã nguồn)</option>
                </select>
              </div>
            </div>
          </div>

          <!-- Divider -->
          <div class="flex items-center gap-3 pt-1">
            <div class="h-px bg-slate-700/60 flex-1"></div>
            <span class="text-[11px] font-extrabold uppercase tracking-wider txt-muted">Dàn Dự Phòng Gemini Luân Phiên</span>
            <div class="h-px bg-slate-700/60 flex-1"></div>
          </div>

          <!-- CARD 3: GEMINI MULTI-KEY POOL -->
          <div class="space-y-3">
            <div class="flex flex-wrap items-center justify-between gap-2">
              <div>
                <div class="text-sm font-extrabold txt-main">🤖 Dàn API Key Luân Phiên Tự Động (Auto-Failover Pool)</div>
                <div id="api-current-mask" class="text-xs txt-muted mt-0.5">Đang kiểm tra dàn khóa...</div>
              </div>
              <span id="api-status-pill" class="badge-amber text-xs px-3 py-1 rounded-full font-bold">Chưa kiểm tra</span>
            </div>

            <div class="p-3 rounded-xl text-xs leading-relaxed badge-brand">
              ⚡ <strong>Cơ chế Bất Tử Quota:</strong> Bạn có thể gắn <strong>2, 5 hoặc 10 API Key</strong> cùng lúc. Khi Key #1 chạm giới hạn miễn phí (429), hệ thống tự động nhảy sang Key #2, #3 trong tích tắc mà không làm gián đoạn bài thi!
            </div>

            <!-- Active Pool List -->
            <div id="api-pool-list" class="space-y-2 max-h-44 overflow-y-auto pr-1"></div>

            <!-- Batch Add Keys Textarea -->
            <div class="space-y-1.5">
              <label class="text-xs font-bold txt-sub">
                Thêm 1 hoặc nhiều API Key cùng lúc — mỗi dòng 1 mã (<a href="https://aistudio.google.com/app/apikey" target="_blank" class="txt-brand underline">Lấy miễn phí tại Google AI Studio ↗</a>)
              </label>
              <textarea id="api-keys-textarea" rows="2"
                placeholder="AIzaSy... (Key tài khoản 1)&#10;AIzaSy... (Key tài khoản 2)"
                class="uni-input w-full p-2.5 text-xs font-mono"></textarea>
            </div>

            <div id="api-test-feedback" class="hidden text-xs p-3 rounded-xl font-bold"></div>

            <div class="flex flex-wrap items-center justify-between gap-2 pt-1">
              <div class="flex flex-wrap gap-2">
                <button onclick="addApiKeysToPool()" class="btn-primary px-4 py-2 text-xs">➕ Thêm Vào Dàn Key</button>
                <button onclick="testAllApiKeys()" class="btn-soft px-4 py-2 text-xs txt-brand">🔌 Kiểm Tra Dàn Key</button>
              </div>
              <button onclick="clearAllApiKeys()" class="btn-soft px-3 py-1.5 text-xs txt-rose">Xóa hết</button>
            </div>
          </div>
        </div>

        <!-- ==========================================
             TAB 4: ÂM THANH, ĐỒNG HỒ & TIỆN ÍCH
             ========================================== -->
        <div id="stab-panel-tools" class="hidden space-y-5">
          <!-- Audio Controls -->
          <div class="p-4 rounded-2xl space-y-4" style="background-color: var(--bg-subtle); border: 1px solid var(--border);">
            <div class="flex items-center justify-between">
              <div>
                <div class="text-xs font-extrabold txt-main">🔊 Âm thanh phím bấm & hiệu ứng đúng/sai</div>
                <div class="text-[11px] txt-muted">Phát tiếng phản hồi êm tai khi chọn đáp án</div>
              </div>
              <label class="relative inline-flex items-center cursor-pointer">
                <input id="pref-sound-toggle" type="checkbox" checked onchange="toggleSoundPref(this.checked)" class="sr-only peer" />
                <div class="w-11 h-6 bg-slate-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-purple-600"></div>
              </label>
            </div>

            <!-- Sound Volume Slider -->
            <div class="space-y-1.5 pt-2" style="border-top: 1px solid var(--border);">
              <div class="flex justify-between items-center text-xs font-bold">
                <span class="txt-sub">Âm lượng hiệu ứng âm thanh</span>
                <span id="lbl-sound-vol" class="txt-brand font-mono font-bold">80%</span>
              </div>
              <input id="slider-sound-vol" type="range" min="0" max="100" step="5" value="80"
                oninput="updateTypographyPrefs()" class="range-slider-modern" />
            </div>

            <!-- Voice TTS Speed -->
            <div class="space-y-1.5 pt-2" style="border-top: 1px solid var(--border);">
              <div class="flex justify-between items-center text-xs font-bold">
                <span class="txt-sub">Tốc độ đọc câu hỏi bằng giọng nói (AI Voice TTS)</span>
                <span class="txt-brand text-[11px]">Tiếng Việt chuẩn</span>
              </div>
              <select id="pref-tts-speed" onchange="updateTypographyPrefs()" class="uni-input w-full px-3 py-2 text-xs font-bold" style="background-color: var(--bg-surface);">
                <option value="0.85">0.85x — Chậm rãi, rành mạch</option>
                <option value="1.0" selected>1.0x — Tốc độ chuẩn tự nhiên</option>
                <option value="1.2">1.2x — Nhanh, tăng tốc độ đọc đề</option>
                <option value="1.45">1.45x — Siêu tốc, luyện phản xạ</option>
              </select>
            </div>
          </div>

          <!-- Auto-Next & Exam Timer Display -->
          <div class="p-4 rounded-2xl space-y-4" style="background-color: var(--bg-subtle); border: 1px solid var(--border);">
            <div class="flex items-center justify-between">
              <div>
                <div class="text-xs font-extrabold txt-main">⏩ Tự chuyển câu mới khi làm ĐÚNG</div>
                <div class="text-[11px] txt-muted">Áp dụng trong chế độ Luyện tập & Blitz</div>
              </div>
              <label class="relative inline-flex items-center cursor-pointer">
                <input id="pref-autonext-toggle" type="checkbox" onchange="toggleAutoNextPref(this.checked)" class="sr-only peer" />
                <div class="w-11 h-6 bg-slate-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-purple-600"></div>
              </label>
            </div>

            <!-- Auto-next delay slider -->
            <div class="space-y-1.5 pt-2" style="border-top: 1px solid var(--border);">
              <div class="flex justify-between items-center text-xs font-bold">
                <span class="txt-sub">Độ trễ trước khi tự chuyển câu:</span>
                <span id="lbl-autonext-delay" class="txt-brand font-mono font-bold">0.8s</span>
              </div>
              <input id="slider-autonext-delay" type="range" min="0.4" max="2.0" step="0.2" value="0.8"
                oninput="updateTypographyPrefs()" class="range-slider-modern" />
            </div>

            <!-- Exam Timer Display Style -->
            <div class="space-y-1.5 pt-2" style="border-top: 1px solid var(--border);">
              <div class="flex justify-between items-center text-xs font-bold">
                <span class="txt-sub">Kiểu hiển thị đồng hồ trong phòng thi:</span>
                <span class="txt-brand text-[11px]">Tùy biến tâm lý</span>
              </div>
              <select id="pref-timer-display" onchange="updateTypographyPrefs()" class="uni-input w-full px-3 py-2 text-xs font-bold" style="background-color: var(--bg-surface);">
                <option value="countdown" selected>⏳ Đếm ngược thời gian còn lại (Chuẩn phòng thi)</option>
                <option value="countup">⏱️ Đếm xuôi thời gian đã làm</option>
                <option value="hidden">🙈 Ẩn đồng hồ (Giảm căng thẳng, tập trung giải đề)</option>
              </select>
            </div>
          </div>

          <!-- Pomodoro Timer Inside Settings -->
          <div class="p-4 rounded-2xl flex items-center justify-between gap-4" style="background-color: var(--bg-subtle); border: 1px solid var(--border);">
            <div>
              <div class="text-xs font-extrabold txt-main">🍅 Đồng Hồ Tập Trung Pomodoro (25 phút)</div>
              <div id="pomo-settings-time" class="text-2xl font-mono font-extrabold txt-brand mt-1">25:00</div>
            </div>
            <div class="flex gap-2">
              <button onclick="togglePomodoro()" id="pomo-toggle-btn" class="btn-primary px-4 py-2 text-xs">Bắt đầu</button>
              <button onclick="resetPomodoro()" class="btn-soft px-3 py-2 text-xs">Đặt lại</button>
            </div>
          </div>
        </div>

        <!-- ==========================================
             TAB 5: CHỐNG GIAN LẬN & ĐỒNG BỘ
             ========================================== -->
        <div id="stab-panel-sync" class="hidden space-y-5">
          <!-- Anti-Cheat Security Level -->
          <div class="p-4 rounded-2xl space-y-3" style="background-color: var(--bg-subtle); border: 1px solid var(--border);">
            <div class="flex items-center justify-between">
              <div>
                <div class="text-xs font-extrabold txt-main flex items-center gap-1.5">
                  <span>🛡️</span> Cấp Độ Chống Gian Lận Phòng Thi (Anti-Cheat)
                </div>
                <div class="text-[11px] txt-muted">Phát hiện khi thí sinh chuyển tab hoặc mở ứng dụng khác trong lúc thi tính giờ</div>
              </div>
              <span class="badge-emerald text-xs px-2.5 py-0.5 rounded-full font-bold">Bảo vệ đề</span>
            </div>

            <div class="pt-1">
              <select id="pref-anticheat-level" onchange="updateTypographyPrefs()" class="uni-input w-full px-3 py-2 text-xs font-bold" style="background-color: var(--bg-surface);">
                <option value="medium" selected>⚖️ Tiêu Chuẩn — Cảnh báo 2 lần, khóa bài sau lần chuyển tab thứ 3</option>
                <option value="strict">🔒 Nghiêm Ngặt — Cảnh báo 1 lần, khóa bài ngay lần chuyển tab thứ 2</option>
                <option value="off">🔓 Tự Do Ôn Tập — Không khóa bài khi chuyển tab (Phù hợp tự học)</option>
              </select>
            </div>
          </div>

          <!-- Wi-Fi QR Sync -->
          <div class="p-4 rounded-2xl flex flex-col sm:flex-row items-center gap-5" style="background-color: var(--bg-subtle); border: 1px solid var(--border);">
            <div id="wifi-qr-box" class="bg-white p-3 rounded-2xl shrink-0 shadow-md flex items-center justify-center w-36 h-36"></div>
            <div class="space-y-2 text-center sm:text-left">
              <div class="badge-emerald text-xs px-2.5 py-0.5 rounded-full font-bold inline-block">Đồng Bộ Trực Tiếp Qua Wi-Fi</div>
              <div class="text-sm font-extrabold txt-main">Quét mã QR bằng Camera iPhone / iPad / Android</div>
              <p class="text-xs txt-muted leading-relaxed">
                Học ngay trên điện thoại hoặc máy tính bảng mà không cần dây cáp. Mọi câu làm sai, ghi chú và XP được đồng bộ thời gian thực về máy tính!
              </p>
              <div class="pt-1">
                <span id="lan-url-text" class="text-xs font-mono font-bold txt-brand px-3 py-1.5 rounded-xl bg-purple-500/10 border border-purple-500/20 inline-block select-all">Đang quét địa chỉ mạng nội bộ...</span>
              </div>
            </div>
          </div>

          <!-- Full Backup Export & Import -->
          <div class="p-4 rounded-2xl space-y-3" style="background-color: var(--bg-subtle); border: 1px solid var(--border);">
            <div class="text-xs font-extrabold txt-main flex items-center gap-1.5">
              <span>💾</span> Sao Lưu & Phục Hồi Dữ Liệu Học Tập
            </div>
            <p class="text-xs txt-muted leading-relaxed">
              Xuất toàn bộ ngân hàng câu hỏi, lịch sử thi và ghi chú ra file JSON để lưu giữ an toàn hoặc chuyển sang máy tính khác:
            </p>
            <div class="flex flex-wrap gap-2 pt-1">
              <button type="button" onclick="exportFullBackup()" class="btn-soft px-4 py-2 text-xs flex items-center gap-1.5">
                <span>📤</span> Xuất Tệp Sao Lưu (.json)
              </button>
              <button type="button" onclick="triggerImportBackupModal()" class="btn-soft px-4 py-2 text-xs flex items-center gap-1.5">
                <span>📥</span> Khôi Phục Từ Tệp Sao Lưu
              </button>
            </div>
          </div>
        </div>

      </div>

      <!-- Modal Footer (Fixed, Clean, Actions) -->
      <div class="px-5 py-3 shrink-0 border-t flex items-center justify-between gap-3" style="border-color: var(--border); background-color: var(--bg-surface);">
        <button type="button" onclick="resetDefaultAppearance()" class="btn-soft px-3.5 py-2 text-xs flex items-center gap-1.5">
          <span>🔄</span> <span>Khôi phục mặc định</span>
        </button>
        <button type="button" onclick="closeModal('modal-settings')" class="btn-primary px-6 py-2 text-xs font-bold shadow-md">
          <span>✅ Đóng & Áp Dụng</span>
        </button>
      </div>
    </div>
  </div>

  """

start_marker = '  <!-- =====================================================================\n       UNIFIED SETTINGS HUB MODAL'
end_marker = '  <!-- Modal: Add Subject -->'

if start_marker in text and end_marker in text:
    start_pos = text.find(start_marker)
    end_pos = text.find(end_marker)
    text = text[:start_pos] + new_modal_settings + '\n' + text[end_pos:]
    print("Replaced modal-settings successfully")
else:
    print("Start or end marker not found!")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Done updating static/index.html with upgraded modal-settings")
