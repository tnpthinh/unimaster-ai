import os
import re

BASE_DIR = r"C:\Users\PC\.gemini\antigravity\scratch\unimaster-ai"
os.chdir(BASE_DIR)

html_path = "static/index.html"
with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update Floating Tutor container
old_container_marker = '<div id="floating-tutor-container"'
old_timed_marker = '<div id="modal-timed-exam"'

start_idx = content.find(old_container_marker)
end_idx = content.find(old_timed_marker)

if start_idx != -1 and end_idx != -1:
    new_tutor_html = '''<div id="floating-tutor-container" class="fixed bottom-20 sm:bottom-6 right-3 sm:right-6 z-50 flex flex-col items-end">
    <!-- Floating Trigger Button (Sleek Gradient Gem with Context Badge) -->
    <button id="floating-tutor-btn" onclick="toggleFloatingTutor()"
      class="group p-2.5 sm:px-4 sm:py-3 rounded-full sm:rounded-2xl shadow-2xl flex items-center gap-2 hover:scale-105 active:scale-95 transition-all relative"
      style="background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #c026d3 100%); border: 1.5px solid rgba(255, 255, 255, 0.25); box-shadow: 0 10px 25px -4px rgba(99, 102, 241, 0.5);"
      title="Gia Sư AI Ôn Thi (Nhấn phím T để bật/tắt)">
      <span class="relative flex h-2.5 w-2.5">
        <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
        <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
      </span>
      <span class="text-lg sm:text-xl">🤖</span>
      <span class="hidden sm:inline font-extrabold text-xs text-white tracking-wide">Gia Sư AI</span>
      <span id="floating-btn-subject-tag" class="hidden md:inline badge-brand text-[10px] px-1.5 py-0.5 rounded font-mono font-bold">Phím T</span>
      <span id="floating-btn-q-badge" class="hidden text-[10px] bg-white/20 text-white px-2 py-0.5 rounded-full font-bold"></span>
    </button>

    <!-- Floating Chat Window (Glassmorphism, Expandable, Multi-Persona, Voice) -->
    <div id="floating-tutor-window"
      class="hidden mt-2 w-[94vw] sm:w-[420px] max-h-[560px] uni-card flex flex-col overflow-hidden shadow-2xl border transition-all duration-200 animate-fade-in"
      style="background: color-mix(in srgb, var(--bg-surface) 96%, transparent); backdrop-filter: blur(24px); border-color: rgba(99, 102, 241, 0.4); box-shadow: 0 20px 40px -10px rgba(0,0,0,0.5);">
      
      <!-- Window Header -->
      <div class="p-3 flex items-center justify-between border-b" style="border-color: var(--border);">
        <div class="flex items-center gap-2 overflow-hidden">
          <div class="w-7 h-7 rounded-lg flex items-center justify-center text-white text-xs shrink-0" style="background: linear-gradient(135deg, #6366f1, #a855f7);">
            🤖
          </div>
          <div class="overflow-hidden">
            <h4 class="text-xs font-black txt-main flex items-center gap-1.5 leading-tight">
              <span>Gia Sư AI Trực Tuyến</span>
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 inline-block animate-pulse"></span>
            </h4>
            <div id="floating-tutor-context" class="text-[10px] txt-muted font-bold truncate max-w-[200px] sm:max-w-[240px]">Đang hỏi: Toàn bộ môn học</div>
          </div>
        </div>
        <div class="flex items-center gap-1">
          <button type="button" onclick="toggleFloatingTutorSize()" id="btn-ft-expand" class="btn-soft p-1.5 text-xs" title="Phóng to / Thu nhỏ">⛶</button>
          <button type="button" onclick="exportFloatingTutorNotes()" class="btn-soft p-1.5 text-xs" title="Xuất sổ tay ôn thi ra tệp">📄</button>
          <button type="button" onclick="clearFloatingTutorChat()" class="btn-soft p-1.5 text-xs" title="Xóa hội thoại">🗑️</button>
          <button type="button" onclick="toggleFloatingTutor()" class="btn-soft p-1.5 text-xs font-bold" title="Đóng (Phím Esc)">✕</button>
        </div>
      </div>

      <!-- Persona Selector Bar (4 Styles) -->
      <div class="px-2.5 py-1.5 border-b flex items-center gap-1 overflow-x-auto no-scrollbar text-[11px]" style="border-color: var(--border); background-color: var(--bg-subtle);">
        <span class="text-[10px] txt-muted font-extrabold uppercase shrink-0 mr-1">Phong cách:</span>
        <button type="button" onclick="setFloatingPersona('professor')" id="ft-persona-professor" class="ft-persona-btn active px-2 py-0.5 rounded-md font-bold shrink-0 transition-all">
          🎓 Giáo Sư
        </button>
        <button type="button" onclick="setFloatingPersona('feynman')" id="ft-persona-feynman" class="ft-persona-btn px-2 py-0.5 rounded-md font-bold shrink-0 transition-all">
          🧒 Feynman
        </button>
        <button type="button" onclick="setFloatingPersona('speed')" id="ft-persona-speed" class="ft-persona-btn px-2 py-0.5 rounded-md font-bold shrink-0 transition-all">
          ⚡ Giải Nhanh
        </button>
        <button type="button" onclick="setFloatingPersona('examiner')" id="ft-persona-examiner" class="ft-persona-btn px-2 py-0.5 rounded-md font-bold shrink-0 transition-all">
          🎤 Vấn Đáp
        </button>
      </div>

      <!-- Pinned Question Context Card (Shows when asking from a specific exam question) -->
      <div id="ft-pinned-question-container" class="hidden px-2.5 pt-2 pb-1">
        <div class="p-2.5 rounded-xl border flex items-start justify-between gap-2"
          style="background: rgba(99, 102, 241, 0.08); border-color: rgba(99, 102, 241, 0.25);">
          <div class="flex items-start gap-2 overflow-hidden flex-1">
            <span class="text-sm shrink-0">📌</span>
            <div class="overflow-hidden space-y-0.5">
              <div class="text-[11px] font-black text-indigo-400 truncate" id="ft-pinned-q-title">Đang xem: Câu 1</div>
              <div class="text-[10px] txt-muted font-semibold line-clamp-1" id="ft-pinned-q-body">Đề bài câu hỏi...</div>
            </div>
          </div>
          <button type="button" onclick="unpinTutorQuestion()" class="text-xs txt-muted hover:text-white px-1 py-0.5 rounded" title="Bỏ ghim câu này để hỏi chung">✕</button>
        </div>
      </div>

      <!-- Quick Action Chips (Dynamic based on whether question is pinned) -->
      <div id="ft-action-chips" class="p-2 border-b flex gap-1.5 overflow-x-auto no-scrollbar" style="border-color: var(--border); background-color: var(--bg-subtle);">
        <!-- Loaded dynamically by renderFloatingActionChips() -->
      </div>

      <!-- Messages Stream Box -->
      <div id="floating-chat-messages" class="p-3 overflow-y-auto space-y-3 flex-1 text-xs max-h-80 sm:max-h-96 min-h-52 leading-relaxed">
        <div class="flex items-start gap-2">
          <div class="w-6 h-6 rounded-md flex items-center justify-center bg-indigo-500/20 text-indigo-400 text-xs shrink-0">🤖</div>
          <div class="p-2.5 rounded-xl bg-white/5 border border-white/5 txt-sub max-w-[85%]">
            Xin chào! Tôi là Gia sư AI phụ trách môn <strong id="floating-welcome-subj" class="txt-brand">này</strong>. Bấm nút <strong>"Hỏi AI Câu Này"</strong> trong đề thi hoặc chọn chip bên trên để hỏi ngay tức thì!
          </div>
        </div>
      </div>

      <!-- Voice Listening Status Bar (Shown when recording) -->
      <div id="ft-voice-listening-bar" class="hidden px-3 py-1.5 text-[11px] font-bold text-red-400 bg-red-500/10 border-t border-red-500/20 flex items-center justify-between">
        <span class="flex items-center gap-1.5">
          <span class="w-2 h-2 rounded-full bg-red-500 animate-ping"></span>
          Đang lắng nghe giọng nói... Hãy nói câu hỏi của bạn!
        </span>
        <button type="button" onclick="stopFloatingVoiceInput()" class="underline text-[10px]">Dừng</button>
      </div>

      <!-- Input Footer -->
      <div class="p-2.5 border-t flex items-center gap-1.5" style="border-color: var(--border); background-color: var(--bg-surface);">
        <button type="button" onclick="toggleFloatingVoiceInput()" id="btn-ft-mic" class="btn-soft p-2 text-xs shrink-0" title="Nhập bằng giọng nói (Micro)">
          🎙️
        </button>
        <input id="floating-chat-input" type="text" placeholder="Hỏi AI bất kỳ điều gì về câu này / môn này..."
          onkeydown="if(event.key==='Enter') sendFloatingTutorMessage()"
          class="uni-input flex-1 px-3 py-2 text-xs font-bold" />
        <button type="button" onclick="sendFloatingTutorMessage()" class="btn-primary px-3.5 py-2 text-xs font-extrabold shrink-0 flex items-center gap-1">
          <span>Gửi</span> <span>➤</span>
        </button>
      </div>
    </div>
  </div>

  <!-- ===================================================================
       MODAL: PHÒNG THI THỬ GIỚI HẠN THỜI GIAN 60 PHÚT (40 CÂU)
       =================================================================== -->
  '''
    content = content[:start_idx] + new_tutor_html + content[end_idx:]
    print("Floating tutor replaced successfully!")
else:
    print("Could not find floating tutor container markers")

# 2. Add btn-ask-ai-current in exam-question-stage
hint_btn = '<button id="btn-ai-hint" onclick="requestAiHint()" title="Gợi ý tư duy AI (Phím H)" class="ai-chip-btn">\n                💡 Gợi ý AI\n              </button>'
ask_ai_btn = '''<button id="btn-ask-ai-current" onclick="askAiAboutCurrentExamQuestion()" title="Hỏi ngay Gia Sư AI về câu hỏi này (Phím T)" class="btn-primary !bg-gradient-to-r !from-indigo-600 !via-purple-600 !to-pink-600 px-3 py-1.5 rounded-xl text-xs font-black flex items-center gap-1.5 shadow-md hover:scale-105 active:scale-95 transition-all">
                <span class="animate-pulse">🤖</span>
                <span>Hỏi AI Câu Này</span>
                <span class="hidden md:inline text-[10px] opacity-75 bg-black/30 px-1 py-0.2 rounded font-mono">T</span>
              </button>
              '''

if 'id="btn-ask-ai-current"' not in content and hint_btn in content:
    content = content.replace(hint_btn, ask_ai_btn + hint_btn)
    print("btn-ask-ai-current added to exam-question-stage!")

# 3. Add ask AI button to q-feedback-panel
deep_btn = '<button onclick="triggerDeepAnalysis()" class="ai-chip-btn">'
ask_ai_feedback_btn = '''<button onclick="askAiAboutCurrentExamQuestion()" class="btn-primary !bg-gradient-to-r !from-indigo-600 !to-purple-600 px-3 py-1.5 rounded-xl text-xs font-black flex items-center gap-1.5 shadow-sm hover:scale-105 active:scale-95 transition-all">
                <span>🤖</span> Hỏi Gia Sư AI Chi Tiết
              </button>
              '''

if 'Hỏi Gia Sư AI Chi Tiết' not in content and deep_btn in content:
    content = content.replace(deep_btn, ask_ai_feedback_btn + deep_btn)
    print("Hỏi Gia Sư AI Chi Tiết added to q-feedback-panel!")

# 4. Add ask AI button to modal-timed-exam
timed_badge_marker = '<span id="timed-q-index-badge" class="badge-brand text-xs px-3 py-1 rounded-lg font-bold">Câu 1 / 40</span>\n            <span id="timed-q-topic-badge" class="badge-subtle text-xs px-2.5 py-0.5 rounded font-bold">Chủ đề</span>'
timed_ask_btn = '''<div class="flex items-center gap-2">
              <span id="timed-q-index-badge" class="badge-brand text-xs px-3 py-1 rounded-lg font-bold">Câu 1 / 40</span>
              <span id="timed-q-topic-badge" class="badge-subtle text-xs px-2.5 py-0.5 rounded font-bold">Chủ đề</span>
            </div>
            <button type="button" onclick="askAiAboutCurrentTimedQuestion()" class="btn-primary !bg-gradient-to-r !from-indigo-600 !to-purple-600 px-3 py-1 text-xs font-black flex items-center gap-1.5 shadow-md hover:scale-105 active:scale-95 transition-all">
              <span>🤖</span> Hỏi AI Câu Này
            </button>'''

if 'askAiAboutCurrentTimedQuestion' not in content and timed_badge_marker in content:
    content = content.replace(timed_badge_marker, timed_ask_btn)
    print("askAiAboutCurrentTimedQuestion added to modal-timed-exam!")

with open(html_path, "w", encoding="utf-8") as f:
    f.write(content)

print("static/index.html updated successfully!")
