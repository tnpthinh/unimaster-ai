import re

html_path = r'C:\Users\PC\.gemini\antigravity\scratch\unimaster-ai\static\index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Fix iPad Top Navigation: change hidden xl:flex to hidden lg:flex
top_nav_target = '<nav class="hidden xl:flex items-center gap-1 p-1 rounded-2xl shrink-0"'
top_nav_replacement = '<nav class="hidden lg:flex items-center gap-1 p-1 rounded-2xl shrink-0"'
if top_nav_target in c:
    c = c.replace(top_nav_target, top_nav_replacement, 1)
    print("1. Fixed iPad Top Nav visibility (hidden lg:flex)")
else:
    print("WARNING: top_nav_target not found!")

# 2. Add Fullscreen button to Header
header_user_target = '<!-- User Account Menu Button -->'
header_fs_html = '''<!-- Global Fullscreen Toggle Button (Tránh vướng tab trình duyệt) -->
        <button id="header-fullscreen-btn" onclick="toggleAppFullscreen()" title="Chế độ Toàn Màn Hình (Không vướng tab trình duyệt)"
          class="btn-soft px-2.5 py-1 sm:h-9 text-xs font-black flex items-center gap-1.5 text-indigo-400 hover:text-indigo-300 rounded-xl border"
          style="border-color: rgba(99, 102, 241, 0.25);">
          <svg id="header-fs-icon" class="w-3.5 h-3.5 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"/>
          </svg>
          <span id="header-fs-label" class="hidden md:inline">Toàn Màn Hình</span>
        </button>

        <!-- User Account Menu Button -->'''

if header_user_target in c and 'id="header-fullscreen-btn"' not in c:
    c = c.replace(header_user_target, header_fs_html, 1)
    print("2. Added Fullscreen button to Header")

# 3. Add Fullscreen button to Home Screen Hero Banner
hero_action_target = '''<button onclick="openSubjectPickerModal()"
              class="btn-soft px-3.5 py-2.5 rounded-xl font-bold text-xs sm:text-sm flex items-center gap-1.5">
              <span>📚</span> Đổi Môn
            </button>'''

hero_action_replacement = '''<button onclick="openSubjectPickerModal()"
              class="btn-soft px-3.5 py-2.5 rounded-xl font-bold text-xs sm:text-sm flex items-center gap-1.5">
              <span>📚</span> Đổi Môn
            </button>
            <button onclick="toggleAppFullscreen()"
              class="btn-soft px-3.5 py-2.5 rounded-xl font-bold text-xs sm:text-sm flex items-center gap-1.5 text-indigo-400 hover:text-indigo-300 border border-indigo-500/30 shadow-sm"
              title="Bật chế độ Toàn Màn Hình để không bị vướng các tab trình duyệt">
              <span id="hero-fs-icon">⛶</span> <span id="hero-fs-label" class="hidden xs:inline">Toàn Màn Hình</span>
            </button>'''

if hero_action_target in c and 'id="hero-fs-icon"' not in c:
    c = c.replace(hero_action_target, hero_action_replacement, 1)
    print("3. Added Fullscreen button to Home Hero Banner")

# 4. Add "Đổi Tài Khoản & Môn Học" tab and panel in modal-account-profile
acc_tabs_target = '''<!-- Tabs: Profile vs Admin (Admin only) -->
      <div class="flex px-5 pt-3 gap-2 border-b" style="border-color: rgba(255, 255, 255, 0.08);">
        <button type="button" id="acc-tab-profile-btn" onclick="switchAccountTab('profile')" class="tab-btn active px-4 py-2 text-xs font-extrabold border-b-2 border-indigo-500 text-white">
          👤 Tài Khoản Của Tôi
        </button>
        <button type="button" id="acc-tab-admin-btn" onclick="switchAccountTab('admin')" class="tab-btn px-4 py-2 text-xs font-extrabold border-b-2 border-transparent text-slate-400 hover:text-white">
          👥 Quản Lý Người Dùng (Admin)
        </button>
      </div>'''

acc_tabs_replacement = '''<!-- Tabs: Switch Account vs Profile vs Admin -->
      <div class="flex px-5 pt-3 gap-1.5 sm:gap-2 border-b overflow-x-auto no-scrollbar" style="border-color: rgba(255, 255, 255, 0.08);">
        <button type="button" id="acc-tab-switch-btn" onclick="switchAccountTab('switch')" class="tab-btn active px-3 sm:px-4 py-2 text-xs font-extrabold border-b-2 border-indigo-500 text-white whitespace-nowrap">
          👥 Chuyển Acc & Môn Học
        </button>
        <button type="button" id="acc-tab-profile-btn" onclick="switchAccountTab('profile')" class="tab-btn px-3 sm:px-4 py-2 text-xs font-extrabold border-b-2 border-transparent text-slate-400 hover:text-white whitespace-nowrap">
          👤 Thông Tin Chi Tiết
        </button>
        <button type="button" id="acc-tab-admin-btn" onclick="switchAccountTab('admin')" class="tab-btn px-3 sm:px-4 py-2 text-xs font-extrabold border-b-2 border-transparent text-slate-400 hover:text-white whitespace-nowrap">
          👑 Quản Trị Hệ Thống
        </button>
      </div>'''

if acc_tabs_target in c:
    c = c.replace(acc_tabs_target, acc_tabs_replacement, 1)
    print("4a. Updated tabs in modal-account-profile")

# Add #acc-panel-switch right before #acc-panel-profile
acc_panel_target = '<!-- Panel 1: Profile & Sync -->'
acc_panel_switch_html = '''<!-- Panel 0: Multi-Account Switcher & Subject Selection -->
      <div id="acc-panel-switch" class="p-5 space-y-4 overflow-y-auto">
        <div class="flex items-center justify-between">
          <div>
            <h4 class="text-xs font-black uppercase tracking-wider txt-sub">Danh Sách Tài Khoản Trên Thiết Bị</h4>
            <p class="text-[11px] txt-muted">Mỗi tài khoản có môn học riêng, tiến độ và màu sắc giao diện độc lập</p>
          </div>
          <button type="button" onclick="promptCreateNewAccount()" class="btn-primary !bg-indigo-600 hover:!bg-indigo-500 px-3 py-1.5 rounded-xl text-xs font-black flex items-center gap-1 shadow-sm">
            <span>➕</span> <span>Thêm Acc Mới</span>
          </button>
        </div>

        <!-- Accounts Grid List -->
        <div id="acc-cards-container" class="space-y-2.5 max-h-[380px] overflow-y-auto pr-1"></div>

        <!-- Quick Subject Selection CTA for Active Account -->
        <div class="p-3.5 rounded-2xl border border-indigo-500/40 bg-indigo-500/10 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 shadow-sm">
          <div class="flex items-center gap-2.5">
            <span class="text-2xl">📚</span>
            <div>
              <div class="text-xs font-black text-indigo-300">Chọn Môn Học Cho Tài Khoản Này</div>
              <div id="acc-active-enrolled-summary" class="text-[11px] txt-muted">Đang học: Tất cả các môn</div>
            </div>
          </div>
          <button type="button" onclick="openAccountSubjectPickerModal()" class="btn-primary px-3.5 py-1.5 rounded-xl text-xs font-black shrink-0">
            <span>✏️</span> <span>Chọn Lại Môn Học</span>
          </button>
        </div>
      </div>

      <!-- Panel 1: Profile & Sync -->'''

if acc_panel_target in c and 'id="acc-panel-switch"' not in c:
    c = c.replace(acc_panel_target, acc_panel_switch_html, 1)
    # Also make #acc-panel-profile hidden by default because switch panel is active
    c = c.replace('<div id="acc-panel-profile" class="p-5 space-y-4 overflow-y-auto">', '<div id="acc-panel-profile" class="hidden p-5 space-y-4 overflow-y-auto">', 1)
    print("4b. Added #acc-panel-switch to modal-account-profile")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(c)

print("Step 1 HTML updates applied successfully!")
