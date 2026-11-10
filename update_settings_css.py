import os, re

# =========================================================================
# 1. UPDATE static/style.css
# =========================================================================
css_path = r'C:\Users\PC\.gemini\antigravity\scratch\unimaster-ai\static\style.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

settings_css = """
/* ==========================================================================
   MODAL SETTINGS & ULTRA-RICH CUSTOMIZATION SUITE
   ========================================================================== */
#modal-settings .uni-card {
  width: min(920px, 96vw) !important;
  max-width: 920px !important;
  height: min(88vh, 850px) !important;
  max-height: 88vh !important;
  border-radius: var(--card-radius, 1.25rem) !important;
}

.settings-tab-btn {
  background: transparent;
  color: var(--text-muted);
  border: 1px solid transparent;
  cursor: pointer;
  user-select: none;
  font-weight: 700;
  white-space: nowrap;
}
.settings-tab-btn:hover {
  color: var(--text-main);
  background: var(--bg-hover);
  border-color: var(--border);
}
.settings-tab-btn.active {
  background: linear-gradient(135deg, var(--brand), var(--brand-2)) !important;
  color: #ffffff !important;
  font-weight: 800 !important;
  box-shadow: 0 4px 14px -3px var(--brand-glow) !important;
  border-color: transparent !important;
}

/* Modern Range Slider Styling */
.range-slider-modern {
  -webkit-appearance: none;
  appearance: none;
  width: 100%;
  height: 6px;
  background: var(--bg-hover);
  border-radius: 9999px;
  outline: none;
  cursor: pointer;
  transition: background 0.16s ease;
}
.range-slider-modern::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--brand), var(--brand-2));
  cursor: pointer;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.4), 0 0 8px var(--brand-glow);
  transition: transform 0.15s ease;
}
.range-slider-modern::-webkit-slider-thumb:hover {
  transform: scale(1.25);
}
.range-slider-modern::-moz-range-thumb {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--brand), var(--brand-2));
  cursor: pointer;
  border: none;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.4), 0 0 8px var(--brand-glow);
}
"""

if 'settings-tab-btn' not in css:
    css += '\n' + settings_css

# Ensure .uni-card uses var(--card-radius)
css = css.replace('border-radius: 1.25rem;\n  box-shadow: var(--card-shadow);', 'border-radius: var(--card-radius, 1.25rem);\n  box-shadow: var(--card-shadow);')
css = css.replace('line-height: 1.62;\n  letter-spacing: -0.006em;', 'line-height: var(--line-height-q, 1.62);\n  letter-spacing: -0.006em;')

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css)

print("Updated style.css with modal settings styles")
