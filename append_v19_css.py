css_path = r'C:\Users\PC\.gemini\antigravity\scratch\unimaster-ai\static\style.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

v19_css = '''
/* =========================================================================
   UniMaster v19: Full-Screen AI Tutor, Interactive Code & Safe Archive Styles
   ========================================================================= */

/* 1. Full-Screen AI Tutor Expansion */
#floating-tutor-container.tutor-expanded-parent {
  position: fixed !important;
  inset: 0 !important;
  width: 100vw !important;
  height: 100vh !important;
  max-width: 100vw !important;
  max-height: 100vh !important;
  z-index: 99999 !important;
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  justify-content: center !important;
  background: rgba(10, 15, 30, 0.78) !important;
  backdrop-filter: blur(14px) !important;
  padding: 1rem !important;
  margin: 0 !important;
  left: 0 !important;
  top: 0 !important;
  right: 0 !important;
  bottom: 0 !important;
}

#floating-tutor-container.tutor-expanded-parent #floating-tutor-window {
  width: 96vw !important;
  max-width: 1440px !important;
  height: 94vh !important;
  max-height: 94vh !important;
  display: flex !important;
  flex-direction: column !important;
  border-radius: 1.5rem !important;
  border: 1.5px solid rgba(139, 92, 246, 0.45) !important;
  box-shadow: 0 30px 70px -15px rgba(0, 0, 0, 0.8) !important;
}

#floating-tutor-container.tutor-expanded-parent #ft-chat-messages {
  flex: 1 1 auto !important;
  max-height: calc(94vh - 180px) !important;
  overflow-y: auto !important;
  font-size: 1.05rem !important;
  line-height: 1.7 !important;
  padding: 1.5rem !important;
}

#floating-tutor-container.tutor-expanded-parent #ft-pinned-question-box {
  padding: 0.9rem 1.2rem !important;
}

/* 2. Interactive Code Line Ask AI */
.code-line-tr {
  cursor: pointer;
  transition: background-color 0.15s ease;
}
.code-line-tr:hover {
  background-color: rgba(99, 102, 241, 0.16) !important;
}
.code-line-tr:hover .code-line-ai-pill {
  opacity: 1 !important;
  transform: scale(1) !important;
}
.code-line-ai-pill {
  opacity: 0;
  transform: scale(0.9);
  transition: all 0.15s cubic-bezier(0.16, 1, 0.3, 1);
}

/* 3. Clickable Key Concept Chips under question */
.q-concept-chip {
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  border: 1px solid rgba(99, 102, 241, 0.4);
  background: rgba(99, 102, 241, 0.12);
  color: #a5b4fc;
  font-size: 0.75rem;
  font-weight: 700;
  padding: 0.25rem 0.65rem;
  border-radius: 9999px;
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
}
.q-concept-chip:hover {
  background: rgba(99, 102, 241, 0.3);
  border-color: #818cf8;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.25);
  color: #ffffff;
}

/* 4. Text Selection Floating AI Bubble */
@keyframes popBubble {
  0% { opacity: 0; transform: translate(-50%, -85%) scale(0.9); }
  100% { opacity: 1; transform: translate(-50%, -100%) scale(1); }
}
#text-select-ai-bubble:not(.hidden) {
  display: block !important;
  animation: popBubble 0.18s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

/* 5. Safe Archive UI styling */
.archive-item-card {
  border: 1.5px dashed var(--border);
  background-color: var(--bg-surface);
  transition: all 0.2s ease;
}
.archive-item-card:hover {
  border-color: var(--brand);
  background-color: var(--bg-subtle);
}
'''

if 'tutor-expanded-parent' not in css:
    css += '\n' + v19_css
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(css)
    print("Added v19 styles to static/style.css successfully!")
else:
    print("v19 styles already present in static/style.css")
