html_path = r'C:\Users\PC\.gemini\antigravity\scratch\unimaster-ai\static\index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    c = f.read()

target = '<!-- Search & Filter Bar -->'
subtab_html = '''<!-- Sub-Tabs: Active vs Safe Archive -->
      <div class="px-5 py-2.5 border-b shrink-0 flex items-center justify-between gap-3 flex-wrap" style="background-color: var(--bg-subtle); border-color: var(--border);">
        <div class="flex items-center gap-2">
          <button type="button" id="tab-tutor-hist-active" onclick="switchTutorHistoryTab('active')" class="px-3.5 py-1.5 rounded-xl text-xs font-black transition-all bg-indigo-600 text-white shadow-sm">
            📂 Đang Trò Chuyện (<span id="tutor-hist-active-count">0</span>)
          </button>
          <button type="button" id="tab-tutor-hist-archive" onclick="switchTutorHistoryTab('archive')" class="px-3.5 py-1.5 rounded-xl text-xs font-bold transition-all text-amber-400 hover:bg-white/5">
            📦 Kho Lưu Trữ Đã Xóa (<span id="tutor-hist-archive-count">0</span>)
          </button>
        </div>
        <div id="tutor-hist-archive-actions" class="hidden flex items-center gap-2">
          <button type="button" onclick="restoreAllTutorHistory()" class="btn-primary !bg-emerald-600 hover:!bg-emerald-500 px-3.5 py-1.5 text-xs font-black flex items-center gap-1.5 shadow-md">
            <span>🔄</span> <span>Khôi Phục Toàn Bộ</span>
          </button>
        </div>
      </div>

      <!-- Search & Filter Bar -->'''

if target in c and 'id="tab-tutor-hist-active"' not in c:
    c = c.replace(target, subtab_html, 1)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(c)
    print("Added subtabs to modal-tutor-chat-history successfully!")
else:
    print("Already added or target not found")
