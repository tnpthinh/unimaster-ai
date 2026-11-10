import re

html_path = r'C:\Users\PC\.gemini\antigravity\scratch\unimaster-ai\static\index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Add #btn-toggle-discussion to Question Toolbar
toolbar_target = '''<button id="btn-5050" onclick="useLifeline5050()" title="Loại 2 đáp án sai (Phím F)" class="btn-soft px-2.5 py-1.5 text-xs">
                ✂️ 50/50
              </button>'''

toolbar_replacement = '''<button id="btn-5050" onclick="useLifeline5050()" title="Loại 2 đáp án sai (Phím F)" class="btn-soft px-2.5 py-1.5 text-xs">
                ✂️ 50/50
              </button>
              <button id="btn-toggle-discussion" onclick="toggleQuestionDiscussionBox()" title="Bình luận & Mẹo nhớ sinh viên câu này" class="btn-soft px-2.5 py-1.5 text-xs flex items-center gap-1.5 text-cyan-400 hover:text-cyan-300">
                <span>💬</span>
                <span class="hidden sm:inline">Bình luận</span>
                <span id="q-toolbar-disc-count" class="badge-brand px-1.5 py-0.2 rounded-full text-[10px] font-bold">0</span>
              </button>'''

if toolbar_target in c:
    c = c.replace(toolbar_target, toolbar_replacement, 1)
    print("1. Added #btn-toggle-discussion to toolbar")
else:
    print("WARNING: toolbar_target not found!")

# 2. Add #q-key-terms-row under #q-prompt-text
prompt_target = '''<div id="q-body-wrapper" class="space-y-4">
            <div id="q-prompt-text" class="question-title-text"></div>
            <div id="q-image-wrapper" class="hidden"></div>'''

prompt_replacement = '''<div id="q-body-wrapper" class="space-y-4">
            <div id="q-prompt-text" class="question-title-text"></div>
            <!-- Clickable Key Concept Chips (Click any term to ask AI) -->
            <div id="q-key-terms-row" class="hidden flex flex-wrap items-center gap-1.5 pt-1"></div>
            <div id="q-image-wrapper" class="hidden"></div>'''

if prompt_target in c:
    c = c.replace(prompt_target, prompt_replacement, 1)
    print("2. Added #q-key-terms-row under #q-prompt-text")
else:
    print("WARNING: prompt_target not found!")

# 3. Upgrade #btn-ft-expand in floating tutor
expand_target = '''<button type="button" onclick="toggleFloatingTutorSize()" id="btn-ft-expand" class="btn-soft p-1.5 text-xs" title="Phóng to / Thu nhỏ">⛶</button>'''
expand_replacement = '''<button type="button" onclick="toggleFloatingTutorSize()" id="btn-ft-expand" class="flex items-center gap-1.5 px-2.5 py-1 rounded-xl text-xs font-black shadow-sm transition-all bg-gradient-to-r from-violet-600 to-indigo-600 hover:from-violet-500 hover:to-indigo-500 text-white border border-white/20 active:scale-95" title="Phóng to toàn màn hình">
            <svg id="ft-expand-svg" class="w-3.5 h-3.5 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M15 3h6v6M9 21H3v-6M21 3l-7 7M3 21l7-7"/>
            </svg>
            <span id="ft-expand-label">Phóng To</span>
          </button>'''

if expand_target in c:
    c = c.replace(expand_target, expand_replacement, 1)
    print("3. Upgraded #btn-ft-expand with sharp SVG and label")
else:
    print("WARNING: expand_target not found!")

# 4. Move #q-community-discussion-box outside #q-feedback-panel
# First extract #q-community-discussion-box
disc_match = re.search(r'(<!-- Contextual Community Discussion & Verified TA Tips -->\s*<div id="q-community-discussion-box"[\s\S]*?</div>\s*</div>\s*</div>)', c)
if disc_match:
    disc_html = '''<!-- Contextual Community Discussion & Verified TA Tips (Available Anytime) -->
          <div id="q-community-discussion-box" class="hidden p-4 rounded-2xl space-y-3 animate-fade-in" style="background-color: var(--bg-subtle); border: 1.5px solid var(--brand-border);">
            <div class="flex flex-wrap items-center justify-between gap-2 border-b pb-2.5" style="border-color: var(--border);">
              <div class="flex items-center gap-2">
                <span class="text-base">💬</span>
                <div>
                  <span class="text-xs font-black txt-main">Thảo Luận & Mẹo Nhớ Sinh Viên Cùng Câu Này</span>
                  <p class="text-[10px] txt-muted">Chia sẻ bí kíp nhớ nhanh, tra cứu công thức hoặc hỏi trợ giảng</p>
                </div>
              </div>
              <div class="flex items-center gap-2">
                <span id="q-discussion-count-badge" class="badge-brand px-2 py-0.5 rounded-full text-[11px] font-bold">0 bình luận</span>
                <button type="button" onclick="toggleQuestionDiscussionBox(false)" class="btn-soft p-1 text-xs" title="Đóng thảo luận">✕</button>
              </div>
            </div>
            <div id="q-discussion-list" class="space-y-2.5 max-h-56 overflow-y-auto pr-1"></div>
            <div class="flex flex-wrap sm:flex-nowrap gap-2 pt-1.5">
              <input id="q-disc-author-input" type="text" placeholder="Tên bạn..." class="uni-input w-28 sm:w-36 px-2.5 py-1.5 !text-xs font-semibold" style="background-color: var(--bg-surface);" />
              <input id="q-disc-content-input" type="text" placeholder="Chia sẻ mẹo nhớ hoặc hỏi về câu này..."
                onkeydown="if(event.key==='Enter') submitQuestionDiscussion()"
                class="uni-input flex-1 px-3 py-1.5 !text-xs" style="background-color: var(--bg-surface);" />
              <button type="button" onclick="submitQuestionDiscussion()" class="btn-primary !bg-cyan-600 hover:!bg-cyan-500 px-4 py-1.5 text-xs font-bold shrink-0">
                <span>Gửi</span> 🚀
              </button>
            </div>
          </div>'''
    
    # Remove from feedback panel
    c = c.replace(disc_match.group(0), '', 1)
    
    # Insert right before bottom navigation
    nav_marker = '<!-- Bottom Navigation -->'
    c = c.replace(nav_marker, disc_html + '\n\n          ' + nav_marker, 1)
    print("4. Relocated #q-community-discussion-box outside #q-feedback-panel")
else:
    print("WARNING: disc_match not found!")

# 5. Add Archive Sub-Tabs in #modal-exam-history
exam_hist_target = '''<!-- Quick Stats Strip -->
      <div class="px-5 py-3 border-b shrink-0 flex items-center justify-between gap-4 flex-wrap text-xs font-bold" style="background-color: var(--bg-subtle); border-color: var(--border);">'''

exam_hist_replacement = '''<!-- Sub-Tabs: Active vs Safe Archive -->
      <div class="px-5 py-2.5 border-b shrink-0 flex items-center justify-between gap-3 flex-wrap" style="background-color: var(--bg-subtle); border-color: var(--border);">
        <div class="flex items-center gap-2">
          <button type="button" id="tab-exam-hist-active" onclick="switchExamHistoryTab('active')" class="px-3.5 py-1.5 rounded-xl text-xs font-black transition-all bg-indigo-600 text-white shadow-sm">
            📂 Đang Hiển Thị (<span id="exam-hist-active-count">0</span>)
          </button>
          <button type="button" id="tab-exam-hist-archive" onclick="switchExamHistoryTab('archive')" class="px-3.5 py-1.5 rounded-xl text-xs font-bold transition-all text-amber-400 hover:bg-white/5">
            📦 Kho Lưu Trữ Đã Xóa (<span id="exam-hist-archive-count">0</span>)
          </button>
        </div>
        <div id="exam-hist-archive-actions" class="hidden flex items-center gap-2">
          <button type="button" onclick="restoreAllLocalExamHistory()" class="btn-primary !bg-emerald-600 hover:!bg-emerald-500 px-3.5 py-1.5 text-xs font-black flex items-center gap-1.5 shadow-md">
            <span>🔄</span> <span>Khôi Phục Toàn Bộ</span>
          </button>
        </div>
      </div>

      <!-- Quick Stats Strip -->
      <div class="px-5 py-3 border-b shrink-0 flex items-center justify-between gap-4 flex-wrap text-xs font-bold" style="background-color: var(--bg-subtle); border-color: var(--border);">'''

if exam_hist_target in c:
    c = c.replace(exam_hist_target, exam_hist_replacement, 1)
    print("5. Added Archive Sub-Tabs to #modal-exam-history")
else:
    print("WARNING: exam_hist_target not found!")

# 6. Add Archive Sub-Tabs in #modal-tutor-chat-history
tutor_hist_target = '''<!-- Search & Filter Strip -->
      <div class="p-3 sm:px-5 border-b shrink-0 flex items-center gap-2 flex-wrap" style="background-color: var(--bg-subtle); border-color: var(--border);">'''

tutor_hist_replacement = '''<!-- Sub-Tabs: Active vs Safe Archive -->
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

      <!-- Search & Filter Strip -->
      <div class="p-3 sm:px-5 border-b shrink-0 flex items-center gap-2 flex-wrap" style="background-color: var(--bg-subtle); border-color: var(--border);">'''

if tutor_hist_target in c:
    c = c.replace(tutor_hist_target, tutor_hist_replacement, 1)
    print("6. Added Archive Sub-Tabs to #modal-tutor-chat-history")
else:
    print("WARNING: tutor_hist_target not found!")

# 7. Add #text-select-ai-bubble before </body>
bubble_target = '</body>'
bubble_html = '''<!-- Floating Quick-Ask AI Bubble upon Text Selection -->
  <div id="text-select-ai-bubble" class="hidden fixed z-[9999] transform -translate-x-1/2 -translate-y-full pb-2 transition-opacity duration-150 pointer-events-auto">
    <button type="button" onclick="askAiAboutSelectedTerm()" class="flex items-center gap-2 px-3.5 py-2 rounded-2xl text-xs font-black text-white shadow-2xl bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 hover:scale-105 active:scale-95 border border-white/30 backdrop-blur-md cursor-pointer">
      <span class="animate-pulse text-sm">🤖</span>
      <span>Hỏi AI từ này:</span>
      <span id="text-select-ai-word" class="max-w-[150px] truncate underline decoration-amber-300 font-extrabold text-amber-200">...</span>
    </button>
  </div>
</body>'''

if bubble_target in c and 'id="text-select-ai-bubble"' not in c:
    c = c.replace(bubble_target, bubble_html, 1)
    print("7. Added #text-select-ai-bubble before </body>")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(c)

print("Done updating static/index.html successfully!")
