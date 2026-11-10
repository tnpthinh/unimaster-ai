css_path = r'C:\Users\PC\.gemini\antigravity\scratch\unimaster-ai\static\style.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

v20_css = '''
/* =========================================================================
   UniMaster v20: Deep Color Customizer, Multi-Account & iOS/iPadOS Styles
   ========================================================================= */

:root {
  --opt-a-accent: #8b5cf6;
  --opt-b-accent: #3b82f6;
  --opt-c-accent: #10b981;
  --opt-d-accent: #f59e0b;
  --custom-q-text-color: var(--text-main);
}

.opt-A .opt-badge {
  border-color: var(--opt-a-accent) !important;
  color: var(--opt-a-accent) !important;
}
.opt-B .opt-badge {
  border-color: var(--opt-b-accent) !important;
  color: var(--opt-b-accent) !important;
}
.opt-C .opt-badge {
  border-color: var(--opt-c-accent) !important;
  color: var(--opt-c-accent) !important;
}
.opt-D .opt-badge {
  border-color: var(--opt-d-accent) !important;
  color: var(--opt-d-accent) !important;
}

.question-title-text {
  color: var(--custom-q-text-color, var(--text-main)) !important;
}

/* Fullscreen Distraction-Free Mode */
body.app-fullscreen-mode header {
  background: rgba(10, 15, 30, 0.98) !important;
  border-bottom-color: rgba(99, 102, 241, 0.35) !important;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
}
body.app-fullscreen-mode #header-fullscreen-btn {
  background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
  color: #ffffff !important;
  border-color: transparent !important;
}

/* Account Card Styles */
.acc-card {
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  border: 1.5px solid var(--border);
  background-color: var(--bg-surface);
}
.acc-card:hover {
  border-color: var(--brand);
  background-color: var(--bg-subtle);
}
.acc-card.is-active {
  border-color: #6366f1 !important;
  background: color-mix(in srgb, #6366f1 12%, var(--bg-surface)) !important;
  box-shadow: 0 4px 20px -4px rgba(99, 102, 241, 0.35);
}

/* Subject Checkbox Card */
.subj-checkbox-card {
  cursor: pointer;
  transition: all 0.18s ease;
  border: 1.5px solid var(--border);
  background-color: var(--bg-surface);
}
.subj-checkbox-card:hover {
  border-color: #6366f1;
  background-color: var(--bg-subtle);
}
.subj-checkbox-card.selected {
  border-color: #6366f1 !important;
  background-color: rgba(99, 102, 241, 0.12) !important;
}

/* Native iOS / iPadOS Safe Area & Touch Optimizations */
@supports (-webkit-touch-callout: none) {
  body {
    -webkit-user-select: none;
    -webkit-tap-highlight-color: transparent;
  }
  input, textarea {
    -webkit-user-select: text;
  }
}

/* iPad Portrait & Landscape Fine-tuning (768px - 1024px) */
@media (min-width: 768px) and (max-width: 1024px) {
  .uni-card {
    border-radius: 1.25rem !important;
  }
  #exam-question-stage {
    padding: 1.5rem !important;
  }
  .option-row {
    padding: 1.1rem 1.35rem !important;
    font-size: 1.05rem !important;
  }
}

/* iPhone Screen Notch & Home Indicator Guard */
@media (max-width: 639px) {
  #floating-tutor-container:not(.tutor-expanded-parent) {
    bottom: calc(5rem + env(safe-area-inset-bottom, 12px)) !important;
    right: max(0.75rem, env(safe-area-inset-right, 0.75rem)) !important;
  }
  .mobile-bottom-nav {
    padding-bottom: max(0.6rem, env(safe-area-inset-bottom, 16px)) !important;
  }
}
'''

if 'UniMaster v20' not in css:
    css += '\n' + v20_css
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(css)
    print("Added v20 styles to static/style.css successfully!")
else:
    print("v20 styles already present")
