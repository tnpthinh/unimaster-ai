# -*- coding: utf-8 -*-
with open('static/app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '<!-- Console Status Indicator -->' in l:
        btn_lines = [
            '              <!-- Fullscreen AI Console button -->\n',
            '              <div class="flex items-center gap-2">\n',
            '                <button type="button" onclick="openAiFullscreenForCurrentTab()" class="px-2.5 py-1 rounded bg-[#333333] hover:bg-[#444444] text-cyan-300 hover:text-white flex items-center gap-1.5 text-[11px] font-mono transition-colors shadow-sm" title="Mở rộng toàn màn hình phần AI trả lời">\n',
            '                  <span>⛶</span> Toàn Màn Hình AI\n',
            '                </button>\n'
        ]
        lines = lines[:i] + btn_lines + lines[i:]
        break

with open('static/app.js', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('Added Fullscreen AI Console button!')
