import re

css_path = r'C:\Users\PC\.gemini\antigravity\scratch\unimaster-ai\static\style.css'
with open(css_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Replace zen-active rules
zen_pattern = r'/\* Zen Mode & Fullscreen.*?(?=/\* Animations)'
new_zen = """/* Zen Mode & Fullscreen (Toàn màn hình & Tối đa hóa kích cỡ câu hỏi / chữ) */
body.zen-active header,
body.zen-active .mobile-bottom-nav,
body.zen-active #global-stat-ribbon {
  display: none !important;
}
body.zen-active main:has(#view-exam:not(.hidden)) {
  max-width: 100% !important;
  width: 98vw !important;
  margin: 0.25rem auto !important;
  padding: 0.5rem 1rem !important;
}
body.zen-active #view-exam {
  max-width: 100% !important;
  width: 100% !important;
}
/* Keep top bar compact and aligned */
body.zen-active #exam-active-screen > div.uni-card:first-child {
  min-height: unset !important;
  display: flex !important;
  flex-direction: row !important;
  align-items: center !important;
  justify-content: space-between !important;
  padding: 0.75rem 1.25rem !important;
  margin-bottom: 0.75rem !important;
}
/* Question stage expands fully with large, crisp, comfortable typography */
body.zen-active #exam-question-stage {
  max-width: 100% !important;
  min-height: calc(100vh - 6.5rem) !important;
  display: flex !important;
  flex-direction: column !important;
  justify-content: space-between !important;
  padding: 1.5rem 2.25rem !important;
  border-radius: 1.5rem !important;
}
body.zen-active #q-prompt-text {
  font-size: clamp(1.25rem, 2.2vw, 1.7rem) !important;
  line-height: 1.75 !important;
  font-weight: 700 !important;
  color: var(--text-main) !important;
  margin: 1rem 0 !important;
}
body.zen-active .option-row {
  padding: 1.2rem 1.6rem !important;
  font-size: clamp(1.05rem, 1.5vw, 1.25rem) !important;
  border-radius: 1.2rem !important;
}
body.zen-active .option-row .opt-badge {
  width: 2.4rem !important;
  height: 2.4rem !important;
  font-size: 1.1rem !important;
}
body.zen-active #exit-zen-btn {
  display: inline-flex !important;
  top: 1rem !important;
  right: 1.5rem !important;
  z-index: 100 !important;
}
.exam-paused-blur { filter: blur(12px); pointer-events: none; user-select: none; }

"""

text = re.sub(zen_pattern, new_zen, text, flags=re.DOTALL)

# Update floating tutor styles
tutor_pattern = r'/\* Enhanced Floating AI Tutor.*?(?=\.ft-persona-btn)'
new_tutor = """/* Enhanced Floating AI Tutor (Docked chế độ thường & Centered Modal khi Mở Rộng) */
#floating-tutor-window {
  width: min(520px, 95vw) !important;
  max-width: 520px !important;
  height: min(78vh, 720px) !important;
  max-height: 80vh !important;
  border-radius: 1.25rem !important;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.8), 0 0 30px -5px var(--brand-glow) !important;
  margin-bottom: 0.25rem !important;
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
}

#floating-tutor-window.expanded {
  position: fixed !important;
  top: 50% !important;
  left: 50% !important;
  transform: translate(-50%, -50%) !important;
  bottom: auto !important;
  right: auto !important;
  width: min(1060px, 96vw) !important;
  max-width: 1060px !important;
  height: min(88vh, 880px) !important;
  max-height: 90vh !important;
  margin: 0 !important;
  border-radius: 1.5rem !important;
  z-index: 9999 !important;
  box-shadow: 0 30px 80px -10px rgba(0, 0, 0, 0.95), 0 0 50px rgba(99, 102, 241, 0.4) !important;
}

#floating-chat-messages {
  max-height: none !important;
  flex: 1 1 auto !important;
  overflow-y: auto !important;
  scroll-behavior: smooth;
  padding: 1.25rem !important;
}

#floating-tutor-window.expanded #floating-chat-messages {
  font-size: 0.95rem !important;
  line-height: 1.7 !important;
  padding: 1.5rem 2rem !important;
}

#floating-tutor-window.expanded #ft-pinned-question-container {
  padding: 0.75rem 1.25rem !important;
}

@media (max-width: 640px) {
  #floating-tutor-window {
    width: 96vw !important;
    height: 78vh !important;
    max-height: 80vh !important;
  }
  #floating-tutor-window.expanded {
    width: 98vw !important;
    height: 92vh !important;
    max-height: 94vh !important;
    border-radius: 1rem !important;
  }
}
"""

text = re.sub(tutor_pattern, new_tutor, text, flags=re.DOTALL)

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated static/style.css successfully")
