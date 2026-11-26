# -*- coding: utf-8 -*-
import os
import re

def patch_index_html():
    path = "static/index.html"
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    idx1 = html.find('id="q-official-expl-box"')
    if idx1 == -1:
        print("Error: q-official-expl-box not found")
        return
    
    # Tìm thẻ đóng </div> của q-official-expl-box
    close_div = html.find('</div>', idx1)
    if close_div == -1:
        print("Error: close_div not found")
        return
    end_box = close_div + len('</div>')

    idx2 = html.find('id="q-feedback-more-ai-wrap"')
    if idx2 == -1:
        print("Error: q-feedback-more-ai-wrap not found")
        return
    
    # Tìm đoạn bắt đầu của <div id="q-feedback-more-ai-wrap"
    start_wrap = html.rfind('<div', end_box, idx2)
    if start_wrap == -1:
        start_wrap = idx2

    replacement = '''
            <!-- 3 Calm Primary AI Pills + Expand Toggle -->
            <div class="flex flex-wrap items-center gap-2">
              <button id="btn-exam-feynman-tutor" onclick="askAiAboutCurrentExamQuestion(true)" class="btn-primary !bg-gradient-to-r !from-amber-500 !via-indigo-600 !to-purple-600 px-3.5 py-1.5 rounded-xl text-xs font-black flex items-center gap-1.5 shadow-sm hover:scale-[1.02] active:scale-95 transition-all" title="Bấm là kích hoạt Feynman giảng giải bản chất sâu sắc ngay lập tức">
                <span>🧒</span> <span>Gia Sư AI Giải Chi Tiết (Feynman)</span>
              </button>
              <button type="button" id="btn-toggle-tutor-style-config" onclick="toggleExamTutorStylePanel()" class="btn-soft px-2.5 py-1.5 rounded-xl text-xs font-bold flex items-center gap-1.5 transition-all border border-indigo-500/30 hover:border-indigo-400" title="Tùy chỉnh phong cách & giọng điệu giảng dạy">
                <span>🎨</span> <span>Phong cách</span>
                <span id="exam-tutor-active-style-badge" class="badge-brand px-1.5 py-0.5 rounded-md text-[10px] font-black truncate max-w-[120px]">Feynman</span>
                <span id="exam-tutor-style-chevron" class="opacity-70">▾</span>
              </button>
              <button id="btn-explain-mistake" onclick="triggerExplainMyMistake()" class="ai-chip-btn">
                <span>🩺</span> Sao tôi chọn nhầm?
              </button>
              <button onclick="triggerAiMnemonic()" class="ai-chip-btn">
                <span>⚡</span> Mẹo nhớ 5s
              </button>
              <button type="button" onclick="openEditQuestionModal()" class="ai-chip-btn" title="Đáp án sai hoặc câu lỗi? Bấm để sửa ngay & đẩy lên GitHub">
                <span>✏️</span> Sửa đáp án / câu lỗi
              </button>
              <button type="button" id="btn-feedback-more-ai" onclick="toggleFeedbackExtraAiTools()" class="btn-soft px-3 py-1.5 rounded-xl text-xs font-bold flex items-center gap-1 ml-auto">
                <span>✨</span> <span>Mở rộng AI</span> <span id="feedback-more-ai-chevron">▾</span>
              </button>
            </div>

            <!-- Bảng Tùy Chỉnh Phong Cách & Sư Phạm Gia Sư AI Phòng Thi (Collapsible) -->
            <div id="exam-tutor-style-panel" class="hidden p-3.5 rounded-2xl border space-y-3 animate-fade-in shadow-md" style="background: color-mix(in srgb, var(--bg-surface) 95%, transparent); border-color: color-mix(in srgb, var(--brand) 40%, var(--border));">
              <!-- Header của Panel -->
              <div class="flex items-center justify-between gap-2 border-b pb-2" style="border-color: var(--border);">
                <div class="flex items-center gap-2">
                  <span class="text-sm">🎨</span>
                  <div>
                    <span class="text-xs font-black txt-main">Tùy Chỉnh Phong Cách Giảng Dạy & Phương Pháp AI</span>
                    <p class="text-[10px] txt-muted">Bấm nút trên là bật Feynman ngay, tự ghi phong cách riêng hoặc bấm chip tự điền mẫu bên dưới</p>
                  </div>
                </div>
                <div class="flex items-center gap-1.5">
                  <button type="button" onclick="resetExamTutorStyleToDefault()" class="btn-soft px-2 py-0.5 text-[10.5px] font-semibold text-slate-400 hover:text-white" title="Trở về phong cách Feynman mặc định">↺ Mặc định</button>
                  <button type="button" onclick="toggleExamTutorStylePanel(false)" class="btn-soft p-1 text-xs" title="Thu gọn bảng">✕</button>
                </div>
              </div>

              <!-- Hàng 1: Giọng giảng (Persona) + Độ dài phản hồi -->
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
                <!-- Giọng Giảng Persona -->
                <div class="space-y-1">
                  <span class="text-[10.5px] font-bold txt-muted flex items-center gap-1">
                    <span>🎭</span> Giọng giảng (Persona):
                  </span>
                  <div class="flex items-center gap-1 flex-wrap">
                    <button type="button" onclick="setExamPersonaDirect('feynman')" data-exam-persona="feynman" class="exam-persona-btn active px-2.5 py-1 rounded-xl text-xs font-bold border transition-all">🧒 Feynman</button>
                    <button type="button" onclick="setExamPersonaDirect('professor')" data-exam-persona="professor" class="exam-persona-btn px-2.5 py-1 rounded-xl text-xs font-bold border transition-all">🎓 Giáo Sư</button>
                    <button type="button" onclick="setExamPersonaDirect('speed')" data-exam-persona="speed" class="exam-persona-btn px-2.5 py-1 rounded-xl text-xs font-bold border transition-all">⚡ Giải Nhanh</button>
                    <button type="button" onclick="setExamPersonaDirect('examiner')" data-exam-persona="examiner" class="exam-persona-btn px-2.5 py-1 rounded-xl text-xs font-bold border transition-all">🎤 Vấn Đáp</button>
                  </div>
                </div>

                <!-- Độ Dài Phản Hồi -->
                <div class="space-y-1">
                  <span class="text-[10.5px] font-bold txt-muted flex items-center gap-1">
                    <span>📏</span> Độ dài giải thích:
                  </span>
                  <div class="flex items-center gap-1 flex-wrap">
                    <button type="button" onclick="setExamLengthDirect('detailed')" data-exam-length="detailed" class="exam-length-btn active px-2.5 py-1 rounded-xl text-xs font-bold border transition-all">📖 Chi tiết (Mặc định)</button>
                    <button type="button" onclick="setExamLengthDirect('concise')" data-exam-length="concise" class="exam-length-btn px-2.5 py-1 rounded-xl text-xs font-bold border transition-all">⚡ Gọn (5s)</button>
                  </div>
                </div>
              </div>

              <!-- Hàng 2: Tự Điền Nhanh Phong Cách (Preset Chips 1-Chạm) -->
              <div class="space-y-1.5">
                <span class="text-[10.5px] font-bold txt-muted flex items-center justify-between">
                  <span class="flex items-center gap-1"><span>⚡</span> Tự điền phong cách mẫu (1-chạm):</span>
                  <span class="text-[10px] text-indigo-400">Bấm chip để điền & lưu ngay</span>
                </span>
                <div class="flex items-center gap-1.5 flex-wrap">
                  <button type="button" data-exam-preset="feynman_pure" onclick="applyTutorPresetStyle('feynman_pure')" class="exam-preset-chip px-2.5 py-1 rounded-xl text-[11px] font-bold border transition-all flex items-center gap-1 hover:border-amber-400">
                    🧒 Feynman Dễ Hiểu
                  </button>
                  <button type="button" data-exam-preset="gen_z" onclick="applyTutorPresetStyle('gen_z')" class="exam-preset-chip px-2.5 py-1 rounded-xl text-[11px] font-bold border transition-all flex items-center gap-1 hover:border-purple-400">
                    🌈 Gen Z Bắt Trend
                  </button>
                  <button type="button" data-exam-preset="root_cause" onclick="applyTutorPresetStyle('root_cause')" class="exam-preset-chip px-2.5 py-1 rounded-xl text-[11px] font-bold border transition-all flex items-center gap-1 hover:border-cyan-400">
                    🔍 Gốc Từ & Bản Chất
                  </button>
                  <button type="button" data-exam-preset="trap_buster" onclick="applyTutorPresetStyle('trap_buster')" class="exam-preset-chip px-2.5 py-1 rounded-xl text-[11px] font-bold border transition-all flex items-center gap-1 hover:border-rose-400">
                    🎯 Chốt Bẫy 5s
                  </button>
                  <button type="button" data-exam-preset="socratic" onclick="applyTutorPresetStyle('socratic')" class="exam-preset-chip px-2.5 py-1 rounded-xl text-[11px] font-bold border transition-all flex items-center gap-1 hover:border-emerald-400">
                    💡 Socratic Gợi Mở
                  </button>
                  <button type="button" data-exam-preset="clinical_sim" onclick="applyTutorPresetStyle('clinical_sim')" class="exam-preset-chip px-2.5 py-1 rounded-xl text-[11px] font-bold border transition-all flex items-center gap-1 hover:border-amber-400">
                    🩺 Thực Chiến / Lâm Sàng
                  </button>
                </div>
              </div>

              <!-- Hàng 3: Ô Tự Ghi Phong Cách (Custom Style Textarea) -->
              <div class="space-y-1.5">
                <div class="flex items-center justify-between text-[10.5px]">
                  <span class="font-bold txt-muted flex items-center gap-1">
                    <span>✍️</span> Tự ghi phong cách của bạn (Prompt sư phạm riêng):
                  </span>
                  <span id="exam-tutor-save-status" class="text-[10px] text-emerald-400 font-bold">Đã lưu ✓</span>
                </div>
                <div class="flex gap-2">
                  <textarea id="exam-tutor-custom-style" rows="2"
                    oninput="handleExamCustomStyleInput(this.value)"
                    placeholder="Tự ghi phong cách bất kỳ... VD: Dùng ví dụ đời thường cho người mất gốc, giọng Gen Z hài hước, phân tích vì sao phương án khác sai..."
                    class="uni-input flex-1 px-3 py-2 text-xs leading-relaxed resize-none rounded-xl" style="background-color: var(--bg-subtle);"></textarea>
                </div>
              </div>

              <!-- Hàng 4: Nút Kích Hoạt Nhanh với Cấu Hình Này -->
              <div class="flex items-center justify-between gap-2 pt-1">
                <div class="text-[10px] txt-muted">
                  AI sẽ áp dụng phong cách này trong mọi giải thích chi tiết & hỏi đáp ngữ cảnh.
                </div>
                <button type="button" onclick="askAiAboutCurrentExamQuestion(true)" class="btn-primary px-3.5 py-1.5 text-xs font-black rounded-xl flex items-center gap-1.5 shadow-sm hover:scale-[1.02] active:scale-95 transition-all">
                  <span>🚀</span> <span>Áp Dụng & Giải Thích Ngay</span>
                </button>
              </div>
            </div>

            '''
    html = html[:end_box] + "\n" + replacement + html[start_wrap:]
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("Successfully patched static/index.html")

if __name__ == "__main__":
    patch_index_html()
