import re

html_path = r'C:\Users\PC\.gemini\antigravity\scratch\unimaster-ai\static\index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update subtab label
html = html.replace(
    '<button onclick="switchSettingsTab(\'ai\')" data-stab="ai" class="preset-pill !rounded-b-none !border-b-0 text-xs whitespace-nowrap">🤖 Gemini AI</button>',
    '<button onclick="switchSettingsTab(\'ai\')" data-stab="ai" class="preset-pill !rounded-b-none !border-b-0 text-xs whitespace-nowrap">⚡ AI: ChatGPT & Gemini</button>'
)

# 2. Add ChatGPT Card into #stab-panel-ai
target_marker = '<div id="stab-panel-ai" class="hidden space-y-4">'
chatgpt_card = """<div id="stab-panel-ai" class="hidden space-y-5">
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

          <!-- Divider -->
          <div class="flex items-center gap-3 pt-1">
            <div class="h-px bg-slate-700/60 flex-1"></div>
            <span class="text-[11px] font-extrabold uppercase tracking-wider txt-muted">Dàn Dự Phòng Gemini Luân Phiên</span>
            <div class="h-px bg-slate-700/60 flex-1"></div>
          </div>"""

if target_marker in html:
    html = html.replace(target_marker, chatgpt_card, 1)
    print("Injected ChatGPT Card into index.html")
else:
    print("Target marker not found in index.html")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Done updating static/index.html")
