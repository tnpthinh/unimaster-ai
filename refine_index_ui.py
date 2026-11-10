# -*- coding: utf-8 -*-
"""
Refine static/index.html to be minimalist, luxury, modern, and uncluttered:
1. Sleek Top Header with Global Active Subject Selector and User Account Menu
2. Streamlined Navigation Pills (reduced visual noise)
3. Elegant, calm Dashboard Hero (no more 6 giant chaotic buttons)
4. Subject Picker Modal
5. Account Profile & Admin User Management Modal
"""

import os
import re

INDEX_PATH = r"C:\Users\PC\.gemini\antigravity\scratch\unimaster-ai\static\index.html"

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Replace Top Header with Luxury Minimalist Header + Active Subject Selector + Account Button
new_header_html = """  <!-- =====================================================================
       LUXURY MINIMALIST TOP HEADER & ACTIVE SUBJECT BAR
       ===================================================================== -->
  <header class="sticky top-0 z-40 backdrop-blur-2xl transition-colors border-b"
    style="background: rgba(9, 10, 15, 0.88); border-color: rgba(255, 255, 255, 0.08);">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between gap-3">
      <!-- Left: Brand + Active Subject Selector -->
      <div class="flex items-center gap-3 shrink-0">
        <button onclick="switchTab('dashboard')" class="flex items-center gap-2.5 text-left group">
          <div class="w-8 h-8 rounded-xl flex items-center justify-center text-white font-black text-sm shadow-md transition-transform group-hover:scale-105"
            style="background: linear-gradient(135deg, #6366f1, #8b5cf6);">
            U
          </div>
          <span class="font-extrabold text-sm sm:text-base tracking-tight text-white hidden sm:inline">UniMaster</span>
        </button>

        <!-- Global Active Subject Selector Pill -->
        <button onclick="openSubjectPickerModal()" title="Bấm để đổi môn học đang ôn"
          class="flex items-center gap-2 px-3 py-1.5 rounded-xl border transition-all text-xs font-bold"
          style="background: rgba(255, 255, 255, 0.05); border-color: rgba(255, 255, 255, 0.1);">
          <span id="active-subj-icon" class="text-sm">🔬</span>
          <span id="active-subj-name" class="font-extrabold txt-main max-w-[130px] sm:max-w-[180px] md:max-w-[220px] truncate">Thực Hành Hóa Sinh (CTUMP)</span>
          <span id="active-subj-badge" class="badge-brand text-[10px] px-1.5 py-0.5 rounded font-mono font-bold">522 câu</span>
          <i data-lucide="chevron-down" class="w-3.5 h-3.5 opacity-60"></i>
        </button>
      </div>

      <!-- Center: Clean Minimalist Navigation Pills -->
      <nav class="hidden lg:flex items-center gap-1 p-1 rounded-2xl" style="background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.06);">
        <button onclick="switchTab('dashboard')" id="tab-dashboard" class="nav-tab active-tab px-3.5 py-1.5 text-xs flex items-center gap-1.5 font-bold">
          <i data-lucide="home" class="w-3.5 h-3.5"></i> Tổng quan
        </button>
        <button onclick="switchTab('exam')" id="tab-exam" class="nav-tab px-3.5 py-1.5 text-xs flex items-center gap-1.5 font-bold">
          <i data-lucide="zap" class="w-3.5 h-3.5"></i> Phòng thi
        </button>
        <button onclick="switchTab('lab')" id="tab-lab" class="nav-tab px-3.5 py-1.5 text-xs flex items-center gap-1.5 font-bold">
          <i data-lucide="flask-conical" class="w-3.5 h-3.5"></i> Thực hành & Lab
        </button>
        <button onclick="switchTab('flashcards')" id="tab-flashcards" class="nav-tab px-3.5 py-1.5 text-xs flex items-center gap-1.5 font-bold">
          <i data-lucide="layers" class="w-3.5 h-3.5"></i> Thẻ nhớ
        </button>
        <button onclick="switchTab('arena')" id="tab-arena" class="nav-tab px-3.5 py-1.5 text-xs flex items-center gap-1.5 font-bold">
          <i data-lucide="trophy" class="w-3.5 h-3.5"></i> Đấu trường
        </button>
        <button onclick="switchTab('tutor')" id="tab-tutor" class="nav-tab px-3.5 py-1.5 text-xs flex items-center gap-1.5 font-bold">
          <i data-lucide="bot" class="w-3.5 h-3.5"></i> AI Gia sư
        </button>
      </nav>

      <!-- Right: User Account Menu & Quick Action Cluster -->
      <div class="flex items-center gap-2 shrink-0">
        <!-- Quick Export Pill -->
        <button onclick="switchTab('lab'); switchLabSubTab('export');" title="Xuất Anki Deck & Đề Thi A4 Word"
          class="btn-soft px-2.5 py-1.5 text-xs hidden sm:flex items-center gap-1.5 font-bold">
          <span>📥</span> <span class="hidden xl:inline">Xuất Anki/In</span>
        </button>

        <!-- 1-Tap Dark/Light Switch -->
        <button id="quick-theme-btn" onclick="quickCycleDarkLight()" title="Đổi giao diện Sáng / Đen OLED"
          class="btn-soft p-2 text-xs flex items-center justify-center">
          <span id="quick-theme-sun" class="hidden inline-flex"><i data-lucide="sun" class="w-4 h-4 text-amber-400"></i></span>
          <span id="quick-theme-moon" class="inline-flex"><i data-lucide="moon" class="w-4 h-4 text-violet-400"></i></span>
        </button>

        <!-- User Account Menu Button -->
        <button id="header-user-btn" onclick="openAccountModal()" title="Hồ sơ tài khoản & Quản trị"
          class="flex items-center gap-2 p-1.5 pr-3 rounded-xl border transition-all text-xs font-bold"
          style="background: rgba(255, 255, 255, 0.05); border-color: rgba(255, 255, 255, 0.1);">
          <div id="header-user-avatar" class="w-6 h-6 rounded-lg bg-gradient-to-tr from-indigo-500 to-purple-600 text-white font-black text-xs flex items-center justify-center">
            A
          </div>
          <span id="header-user-name" class="font-bold txt-main hidden md:inline">Admin</span>
          <span id="header-user-role" class="badge-rose px-1.5 py-0.5 rounded text-[10px] font-black">👑 Quản Trị</span>
        </button>

        <!-- Settings Cog -->
        <button onclick="openSettingsModal('appearance')" title="Cài đặt hệ thống"
          class="btn-soft p-2 text-xs flex items-center justify-center">
          <i data-lucide="settings" class="w-4 h-4"></i>
        </button>
      </div>
    </div>
  </header>"""

# Replace header block
header_pattern = re.compile(r'<!-- =+\s*CLEAN TOP HEADER\s*=+\s*-->.*?<\/header>', re.DOTALL)
html = header_pattern.sub(new_header_html, html)

# 2. Refine Hero Banner in View Dashboard to be calm, minimalist, luxury
new_hero_html = """      <!-- Luxury Minimalist Subject Focus Hero -->
      <div class="uni-card p-6 sm:p-7 relative overflow-hidden" style="background: linear-gradient(135deg, rgba(30, 27, 75, 0.6) 0%, rgba(15, 23, 42, 0.8) 100%); border: 1px solid rgba(255, 255, 255, 0.08);">
        <div class="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div class="space-y-2.5 max-w-xl">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-bold badge-brand">
              <span id="hero-rank-title">🎓 Sinh Viên</span>
              <span>•</span>
              <span>🔥 Chuỗi <span id="hero-streak-days">1</span> ngày ôn tập</span>
            </div>
            <h1 class="text-2xl sm:text-3xl font-black tracking-tight text-white">
              Ôn thi thông minh với UniMaster AI
            </h1>
            <p class="text-xs sm:text-sm text-slate-300 leading-relaxed">
              Hệ thống cá nhân hóa bám sát chương trình. Chọn môn học để luyện trắc nghiệm, lật thẻ flashcard, thực hành lâm sàng và tra cứu dược lý.
            </p>
          </div>

          <!-- 2 Clean Primary Action Buttons -->
          <div class="flex flex-wrap sm:flex-nowrap items-center gap-3 shrink-0">
            <button onclick="quickStartBai2Protid()"
              class="btn-primary px-5 py-3 rounded-xl font-black text-xs sm:text-sm flex items-center gap-2 shadow-xl hover:-translate-y-0.5 transition-all">
              <span>⚡</span> Làm Bài Thi Ngay
            </button>
            <button onclick="openSubjectPickerModal()"
              class="btn-soft px-4 py-3 rounded-xl font-bold text-xs sm:text-sm flex items-center gap-2">
              <span>📚</span> Đổi Môn Học
            </button>
          </div>
        </div>

        <!-- Quick Sub-feature Pills Strip -->
        <div class="relative z-10 pt-5 mt-5 border-t flex flex-wrap items-center gap-2" style="border-color: rgba(255, 255, 255, 0.07);">
          <span class="text-[11px] font-bold text-slate-400 uppercase tracking-wider mr-1">Lối tắt nhanh:</span>
          <button onclick="quickStartBai2Protid()" class="badge-soft px-3 py-1 rounded-lg text-xs font-bold hover:border-emerald-500/50 transition-all flex items-center gap-1.5">
            <span>🩸</span> 200 câu Protid & Thận
          </button>
          <button onclick="switchTab('lab'); switchLabSubTab('spectro')" class="badge-soft px-3 py-1 rounded-lg text-xs font-bold hover:border-cyan-500/50 transition-all flex items-center gap-1.5">
            <span>🔬</span> Máy quang phổ Beer–Lambert
          </button>
          <button onclick="switchTab('lab'); switchLabSubTab('osce')" class="badge-soft px-3 py-1 rounded-lg text-xs font-bold hover:border-amber-500/50 transition-all flex items-center gap-1.5">
            <span>⏱️</span> Chạy trạm OSCE 6 trạm
          </button>
          <button onclick="switchTab('lab'); switchLabSubTab('patient')" class="badge-soft px-3 py-1 rounded-lg text-xs font-bold hover:border-purple-500/50 transition-all flex items-center gap-1.5">
            <span>🩺</span> Bệnh nhân ảo lâm sàng
          </button>
          <button onclick="switchTab('lab'); switchLabSubTab('dosing')" class="badge-soft px-3 py-1 rounded-lg text-xs font-bold hover:border-pink-500/50 transition-all flex items-center gap-1.5">
            <span>💊</span> Hiệu chỉnh liều theo thận
          </button>
        </div>
      </div>"""

# Replace Hero Banner
hero_pattern = re.compile(r'<!-- Vibrant Hero Card -->\s*<div class="hero-banner p-6 sm:p-7">.*?<!-- 4 Colorful Stat Cards -->', re.DOTALL)
html = hero_pattern.sub(new_hero_html + "\n\n      <!-- 4 Colorful Stat Cards -->", html)

# 3. Add Subject Picker Modal and Account Profile / Admin Modal before closing body tag
modals_html = """
  <!-- =====================================================================
       SUBJECT PICKER MODAL (CHỌN MÔN HỌC TRUNG TÂM)
       ===================================================================== -->
  <div id="modal-subject-picker" class="hidden fixed inset-0 z-50 modal-overlay flex items-center justify-center p-4">
    <div class="uni-card w-full max-w-lg max-h-[85vh] flex flex-col overflow-hidden animate-fade-in" style="background: #0f1118; border: 1px solid rgba(255, 255, 255, 0.1);">
      <div class="p-5 flex items-center justify-between border-b" style="border-color: rgba(255, 255, 255, 0.08);">
        <div class="flex items-center gap-2">
          <span class="text-xl">📚</span>
          <h3 class="text-base font-extrabold txt-main">Chọn Môn Học Đang Ôn Tập</h3>
        </div>
        <button onclick="closeModal('modal-subject-picker')" class="btn-soft p-1.5"><i data-lucide="x" class="w-4 h-4"></i></button>
      </div>
      <p class="px-5 pt-3 text-xs txt-muted">
        Chọn môn học để hệ thống tự động lọc đề thi, thẻ flashcard, bài tập và công cụ thực hành chuyên biệt cho môn đó.
      </p>
      <div id="subj-picker-list" class="p-5 space-y-2.5 overflow-y-auto max-h-[60vh]"></div>
    </div>
  </div>

  <!-- =====================================================================
       ACCOUNT PROFILE & ADMIN MANAGEMENT MODAL
       ===================================================================== -->
  <div id="modal-account-profile" class="hidden fixed inset-0 z-50 modal-overlay flex items-center justify-center p-4">
    <div class="uni-card w-full max-w-xl max-h-[90vh] flex flex-col overflow-hidden animate-fade-in" style="background: #0f1118; border: 1px solid rgba(255, 255, 255, 0.1);">
      <!-- Header -->
      <div class="p-5 flex items-center justify-between border-b" style="border-color: rgba(255, 255, 255, 0.08);">
        <div class="flex items-center gap-2.5">
          <div class="w-8 h-8 rounded-xl bg-gradient-to-tr from-indigo-500 to-purple-600 text-white font-black text-sm flex items-center justify-center">
            👤
          </div>
          <div>
            <h3 class="text-base font-extrabold txt-main">Hồ Sơ & Quản Trị Hệ Thống</h3>
            <div class="text-[11px] txt-muted">Bảo mật tài khoản & Đồng bộ tiến độ đám mây</div>
          </div>
        </div>
        <button onclick="closeModal('modal-account-profile')" class="btn-soft p-1.5"><i data-lucide="x" class="w-4 h-4"></i></button>
      </div>

      <!-- Tabs: Profile vs Admin (Admin only) -->
      <div class="flex px-5 pt-3 gap-2 border-b" style="border-color: rgba(255, 255, 255, 0.08);">
        <button type="button" id="acc-tab-profile-btn" onclick="switchAccountTab('profile')" class="tab-btn active px-4 py-2 text-xs font-extrabold border-b-2 border-indigo-500 text-white">
          👤 Tài Khoản Của Tôi
        </button>
        <button type="button" id="acc-tab-admin-btn" onclick="switchAccountTab('admin')" class="tab-btn px-4 py-2 text-xs font-extrabold border-b-2 border-transparent text-slate-400 hover:text-white">
          👥 Quản Lý Người Dùng (Admin)
        </button>
      </div>

      <!-- Panel 1: Profile & Sync -->
      <div id="acc-panel-profile" class="p-5 space-y-4 overflow-y-auto">
        <div class="p-4 rounded-2xl flex items-center justify-between" style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.06);">
          <div>
            <div id="acc-modal-fullname" class="text-base font-black text-white">Quản Trị Viên</div>
            <div id="acc-modal-username" class="text-xs font-mono text-indigo-400 mt-0.5">@admin</div>
          </div>
          <span id="acc-modal-role" class="badge-rose px-3 py-1 rounded-full text-xs font-black">👑 Quản Trị Viên</span>
        </div>

        <!-- Sync & Stats Grid -->
        <div class="grid grid-cols-3 gap-3 text-center">
          <div class="p-3 rounded-xl bg-white/5 border border-white/5">
            <div class="text-[11px] txt-muted">Đã thi</div>
            <div id="acc-modal-exams-count" class="text-sm font-black text-emerald-400 mt-0.5">0 bài</div>
          </div>
          <div class="p-3 rounded-xl bg-white/5 border border-white/5">
            <div class="text-[11px] txt-muted">Sổ câu sai</div>
            <div id="acc-modal-mistakes-count" class="text-sm font-black text-rose-400 mt-0.5">0 câu</div>
          </div>
          <div class="p-3 rounded-xl bg-white/5 border border-white/5">
            <div class="text-[11px] txt-muted">Chuỗi học</div>
            <div id="acc-modal-streak" class="text-sm font-black text-amber-400 mt-0.5">1 ngày 🔥</div>
          </div>
        </div>

        <!-- Cloud Sync Status Banner -->
        <div class="p-3.5 rounded-xl border border-emerald-500/30 bg-emerald-500/10 flex items-center justify-between text-xs">
          <div class="flex items-center gap-2">
            <span class="text-emerald-400">🟢</span>
            <span class="txt-main font-bold">Trạng thái đồng bộ: Đã kết nối máy chủ</span>
          </div>
          <button type="button" onclick="syncUserStateToServer(); showToast('Đã lưu tiến độ lên máy chủ!', 'success')" class="btn-soft px-3 py-1 text-[11px] font-bold">
            🔄 Đồng bộ ngay
          </button>
        </div>

        <!-- Logout Button -->
        <div class="pt-2">
          <button type="button" onclick="handleLogout()" class="btn-soft w-full py-2.5 text-xs font-extrabold text-rose-400 hover:bg-rose-500/10 flex items-center justify-center gap-2">
            <span>🚪</span> Đăng Xuất Khỏi Tài Khoản
          </button>
        </div>
      </div>

      <!-- Panel 2: Admin User Management -->
      <div id="acc-panel-admin" class="hidden p-5 space-y-4 overflow-y-auto">
        <div class="flex items-center justify-between">
          <h4 class="text-xs font-black uppercase tracking-wider txt-sub">Danh Sách Tài Khoản Đã Đăng Ký</h4>
          <button type="button" onclick="loadAdminUsersList()" class="btn-soft px-2.5 py-1 text-[11px] font-bold">🔄 Làm mới</button>
        </div>
        <div id="acc-admin-users-list" class="space-y-2.5 max-h-[50vh] overflow-y-auto"></div>
      </div>
    </div>
  </div>
"""

if 'id="modal-subject-picker"' not in html:
    html = html.replace('</body>', modals_html + "\n</body>")

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("Updated static/index.html refined UI successfully! Total length:", len(html))
